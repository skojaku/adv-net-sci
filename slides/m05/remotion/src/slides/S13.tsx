import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {C} from '../theme';
import {betweenStages, prog} from '../lib/anim';
import {Row8, eightX} from '../lib/entropy8';

/**
 * 0: two nodes lit and joined by a line: the Rand index counts pairs of nodes.
 * 1: the pair fades, one node lights: NMI looks at one node at a time.
 */
export const marks = [45, 90];

const CX = 960;
const ROW_Y = 520;
const GAP = 170;
const D = 96;
const PAIR = [1, 5] as const; // nodes 2 and 6
const ONE = 2; // node 3

export const S13: React.FC = () => {
  const frame = useCurrentFrame();

  const pair = betweenStages(frame, marks, 0, 0);
  const pairIn = prog(frame, 18, 34);
  const line = prog(frame, 24, 40);
  const one = betweenStages(frame, marks, 1, 1);
  const cap0 = betweenStages(frame, marks, 0, 0);
  const capIn = prog(frame, 30, 44);

  const xa = eightX(PAIR[0], CX, GAP);
  const xb = eightX(PAIR[1], CX, GAP);
  const arcTop = ROW_Y - D / 2 - 6;
  // an arc above the row joins the two nodes of the pair
  const arc = `M ${xa} ${arcTop} Q ${(xa + xb) / 2} ${arcTop - 190} ${xb} ${arcTop}`;

  return (
    <Frame n={13} title="Pairs or nodes?">
      <Canvas>
        <Row8 cx={CX} y={ROW_Y} gap={GAP} d={D} nodeOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)} lit={(i) => (PAIR.includes(i as 1 | 5) ? pair * pairIn : i === ONE ? one : 0)} />
        <path d={arc} fill="none" stroke={C.blue} strokeWidth={7} strokeLinecap="round" opacity={pair * line} />
      </Canvas>
      <Fade o={cap0 * capIn} dy={14}>
        <Box x={CX} y={730} w={1400} align="center" size={54}>
          Rand index: a pair of nodes
        </Box>
      </Fade>
      <Fade o={one * prog(frame, 62, 76)} dy={14}>
        <Box x={CX} y={730} w={1400} align="center" size={54}>
          NMI: one node
        </Box>
      </Fade>
    </Frame>
  );
};
