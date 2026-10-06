import React from 'react';
import {C} from '../theme';
import {type Look} from './look';
import {TOY_DEG, TOY_EDGES, TOY_POS, TOY_STUB_NODE} from '../data/data';
import {toCanvas, type Pt} from './network';
import {Box} from '../components/Text';

/** The small example of S05 to S11: a star joined to a triangle by one edge (6 nodes, 6 edges, degrees 3, 1, 1, 3, 2, 2). Shared helpers of S05 to S08. */

export const TOY_N = TOY_POS.length;
export const toyPos = (x: number, y: number, w: number, h: number): Pt[] => toCanvas(TOY_POS, x, y, w, h);

/** for every stub (an edge end, numbered as in data.ts), the edge it comes from and the node at the other end of that edge */
export const STUB_EDGE: number[] = [];
export const STUB_OTHER: number[] = [];
for (let n = 0; n < TOY_N; n++) {
  TOY_EDGES.forEach((e, k) => {
    if (e[0] === n || e[1] === n) {
      STUB_EDGE.push(k);
      STUB_OTHER.push(e[0] === n ? e[1] : e[0]);
    }
  });
}
if (STUB_EDGE.length !== TOY_STUB_NODE.length || TOY_STUB_NODE.some((n, s) => n !== TOY_EDGES[STUB_EDGE[s]].find((v) => v === n))) {
  throw new Error('a_toy: the stubs of data.ts do not match the edges');
}

export const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
export const lerpPos = (a: ReadonlyArray<Pt>, b: ReadonlyArray<Pt>, t: number): Pt[] => a.map((p, i) => [lerp(p[0], b[i][0], t), lerp(p[1], b[i][1], t)] as const);

/** a numbered disc (the node number is written in it) */
export const ToyDisc: React.FC<{p: Pt; d: number; look: Look; label: number | string; size?: number; o?: number}> = ({p, d, look, label, size = 40, o = 1}) => (
  <g opacity={o}>
    <circle cx={p[0]} cy={p[1]} r={d / 2 - look.sw / 2} fill={look.fill} stroke={look.stroke} strokeWidth={look.sw} />
    <text x={p[0]} y={p[1] + size * 0.35} textAnchor="middle" fontFamily="inherit" fontSize={size} fontWeight={700} fill={look.text}>
      {label}
    </text>
  </g>
);

// the degree label of a node goes above it (nodes 1 and 5 of the drawing: the top ones) or below it
const ABOVE = [true, false, false, false, true, false];

/** "k = 3" next to every node: a label of the slide (under five words) */
export const DegLabels: React.FC<{pos: ReadonlyArray<Pt>; d: number; size: number; o: number}> = ({pos, d, size, o}) => (
  <div style={{opacity: o}}>
    {pos.map((p, i) => (
      <Box key={i} x={p[0]} y={ABOVE[i] ? p[1] - d / 2 - size * 1.45 : p[1] + d / 2 + size * 0.1} w={220} align="center" size={size} color={C.soft} hand>
        <span style={{background: '#fff', padding: '0 10px'}}>k = {TOY_DEG[i]}</span>
      </Box>
    ))}
  </div>
);
