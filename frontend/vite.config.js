import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // While running "npm run dev", questions are passed on to the Python backend.
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
});
