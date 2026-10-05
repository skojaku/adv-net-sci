import React from 'react';
import {C, F} from '../theme';
import {SBM_SHUFFLE} from '../data/data';
import type {Edge, Pt} from './network';
import {LOOK, type Look} from './look';

/** The 8-node network of S18 to S20 on a ring: the same layout as S21 to S23 (`arcs8`). */
export {arcs8 as ring8} from './sbmLayout';

/** Layout shared by S19 and S20, so that S20 opens on the picture S19 ends on. */
export const PIC = {netCx: 480, netCy: 665, netR: 235, nodeD: 78, mx: 1040, my: 335, cell: 80} as const;

const toSlots = (order: ReadonlyArray<number>): number[] => {
  const p: number[] = Array(order.length).fill(0);
  order.forEach((node, slot) => {
    p[node] = slot;
  });
  return p;
};

/**
 * The shuffled order sorted by insertion: each state `SORT_STEPS[k]` lists the slot of every node. Step k moves one node
 * into its place and shifts the nodes it passes by one slot, so only one row and one column cross the others at a time.
 * (Sliding all rows at once folds the middle of the matrix into a blob, because the slots of the middle rows come together.)
 * The first state is the shuffled order, the last is the sorted order (node i in slot i).
 */
export const SORT_STEPS: number[][] = (() => {
  let order: number[] = [...SBM_SHUFFLE];
  const states = [toSlots(order)];
  for (let k = 0; k < order.length; k++) {
    if (order.indexOf(k) === k) continue;
    order = order.filter((n) => n !== k);
    order.splice(k, 0, k);
    states.push(toSlots(order));
  }
  return states;
})();

/** Slot of each node in the shuffled order. */
export const SHUFFLED_POS: number[] = SORT_STEPS[0];

/** Slot of each node when the nodes are sorted by group: node i in slot i. */
export const SORTED_POS: number[] = SORT_STEPS[SORT_STEPS.length - 1];

/** Slot of each node when step k of the sort is a fraction `progress[k]` done (0 to 1). Steps are added, so they may overlap in time. */
export const slotsAt = (progress: ReadonlyArray<number>): number[] =>
  SHUFFLED_POS.map((s0, a) => SORT_STEPS.slice(1).reduce((x, state, k) => x + (progress[k] ?? 0) * (state[a] - SORT_STEPS[k][a]), s0));

/**
 * The adjacency matrix of a network: a filled cell is an edge.
 * `pos[a]` is the row and column slot of node a; it may be fractional, so rows and columns can slide.
 * Each row and column is labelled with its node: the same disc as in the network (`look`, cross-faded to `lookTo` by `t`).
 */
export const AdjMatrix: React.FC<{
  x: number;
  y: number;
  cell: number;
  edges: ReadonlyArray<Edge>;
  pos: ReadonlyArray<number>;
  /** opacity of each edge's two cells */
  edgeOp?: (i: number, e: Edge) => number;
  /** the look of the label discs: one for all nodes, or one per node (default: blue) */
  look?: Look | ReadonlyArray<Look>;
  lookTo?: ReadonlyArray<Look>;
  t?: number;
  labelD?: number;
  labelSize?: number;
  fill?: string;
  opacity?: number;
}> = ({x, y, cell, edges, pos, edgeOp, look = LOOK[0], lookTo, t = 0, labelD = 50, labelSize = 34, fill = C.blue, opacity = 1}) => {
  const n = pos.length;
  const inset = 3;
  const size = n * cell;
  const lk = (a: number): Look => (Array.isArray(look) ? (look as ReadonlyArray<Look>)[a] : (look as Look));
  const off = labelD / 2 + 12;
  const disc = (cx: number, cy: number, l: Look, o: number, key: string) => (
    <circle key={key} cx={cx} cy={cy} r={labelD / 2 - l.sw / 2} fill={l.fill} stroke={l.stroke} strokeWidth={l.sw} opacity={o} />
  );
  return (
    <g opacity={opacity}>
      {Array.from({length: n * n}, (_, k) => {
        const r = Math.floor(k / n);
        const c = k % n;
        return <rect key={k} x={x + c * cell} y={y + r * cell} width={cell} height={cell} fill="#fff" stroke={C.rule} strokeWidth={2} />;
      })}
      {/* the diagonal (a node with itself) moves with its node */}
      {pos.map((p, a) => (
        <rect key={`d${a}`} x={x + p * cell} y={y + p * cell} width={cell} height={cell} fill={C.panel} stroke={C.rule} strokeWidth={2} />
      ))}
      <rect x={x} y={y} width={size} height={size} fill="none" stroke={C.soft} strokeWidth={3} />
      {edges.map((e, i) => {
        const o = edgeOp ? edgeOp(i, e) : 1;
        if (o <= 0.001) return null;
        const [a, b] = e;
        return (
          <g key={i} opacity={o}>
            <rect x={x + pos[b] * cell + inset} y={y + pos[a] * cell + inset} width={cell - 2 * inset} height={cell - 2 * inset} fill={fill} />
            <rect x={x + pos[a] * cell + inset} y={y + pos[b] * cell + inset} width={cell - 2 * inset} height={cell - 2 * inset} fill={fill} />
          </g>
        );
      })}
      {pos.map((p, a) => {
        const to = lookTo && t > 0.001 ? lookTo[a] : null;
        const shown = to && t > 0.5 ? to : lk(a);
        const spots = [
          [x - off, y + (p + 0.5) * cell],
          [x + (p + 0.5) * cell, y - off],
        ];
        return (
          <g key={`l${a}`} fontFamily={F.serif} fontSize={labelSize} fontWeight={700} fill={shown.text} textAnchor="middle">
            {spots.map(([cx, cy], k) => (
              <g key={k}>
                {disc(cx, cy, lk(a), 1, 'a')}
                {to && disc(cx, cy, to, t, 'b')}
                <text x={cx} y={cy + labelSize * 0.35}>{a + 1}</text>
              </g>
            ))}
          </g>
        );
      })}
    </g>
  );
};
