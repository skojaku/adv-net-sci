import {KeyEv, KeyKind, hashString, planTyping} from './typing';

/**
 * The timeline of the narrated video, from the stage marks of the slides and the narration lines.
 * Pure (no React), so that the typing sound can be synthesized from the same keystrokes (scripts/make_typing_audio.mjs).
 *
 * A slide plays stage by stage, as in the click-through deck: the animation of a stage runs, then the picture is held while the
 * narration of that stage is typed, then the next stage starts. Bubbles stay until the slide changes.
 */
export const FPS = 30;
/** narration[slide number][stage index] = lines; each line is one bubble */
export type Narration = Record<number, Record<number, string[]>>;

export type Bubble = {
  slide: number;
  stage: number;
  index: number;
  text: string;
  /** the frame the bubble pops up */
  start: number;
  /** the keystrokes, at global frames (fractions allowed) */
  keys: {frame: number; kind: KeyKind; text: string}[];
  /** the frame of the last keystroke */
  typedEnd: number;
};
export type StageSeg = {k: number; from: number; anim: number; hold: number; slideFrom: number; slideTo: number};
export type SlideSeg = {n: number; from: number; dur: number; stages: StageSeg[]};
export type Timeline = {slides: SlideSeg[]; bubbles: Bubble[]; keys: {frame: number; kind: KeyKind}[]; total: number};

export const LEAD_IN = 18; // frames of the first picture before anything happens
export const LEAD = 14; // narration starts this long after its stage starts
export const POP = 9; // the bubble pops up this long before the first key
export const GAP = 26; // between two bubbles of one stage
export const READ = 42; // after the last key of a stage
export const HOLD = 30; // after the animation of a stage without narration
export const HOLD_ANIM = 20; // after the animation of a stage whose narration is already done
export const END_PAD = 75;
export const MAX_CHARS = 64; // a line longer than this wraps in its bubble

export const buildTimeline = (marks: number[][], narration: Narration): Timeline => {
  let pos = LEAD_IN;
  const slides: SlideSeg[] = [];
  const bubbles: Bubble[] = [];
  marks.forEach((mk, si) => {
    const n = si + 1;
    const from = pos;
    const stages: StageSeg[] = [];
    mk.forEach((end, k) => {
      const slideFrom = k === 0 ? 0 : mk[k - 1];
      const anim = end - slideFrom;
      const lines = narration[n]?.[k] ?? [];
      const stageFrom = pos;
      let t = LEAD;
      let lastEnd = 0;
      lines.forEach((text, j) => {
        if (text.length > MAX_CHARS) throw new Error(`narration S${n} stage ${k + 1}: "${text}" is ${text.length} characters (limit ${MAX_CHARS})`);
        const start = stageFrom + t;
        const plan = planTyping(text, hashString(`${n}/${k}/${j}/${text}`));
        const keys = plan.events.map((e: KeyEv) => ({frame: start + POP + (e.t * FPS) / 1000, kind: e.kind, text: e.text}));
        const typedEnd = keys[keys.length - 1].frame;
        bubbles.push({slide: n, stage: k, index: j, text, start, keys, typedEnd});
        lastEnd = typedEnd - stageFrom;
        t = lastEnd + GAP;
      });
      const dur = lines.length ? Math.max(anim + HOLD_ANIM, Math.ceil(lastEnd) + READ) : anim + HOLD;
      stages.push({k, from: stageFrom, anim, hold: dur - anim, slideFrom, slideTo: end});
      pos += dur;
    });
    slides.push({n, from, dur: pos - from, stages});
  });
  const total = pos + END_PAD;
  const keys = bubbles.flatMap((b) => b.keys.map((e) => ({frame: e.frame, kind: e.kind}))).sort((a, b) => a.frame - b.frame);
  return {slides, bubbles, keys, total};
};
