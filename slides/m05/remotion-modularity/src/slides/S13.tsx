import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {Tex} from '../components/Tex';
import {FormulaStack, type StackRow} from '../components/FormulaStack';
import {C} from '../theme';
import {prog} from '../lib/anim';
import {q3} from '../lib/club';
import {Q_REAL} from '../data/data';
import {CLUB_B, CLUB_BAR, CLUB_GROUP, CLUB_SPLIT, Matrix, fillB, type CellStyle} from '../lib/b_matrix';

/**
 * The karate club's Q_ij (sorted by group) at the left, the formula at the right, one row per stage.
 * 0: the groups as bars outside the matrix, c_i = group of node i.
 * 1: only the cells of two nodes in the same group stay (delta = 1); the others fade.
 * 2: the kept cells are added: Q = (1 / 2M) sum Q_ij delta(c_i, c_j).
 * 3: Q = 0.358, with the paper.
 */
export const marks = [64, 134, 204, 268];

const CELL = 14;
const N = 34;
const W = N * CELL;
const MX = 210;
const MY = 330;

const ROWS: ReadonlyArray<StackRow> = [
  {group: 0, tex: 'c_i=\\text{group of node }i'},
  {group: 1, tex: '\\delta(c_i,c_j)=1\\text{ if }c_i=c_j\\text{, else }0'},
  {group: 2, tex: 'Q=\\dfrac{1}{2M}\\sum_{i,j}Q_{ij}\\,\\delta(c_i,c_j)'},
];

export const S13: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const bars = prog(frame, 22, 42);
  const row = (r: number) => prog(frame, 4 + r, 14 + r);
  const lab = prog(frame, 6, 24);
  // stage 1
  const mask = prog(frame, 72, 104);
  // stage 2
  const blocks = prog(frame, 140, 160);
  // stage 3
  const tag = prog(frame, 208, 226);
  const credit = prog(frame, 222, 240);
  const say = prog(frame, 240, 262);

  const at = (r: number, c: number): CellStyle => {
    const same = CLUB_GROUP[r] === CLUB_GROUP[c];
    return {fill: fillB(CLUB_B[r][c], 0.8), op: row(r) * (same ? 1 : 1 - 0.88 * mask)};
  };
  const x2 = MX + CLUB_SPLIT * CELL;
  const y2 = MY + CLUB_SPLIT * CELL;

  return (
    <Frame n={13} top={190}>
      <Canvas>
        <Matrix x={MX} y={MY} cell={CELL} n={N} at={at} grid={false} bars={{colors: CLUB_BAR, t: 14, gap: 6, op: bars}} />
        <g opacity={blocks} fill="none" stroke={C.ink} strokeWidth={3.5}>
          <rect x={MX} y={MY} width={CLUB_SPLIT * CELL} height={CLUB_SPLIT * CELL} />
          <rect x={x2} y={y2} width={W - CLUB_SPLIT * CELL} height={W - CLUB_SPLIT * CELL} />
        </g>
      </Canvas>
      <Fade o={lab} dy={10}>
        <Box x={MX + W / 2} y={180} w={400} align="center" size={60}><Tex tex="Q_{ij}" /></Box>
      </Fade>
      <Fade o={bars} dy={6}>
        <Box x={MX + W + 52} y={MY - 40} w={90} align="center" size={42}><Tex tex="c_j" /></Box>
        <Box x={MX - 62} y={MY + W + 6} w={90} align="center" size={42}><Tex tex="c_i" /></Box>
      </Fade>
      <FormulaStack rows={ROWS} marks={marks} x={830} y={300} w={980} big={60} small={44} gap={30} />
      <Fade o={tag} dy={14}>
        <Tag x={1320} y={670} hot>Q = {q3(Q_REAL)}</Tag>
      </Fade>
      <Fade o={credit} dy={10}>
        <Cap x={1320} y={750} w={900}>Newman and Girvan, 2004</Cap>
        <Cap x={1320} y={806} w={900} style={{fontSize: 38}}>Phys. Rev. E 69, 026113</Cap>
      </Fade>
      <Fade o={say} dy={14}>
        <Box x={830} y={880} w={980} size={36}>
          Q is the fraction of edges inside groups minus the fraction expected in a random network.
        </Box>
      </Fade>
    </Frame>
  );
};
