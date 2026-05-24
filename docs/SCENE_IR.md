# Scene IR — Specification & Live Motor Model

> **Scope:** `live` product repo (`Homelab/live/`).  
> **Companion:** `VISION.md` · parent research `$HOME/KpihX-Labs/𝛱/STATE_OF_THE_ART.md`  
> **Purpose:** Scene IR + live motor — fluid visuals without batch video or slide chains.

---

## 1. What Scene IR Is (and Is Not)

### 1.1 Definition

**Scene IR** is the **canonical semantic + spatial + temporal state** of an explanation. It is:

- The **mental diagram** made explicit (objects, relations, focus, invariants).
- The **contract** between brain modules (dialogue, pedagogy, renderer, conductor).
- **Continuously patchable** while the user speaks or interrupts.

Scene IR is **not**:

| Not IR | What people mistake for “live AI visuals” |
|--------|-------------------------------------------|
| A PNG / MP4 / GIF | Batch output (NotebookLM, “AI video”) |
| Raw Manim Python per turn | Slow compile; discrete scene jumps |
| A chat message with Markdown | Text-primary |
| A list of bullet slides | Static succession of images |
| Pixel latents from diffusion | Pretty but non-editable, drift-prone |

### 1.2 Analogy

```text
Human explaining at a whiteboard:
  • Persistent world: axes, curve, regions stay in space
  • Hands: micro-motion, point, circle, erase, redraw (continuous)
  • Voice: prosody locks attention to one part of the board
  • Mental model: “what exists” ≠ “what is drawn this frame”

Scene IR  = what exists + what matters pedagogically
Live Motor = hands + physics of motion (60 fps, no LLM per frame)
Conductor  = breath + rhythm tying voice to emphasis
```

---

## 2. Why Manim-on-the-fly and NotebookLM Fail Your Goal

| Approach | What happens | Why it feels “dead” |
|----------|--------------|---------------------|
| **Manim render loop** | Python → scene graph → partial movies → ffmpeg | Each change is a **job** (seconds). Motion is **pre-baked**, not reactive to the next word. |
| **LLM → Manim code → video** | New script per idea | **Discrete jumps**; no shared persistent coordinates; desync if TTS starts before render ends. |
| **NotebookLM / slide video** | LLM storyboard → image per beat → stitch | **No world persistence**; cross-fade between stills ≠ manipulating objects in space. |
| **Talking avatar only** | Lip-sync on a face | Hands move; **math does not** live in a manipulable space. |

**Your target:** a **persistent manipulable space** + **continuous motor layer** (like hands), not a **sequence of illustrations**.

Manim remains valuable as an **offline compiler** (export, YouTube, highest polish). It must **not** sit in the realtime feedback loop.

---

## 3. Scene IR — Layered Structure

Scene IR has **four layers**. Only layers 1–3 are LLM-written; layer 4 is **engine-owned**.

