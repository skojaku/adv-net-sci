// node scripts/port_video.mjs <target remotion project> --id=M06 [--out=m06-narrated.mp4] [--skip=1,8] [--kicker="Module 6" --title="..." --subtitle="..."] [--update]
//
// Puts the narrated-video machinery of this project (Module 05) into another Remotion deck, so that the deck can have a video of its own.
// Shared code is copied (src/video/*.ts(x), the character frames, the scripts, the typing samples) and the four files that are specific to one
// video are written as stubs: video.config.json, narration.ts, moods.ts, prose.json. Nothing is overwritten except with --update, and --update
// refreshes the shared code only, never the four stubs. package.json (scripts) and .gitignore of the target are completed.
// The target must already be a Remotion click-through deck made as REMOTION_DECK_GUIDE.md says; this script checks what it can and says what is missing.
// Then: NARRATED_VIDEO_GUIDE.md, "Making the video of another deck".
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const args = process.argv.slice(2);
const flag = (name) => args.includes(`--${name}`);
const opt = (name, fallback) => {
  const a = args.find((x) => x.startsWith(`--${name}=`));
  return a ? a.slice(name.length + 3) : fallback;
};
const targetArg = args.find((a) => !a.startsWith('--'));
if (!targetArg || !opt('id')) {
  console.error('usage: node scripts/port_video.mjs <target remotion project> --id=M06 [--out=m06-narrated.mp4] [--skip=1,8] [--kicker="Module 6" --title="..." --subtitle="..."] [--update]');
  process.exit(1);
}
const target = path.resolve(targetArg);
if (target === root) {
  console.error('the target is this project');
  process.exit(1);
}
const id = opt('id');
const out = opt('out', `${id.toLowerCase()}-narrated.mp4`);
const skip = opt('skip', '').split(',').filter(Boolean).map(Number);
const update = flag('update');
const intro = {kicker: opt('kicker', ''), title: opt('title', ''), subtitle: opt('subtitle', '')}; // the title of the introduction (narration[0][0] holds its lines)

const notes = [];
const read = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null);
const rel = (p) => path.relative(target, p);

