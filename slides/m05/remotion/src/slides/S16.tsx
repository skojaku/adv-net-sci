import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {prog} from '../lib/anim';
import {AB_RANGES, BOX_PAD, GROUP_A, GROUP_B, H_GIVEN, HiddenNode, Row8, eightX, f3} from '../lib/entropy8';

/**
 * 0: the hidden node is in found group A (4 solid, 1 hollow): still unsure, 0.722 questions left.
 * 1: if it were in group B (all hollow): 0 questions left.
 * 2: the average over the nodes: H(true given found) = 5/8 x 0.722 + 3/8 x 0 = 0.451.
 */
export const marks = [55, 105, 165];

const CX = 1020;
const GAP = 150;
const ROW_Y = 500;
const PICK_Y = 310;
// the arrows point at the group box, between two nodes, so that they do not single out a node
const A_MID = (eightX(0, CX, GAP) + eightX(4, CX, GAP)) / 2;
const B_MID = (eightX(5, CX, GAP) + eightX(7, CX, GAP)) / 2;
const A_ARROW = A_MID + GAP / 2;
const B_ARROW = B_MID - GAP / 2;
const BOX_TOP = ROW_Y - BOX_PAD;

const texGiven = `H(\\text{true given found}) = \\dfrac{${GROUP_A.n}}{8} \\times ${f3(GROUP_A.h)} + \\dfrac{${GROUP_B.n}}{8} \\times ${GROUP_B.h} = ${f3(H_GIVEN)}`;

/** A short arrow from the hidden node down to its box. */
const Arrow: React.FC<{x: number; op: number}> = ({x, op}) => (
  <g opacity={op}>
    <line x1={x} y1={PICK_Y + 66} x2={x} y2={BOX_TOP - 14} stroke={C.ink} strokeWidth={5} />
    <path d={`M ${x - 14} ${BOX_TOP - 30} L ${x} ${BOX_TOP - 8} L ${x + 14} ${BOX_TOP - 30}`} fill="none" stroke={C.ink} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
  </g>
);

export const S16: React.FC = () => {
  const frame = useCurrentFrame();

  const boxes = prog(frame, 10, 28);
  const names = prog(frame, 20, 34);
  const pickA = prog(frame, 28, 44);
  const capA = prog(frame, 40, 54);
  const pickB = prog(frame, 60, 76);
  const capB = prog(frame, 76, 92);
  const formula = prog(frame, 112, 134);
  const avg = prog(frame, 144, 160);

  return (
    <Frame n={16} title="Now we see the found group">
      <Canvas>
        <Row8 cx={CX} y={ROW_Y} gap={GAP} boxes={AB_RANGES} boxOp={boxes} boxHot={(k) => (k === 0 ? pickA : pickB)} nodeOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)} />
        <HiddenNode x={A_ARROW} y={PICK_Y} halo={1} op={pickA} />
        <Arrow x={A_ARROW} op={pickA} />
        <HiddenNode x={B_ARROW} y={PICK_Y} halo={1} op={pickB} />
        <Arrow x={B_ARROW} op={pickB} />
      </Canvas>
      <Fade o={names} dy={10}>
        <Box x={eightX(0, CX, GAP) - BOX_PAD + 6} y={BOX_TOP - 62} w={200} size={45} color={C.soft} hand>
          A
        </Box>
        <Box x={eightX(5, CX, GAP) - BOX_PAD + 6} y={BOX_TOP - 62} w={200} size={45} color={C.soft} hand>
          B
        </Box>
      </Fade>
      <Fade o={capA} dy={12}>
        <Box x={A_MID} y={ROW_Y + 78} w={720} align="center" size={45}>
          {f3(GROUP_A.h)} questions left
        </Box>
      </Fade>
      <Fade o={capB} dy={12}>
        <Box x={B_MID} y={ROW_Y + 78} w={560} align="center" size={45}>
          {GROUP_B.h} questions left
        </Box>
      </Fade>
      <Fade o={formula} dy={14}>
        <div style={{position: 'absolute', left: 120, top: 690, width: 1680, display: 'flex', justifyContent: 'center', fontFamily: F.serif, fontSize: 50, whiteSpace: 'nowrap'}}>
          <Tex tex={texGiven} />
        </div>
      </Fade>
      <Fade o={avg} dy={12}>
        <Cap x={960} y={850} w={1500}>
          average over nodes: {GROUP_A.n} in A, {GROUP_B.n} in B
        </Cap>
      </Fade>
    </Frame>
  );
};
