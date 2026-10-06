// node scripts/frames.mjs S13-nodes-or-pairs 0,30,60 outdir
// Renders the given frames of one slide at half size, for looking at an animation between its stage ends.
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const [id, list, outDir] = process.argv.slice(2);
const root = path.resolve(import.meta.dirname, '..');
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.join(root, 'src/remotion-entry.ts')});
const composition = await selectComposition({serveUrl, id});
for (const f of list.split(',').map(Number)) {
  await renderStill({composition, serveUrl, frame: f, output: path.join(outDir, `${id}-f${String(f).padStart(3, '0')}.png`), scale: 0.5});
}
console.log('done');
