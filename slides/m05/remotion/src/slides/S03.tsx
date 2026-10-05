import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {C} from '../theme';
import {lin, prog, smooth, stepped} from '../lib/anim';
import {Ring} from '../lib/ring';
import {clamp, lerp} from '../lib/plot';

/**
 * 0: the ring grows from 4 to 10 triangles, one triangle at a time.
 * 1: the ring is drawn twice with the two groupings (S04's picture without the values), and the question.
 * No Q value anywhere.
 */
export const marks = [68, 124];

const ALL = Array.from({length: 10}, () => 1);
const CY = 565;
const SLOT = 150;

export const S03: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0: the count moves 4, 5, ..., 10 one step at a time
  const count = stepped(frame, 8, 9, 7, [4, 5, 6, 7, 8, 9, 10]);
  const w = ALL.map((_, i) => clamp(count - i, 0, 1));
  const n = Math.round(count);
  const nOp = prog(frame, 0, 14);

  // stage 1: the ring slides left, its copy slides right, the bands come, then the question
  const slide = smooth(frame, 70, 94);
  const copy = smooth(frame, 76, 96);
  const bands = prog(frame, 88, 106);
  const q = prog(frame, 102, 120);
  const cxL = lerp(960, 480, slide);
  const cxR = lerp(960, 1340, slide);
  const stage1 = lin(frame, 68, 70);

  return (
    <Frame n={3}>
      <Canvas>
        <Ring w={w} cx={cxL} cy={CY} slot={SLOT} apart={bands} />
        <g opacity={copy * stage1}>
          <Ring w={ALL} cx={cxR} cy={CY} slot={SLOT} pairs={bands} />
        </g>
      </Canvas>
      <Fade o={nOp}>
        <Box x={960} y={200} w={600} align="center" size={40} color={C.soft}>
          n = {n} triangles
        </Box>
      </Fade>
      <Fade o={q} dy={16}>
        <Box x={960} y={905} w={1500} align="center" size={45}>
          Which grouping has the higher Q now?
        </Box>
      </Fade>
    </Frame>
  );
};
