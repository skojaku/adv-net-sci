import {FOUND8, TRUTH8, mutualInfo} from './metrics';

/**
 * The eight-node example as a probability table: rows are the true groups (blue, orange), columns the found groups
 * (A = nodes 1 to 5, B = nodes 6 to 8). Every number is computed from the two splits.
 */
export const N8 = TRUTH8.length;
export const COUNT = [0, 1].map((r) => [0, 1].map((c) => TRUTH8.filter((t, i) => t === r && FOUND8[i] === c).length));
/** joint probability p(true = r, found = c) */
export const JOINT = COUNT.map((row) => row.map((n) => n / N8));
/** marginal probabilities: p(true = r) and p(found = c) */
export const P_TRUE = JOINT.map((row) => row[0] + row[1]);
export const P_FOUND = [0, 1].map((c) => JOINT[0][c] + JOINT[1][c]);
/** what the joint would be if the two splits were unrelated: the product of the marginals */
export const PRODUCT = [0, 1].map((r) => [0, 1].map((c) => P_TRUE[r] * P_FOUND[c]));
/** joint / (marginal x marginal) */
export const RATIO = JOINT.map((row, r) => row.map((p, c) => p / PRODUCT[r][c]));
/** each cell's share of the mutual information: joint x log2(ratio); a cell with joint 0 adds nothing */
export const TERM = JOINT.map((row, r) => row.map((p, c) => (p === 0 ? 0 : p * Math.log2(RATIO[r][c]))));
export const MI = TERM.flat().reduce((a, b) => a + b, 0);

if (COUNT.flat().join() !== '4,0,1,3' || Math.abs(MI - mutualInfo(TRUTH8, FOUND8)) > 1e-9 || Math.abs(MI - 0.549) > 5e-4) {
  throw new Error('prob: unexpected table');
}

/** A number as it is read: no trailing zeros, at most `d` decimals, a proper minus sign. */
export const fmt = (x: number, d = 4): string => Number(x.toFixed(d)).toString().replace('-', '−');
