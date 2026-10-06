// npm run video                       the whole video: out/m05-narrated.mp4
// node scripts/render_video.mjs --frames=0-400 --out=out/test.mp4      a part of it
// node scripts/render_video.mjs --still=120,900,3000 --dir=out/video-stills   single frames (png), for looking
// --id=M05-sampler renders the listening test of the keyboard packs (npm run video:sampler first).
// Needs out/video-public/typing.wav first (npm run video:audio).
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';

const root = path.resolve(import.meta.dirname, '..');
const arg = (name, fallback) => {
  const a = process.argv.find((x) => x.startsWith(`--${name}=`));
  return a ? a.slice(name.length + 3) : fallback;
};
const publicDir = path.join(root, 'out', 'video-public');
if (!fs.existsSync(path.join(publicDir, 'typing.wav')) && !fs.existsSync(path.join(publicDir, 'sampler.wav'))) throw new Error('run `npm run video:audio` (or `npm run video:sampler`) first');

const serveUrl = await bundle({entryPoint: path.join(root, 'src/video/entry.ts'), publicDir});
const id = arg('id', 'M05-narrated');
const composition = await selectComposition({serveUrl, id});
console.log(`${composition.durationInFrames} frames = ${(composition.durationInFrames / composition.fps / 60).toFixed(1)} min`);

const still = arg('still');
if (still) {
  const dir = path.resolve(root, arg('dir', 'out/video-stills'));
  fs.mkdirSync(dir, {recursive: true});
  for (const f of still.split(',').map(Number)) {
    await renderStill({composition, serveUrl, frame: f, output: path.join(dir, `f${String(f).padStart(5, '0')}.png`), scale: Number(arg('scale', 0.5))});
  }
  console.log('stills done');
} else {
  const range = arg('frames');
  const out = path.resolve(root, arg('out', 'out/m05-narrated.mp4'));
  fs.mkdirSync(path.dirname(out), {recursive: true});
  let lastPct = -1;
  await renderMedia({
    composition,
    serveUrl,
    codec: 'h264',
    audioCodec: 'aac',
    outputLocation: out,
    frameRange: range ? range.split('-').map(Number) : null,
    concurrency: Number(arg('concurrency', 12)),
    crf: 20,
    onProgress: ({progress}) => {
      const pct = Math.floor(progress * 20) * 5;
      if (pct !== lastPct) {
        lastPct = pct;
        console.log(`${pct}%`);
      }
    },
  });
  console.log(`wrote ${out} (${(fs.statSync(out).size / 1e6).toFixed(1)} MB)`);
}
