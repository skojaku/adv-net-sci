// node scripts/line_lengths.mjs: how long the typed lines of the video are (the font size must let the longest one fit in the width of the lines, see Narrator.tsx)
import fs from 'node:fs';
import path from 'node:path';
import {build} from 'esbuild';

const root = path.resolve(import.meta.dirname, '..');
const outDir = path.join(root, 'out', 'video-public');
fs.mkdirSync(outDir, {recursive: true});
const bundled = path.join(outDir, '_lengths.mjs');
await build({entryPoints: [path.join(root, 'src/video/audio-entry.ts')], bundle: true, platform: 'node', format: 'esm', outfile: bundled, logLevel: 'error'});
const {buildTimeline, narration, SKIP} = await import(`${bundled}?${Date.now()}`);
fs.rmSync(bundled);
const index = fs.readFileSync(path.join(root, 'src/slides/index.ts'), 'utf8');
const marks = [...index.matchAll(/\{n: (\d+), id: '([^']+)'/g)].map((m) => {
  const file = fs.readFileSync(path.join(root, `src/slides/S${String(Number(m[1])).padStart(2, '0')}.tsx`), 'utf8');
  return file.match(/export const marks = \[([\d,\s]+)\]/)[1].split(',').map((x) => Number(x.trim()));
});
const prose = JSON.parse(fs.readFileSync(path.join(root, 'src/video/prose.json'), 'utf8'));
const tl = buildTimeline(marks, narration, prose, SKIP);
const lens = tl.bubbles.map((b) => b.text.length);
const hist = {};
for (const l of lens) hist[Math.floor(l / 5) * 5] = (hist[Math.floor(l / 5) * 5] || 0) + 1;
console.log('lines', lens.length, 'longest', Math.max(...lens), 'characters; histogram by 5:', JSON.stringify(hist));
const longest = tl.bubbles.reduce((a, b) => (b.text.length > a.text.length ? b : a));
console.log(`longest: S${longest.slide}.${longest.stage + 1} typed by frame ${Math.round(longest.typedEnd)}: ${longest.text}`);
for (const th of [54, 58, 60, 62]) console.log(`> ${th}:`, tl.bubbles.filter((b) => b.text.length > th).map((b) => `S${b.slide}.${b.stage + 1} (${b.text.length}) ${b.text}`).join(' | ') || 'none');
