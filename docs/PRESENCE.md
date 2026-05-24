# Presence — The warm soul of 𝛱 Live

> **Reference:** `assets/references/copilot-voice-chat-reference.png` (Microsoft Copilot voice chat — layout inspiration, not a clone).  
> **Principle:** Content matters — but users stay for the **felt relationship**. Presence carries that.

---

## What presence is

Presence is the **named personality** you talk to: a small expressive face over a **personalized, always-moving background**.

It is **not** decoration on top of lessons.  
It is what makes the platform **convivial** before any diagram exists, between topics, and when you return.

```text
  ┌────────────────────────────────────────┐
  │  ambient field (your interests, motion) │
  │                                         │
  │         ╭───╮  ← face: eyes, mouth       │
  │         │ ◕ ◕│     audio-reactive       │
  │         ╰───╯                           │
  │                                         │
  │   (no lesson yet — this IS the screen)   │
  └────────────────────────────────────────┘
```

---

## Three visual layers (stacking)

| Layer | What | When |
|-------|------|------|
| **0 — Ambient field** | Slow motion gradients, subtle particles, mood from user profile (tech, culture, …) | Always |
| **1 — Presence face** | Soft blob / stylized 3D face; expressions; lip-sync | Default until lesson needs space |
| **2 — Lesson field** | Scene IR + live motor (diagrams, news, code, …) | When there is a **topic** to show |

Layer 1 and 2 **share** the screen — they do not replace the soul with cold slides.

---

## Modes (layout manager)

```text
     WELCOME          DIALOGUE           LESSON            BETWEEN
   (arrival)      (no topic yet)    (topic active)      (topics)
        │                │                │                 │
        ▼                ▼                ▼                 ▼
   face center      face center      face corner       face center
   bg full          bg full          bg + IR field     bg calm
   "bonjour…"       listens/speaks   face retreats     recap optional
```

| Mode | Face | Background | Lesson IR |
|------|------|------------|-----------|
| `welcome` | Large, center | Profile motion | Hidden |
| `dialogue_open` | Large, center | Full ambient | None yet |
| `lesson_shared` | Small corner or side strip | Dimmed ambient + IR | Primary |
| `lesson_full` | Minimal glow / eyes only | IR full stage | User asked focus |
| `farewell` | Center, soft | Slow fade | Optional recap card |

**Retreat** means smaller and off-center — **not** disappearance. The agent stays **there**.

---

## Copilot reference (what we take from it)

From `copilot-voice-chat-reference.png`:

| Element | 𝛱 Live interpretation |
|---------|----------------------|
| Dark cosmic ambient | Personalized **ambient field** (not one global theme) |
| Glowing friendly blob | **Presence mesh** — simple features, inner light |
| No search / no feed | **Zero chrome** — controls appear only when agent invokes them |
| Mic-centric bottom bar | **Ephemeral** control strip — voice session only, not permanent nav |
| Palette icon (top) | Optional **voice-only** “change mood” — never a settings maze |

We add: **memory** (“we already talked about…”), **Scene IR** when topics need space, **clarification** culture, sovereign stack.

---

## Audio ↔ face (mandatory)

| Signal | Face |
|--------|------|
| Agent speaking | Mouth + subtle body pulse |
| User speaking | Listen expression (eyes on user) |
| Thinking / searching | Soft idle animation + ambient swirl |
| Clarifying | Curious tilt |
| Silence (not addressed) | Calm idle — **no random speech** |

Same **Conductor clock** as TTS — no desync between voice and expression.

---

## Relationship to Scene IR

```text
  User arrives
       → Presence + ambient only  (warmth, zero cognitive load)

  User names a topic
       → Orchestrator may search / plan
       → IR grows IN the field; face steps to corner

  User says "ok stop visuals" / new small talk
       → IR fades down; Presence returns center
```

Scene IR is the **explanation board**.  
Presence is **who** explains.

---

## Implementation notes (Path A)

| Piece | Suggestion |
|-------|------------|
| Render | WebGL: shader background + rigged face or 2.5D sprite |
| Assets | `live/assets/presence/` — meshes, expression map |
| State | `presence_mode` in session JSON; layout manager in `web/` |
| API | `set_presence(mode)` tool for orchestrator |

---

*See `VISION.md` · `ARCHITECTURE.md` · `SCENE_IR.md`*
