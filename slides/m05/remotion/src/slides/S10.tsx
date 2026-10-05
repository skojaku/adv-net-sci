import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {Frac} from '../lib/eight';
import {CoMatrix, N_AGREE, N_DISAGREE, N_PAIRS} from '../lib/pairmatrix';

/**
 * Pairs of nodes as the cells of a matrix. A pair is never drawn as two nodes joined by a line.
 * 0: the true split: a cell is shaded when the two nodes have the same colour.
 * 1: the found split: a cell is shaded when the two nodes are in the same box.
 * 2: the third matrix compares the two: a blue check where the two splits give the same answer for the pair (shaded in
 *    both, or white in both: together in both, or apart in both), then a black cross where they differ. 21 pairs agree, 7 do not.
 * 3: Rand index = agreeing pairs / all pairs = 21 / 28 = 0.75.
 */
export const marks = [50, 106, 190, 250];

const C54 = 54;
const SLOT_X = [180, 762, 1344];
const MY = 350;

const stagger = (frame: number, start: number, step = 0.45) => (k: number) => prog(frame, start + k * step, start + k * step + 10);

export const S10: React.FC = () => {
  const frame = useCurrentFrame();

  const f0 = prog(frame, 0, 16);
  const found = fromStage(frame, marks, 1, 14);
  const agree = fromStage(frame, marks, 2, 10);
  const cap0 = betweenStages(frame, marks, 0, 0);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = betweenStages(frame, marks, 2, 2) * prog(frame, marks[1] + 52, marks[1] + 68);
  const cap3 = fromStage(frame, marks, 3, 14);

  return (
    <Frame n={10}>
      <Canvas>
        <CoMatrix x={SLOT_X[0]} y={MY} c={C54} mode="true" frame={f0} label="true" reveal={stagger(frame, 4)} />
        <g opacity={found}>
          <CoMatrix x={SLOT_X[1]} y={MY} c={C54} mode="found" label="found" reveal={stagger(frame, marks[0] + 6)} />
        </g>
        <CoMatrix
          x={SLOT_X[2]}
          y={MY}
          c={C54}
          mode="agree"
          label="agree?"
          frame={agree}
          reveal={stagger(frame, marks[1] + 8, 0.35)}
          revealCross={stagger(frame, marks[1] + 48, 0.45)}
        />
      </Canvas>

      <Fade o={cap0} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          True split: shaded = the two nodes have the same color
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          Found split: shaded = the two nodes are in the same box
        </Box>
      </Fade>
      <Fade o={cap2} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          <span style={{color: C.blue}}>Agree</span>: {N_AGREE} pairs. Disagree: {N_DISAGREE} pairs.
        </Box>
      </Fade>
      <Fade o={cap3} dy={14}>
        <div style={{position: 'absolute', left: 150, top: 815, width: 1620, background: C.panel, padding: '12px 28px', fontFamily: F.serif, fontSize: 40, lineHeight: 1.3, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 16, whiteSpace: 'nowrap'}}>
          <Term>Rand index</Term>
          <span>=</span>
          <Frac top="agreeing pairs of nodes" bottom="all pairs of nodes" />
          <span>=</span>
          <Frac top={N_AGREE} bottom={N_PAIRS} />
          <span>= {(N_AGREE / N_PAIRS).toFixed(2)}</span>
        </div>
      </Fade>
    </Frame>
  );
};
