import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {C} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {LOOK, type Look} from '../lib/look';
import {mix} from '../lib/network';
import {q3} from '../lib/club';
import {BR_Q, BR_S1, BR_S2} from '../data/data';
import {BridgeScene} from '../lib/c_bridge';
import {LoopDiagram, loopWidth, type LoopBox} from '../lib/c_loop';

/**
 * Opens on the picture S21 ends with (the constructed example: two blue pieces, Q = 0.357).
 * 0: the same picture.
 * 1: Leiden splits the blue group into its two connected parts (the right triangle turns purple): Q = 0.482.
 * 2: the loop of Leiden: move nodes, split groups into connected parts, merge parts into nodes.
 * 3: every group stays connected; the name and the paper.
 */
export const marks = [26, 96, 168, 214];

const BLUE = LOOK[0];
const ORANGE = LOOK[1];
const PURPLE = LOOK[3];
const LOOKS1: Look[] = BR_S1.map((g) => (g === 0 ? BLUE : ORANGE));
const LOOKS2: Look[] = BR_S2.map((g) => (g === 0 ? BLUE : g === 1 ? PURPLE : ORANGE));

const BOXES: LoopBox[] = [
  {text: 'Move nodes', w: 270},
  {text: 'Split into connected parts', w: 520},
  {text: 'Merge parts into nodes', w: 470},
];
const GAP = 90;
const X0 = (1920 - loopWidth(BOXES, GAP)) / 2;

export const S22: React.FC = () => {
  const frame = useCurrentFrame();
  const t = prog(frame, 30, 54);
  const lookTo = LOOKS1.map((l, i) => (i >= 3 && i <= 5 ? PURPLE : l));
  const lab = t > 0.5 ? BR_S2 : BR_S1;
  const looksNow = t > 0.5 ? LOOKS2 : LOOKS1;
  const dim = 1 - prog(frame, 30, 54);
  const hot = prog(frame, 50, 66);
  const gap = 1 - prog(frame, 28, 42);
  const diagram = (i: number) => prog(frame, marks[1] + 4 + 18 * i, marks[1] + 22 + 18 * i);

  return (
    <Frame n={22} zoom={1.08} top={200}>
      <Canvas>
        <BridgeScene
          lab={lab}
          looks={LOOKS1}
          lookTo={lookTo}
          t={t}
          edgeLab={lab}
          edgeLooks={looksNow}
          dim={dim}
          rings={{o: 1, left: C.blue, right: mix(C.blue, C.purple, t)}}
          gap={gap}
        />
        <LoopDiagram
          x={X0}
          y={770}
          h={96}
          boxes={BOXES}
          gap={GAP}
          font={36}
          appear={[diagram(0), diagram(1), diagram(2)]}
          back={{from: 2, to: 0, label: 'repeat', appear: prog(frame, marks[1] + 58, marks[1] + 74)}}
        />
      </Canvas>
      <Fade o={1 - hot}>
        <Tag x={960} y={215} hot style={{fontSize: 56}}>
          Q = {q3(BR_Q[1])}
        </Tag>
      </Fade>
      <Fade o={hot}>
        <Tag x={960} y={215} hot style={{fontSize: 56}}>
          Q = {q3(BR_Q[2])}
        </Tag>
      </Fade>
      <Fade o={betweenStages(frame, marks, 1, 1)} dy={14}>
        <Box x={960} y={715} w={1680} align="center">
          Leiden splits each group into well-connected parts
          <br />
          before it merges them.
        </Box>
      </Fade>
      <Fade o={fromStage(frame, marks, 3, 16)} dy={14}>
        <Box x={960} y={688} w={1500} align="center" size={44}>
          Every group stays connected.
        </Box>
        <Tag x={250} y={215} hot style={{fontSize: 56}}>
          Leiden
        </Tag>
        <Cap x={1460} y={222} w={560}>
          Traag, Waltman, van Eck, 2019
        </Cap>
      </Fade>
    </Frame>
  );
};
