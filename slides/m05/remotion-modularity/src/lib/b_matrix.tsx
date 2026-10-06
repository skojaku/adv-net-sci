import React from 'react';
import {C, F} from '../theme';
import {LOOK, type Look} from './look';
import {Network, mix, toCanvas} from './network';
import {DEG, KARATE_EDGES, KARATE_REAL, TOY_DEG, TOY_EDGES, TOY_POS, TWO_M} from '../data/data';

/* ---------- the matrices, computed from data.ts (pure functions) ---------- */

/** The adjacency matrix: A[i][j] = 1 if i and j share an edge (symmetric, zero diagonal). */
export const adjacency = (n: number, edges: ReadonlyArray<ReadonlyArray<number>>): number[][] => {
  const a = Array.from({length: n}, () => Array<number>(n).fill(0));
  for (const [u, v] of edges) {
    a[u][v] = 1;
    a[v][u] = 1;
  }
  return a;
};

/** E[i][j] = k_i k_j / 2M: the edges expected between i and j in a random network with the same degrees. */
export const expected = (deg: ReadonlyArray<number>): number[][] => {
  const twoM = deg.reduce((s, k) => s + k, 0);
  return deg.map((ki) => deg.map((kj) => (ki * kj) / twoM));
};

/** B = A - E, the modularity matrix. */
export const modMatrix = (a: number[][], e: number[][]): number[][] => a.map((row, i) => row.map((v, j) => v - e[i][j]));

export const TOY_A = adjacency(6, TOY_EDGES);
export const TOY_E = expected(TOY_DEG);
export const TOY_B = modMatrix(TOY_A, TOY_E);

/** The club's nodes sorted by group (all REAL = 0 first), ties by node number. */
export const CLUB_ORDER: number[] = Array.from({length: KARATE_REAL.length}, (_, i) => i).sort((a, b) => KARATE_REAL[a] - KARATE_REAL[b] || a - b);
const clubA0 = adjacency(KARATE_REAL.length, KARATE_EDGES);
const clubE0 = expected(DEG);
const reorder = (m: number[][]) => CLUB_ORDER.map((i) => CLUB_ORDER.map((j) => m[i][j]));
export const CLUB_A = reorder(clubA0);
export const CLUB_E = reorder(clubE0);
export const CLUB_B = modMatrix(CLUB_A, CLUB_E);
/** the group of the node in each row (and column) of the sorted matrices */
export const CLUB_GROUP: number[] = CLUB_ORDER.map((i) => KARATE_REAL[i]);
export const CLUB_BAR: string[] = CLUB_GROUP.map((g) => LOOK[g].fill);
/** the number of nodes in the first group of the sorted club */
export const CLUB_SPLIT: number = CLUB_GROUP.filter((g) => g === 0).length;
if (TWO_M !== 156) throw new Error('data.ts changed: check the club numbers');

/** A number with two decimals and a true minus sign. */
export const num2 = (v: number): string => (v < -0.005 ? '−' : '') + Math.abs(v).toFixed(2);

/* ---------- colours of a cell ---------- */

const tint = (c: string, t: number) => mix('#ffffff', c, Math.max(0, Math.min(1, t)));
export const fillA = (v: number): string => (v > 0.5 ? C.blue : '#ffffff');
/** a value of E: blue, the darker the larger (vmax is the value that gets the darkest tint) */
export const fillE = (v: number, vmax: number): string => tint(C.blue, 0.55 * Math.pow(Math.min(1, v / vmax), 0.8));
/** a value of B: blue above 0, brown below 0 */
export const fillB = (v: number, vmax: number): string =>
  v >= 0 ? tint(C.blue, 0.65 * Math.pow(Math.min(1, v / vmax), 0.8)) : tint(C.brown, 0.65 * Math.pow(Math.min(1, -v / vmax), 0.8));

/* ---------- the matrix drawing ---------- */

/** consecutive equal colours as [colour, first index, one past the last index] (one bar per run, so that no seams show) */
const runs = (colors: ReadonlyArray<string>): Array<[string, number, number]> => {
  const out: Array<[string, number, number]> = [];
  colors.forEach((c, i) => {
    if (out.length && out[out.length - 1][0] === c) out[out.length - 1][2] = i + 1;
    else out.push([c, i, i + 1]);
  });
  return out;
};

export type CellStyle = {
  fill: string;
  /** a number or a short text in the cell; none for the colour maps */
  text?: string | null;
  color?: string;
  /** opacity of the cell's colour and text (the grid under it stays) */
  op?: number;
};

/**
 * An n x n matrix in canvas coordinates (an SVG group). `at(row, col)` says what a cell shows.
 * Optional: numbered discs at the left and the top (`discs`), two-colour bars outside (`bars`, the group of each row and column),
 * a ring round chosen cells (`rings`). The grid (light lines, shaded diagonal) is drawn when `grid` is true; the 34 x 34 colour maps have none.
 */
