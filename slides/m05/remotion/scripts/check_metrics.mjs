// node scripts/check_metrics.mjs  (after: npx esbuild src/lib/metrics.ts --format=esm --outfile=out/metrics.mjs)
import * as m from '../out/metrics.mjs';
const near = (a, b, t = 5e-4) => { if (Math.abs(a - b) > t) throw new Error(`${a} vs ${b}`); };
const {TRUTH8: t, FOUND8: f, ALONE8: s} = m;
near(m.randIndex(t, f), 0.75); near(m.ari(t, f), 0.4948); near(m.nmi(t, f), 0.5616);
near(m.entropy(t), 1); near(m.entropy(f), 0.954); near(m.mutualInfo(t, f), 0.549);
near(m.expectedRand(t, f), 0.505);
const p = m.pairCounts(t, f);
if (p.both !== 9 || p.xOnly !== 3 || p.yOnly !== 4 || p.neither !== 12) throw new Error(JSON.stringify(p));
near(m.randIndex(t, s), 16 / 28); near(m.nmi(t, s), 0.5); near(m.ari(t, s), 0);
console.log('metrics ok');
