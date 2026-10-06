import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Cap, Tag} from '../components/Text';
import {fromStage, prog} from '../lib/anim';
import {clamp} from '../lib/plot';
import {LEVEL_Q} from '../data/data';
import {q3} from '../lib/club';
import {LoopDiagram, loopWidth, type LoopBox} from '../lib/c_loop';
import {QPlot} from '../lib/c_qplot';

/**
 * Louvain as a loop.
 * 0: the loop: move nodes, merge groups into nodes, repeat; stop when Q does not rise.
 * 1: Q at each level (dots joined by a line): start, level 1, level 2, level 3 (no change).
 * 2: the name and the paper.
 */
export const marks = [72, 164, 214];

const BOXES: LoopBox[] = [
  {text: 'Move nodes', w: 300},
  {text: 'Merge groups into nodes', w: 520},
  {text: 'Stop when Q stops rising', w: 520},
];
const GAP = 100;
const X0 = (1920 - loopWidth(BOXES, GAP)) / 2;

const XS = [0, 1, 2, 3];
const YS = [...LEVEL_Q, LEVEL_Q[LEVEL_Q.length - 1]];

export const S20: React.FC = () => {
  const frame = useCurrentFrame();
  const shown = 1 + 3 * clamp((frame - 80) / 78, 0, 1);
  const plotO = prog(frame, marks[0] + 2, marks[0] + 18);
  const credit = fromStage(frame, marks, 2, 16);
  return (
    <Frame n={20} zoom={1.08} top={200}>
      <Canvas>
        <LoopDiagram
          x={X0}
          y={225}
          boxes={BOXES}
          gap={GAP}
          font={38}
          appear={[prog(frame, 4, 22), prog(frame, 24, 42), prog(frame, 50, 68)]}
          arrowLabels={[undefined, undefined, 'no gain']}
          back={{from: 1, to: 0, label: 'repeat', appear: prog(frame, 38, 56)}}
        />
        <QPlot
          x={260}
          y={570}
          w={800}
          h={300}
          xs={XS}
          ys={YS}
          shown={shown}
          xMin={-0.35}
          xMax={3.35}
          yMin={-0.1}
          yMax={0.52}
          xTicks={[
            {v: 0, label: 'start'},
            {v: 1, label: 'level 1'},
            {v: 2, label: 'level 2'},
            {v: 3, label: 'level 3'},
          ]}
          yTicks={[0, 0.2, 0.4].map((v) => ({v, label: v === 0 ? '0' : String(v)}))}
          yLabel="Q"
          lastHollow
          opacity={plotO}
          pointLabels={[q3(YS[0]), q3(YS[1]), q3(YS[2]), 'no change']}
          labelBelow={[0]}
        />
      </Canvas>
      <Fade o={credit} dy={16}>
        <Tag x={1490} y={560} hot style={{fontSize: 64}}>
          Louvain
        </Tag>
        <Cap x={1190} y={690} w={600} align="left">
          Blondel, Guillaume, Lambiotte,
          <br />
          Lefebvre, 2008
        </Cap>
        <Cap x={1190} y={830} w={600} align="left">
          Fast unfolding of communities
          <br />
          in large networks
        </Cap>
      </Fade>
    </Frame>
  );
};
