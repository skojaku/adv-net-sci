// Partition scores, written out so a slide can show every term. Checked against scikit-learn in
// scripts/verify_numbers.py (same values) and by scripts/check_metrics.mjs.

export const choose2 = (n: number) => (n * (n - 1)) / 2;

const counts = (x: ReadonlyArray<number>) => {
  const m = new Map<number, number>();
  x.forEach((v) => m.set(v, (m.get(v) ?? 0) + 1));
  return m;
};

/** Entropy in bits: the average number of yes/no questions needed to name a node's group. */
export const entropy = (x: ReadonlyArray<number>): number => {
  const n = x.length;
  let h = 0;
  counts(x).forEach((c) => {
    const p = c / n;
    h -= p * Math.log2(p);
  });
  return h;
};

/** Mutual information in bits. */
export const mutualInfo = (x: ReadonlyArray<number>, y: ReadonlyArray<number>): number => {
  const n = x.length;
  const cx = counts(x);
  const cy = counts(y);
  const joint = new Map<string, number>();
  x.forEach((a, i) => joint.set(`${a},${y[i]}`, (joint.get(`${a},${y[i]}`) ?? 0) + 1));
  let mi = 0;
  joint.forEach((c, key) => {
    const [a, b] = key.split(',').map(Number);
    mi += (c / n) * Math.log2((c / n) / ((cx.get(a)! / n) * (cy.get(b)! / n)));
  });
  return mi;
};

/** NMI = 2 I / (H(x) + H(y)). */
export const nmi = (x: ReadonlyArray<number>, y: ReadonlyArray<number>): number =>
  (2 * mutualInfo(x, y)) / (entropy(x) + entropy(y));

/** For every pair of nodes: together or apart in x, together or apart in y. */
export const pairCounts = (x: ReadonlyArray<number>, y: ReadonlyArray<number>) => {
  let both = 0;
  let xOnly = 0;
  let yOnly = 0;
  let neither = 0;
  for (let i = 0; i < x.length; i++) {
    for (let j = i + 1; j < x.length; j++) {
      const sx = x[i] === x[j];
      const sy = y[i] === y[j];
      if (sx && sy) both++;
      else if (sx) xOnly++;
      else if (sy) yOnly++;
      else neither++;
    }
  }
  return {both, xOnly, yOnly, neither};
};

export const randIndex = (x: ReadonlyArray<number>, y: ReadonlyArray<number>): number => {
  const p = pairCounts(x, y);
  return (p.both + p.neither) / (p.both + p.xOnly + p.yOnly + p.neither);
};

/** The Rand index a random relabeling of the same group sizes is expected to get. */
export const expectedRand = (x: ReadonlyArray<number>, y: ReadonlyArray<number>): number => {
  const N = choose2(x.length);
  let A = 0;
  counts(x).forEach((c) => (A += choose2(c)));
  let B = 0;
  counts(y).forEach((c) => (B += choose2(c)));
  const ea = (A * B) / N;
  return (N + 2 * ea - A - B) / N;
};

/** ARI = (Rand - expected Rand) / (1 - expected Rand). */
export const ari = (x: ReadonlyArray<number>, y: ReadonlyArray<number>): number => {
  const e = expectedRand(x, y);
  return (randIndex(x, y) - e) / (1 - e);
};

/** The eight-node example of S09 to S15: nodes 1 to 4 blue, 5 to 8 red; found A = 1 to 5, B = 6 to 8. */
export const TRUTH8 = [0, 0, 0, 0, 1, 1, 1, 1] as const;
export const FOUND8 = [0, 0, 0, 0, 0, 1, 1, 1] as const;
export const ALONE8 = [0, 1, 2, 3, 4, 5, 6, 7] as const;
