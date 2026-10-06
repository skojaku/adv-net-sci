import React from 'react';
import {C, F} from '../theme';
import {AGG_SIZE, AGG_W, MERGE_PAIR, STUCK} from '../data/data';
import {CLUB_L} from './club';
import {LOOK, type Look} from './look';
import {mix, toCanvas, type Pt} from './network';

type P = readonly [number, number];

/**
 * Where the constructed bridge example (S21, S22; the nodes and edges are BR_EDGES in data.ts) is drawn: the same in both, so that S22 opens on the picture S21 ends with.
 * Two triangles (0 1 2) and (3 4 5), the bridge node 6 between them, and the triangle (7 8 9) hanging under the bridge: its edges do not cross the other nodes.
 */
export const BR_UNIT: number[][] = [
  [0.02, 0.18], [0.02, 0.62], [0.2, 0.4], // 0 1 2
  [0.8, 0.4], [0.98, 0.18], [0.98, 0.62], // 3 4 5
  [0.5, 0.4], // 6, the bridge
  [0.36, 1.0], [0.64, 1.0], [0.5, 0.78], // 7 8 9
];
export const BR_CANVAS: Pt[] = toCanvas(BR_UNIT, 460, 295, 1000, 345);

// ---------------------------------------------------------------- hulls

/** convex hull of points (Andrew's monotone chain) */
export const hullOf = (pts: ReadonlyArray<P>): P[] => {
  const p = [...pts].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  if (p.length < 3) return p;
  const cross = (o: P, a: P, b: P) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lower: P[] = [];
  for (const q of p) {
    while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], q) <= 0) lower.pop();
    lower.push(q);
  }
  const upper: P[] = [];
  for (const q of [...p].reverse()) {
    while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], q) <= 0) upper.pop();
    upper.push(q);
  }
  return [...lower.slice(0, -1), ...upper.slice(0, -1)];
};

/** A soft band around a group: the hull of its points, thickened by `pad` (a filled shape with a round stroke). */
export const Band: React.FC<{pts: ReadonlyArray<P>; pad: number; color: string; opacity?: number}> = ({pts, pad, color, opacity = 1}) => {
  if (!pts.length) return null;
  const h = hullOf(pts);
  if (h.length === 1) return <circle cx={h[0][0]} cy={h[0][1]} r={pad} fill={color} opacity={opacity} />;
  const d = h.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ') + ' Z';
  return <path d={d} fill={color} stroke={color} strokeWidth={pad * 2} strokeLinejoin="round" opacity={opacity} />;
};

/** A dashed ring around a few points: the circle that holds them, plus `pad`. */
export const DashRing: React.FC<{pts: ReadonlyArray<P>; pad: number; color: string; opacity?: number}> = ({pts, pad, color, opacity = 1}) => {
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
  const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  const r = Math.max(...pts.map((p) => Math.hypot(p[0] - cx, p[1] - cy))) + pad;
  return <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={5} strokeDasharray="14 11" opacity={opacity} />;
};

// ---------------------------------------------------------------- the network of groups

/** disc diameter of a supernode of `size` nodes */
export const discD = (size: number): number => 44 + 16 * Math.sqrt(size);

export type SDisc = {c: P; size: number; look: Look; op: number};
export type SLine = {a: P; b: P; count: number; op: number};
export type SLoop = {c: P; size: number; dir: P; count: number; op: number};

const lineW = (count: number) => 2 + 2 * count;

/**
 * Supernodes: a disc per group (its diameter grows with the number of nodes in it, and it carries that number), a thick line between two groups
 * (its width grows with the number of edges between them, and it carries that number), a small loop on a disc (the edges inside the group, with that number).
 * Draw it inside a <Canvas>.
 */