```text
┌─────────────────────────────────────────────────────────────┐
│ L4  MOTOR STATE (engine)     ← 60 fps, procedural, hidden   │
│     position, velocity, easing, idle noise, camera drift     │
├─────────────────────────────────────────────────────────────┤
│ L3  DISCOURSE BINDINGS       ← Conductor + pedagogy          │
│     focus_entity, stress_curve, subtitle_refs                │
├─────────────────────────────────────────────────────────────┤
│ L2  SEMANTIC SCENE GRAPH     ← LLM patches (slow, ~2–10 Hz) │
│     entities, relations, props, invariants                     │
├─────────────────────────────────────────────────────────────┤
│ L1  SESSION & PEDAGOGY META  ← course graph, learner model   │
│     lesson_id, move, prerequisites, difficulty               │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 Layer 1 — Session meta

```json
{
  "session_id": "uuid",
  "lesson_id": "integration_odyssey.act2_lebesgue",
  "pedagogy_move": "contrast_representations",
  "learner": {
    "known_concepts": ["riemann_integral", "measure_zero"],
    "confusion_tags": ["vertical_vs_horizontal_slice"]
  },
  "ir_version": 12,
  "coordinate_frame": "2d_cartesian_v1"
}
```

### 3.2 Layer 2 — Semantic scene graph (core)

**Entities** are typed nodes. **Relations** are edges. **Props** hold parameters the renderer understands.

```json
{
  "entities": [
    {
      "id": "axes_main",
      "type": "axis_pair",
      "props": {
        "x": { "label": "x", "range": [0, 1], "ticks": 5 },
        "y": { "label": "f(x)", "range": [0, 1.2], "ticks": 4 }
      },
      "style": { "opacity": 1.0, "layer": 0 }
    },
    {
      "id": "curve_f",
      "type": "function_plot",
      "props": {
        "expr": "dirichlet_indicator",
        "domain": [0, 1],
        "color": "accent_blue"
      },
      "style": { "stroke_width": 2, "layer": 1 }
    },
    {
      "id": "riemann_rects",
      "type": "riemann_sum",
      "props": {
        "partition": 20,
        "method": "upper",
        "attached_to": "curve_f"
      },
      "visible": true
    },
    {
      "id": "lebesgue_bands",
      "type": "horizontal_measure_bands",
      "props": {
        "levels": 8,
        "attached_to": "curve_f"
      },
      "visible": false
    },
    {
      "id": "gesture_pointer",
      "type": "spatial_pointer",
      "props": { "role": "teacher_hand_proxy" },
      "visible": true
    }
  ],
  "relations": [
    { "from": "riemann_rects", "to": "axes_main", "type": "anchored" },
    { "from": "lebesgue_bands", "to": "curve_f", "type": "derived_from" }
  ],
  "invariants": [
    {
      "id": "dirichlet_measure_zero",
      "statement": "mu(Q)=0 on [0,1]",
      "symbolic": "measure(Q)==0"
    }
  ],
  "focus_stack": ["riemann_rects"]
}
```

**Entity types (v0 catalog — extensible):**

| Type | Role |
|------|------|
| `axis_pair`, `polar_axes` | Coordinate scaffolding |
| `function_plot`, `parametric_curve` | Curves |
| `riemann_sum`, `horizontal_measure_bands` | Integration visuals |
| `vector`, `vector_field_sample` | Linear algebra |
| `region_fill`, `contour_level` | Sets, level sets |
| `equation_block` | LaTeX layout slot (linked to symbolic) |
| `label`, `brace`, `arrow_annotation` | Callouts |
| `spatial_pointer` | Proxy for “hand” — point, drag, circle |
| `camera` | Pan, zoom, orbit (2D/3D) |
| `group` | VGroup-equivalent |

Each type has a JSON Schema + **validator** (SymPy for `expr`, domain checks, etc.).

### 3.3 Layer 3 — Discourse bindings (Conductor-owned)

Links **speech timeline** to **semantic focus** without redrawing the world.

```json
{
  "utterance_plan_id": "utt_0042",
  "speech": {
    "text": "On coupe selon les ordonnées, pas les abscisses.",
    "phonemes_ref": "phoneme_align_0042",
    "duration_ms": 2800
  },
  "bindings": [
    {
      "t_start_ms": 0,
      "t_end_ms": 900,
      "focus": ["axes_main.y"],
      "motor_hint": "pulse_axis",
      "subtitle_id": "sub_042a"
    },
    {
      "t_start_ms": 900,
      "t_end_ms": 2800,
      "focus": ["lebesgue_bands"],
      "motor_hint": "reveal_horizontal",
      "subtitle_id": "sub_042b"
    }
  ],
  "beats": [
    {
      "t_ms": 900,
      "semantic_op": "patch",
      "patch_ref": "patches/reveal_lebesgue.json"
    }
  ]
}
```

**Beat** = one pedagogical intention (human: “now I switch gesture”).  
**Binding** = sub-interval within beat for prosody (human: “this word = this emphasis”).

### 3.4 Layer 4 — Motor state (renderer-owned, never LLM per frame)

```json
{
  "frame": 18442,
  "tau_ms": 307367,
  "entities_runtime": {
    "gesture_pointer": {
      "pos": [0.42, 0.71],
      "vel": [0.02, -0.01],
      "mode": "orbit_focus",
      "target": "lebesgue_bands"
    },
    "lebesgue_bands": {
      "reveal_progress": 0.73,
      "wobble": 0.02
    },
    "camera": {
      "zoom": 1.05,
      "pan": [-0.03, 0.0]
    }
  },
  "procedural": {
    "idle_energy": 0.4,
    "breath_phase": 2.71
  }
}
```

Layer 4 is computed by **interpolation + procedural rules** between beats — this is what creates **non-fade, always-alive** motion.

---

## 4. Operations: Patches, Not Rewrites

The LLM (or Pedagogy Engine) emits **RFC 6902 JSON Patch** or typed ops — never full scene replacement.

```json
{
  "patch_id": "reveal_lebesgue",
  "base_version": 11,
  "ops": [
    { "op": "replace", "path": "/entities/2/visible", "value": true },
    { "op": "replace", "path": "/entities/1/visible", "value": false },
    { "op": "replace", "path": "/focus_stack", "value": ["lebesgue_bands"] },
    {
      "op": "add",
      "path": "/bindings/-",
      "value": {
        "utterance_plan_id": "utt_0042",
        "motor_program": "crossfade_horizontal_emphasis",
        "duration_ms": 1200
      }
    }
  ]
}
```

**Typed semantic ops (safer than raw JSON Patch):**

| Op | Effect |
|----|--------|
| `set_focus` | Change attention stack |
| `show` / `hide` | Visibility |
| `morph_entity` | `from` props → `to` props over `duration_ms` (compiler picks easing) |
| `attach_pointer` | Hand proxy tracks entity |
| `camera_move` | Zoom/pan program |
| `assert_invariant` | Pedagogy check; block if violated |
| `branch_scene` | Save checkpoint; learner question → sub-scene |

On **user interrupt**, Conductor **freezes** motor at current Layer 4, applies new patch from `base_version` or fork.

---

## 5. The Live Motor — How Fluidity Actually Works

### 5.1 Two clocks (fundamental)

| Clock | Rate | Owner | Purpose |
|-------|------|-------|---------|
| **Semantic clock** | 0.5–5 Hz | LLM + Pedagogy | Change *what* the scene means |
| **Motor clock** | 30–60 Hz | WebGL/SVG engine | Change *how* it moves |

Humans use both: you don’t redesign the integral every 16 ms; you **continuously move** while the concept stays stable.

```text
     Semantic beats:    ●────────●────────●────────●
                        │ morph  │ focus  │ branch │
     Motor frames:      │|||||||||||||||||||||||||||│
                        continuous interpolation + idle
