import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'; // <-- Fixed plugin package name
import tailwindcss from '@tailwindcss/vite';

// https://vite.dev
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
});
