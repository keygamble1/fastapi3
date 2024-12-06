import { svelte } from '@sveltejs/vite-plugin-svelte'
import { defineConfig } from 'vite'
import svgr from 'vite-plugin-svgr'
// https://vite.dev/config/
export default defineConfig({

  plugins: [svelte()],

  plugins: [

    svelte(),
    svgr()],
    

})
