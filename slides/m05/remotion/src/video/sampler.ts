import {Bubble, FPS} from './timeline';
import {planTyping} from './typing';

/**
 * A listening test of the Mechvibes keyboard packs: every pack types the same sentence with the same keystrokes, one after the other,
 * so that only the sound differs. Pure, like timeline.ts (scripts/make_sampler.mjs builds the sound from it).
 */
export type SamplerPack = {id: string; name: string; feel: string};
export const SAMPLER_PACKS: SamplerPack[] = [
  {id: 'cherrymx-red-abs', name: 'Cherry MX Red (ABS)', feel: 'smooth linear: the current choice'},
  {id: 'cherrymx-black-abs', name: 'Cherry MX Black (ABS)', feel: 'deeper linear'},
  {id: 'cherrymx-black-pbt', name: 'Cherry MX Black (PBT)', feel: 'deeper linear, a little firmer'},
  {id: 'topre-purple-hybrid-pbt', name: 'Topre Purple Hybrid (PBT)', feel: 'low and soft thock'},
  {id: 'eg-crystal-purple', name: 'EG Crystal Purple', feel: 'tactile, mid'},
  {id: 'eg-oreo', name: 'EG Oreo', feel: 'thock with a bright top'},
  {id: 'cherrymx-brown-abs', name: 'Cherry MX Brown (ABS)', feel: 'tactile'},
  {id: 'cherrymx-brown-pbt', name: 'Cherry MX Brown (PBT)', feel: 'tactile, a little softer'},
  {id: 'cherrymx-blue-pbt', name: 'Cherry MX Blue (PBT)', feel: 'clicky'},
  {id: 'cherrymx-blue-abs', name: 'Cherry MX Blue (ABS)', feel: 'clicky and bright: the first version'},
];

export const SAMPLER_TEXT = 'Take a moment: which grouping has the higher Q?';
export const PRE = 36; // frames of the pack's name before the typing starts
export const POST = 54; // frames of quiet after it

/** the first seed whose typing includes a typo and a backspace, so that the backspace can be heard too */
const SEED = (() => {
  for (let s = 1; s < 500; s++) if (planTyping(SAMPLER_TEXT, s).events.some((e) => e.kind === 'back')) return s;
  return 1;
})();
const PLAN = planTyping(SAMPLER_TEXT, SEED);
const TYPED = Math.ceil((PLAN.duration * FPS) / 1000);
export const SEGMENT = PRE + 10 + TYPED + POST;

export type SamplerSegment = {pack: SamplerPack; from: number};
export const samplerTimeline = (): {segments: SamplerSegment[]; bubbles: Bubble[]; keys: {frame: number; kind: 'key' | 'space' | 'back'; pack: number}[]; total: number} => {
  const segments: SamplerSegment[] = [];
  const bubbles: Bubble[] = [];
  const keys: {frame: number; kind: 'key' | 'space' | 'back'; pack: number}[] = [];
  SAMPLER_PACKS.forEach((pack, i) => {
    const from = i * SEGMENT;
    segments.push({pack, from});
    const start = from + PRE;
    const ks = PLAN.events.map((e) => ({frame: start + 10 + (e.t * FPS) / 1000, kind: e.kind, text: e.text}));
    bubbles.push({slide: i + 1, stage: 0, index: 0, text: SAMPLER_TEXT, start, keys: ks, typedEnd: ks[ks.length - 1].frame});
    for (const k of ks) keys.push({frame: k.frame, kind: k.kind, pack: i});
  });
  return {segments, bubbles, keys, total: SAMPLER_PACKS.length * SEGMENT};
};
