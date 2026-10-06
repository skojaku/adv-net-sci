import {KARATE_POS} from '../data/data';
import {toCanvas} from './network';

/** The karate club drawn at the left of the canvas (S01 to S03 and others: a slide that follows another opens on the same picture). */
export const CLUB_L = toCanvas(KARATE_POS, 130, 230, 800, 620);
/** The club in the middle of the canvas. */
export const CLUB_C = toCanvas(KARATE_POS, 560, 230, 800, 620);
/** The club at the right of the canvas. */
export const CLUB_R = toCanvas(KARATE_POS, 990, 230, 800, 620);

/** Q (or a fraction) with three decimals and a true minus sign: 0.358, 0.000, \u22120.050. */
export const q3 = (x: number): string => (x < -0.0005 ? '\u2212' : '') + Math.abs(x).toFixed(3);
