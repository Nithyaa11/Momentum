import path from 'node:path'

import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The backend runs on :8000. In Docker it's reachable as "backend", locally as localhost.
const API_TARGET = process.env.API_PROXY_TARGET ?? 'http://localhost:8000'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { '@': path.resolve(import.meta.dirname, 'src') },
  },
  server: {
    // /api/* and /health are forwarded to FastAPI, so the browser never deals with CORS
    proxy: {
      '/api': API_TARGET,
      '/health': API_TARGET,
    },
  },
})
