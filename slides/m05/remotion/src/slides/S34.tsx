import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {C, F} from '../theme';
import {fromStage, prog} from '../lib/anim';
import {stackDots} from '../lib/dotstack';
import {KARATE_EDGES, NOISE_EDGES} from '../data/data';

/**
 * Real networks have hubs; a group of an SBM has one expected degree.
 * 0: the degrees of the karate club (34 nodes, 78 edges) as a dot plot.
 * 1: the degrees of the random network of S06 and S07 (the same numbers of nodes and edges): no node above 8.
 * 2: in an SBM, every node of a group has the same expected degree; to fit hubs the SBM makes a group of hubs.
 */
export const marks = [60, 120, 176];

const degrees = (edges: ReadonlyArray<readonly [number, number]>) => {
  const d = new Array<number>(34).fill(0);
  for (const [a, b] of edges) {
    d[a]++;
    d[b]++;
  }
  return d;
};
const KARATE = degrees(KARATE_EDGES);
const RANDOM = degrees(NOISE_EDGES);
if (Math.max(...KARATE) !== 17 || Math.max(...RANDOM) !== 8 || KARATE.reduce((a, b) => a + b, 0) !== 156 || RANDOM.reduce((a, b) => a + b, 0) !== 156) {
  throw new Error('S34: the degrees are not the expected ones');
}

const PX = 40; // px per degree
const DOT = 26;
const STEP = 28;
const BASE = 735;
const X0 = [140, 1000];
const place = (values: ReadonlyArray<number>) => stackDots(values, (v) => v * PX, PX);
const KP = place(KARATE);
const RP = place(RANDOM);

const Axis: React.FC<{x0: number; op: number}> = ({x0, op}) => (
  <g opacity={op}>
    <line x1={x0} y1={BASE} x2={x0 + 19 * PX} y2={BASE} stroke={C.soft} strokeWidth={3} />
    {[0, 5, 10, 15].map((d) => (
      <g key={d}>
        <line x1={x0 + (d + 0.5) * PX} y1={BASE} x2={x0 + (d + 0.5) * PX} y2={BASE + 10} stroke={C.soft} strokeWidth={3} />
        <text x={x0 + (d + 0.5) * PX} y={BASE + 52} textAnchor="middle" fontFamily={F.serif} fontSize={34} fill={C.soft}>
          {d}
        </text>
      </g>
    ))}
    <text x={x0 + 19 * PX} y={BASE + 52} textAnchor="end" fontFamily={F.hand} fontSize={40} fill={C.soft}>
      degree
    </text>
  </g>
);

export const S34: React.FC = () => {
  const frame = useCurrentFrame();

  const a = prog(frame, 0, 16);
  const capA = prog(frame, 6, 22);
  const dotA = (k: number) => prog(frame, 8 + 1.2 * k, 16 + 1.2 * k);
  const b = fromStage(frame, marks, 1, 14);
  const dotB = (k: number) => prog(frame, marks[0] + 8 + 1.2 * k, marks[0] + 16 + 1.2 * k);
  const text1 = fromStage(frame, marks, 2, 16);
  const text2 = prog(frame, marks[1] + 24, marks[1] + 42);

  return (
    <Frame n={34}>
      <Canvas>
        <Axis x0={X0[0]} op={a} />
        <Axis x0={X0[1]} op={b} />
        {KP.map((p, k) => (
          <circle key={`k${k}`} cx={X0[0] + p.x} cy={BASE - 16 - p.row * STEP} r={DOT / 2} fill={C.blue} stroke="#fff" strokeWidth={2} opacity={dotA(k)} />
        ))}
        {RP.map((p, k) => (
          <circle key={`r${k}`} cx={X0[1] + p.x} cy={BASE - 16 - p.row * STEP} r={DOT / 2} fill={C.blue} stroke="#fff" strokeWidth={2} opacity={dotB(k)} />
        ))}
      </Canvas>
      <Fade o={capA} dy={12}>
        <Cap x={X0[0]} y={232} w={760} align="left">karate club</Cap>
      </Fade>
      <Fade o={b} dy={12}>
        <Cap x={X0[1]} y={232} w={760} align="left">random network, the same numbers of nodes and edges</Cap>
      </Fade>
      <Fade o={text1} dy={14}>
        <Box x={120} y={835} w={1680} size={46}>
          In an SBM, every node of a group has the same expected degree.
        </Box>
      </Fade>
      <Fade o={text2} dy={14}>
        <Box x={120} y={897} w={1680} size={46}>
          To fit the hubs, the SBM makes a group of hubs.
        </Box>
      </Fade>
    </Frame>
  );
};
