// node scripts/extract_mechvibes.mjs --pack=cherrymx-blue-abs
// Cuts the typing samples for the video out of a Mechvibes sound pack (the packs installed with MechvibesDX or Mechvibes) and writes them to
// sounds/ as key-*.wav, space-1.wav and back-1.wav. A pack is one long audio file with a table of (start, end) times for the press and the release
// of every key; each sample here is a press and its release in one clip. Run it again with another pack name to try another keyboard.
//   --pack=NAME   a folder name under keyboard/ (default cherrymx-blue-abs); see `ls <packs>/keyboard`
//   --from=DIR    the soundpacks folder (default: the one inside /Applications/MechvibesDX.app)
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const root = path.resolve(import.meta.dirname, '..');
const arg = (name, fallback) => {
  const a = process.argv.find((x) => x.startsWith(`--${name}=`));
  return a ? a.slice(name.length + 3) : fallback;
};
const pack = arg('pack', 'cherrymx-blue-abs');
const from = arg('from', '/Applications/MechvibesDX.app/Contents/Resources/soundpacks');
const dir = path.join(from, 'keyboard', pack);
const config = JSON.parse(fs.readFileSync(path.join(dir, 'config.json'), 'utf8'));
const defs = config.definitions ?? config.defines;
if (!defs || config.definition_method !== 'single') throw new Error(`${pack}: only "single file" packs with a definitions table are supported`);

// decode the pack's audio to a 16-bit stereo wav with the ffmpeg that Remotion ships
const tmp = path.join(root, 'out', 'mechvibes-tmp.wav');
fs.mkdirSync(path.dirname(tmp), {recursive: true});
execFileSync('npx', ['remotion', 'ffmpeg', '-y', '-i', path.join(dir, config.audio_file), '-ac', '1', '-ar', '44100', '-acodec', 'pcm_s16le', tmp], {cwd: root, stdio: 'ignore'});
const wav = fs.readFileSync(tmp);
let pos = 12, data = null;
while (pos + 8 <= wav.length) {
  const id = wav.toString('ascii', pos, pos + 4), size = wav.readUInt32LE(pos + 4);
  if (id === 'data') data = wav.subarray(pos + 8, pos + 8 + Math.min(size, wav.length - pos - 8));
  pos += 8 + size + (size % 2);
}
const SR = 44100;
const total = Math.floor(data.length / 2);

const clip = (code) => {
  const t = defs[code]?.timing;
  if (!t) return null;
  const a = t[0][0];
  const b = t[1] ? Math.min(t[1][1], a + 420) : a + 200; // the press and, right after it, the release
  const i0 = Math.floor((a / 1000) * SR), i1 = Math.min(total, Math.floor((b / 1000) * SR));
  const out = Buffer.alloc((i1 - i0) * 2);
  for (let i = i0; i < i1; i++) out.writeInt16LE(data.readInt16LE(i * 2), (i - i0) * 2);
  return out;
};
const writeWav = (file, pcm) => {
  const h = Buffer.alloc(44);
  h.write('RIFF', 0); h.writeUInt32LE(36 + pcm.length, 4); h.write('WAVE', 8); h.write('fmt ', 12);
  h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(1, 22); h.writeUInt32LE(SR, 24); h.writeUInt32LE(SR * 2, 28);
  h.writeUInt16LE(2, 32); h.writeUInt16LE(16, 34); h.write('data', 36); h.writeUInt32LE(pcm.length, 40);
  fs.writeFileSync(file, Buffer.concat([h, pcm]));
};

const soundsDir = path.join(root, 'sounds');
fs.mkdirSync(soundsDir, {recursive: true});
for (const f of fs.readdirSync(soundsDir)) if (/^(key|space|back)[-_ ]?\d*\.wav$/i.test(f)) fs.rmSync(path.join(soundsDir, f));

const LETTERS = ['KeyA', 'KeyE', 'KeyN', 'KeyO', 'KeyT', 'KeyI', 'KeyR', 'KeyS', 'KeyL', 'KeyD'];
let n = 0;
for (const code of LETTERS) {
  const c = clip(code);
  if (c) writeWav(path.join(soundsDir, `key-${++n}.wav`), c);
}
const sp = clip('Space');
if (sp) writeWav(path.join(soundsDir, 'space-1.wav'), sp);
const bk = clip('Backspace');
if (bk) writeWav(path.join(soundsDir, 'back-1.wav'), bk);
fs.writeFileSync(
  path.join(soundsDir, 'SOURCE.txt'),
  `Samples cut from the Mechvibes sound pack "${config.name}" (id ${config.id}, author ${config.author}) by scripts/extract_mechvibes.mjs.\\nMechvibes and MechvibesDX are MIT licensed (github.com/hainguyents13/mechvibes, github.com/hainguyents13/mechvibes-dx).\\n`,
);
fs.rmSync(tmp);
console.log(`${config.name}: ${n} key samples${sp ? ', space' : ''}${bk ? ', backspace' : ''} -> sounds/`);
