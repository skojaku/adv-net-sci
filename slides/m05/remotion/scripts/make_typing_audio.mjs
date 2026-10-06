// npm run video:audio
// Synthesizes the typing sound of the narrated video (out/video-public/typing.wav) from the same keystrokes the video shows, so that
// every key on the screen has its sound at the same frame. Key clicks, thocks, a heavier space bar, a backspace; no sample files.
import fs from 'node:fs';
import path from 'node:path';
import {build} from 'esbuild';

const root = path.resolve(import.meta.dirname, '..');
const outDir = path.join(root, 'out', 'video-public');
fs.mkdirSync(outDir, {recursive: true});

// the pure part of the video, bundled for node
const bundled = path.join(outDir, 'audio-entry.mjs');
await build({entryPoints: [path.join(root, 'src/video/audio-entry.ts')], bundle: true, platform: 'node', format: 'esm', outfile: bundled, logLevel: 'error'});
const {buildTimeline, FPS, narration} = await import(`${bundled}?${Date.now()}`);
fs.rmSync(bundled);

// the stage marks, read from the slide files exactly as scripts/review.mjs does
const index = fs.readFileSync(path.join(root, 'src/slides/index.ts'), 'utf8');
const marks = [...index.matchAll(/\{n: (\d+), id: '([^']+)'/g)].map((m) => {
  const file = fs.readFileSync(path.join(root, `src/slides/S${String(Number(m[1])).padStart(2, '0')}.tsx`), 'utf8');
  return file.match(/export const marks = \[([\d,\s]+)\]/)[1].split(',').map((x) => Number(x.trim()));
});
const tl = buildTimeline(marks, narration);

const SR = 44100;
const seconds = tl.total / FPS;
const L = new Float32Array(Math.ceil((seconds + 1) * SR));
const R = new Float32Array(L.length);

let seed = 12345;
const rnd = () => {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed / 4294967296;
};
const noise = () => rnd() * 2 - 1;

/** a two-pole band-pass filter (RBJ biquad), applied to a buffer in place */
const bandpass = (x, fc, q) => {
  const w = (2 * Math.PI * fc) / SR;
  const alpha = Math.sin(w) / (2 * q);
  const b0 = alpha, b2 = -alpha, a0 = 1 + alpha, a1 = -2 * Math.cos(w), a2 = 1 - alpha;
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) {
    const y = (b0 * x[i] + b2 * x2 - a1 * y1 - a2 * y2) / a0;
    x2 = x1; x1 = x[i]; y2 = y1; y1 = y;
    x[i] = y;
  }
  return x;
};

/** one piece of a keystroke: filtered noise with an exponential decay, plus a body (a sine that drops in pitch) */
const hit = (t0, {fc, q = 1.1, tau, amp, body = 0, f0 = 280, f1 = 140, btau = 0.02, pan = 0}) => {
  const n = Math.floor(Math.min(0.25, tau * 8 + 0.02) * SR);
  const buf = new Float32Array(n);
  for (let i = 0; i < n; i++) buf[i] = noise() * Math.exp(-i / SR / tau);
  bandpass(buf, fc, q);
  let phase = 0;
  const start = Math.floor(t0 * SR);
  const gl = Math.cos(((pan + 1) * Math.PI) / 4), gr = Math.sin(((pan + 1) * Math.PI) / 4);
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    let v = buf[i] * amp * 3.2;
    if (body) {
      const f = f1 + (f0 - f1) * Math.exp(-t / 0.018);
      phase += (2 * Math.PI * f) / SR;
      v += Math.sin(phase) * body * Math.exp(-t / btau);
    }
    const j = start + i;
    if (j >= L.length) break;
    L[j] += v * gl;
    R[j] += v * gr;
  }
};

