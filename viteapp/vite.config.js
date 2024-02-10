import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3080,
  },
  build: {
    // generate .vite/manifest.json in outDir
    manifest: true,
    outDir: "../static/viteapp"
  },

  // resolve: {
  //   alias: {
  //     '@': resolve(__dirname, 'out'), // resolve path
  //   },
  // },
  // rollupInputOptions: {
  //   input: resolve(__dirname, 'out/main.js') // custom main
  // }
})
