import { config } from "../config";

export type LiveMessage = Record<string, unknown>;

export function liveWebSocketUrl(): string {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${proto}//${window.location.host}${config.wsPath}`;
}

export function connectSession(onMessage: (msg: LiveMessage) => void): WebSocket {
  const ws = new WebSocket(liveWebSocketUrl());
  ws.addEventListener("message", (ev) => {
    try {
      onMessage(JSON.parse(String(ev.data)) as LiveMessage);
    } catch {
      console.warn("live: non-JSON WebSocket frame");
    }
  });
  ws.addEventListener("open", () => {
    ws.send(JSON.stringify({ type: "ping", t_ms: Date.now() }));
  });
  return ws;
}
