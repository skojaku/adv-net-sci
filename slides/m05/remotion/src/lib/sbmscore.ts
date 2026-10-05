import {SBM_PAIRS, sbmEdges} from './sbm';

/**
 * Scores of a grouping of the 8-node network of S23 to S28 (12 edges), computed exactly.
 * Natural logarithms; 0 log 0 = 0.
 *   maximum likelihood:  log L(c) = sum over pairs of groups r <= s of  m log(m / n) + (n - m) log(1 - m / n)
 *   Bayesian (simple):   log P(c) + sum over r <= s of  log[ m! (n - m)! / (n + 1)! ]
 *   (a uniform prior on every block probability, integrated out; P(K) = 1/8 and P(c | K) uniform over the groupings into K groups)
 * Peixoto's models use finer priors; this is the same idea in its simplest form.
 */
const EDGE_SET = new Set(sbmEdges(0.9, 0.1).map(([a, b]) => `${a},${b}`));
const isEdge = (a: number, b: number) => EDGE_SET.has(`${Math.min(a, b)},${Math.max(a, b)}`);
const N = 8;

const LOGFACT: number[] = [0];
for (let i = 1; i <= 40; i++) LOGFACT.push(LOGFACT[i - 1] + Math.log(i));

/** edges m and pairs n in every block (r, s), r <= s */
export const blocksOf = (c: ReadonlyArray<number>) => {
  const K = Math.max(...c) + 1;
  const m: number[][] = Array.from({length: K}, () => Array(K).fill(0));
  const n: number[][] = Array.from({length: K}, () => Array(K).fill(0));
  for (const [a, b] of SBM_PAIRS) {
    const r = Math.min(c[a], c[b]);
    const s = Math.max(c[a], c[b]);
    n[r][s] += 1;
    if (isEdge(a, b)) m[r][s] += 1;
  }
  return {K, m, n};
};

const blockLik = (m: number, n: number) => (m === 0 || m === n ? 0 : m * Math.log(m / n) + (n - m) * Math.log(1 - m / n));
const blockBayes = (m: number, n: number) => LOGFACT[m] + LOGFACT[n - m] - LOGFACT[n + 1];

export const logLik = (c: ReadonlyArray<number>): number => {
  const {K, m, n} = blocksOf(c);
  let t = 0;
  for (let r = 0; r < K; r++) for (let s = r; s < K; s++) if (n[r][s] > 0) t += blockLik(m[r][s], n[r][s]);
  return t;
};
export const logMarginal = (c: ReadonlyArray<number>): number => {
  const {K, m, n} = blocksOf(c);
  let t = 0;
  for (let r = 0; r < K; r++) for (let s = r; s < K; s++) if (n[r][s] > 0) t += blockBayes(m[r][s], n[r][s]);
  return t;
};

/** Stirling numbers of the second kind: the number of groupings of n nodes into k non-empty groups */
const stirling = (n: number, k: number): number => {
  const S: number[][] = Array.from({length: n + 1}, () => Array(k + 1).fill(0));
  S[0][0] = 1;
  for (let i = 1; i <= n; i++) for (let j = 1; j <= Math.min(i, k); j++) S[i][j] = j * S[i - 1][j] + S[i - 1][j - 1];
  return S[n][k];
};
export const logPrior = (K: number): number => -Math.log(stirling(N, K)) - Math.log(N);

/** best score over all 4140 groupings of the 8 nodes into exactly K groups, K = 1 to 8 (index K - 1) */
export const BEST_LIK: number[] = Array(N).fill(-Infinity);
export const BEST_BAYES: number[] = Array(N).fill(-Infinity);
const walk = (cur: number[], groups: number) => {
  if (cur.length === N) {
    BEST_LIK[groups - 1] = Math.max(BEST_LIK[groups - 1], logLik(cur));
    BEST_BAYES[groups - 1] = Math.max(BEST_BAYES[groups - 1], logMarginal(cur) + logPrior(groups));
    return;
  }
  for (let g = 0; g <= groups; g++) {
    cur.push(g);
    walk(cur, Math.max(groups, g + 1));
    cur.pop();
  }
};
walk([0], 1);

// checked against the exact enumeration in scripts/verify_numbers.py
const WANT_LIK = [-19.121, -6.444, -3.014, -1.386, 0, 0, 0, 0];
const WANT_BAYES = [-22.677, -18.213, -20.33, -21.85, -22.596, -22.912, -23.094, -21.488];
WANT_LIK.forEach((w, i) => {
  if (Math.abs(BEST_LIK[i] - w) > 2e-3) throw new Error(`sbmscore: best log L for K = ${i + 1} is ${BEST_LIK[i]}, expected ${w}`);
});
WANT_BAYES.forEach((w, i) => {
  if (Math.abs(BEST_BAYES[i] - w) > 2e-3) throw new Error(`sbmscore: best Bayesian score for K = ${i + 1} is ${BEST_BAYES[i]}, expected ${w}`);
});
for (let i = 1; i < N; i++) if (BEST_LIK[i] < BEST_LIK[i - 1] - 1e-12) throw new Error('sbmscore: log L decreased with K');
