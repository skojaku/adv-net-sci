import type React from 'react';
import {S01, marks as marks01} from './S01';
import {S02, marks as marks02} from './S02';
import {S03, marks as marks03} from './S03';
import {S04, marks as marks04} from './S04';
import {S05, marks as marks05} from './S05';
import {S06, marks as marks06} from './S06';
import {S07, marks as marks07} from './S07';
import {S08, marks as marks08} from './S08';
import {S09, marks as marks09} from './S09';
import {S10, marks as marks10} from './S10';
import {S11, marks as marks11} from './S11';
import {S12, marks as marks12} from './S12';
import {S13, marks as marks13} from './S13';
import {S14, marks as marks14} from './S14';
import {S15, marks as marks15} from './S15';
import {S16, marks as marks16} from './S16';
import {S17, marks as marks17} from './S17';
import {S18, marks as marks18} from './S18';
import {S19, marks as marks19} from './S19';
import {S20, marks as marks20} from './S20';
import {S21, marks as marks21} from './S21';
import {S22, marks as marks22} from './S22';
import {S23, marks as marks23} from './S23';
import {S24, marks as marks24} from './S24';
import {S25, marks as marks25} from './S25';
import {S26, marks as marks26} from './S26';
import {S27, marks as marks27} from './S27';
import {S28, marks as marks28} from './S28';
import {S29, marks as marks29} from './S29';
import {S30, marks as marks30} from './S30';
import {S31, marks as marks31} from './S31';
import {S32, marks as marks32} from './S32';
import {S33, marks as marks33} from './S33';
import {S34, marks as marks34} from './S34';
import {S35, marks as marks35} from './S35';

export type SlideDef = {
  /** the slide's number in DECK_SPEC.md */
  n: number;
  id: string;
  /** marks[i] is the frame where stage i is finished. Clicks move between stages. */
  marks: number[];
  Component: React.FC;
};

export const slides: SlideDef[] = [
  {n: 1, id: 'limits', marks: marks01, Component: S01},
  {n: 2, id: 'ring-of-triangles', marks: marks02, Component: S02},
  {n: 3, id: 'add-triangles', marks: marks03, Component: S03},
  {n: 4, id: 'resolution-limit', marks: marks04, Component: S04},
  {n: 5, id: 'similar-q', marks: marks05, Component: S05},
  {n: 6, id: 'no-groups', marks: marks06, Component: S06},
  {n: 7, id: 'noise', marks: marks07, Component: S07},
  {n: 8, id: 'compare', marks: marks08, Component: S08},
  {n: 9, id: 'eight-nodes', marks: marks09, Component: S09},
  {n: 10, id: 'why-pairs', marks: marks10, Component: S10},
  {n: 11, id: 'rand-index', marks: marks11, Component: S11},
  {n: 12, id: 'shuffle', marks: marks12, Component: S12},
  {n: 13, id: 'ari', marks: marks13, Component: S13},
  {n: 14, id: 'pairs-or-nodes', marks: marks14, Component: S14},
  {n: 15, id: 'yes-no-questions', marks: marks15, Component: S15},
  {n: 16, id: 'guess-the-group', marks: marks16, Component: S16},
  {n: 17, id: 'found-group-hint', marks: marks17, Component: S17},
  {n: 18, id: 'mutual-information', marks: marks18, Component: S18},
  {n: 19, id: 'nmi', marks: marks19, Component: S19},
  {n: 20, id: 'tiny-groups', marks: marks20, Component: S20},
  {n: 21, id: 'karate-compare', marks: marks21, Component: S21},
  {n: 22, id: 'turn-it-around', marks: marks22, Component: S22},
  {n: 23, id: 'groups-first', marks: marks23, Component: S23},
  {n: 24, id: 'see-groups', marks: marks24, Component: S24},
  {n: 25, id: 'sort-blocks', marks: marks25, Component: S25},
  {n: 26, id: 'outward-question', marks: marks26, Component: S26},
  {n: 27, id: 'outward', marks: marks27, Component: S27},
  {n: 28, id: 'inference', marks: marks28, Component: S28},
  {n: 29, id: 'sbm-likelihood', marks: marks29, Component: S29},
  {n: 30, id: 'fix-c-find-p', marks: marks30, Component: S30},
  {n: 31, id: 'back-to-c', marks: marks31, Component: S31},
  {n: 32, id: 'more-groups', marks: marks32, Component: S32},
  {n: 33, id: 'bayesian-sbm', marks: marks33, Component: S33},
  {n: 34, id: 'graph-tool', marks: marks34, Component: S34},
  {n: 35, id: 'karate-one-group', marks: marks35, Component: S35},
];
