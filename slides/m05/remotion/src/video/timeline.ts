import {KeyEv, KeyKind, hashString, planTyping} from './typing';

/**
 * The timeline of the narrated video, from the stage marks of the slides and the narration lines.
 * Pure (no React), so that the typing sound can be synthesized from the same keystrokes (scripts/make_typing_audio.mjs).
 *
 * A slide plays stage by stage, as in the click-through deck: the animation of a stage runs and finishes, then the picture is held
 * while the narration of that stage is typed (nothing on the slide moves while a note is being read), then the next stage starts.
 * Bubbles stay until the slide changes.
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
export const LEAD = 40; // narration starts this long after the animation of its stage has finished, so text never moves while a note is being read
export const POP = 9; // the bubble pops up this long before the first key
export const GAP = 44; // between two bubbles of one stage
export const READ = 72; // after the last key of a stage: time to finish reading and to look at the slide
export const HOLD = 48; // after the animation of a stage without narration
export const END_PAD = 75;
export const MAX_CHARS = 64; // a line longer than this wraps in its bubble
/** the three section dividers of the deck are left out of the video: it is one continuous talk, not three chapters */
export const SKIP = [1, 8, 22];
/** in a stage's narration this line stands where the slide's own sentences are typed (by default they come first) */
export const MIRROR = '@mirror';

/** a sentence of the slide, cut into lines that fit a bubble: at sentence ends first; a long sentence is cut near its middle, at a comma, colon or semicolon if there is one there, else at a space */
export const splitLine = (text: string): string[] => {
  const out: string[] = [];
  const cutLong = (t: string) => {
    if (t.length <= MAX_CHARS) {
      out.push(t);
      return;
    }
    const target = Math.min(t.length / 2, MAX_CHARS);
    let best = -1;
    let bestDist = 1e9;
    for (let i = 1; i < t.length - 1; i++) {
      const ch = t[i];
      const isSpace = ch === ' ';
      const isPunctuationCut = (ch === ',' || ch === ':' || ch === ';') && t[i + 1] === ' ';
      if (!isSpace && !isPunctuationCut) continue;
      const cut = isPunctuationCut ? i + 1 : i;
      const dist = Math.abs(cut - target) - (isPunctuationCut ? 8 : 0); // a punctuation cut is worth eight characters
      if (cut <= MAX_CHARS && dist < bestDist) {
        best = cut;
        bestDist = dist;
      }
    }
    if (best < 0) best = MAX_CHARS;
    out.push(t.slice(0, best).trim());
    cutLong(t.slice(best).trim());
  };
  for (const sentence of text.split(/(?<=[.?!])\s+/)) if (sentence.trim()) cutLong(sentence.trim());
  return out;
};

/** the lines of a stage: the slide's own sentences (typed in the chat instead of standing on the slide) and the narration */
export const stageLines = (mirror: string[] | undefined, authored: string[] | undefined): string[] => {
  const words = (mirror ?? []).flatMap(splitLine).map((t) => t.charAt(0).toUpperCase() + t.slice(1)); // a hand-written caption becomes a message
  const mine = authored ?? [];
  const i = mine.indexOf(MIRROR);
  return i < 0 ? [...words, ...mine] : [...mine.slice(0, i), ...words, ...mine.slice(i + 1)];
};

export type Prose = Record<string, Record<string, string[]>>;

export const buildTimeline = (marks: number[][], narration: Narration, prose: Prose = {}, skip: number[] = []): Timeline => {
  let pos = LEAD_IN;
  const slides: SlideSeg[] = [];
  const bubbles: Bubble[] = [];
  marks.forEach((mk, si) => {
    const n = si + 1;
    if (skip.includes(n)) return;
    const from = pos;
    const stages: StageSeg[] = [];
    mk.forEach((end, k) => {
      const slideFrom = k === 0 ? 0 : mk[k - 1];
      const anim = end - slideFrom;
      const lines = stageLines(prose[String(n)]?.[String(k)], narration[n]?.[k]);
      const stageFrom = pos;
      let t = anim + LEAD; // after the animation of the stage
      let lastEnd = 0;
      lines.forEach((text, j) => {
        if (text.length > MAX_CHARS) throw new Error(`S${n} stage ${k + 1}: "${text}" is ${text.length} characters (limit ${MAX_CHARS})`);
        const start = stageFrom + t;
        const plan = planTyping(text, hashString(`${n}/${k}/${j}/${text}`));
        const keys = plan.events.map((e: KeyEv) => ({frame: start + POP + (e.t * FPS) / 1000, kind: e.kind, text: e.text}));
        const typedEnd = keys[keys.length - 1].frame;
        bubbles.push({slide: n, stage: k, index: j, text, start, keys, typedEnd});
        lastEnd = typedEnd - stageFrom;
        t = lastEnd + GAP;
      });
      const dur = lines.length ? Math.ceil(lastEnd) + READ : anim + HOLD;
      stages.push({k, from: stageFrom, anim, hold: dur - anim, slideFrom, slideTo: end});
      pos += dur;
    });
    slides.push({n, from, dur: pos - from, stages});
  });
  const total = pos + END_PAD;
  const keys = bubbles.flatMap((b) => b.keys.map((e) => ({frame: e.frame, kind: e.kind}))).sort((a, b) => a.frame - b.frame);
  return {slides, bubbles, keys, total};
};

/** how the narrator reacts to a stage: after the last line of the stage is typed he takes his hands off the keyboard and shows the mood */
export type Mood = 'worry' | 'shrug';
export type MoodRule = {slide: number; stage: number; mood: Mood};
export type Reaction = {from: number; to: number; mood: Mood};
export const REACT_AFTER = 6; // frames after the last key before the mood starts
export const REACT_BEFORE = 6; // the mood has ended this long before the next line pops up
export const REACT_MAX = 100; // frames a mood is held at most

/** The reactions of a timeline. A rule names a stage and must find it: a stage without lines would never show the mood, so that is an error. */
export const reactionsOf = (tl: Timeline, rules: MoodRule[]): Reaction[] =>
  rules.map(({slide, stage, mood}) => {
    const mine = tl.bubbles.filter((b) => b.slide === slide && b.stage === stage);
    if (!mine.length) throw new Error(`mood rule S${slide} stage ${stage + 1}: that stage has no lines`);
    const last = mine[mine.length - 1];
    const next = tl.bubbles.find((b) => b.start > last.start);
    const from = Math.ceil(last.typedEnd) + REACT_AFTER;
    const to = Math.min((next ? next.start : tl.total) - REACT_BEFORE, from + REACT_MAX);
    if (to - from < 20) throw new Error(`mood rule S${slide} stage ${stage + 1}: only ${to - from} frames of room`);
    return {from, to, mood};
  });
