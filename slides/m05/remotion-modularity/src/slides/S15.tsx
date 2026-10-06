import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {fromStage, prog} from '../lib/anim';

/**
 * 0: the number of ways to split 34 nodes into groups (the Bell number, 2.1e+28).
 * 1: we cannot try them all; we improve one partition step by step.
 */
export const marks = [52, 108];

export const S15: React.FC = () => {
  const frame = useCurrentFrame();
  const num = prog(frame, 6, 30);
  const cap = prog(frame, 30, 50);
  const second = fromStage(frame, marks, 1, 16);
  return (
    <Frame n={15} zoom={1.15} top={250}>
      <Fade o={num} dy={24}>
        <div style={{position: 'absolute', left: 0, width: 1920, top: 330, textAlign: 'center', fontSize: 190, color: C.ink}}>
          <Tex tex="2.1\times10^{28}" />
        </div>
      </Fade>
      <Fade o={cap} dy={16}>
        <Box x={960} y={610} w={1500} align="center" size={56} color={C.soft}>
          ways to split 34 nodes into groups
        </Box>
      </Fade>
      <Fade o={second} dy={16}>
        <Box x={960} y={760} w={1500} align="center" size={56}>
          We cannot try them all. We improve one partition step by step.
        </Box>
      </Fade>
    </Frame>
  );
};
