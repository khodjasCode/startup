import { fileURLToPath, URL } from 'node:url'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Frontend build → web/frontend/dist, FastAPI (web/main.py) uni statik tarzda
// beradi. Dev rejimida `/api` so'rovlari uvicorn'ga (127.0.0.1:8000) proksilanadi,
// shuning uchun ikkala serverni parallel ishlatish kifoya:
//   uvicorn web.main:app --reload      (repo ildizidan)
//   npm run dev                        (web/frontend ichidan)
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@app': fileURLToPath(new URL('./src/app', import.meta.url)),
      '@pages': fileURLToPath(new URL('./src/pages', import.meta.url)),
      '@features': fileURLToPath(new URL('./src/features', import.meta.url)),
      '@shared': fileURLToPath(new URL('./src/shared', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // Soat uchun WebSocket.
      '/ws': {
        target: 'ws://127.0.0.1:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
  },
})
