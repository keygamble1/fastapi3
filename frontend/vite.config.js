import { svelte } from '@sveltejs/vite-plugin-svelte'
import { defineConfig } from 'vite'
import svgr from 'vite-plugin-svgr'
// https://vite.dev/config/
export default defineConfig({
<<<<<<< HEAD
  plugins: [svelte()],
=======
  plugins: [

    svelte(),
    svgr()],
    
>>>>>>> 4c47fd13265df3d3025914658f70ac89a0357202
})
