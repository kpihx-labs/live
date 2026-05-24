"""FastAPI application — health + WebSocket scaffold."""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from live_brain.config import get_settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title="live-brain",
    version="0.1.0",
    description="Immersive agentic platform — brain API",
)


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "live-brain"})


@app.websocket("/ws")
async def websocket_session(ws: WebSocket) -> None:
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            try:
                payload: dict[str, Any] = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json(
                    {
                        "type": "error",
                        "code": "invalid_payload",
                        "message": "Expected JSON object",
                    }
                )
                continue

            if payload.get("type") == "ping":
                await ws.send_json({"type": "pong", "t_ms": payload.get("t_ms", 0)})
            else:
                await ws.send_json(
                    {
                        "type": "error",
                        "code": "invalid_payload",
                        "message": f"Unknown type: {payload.get('type')!r}",
                    }
                )
    except WebSocketDisconnect:
        logger.debug("WebSocket disconnected")


def run() -> None:
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "live_brain.main:app",
        host=settings.http_host,
        port=settings.http_port,
        reload=False,
    )


if __name__ == "__main__":
    run()
