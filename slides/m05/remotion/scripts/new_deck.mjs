// node scripts/new_deck.mjs <new project dir> --name=m05-modularity --ids=club,count,... [--video-id=M05MOD --out=x.mp4 --skip=1,8 --kicker=.. --title=.. --subtitle=..]
//
// Starts a new Remotion click-through deck (and, with --video-id, its narrated video) from the shared parts of this project (Module 05).
// Run it from slides/m05/remotion. It copies what every deck shares, writes one stub slide per id (S01.tsx ...), src/slides/index.ts and TOTAL in Frame.tsx,
// patches the few names that belong to the deck, and refuses to write into a directory that is not empty (a script that writes into a tree must not overwrite).
// Not copied (they belong to one deck): src/slides/S*.tsx, src/data/, DECK_SPEC.md, src/lib/*.tsx drawing helpers other than the generic ones below.
// Then: `cd <dir> && npm install`, write DECK_SPEC.md and scripts/make_data.py, the slides; with --video-id the video code is ported as port_video.mjs does.
// See NARRATED_VIDEO_GUIDE.md, "Starting a new topic".
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const root = path.resolve(import.meta.dirname, '..');
const args = process.argv.slice(2);
const opt = (n, d) => {
  const a = args.find((x) => x.startsWith(`--${n}=`));
  return a ? a.slice(n.length + 3) : d;
};
const targetArg = args.find((a) => !a.startsWith('--'));
const ids = opt('ids', '').split(',').filter(Boolean);
const name = opt('name', targetArg ? path.basename(path.resolve(targetArg)) : '');
if (!targetArg || !ids.length) {
  console.error('usage: node scripts/new_deck.mjs <new project dir> --name=m05-modularity --ids=slide-one,slide-two,... [--video-id=M05MOD --out=x.mp4 --skip=1,8 --kicker=.. --title=.. --subtitle=..]');
  process.exit(1);
}
const target = path.resolve(targetArg);
if (target === root) {
  console.error('the target is this project');
  process.exit(1);
}
if (fs.existsSync(target) && fs.readdirSync(target).length) {
  console.error(`${target} is not empty: nothing was written`);
  process.exit(1);
}

const shared = [
  'package.json', 'package-lock.json', 'tsconfig.json', 'vite.config.ts', 'index.html',
  'src/App.tsx', 'src/main.tsx', 'src/Root.tsx', 'src/remotion-entry.ts', 'src/theme.ts', 'src/assets.d.ts',
  ...['Fade', 'FormulaStack', 'Frame', 'Patterns', 'Tex', 'Text'].map((f) => `src/components/${f}.tsx`),
  ...['anim.ts', 'network.tsx', 'look.ts', 'plot.ts', 'idle.tsx'].map((f) => `src/lib/${f}`),
  ...fs.readdirSync(path.join(root, 'src/single')).map((f) => `src/single/${f}`),
  ...['build_single.mjs', 'check_bottom.py', 'check_metrics.mjs', 'frames.mjs', 'review.mjs'].map((f) => `scripts/${f}`),
];
for (const f of shared) {
  const from = path.join(root, f);
  if (!fs.existsSync(from)) {
    console.error(`missing in this project: ${f}`);
    process.exit(1);
  }
  fs.mkdirSync(path.dirname(path.join(target, f)), {recursive: true});
  fs.copyFileSync(from, path.join(target, f));
}
fs.mkdirSync(path.join(target, 'src/slides'), {recursive: true});
fs.mkdirSync(path.join(target, 'src/data'), {recursive: true});
fs.writeFileSync(path.join(target, '.gitignore'), 'node_modules\ndist\nout\nreview\n');

const patch = (file, f) => {
  const p = path.join(target, file);
  fs.writeFileSync(p, f(fs.readFileSync(p, 'utf8')));
};
patch('package.json', (s) => {
  const pkg = JSON.parse(s);
  pkg.name = `${name}-remotion`;
  for (const k of Object.keys(pkg.scripts ?? {})) if (k.startsWith('video')) delete pkg.scripts[k]; // port_video.mjs adds them again
  return JSON.stringify(pkg, null, 2) + '\n';
});
patch('scripts/build_single.mjs', (s) => s.replaceAll('m05-community-detection.html', `${name}.html`));
patch('scripts/check_bottom.py', (s) => s.replace(/^PARTS = .*$/m, 'PARTS: set = set()  # no section dividers: edit if the deck has some'));
patch('scripts/review.mjs', (s) => s.replace(/M05 (modularity deck|slide) review/g, `${name} review`));
patch('src/components/Frame.tsx', (s) => s.replace(/export const TOTAL = \d+;/, `export const TOTAL = ${ids.length};`));

// stub slides and the index
const pad = (n) => String(n).padStart(2, '0');
ids.forEach((id, k) => {
  fs.writeFileSync(
    path.join(target, `src/slides/S${pad(k + 1)}.tsx`),
    `import React from 'react';\nimport {Frame} from '../components/Frame';\n\n/** stub: replaced by the real slide (see DECK_SPEC.md) */\nexport const marks = [30];\n\nexport const S${pad(k + 1)}: React.FC = () => <Frame n={${k + 1}}><div /></Frame>;\n`,
  );
});
const index = [
  "import type React from 'react';",
  ...ids.map((_, k) => `import {S${pad(k + 1)}, marks as marks${pad(k + 1)}} from './S${pad(k + 1)}';`),
  `
export type SlideDef = {
  /** the slide's number in DECK_SPEC.md */
  n: number;
  id: string;
  /** marks[i] is the frame where stage i is finished. Clicks move between stages. */
  marks: number[];
  Component: React.FC;
};

export const slides: SlideDef[] = [`,
  ...ids.map((id, k) => `  {n: ${k + 1}, id: '${id}', marks: marks${pad(k + 1)}, Component: S${pad(k + 1)}},`),
  '];',
];
fs.writeFileSync(path.join(target, 'src/slides/index.ts'), index.join('\n') + '\n');
console.log(`wrote ${shared.length} shared files and ${ids.length} stub slides into ${target}`);

const videoId = opt('video-id');
if (videoId) {
  const a = [path.join(root, 'scripts/port_video.mjs'), target, `--id=${videoId}`];
  for (const k of ['out', 'skip', 'kicker', 'title', 'subtitle']) if (opt(k)) a.push(`--${k}=${opt(k)}`);
  const r = spawnSync('node', a, {stdio: 'inherit'});
  if (r.status !== 0) process.exit(r.status ?? 1);
}
console.log(`
next:
  cd ${target} && npm install
  DECK_SPEC.md (a table of slides and stages, shown to the lecturer), scripts/make_data.py -> src/data/data.ts, scripts/verify_numbers.py, then the slides
  ${videoId ? 'npm run video:prose, video:skeleton, the narration (NARRATED_VIDEO_GUIDE.md)' : 'for a video: node scripts/port_video.mjs <this dir> --id=...'}`);
