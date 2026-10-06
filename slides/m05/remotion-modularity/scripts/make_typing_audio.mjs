// npm run video:audio
// Writes the typing sound of the narrated video (out/video-public/typing.wav) from the same keystrokes the video shows, so that every key on the
// screen has its sound at the same frame. Recorded samples from sounds/ are used when they exist, otherwise the sound is synthesized
// (see scripts/lib/typing_sound.mjs). The space bar is silent unless --space-sound is given.
import fs from 'node:fs';
import path from 'node:path';
import {build} from 'esbuild';
import {createMixer, describeSamples, loadSamples} from './lib/typing_sound.mjs';

const root = path.resolve(import.meta.dirname, '..');
const outDir = path.join(root, 'out', 'video-public');
fs.mkdirSync(outDir, {recursive: true});

// the pure part of the video, bundled for node
const bundled = path.join(outDir, 'audio-entry.mjs');
await build({entryPoints: [path.join(root, 'src/video/audio-entry.ts')], bundle: true, platform: 'node', format: 'esm', outfile: bundled, logLevel: 'error'});
const {buildTimeline, reactionsOf, MOODS, FPS, narration, SKIP} = await import(`${bundled}?${Date.now()}`);
fs.rmSync(bundled);

// the stage marks, read from the slide files exactly as scripts/review.mjs does
const index = fs.readFileSync(path.join(root, 'src/slides/index.ts'), 'utf8');
const marks = [...index.matchAll(/\{n: (\d+), id: '([^']+)'/g)].map((m) => {
  const file = fs.readFileSync(path.join(root, `src/slides/S${String(Number(m[1])).padStart(2, '0')}.tsx`), 'utf8');
  return file.match(/export const marks = \[([\d,\s]+)\]/)[1].split(',').map((x) => Number(x.trim()));
});
// the words of the slides that the video moves into the chat (scripts/collect_prose.mjs)
const proseFile = path.join(root, 'src/video/prose.json');
const prose = fs.existsSync(proseFile) ? JSON.parse(fs.readFileSync(proseFile, 'utf8')) : {};
if (!fs.existsSync(proseFile)) console.log('no src/video/prose.json: run `npm run video:prose` first for the slide text in the chat');
const tl = buildTimeline(marks, narration, prose, SKIP);

// the introduction (narration[0]): the frames of the move into the band, listed here so that they can be looked at
if (tl.intro) console.log(`introduction: typed frames ${Math.round(tl.intro.from)}-${Math.round(tl.intro.typedEnd)}, the narrator moves up in frames ${tl.intro.transFrom}-${tl.intro.transTo} (the first slide starts at ${tl.slides[0]?.from})`);
// where the narrator reacts (src/video/moods.ts): listed here so that the frames can be looked at
for (const r of reactionsOf(tl, MOODS)) console.log(`reaction ${r.mood}: frames ${Math.round(r.from)}-${Math.round(r.to)} (${(r.from / FPS).toFixed(1)}s-${(r.to / FPS).toFixed(1)}s)`);

const samples = loadSamples(path.join(root, 'sounds'));
console.log(describeSamples(samples));
const mixer = createMixer(tl.total / FPS, samples);
const spaceSound = process.argv.includes('--space-sound');
for (const k of tl.keys) {
  if (k.kind === 'space' && !spaceSound) continue;
  mixer.key(k.frame / FPS, k.kind);
}
const peak = mixer.write(path.join(outDir, 'typing.wav'));

const typos = tl.bubbles.reduce((a, b) => a + b.keys.filter((e) => e.kind === 'back').length, 0);
console.log(`${tl.bubbles.length} bubbles, ${tl.keys.length} keystrokes (${typos} backspaces), ${tl.total} frames = ${(tl.total / FPS / 60).toFixed(1)} min`);
console.log(`wrote ${path.join(outDir, 'typing.wav')} (peak before normalising ${peak.toFixed(2)})`);
