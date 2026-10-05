import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {betweenStages, prog} from '../lib/anim';
import {Network, toCanvas} from '../lib/network';
import {NOISE_EDGES, NOISE_POS} from '../data/data';

/**
 * 0: 34 nodes, then the 78 random edges one at a time.
 * 1: the question. No answer on the slide.
 */
export const marks = [88, 124];

const POS = toCanvas(NOISE_POS, 160, 205, 900, 760);
const EDGES = NOISE_EDGES as unknown as [number, number][];

export const S06: React.FC = () => {
  const frame = useCurrentFrame();
  const nodeOp = (i: number) => prog(frame, 0.3 * i, 0.3 * i + 10);
  const edgeOp = (i: number) => prog(frame, 14 + 0.7 * i, 14 + 0.7 * i + 5);
  const cap = betweenStages(frame, marks, 0, 0);
  const capIn = prog(frame, 66, 84);
  const q = prog(frame, 94, 114);
  return (
    <Frame n={6} title="A network with no groups">
      <Canvas>
        <Network pos={POS} edges={EDGES} nodeD={46} nodeOp={nodeOp} edgeOp={edgeOp} />
      </Canvas>
      <Fade o={cap * capIn} dy={14}>
        <Cap x={1160} y={470} w={620} align="left">34 nodes, 78 edges, chosen at random.</Cap>
      </Fade>
      <Fade o={q} dy={16}>
        <Box x={1160} y={440} w={620} size={45}>
          We run Louvain on this network. What Q do we expect?
        </Box>
      </Fade>
    </Frame>
  );
};