// what the target needs before a video can be made of it
if (!fs.existsSync(path.join(target, 'package.json'))) {
  console.error(`${target} has no package.json: it is not a project`);
  process.exit(1);
}
const pkg = JSON.parse(read(path.join(target, 'package.json')));
const deps = {...pkg.dependencies, ...pkg.devDependencies};
for (const d of ['remotion', '@remotion/cli', '@remotion/google-fonts', 'react']) if (!deps[d]) notes.push(`package.json lacks "${d}" (npm install ${d}@<the version of remotion>)`);
if (!deps.vite && !deps.esbuild) notes.push('the scripts bundle with esbuild: it comes with vite, or `npm install -D esbuild`');
const index = read(path.join(target, 'src/slides/index.ts'));
if (!index || !/\{n: \d+, id: '[^']+'/.test(index)) notes.push("src/slides/index.ts must list the slides as {n: 1, id: 'name', marks, Component}: the scripts read the slide list and the stage marks from it");
if (!/export const ProseContext/.test(read(path.join(target, 'src/components/Text.tsx')) ?? '')) notes.push('src/components/Text.tsx must export ProseContext (the video hides the slides\' sentences and collects them): copy it from this project');
if (!/export const C\b/.test(read(path.join(target, 'src/theme.ts')) ?? '')) notes.push('src/theme.ts must export the colour table C (Narrator.tsx uses C.ink and C.blue)');
const tsconfig = read(path.join(target, 'tsconfig.json')) ?? '';
if (!/resolveJsonModule["']?\s*:\s*true/.test(tsconfig)) notes.push('tsconfig.json needs "resolveJsonModule": true (video.config.json and prose.json are imported)');

const copied = [];
const kept = [];
const copyFile = (from, to, always = false) => {
  if (!fs.existsSync(from)) return;
  if (fs.existsSync(to) && !(update && !always)) {
    kept.push(rel(to));
    return;
  }
  fs.mkdirSync(path.dirname(to), {recursive: true});
  fs.copyFileSync(from, to);
  copied.push(rel(to));
};
const copyDir = (dir, pattern) => {
  const from = path.join(root, dir);
  if (!fs.existsSync(from)) return;
  for (const f of fs.readdirSync(from)) if (pattern.test(f)) copyFile(path.join(from, f), path.join(target, dir, f));
};

// the shared code
for (const f of ['Character.tsx', 'IntroTitle.tsx', 'NarratedDeck.tsx', 'Narrator.tsx', 'SoundSampler.tsx', 'VideoRoot.tsx', 'audio-entry.ts', 'entry.ts', 'sampler.ts', 'timeline.ts', 'typing.ts']) copyFile(path.join(root, 'src/video', f), path.join(target, 'src/video', f));
copyDir('src/video/character', /\.(png|json)$/);
copyFile(path.join(root, 'src/assets.d.ts'), path.join(target, 'src/assets.d.ts')); // `import png from '...png'`
for (const f of ['make_typing_audio.mjs', 'render_video.mjs', 'collect_prose.mjs', 'extract_mechvibes.mjs', 'make_sampler.mjs', 'line_lengths.mjs', 'narration_skeleton.mjs', 'prep_character.py', 'gen_character.py', 'lib/typing_sound.mjs']) copyFile(path.join(root, 'scripts', f), path.join(target, 'scripts', f));
copyDir('sounds', /\.(wav|md|txt)$/);

// the four files that belong to one video: written once, never refreshed
const stub = (file, text) => {
  const to = path.join(target, file);
  if (fs.existsSync(to)) {
    kept.push(file);
    return;
  }
  fs.mkdirSync(path.dirname(to), {recursive: true});
  fs.writeFileSync(to, text);
  copied.push(file);
};
stub('src/video/video.config.json', JSON.stringify({id, out, skip, intro}, null, 2) + '\n');
stub('src/video/narration.ts', "import type {Narration} from './timeline';\n\n// stub: replace with `npm run video:skeleton`\nexport const narration: Narration = {};\n");
stub('src/video/moods.ts', "import type {MoodRule} from './timeline';\n\n/** Where the figure reacts after the last line of a stage: {slide, stage (0-based), mood: 'worry' | 'shrug'}. Few of them. See NARRATED_VIDEO_GUIDE.md, \"Reactions\". */\nexport const MOODS: MoodRule[] = [];\n");
stub('src/video/prose.json', '{}\n');

// package.json scripts and .gitignore
const want = {
  video: 'node scripts/render_video.mjs',
  'video:audio': 'node scripts/make_typing_audio.mjs',
  'video:sampler': 'node scripts/make_sampler.mjs',
  'video:prose': 'node scripts/collect_prose.mjs',
  'video:skeleton': 'node scripts/narration_skeleton.mjs',
  'video:lengths': 'node scripts/line_lengths.mjs',
};
pkg.scripts = pkg.scripts ?? {};
const added = Object.keys(want).filter((k) => !pkg.scripts[k]);
for (const k of added) pkg.scripts[k] = want[k];
if (added.length) fs.writeFileSync(path.join(target, 'package.json'), JSON.stringify(pkg, null, 2) + '\n');
const giPath = path.join(target, '.gitignore');
const gi = read(giPath) ?? '';
const giAdd = ['out', 'sounds/*.wav', 'sounds/SOURCE.txt'].filter((l) => !gi.split('\n').some((x) => x.trim() === l || x.trim() === `${l}/`));
if (giAdd.length) fs.writeFileSync(giPath, gi + (gi && !gi.endsWith('\n') ? '\n' : '') + giAdd.join('\n') + '\n');

console.log(`copied ${copied.length} files${update ? ' (shared code refreshed: --update)' : ''}; kept ${kept.length} that already exist${kept.length && !update ? ' (pass --update to refresh the shared code)' : ''}`);
for (const f of copied) console.log(`  + ${f}`);
if (added.length) console.log(`package.json: added scripts ${added.join(', ')}`);
if (giAdd.length) console.log(`.gitignore: added ${giAdd.join(', ')}`);
if (notes.length) {
  console.log('\nTO FIX in the target before the video will build:');
  for (const n of notes) console.log(`  - ${n}`);
}
console.log(`
next, in ${target}:
  npm install                 (if the project is new)
  npm run video:prose         the slides' own sentences -> src/video/prose.json
  npm run video:skeleton -- --out=src/video/narration.ts      one entry per slide and stage, to fill in
  ... write narration.ts and moods.ts, set "skip" in src/video/video.config.json, then npm run video:lengths, video:audio, video (NARRATED_VIDEO_GUIDE.md)`);
