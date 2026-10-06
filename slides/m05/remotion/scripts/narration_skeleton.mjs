// npm run video:skeleton            prints a skeleton of src/video/narration.ts for this deck
// node scripts/narration_skeleton.mjs --out=src/video/narration.ts      writes it; refuses if the file exists (unless it is the empty stub of scripts/port_video.mjs, or --force)
//
// For every slide and every stage of the deck: an empty list of lines to fill in, and, as a comment, the slide's own sentences of that stage (from
// src/video/prose.json, `npm run video:prose` first), which the video types in the chat before your lines (or where you write '@mirror').
// The slides that video.config.json skips are listed as comments only. How to write the lines: NARRATED_VIDEO_GUIDE.md, "Writing the narration".
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const arg = (name, fallback) => {
  const a = process.argv.find((x) => x.startsWith(`--${name}=`));
  return a ? a.slice(name.length + 3) : fallback;
};
const config = JSON.parse(fs.readFileSync(path.join(root, 'src/video/video.config.json'), 'utf8'));
const proseFile = path.join(root, 'src/video/prose.json');
const prose = fs.existsSync(proseFile) ? JSON.parse(fs.readFileSync(proseFile, 'utf8')) : {};
if (!fs.existsSync(proseFile)) console.error('no src/video/prose.json: run `npm run video:prose` first to see the slides\' own sentences');

const index = fs.readFileSync(path.join(root, 'src/slides/index.ts'), 'utf8');
const slides = [...index.matchAll(/\{n: (\d+), id: '([^']+)'/g)].map((m) => {
  const n = Number(m[1]);
  const file = fs.readFileSync(path.join(root, `src/slides/S${String(n).padStart(2, '0')}.tsx`), 'utf8');
  const marks = file.match(/export const marks = \[([\d,\s]+)\]/)[1].split(',').map((x) => Number(x.trim()));
  return {n, id: m[2], marks};
});

const lines = [];
lines.push("import type {Narration} from './timeline';");
lines.push('');
lines.push('/**');
lines.push(` * The narration of the ${config.id} video: narration[slide number][stage index (0 = the first)] = lines; each line is one bubble of the chat (at most 64 characters).`);
lines.push(" * The slide's own sentences are typed first, from prose.json (shown below as comments); the lines here ADD to them (why, how to read the picture, what to compare).");
lines.push(" * '@mirror' puts the slide's sentences somewhere else in the stage. Rules and examples: slides/NARRATED_VIDEO_GUIDE.md, \"Writing the narration\".");
lines.push(' */');
lines.push('export const narration: Narration = {');
lines.push('  // 0 = the introduction: a greeting and what the module covers, typed with the title (video.config.json, intro) on screen and the narrator in the middle of the screen; [] for none');
lines.push('  0: {0: []},');
for (const s of slides) {
  if (config.skip.includes(s.n)) {
    lines.push(`  // S${s.n} ${s.id}: left out of the video (skip in video.config.json)`);
    continue;
  }
  lines.push(`  ${s.n}: {`);
  lines.push(`    // ${s.id}: ${s.marks.length} stage${s.marks.length === 1 ? '' : 's'}`);
  s.marks.forEach((_, k) => {
    const words = prose[String(s.n)]?.[String(k)] ?? [];
    lines.push(`    ${k}: [], // ${words.length ? 'slide: ' + words.map((w) => JSON.stringify(w)).join(' | ') : 'no slide sentence'}`);
  });
  lines.push('  },');
}
lines.push('};');
lines.push('');
const text = lines.join('\n');

const STUB_MARK = 'stub: replace with `npm run video:skeleton`'; // scripts/port_video.mjs writes this into the empty narration.ts of a new project
const out = arg('out');
if (!out) {
  process.stdout.write(text);
} else {
  const target = path.resolve(root, out);
  const isStub = fs.existsSync(target) && fs.readFileSync(target, 'utf8').includes(STUB_MARK);
  if (fs.existsSync(target) && !isStub && !process.argv.includes('--force')) {
    console.error(`${out} exists: not overwritten (print to the terminal with no --out and merge by hand, or pass --force)`);
    process.exit(1);
  }
  fs.writeFileSync(target, text);
  console.log(`wrote ${out}: ${slides.length - config.skip.filter((n) => slides.some((s) => s.n === n)).length} slides, ${slides.filter((s) => !config.skip.includes(s.n)).reduce((a, s) => a + s.marks.length, 0)} stages`);
}
