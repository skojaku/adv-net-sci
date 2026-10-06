import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {betweenStages, fromStage, prog, stageStart} from '../lib/anim';
import {lerp} from '../lib/plot';
import {LoopDiagram, type LoopBox} from '../lib/c_loop';

/**
 * 0: the formula of Q, with one sentence.
 * 1: Louvain: move nodes, merge groups into nodes, repeat (the formula moves up and shrinks).
 * 2: Leiden: the same with a split step.
 * 3: Q has limits of its own: the bridge to the next deck (M05 S01).
 */
export const marks = [58, 132, 204, 262];

const LOUVAIN: LoopBox[] = [
  {text: 'Move nodes', w: 240},
  {text: 'Merge groups into nodes', w: 430},
];
const LEIDEN: LoopBox[] = [
  {text: 'Move nodes', w: 240},
  {text: 'Split into connected parts', w: 450},
  {text: 'Merge parts into nodes', w: 410},
];
const GAP = 70;
const X0 = 480;
const ROW1 = 375;
const ROW2 = 680;

export const S23: React.FC = () => {
  const frame = useCurrentFrame();
  const k = prog(frame, stageStart(marks, 1) + 2, stageStart(marks, 1) + 26);
  const formulaTop = lerp(300, 200, k);
  const formulaSize = lerp(66, 42, k);
  // stage 3: the two loop rows leave, the formula stays (docked at the top) and the last sentence gets the free space
  const rows = 1 - fromStage(frame, marks, 3, 14);
  const s1 = stageStart(marks, 1);
  const s2 = stageStart(marks, 2);
  return (
    <Frame n={23} zoom={1.08} top={190}>
      <Fade o={prog(frame, 6, 26)} dy={20}>
        <div style={{position: 'absolute', left: 0, width: 1920, top: formulaTop, textAlign: 'center', fontSize: formulaSize, color: C.ink}}>
          <Tex tex="Q=\dfrac{1}{2M}\sum_{i,j}\left(A_{ij}-\dfrac{k_ik_j}{2M}\right)\delta(c_i,c_j)" />
        </div>
      </Fade>
      <Fade o={betweenStages(frame, marks, 0, 0)} dy={14}>
        <Box x={960} y={560} w={1500} align="center" size={48}>
          Edges inside groups, minus the edges that a random network with the same degrees puts there.
        </Box>
      </Fade>

      <Fade o={rows} dy={0}>
        <Canvas>
          <LoopDiagram
            x={X0}
            y={ROW1}
            h={90}
            gap={GAP}
            font={32}
            boxes={LOUVAIN}
            appear={[prog(frame, s1 + 8, s1 + 26), prog(frame, s1 + 28, s1 + 46)]}
            back={{from: 1, to: 0, label: 'repeat', appear: prog(frame, s1 + 44, s1 + 60)}}
          />
          <LoopDiagram
            x={X0}
            y={ROW2}
            h={90}
            gap={GAP}
            font={32}
            boxes={LEIDEN}
            appear={[prog(frame, s2 + 8, s2 + 26), prog(frame, s2 + 28, s2 + 46), prog(frame, s2 + 48, s2 + 66)]}
            back={{from: 2, to: 0, label: 'repeat', appear: prog(frame, s2 + 64, s2 + 80)}}
          />
        </Canvas>
        <Fade o={fromStage(frame, marks, 1, 16)} dy={14}>
          <Tag x={290} y={ROW1 + 10} hot style={{fontSize: 56}}>
            Louvain
          </Tag>
          <Box x={X0} y={585} w={1300} size={40} color={C.soft}>
            Louvain: move nodes, merge groups, repeat.
          </Box>
        </Fade>
        <Fade o={fromStage(frame, marks, 2, 16)} dy={14}>
          <Tag x={290} y={ROW2 + 10} hot style={{fontSize: 56}}>
            Leiden
          </Tag>
          <Box x={X0} y={890} w={1300} size={40} color={C.soft}>
            Leiden: the same, with a split step, so groups stay connected.
          </Box>
        </Fade>
      </Fade>

      <Fade o={fromStage(frame, marks, 3, 16)} dy={16}>
        <Box x={960} y={500} w={1500} align="center" size={54}>
          Q has limits of its own. A ring of triangles merges neighbours. That is next.
        </Box>
      </Fade>
    </Frame>
  );
};
