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
const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;');

// Group the cards by slide, so a slide's stages sit together.
const bySlide = new Map();
for (const c of cards) {
  const n = Number(c.label.split('-')[0]);
  if (!bySlide.has(n)) bySlide.set(n, []);
  bySlide.get(n).push(c);
}

const styles = `
:root{--bg:#ffffff;--fg:#14161c;--soft:#5d6270;--rule:#d9dce4;--accent:#3959A6;--card:#f4f5f9}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12141a;--fg:#e9ebf1;--soft:#a2a8b8;--rule:#2b2f3b;--accent:#9db3ee;--card:#1b1e27;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#12141a;--fg:#e9ebf1;--soft:#a2a8b8;--rule:#2b2f3b;--accent:#9db3ee;--card:#1b1e27;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;padding-inline:16px;padding-block:24px}
main{max-width:1440px;margin:0 auto}
h1{font-size:26px;margin:0 0 6px;letter-spacing:-0.01em}
p.lead{margin:0 0 28px;color:var(--soft);max-width:70ch}
section{margin:0 0 36px}
h2{font-size:19px;margin:0 0 12px;display:flex;gap:12px;align-items:baseline;border-bottom:1px solid var(--rule);padding-bottom:6px}
h2 .n{color:var(--accent);font-variant-numeric:tabular-nums;min-width:2.2ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:18px}
figure{margin:0;min-width:0}
figure img{width:100%;height:auto;display:block;border:1px solid var(--rule);background:#fff}
figcaption{margin-top:6px;font-size:14px;color:var(--soft);font-variant-numeric:tabular-nums}
figcaption b{color:var(--fg);font-size:16px;margin-right:6px}
`;

const body = (src) => `<main>
<h1>M05 slide review${esc(version)}</h1>
<p class="lead">One card per stage: the picture left on screen when the stage ends. The card number is slide-stage, for example 4-2 is the second stage of slide 4. Motion is not shown here.</p>
${[...bySlide.entries()].map(([n, cs]) => `<section id="s${n}"><h2><span class="n">${n}</span><span>${esc(cs[0].title)}</span></h2><div class="grid">
${cs.map((c) => `<figure id="c${c.label}"><img loading="lazy" src="${src(c)}" alt="Slide ${c.label}"><figcaption><b>${c.label}</b>frame ${c.frame}</figcaption></figure>`).join('\n')}
</div></section>`).join('\n')}
</main>`;

// Local page: a complete document, with image files next to it.
fs.writeFileSync(
  path.join(out, 'index.html'),
  `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>M05 slide review</title><style>${styles}</style></head><body>${body((c) => `${c.base}.png`)}</body></html>`,
);
// Page to publish: a fragment (the host supplies the document), pictures inline at half size.
fs.writeFileSync(
  path.join(out, 'artifact.html'),
  `<title>M05 Slide Review</title><style>${styles}</style>${body((c) => `data:image/jpeg;base64,${fs.readFileSync(path.join(out, `${c.base}.jpg`)).toString('base64')}`)}`,
);
console.log('wrote', path.join(out, 'index.html'), 'and artifact.html,', cards.length, 'cards');
