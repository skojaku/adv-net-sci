import {SBM_GROUP, sbmEdges} from './sbm';

/**
 * The 8-node network of S23 to S31 (12 edges, true split 1 to 4 against 5 to 8) seen by the degree-corrected SBM.
 * The convention of Karrer and Newman: m_rs counts the edges between groups r and s, an edge inside a group twice, so that
 * kappa_r = sum_s m_rs is the total degree of group r. (scripts/verify_dcsbm.py checks every identity used in S35 to S38.)
 */
export const DC_EDGES = sbmEdges(0.9, 0.1);
export const DC_GROUP = SBM_GROUP;

export const DEG = (() => {
  const d = new Array<number>(8).fill(0);
  for (const [a, b] of DC_EDGES) {
    d[a]++;
    d[b]++;
  }
  return d;
})();

export const M2: [[number, number], [number, number]] = [
  [0, 0],
  [0, 0],
];
for (const [a, b] of DC_EDGES) {
  M2[DC_GROUP[a]][DC_GROUP[b]]++;
  M2[DC_GROUP[b]][DC_GROUP[a]]++;
}
export const KAPPA: [number, number] = [M2[0][0] + M2[0][1], M2[1][0] + M2[1][1]];
export const TWO_M = 2 * DC_EDGES.length;

/** theta-hat_i = k_i / kappa_{c_i} */
export const THETA = DEG.map((k, i) => k / KAPPA[DC_GROUP[i]]);
/** the edges between r and s that the degrees alone would give: kappa_r kappa_s / 2m */
export const FROM_DEGREES: [[number, number], [number, number]] = [
  [(KAPPA[0] * KAPPA[0]) / TWO_M, (KAPPA[0] * KAPPA[1]) / TWO_M],
  [(KAPPA[1] * KAPPA[0]) / TWO_M, (KAPPA[1] * KAPPA[1]) / TWO_M],
];

if (
  DEG.join() !== '2,3,2,4,3,3,4,3' ||
  M2.flat().join() !== '10,1,1,12' ||
  KAPPA.join() !== '11,13' ||
  TWO_M !== 24 ||
  FROM_DEGREES.flat().map((x) => x.toFixed(2)).join() !== '5.04,5.96,5.96,7.04'
) {
  throw new Error('dc8: the 8-node network is not the one checked in scripts/verify_dcsbm.py');
}
