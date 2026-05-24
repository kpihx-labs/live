/** Client runtime config — build-time defaults; override via import.meta.env in Vite. */

export const config = {
  wsPath: "/ws",
  healthPath: "/api/health",
  appName: "live",
} as const;
