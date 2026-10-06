import {FINAL, KARATE_EDGES, MOVES, Q_SINGLES, STUCK} from '../data/data';
import {C} from '../theme';
import {HOLLOW, LOOK, type Look} from './look';
import type {Edge} from './network';

/** The replay of the local moves (S16, S17, S18): pure functions of data.ts, no state. */

export const NODES = 34;
export const EDGES = KARATE_EDGES as unknown as ReadonlyArray<Edge>;
export const N_MOVES = MOVES.length;

/**
 * The hue (an index into LOOK) of each group of the stuck partition STUCK. The groups 1 and 2 are the two that Louvain merges later, so
 * they differ now; and the final colours (FINAL, the 4-group picture of S14: blue, orange, brown, purple) are kept: group 2 turns orange when it joins group 1.
 */
export const STUCK_HUE = [0, 1, 4, 2, 3] as const;
export const STUCK_LOOKS: Look[] = STUCK.map((g) => LOOK[STUCK_HUE[g]]);
export const FINAL_LOOKS: Look[] = FINAL.map((g) => LOOK[g]);

/** LABELS[k][v] = the label of node v after k moves (k = 0 to 36). Each node starts with its own label (its number). */
export const LABELS: number[][] = (() => {
  const out = [Array.from({length: NODES}, (_, i) => i)];
  for (const [v, , to] of MOVES) {
    const next = out[out.length - 1].slice();
    next[v] = to;
    out.push(next);
  }
  return out;
})();

/** Q after k moves (k = 0: every node alone). */
export const Q_AFTER: number[] = [Q_SINGLES, ...MOVES.map((m) => m[3])];

// the five labels that are left at the end get the hue of their stuck group; any other label gets a hue by its number
const HUE_OF_LABEL = (() => {
  const m = new Map<number, number>();
  LABELS[N_MOVES].forEach((l, v) => m.set(l, STUCK_HUE[STUCK[v]]));
  return (l: number): number => m.get(l) ?? l % 5;
})();

/** The look of every node after k moves: a node alone with its label is hollow, a group of two or more has a hue. */
export const LOOKS_AT: Look[][] = LABELS.map((lab) => {
  const count = new Map<number, number>();
  lab.forEach((l) => count.set(l, (count.get(l) ?? 0) + 1));
  return lab.map((l) => (count.get(l) === 1 ? HOLLOW : LOOK[HUE_OF_LABEL(l)]));
});

/** Edges inside a group are heavy and in the group's hue, edges between groups are thin and pale. */
export const groupEdgeLook =
  (lab: ReadonlyArray<number>, looks: ReadonlyArray<Look>) =>
  (_i: number, e: Edge): {color: string; w: number} =>
    lab[e[0]] === lab[e[1]] && looks[e[0]] !== HOLLOW ? {color: looks[e[0]].fill, w: 7} : {color: C.faint, w: 2.5};

/** Opacity of an edge: inside a group full, between groups lower. */
export const groupEdgeOp =
  (lab: ReadonlyArray<number>, looks: ReadonlyArray<Look>) =>
  (_i: number, e: Edge): number =>
    lab[e[0]] === lab[e[1]] && looks[e[0]] !== HOLLOW ? 1 : 0.6;
