// https://nuxt.com/docs/api/configuration/nuxt-config
import { fileURLToPath } from 'node:url'
export default defineNuxtConfig({
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
      ]
    }
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@pinia/nuxt'],
  // Try using '@/' or a direct relative path './assets/...'
  // css: ['@/assets/css/main.css'],
  css: [fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url))
  ],  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
    },
  },
})