```

### 5.2 Motor programs (not LLM)

Pre-authored **motor programs** map semantic ops → curves:

| Program | Visual effect |
|---------|----------------|
| `pulse_axis` | Subtle thickness + glow oscillation |
| `reveal_horizontal` | Bands slide in + pointer traces y-level |
| `orbit_focus` | Camera + pointer circulate focus region |
| `idle_breathe` | Global 1–2% scale oscillation when “listening” |
| `stress_shake` | Micro-shake on error / surprise |
| `morph_riemann_to_lebesgue` | Rect widths → horizontal strips (2–3 s ease) |

These are **code** (easing functions, spring physics, Perlin drift) — like game animation blend trees.

### 5.3 “Hand in space” without a human avatar

`spatial_pointer` entity:

- Points, drags, circles regions, “pushes” labels.
- Driven by **focus_stack** + **prosody energy** from audio RMS/phoneme stress.
- Optional: 2D rigged hand sprite **or** abstract cursor (Apple-style glow).

This delivers **gesture accompaniment** on the **lesson objects**, which is stronger for math than a talking head.

### 5.4 Latency budget (achievable)

| Stage | Target | Tech |
|-------|--------|------|
| ASR partial | 100–300 ms | streaming Whisper |
| Intent + patch | 200–600 ms | small local LLM / cached moves |
| Patch validate | 5–20 ms | JSON Schema + SymPy |
| Motor start | **<50 ms** | already-running WebGL loop |
| Visible change | **<800 ms** from end of user phrase | beat + program start |
| Full morph | 1–3 s | interpolated, **synced to TTS** via Conductor |

TTS starts **after** beat schedule is fixed for that clause — fixes desync.

---

## 6. Renderer Strategy (Live vs Polish)

```text
                    ┌─────────────────┐
  Scene IR ────────►│  LIVE RENDERER   │──► WebSocket stream
  (L2–L3)           │  Three.js / Pixi │    60 fps parametric
                    │  or D3 + Canvas  │
                    └────────┬────────┘
                             │ snapshot @ keyframes
                             ▼
                    ┌─────────────────┐
                    │ POLISH COMPILER  │──► MP4 / social
                    │ Manim (async)    │
                    └─────────────────┘
