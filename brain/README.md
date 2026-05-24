# live-brain

FastAPI service: session WebSocket, health, future gate / orchestrator / conductor.

```bash
uv sync --group dev
uv run live-brain
# or: uv run uvicorn live_brain.main:app --reload --host 0.0.0.0 --port 8000
```

Config: `src/live_brain/config.yaml` + env (see repo `.env.example`).
