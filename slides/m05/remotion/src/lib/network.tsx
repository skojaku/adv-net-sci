import React from 'react';
import {C, F} from '../theme';
import {LOOK, type Look} from './look';

export type Pt = readonly [number, number];
export type Edge = readonly [number, number];

const hex = (c: string): [number, number, number] => [
  parseInt(c.slice(1, 3), 16),
  parseInt(c.slice(3, 5), 16),
  parseInt(c.slice(5, 7), 16),
];

/** Linear mix of two #rrggbb colours: t = 0 gives a, t = 1 gives b. */
export const mix = (a: string, b: string, t: number): string => {
  const [r1, g1, b1] = hex(a);
  const [r2, g2, b2] = hex(b);
  const f = (x: number, y: number) => Math.round(x + (y - x) * t);
  return `rgb(${f(r1, r2)}, ${f(g1, g2)}, ${f(b1, b2)})`;
};

/** Map unit-box positions onto the rectangle [x, x + w] x [y, y + h]. */
export const toCanvas = (unit: ReadonlyArray<ReadonlyArray<number>>, x: number, y: number, w: number, h: number): Pt[] =>
  unit.map((p) => [x + p[0] * w, y + p[1] * h] as const);

type Num<T> = number | ((i: number, item: T) => number);
const val = <T,>(v: Num<T> | undefined, i: number, item: T, dflt: number) => (v === undefined ? dflt : typeof v === 'number' ? v : v(i, item));

/**
 * A node-link drawing in canvas coordinates: edges under, discs on top.
 * `fill` is one colour for all nodes or one per node. `ring` draws an outline in a second colour
 * (for example the true group while the fill shows the found group). `label` writes a short text in
 * a disc (a degree, a node number).
 */
export const Network: React.FC<{
  pos: ReadonlyArray<Pt>;
  edges: ReadonlyArray<Edge>;
  /** one Look for all nodes, or one per node (see lib/look.ts); default: blue */
  look?: Look | ReadonlyArray<Look>;
  /** a second look per node, cross-faded in by `t` (0 = look only, 1 = lookTo only) */
  lookTo?: ReadonlyArray<Look>;
  t?: number;
  nodeD?: number;
  nodeOp?: Num<number>;
  edgeOp?: Num<Edge>;
  edgeColor?: string;
  edgeW?: number;
  /** an outline drawn around chosen nodes (for example the nodes that changed group) */
  ring?: ReadonlyArray<string | null>;
  ringW?: number;
  label?: ReadonlyArray<string | number | null>;
  labelSize?: number;
  opacity?: number;
}> = ({pos, edges, look = LOOK[0], lookTo, t = 0, nodeD = 46, nodeOp, edgeOp, edgeColor = C.ink, edgeW = 3.5, ring, ringW = 7, label, labelSize = 26, opacity = 1}) => {
  const lk = (i: number): Look => (Array.isArray(look) ? (look as ReadonlyArray<Look>)[i] : (look as Look));
  const disc = (p: Pt, l: Look, key: string, o: number) => (
    <circle key={key} cx={p[0]} cy={p[1]} r={nodeD / 2 - l.sw / 2} fill={l.fill} stroke={l.stroke} strokeWidth={l.sw} opacity={o} />
  );
  return (
    <g opacity={opacity}>
      {edges.map((e, i) => {
        const o = val(edgeOp, i, e, 1);
        return o > 0.001 ? (
          <line key={`e${i}`} x1={pos[e[0]][0]} y1={pos[e[0]][1]} x2={pos[e[1]][0]} y2={pos[e[1]][1]} stroke={edgeColor} strokeWidth={edgeW} opacity={0.7 * o} />
        ) : null;
      })}
      {pos.map((p, i) => {
        const o = val(nodeOp, i, i, 1);
        if (o <= 0.001) return null;
        const rg = ring?.[i];
        const to = lookTo && t > 0.001 ? lookTo[i] : null;
        const shown = to && t > 0.5 ? to : lk(i);
        return (
          <g key={`n${i}`} opacity={o}>
            {disc(p, lk(i), 'a', 1)}
            {to && disc(p, to, 'b', t)}
            {rg && <circle cx={p[0]} cy={p[1]} r={nodeD / 2 + ringW / 2 + 2} fill="none" stroke={rg} strokeWidth={ringW} />}
            {label?.[i] != null && (
              <text x={p[0]} y={p[1] + labelSize * 0.35} textAnchor="middle" fontFamily={F.serif} fontSize={labelSize} fontWeight={700} fill={shown.text}>
                {label[i]}
              </text>
            )}
          </g>
        );
      })}
    </g>
  );
};