const clack = (t, kind) => {
  const v = 0.88 + rnd() * 0.24; // a little different every time
  const pan = (rnd() - 0.5) * 0.3;
  if (kind === 'space') {
    hit(t, {fc: 1500 * v, q: 0.9, tau: 0.012, amp: 0.7, body: 0.2, f0: 210 * v, f1: 90, btau: 0.04, pan});
    hit(t, {fc: 3200, q: 0.9, tau: 0.004, amp: 0.45, pan});
    hit(t + 0.095 + rnd() * 0.02, {fc: 2600, q: 1, tau: 0.006, amp: 0.2, body: 0.03, f0: 160, f1: 100, btau: 0.02, pan});
  } else if (kind === 'back') {
    hit(t, {fc: 2200 * v, q: 1.0, tau: 0.009, amp: 0.85, body: 0.17, f0: 240 * v, f1: 120, btau: 0.028, pan});
    hit(t, {fc: 6500, q: 0.8, tau: 0.002, amp: 0.6, pan});
    hit(t + 0.07 + rnd() * 0.02, {fc: 4200, q: 1, tau: 0.004, amp: 0.22, pan});
  } else {
    hit(t, {fc: 1300 * v, q: 0.9, tau: 0.01, amp: 0.45, pan}); // the plastic clack
    hit(t, {fc: 3000 * v, q: 1.2, tau: 0.006, amp: 0.8, body: 0.3, f0: 300 * v, f1: 150, btau: 0.024, pan});
    hit(t, {fc: 7500, q: 0.8, tau: 0.0016, amp: 0.4, pan}); // the sharp edge of the click
    hit(t + 0.075 + rnd() * 0.03, {fc: 4400 * v, q: 1, tau: 0.004, amp: 0.24, body: 0.02, f0: 200, f1: 150, btau: 0.012, pan}); // the key coming back up
  }
};

// ---- recorded samples (sounds/key-*.wav, space-*.wav, back-*.wav), used instead of the synthesized sound when they exist
const soundsDir = path.join(root, 'sounds');
const readWav = (file) => {
  const b = fs.readFileSync(file);
  if (b.toString('ascii', 0, 4) !== 'RIFF' || b.toString('ascii', 8, 12) !== 'WAVE') throw new Error(`${file}: not a WAV file`);
  let pos = 12, fmt = null, data = null;
  while (pos + 8 <= b.length) {
    const id = b.toString('ascii', pos, pos + 4);
    const size = b.readUInt32LE(pos + 4);
    if (id === 'fmt ') fmt = {tag: b.readUInt16LE(pos + 8), ch: b.readUInt16LE(pos + 10), sr: b.readUInt32LE(pos + 12), bits: b.readUInt16LE(pos + 22)};
    if (id === 'data') data = b.subarray(pos + 8, pos + 8 + size);
    pos += 8 + size + (size % 2);
  }
  if (!fmt || !data) throw new Error(`${file}: no fmt or data chunk`);
  const bytes = fmt.bits / 8;
  const frames = Math.floor(data.length / (bytes * fmt.ch));
  const mono = new Float32Array(frames);
  for (let i = 0; i < frames; i++) {
    let sum = 0;
    for (let c = 0; c < fmt.ch; c++) {
      const o = (i * fmt.ch + c) * bytes;
      let v;
      if (fmt.tag === 3 && fmt.bits === 32) v = data.readFloatLE(o);
      else if (fmt.bits === 16) v = data.readInt16LE(o) / 32768;
      else if (fmt.bits === 24) v = data.readIntLE(o, 3) / 8388608;
      else if (fmt.bits === 32) v = data.readInt32LE(o) / 2147483648;
      else throw new Error(`${file}: ${fmt.bits}-bit samples are not supported`);
      sum += v;
    }
    mono[i] = sum / fmt.ch;
  }
  // cut the silence before the click (keep 3 ms); the level is set for all the samples together afterwards, so the space bar stays louder than a letter
  let peak = 0;
  for (const v of mono) peak = Math.max(peak, Math.abs(v));
  let start = 0;
  while (start < frames && Math.abs(mono[start]) < 0.04 * peak) start++;
  start = Math.max(0, start - Math.floor(0.003 * fmt.sr));
  return {sr: fmt.sr, x: mono.slice(start), peak};
};
const samples = {key: [], space: [], back: []};
if (fs.existsSync(soundsDir)) {
  for (const f of fs.readdirSync(soundsDir).sort()) {
    const m = /^(key|space|back)[-_ ]?\d*\.wav$/i.exec(f);
    if (m) samples[m[1].toLowerCase()].push(readWav(path.join(soundsDir, f)));
  }
}
{
  let all = 0;
  for (const bank of Object.values(samples)) for (const smp of bank) all = Math.max(all, smp.peak);
  for (const bank of Object.values(samples)) for (const smp of bank) for (let i = 0; i < smp.x.length; i++) smp.x[i] = (smp.x[i] / (all || 1)) * 0.8;
}
const lastPick = {key: -1, space: -1, back: -1};
const playSample = (t0, kind) => {
  const bank = samples[kind];
  let i = Math.floor(rnd() * bank.length);
  if (bank.length > 1 && i === lastPick[kind]) i = (i + 1) % bank.length;
  lastPick[kind] = i;
  const {sr, x} = bank[i];
  const wide = bank.length < 3 ? 0.12 : 0.07; // a bank with few recordings gets more pitch variation
  const rate = (sr / SR) * (1 - wide / 2 + rnd() * wide);
  const gain = 0.85 + rnd() * 0.3;
  const pan = (rnd() - 0.5) * 0.3;
  const gl = Math.cos(((pan + 1) * Math.PI) / 4), gr = Math.sin(((pan + 1) * Math.PI) / 4);
  const start = Math.floor(t0 * SR);
  const n = Math.floor(x.length / rate);
  for (let k = 0; k < n; k++) {
    const pos = k * rate, i0 = Math.floor(pos), f = pos - i0;
    const v = (x[i0] * (1 - f) + (x[i0 + 1] ?? 0) * f) * gain;
    const j = start + k;
    if (j >= L.length) break;
    L[j] += v * gl;
    R[j] += v * gr;
  }
};
const used = Object.entries(samples).filter(([, v]) => v.length).map(([k, v]) => `${k}: ${v.length}`);
console.log(used.length ? `recorded samples: ${used.join(', ')}; the other kinds are synthesized` : 'no recorded samples in sounds/: all synthesized');

