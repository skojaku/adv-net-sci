import React from 'react';
import {C, F} from '../theme';
import {BR_EDGES} from '../data/data';
import {groupEdgeLook, groupEdgeOp} from './c_trace';
import {BR_CANVAS, DashRing} from './c_super';
import {type Look} from './look';
import {Network, type Edge} from './network';

const EDGES = BR_EDGES as unknown as ReadonlyArray<Edge>;
const LEFT = [0, 1, 2];
const RIGHT = [3, 4, 5];
const NODES = BR_CANVAS.length;
const PAD = 38;

const ringOf = (idx: number[]) => {
  const pts = idx.map((i) => BR_CANVAS[i]);
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
  const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  return {cx, cy, r: Math.max(...pts.map((p) => Math.hypot(p[0] - cx, p[1] - cy))) + PAD};
};
const L = ringOf(LEFT);
const R = ringOf(RIGHT);

/**
 * The constructed bridge example, drawn in <Canvas>: S21 and S22 share it.
 * `lab` is the grouping at this moment (edges inside a group are heavy), `looks` the colour of every node, `lookTo` and `t` a cross-fade of some nodes.
 * `dim` (0 to 1) pales the bridge and the third group, which are not the point of the picture while the two pieces are looked at.
 */
export const BridgeScene: React.FC<{
  lab: ReadonlyArray<number>;
  looks: ReadonlyArray<Look>;
  lookTo?: ReadonlyArray<Look>;
  t?: number;
  /** the grouping to draw edges with (labels and looks of the cross-fade's finished side when t > 0.5) */
  edgeLab?: ReadonlyArray<number>;
  edgeLooks?: ReadonlyArray<Look>;
  nodeAppear?: (i: number) => number;
  edgeAppear?: (i: number) => number;
  dim?: number;
  /** a ring round the bridge node */
  bridgeRing?: number;
  /** dashed rings round the two triangles, with the colour of each */
  rings?: {o: number; left: string; right: string};
  /** the mark "no edge between" */
  gap?: number;
  /** the word "bridge" above node 6 */
  bridgeLabel?: number;
}> = ({lab, looks, lookTo, t = 0, edgeLab, edgeLooks, nodeAppear, edgeAppear, dim = 0, bridgeRing = 0, rings, gap = 0, bridgeLabel = 0}) => {
  const el = edgeLab ?? lab;
  const ek = edgeLooks ?? looks;
  const opE = groupEdgeOp(el, ek);
  const lkE = groupEdgeLook(el, ek);
  const dimOf = (i: number) => (i >= 6 ? 1 - 0.55 * dim : 1);
  const b = BR_CANVAS[6];
  const yMark = Math.min(L.cy, R.cy) - 92;
  return (
    <g fontFamily={F.hand}>
      <Network
        pos={BR_CANVAS}
        edges={EDGES}
        look={looks}
        lookTo={lookTo}
        t={t}
        nodeD={52}
        nodeOp={(i) => (nodeAppear ? nodeAppear(i) : 1) * dimOf(i)}
        edgeOp={(i, e) => (edgeAppear ? edgeAppear(i) : 1) * opE(i, e) * (e[0] >= 6 || e[1] >= 6 ? 1 - 0.55 * dim : 1)}
        edgeLook={lkE}
      />
      {bridgeRing > 0.001 && <circle cx={b[0]} cy={b[1]} r={26 + 12} fill="none" stroke={C.ink} strokeWidth={7} opacity={bridgeRing} />}
      {bridgeLabel > 0.001 && (
        <text x={b[0]} y={b[1] - 56} textAnchor="middle" fontSize={44} fill={C.soft} opacity={bridgeLabel}>
          bridge
        </text>
      )}
      {rings && rings.o > 0.001 && (
        <>
          <DashRing pts={LEFT.map((i) => BR_CANVAS[i])} pad={PAD} color={rings.left} opacity={rings.o} />
          <DashRing pts={RIGHT.map((i) => BR_CANVAS[i])} pad={PAD} color={rings.right} opacity={rings.o} />
        </>
      )}
      {gap > 0.001 && (
        <g opacity={gap}>
          <line x1={L.cx + L.r + 14} y1={yMark + 34} x2={R.cx - R.r - 14} y2={yMark + 34} stroke={C.soft} strokeWidth={4} strokeDasharray="12 10" />
          <g stroke={C.ink} strokeWidth={6} strokeLinecap="round">
            <line x1={(L.cx + R.cx) / 2 - 15} y1={yMark + 19} x2={(L.cx + R.cx) / 2 + 15} y2={yMark + 49} />
            <line x1={(L.cx + R.cx) / 2 - 15} y1={yMark + 49} x2={(L.cx + R.cx) / 2 + 15} y2={yMark + 19} />
          </g>
          <text x={(L.cx + R.cx) / 2} y={yMark} textAnchor="middle" fontSize={44} fill={C.soft}>
            no edge between
          </text>
        </g>
      )}
    </g>
  );
};

export {NODES as BR_NODES};
