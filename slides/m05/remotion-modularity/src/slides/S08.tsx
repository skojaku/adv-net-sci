import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {prog} from '../lib/anim';
import {TOY_EDGES} from '../data/data';
import {Matrix, TOY, TOY_A, ToyNet, type CellStyle} from '../lib/b_matrix';

/**
 * 0: the small network (6 nodes, 6 edges) and an empty 6 x 6 grid, labelled A_ij.
 * 1: the cells fill: an edge lights both its cells (1), then the other cells, the diagonal included, get 0.
 */
export const marks = [50, 124];

const edgeIndex = (r: number, c: number): number => TOY_EDGES.findIndex(([u, v]) => (u === r && v === c) || (u === c && v === r));

export const S08: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const net = prog(frame, 2, 26);
  const grid = prog(frame, 22, 42);
  const label = prog(frame, 30, 46);

  // stage 1
  const one = (e: number) => prog(frame, 56 + 5 * e, 66 + 5 * e);
  const zeros = (r: number) => prog(frame, 100 + 2 * r, 112 + 2 * r);
  const cap = prog(frame, 104, 122);

  const at = (r: number, c: number): CellStyle => {
    const e = edgeIndex(r, c);
    if (e >= 0) return {fill: C.blue, text: '1', color: '#fff', op: one(e)};
    return {fill: 'none', text: '0', color: C.faint, op: zeros(r)};
  };

  return (
    <Frame n={8} top={190}>
      <Canvas>
        <ToyNet opacity={net} />
        <Matrix x={TOY.mx} y={TOY.my} cell={TOY.cell} n={6} at={at} font={36} discs={{d: 52, size: 32}} opacity={grid} />
      </Canvas>
      <Fade o={label} dy={14}>
        <Box x={TOY.net[0][0] + 250} y={TOY.labelY} w={500} align="center" size={72}>
          <Tex tex="A_{ij}" />
        </Box>
      </Fade>
      <Fade o={cap} dy={14}>
        <Box x={TOY.net[0][0] - 60} y={TOY.captionY} w={640} size={38}>
          The entry for nodes i and j is 1 if they share an edge, and 0 if not.
        </Box>
      </Fade>
    </Frame>
  );
};