// the space bar is silent unless --space-sound is given (the thud of a space bar was found distracting)
const spaceSound = process.argv.includes('--space-sound');
for (const k of tl.keys) {
  if (k.kind === 'space' && !spaceSound) continue;
  if (samples[k.kind].length) playSample(k.frame / FPS, k.kind);
  else clack(k.frame / FPS, k.kind);
}

// a soft limiter, then to 16-bit
let peak = 0;
for (let i = 0; i < L.length; i++) {
  L[i] = Math.tanh(L[i] * 1.1);
  R[i] = Math.tanh(R[i] * 1.1);
  peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
}
const gain = 0.8 / peak;
const pcm = Buffer.alloc(L.length * 4);
for (let i = 0; i < L.length; i++) {
  pcm.writeInt16LE(Math.round(L[i] * gain * 32767), i * 4);
  pcm.writeInt16LE(Math.round(R[i] * gain * 32767), i * 4 + 2);
}
const header = Buffer.alloc(44);
header.write('RIFF', 0); header.writeUInt32LE(36 + pcm.length, 4); header.write('WAVE', 8); header.write('fmt ', 12);
header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20); header.writeUInt16LE(2, 22); header.writeUInt32LE(SR, 24);
header.writeUInt32LE(SR * 4, 28); header.writeUInt16LE(4, 32); header.writeUInt16LE(16, 34); header.write('data', 36); header.writeUInt32LE(pcm.length, 40);
fs.writeFileSync(path.join(outDir, 'typing.wav'), Buffer.concat([header, pcm]));

const typos = tl.bubbles.reduce((a, b) => a + b.keys.filter((e) => e.kind === 'back').length, 0);
console.log(`${tl.bubbles.length} bubbles, ${tl.keys.length} keystrokes (${typos} backspaces), ${tl.total} frames = ${(seconds / 60).toFixed(1)} min`);
console.log(`wrote ${path.join(outDir, 'typing.wav')} (peak before normalising ${peak.toFixed(2)})`);
