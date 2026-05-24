# live — Architecture (Path A)

> **Path B** (learned SS-WM / motor policy) attaches later to the same IR — see `SCENE_IR.md` §8.

## Stack overview

```text
                         ┌────────────── web/ ──────────────┐
                         │  fullscreen canvas + presence    │
                         │  WebSocket client                │
                         └───────────────┬──────────────────┘
                                         │  /ws  /api
┌────────────────────────────────────────┴────────────────────────────────────────┐
│                              brain/ (FastAPI + uv)                             │
│  ┌─────────┐   ┌──────────────┐   ┌────────────┐   ┌─────────────────────────┐ │
│  │  Gate   │──►│ Orchestrator │──►│ Conductor  │──►│ Tool plane              │ │
│  └─────────┘   └──────────────┘   └────────────┘   └─────────────────────────┘ │
│                       │                   │                                      │
│                       ▼                   ▼                                      │
│                 Scene IR store      live renderer (WebGL client)               │
└──────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
    redis (session IR + conductor clock)
```

## Modules

| Module | Path | Job |
|--------|------|-----|
| **Gate** | `brain/.../gate/` | Addressed? Ambiguous? Background filter |
| **Orchestrator** | `brain/.../orchestrator/` | Mistral + tools → structured plans |
| **Conductor** | `brain/.../conductor/` | Single timeline: TTS, beats, subtitles |
| **Tools** | `brain/.../tools/` | search, files, patch_scene, export, presence |
| **Web client** | `web/` | One route `/`, no chrome |

## LLM (v1)

| Piece | Choice |
|-------|--------|
| Provider | **Mistral API** (`MISTRAL_API_KEY`) |
| Integration | Native `httpx` — **no** LangChain / Crew / Dify |
| Model | `mistral-small-latest` (configurable) |

## Homelab deploy

| Service | Role |
|---------|------|
| `live-web` | nginx — static + reverse proxy `/api` `/ws` → brain |
| `live-brain` | FastAPI on internal network |
| `live-redis` | Session + IR patches |

Public URL: **`https://live.kpihx-labs.com`** (Traefik → `live-web` only).

## Phased delivery

| Phase | Deliverable |
|-------|-------------|
| **P0** | Health + fullscreen placeholder + WSS echo |
| **P1** | Gate + Clarifier + scripted conductor |
| **P2** | Orchestrator + search → IR cards |
| **P3** | Presence face + retreat layout |
| **P4** | User files + upload overlay |
| **P5** | Voice exports + session memory |
| **P6** | Subject adapters |

## Related research

Parent strategy & SOTA survey: `$HOME/KpihX-Labs/𝛱/STATE_OF_THE_ART.md` (not deployed).
