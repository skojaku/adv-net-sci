import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {fromStage, prog} from '../lib/anim';

/**
 * 0: graph-tool, the Python library by Tiago Peixoto that fits the Bayesian SBM.
 * 1: the function to call, and where to find it.
 */
export const marks = [60, 120];

export const S34: React.FC = () => {
  const frame = useCurrentFrame();

  const a = prog(frame, 8, 26);
  const b = prog(frame, 26, 46);
  const c = fromStage(frame, marks, 1, 16);
  const d = prog(frame, marks[0] + 24, marks[0] + 42);

  return (
    <Frame n={34} zoom={1.25} top={300}>
      <Fade o={a} dy={14}>
        <Box x={260} y={300} w={1500} size={56}>
          <Term>graph-tool</Term>: a Python library by Tiago Peixoto
        </Box>
      </Fade>
      <Fade o={b} dy={14}>
        <Box x={260} y={420} w={1500} size={56}>
          The Bayesian SBM: nested, degree-corrected
        </Box>
      </Fade>
      <Fade o={c} dy={14}>
        <Box x={260} y={600} w={1500} size={44} color={C.soft} style={{fontFamily: F.mono}}>
          minimize_nested_blockmodel_dl
        </Box>
      </Fade>
      <Fade o={d} dy={14}>
        <Box x={260} y={720} w={1500} size={50} color={C.blue}>
          graph-tool.skewed.de
        </Box>
      </Fade>
    </Frame>
  );
};
