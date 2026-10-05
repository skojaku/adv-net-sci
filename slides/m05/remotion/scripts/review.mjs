// npm run review
// Renders a still at the end of every stage of every slide, and writes
//   out/review/index.html     the stills side by side, to open locally (full size)
//   out/review/artifact.html  the same, self-contained at half size, to publish
// Card numbers are <slide>-<stage>, e.g. 4-2 is the second stage of slide 4 (stages count from 1).
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'out', 'review');
fs.mkdirSync(out, {recursive: true});

const index = fs.readFileSync(path.join(root, 'src/slides/index.ts'), 'utf8');
const slides = [...index.matchAll(/\{n: (\d+), id: '([^']+)'/g)].map((m) => {
  const n = Number(m[1]);
  const file = fs.readFileSync(path.join(root, `src/slides/S${String(n).padStart(2, '0')}.tsx`), 'utf8');
  const marks = file.match(/export const marks = \[([\d,\s]+)\]/)[1].split(',').map((x) => Number(x.trim()));
  return {n, id: m[2], marks, title: (file.match(/title="([^"]+)"/) || file.match(/title: ?'([^']+)'/) || [])[1] ?? ''};
});

const serveUrl = await bundle({entryPoint: path.join(root, 'src/remotion-entry.ts')});
const cards = [];
for (const s of slides) {
  const id = `S${String(s.n).padStart(2, '0')}-${s.id}`;
  const composition = await selectComposition({serveUrl, id});
  for (let k = 0; k < s.marks.length; k++) {
    const base = `S${String(s.n).padStart(2, '0')}-s${k + 1}`;
    await renderStill({composition, serveUrl, frame: s.marks[k], output: path.join(out, `${base}.png`)});
    await renderStill({
      composition, serveUrl, frame: s.marks[k], output: path.join(out, `${base}.jpg`),
      imageFormat: 'jpeg', jpegQuality: 78, scale: 0.5,
    });
    cards.push({label: `${s.n}-${k + 1}`, title: s.title, base, frame: s.marks[k]});
  }
  console.log(`${id}: ${s.marks.length} stage(s)`);
}

const version = process.env.REVIEW_VERSION ? ` ${process.env.REVIEW_VERSION}` : '';
const page = (src) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>M05 slides review${version}</title>
<style>
:root{--bg:#fff;--fg:#111;--soft:#6b6b6b;--rule:#ddd}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141414;--fg:#eee;--soft:#aaa;--rule:#333}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.4 system-ui,sans-serif}
main{max-width:1500px;margin:0 auto;padding:24px 16px}
h1{font-size:24px;margin:0 0 4px}p.note{color:var(--soft);margin:0 0 24px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:20px}
figure{margin:0}figure img{width:100%;display:block;border:1px solid var(--rule)}
figcaption{margin-top:6px;font-size:15px}figcaption b{font-size:18px}figcaption span{color:var(--soft)}
</style></head><body><main>
<h1>M05 animated slides${version}</h1>
<p class="note">One card per stage, the picture left on screen when the stage ends. Card number = slide-stage. Motion is not shown here.</p>
<div class="grid">
${cards.map((c) => `<figure id="c${c.label}"><img loading="lazy" src="${src(c)}" alt="${c.label}"><figcaption><b>${c.label}</b> <span>${c.title.replace(/&/g, '&amp;').replace(/</g, '&lt;')} · frame ${c.frame}</span></figcaption></figure>`).join('\n')}
</div></main></body></html>`;

fs.writeFileSync(path.join(out, 'index.html'), page((c) => `${c.base}.png`));
fs.writeFileSync(
  path.join(out, 'artifact.html'),
  page((c) => `data:image/jpeg;base64,${fs.readFileSync(path.join(out, `${c.base}.jpg`)).toString('base64')}`),
);
console.log('wrote', path.join(out, 'index.html'), 'and artifact.html,', cards.length, 'cards');
