/** Geometry of two overlapping discs, for S14: the overlap (a lens) must have an exact area. */

/** Area of the overlap of discs with radii r1 and r2 whose centres are d apart. */
export const lensArea = (r1: number, r2: number, d: number): number => {
  if (d >= r1 + r2) return 0;
  if (d <= Math.abs(r1 - r2)) return Math.PI * Math.min(r1, r2) ** 2;
  const a1 = Math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1));
  const a2 = Math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2));
  const k = Math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2));
  return r1 * r1 * a1 + r2 * r2 * a2 - 0.5 * k;
};

/** The same area by summing thin vertical slices: an independent check of `lensArea`. */
export const lensAreaByIntegration = (r1: number, r2: number, d: number, steps = 40000): number => {
  const x0 = Math.max(-r1, d - r2);
  const x1 = Math.min(r1, d + r2);
  if (x1 <= x0) return 0;
  const dx = (x1 - x0) / steps;
  let area = 0;
  for (let i = 0; i < steps; i++) {
    const x = x0 + (i + 0.5) * dx;
    const h1 = Math.sqrt(Math.max(0, r1 * r1 - x * x));
    const h2 = Math.sqrt(Math.max(0, r2 * r2 - (x - d) * (x - d)));
    area += 2 * Math.min(h1, h2) * dx;
  }
  return area;
};

/** The centre distance at which the overlap has area `target`, by bisection (the area falls as d grows). */
export const distanceForOverlap = (r1: number, r2: number, target: number): number => {
  let lo = Math.abs(r1 - r2);
  let hi = r1 + r2;
  for (let i = 0; i < 80; i++) {
    const mid = (lo + hi) / 2;
    if (lensArea(r1, r2, mid) > target) lo = mid;
    else hi = mid;
  }
  return (lo + hi) / 2;
};
