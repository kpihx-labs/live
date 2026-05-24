from fastapi.testclient import TestClient

from live_brain.main import app


def test_websocket_ping_pong() -> None:
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.send_json({"type": "ping", "t_ms": 42})
        data = ws.receive_json()
        assert data == {"type": "pong", "t_ms": 42}
