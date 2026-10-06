import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {FormulaStack, type StackRow} from '../components/FormulaStack';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {caption, prog} from '../lib/anim';
import {LOOK} from '../lib/look';
import {ToyDisc} from '../lib/a_toy';

/**
 * A grid of the stubs of i (rows) and the stubs of j (columns): k_i x k_j = 3 x 3 cells; each cell is one stub of i with one stub of j.
 * 0: the grid; 9 cells.
 * 1: each cell joins with probability about 1 / 2M; the expected number of edges is 9 / 14.
 * 2: counting the cells by rows (from i) and by columns (from j) gives the same 9 cells.
 */
export const marks = [62, 130, 232];

const K = 3;
const CELL = 150;
const X0 = 250;
const Y0 = 340;
const HEAD_D = 48;

const ROWS: StackRow[] = [
  {group: 0, tex: 'k_i\\times k_j=3\\times3=9\\ \\text{pairs}'},
  {group: 1, tex: '\\dfrac{k_ik_j}{2M}=\\dfrac{3\\times3}{14}=0.64'},
  {group: 2, tex: '\\dfrac{k_ik_j}{2M}=\\dfrac{k_jk_i}{2M}'},
];

const BALANCE = {textWrap: 'balance'} as React.CSSProperties;
const BLUE_SOFT = C.blueSoft;
const ORANGE_SOFT = 'rgba(230, 159, 0, 0.2)';

export const S07: React.FC = () => {
  const frame = useCurrentFrame();

  const cellIn = (r: number, c: number) => prog(frame, 4 + 3 * (r * K + c), 4 + 3 * (r * K + c) + 14);
  const head = prog(frame, 24, 42);
  const prob = (r: number, c: number) => prog(frame, marks[0] + 6 + 3 * (r * K + c), marks[0] + 6 + 3 * (r * K + c) + 16);
  const rowPass = (r: number) => prog(frame, marks[1] + 6 + 14 * r, marks[1] + 6 + 14 * r + 14);
  const colPass = (c: number) => prog(frame, marks[1] + 54 + 14 * c, marks[1] + 54 + 14 * c + 14);
  const rowTotal = prog(frame, marks[1] + 50, marks[1] + 66);
  const colTotal = prog(frame, marks[1] + 98, marks[1] + 114);
  const s0 = caption(frame, marks, 0);
  const s1 = caption(frame, marks, 1);
  const s2 = caption(frame, marks, 2);

  const cx = (c: number) => X0 + CELL * c + CELL / 2;
  const cy = (r: number) => Y0 + CELL * r + CELL / 2;
  const tx = X0 + K * CELL + 36; // the row counts, to the right of the grid
  const ty = Y0 + K * CELL + 22; // the column counts, under the grid

  return (
    <Frame n={7}>
      <Canvas>
        {/* the grid */}
        {[0, 1, 2].flatMap((r) =>
          [0, 1, 2].map((c) => (
            <g key={`${r}${c}`} opacity={cellIn(r, c)}>
              <rect x={X0 + c * CELL} y={Y0 + r * CELL} width={CELL} height={CELL} fill="#fff" stroke={C.rule} strokeWidth={3} />
              <rect x={X0 + c * CELL} y={Y0 + r * CELL} width={CELL} height={CELL} fill={BLUE_SOFT} opacity={rowPass(r)} />
              <rect x={X0 + c * CELL} y={Y0 + r * CELL} width={CELL} height={CELL} fill={ORANGE_SOFT} opacity={colPass(c)} />
            </g>
          )),
        )}
        <rect x={X0} y={Y0} width={K * CELL} height={K * CELL} fill="none" stroke={C.soft} strokeWidth={3} opacity={cellIn(2, 2)} />
        {/* the stubs of i (rows) and of j (columns) */}
        <g opacity={head}>
          {[0, 1, 2].map((r) => (
            <ToyDisc key={`i${r}`} p={[X0 - 50, cy(r)]} d={HEAD_D} look={LOOK[0]} label={r + 1} size={26} />
          ))}
          {[0, 1, 2].map((c) => (
            <ToyDisc key={`j${c}`} p={[cx(c), Y0 - 50]} d={HEAD_D} look={LOOK[1]} label={c + 1} size={26} />
          ))}
        </g>
        {/* counted by rows (blue) and by columns (orange) */}
        <g opacity={rowTotal}>
          <line x1={tx + 36} y1={Y0 + 12} x2={tx + 36} y2={Y0 + K * CELL - 12} stroke={LOOK[0].fill} strokeWidth={5} strokeLinecap="round" />
        </g>
        <g opacity={colTotal}>
          <line x1={X0 + 12} y1={ty + 48} x2={X0 + K * CELL - 12} y2={ty + 48} stroke={LOOK[1].fill} strokeWidth={5} strokeLinecap="round" />
        </g>
      </Canvas>
      {/* 1 / 2M in every cell (stage 1) */}
      {[0, 1, 2].flatMap((r) =>
        [0, 1, 2].map((c) => (
          <div key={`p${r}${c}`} style={{opacity: prob(r, c)}}>
            <Box x={cx(c)} y={cy(r) - 36} w={CELL} align="center" size={38} color={C.soft}>
              <Tex tex="\dfrac{1}{2M}" />
            </Box>
          </div>
        )),
      )}
      <div style={{opacity: head}}>
        <Box x={X0 - 50} y={Y0 - 140} w={120} align="center" size={50} color={LOOK[0].fill}><Tex tex="i" /></Box>
        <Box x={X0 + (K * CELL) / 2} y={Y0 - 150} w={120} align="center" size={50} color={LOOK[1].fill}><Tex tex="j" /></Box>
      </div>
      {/* the counts */}
      {[0, 1, 2].map((r) => (
        <div key={`rc${r}`} style={{opacity: rowPass(r)}}>
          <Box x={tx} y={cy(r) - 30} w={50} align="center" size={44} color={LOOK[0].fill}>3</Box>
        </div>
      ))}
      <div style={{opacity: rowTotal}}>
        <Box x={tx + 56} y={Y0 + (K * CELL) / 2 - 30} w={120} size={44} color={LOOK[0].fill}>= 9</Box>
      </div>
      {[0, 1, 2].map((c) => (
        <div key={`cc${c}`} style={{opacity: colPass(c)}}>
          <Box x={cx(c)} y={ty - 26} w={50} align="center" size={44} color={LOOK[1].fill}>3</Box>
        </div>
      ))}
      <div style={{opacity: colTotal}}>
        <Box x={X0 + (K * CELL) / 2} y={ty + 58} w={200} align="center" size={44} color={LOOK[1].fill}>= 9</Box>
      </div>
      <FormulaStack rows={ROWS} marks={marks} x={960} y={340} w={860} big={58} small={46} gap={26} />
      <div style={{opacity: s0}}>
        <Box x={960} y={760} w={860} size={42} style={BALANCE}>Each cell is one stub of i and one stub of j.</Box>
      </div>
      <div style={{opacity: s1}}>
        <Box x={960} y={760} w={860} size={42} style={BALANCE}>Each pair of stubs is joined with probability about 1/2M.</Box>
      </div>
      <div style={{opacity: s2}}>
        <Box x={960} y={760} w={860} size={42} style={BALANCE}>Counting from i or from j covers the same cells. Do not add the two counts.</Box>
      </div>
    </Frame>
  );
};
