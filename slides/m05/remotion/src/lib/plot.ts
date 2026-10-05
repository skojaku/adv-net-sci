export type Pt = readonly [number, number];

export const TAU = Math.PI * 2;

export const toPath = (pts: ReadonlyArray<Pt>): string =>
  pts.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');

export const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;

export const clamp = (x: number, lo: number, hi: number): number => Math.min(hi, Math.max(lo, x));