```

| Path | When | Output |
|------|------|--------|
| **Live** | Dialogue, Socratic session | Continuous scene state stream |
| **Polish** | Export, replay, YouTube | Manim from same IR |

Same IR → two compilers. **Never** block live on Manim.

---

## 7. Path A — Compose Existing Bricks (Recommended v1)

No new foundation model required for MVP.

| Brick | Role |
|-------|------|
| **Scene IR store** | Redis/Postgres + version chain |
| **Validators** | JSON Schema, SymPy, custom |
| **Pedagogy FSM** | Tutorly/CogApp-style moves → allowed patches |
| **Dialogue** | Qwen2.5-Omni / Gemini Live → tool `apply_patch` |
| **Conductor** | Python asyncio timeline + phoneme aligner |
| **Live renderer** | Three.js + KaTeX textures + custom shaders |
| **Motor library** | TS/Python easing catalog |
| **TTS** | Kokoro / Piper with **scheduled** start times |
| **Optional JEPA** | Learner surprise → trigger `branch_scene` |

**MVP flow:**

1. User speaks → partial transcript.  
2. Pedagogy picks move → template patch (often **cached**, not full LLM).  
3. Conductor schedules beat + TTS + motor program.  
4. Client already at 60 fps; patch arrives → morph begins **this frame**.  
5. LLM only refines if user asks off-script question.

### 7.1 Why this can feel “evolved” vs human hands

Humans manipulate **objects in shared space**. You replicate that with:

- **Persistence** (entities stay in IR)  
- **Continuous motor** (Layer 4 always running)  
- **Pointer + camera** as gesture proxies  
- **Prosody-driven energy** (louder syllable → pulse amplitude)

Not with more **images per minute**.

---

## 8. Path B — New Model Type (Research / v2+)

If you invest in a **fundamental** bet, train **small specialized models** on **Scene IR trajectories**, not pixels.

### 8.1 Scene-State World Model (SS-WM)

```text
Input:  IR_t, audio_features_t, learner_state
Output: IR_{t+1} distribution (patch ops), surprise score
```

- Architecture: JEPA / LeWM-style on **graph embeddings** of IR (not pixels).  
- Learns: “when teacher voice rises, which `focus` changes next?”  
- Does **not** render; Conductor + Motor still execute.

### 8.2 Motor Policy Network (MPN)

```text
Input:  IR focus, phoneme, beat_phase
Output: motor parameters (velocity, easing_id, pointer path)
```

- Imitation learning from **recorded human whiteboard sessions** (if collected) or synthetic prosody rules.  
- 1–10M params; runs at 60 Hz on GPU/CPU.  
- This is your “hands model” without generating video.

### 8.3 Latent motion diffusion (usually **not** worth it v1)

Diffusion in pixel space for **live** math = latency + errors.  
If used at all: only for **hero textures** (background style), not lesson logic.

### 8.4 When to choose Path B

| Signal | Action |
|--------|--------|
| Brick path hits 60 fps + good pedagogy but motion feels robotic | Add MPN |
| Branching dialogue hard to script | Add SS-WM |
| Enough logged sessions (IR + audio + outcomes) | Train SS-WM |

---

## 9. Anti-Patterns (Explicit)

| Anti-pattern | Why |
|--------------|-----|
| LLM generates 10 PNGs per answer | Slide deck; no manipulation |
| Play MP4 while TTS runs | Desync; no interrupt |
| Rebuild entire Manim scene per question | Seconds latency |
| Single omni model outputs “video tokens” | No editability; math wrong |
| No Layer 4 motor | “Fade” between static states |
| TTS before Conductor schedule | Classic desync |

---

## 10. Minimal v0.1 Schema Files (Next Step)

```text
live/schemas/         # JSON Schema for IR
live/brain/           # conductor, orchestrator, gate, tools
live/renderers/       # live_web + async export (Manim, PDF, …)
live/web/             # immersive single-page client
```

---

## 11. One-Sentence Product Definition

> **Project 𝛱 Dynamic** is a system where the teacher’s **voice** and a **persistent manipulable visual world** stay locked on one clock, with **semantic changes** planned slowly and **motion** generated continuously — filling the gap between mental spatial explanation and what a whiteboard can do.

---

*See also: `VISION.md` · `ARCHITECTURE.md` · `../STATE_OF_THE_ART.md`*
