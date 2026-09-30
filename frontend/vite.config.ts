import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [tailwindcss(), react(), reactRouter()],
  resolve: {
    tsconfigPaths: true,
  },
  server: {
    port: 4200,
  },
});
