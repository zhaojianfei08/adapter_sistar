import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0', // 监听所有地址
    port: 5173 // 你想要监听的端口号
  },
  plugins: [vue()],
})
