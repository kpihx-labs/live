# CONTRACT.md — live

> **Source of truth** for transports and payloads. Implementation must match; tests enforce drift.

---

## 1) Metadata

| Field | Value |
|-------|-------|
| `schema_version` | `live.contract.v1` |
| `contract_version` | `1.0.0` |

---

## 2) Conventions

- Time: milliseconds as `*_ms` (integers).
- IDs: `sess_*`, `req_*`, `beat_*`.
- JSON only on WebSocket; UTF-8.
- Errors: stable `code` string + human `message` (English).

---

## 3) HTTP (brain, proxied via web)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Liveness (`{"status":"ok","service":"live-brain"}`) |
| `GET` | `/api/health` | Same (nginx prefix) |

Future: `POST /api/session` — not in v1.0.0 scaffold.

---

## 4) WebSocket

| Item | Value |
|------|-------|
| URL (prod) | `wss://live.kpihx-labs.com/ws` |
| URL (local) | `ws://127.0.0.1:8000/ws` or via Vite proxy |
| Subprotocol | none (v1) |

### Client → server (v1 scaffold)

```json
{ "type": "ping", "t_ms": 0 }
```

### Server → client (v1 scaffold)

```json
{ "type": "pong", "t_ms": 0 }
```

### Planned (documented, not implemented in v1.0.0)

| `type` | Direction | Role |
|--------|-----------|------|
| `session.start` | S→C | Session id + presence mode |
| `scene.patch` | S→C | Scene IR JSON Patch |
| `presence.set` | S→C | Layout + expression |
| `audio.schedule` | S→C | Conductor timeline chunk |
| `user.utterance` | C→S | ASR final text |
| `interrupt` | C→S | Barge-in |

Full schemas → `schemas/` (JSON Schema, versioned).

---

## 5) Error model

| `code` | Meaning |
|--------|---------|
| `invalid_payload` | JSON/schema violation |
| `not_addressed` | Gate rejected (no reply) |
| `clarify` | Need user confirmation |
| `upstream_llm` | Mistral API failure |
| `internal` | Unexpected server error |

---

## 6) Compliance

- Wrappers (nginx, future MCP) must not remap error codes.
- Breaking wire changes → bump `schema_version` major.
- Scene IR semantics → `docs/SCENE_IR.md` wins for visual meaning.

---

## 7) Dev facet

| Command | Expectation |
|---------|-------------|
| `make check` | brain tests + web typecheck pass |
| `curl -fsS …/health` | `status` == `ok` |
| WSS ping | `pong` within 5s on scaffold |
