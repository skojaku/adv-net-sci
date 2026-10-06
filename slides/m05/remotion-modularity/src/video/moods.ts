import type {MoodRule} from './timeline';

/**
 * Where the narrator stops typing and reacts, after the last line of a stage. Stage numbers are 0-based, as in narration.ts.
 * worry: something goes wrong or misleads; shrug: no single answer; puzzled: a question to think about; surprise: a result nobody expects;
 * happy: a step that works; sparkle: an aha; smug: "and nothing is lost". (Lecturer: the narrator was monotone, so there are more faces.)
 */
export const MOODS: MoodRule[] = [
  {slide: 1, stage: 1, mood: 'puzzled'}, // is each colour a strong community?
  {slide: 3, stage: 0, mood: 'puzzled'}, // which grouping gives the highest score?
  {slide: 3, stage: 2, mood: 'worry'}, // everyone in one group gets the best score
  {slide: 4, stage: 2, mood: 'smug'}, // now we need that random network
  {slide: 7, stage: 1, mood: 'happy'}, // k_i k_j / 2M
  {slide: 10, stage: 3, mood: 'surprise'}, // every row sums to 0: one group gives Q = 0
  {slide: 12, stage: 3, mood: 'happy'}, // the formula of Q, Q = 0.358
  {slide: 13, stage: 3, mood: 'sparkle'}, // four groups give 0.420
  {slide: 14, stage: 0, mood: 'shrug'}, // 2.1e28 partitions: no way to try them all
  {slide: 15, stage: 3, mood: 'happy'}, // label switching ends in 5 groups, Q = 0.399
  {slide: 16, stage: 1, mood: 'worry'}, // moving one node lowers Q
  {slide: 16, stage: 2, mood: 'sparkle'}, // merging two whole groups raises Q
  {slide: 17, stage: 2, mood: 'smug'}, // the network of groups has the same Q: nothing is lost
  {slide: 19, stage: 1, mood: 'smug'}, // a third level changes nothing, so we stop
  {slide: 20, stage: 2, mood: 'worry'}, // the blue group is in two pieces
  {slide: 20, stage: 3, mood: 'surprise'}, // up to 25% badly connected, up to 16% disconnected
  {slide: 21, stage: 1, mood: 'sparkle'}, // splitting raises Q to 0.482
  {slide: 21, stage: 3, mood: 'shrug'}, // merging too much comes from Q itself
];
