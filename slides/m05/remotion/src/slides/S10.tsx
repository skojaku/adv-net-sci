import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {Frac} from '../lib/eight';
import {CoMatrix, N_APART, N_BOTH, N_PAIRS} from '../lib/pairmatrix';

/**
 * Pairs of nodes as the cells of a matrix. A pair is never drawn as two nodes joined by a line.
 * 0: the true split: a cell is shaded when the two nodes have the same colour.
 * 1: the found split: a cell is shaded when the two nodes are in the same box.
 * 2: the product of the two: a check on the cells shaded in BOTH (together in both splits): 9 pairs.
 * 3: the product of what is white in each: a check on the cells white in BOTH (apart in both splits): 12 pairs.
 *    The Rand index counts both: the splits agree about a pair when it is together in both or apart in both.
 * 4: Rand index = (together in both + apart in both) / all pairs = (9 + 12) / 28 = 0.75.
 */
export const marks = [50, 106, 166, 226, 290];

const C54 = 54;
const SLOT_X = [180, 762, 1344];
const MY = 350;

const stagger = (frame: number, start: number) => (k: number) => prog(frame, start + k * 0.45, start + k * 0.45 + 10);

export const S10: React.FC = () => {
  const frame = useCurrentFrame();

  const f0 = prog(frame, 0, 16);
  const found = fromStage(frame, marks, 1, 14);
  const both = betweenStages(frame, marks, 2, 2);
  const apart = fromStage(frame, marks, 3, 14);
  const cap0 = betweenStages(frame, marks, 0, 0);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = betweenStages(frame, marks, 2, 2);
  const cap3 = betweenStages(frame, marks, 3, 3);
  const cap4 = fromStage(frame, marks, 4, 14);

  return (
    <Frame n={10}>
      <Canvas>
        <CoMatrix x={SLOT_X[0]} y={MY} c={C54} mode="true" frame={f0} label="true" reveal={stagger(frame, 4)} />
        <g opacity={found}>
          <CoMatrix x={SLOT_X[1]} y={MY} c={C54} mode="found" label="found" reveal={stagger(frame, marks[0] + 6)} />
        </g>
        <g opacity={both}>
          <CoMatrix x={SLOT_X[2]} y={MY} c={C54} mode="both" label="together in both" reveal={stagger(frame, marks[1] + 8)} />
        </g>
        <g opacity={apart}>
          <CoMatrix x={SLOT_X[2]} y={MY} c={C54} mode="apart" label="apart in both" reveal={stagger(frame, marks[2] + 8)} />
        </g>
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
          Shaded in both: <span style={{color: C.blue}}>together in both splits</span>, {N_BOTH} pairs
        </Box>
      </Fade>
      <Fade o={cap3} dy={14}>
        <Box x={960} y={830} w={1600} align="center" size={48}>
          White in both: <span style={{color: C.blue}}>apart in both splits</span>, {N_APART} pairs
        </Box>
      </Fade>
      <Fade o={cap4} dy={14}>
        <div style={{position: 'absolute', left: 150, top: 815, width: 1620, background: C.panel, padding: '12px 28px', fontFamily: F.serif, fontSize: 40, lineHeight: 1.3, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 16, whiteSpace: 'nowrap'}}>
          <Term>Rand index</Term>
          <span>=</span>
          <Frac top="together in both + apart in both" bottom="all pairs of nodes" />
          <span>=</span>
          <Frac top={`${N_BOTH} + ${N_APART}`} bottom={N_PAIRS} />
          <span>= {((N_BOTH + N_APART) / N_PAIRS).toFixed(2)}</span>
        </div>
      </Fade>
    </Frame>
  );
};
