import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {betweenStages, prog} from '../lib/anim';
import {Row8, eightX} from '../lib/entropy8';
import {PAIRS8, PairMatrix} from '../lib/pairmatrix';

/**
 * 0: a pair of nodes is one cell of a matrix (nodes along both sides): the Rand index counts pairs of nodes.
 *    A pair is not drawn as two nodes joined by a line, which would read as a network edge.
 * 1: the matrix fades, one node lights: NMI looks at one node at a time.
 */
export const marks = [50, 100];

const CX = 960;
const ROW_Y = 520;
const GAP = 170;
const D = 96;
const PAIR = [1, 5] as const; // nodes 2 and 6
const ONE = 2; // node 3
const HOT = PAIRS8.find((p) => p.i === PAIR[0] && p.j === PAIR[1])!.k;

export const S14: React.FC = () => {
  const frame = useCurrentFrame();

  const pair = betweenStages(frame, marks, 0, 0);
  const one = betweenStages(frame, marks, 1, 1);
  const capPair = prog(frame, 24, 40);
  const capOne = prog(frame, 62, 76);

  return (
    <Frame n={14} title="Pairs or nodes?">
      <Canvas>
        <g opacity={pair}>
          <PairMatrix x={360} y={345} c={76} labels={false} boxes={false} hot={[HOT]} ringNodes={[...PAIR]} headerOp={prog(frame, 0, 16)} />
        </g>
        <g opacity={one}>
          <Row8 cx={CX} y={ROW_Y} gap={GAP} d={D} nodeOp={(i) => prog(frame, 50 + i * 1.5, 64 + i * 1.5)} lit={(i) => (i === ONE ? prog(frame, 60, 74) : 0)} />
        </g>
      </Canvas>
      <Fade o={pair * capPair} dy={14}>
        <Box x={1060} y={500} w={740} size={54}>
          Rand index: a pair of nodes
        </Box>
        <Box x={1060} y={680} w={740} size={45} color="#6b6b6b">
          One cell is one pair.
        </Box>
      </Fade>
      <Fade o={one * capOne} dy={14}>
        <Box x={CX} y={730} w={1400} align="center" size={54}>
          NMI: one node
        </Box>
      </Fade>
    </Frame>
  );
};
