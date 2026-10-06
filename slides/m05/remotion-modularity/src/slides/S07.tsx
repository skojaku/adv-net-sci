import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {FormulaStack, type StackRow} from '../components/FormulaStack';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {caption, prog} from '../lib/anim';
import {LOOK} from '../lib/look';
import {ToyDisc} from '../lib/a_toy';
import {TOY_DEG, TOY_E04} from '../data/data';

/**
 * A grid of the stubs of i (rows) and the stubs of j (columns): k_i x k_j = 3 x 2 cells; each cell is one stub of i with one stub of j.
 * 0: the grid; 6 cells.
 * 1: each cell joins with probability about 1 / 2M; the expected number of edges is 6 / 12 = 0.50.
 * (Lecturer: short. The count-by-rows-or-columns stage that showed k_i k_j = k_j k_i is gone; the narration says it in one line.)
 */
export const marks = [62, 130];

const KI = TOY_DEG[0]; // rows: the stubs of i (node 1, degree 3)
const KJ = TOY_DEG[4]; // columns: the stubs of j (node 5, degree 2)
const CELL = 150;
const X0 = 250;
const Y0 = 340;
const HEAD_D = 48;
const ROWS_I = Array.from({length: KI}, (_, r) => r);
const COLS_J = Array.from({length: KJ}, (_, c) => c);

const TWO_M_TOY = TOY_DEG.reduce((a, b) => a + b, 0); // 12

const ROWS: StackRow[] = [
  {group: 0, tex: `k_i\\times k_j=${KI}\\times${KJ}=${KI * KJ}\\ \\text{pairs}`},
  {group: 1, tex: `\\dfrac{k_ik_j}{2M}=\\dfrac{${KI}\\times${KJ}}{${TWO_M_TOY}}=${(TOY_E04).toFixed(2)}`},
];

const BALANCE = {textWrap: 'balance'} as React.CSSProperties;

export const S07: React.FC = () => {
  const frame = useCurrentFrame();

  const cellIn = (r: number, c: number) => prog(frame, 4 + 3 * (r * KJ + c), 4 + 3 * (r * KJ + c) + 14);
  const head = prog(frame, 24, 42);
  const prob = (r: number, c: number) => prog(frame, marks[0] + 6 + 3 * (r * KJ + c), marks[0] + 6 + 3 * (r * KJ + c) + 16);
  const s0 = caption(frame, marks, 0);
  const s1 = caption(frame, marks, 1);

  const cx = (c: number) => X0 + CELL * c + CELL / 2;
  const cy = (r: number) => Y0 + CELL * r + CELL / 2;
  
  return (
    <Frame n={7}>
      <Canvas>
        {/* the grid */}
        {ROWS_I.flatMap((r) =>
          COLS_J.map((c) => (
            <g key={`${r}${c}`} opacity={cellIn(r, c)}>
              <rect x={X0 + c * CELL} y={Y0 + r * CELL} width={CELL} height={CELL} fill="#fff" stroke={C.rule} strokeWidth={3} />
            </g>
          )),
        )}
        <rect x={X0} y={Y0} width={KJ * CELL} height={KI * CELL} fill="none" stroke={C.soft} strokeWidth={3} opacity={cellIn(KI - 1, KJ - 1)} />
        {/* the stubs of i (rows) and of j (columns) */}
        <g opacity={head}>
          {ROWS_I.map((r) => (
            <ToyDisc key={`i${r}`} p={[X0 - 50, cy(r)]} d={HEAD_D} look={LOOK[0]} label={r + 1} size={26} />
          ))}
          {COLS_J.map((c) => (
            <ToyDisc key={`j${c}`} p={[cx(c), Y0 - 50]} d={HEAD_D} look={LOOK[1]} label={c + 1} size={26} />
          ))}
        </g>
      </Canvas>
      {/* 1 / 2M in every cell (stage 1) */}
      {ROWS_I.flatMap((r) =>
        COLS_J.map((c) => (
          <div key={`p${r}${c}`} style={{opacity: prob(r, c)}}>
            <Box x={cx(c)} y={cy(r) - 36} w={CELL} align="center" size={38} color={C.soft}>
              <Tex tex="\dfrac{1}{2M}" />
            </Box>
          </div>
        )),
      )}
      <div style={{opacity: head}}>
        <Box x={X0 - 50} y={Y0 - 140} w={120} align="center" size={50} color={LOOK[0].fill}><Tex tex="i" /></Box>
        <Box x={X0 + (KJ * CELL) / 2} y={Y0 - 150} w={120} align="center" size={50} color={LOOK[1].fill}><Tex tex="j" /></Box>
      </div>
      <FormulaStack rows={ROWS} marks={marks} x={960} y={340} w={860} big={58} small={46} gap={26} />
      <div style={{opacity: s0}}>
        <Box x={960} y={700} w={860} size={42} style={BALANCE}>Each cell is one pair of stubs: one of i, one of j.</Box>
      </div>
      <div style={{opacity: s1}}>
        <Box x={960} y={700} w={860} size={42} style={BALANCE}>Each pair of stubs contributes 1/2M edges on average.</Box>
        <Cap x={1390} y={560} w={600} align="left">expected number of edges</Cap>
      </div>
    </Frame>
  );
};
