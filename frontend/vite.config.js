import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  server: {
    proxy: {
      '/login': 'http://127.0.0.1:8080',
      '/register': 'http://127.0.0.1:8080',
      '/expenses': 'http://127.0.0.1:8080',
      '/income': 'http://127.0.0.1:8080',
      '/dashboard': 'http://127.0.0.1:8080',
      '/admin': 'http://127.0.0.1:8080',
      '/ai': 'http://127.0.0.1:8080',
      '/documents': 'http://127.0.0.1:8080',
      '/uploads': 'http://127.0.0.1:8080',
    },
  },
})