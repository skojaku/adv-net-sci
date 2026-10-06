// npm run video:sampler
// A listening test of all the Mechvibes keyboard packs: out/sound-packs.mp4 shows each pack's name and the same sentence typed with
// the same keystrokes, so that only the sound differs. Needs MechvibesDX installed (scripts/extract_mechvibes.mjs).
//   node scripts/make_sampler.mjs [--release=0.5] [--space-sound]
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {build} from 'esbuild';
import {createMixer, loadSamples} from './lib/typing_sound.mjs';

const root = path.resolve(import.meta.dirname, '..');
const outDir = path.join(root, 'out', 'video-public');
fs.mkdirSync(outDir, {recursive: true});
const arg = (name, fallback) => {
  const a = process.argv.find((x) => x.startsWith(`--${name}=`));
  return a ? a.slice(name.length + 3) : fallback;
};

const bundled = path.join(outDir, 'audio-entry.mjs');
await build({entryPoints: [path.join(root, 'src/video/audio-entry.ts')], bundle: true, platform: 'node', format: 'esm', outfile: bundled, logLevel: 'error'});
const {samplerTimeline, SAMPLER_PACKS} = await import(`${bundled}?${Date.now()}`);
fs.rmSync(bundled);
const tl = samplerTimeline();

const banks = SAMPLER_PACKS.map((p) => {
  const dir = path.join(root, 'out', 'sampler', p.id);
  execFileSync('node', [path.join(root, 'scripts/extract_mechvibes.mjs'), `--pack=${p.id}`, `--release=${arg('release', 0.5)}`, `--out=${dir}`], {cwd: root, stdio: 'ignore'});
  return loadSamples(dir);
});
const mixer = createMixer(tl.total / 30, banks[0]);
const spaceSound = process.argv.includes('--space-sound');
for (const k of tl.keys) {
  if (k.kind === 'space' && !spaceSound) continue;
  mixer.key(k.frame / 30, k.kind, banks[k.pack]);
}
mixer.write(path.join(outDir, 'sampler.wav'));
console.log(`${SAMPLER_PACKS.length} packs, ${tl.total} frames = ${(tl.total / 30).toFixed(0)} s -> out/video-public/sampler.wav`);
console.log('now: node scripts/render_video.mjs --id=M05-sampler --out=out/sound-packs.mp4');
