import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Network} from '../lib/network';
import {prog} from '../lib/anim';
import {sbmEdges} from '../lib/sbm';
import {AdjMatrix, PIC, SHUFFLED_POS, ring8} from '../lib/matrix';

/** 0: the network with every node alike, its adjacency matrix in a shuffled order, and the question. */
export const marks = [66];

const POS = ring8(PIC.netCx, PIC.netCy, PIC.netR);
const EDGES = sbmEdges(0.9, 0.1);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));

export const S23: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Frame n={23} title="Can we see the groups?">
      <Canvas>
        <Network
          pos={POS}
          edges={EDGES}
          nodeD={PIC.nodeD}
          nodeOp={(i) => prog(frame, 4 + 2 * i, 16 + 2 * i)}
          edgeOp={(i) => prog(frame, 14 + 2 * i, 26 + 2 * i)}
          edgeW={5}
          label={LABELS}
          labelSize={36}
        />
        <AdjMatrix
          x={PIC.mx}
          y={PIC.my}
          cell={PIC.cell}
          edges={EDGES}
          pos={SHUFFLED_POS}
          opacity={prog(frame, 10, 26)}
          edgeOp={(i) => prog(frame, 28 + 2 * i, 38 + 2 * i)}
        />
      </Canvas>
      <Fade o={prog(frame, 48, 62)} dy={14}>
        <Box x={960} y={184} w={1680} align="center" size={45}>
          Where are the two groups?
        </Box>
      </Fade>
    </Frame>
  );
};
