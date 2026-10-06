import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {FormulaStack, type StackRow} from '../components/FormulaStack';
import {Box} from '../components/Text';
import {C} from '../theme';
import {caption} from '../lib/anim';

/**
 * Formulas only, one per stage; nothing is removed.
 * 0: the inside fraction.
 * 1: Q = inside fraction minus the fraction expected in a random network.
 * 2: everyone in one group gives 1 - 1 = 0.
 */
export const marks = [60, 124, 188];

const ROWS: StackRow[] = [
  {
    group: 0,
    tex: '\\text{inside fraction}=\\dfrac{\\text{edges inside groups}}{M}',
    note: 'M is the number of edges',
  },
  {
    group: 1,
    tex: 'Q=\\text{inside fraction}\\;-\\;\\text{inside fraction of a random network}',
  },
  {
    group: 2,
    tex: '\\text{everyone in one group: }\\;1-1=0',
  },
];

export const S04: React.FC = () => {
  const frame = useCurrentFrame();
  const s1 = caption(frame, marks, 1);
  const s2 = caption(frame, marks, 2);
  return (
    <Frame n={4} zoom={1.1} top={210}>
      <FormulaStack rows={ROWS} marks={marks} x={150} y={250} w={1620} big={56} small={48} gap={52} />
      <div style={{opacity: s1}}>
        <Box x={150} y={760} w={1620} size={46} color={C.soft}>
          The random network has the same number of edges and the same degree for every node.
        </Box>
      </div>
      <div style={{opacity: s2}}>
        <Box x={150} y={760} w={1620} size={46} color={C.soft}>
          Now we need that random network.
        </Box>
      </div>
    </Frame>
  );
};
