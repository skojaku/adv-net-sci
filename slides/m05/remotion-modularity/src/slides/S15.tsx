import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {C} from '../theme';
import {caption, prog} from '../lib/anim';
import {clamp} from '../lib/plot';
import {mix, Network} from '../lib/network';
import {HOLLOW} from '../lib/look';
import {CLUB_L, q3} from '../lib/club';
import {MOVES} from '../data/data';
import {EDGES, groupEdgeLook, groupEdgeOp, LABELS, LOOKS_AT, N_MOVES, NODES, Q_AFTER} from '../lib/c_trace';
import {QPlot} from '../lib/c_qplot';

/**
 * Label switching on the club, one node at a time (MOVES: each node visits in the order of ORDER and takes the label of the neighbouring group that raises Q most).
 * 0: the club, every node with its own label (a number in a hollow disc), Q = -0.050.
 * 1: moves 1 to 12.
 * 2: moves 13 to 36: five groups, Q = 0.399.
 * 3: no single move raises Q any more.
 */
export const marks = [56, 130, 264, 314];

const MV = 5; // frames per move
const S1 = 62; // the first move of stage 1 starts
const S2 = 136; // the first move of stage 2 starts

/** how many moves are done at this frame (fractional: the move in progress) */
const moves = (frame: number): number => (frame < S2 ? clamp((frame - S1) / MV, 0, 12) : 12 + clamp((frame - S2) / MV, 0, N_MOVES - 12));

const PLOT = {x: 1070, y: 330, w: 690, h: 330};
const XS = Array.from({length: N_MOVES + 1}, (_, i) => i);

export const S15: React.FC = () => {
  const frame = useCurrentFrame();
  const p = moves(frame);
  const m = Math.min(N_MOVES, Math.floor(p + 1e-9));
  const f = m >= N_MOVES ? 0 : p - m;
  const lookA = LOOKS_AT[m];
  const lookB = LOOKS_AT[Math.min(m + 1, N_MOVES)];
  const labelsNow = LABELS[f > 0.5 ? m + 1 : m];
  const looksNow = f > 0.5 ? lookB : lookA;
  const mover = m < N_MOVES && f > 0 ? MOVES[m][0] : -1;
  const ring = Array.from({length: NODES}, (_, i) => (i === mover ? mix('#ffffff', C.ink, Math.sin(Math.PI * f)) : null));
  const numbers = looksNow.map((l, i) => (l === HOLLOW ? labelsNow[i] + 1 : null));

  const nodeOp = (i: number) => prog(frame, 0.4 * i, 0.4 * i + 12);
  const edgeAppear = (i: number) => prog(frame, 6 + 0.28 * i, 6 + 0.28 * i + 10);
  const edgeOp = groupEdgeOp(labelsNow, looksNow);
  const q = Q_AFTER[Math.round(p)];
  const plotOp = prog(frame, 16, 36);

  return (
    <Frame n={15}>
      <Canvas>
        <Network
          pos={CLUB_L}
          edges={EDGES}
          look={lookA}
          lookTo={lookB}
          t={f}
          nodeD={42}
          nodeOp={(i) => nodeOp(i)}
          edgeOp={(i, e) => edgeAppear(i) * edgeOp(i, e)}
          edgeLook={groupEdgeLook(labelsNow, looksNow)}
          ring={ring}
          ringW={7}
          label={numbers}
          labelSize={20}
        />
        <QPlot
          {...PLOT}
          xs={XS}
          ys={Q_AFTER}
          shown={p + 1}
          xMin={0}
          xMax={N_MOVES}
          yMin={-0.08}
          yMax={0.46}
          xTicks={[0, 12, 24, 36].map((v) => ({v, label: String(v)}))}
          yTicks={[0, 0.2, 0.4].map((v) => ({v, label: v === 0 ? '0' : String(v)}))}
          xLabel="move"
          yLabel="Q"
          opacity={plotOp}
        />
      </Canvas>
      <Fade o={plotOp} dy={14}>
        <Tag x={1415} y={222} style={{fontSize: 56}}>
          Q = {q3(q)}
        </Tag>
      </Fade>
      <Fade o={caption(frame, marks, 0)} dy={14}>
        <Box x={1010} y={790} w={770}>
          Every node starts
          <br />
          with its own label.
        </Box>
      </Fade>
      <Fade o={caption(frame, marks, 1)} dy={14}>
        <Box x={1010} y={790} w={770}>
          A node takes the label of the neighbouring group that raises Q the most.
        </Box>
      </Fade>
      <Fade o={caption(frame, marks, 3)} dy={14}>
        <Box x={1010} y={790} w={770}>
          No single move
          <br />
          raises Q any more.
        </Box>
      </Fade>
    </Frame>
  );
};
