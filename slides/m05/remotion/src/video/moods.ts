import type {MoodRule} from './timeline';

/**
 * Where the narrator stops typing and reacts, after the last line of a stage: 'worry' (arms crossed, a sweat drop) where something goes wrong or
 * misleads, 'shrug' where there is no single answer. Kept few, so that they stay special. Stage numbers are 0-based, as in narration.ts.
 */
export const MOODS: MoodRule[] = [
  {slide: 7, stage: 1, mood: 'worry'}, // every random network scores above 0.3
  {slide: 7, stage: 3, mood: 'shrug'}, // a high Q does not prove that groups exist
  {slide: 14, stage: 1, mood: 'worry'}, // the same split, the columns reordered: 1 of 8 on the diagonal
  {slide: 14, stage: 2, mood: 'worry'}, // three found groups: no diagonal at all
  {slide: 20, stage: 1, mood: 'worry'}, // Rand looks fine, the ARI is 0
  {slide: 21, stage: 3, mood: 'shrug'}, // NMI and ARI disagree
  {slide: 32, stage: 2, mood: 'worry'}, // K = 8 fits perfectly and means nothing
  {slide: 41, stage: 2, mood: 'shrug'}, // one group, no stronger than in a random network
];
