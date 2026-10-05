import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {Num, ProbGrid, cellC} from '../components/ProbGrid';
import {MI, RATIO, TERM, fmt} from '../lib/prob';

/**
 * Mutual information as a weighted average of the log of the ratio of S17.
 * 0: the ratio of every cell, and the formula.
 * 1: each cell's share: joint x log2(ratio).
 * 2: the shares add up to I = 0.549; unrelated splits give I = 0.
 */
export const marks = [56, 116, 176];

const SUM = `I = ${TERM.flat().map((t, k) => (k === 0 ? fmt(t, 3) : t < 0 ? `- ${fmt(-t, 3)}` : `+ ${fmt(t, 3)}`)).join(' ')} = ${fmt(MI, 3)}`;

export const S18: React.FC = () => {
  const frame = useCurrentFrame();

  const grid = prog(frame, 0, 16);
  const ratio = betweenStages(frame, marks, 0, 0) * prog(frame, 14, 30);
  const term = fromStage(frame, marks, 1, 16);
  const formula = prog(frame, 28, 46);
  const sum = fromStage(frame, marks, 2, 16);

  return (
    <Frame n={18} zoom={1.15} top={245}>
      <Canvas>
        <ProbGrid op={grid} />
        {[0, 1].map((r) =>
          [0, 1].map((c) => (
            <g key={`${r}${c}`}>
              <Num at={cellC(r, c)} text={fmt(RATIO[r][c], 2)} size={64} color={C.soft} op={ratio} />
              <Num at={cellC(r, c)} text={fmt(TERM[r][c], 3)} size={56} bold op={term} />
            </g>
          )),
        )}
      </Canvas>
      <Fade o={formula} dy={14}>
        <Box x={960} y={662} w={1700} align="center" size={56}>
          <Term>mutual information</Term> <Tex tex={'I'} /> = <Tex tex={'\\sum p(t,f)\\,\\log_2 \\dfrac{p(t,f)}{p(t)\\,p(f)}'} />
        </Box>
      </Fade>
      <Fade o={term * (1 - sum)} dy={14}>
        <Cap x={960} y={880} w={1500}>
          each cell: joint × log of the ratio
        </Cap>
      </Fade>
      <Fade o={sum} dy={14}>
        <Box x={960} y={840} w={1700} align="center" size={50}>
          <Tex tex={SUM.replace(/-/g, '-')} />
        </Box>
        <Cap x={960} y={925} w={1500}>
          unrelated splits: every ratio is 1, log 1 = 0, so I = 0
        </Cap>
      </Fade>
    </Frame>
  );
};
