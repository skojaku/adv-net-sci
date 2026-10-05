import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {C} from '../theme';
import {prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {SHUFFLES} from '../data/data';
import {NDOT, NodeDot, TRUE30, dotCentre, scatter} from '../lib/dots30';

/**
 * 0: 30 nodes gather into 5 groups of 6 (true groups).
 * 1: the same nodes again below, labelled by a random relabeling with the same group sizes; the question.
 * A question slide: no number and no answer anywhere on it.
 */
export const marks = [52, 112];

const D = 56;
const PITCH = 70;
const STRIDE = 290;
const X0 = 310;
const Y_TOP = 330;
const Y_BOT = 620;
const ROW = [...Array(NDOT).keys()];

export const S12: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0: nodes appear scattered, then gather group by group
  const appear = prog(frame, 0, 12);
  const gather = (i: number) => smooth(frame, 12 + 3 * Math.floor(i / 6), 36 + 3 * Math.floor(i / 6));
  const cap0 = prog(frame, 38, 52);

  // stage 1: copies slide down and change their fill on the way (a cross-fade, never a blend)
  const start = (i: number) => 56 + 0.5 * i;
  const slide = (i: number) => smooth(frame, start(i), start(i) + 30);
  const refill = (i: number) => smooth(frame, start(i) + 8, start(i) + 22);
  const cap1 = prog(frame, 58, 74);
  const q = prog(frame, 94, 110);

  return (
    <Frame n={12} title="Shuffle the labels">
      <Canvas>
        {ROW.map((i) => {
          const [hx, hy] = dotCentre(i, X0, Y_TOP, PITCH, STRIDE);
          const [sx, sy] = scatter(i, 200, 300, 1520, 150);
          const t = gather(i);
          return <NodeDot key={`t${i}`} x={lerp(sx, hx, t)} y={lerp(sy, hy, t)} d={D} g={TRUE30[i]} op={appear} />;
        })}
        {ROW.map((i) => {
          if (frame < start(i)) return null;
          const [x, y] = dotCentre(i, X0, Y_TOP, PITCH, STRIDE);
          const [bx, by] = dotCentre(i, X0, Y_BOT, PITCH, STRIDE);
          const s = slide(i);
          return <NodeDot key={`b${i}`} x={lerp(x, bx, s)} y={lerp(y, by, s)} d={D} g={TRUE30[i]} gTo={SHUFFLES[0][i]} t={refill(i)} />;
        })}
      </Canvas>
      <Fade o={cap0} dy={14}>
        <Box x={960} y={205} w={1200} align="center" size={45} color={C.soft} hand>
          true groups
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={960} y={500} w={1200} align="center" size={45} color={C.soft} hand>
          random labels
        </Box>
      </Fade>
      <Fade o={q} dy={16}>
        <Box x={960} y={850} w={1680} align="center" size={45}>
          What Rand index do we expect for random labels?
        </Box>
      </Fade>
    </Frame>
  );
};