export const SuperNet: React.FC<{discs: ReadonlyArray<SDisc>; lines: ReadonlyArray<SLine>; loops: ReadonlyArray<SLoop>}> = ({discs, lines, loops}) => (
  <g fontFamily={F.serif}>
    {lines.map((l, i) =>
      l.op > 0.001 ? (
        <line key={`l${i}`} x1={l.a[0]} y1={l.a[1]} x2={l.b[0]} y2={l.b[1]} stroke={C.ink} strokeWidth={lineW(l.count)} strokeLinecap="round" opacity={0.7 * l.op} />
      ) : null,
    )}
    {loops.map((p, i) => {
      if (p.op <= 0.001) return null;
      const r = 28;
      const dist = discD(p.size) / 2 + r * 0.9;
      const lx = p.c[0] + p.dir[0] * dist;
      const ly = p.c[1] + p.dir[1] * dist;
      return (
        <g key={`o${i}`} opacity={p.op}>
          <circle cx={lx} cy={ly} r={r} fill="#fff" stroke={C.ink} strokeWidth={4.5} opacity={0.85} />
          <text x={lx} y={ly + 11} textAnchor="middle" fontSize={30} fontWeight={700} fill={C.ink}>
            {p.count}
          </text>
        </g>
      );
    })}
    {discs.map((d, i) =>
      d.op > 0.001 ? (
        <g key={`d${i}`} opacity={d.op}>
          <circle cx={d.c[0]} cy={d.c[1]} r={discD(d.size) / 2 - d.look.sw / 2} fill={d.look.fill} stroke={d.look.stroke} strokeWidth={d.look.sw} />
          <text x={d.c[0]} y={d.c[1] + 12} textAnchor="middle" fontSize={36} fontWeight={700} fill={d.look.text}>
            {d.size}
          </text>
        </g>
      ) : null,
    )}
    {lines.map((l, i) =>
      l.op > 0.001 ? (
        <g key={`t${i}`} opacity={l.op}>
          <rect x={(l.a[0] + l.b[0]) / 2 - 22} y={(l.a[1] + l.b[1]) / 2 - 22} width={44} height={44} rx={10} fill="#fff" />
          <text x={(l.a[0] + l.b[0]) / 2} y={(l.a[1] + l.b[1]) / 2 + 11} textAnchor="middle" fontSize={30} fontWeight={700} fill={C.ink}>
            {l.count}
          </text>
        </g>
      ) : null,
    )}
  </g>
);

// ---------------------------------------------------------------- the 5 groups of the stuck partition, in the drawing of the club (CLUB_L)

const centroid = (idx: ReadonlyArray<number>): P => [idx.reduce((s, v) => s + CLUB_L[v][0], 0) / idx.length, idx.reduce((s, v) => s + CLUB_L[v][1], 0) / idx.length];

export const GROUPS: number[][] = [0, 1, 2, 3, 4].map((g) => STUCK.map((s, v) => (s === g ? v : -1)).filter((v) => v >= 0));
export const CENTRES: P[] = GROUPS.map(centroid);
export const SIZES: number[] = [...AGG_SIZE];

const unit = (x: number, y: number): P => {
  const n = Math.hypot(x, y) || 1;
  return [x / n, y / n];
};
/** the direction in which a group's loop is drawn: away from the other groups */
const awayFrom = (c: P, others: ReadonlyArray<P>): P => {
  const mx = others.reduce((s, p) => s + p[0], 0) / others.length;
  const my = others.reduce((s, p) => s + p[1], 0) / others.length;
  return unit(c[0] - mx, c[1] - my);
};
export const DIRS: P[] = CENTRES.map((c, g) => awayFrom(c, CENTRES.filter((_, k) => k !== g)));

/** edges inside group g (the diagonal of AGG_W counts each of them twice) */
export const LOOP_COUNT: number[] = AGG_W.map((row, g) => row[g] / 2);
/** the pairs of groups that share edges, with the number of edges */
export const PAIRS: Array<{a: number; b: number; count: number}> = (() => {
  const out: Array<{a: number; b: number; count: number}> = [];
  for (let a = 0; a < 5; a++) for (let b = a + 1; b < 5; b++) if (AGG_W[a][b] > 0) out.push({a, b, count: AGG_W[a][b]});
  return out;
})();

/** the group that Louvain's second level builds: the two groups of MERGE_PAIR in one (S19) */
export const MERGED = (() => {
  const [g1, g2] = MERGE_PAIR;
  const members = [...GROUPS[g1], ...GROUPS[g2]];
  const c = centroid(members);
  const others = [0, 1, 2, 3, 4].filter((g) => g !== g1 && g !== g2);
  return {
    g1,
    g2,
    c,
    size: SIZES[g1] + SIZES[g2],
    loop: LOOP_COUNT[g1] + LOOP_COUNT[g2] + AGG_W[g1][g2],
    dir: awayFrom(c, others.map((g) => CENTRES[g])),
    /** edges from the merged group to each other group */
    to: others.map((g) => ({g, count: AGG_W[g1][g] + AGG_W[g2][g]})).filter((e) => e.count > 0),
  };
})();

/** tint of a group's colour, for a band */
export const tint = (look: Look, t = 0.8): string => mix(look.fill, '#ffffff', t);
export const GROUP_LOOKS = (hue: ReadonlyArray<number>): Look[] => hue.map((h) => LOOK[h]);
