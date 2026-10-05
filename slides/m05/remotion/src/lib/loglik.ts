import type {Edge} from './network';

/** One cell of the table for a grouping: the edges among the pairs between (or inside) groups a and b. */
export type Cell = {a: number; b: number; k: number; pairs: number};

const clampP = (x: number) => Math.min(1 - 1e-6, Math.max(1e-6, x));

/** The group labels that occur, in increasing order. */
export const groupsOf = (c: ReadonlyArray<number>): number[] => Array.from(new Set(c)).sort((x, y) => x - y);

/**
 * For every pair of groups a <= b: the number of node pairs between them and the number of
 * edges among those pairs. Pairs of identical groups count each node pair once.
 */
export const blockCounts = (edges: ReadonlyArray<Edge>, c: ReadonlyArray<number>): Cell[] => {
  const gs = groupsOf(c);
  const size = (g: number) => c.filter((x) => x === g).length;
  const cells: Cell[] = [];
  for (let i = 0; i < gs.length; i++) {
    for (let j = i; j < gs.length; j++) {
      const a = gs[i];
      const b = gs[j];
      const pairs = a === b ? (size(a) * (size(a) - 1)) / 2 : size(a) * size(b);
      const k = edges.filter(([u, v]) => (c[u] === a && c[v] === b) || (c[u] === b && c[v] === a)).length;
      cells.push({a, b, k, pairs});
    }
  }
  return cells;
};

/**
 * The log-likelihood of the network given the grouping c, with each cell's probability set to
 * its observed fraction k / pairs (clamped to [1e-6, 1 - 1e-6]):
 * sum over cells of k ln p + (pairs - k) ln(1 - p). This is the log of the probability of this exact network.
 */
export const logLik = (edges: ReadonlyArray<Edge>, c: ReadonlyArray<number>): number =>
  blockCounts(edges, c).reduce((s, {k, pairs}) => {
    if (pairs === 0) return s;
    const p = clampP(k / pairs);
    return s + k * Math.log(p) + (pairs - k) * Math.log(1 - p);
  }, 0);
