// node scripts/collect_prose.mjs
// Finds the sentences that each stage of each slide adds (the Box, Cap and Tag texts of five words or more with no formula in them: see
// src/components/Text.tsx), by rendering the slide at the end of every stage with ProseContext = 'collect' and reading what the page logs.
// Writes src/video/prose.json (committed, like src/data/data.ts; run it again whenever a slide's sentences change): { "<slide>": { "<stage>": ["sentence", ...] } }. The narrated video types these in the chat, in the order
// they stand on the slide (top to bottom, then left to right), and leaves them off the slide.
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const root = path.resolve(import.meta.dirname, '..');
const outDir = path.join(root, 'out', 'video-public');
fs.mkdirSync(outDir, {recursive: true});

const index = fs.readFileSync(path.join(root, 'src/slides/index.ts'), 'utf8');
const slides = [...index.matchAll(/\{n: (\d+), id: '([^']+)'/g)].map((m) => {
  const n = Number(m[1]);
  const file = fs.readFileSync(path.join(root, `src/slides/S${String(n).padStart(2, '0')}.tsx`), 'utf8');
  return {n, marks: file.match(/export const marks = \[([\d,\s]+)\]/)[1].split(',').map((x) => Number(x.trim()))};
});

const serveUrl = await bundle({entryPoint: path.join(root, 'src/video/entry.ts')});
const tmpPng = path.join(outDir, 'prose-tmp.png');
const prose = {};
let total = 0;
for (const s of slides) {
  const composition = await selectComposition({serveUrl, id: `Collect-S${String(s.n).padStart(2, '0')}`});
  let previous = new Set();
  for (let k = 0; k < s.marks.length; k++) {
    const items = [];
    await renderStill({
      composition,
      serveUrl,
      frame: s.marks[k],
      output: tmpPng,
      scale: 0.1,
      logLevel: 'error',
      onBrowserLog: (log) => {
        if (log.text.startsWith('PROSE ')) items.push(JSON.parse(log.text.slice(6)));
      },
    });
    const visible = [];
    for (const it of items.filter((i) => i.visible).sort((a, b) => a.y - b.y || a.x - b.x)) if (!visible.includes(it.text)) visible.push(it.text);
    const added = visible.filter((t) => !previous.has(t));
    if (added.length) {
      (prose[s.n] ??= {})[k] = added;
      total += added.length;
    }
    previous = new Set(visible);
  }
}
fs.rmSync(tmpPng, {force: true});
fs.writeFileSync(path.join(root, 'src/video/prose.json'), JSON.stringify(prose, null, 1) + '\n');
console.log(`${total} sentences on ${Object.keys(prose).length} slides -> src/video/prose.json`);
