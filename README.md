# live

```text
   ╦  ╦┬┌┐┌┌─┐
   ║  ║││││├┤   Immersive voice-first agentic platform
   ╚═╝╩┘└┘└─┘   One page · zero chrome · Scene IR + presence
```

> **Public:** `https://live.kpihx-labs.com`  
> **Stack:** Bun + Vite + TypeScript (`web/`) · FastAPI + uv (`brain/`)

## What this is

A single full-screen web experience: you **speak**, the system **shows** (live visuals + warm presence), searches, uploads, and exports — without teaching you how the platform works.

| Doc | Content |
|-----|---------|
| [CONTRACT.md](CONTRACT.md) | HTTP + WebSocket contract (source of truth) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Modules, phases, deploy topology |
| [docs/VISION.md](docs/VISION.md) | Product contract |
| [docs/PRESENCE.md](docs/PRESENCE.md) | Face + ambient layer |
| [docs/SCENE_IR.md](docs/SCENE_IR.md) | Visual state IR + motor |
| [docs/LICENSING.md](docs/LICENSING.md) | License strategy (proprietary vs OSS) |
| [CHANGELOG.md](CHANGELOG.md) | Releases |
| [TODO.md](TODO.md) | Active backlog |

## Repository layout

```text
live/
├── brain/          FastAPI — gate, orchestrator, conductor, tools
├── web/            Vite client — canvas, presence, WebSocket
├── deploy/         Docker Compose + nginx (homelab)
├── schemas/        Scene IR JSON Schema (versioned)
├── docs/           Product & architecture specs
└── assets/         Reference images
```

## Quick start (local)

```bash
make init          # .env + docker-compose.override from examples
make dev-brain     # http://127.0.0.1:8000/health
make dev-web       # http://127.0.0.1:5173
make check         # brain tests + web typecheck
```

Secrets: `MISTRAL_API_KEY` via `bw-env` (see `.env.example`).

## Deploy

Homelab GitLab CI (`main` → `deploy_homelab`). Traefik host: `live.kpihx-labs.com` only.

```bash
make deploy        # docker compose in deploy/ (local smoke)
```

## License

**Proprietary — All Rights Reserved.** See [LICENSE](LICENSE) and [docs/LICENSING.md](docs/LICENSING.md).