export const Matrix: React.FC<{
  x: number;
  y: number;
  cell: number;
  n: number;
  at: (r: number, c: number) => CellStyle;
  font?: number;
  grid?: boolean;
  discs?: {d: number; size: number; op?: number; look?: Look};
  bars?: {colors: ReadonlyArray<string>; t: number; gap?: number; op?: number};
  rings?: ReadonlyArray<readonly [number, number]>;
  ringOp?: number;
  /** a thin line after this many rows and columns (the border between the two groups of the sorted club) */
  splitAt?: number;
  opacity?: number;
}> = ({x, y, cell, n, at, font = 28, grid = true, discs, bars, rings, ringOp = 1, splitAt, opacity = 1}) => {
  const size = n * cell;
  const inset = grid ? 3 : 0;
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const s = at(r, c);
      const o = s.op ?? 1;
      if (o <= 0.001) continue;
      const has = s.fill.toLowerCase() !== '#ffffff' || (s.text !== undefined && s.text !== null);
      if (!has) continue;
      cells.push(
        <g key={r * n + c} opacity={o}>
          <rect x={x + c * cell + inset} y={y + r * cell + inset} width={cell - 2 * inset} height={cell - 2 * inset} fill={s.fill} />
          {s.text != null && (
            <text x={x + (c + 0.5) * cell} y={y + (r + 0.5) * cell + font * 0.35} textAnchor="middle" fontFamily={F.serif} fontSize={font} fill={s.color ?? C.ink} style={{fontVariantNumeric: 'tabular-nums'}}>
              {s.text}
            </text>
          )}
        </g>,
      );
    }
  }
  const lk = discs?.look ?? LOOK[0];
  const off = discs ? discs.d / 2 + 10 : 0;
  return (
    <g opacity={opacity}>
      {grid &&
        Array.from({length: n * n}, (_, k) => {
          const r = Math.floor(k / n);
          const c = k % n;
          return <rect key={k} x={x + c * cell} y={y + r * cell} width={cell} height={cell} fill={r === c ? C.panel : '#fff'} stroke={C.rule} strokeWidth={2} />;
        })}
      {cells}
      <rect x={x} y={y} width={size} height={size} fill="none" stroke={C.soft} strokeWidth={grid ? 3 : 2} />
      {splitAt !== undefined && (
        <g stroke={C.ink} strokeWidth={1.5} opacity={0.55}>
          <line x1={x + splitAt * cell} y1={y} x2={x + splitAt * cell} y2={y + size} />
          <line x1={x} y1={y + splitAt * cell} x2={x + size} y2={y + splitAt * cell} />
        </g>
      )}
      {bars && (
        <g opacity={bars.op ?? 1}>
          {runs(bars.colors).map(([col, from, to], i) => (
            <g key={i}>
              <rect x={x - (bars.gap ?? 6) - bars.t} y={y + from * cell} width={bars.t} height={(to - from) * cell} fill={col} />
              <rect x={x + from * cell} y={y - (bars.gap ?? 6) - bars.t} width={(to - from) * cell} height={bars.t} fill={col} />
            </g>
          ))}
        </g>
      )}
      {discs &&
        Array.from({length: n}, (_, a) => (
          <g key={a} opacity={discs.op ?? 1} fontFamily={F.serif} fontSize={discs.size} fontWeight={700} fill={lk.text} textAnchor="middle">
            {[
              [x - off, y + (a + 0.5) * cell],
              [x + (a + 0.5) * cell, y - off],
            ].map(([cx, cy], k) => (
              <g key={k}>
                <circle cx={cx} cy={cy} r={discs.d / 2 - lk.sw / 2} fill={lk.fill} stroke={lk.stroke} strokeWidth={lk.sw} />
                <text x={cx} y={cy + discs.size * 0.35}>{a + 1}</text>
              </g>
            ))}
          </g>
        ))}
      {rings?.map(([r, c], k) => (
        <rect key={k} opacity={ringOp} x={x + c * cell + 2} y={y + r * cell + 2} width={cell - 4} height={cell - 4} fill="none" stroke={C.ink} strokeWidth={6} />
      ))}
    </g>
  );
};

/* ---------- the layout that S09, S10 and S11 share (S11 opens on S10's last picture) ---------- */

export const TOY = {
  /** the small network, at the left */
  net: toCanvas(TOY_POS, 120, 330, 630, 300),
  /** the matrix, at the right (S09 and S10) */
  mx: 1010,
  my: 285,
  cell: 100,
  /** the Tex label of the matrix above the network, the formula under it, the sentence under that */
  labelY: 205,
  formulaY: 690,
  captionY: 810,
} as const;

/** Degree tags next to the nodes of the small network ("k = 2"): above the top nodes and the middle ones, below the bottom ones. */
const DEG_BELOW = [false, true, false, false, false, true];

export const ToyNet: React.FC<{degrees?: number; opacity?: number}> = ({degrees = 0, opacity = 1}) => (
  <g opacity={opacity}>
    <Network pos={TOY.net} edges={TOY_EDGES as unknown as ReadonlyArray<readonly [number, number]>} look={LOOK[0]} nodeD={72} labelSize={34} edgeW={5} label={[1, 2, 3, 4, 5, 6]} />
    {degrees > 0.001 && (
      <g opacity={degrees} fontFamily={F.serif} fontSize={34} fill={C.soft} textAnchor="middle">
        {TOY.net.map((p, i) => (
          <text key={i} x={p[0]} y={p[1] + (DEG_BELOW[i] ? 80 : -52)}>
            k = {TOY_DEG[i]}
          </text>
        ))}
      </g>
    )}
  </g>
);

/** The degrees along the right and the bottom edge of the 6 x 6 matrix at (mx, my) with the given cell size. */
export const MatrixDegrees: React.FC<{x: number; y: number; cell: number; opacity?: number; font?: number}> = ({x, y, cell, opacity = 1, font = 30}) => (
  <g opacity={opacity} fontFamily={F.serif} fontSize={font} fill={C.soft} textAnchor="middle">
    {TOY_DEG.map((k, i) => (
      <g key={i}>
        <text x={x + 6 * cell + 34} y={y + (i + 0.5) * cell + font * 0.35}>{k}</text>
        <text x={x + (i + 0.5) * cell} y={y + 6 * cell + 40}>{k}</text>
      </g>
    ))}
    <text x={x + 6 * cell + 34} y={y - 14}>k</text>
    <text x={x - 34} y={y + 6 * cell + 40}>k</text>
  </g>
);
