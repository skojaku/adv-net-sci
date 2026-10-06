import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {caption, fromStage, prog} from '../lib/anim';
import {LOOK} from '../lib/look';
import {DEG, PAIR_0_33, TWO_M} from '../data/data';
import {ToyDisc} from '../lib/a_toy';

/**
 * The value k_i k_j / 2M is a number of edges, not a probability.
 * 0: the formula; two hubs of the club (degrees 16 and 17): 16 x 17 / 156 = 1.74, above 1.
 * 1: two nodes of low degree (2 and 3): 2 x 3 / 156 = 0.04, close to a probability; for hubs or dense networks the approximation breaks.
 */
export const marks = [70, 130];

const HUBS: [number, number] = [DEG[0], DEG[33]]; // 16 and 17
const SMALL: [number, number] = [2, 3];
const ROW_A = 503;
const ROW_B = 673;
const D = 96;

const f2 = (x: number) => x.toFixed(2);

export const S08: React.FC = () => {
  const frame = useCurrentFrame();

  const top = prog(frame, 4, 24);
  const label = prog(frame, 22, 40);
  const rowA = prog(frame, 28, 50);
  const rowAValue = prog(frame, 40, 62);
  const rowB = fromStage(frame, marks, 1, 18);
  const s0 = caption(frame, marks, 0);
  const s1 = fromStage(frame, marks, 1, 16);

  const small = (SMALL[0] * SMALL[1]) / TWO_M;
  const hubs = (HUBS[0] * HUBS[1]) / TWO_M;
  if (Math.abs(hubs - PAIR_0_33) > 1e-3) throw new Error('S08: the hub value does not match data.ts');

  return (
    <Frame n={8}>
      <Canvas>
        <g opacity={rowA}>
          <ToyDisc p={[720, ROW_A]} d={D} look={LOOK[0]} label={HUBS[0]} size={44} />
          <ToyDisc p={[840, ROW_A]} d={D} look={LOOK[0]} label={HUBS[1]} size={44} />
        </g>
        <g opacity={rowB}>
          <ToyDisc p={[720, ROW_B]} d={D} look={LOOK[0]} label={SMALL[0]} size={44} />
          <ToyDisc p={[840, ROW_B]} d={D} look={LOOK[0]} label={SMALL[1]} size={44} />
        </g>
      </Canvas>
      <div style={{opacity: top}}>
        <Box x={650} y={225} w={700} size={66}>
          <Tex tex="\dfrac{k_ik_j}{2M}" />
        </Box>
      </div>
      <div style={{opacity: label}}>
        <Cap x={1010} y={290} w={800} align="left">expected number of edges</Cap>
      </div>
      <div style={{opacity: rowA}}>
        <Cap x={390} y={ROW_A - 32} w={280} align="left">two hubs</Cap>
      </div>
      <div style={{opacity: rowAValue}}>
        <Box x={950} y={ROW_A - 70} w={1000} size={56}>
          <Tex tex={`\\dfrac{${HUBS[0]}\\times${HUBS[1]}}{${TWO_M}}=${f2(hubs)}`} />
        </Box>
      </div>
      <div style={{opacity: rowB}}>
        <Cap x={390} y={ROW_B - 32} w={280} align="left">two small nodes</Cap>
        <Box x={950} y={ROW_B - 70} w={1000} size={56}>
          <Tex tex={`\\dfrac{${SMALL[0]}\\times${SMALL[1]}}{${TWO_M}}=${f2(small)}`} />
        </Box>
      </div>
      <div style={{opacity: s0}}>
        <Box x={390} y={800} w={1400} size={46} color={C.soft}>This is a number of edges, not a probability. Here it is above 1.</Box>
      </div>
      <div style={{opacity: s1}}>
        <Box x={390} y={800} w={1400} size={46} color={C.soft}>When it is small, it is close to a probability.</Box>
        <Box x={390} y={868} w={1400} size={46} color={C.soft}>For hubs or dense networks the approximation breaks. We leave that for another time.</Box>
      </div>
    </Frame>
  );
};
