import type { Config } from "@react-router/dev/config";

export default {
  appDirectory: "app",
  buildDirectory: "build",
  // SPA mode: no runtime server. The root route is pre-rendered at build time
  // into a single index.html that hydrates for any client-side path.
  ssr: false,
} satisfies Config;
