/**
 * Human-looking typing, planned in advance (pure and deterministic: the same text and seed always give the same keystrokes).
 * Keys come in uneven bursts, slow down after spaces and punctuation, and now and then land on a neighbouring key; the typist
 * notices after a beat (sometimes after one or two more letters), deletes with the backspace key, and types the letter again.
 */
export type KeyKind = 'key' | 'space' | 'back';
export type KeyEv = {
  /** milliseconds after the first keystroke of the line is allowed to happen */
  t: number;
  kind: KeyKind;
  /** the whole text on screen right after this keystroke */
  text: string;
};

const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

export const hashString = (s: string): number => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
};

const ROWS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'];
/** the keys next to a letter on a QWERTY keyboard (same row, and the two above and below it) */
const neighbours = (ch: string): string[] => {
  const lower = ch.toLowerCase();
  const r = ROWS.findIndex((row) => row.includes(lower));
  if (r < 0) return [];
  const i = ROWS[r].indexOf(lower);
  const out: string[] = [];
  const add = (row: number, idx: number) => {
    if (row >= 0 && row < ROWS.length && idx >= 0 && idx < ROWS[row].length) out.push(ROWS[row][idx]);
  };
  add(r, i - 1);
  add(r, i + 1);
  add(r - 1, i);
  add(r - 1, i + 1);
  add(r + 1, i - 1);
  add(r + 1, i);
  return out;
};

/** `speed` > 1 types faster. Returns the keystrokes and the time of the last one. */
export const planTyping = (text: string, seed: number, speed = 1): {events: KeyEv[]; duration: number} => {
  const rng = mulberry32(seed);
  const events: KeyEv[] = [];
  let shown = '';
  let t = 0;
  let typos = 0;
  let noTypoBefore = 0;
  let i = 0;
  const press = (ch: string, gap: number) => {
    t += gap;
    shown += ch;
    events.push({t, kind: ch === ' ' ? 'space' : 'key', text: shown});
  };
  const back = (gap: number) => {
    t += gap;
    shown = shown.slice(0, -1);
    events.push({t, kind: 'back', text: shown});
  };
  const base = 58 / speed;
  const gapFor = (ch: string) => {
    let g = base * (0.62 + rng() * 0.9);
    if (rng() < 0.12) g *= 0.45; // two keys in quick succession
    if (rng() < 0.04) g += 220 + rng() * 200; // a hesitation
    if (ch === ' ') g += 18 + rng() * 55;
    if (/[.,;:?!]/.test(ch)) g += 110 + rng() * 140;
    return g;
  };

  while (i < text.length) {
    const ch = text[i];
    const eligible = typos < 2 && i >= noTypoBefore && i >= 3 && text.length >= 14 && /[a-z]/i.test(ch) && neighbours(ch).length > 0;
    if (eligible && rng() < 0.012) {
      typos++;
      const options = neighbours(ch);
      let wrong = options[Math.floor(rng() * options.length)];
      if (ch !== ch.toLowerCase()) wrong = wrong.toUpperCase();
      press(wrong, gapFor(ch));
      // sometimes the typist carries on for a letter or two before noticing
      let extra = rng() < 0.5 ? 0 : rng() < 0.6 ? 1 : 2;
      extra = Math.min(extra, text.length - 1 - i);
      for (let k = 1; k <= extra; k++) press(text[i + k], gapFor(text[i + k]) * 0.85);
      t += 190 + rng() * 230; // the moment of noticing
      for (let k = 0; k < 1 + extra; k++) back(k === 0 ? 40 : 52 + rng() * 38);
      t += 70 + rng() * 90;
      noTypoBefore = i + 4;
      continue; // type the right letter now
    }
    press(ch, gapFor(ch));
    i++;
  }
  if (shown !== text) throw new Error(`planTyping: "${shown}" is not "${text}"`);
  return {events, duration: t};
};
