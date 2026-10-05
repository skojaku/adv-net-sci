import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {GX, GY, CH, CW, MARG, Num, ProbGrid, cellC, colSumC, rowSumC} from '../components/ProbGrid';
import {P_FOUND, P_TRUE, PRODUCT, RATIO, fmt} from '../lib/prob';

/**
 * The marginals stay on the table.
 * 0: if the two splits were unrelated, a cell's joint probability would be its two marginals multiplied.
 * 1: the ratio joint / (marginal x marginal): above 1 the pair of groups occurs more often than chance, below 1 less often.
 */
export const marks = [60, 124];

export const S17: React.FC = () => {
  const frame = useCurrentFrame();

  const grid = prog(frame, 0, 16);
  const prod = betweenStages(frame, marks, 0, 0) * prog(frame, 18, 34);
  const ratio = fromStage(frame, marks, 1, 16);
  const cap0 = betweenStages(frame, marks, 0, 0) * prog(frame, 34, 50);
  const hot: [number, number][] = [
    [0, 0],
    [1, 1],
  ];

  return (
    <Frame n={17} title="Joint against marginals">
      <Canvas>
        <ProbGrid rowsOp={1} colsOp={1} op={grid} hot={frame >= marks[0] + 6 ? hot.filter(([r, c]) => RATIO[r][c] > 1) : []} />
        {[0, 1].map((r) => (
          <Num key={`r${r}`} at={rowSumC(r)} text={fmt(P_TRUE[r], 3)} size={56} color={C.soft} op={grid} />
        ))}
        {[0, 1].map((c) => (
          <Num key={`c${c}`} at={colSumC(c)} text={fmt(P_FOUND[c], 3)} size={56} color={C.soft} op={grid} />
        ))}
        {[0, 1].map((r) =>
          [0, 1].map((c) => (
            <g key={`${r}${c}`}>
              <Num at={cellC(r, c)} text={fmt(PRODUCT[r][c], 4)} size={58} op={prod} />
              <Num at={cellC(r, c)} text={fmt(RATIO[r][c], 2)} size={72} bold={RATIO[r][c] > 1} color={RATIO[r][c] < 1 ? C.soft : C.ink} op={ratio} />
            </g>
          )),
        )}
        <g fontFamily={F.hand} fontSize={45} fill={C.soft} textAnchor="middle" opacity={grid}>
          <text x={GX + 2 * CW + 20 + MARG / 2} y={GY - 30}>
            true
          </text>
          <text x={GX - 80} y={GY + 2 * CH + 96}>
            found
          </text>
        </g>
      </Canvas>
      <Fade o={cap0} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={50}>
          Unrelated splits: joint = marginal × marginal
        </Box>
      </Fade>
      <Fade o={ratio} dy={14}>
        <Box x={960} y={812} w={1600} align="center" size={56}>
          <Tex tex={'\\text{joint}\\ /\\ (\\text{marginal} \\times \\text{marginal})'} />
        </Box>
        <Cap x={960} y={900} w={1600}>
          above 1: more often than chance. below 1: less often.
        </Cap>
      </Fade>
    </Frame>
  );
};
