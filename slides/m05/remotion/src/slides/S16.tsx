import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {betweenStages, prog} from '../lib/anim';
import {GX, GY, CH, CW, MARG, Num, ProbGrid, cellC, colSumC, rowSumC} from '../components/ProbGrid';
import {JOINT, P_FOUND, P_TRUE, fmt} from '../lib/prob';

/**
 * 0: add up each row: the marginal probability of a true group.
 * 1: add up each column: the marginal probability of a found group.
 */
export const marks = [56, 116];

export const S16: React.FC = () => {
  const frame = useCurrentFrame();

  const rows = prog(frame, 10, 28);
  const cols = prog(frame, 64, 82);
  const cap0 = betweenStages(frame, marks, 0, 0) * prog(frame, 26, 42);
  const cap1 = betweenStages(frame, marks, 1, 1);

  return (
    <Frame n={16} title="Marginal probability">
      <Canvas>
        <ProbGrid rowsOp={rows} colsOp={cols} />
        {[0, 1].map((r) =>
          [0, 1].map((c) => <Num key={`${r}${c}`} at={cellC(r, c)} text={fmt(JOINT[r][c], 3)} size={64} color={C.soft} />),
        )}
        {[0, 1].map((r) => (
          <Num key={`r${r}`} at={rowSumC(r)} text={fmt(P_TRUE[r], 3)} size={64} bold op={rows} />
        ))}
        {[0, 1].map((c) => (
          <Num key={`c${c}`} at={colSumC(c)} text={fmt(P_FOUND[c], 3)} size={64} bold op={cols} />
        ))}
        <g fontFamily={F.hand} fontSize={45} fill={C.soft} textAnchor="middle">
          <text x={GX + 2 * CW + 20 + MARG / 2} y={GY - 30} opacity={rows}>
            true
          </text>
          <text x={GX - 80} y={GY + 2 * CH + 96} opacity={cols}>
            found
          </text>
        </g>
      </Canvas>
      <Fade o={cap0} dy={14}>
        <Box x={960} y={850} w={1500} align="center" size={54}>
          Add up each row: <Term>marginal probability</Term>
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={960} y={850} w={1500} align="center" size={54}>
          Add up each column: <Term>marginal probability</Term>
        </Box>
      </Fade>
    </Frame>
  );
};
