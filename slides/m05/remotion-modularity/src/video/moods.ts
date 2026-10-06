import type {MoodRule} from './timeline';

/**
 * Where the narrator stops typing and reacts, after the last line of a stage. Stage numbers are 0-based, as in narration.ts.
 * worry: something goes wrong or misleads; shrug: no single answer; surprise: a result nobody expects; smug: "and nothing is lost" / a step that works;
 * focus: a serious step; glance: his eyes go to the cup of tea (time to think); onback: lying on his back, relief.
 * (Lecturer: the narrator was monotone. Kept: expr-4 surprise, expr-7 smug, expr-8 focus; added: onback (new-6), glance (new-9); a cup of tea next to the keyboard in every frame.)
 */
export const MOODS: MoodRule[] = [
  {slide: 1, stage: 1, mood: 'glance'}, // is each colour a strong community? take a moment to think
  {slide: 3, stage: 0, mood: 'focus'}, // which grouping gives the highest score?
  {slide: 3, stage: 2, mood: 'worry'}, // everyone in one group gets the best score
  {slide: 4, stage: 2, mood: 'smug'}, // now we need that random network
  {slide: 7, stage: 1, mood: 'onback'}, // k_i k_j / 2M: the derivation is done
  {slide: 10, stage: 3, mood: 'focus'}, // every row sums to 0: one group gives Q = 0
  {slide: 12, stage: 3, mood: 'smug'}, // the formula of Q, Q = 0.358
  {slide: 13, stage: 3, mood: 'surprise'}, // four groups give 0.420
  {slide: 14, stage: 0, mood: 'shrug'}, // 2.1e28 partitions: no way to try them all
  {slide: 15, stage: 3, mood: 'glance'}, // label switching ends in 5 groups, Q = 0.399
  {slide: 16, stage: 1, mood: 'worry'}, // moving one node lowers Q
  {slide: 16, stage: 2, mood: 'surprise'}, // merging two whole groups raises Q
  {slide: 17, stage: 2, mood: 'smug'}, // the network of groups has the same Q: nothing is lost
  {slide: 19, stage: 1, mood: 'onback'}, // a third level changes nothing, so we stop
  {slide: 20, stage: 2, mood: 'worry'}, // the blue group is in two pieces
  {slide: 20, stage: 3, mood: 'surprise'}, // up to 25% badly connected, up to 16% disconnected
  {slide: 21, stage: 1, mood: 'focus'}, // splitting raises Q to 0.482
  {slide: 21, stage: 3, mood: 'shrug'}, // merging too much comes from Q itself
];
