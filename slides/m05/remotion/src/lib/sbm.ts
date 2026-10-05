import {C} from '../theme';
import {SBM_U} from '../data/data';
import type {Edge, Pt} from './network';

/** The 28 pairs of the 8-node model of S18 to S23, in the order SBM_U is indexed. Nodes 0 to 3 are blue, 4 to 7 red. */
export const SBM_PAIRS: Edge[] = [];
for (let a = 0; a < 8; a++) for (let b = a + 1; b < 8; b++) SBM_PAIRS.push([a, b]);

export const SBM_GROUP = [0, 0, 0, 0, 1, 1, 1, 1] as const;
export const SBM_COLORS = [C.blue, C.red] as const;
export const sbmInside = (a: number, b: number) => SBM_GROUP[a] === SBM_GROUP[b];

/** The probability of the pair's block, given p inside a group and p between groups. */
export const sbmP = (a: number, b: number, pIn: number, pOut: number) => (sbmInside(a, b) ? pIn : pOut);

/** An edge exists when its fixed uniform number is below the block probability. */
export const sbmEdges = (pIn: number, pOut: number): Edge[] => SBM_PAIRS.filter(([a, b], k) => SBM_U[k] < sbmP(a, b, pIn, pOut));

/** Index of a pair in SBM_PAIRS and SBM_U. */
export const pairIndex = (a: number, b: number) => SBM_PAIRS.findIndex(([x, y]) => x === Math.min(a, b) && y === Math.max(a, b));

/** The 8 nodes on a circle, first group on one half, second on the other. */
export const circle8 = (cx: number, cy: number, r: number): Pt[] =>
  Array.from({length: 8}, (_, i) => {
    const t = (-Math.PI / 2) + ((i + 0.5) * Math.PI) / 4 + (i >= 4 ? Math.PI / 12 : -Math.PI / 12);
    return [cx + r * Math.cos(t), cy + r * Math.sin(t)] as const;
  });
