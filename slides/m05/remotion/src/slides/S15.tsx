import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {C} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {Num, ProbGrid, cellC} from '../components/ProbGrid';
import {COUNT, JOINT, fmt} from '../lib/prob';

/**
 * The table of S09 as probabilities.
 * 0: the number of nodes in each cell.
 * 1: divided by 8, each cell is a joint probability: a node is in this true group AND this found group.
 */
export const marks = [50, 110];

export const S15: React.FC = () => {
  const frame = useCurrentFrame();

  const grid = prog(frame, 0, 16);
  const counts = betweenStages(frame, marks, 0, 0);
  const probs = fromStage(frame, marks, 1, 16);
  const cap0 = betweenStages(frame, marks, 0, 0) * prog(frame, 24, 40);

  return (
    <Frame n={15} zoom={1.15} top={245}>
      <Canvas>
        <ProbGrid op={grid} />
        {[0, 1].map((r) =>
          [0, 1].map((c) => (
            <g key={`${r}${c}`}>
              <Num at={cellC(r, c)} text={String(COUNT[r][c])} size={72} op={counts * grid} />
              <Num at={cellC(r, c)} text={fmt(JOINT[r][c], 3)} size={64} op={probs} />
            </g>
          )),
        )}
      </Canvas>
      <Fade o={cap0} dy={14}>
        <Box x={960} y={760} w={1500} align="center" size={54}>
          Count the nodes in each cell.
        </Box>
      </Fade>
      <Fade o={probs} dy={14}>
        <Box x={960} y={760} w={1500} align="center" size={54}>
          Divide by 8: <Term>joint probability</Term>
        </Box>
        <Cap x={960} y={850} w={1500}>
          a node is in this row and this column
        </Cap>
      </Fade>
    </Frame>
  );
};
