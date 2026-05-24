import "./styles.css";
import { config } from "./config";
import { connectSession } from "./ws/client";

const root = document.querySelector<HTMLDivElement>("#app");
if (!root) throw new Error("missing #app");

root.innerHTML = `
  <canvas id="stage" aria-label="${config.appName} immersive surface"></canvas>
  <div id="status" role="status"></div>
`;

const stage = document.querySelector<HTMLCanvasElement>("#stage");
const status = document.querySelector<HTMLDivElement>("#status");
if (!stage || !status) throw new Error("missing stage elements");
const canvas: HTMLCanvasElement = stage;

function resize(): void {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const g = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
  g.addColorStop(0, "#0b1020");
  g.addColorStop(1, "#141c33");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(255,255,255,0.08)";
  ctx.font = "16px system-ui, sans-serif";
  ctx.fillText("live — P0 surface (presence + Scene IR next)", 24, 40);
}

window.addEventListener("resize", resize);
resize();

connectSession((msg) => {
  if (msg.type === "pong") {
    status.textContent = `connected · pong @ ${String(msg.t_ms)}`;
  }
});

fetch(config.healthPath)
  .then((r) => r.json())
  .then((body) => {
    status.textContent = `brain ${String((body as { status?: string }).status ?? "?")}`;
  })
  .catch(() => {
    status.textContent = "brain unreachable (start make dev-brain)";
  });
