import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {prog} from '../lib/anim';
import {TOY_EDGES} from '../data/data';
import {Matrix, MatrixDegrees, TOY, TOY_A, TOY_E, ToyNet, fillE, num2, type CellStyle} from '../lib/b_matrix';

/**
 * Opens on the last picture of S09 (the network, A, its label and sentence).
 * 0: A fades out; the degrees k appear next to the nodes and along the matrix; the label becomes E_ij.
 * 1: the cells fill row by row with k_i k_j / 14; the cell of nodes 3 and 4 is ringed, with its arithmetic.
 * 2: the sentence.
 */
export const marks = [50, 174, 204];

const edgeIndex = (r: number, c: number): number => TOY_EDGES.findIndex(([u, v]) => (u === r && v === c) || (u === c && v === r));

export const S10: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const aOut = 1 - prog(frame, 0, 14);
  const degNet = prog(frame, 16, 36);
  const degMat = prog(frame, 26, 44);
  const eLabel = prog(frame, 16, 34);

  // stage 1
  const cellOp = (r: number, c: number) => prog(frame, 56 + 13 * r + 2 * c, 66 + 13 * r + 2 * c);
  const ring = prog(frame, 146, 158);
  const formula = prog(frame, 152, 170);

  // stage 2
  const cap = prog(frame, 176, 198);

  const at = (r: number, c: number): CellStyle => {
    if (frame < 55) {
      return edgeIndex(r, c) >= 0 ? {fill: C.blue, text: '1', color: '#fff', op: aOut} : {fill: 'none', text: '0', color: C.faint, op: aOut};
    }
    return {fill: fillE(TOY_E[r][c], 0.75), text: num2(TOY_E[r][c]), op: cellOp(r, c)};
  };
  void TOY_A;

  return (
    <Frame n={10} top={190}>
      <Canvas>
        <ToyNet degrees={degNet} />
        <Matrix x={TOY.mx} y={TOY.my} cell={TOY.cell} n={6} at={at} font={36} discs={{d: 52, size: 32}} rings={[[2, 3]]} ringOp={ring} />
        <MatrixDegrees x={TOY.mx} y={TOY.my} cell={TOY.cell} opacity={degMat} />
      </Canvas>
      <Fade o={aOut} dy={0}>
        <Box x={TOY.net[0][0] + 250} y={TOY.labelY} w={500} align="center" size={72}>
          <Tex tex="A_{ij}" />
        </Box>
        <Box x={TOY.net[0][0] - 60} y={TOY.captionY} w={640} size={38}>
          The entry for nodes i and j is 1 if they share an edge, and 0 if not.
        </Box>
      </Fade>
      <Fade o={eLabel} dy={14}>
        <Box x={TOY.net[0][0] + 250} y={TOY.labelY} w={500} align="center" size={72}>
          <Tex tex="E_{ij}" />
        </Box>
      </Fade>
      <Fade o={formula} dy={14}>
        <Box x={TOY.net[0][0] + 250} y={TOY.formulaY - 10} w={640} align="center" size={44}>
          <Tex tex="\dfrac{k_ik_j}{2M}=\dfrac{3\times3}{14}=0.64" />
        </Box>
      </Fade>
      <Fade o={cap} dy={14}>
        <Box x={TOY.net[0][0] - 60} y={TOY.captionY + 25} w={640} size={36}>
          A random network with the same degrees has this many edges between each pair, on average.
        </Box>
      </Fade>
    </Frame>
  );
};
