import type {MoodRule} from './timeline';

/**
 * Where the narrator stops typing and reacts, after the last line of a stage: 'worry' where something goes wrong or misleads,
 * 'shrug' where there is no single answer. Kept few, so that they stay special. Stage numbers are 0-based, as in narration.ts.
 */
export const MOODS: MoodRule[] = [
  {slide: 3, stage: 2, mood: 'worry'}, // everyone in one group gets the best score
  {slide: 15, stage: 0, mood: 'shrug'}, // 2.1e28 partitions: no way to try them all
  {slide: 17, stage: 1, mood: 'worry'}, // moving one node lowers Q
  {slide: 21, stage: 2, mood: 'worry'}, // the blue group is in two pieces
  {slide: 8, stage: 2, mood: 'shrug'}, // the approximation breaks for hubs and dense networks: left for another time
];
