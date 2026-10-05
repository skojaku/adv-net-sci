import React from 'react';
import {C} from '../theme';

export type Pt = readonly [number, number];

/** Disc diameter in the ring figures: 39px (the Marp floor is 39px at this scale). */
export const NODE_D = 39;
/** Half the base of a triangle, and the room one triangle takes along the ring. */
const SIDE = 28;
const SLOT = 120;
const BAND = 34;

/**
 * A ring of triangles. Triangle i has nodes a, b, c; one edge joins b of triangle i to a of
 * triangle i+1. m = 4n edges for n triangles.
 *
 * `w[i]` in [0, 1] is how present triangle i is. The ring is laid out for the total weight, so a
 * triangle that fades in pushes the others apart instead of overlapping them.
 */
export const ringLayout = (w: number[], cx: number, cy: number, scale = 1, slot = SLOT) => {
  const total = Math.max(w.reduce((a, b) => a + b, 0), 3);
  const s = SIDE * scale;
  const h = Math.sqrt(3) * s;
  const R = Math.max(120 * scale, (slot * scale * total) / (2 * Math.PI));
  let acc = 0;
  const tri = w.map((wi) => {
    const theta = -Math.PI / 2 + (2 * Math.PI * (acc + wi / 2)) / total;
    acc += wi;
    const ux = Math.cos(theta);
    const uy = Math.sin(theta); // radial
    const tx = -uy;
    const ty = ux; // tangent, towards the next triangle
    const px = cx + R * ux;
    const py = cy + R * uy;
    const a: Pt = [px - s * tx - (h / 3) * ux, py - s * ty - (h / 3) * uy];
    const b: Pt = [px + s * tx - (h / 3) * ux, py + s * ty - (h / 3) * uy];
    const c: Pt = [px + ((2 * h) / 3) * ux, py + ((2 * h) / 3) * uy];
    return {a, b, c};
  });
  return {tri, R};
};

const blob = (pts: Pt[], links: [Pt, Pt][], color: string, opacity: number, key: string, rad = BAND) => (
  <g key={key} opacity={opacity}>
    {links.map(([p, q], i) => (
      <line key={i} x1={p[0]} y1={p[1]} x2={q[0]} y2={q[1]} stroke={color} strokeWidth={2 * rad} strokeLinecap="round" />
    ))}
    {pts.map((p, i) => (
      <circle key={`c${i}`} cx={p[0]} cy={p[1]} r={rad} fill={color} />
    ))}
  </g>
);

/**
 * Draws the ring. `apart` and `pairs` are the opacities of the two groupings' bands:
 * blue bands, one per triangle; red bands, one per two neighbouring triangles.
 */
export const Ring: React.FC<{
  w: number[];
  cx: number;
  cy: number;
  scale?: number;
  slot?: number;
  apart?: number;
  pairs?: number;
  opacity?: number;
}> = ({w, cx, cy, scale = 1, slot = SLOT, apart = 0, pairs = 0, opacity = 1}) => {
  const {tri} = ringLayout(w, cx, cy, scale, slot);
  const N = w.reduce((last, wi, i) => (wi > 0.001 ? i + 1 : last), 0);
  const rad = BAND * scale;
  const els: React.ReactNode[] = [];

  // bands first, so edges and discs sit on top
  if (apart > 0.001) {
    tri.forEach((t, i) => {
      if (w[i] < 0.001) return;
      els.push(blob([t.a, t.b, t.c], [[t.a, t.b], [t.b, t.c], [t.a, t.c]], C.blue, 0.3 * apart * w[i], `ba${i}`, rad));
    });
  }
  if (pairs > 0.001) {
    for (let k = 0; 2 * k < N; k++) {
      const i = 2 * k;
      const j = i + 1;
      const wi = w[i];
      const wj = j < N ? w[j] : 0;
      const T = tri[i];
      if (wj > 0.001) {
        const U = tri[j];
        els.push(
          blob(
            [T.a, T.b, T.c, U.a, U.b, U.c],
            [[T.a, T.b], [T.b, T.c], [T.a, T.c], [T.b, U.a], [U.a, U.b], [U.b, U.c], [U.a, U.c]],
            C.red,
            0.3 * pairs * Math.min(wi, wj),
            `bp${k}`,
            rad,
          ),
        );
      }
      if (wj < 0.999) {
        els.push(blob([T.a, T.b, T.c], [[T.a, T.b], [T.b, T.c], [T.a, T.c]], C.red, 0.3 * pairs * wi * (1 - wj), `bs${k}`, rad));
      }
    }
  }

  const edge = (p: Pt, q: Pt, op: number, key: string) =>
    op > 0.001 ? <line key={key} x1={p[0]} y1={p[1]} x2={q[0]} y2={q[1]} stroke={C.ink} strokeWidth={4} opacity={0.8 * op} /> : null;

  tri.forEach((t, i) => {
    if (w[i] < 0.001) return;
    els.push(edge(t.a, t.b, w[i], `ab${i}`), edge(t.b, t.c, w[i], `bc${i}`), edge(t.a, t.c, w[i], `ac${i}`));
  });
  // ring edges: b of triangle i to a of triangle i+1, and the closing edge that moves as the last triangle arrives
  for (let i = 0; i + 1 < N; i++) els.push(edge(tri[i].b, tri[i + 1].a, Math.min(w[i], w[i + 1]), `r${i}`));
  if (N >= 2) {
    els.push(edge(tri[N - 1].b, tri[0].a, Math.min(w[N - 1], w[0]), 'close'));
    if (N >= 3) els.push(edge(tri[N - 2].b, tri[0].a, 1 - w[N - 1], 'close2'));
  }
  tri.forEach((t, i) => {
    if (w[i] < 0.001) return;
    [t.a, t.b, t.c].forEach((p, k) =>
      els.push(
        <circle key={`n${i}${k}`} cx={p[0]} cy={p[1]} r={(NODE_D * scale) / 2} fill={C.blue} stroke="#fff" strokeWidth={3} opacity={w[i]} />,
      ),
    );
  });

  return <g opacity={opacity}>{els}</g>;
};

/** The Q of the two groupings of a ring of n triangles (n even). */
export const qApart = (n: number) => 3 / 4 - 1 / n;
export const qPairs = (n: number) => 7 / 8 - 2 / n;
