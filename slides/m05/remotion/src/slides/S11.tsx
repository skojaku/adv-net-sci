import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {Frac} from '../lib/eight';
import {CoMatrix, N_AGREE, PAIRS8} from '../lib/pairmatrix';

/**
 * Three matrices, one cell for each of the 28 pairs of nodes. A pair is never drawn as two nodes joined by a line.
 * 0: the matrix of the true split, still empty. "8 nodes make 28 pairs of nodes."
 * 1: true split: a cell is shaded when the two nodes have the same colour.
 * 2: found split: a cell is shaded when the two nodes are in the same box.
 * 3: the two matrices compared: alike in both (both shaded or both white) is a check (agree), different is a cross (disagree).
 * 4: Rand index = agreeing pairs of nodes / all pairs of nodes = 21 / 28.
 */
export const marks = [44, 100, 160, 226, 288];

const C54 = 54;
const SLOT_X = [180, 762, 1344];
const MY = 370;

const stagger = (frame: number, start: number) => (k: number) => prog(frame, start + k * 1.0, start + k * 1.0 + 10);

export const S11: React.FC = () => {
  const frame = useCurrentFrame();

  const f0 = prog(frame, 0, 16);
  const found = fromStage(frame, marks, 2, 14);
  const agreeFrame = fromStage(frame, marks, 3, 14);
  const cap0 = betweenStages(frame, marks, 0, 0) * prog(frame, 22, 38);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = betweenStages(frame, marks, 2, 2);
  const cap3 = betweenStages(frame, marks, 3, 3);
  const cap4 = fromStage(frame, marks, 4, 14);

  return (
    <Frame n={11} title="Rand index: pairs of nodes">
      <Canvas>
        <CoMatrix x={SLOT_X[0]} y={MY} c={C54} mode="true" frame={f0} label="true" reveal={stagger(frame, marks[0] + 2)} />
        <g opacity={found}>
          <CoMatrix x={SLOT_X[1]} y={MY} c={C54} mode="found" label="found" reveal={stagger(frame, marks[1] + 6)} />
        </g>
        <g opacity={agreeFrame}>
          <CoMatrix x={SLOT_X[2]} y={MY} c={C54} mode="agree" label="agree?" reveal={stagger(frame, marks[2] + 8)} />
        </g>
      </Canvas>

      <Fade o={cap0} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          8 nodes make 28 pairs of nodes. One cell is one pair.
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          True split: shaded = the two nodes have the same color
        </Box>
      </Fade>
      <Fade o={cap2} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          Found split: shaded = the two nodes are in the same box
        </Box>
      </Fade>
      <Fade o={cap3} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          Alike in both: <span style={{color: C.blue}}>agree</span>. Different: <Term>disagree</Term>. {N_AGREE} of {PAIRS8.length} agree.
        </Box>
      </Fade>
      <Fade o={cap4} dy={14}>
        <div style={{position: 'absolute', left: 150, top: 815, width: 1620, background: C.panel, padding: '12px 28px', fontFamily: F.serif, fontSize: 42, lineHeight: 1.3, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 16, whiteSpace: 'nowrap'}}>
          <Term>Rand index</Term>
          <span>=</span>
          <Frac top="agreeing pairs of nodes" bottom="all pairs of nodes" />
          <span>=</span>
          <Frac top={N_AGREE} bottom={PAIRS8.length} />
          <span>= {(N_AGREE / PAIRS8.length).toFixed(2)}</span>
        </div>
      </Fade>
    </Frame>
  );
};
