// npm run build:single
// Builds the click-through deck as ONE html file with everything inside it (scripts, styles, fonts, the two pictures), so that it
// can be handed to students and opened from the file system, with no network. Writes out/m05-community-detection.html.
import fs from 'node:fs';
import path from 'node:path';
import react from '@vitejs/plugin-react';
import {build} from 'vite';

const root = path.resolve(import.meta.dirname, '..');
const tmp = path.join(root, 'out', 'single-tmp');
const target = path.join(root, 'out', 'm05-community-detection.html');

/** KaTeX and the font packages list woff2, woff and ttf; keep woff2 only (every current browser reads it), or the file triples in size. */
const woff2Only = {
  name: 'woff2-only',
  enforce: 'pre',
  transform(code, id) {
    if (!/\.css(\?|$)/.test(id) || !/katex|fontsource/.test(id)) return null;
    return code.replace(/,\s*url\([^)]*\.(?:woff|ttf)\)\s*format\(["'][^"']*["']\)/g, '');
  },
};

await build({
  configFile: false,
  root,
  logLevel: 'warn',
  plugins: [react(), woff2Only],
  resolve: {
    alias: {
      '@remotion/google-fonts/LibreBaskerville': path.join(root, 'src/single/fonts-baskerville.ts'),
      '@remotion/google-fonts/Caveat': path.join(root, 'src/single/fonts-caveat.ts'),
    },
  },
  build: {
    outDir: tmp,
    emptyOutDir: true,
    assetsInlineLimit: 1e9,
    cssCodeSplit: false,
    chunkSizeWarningLimit: 1e9,
    rollupOptions: {output: {inlineDynamicImports: true}},
  },
});

let html = fs.readFileSync(path.join(tmp, 'index.html'), 'utf8');
const read = (href) => fs.readFileSync(path.join(tmp, href.replace(/^\//, '')), 'utf8');
html = html.replace(/<link rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/g, (_, href) => `<style>${read(href)}</style>`);
html = html.replace(/<script type="module"[^>]*src="([^"]+)"[^>]*><\/script>/g, (_, src) => `<script type="module">${read(src).replace(/<\/script/gi, '<\\/script')}</script>`);
if (/(src|href)="\/assets\//.test(html)) throw new Error('build_single: something is still loaded from a separate file');
fs.writeFileSync(target, html);
fs.rmSync(tmp, {recursive: true, force: true});
console.log(`wrote ${target} (${(fs.statSync(target).size / 1e6).toFixed(2)} MB)`);
