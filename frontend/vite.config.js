import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { readFileSync } from 'fs'
import { resolve } from 'path'

// Läs versionsnummer från package.json
const packageJson = JSON.parse(readFileSync(resolve(__dirname, 'package.json'), 'utf-8'))

export default defineConfig(({ mode }) => {
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    build: {
      outDir: 'dist',
      sourcemap: mode === 'development',
      rollupOptions: {
        // Extra Rollup build inställningar
      }
    },
    define: {
      __APP_VERSION__: JSON.stringify(packageJson.version),
    },
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: process.env.VITE_API_BASE_URL,
          changeOrigin: true,
        }
      },
      watch: {
        usePolling: true,
      }
    }
  };
});
