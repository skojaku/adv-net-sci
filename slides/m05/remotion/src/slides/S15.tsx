import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {prog} from '../lib/anim';
import {H_TRUE, HiddenNode, Row8, f3} from '../lib/entropy8';

/**
 * 0: eight nodes (4 solid, 4 hollow) and one node picked at random, its look hidden: solid or hollow?
 * 1: H(true) = 1.000, which is 1 question.
 */
export const marks = [50, 100];

const CX = 960;
const ROW_Y = 610;

export const S15: React.FC = () => {
  const frame = useCurrentFrame();

  const pick = prog(frame, 16, 32);
  const ask = prog(frame, 28, 44);
  const eq = prog(frame, 56, 74);
  const q1 = prog(frame, 72, 90);

  return (
    <Frame n={15} title="Guess the true group of a node">
      <Canvas>
        <Row8 cx={CX} y={ROW_Y} gap={150} nodeOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)} />
        <HiddenNode x={CX} y={320} halo={1} op={pick} />
      </Canvas>
      <Fade o={ask} dy={12}>
        <Box x={CX} y={400} w={1200} align="center" size={48}>
          A random node: solid or hollow?
        </Box>
      </Fade>
      <Fade o={eq} dy={14}>
        <Box x={CX} y={742} w={1200} align="center" size={64}>
          <Tex tex={`H(\\text{true}) = ${f3(H_TRUE)}`} />
        </Box>
      </Fade>
      <Fade o={q1} dy={14}>
        <Cap x={CX} y={850} w={1200}>
          1 question
        </Cap>
      </Fade>
    </Frame>
  );
};
