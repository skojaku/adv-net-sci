import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {TOY_EDGES} from '../data/data';
import {Matrix, MatrixDegrees, TOY, TOY_B, TOY_E, ToyNet, fillB, fillE, num2, type CellStyle} from '../lib/b_matrix';

/**
 * Opens on the last picture of S10 (the network, E with its degrees and the ringed cell, the formula, the sentence).
 * 0: those fade out, E moves to the middle and shrinks, A appears at its left, a minus sign between them.
 * 1: "=" and B, A - E, cell by cell (blue above 0, brown below 0); the formula B_ij = A_ij - k_i k_j / 2M.
 * 2: the sentence about the colours.
 * 3: the row sums of B (all 0).
 */
export const marks = [72, 148, 188, 232];

const CELL = 72;
const MY = 340;
const AX = 164;
const EX = 700;
const BX = 1262;
const W = 6 * CELL;
const OPS_Y = MY + W / 2 - 52;

const edgeIndex = (r: number, c: number): number => TOY_EDGES.findIndex(([u, v]) => (u === r && v === c) || (u === c && v === r));

export const S11: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const oldOut = 1 - prog(frame, 0, 14);
  const netOut = 1 - prog(frame, 0, 18);
  const move = smooth(frame, 6, 56);
  const aRow = (r: number) => prog(frame, 30 + 3 * r, 44 + 3 * r);
  const minus = prog(frame, 52, 68);

  // stage 1
  const equals = prog(frame, 74, 90);
  const bLabel = prog(frame, 84, 100);
  const bCell = (r: number, c: number) => prog(frame, 80 + (6 * r + c), 92 + (6 * r + c));
  const formula = prog(frame, 112, 132);

  // stage 2 and 3
  const say2 = prog(frame, 150, 170) * (1 - prog(frame, 190, 202));
  const say3 = prog(frame, 192, 212);
  const sum = (r: number) => prog(frame, 196 + 4 * r, 210 + 4 * r);
  const sumHead = prog(frame, 192, 208);

  const eX = lerp(TOY.mx, EX, move);
  const eY = lerp(TOY.my, MY, move);
  const eCell = lerp(TOY.cell, CELL, move);
  const eFont = lerp(36, 24, move);
  const eDisc = lerp(52, 40, move);
  const eDiscSize = lerp(32, 24, move);

  const atA = (r: number, c: number): CellStyle =>
    edgeIndex(r, c) >= 0 ? {fill: C.blue, text: '1', color: '#fff', op: aRow(r)} : {fill: 'none', text: '0', color: C.faint, op: aRow(r)};
  const atE = (r: number, c: number): CellStyle => ({fill: fillE(TOY_E[r][c], 0.75), text: num2(TOY_E[r][c])});
  const atB = (r: number, c: number): CellStyle => ({fill: fillB(TOY_B[r][c], 0.75), text: num2(TOY_B[r][c]), op: bCell(r, c)});

  const rowSum = (r: number) => {
    const s = TOY_B[r].reduce((t, v) => t + v, 0);
    return Math.abs(s) < 1e-9 ? '0' : num2(s);
  };

  const labelAt = (x: number) => x + W / 2;

  return (
    <Frame n={11} top={190}>
      <Canvas>
        <ToyNet degrees={1} opacity={netOut} />
        <Matrix x={AX} y={MY} cell={CELL} n={6} at={atA} font={24} discs={{d: 40, size: 24}} opacity={aRow(0)} />
        <Matrix x={eX} y={eY} cell={eCell} n={6} at={atE} font={eFont} discs={{d: eDisc, size: eDiscSize}} rings={[[2, 3]]} ringOp={oldOut} />
        <MatrixDegrees x={TOY.mx} y={TOY.my} cell={TOY.cell} opacity={oldOut} />
        <Matrix x={BX} y={MY} cell={CELL} n={6} at={atB} font={24} discs={{d: 40, size: 24, op: equals}} opacity={equals} />
        <g fontFamily={F.serif} fontSize={30} fill={C.ink} textAnchor="middle">
          <text x={BX + W + 52} y={MY - 12} fill={C.soft} opacity={sumHead}>sum</text>
          {TOY_B.map((_, r) => (
            <text key={r} x={BX + W + 52} y={MY + (r + 0.5) * CELL + 10} opacity={sum(r)}>{rowSum(r)}</text>
          ))}
        </g>
      </Canvas>
      <Fade o={oldOut} dy={0}>
        <Box x={TOY.net[0][0] + 250} y={TOY.labelY} w={500} align="center" size={72}>
          <Tex tex="E_{ij}" />
        </Box>
        <Box x={TOY.net[0][0] + 250} y={TOY.formulaY - 10} w={640} align="center" size={44}>
          <Tex tex="\dfrac{k_ik_j}{2M}=\dfrac{3\times3}{14}=0.64" />
        </Box>
        <Box x={TOY.net[0][0] - 60} y={TOY.captionY + 25} w={640} size={36}>
          A random network with the same degrees has this many edges between each pair, on average.
        </Box>
      </Fade>
      <Fade o={aRow(0) * move}>
        <Box x={labelAt(AX)} y={185} w={400} align="center" size={60}><Tex tex="A_{ij}" /></Box>
        <Box x={labelAt(EX)} y={185} w={400} align="center" size={60}><Tex tex="E_{ij}" /></Box>
      </Fade>
      <Fade o={minus}>
        <Box x={AX + W + 29} y={OPS_Y} w={100} align="center" size={80}>{'−'}</Box>
      </Fade>
      <Fade o={equals}>
        <Box x={EX + W + 39} y={OPS_Y} w={100} align="center" size={80}>=</Box>
      </Fade>
      <Fade o={bLabel} dy={10}>
        <Box x={labelAt(BX)} y={185} w={400} align="center" size={60}><Tex tex="B_{ij}" /></Box>
      </Fade>
      <Fade o={formula} dy={14}>
        <Box x={AX + 40} y={MY + W + 70} w={1000} size={50}>
          <Tex tex="B_{ij}=A_{ij}-\dfrac{k_ik_j}{2M}" />
        </Box>
      </Fade>
      <Fade o={say2} dy={14}>
        <Box x={BX - 50} y={MY + W + 52} w={600} size={36}>
          <span style={{color: C.blue, fontWeight: 700}}>Positive</span>: more edges than chance. <span style={{color: C.brown, fontWeight: 700}}>Negative</span>: fewer.
        </Box>
      </Fade>
      <Fade o={say3} dy={14}>
        <Box x={BX - 50} y={MY + W + 52} w={600} size={36}>
          Each row of B sums to 0.
        </Box>
      </Fade>
    </Frame>
  );
};
