import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {prog} from '../lib/anim';
import {CLUB_A, CLUB_B, CLUB_BAR, CLUB_E, CLUB_SPLIT, Matrix, fillA, fillB, fillE, type CellStyle} from '../lib/b_matrix';

/**
 * The same three matrices for the karate club (34 x 34, nodes sorted by group, a bar of the group's colour outside).
 * 0: A (156 filled cells: 78 edges, both ways).
 * 1: a minus sign and E = k_i k_j / 2M.
 * 2: an equals sign and Q_ij = A - E.
 */
export const marks = [64, 122, 180];

const CELL = 14;
const N = 34;
const W = N * CELL;
const MY = 330;
const AX = 170;
const EX = 740;
const BX = 1320;
const BAR = {t: 14, gap: 6};

export const S12: React.FC = () => {
  const frame = useCurrentFrame();

  const bars = prog(frame, 0, 14);
  const aRow = (r: number) => prog(frame, 6 + r, 16 + r);
  const eRow = (r: number) => prog(frame, 68 + r, 78 + r);
  const bRow = (r: number) => prog(frame, 126 + r, 136 + r);
  const minus = prog(frame, 64, 80);
  const equals = prog(frame, 122, 138);
  const eIn = prog(frame, 64, 80);
  const bIn = prog(frame, 122, 138);
  const cap = prog(frame, 30, 52);

  const atA = (r: number, c: number): CellStyle => ({fill: fillA(CLUB_A[r][c]), op: aRow(r)});
  const atE = (r: number, c: number): CellStyle => ({fill: fillE(CLUB_E[r][c], 0.6), op: eRow(r)});
  const atB = (r: number, c: number): CellStyle => ({fill: fillB(CLUB_B[r][c], 0.8), op: bRow(r)});

  return (
    <Frame n={12} top={190}>
      <Canvas>
        <Matrix x={AX} y={MY} cell={CELL} n={N} at={atA} grid={false} bars={{colors: CLUB_BAR, ...BAR, op: bars}} splitAt={CLUB_SPLIT} />
        <Matrix x={EX} y={MY} cell={CELL} n={N} at={atE} grid={false} bars={{colors: CLUB_BAR, ...BAR}} splitAt={CLUB_SPLIT} opacity={eIn} />
        <Matrix x={BX} y={MY} cell={CELL} n={N} at={atB} grid={false} bars={{colors: CLUB_BAR, ...BAR}} splitAt={CLUB_SPLIT} opacity={bIn} />
      </Canvas>
      <Fade o={bars} dy={10}>
        <Box x={AX + W / 2} y={190} w={400} align="center" size={60}><Tex tex="A_{ij}" /></Box>
      </Fade>
      <Fade o={eIn} dy={10}>
        <Box x={EX + W / 2} y={190} w={400} align="center" size={60}><Tex tex="E_{ij}" /></Box>
      </Fade>
      <Fade o={bIn} dy={10}>
        <Box x={BX + W / 2} y={190} w={400} align="center" size={60}><Tex tex="Q_{ij}" /></Box>
      </Fade>
      <Fade o={minus}>
        <Box x={AX + W + 38} y={MY + W / 2 - 54} w={100} align="center" size={80}>{'−'}</Box>
      </Fade>
      <Fade o={equals}>
        <Box x={EX + W + 62} y={MY + W / 2 - 54} w={100} align="center" size={80}>=</Box>
      </Fade>
      <Fade o={cap} dy={14}>
        <Box x={960} y={MY + W + 50} w={1700} align="center" size={40}>
          The same three matrices for the karate club, with the nodes sorted by group.
        </Box>
      </Fade>
    </Frame>
  );
};
