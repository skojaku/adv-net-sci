import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {fromStage, prog} from '../lib/anim';
import {Network} from '../lib/network';
import {FLIP_INSIDE, FLIP_ORDER} from '../data/data';
import {CLUB_L} from '../lib/club';
import {CountRow, EDGES, FRAC_Y, Fraction, PANEL_X, Legend, REAL_B, ROW1_Y, ROW2_Y, clubEdges, discLook} from '../lib/a_club';

/**
 * Opens on the picture S02 ends with (club at the left, counts and the fraction at the right).
 * 0: the question.
 * 1: the orange nodes join the blue group one at a time (FLIP_ORDER); the counts follow (FLIP_INSIDE).
 * 2: everyone in one group: 78 of 78.
 */
export const marks = [24, 130, 190];

const FLIP_START = marks[0] + 6;
const PER = 5; // frames between two flips
const DUR = 10; // frames one node takes to change colour

const FRAC_TEXT = (n: number) => (n / 78).toFixed(3);

export const S03: React.FC = () => {
  const frame = useCurrentFrame();

  // b[i]: how blue node i is
  const b = REAL_B.map((v) => v);
  FLIP_ORDER.forEach((node, k) => {
    b[node] = prog(frame, FLIP_START + PER * k, FLIP_START + PER * k + DUR);
  });
  // the count changes in the middle of the colour change
  const done = FLIP_ORDER.filter((_, k) => frame >= FLIP_START + PER * k + DUR / 2).length;
  const inside = FLIP_INSIDE[done];
  const last = done === FLIP_ORDER.length;

  const answer = fromStage(frame, marks, 2, 18);
  const question = prog(frame, 0, 14) * (1 - answer);

  return (
    <Frame n={3} zoom={1.07}>
      <Canvas>
        <Network pos={CLUB_L} edges={EDGES} look={b.map(discLook)} nodeD={46} {...clubEdges(b, 1)} />
        <Legend o1={1} o2={1} />
      </Canvas>
      <CountRow y={ROW1_Y} label="inside" n={inside} o={1} />
      <CountRow y={ROW2_Y} label="between" n={78 - inside} o={1} />
      <Fraction inside={inside} m={78} value={last ? '1.000' : FRAC_TEXT(inside)} red={last} o={1} />
      <Cap x={PANEL_X + 500} y={FRAC_Y + 62} w={300} align="left">M = 78 edges</Cap>
      <div style={{opacity: question}}>
        <Box x={1010} y={FRAC_Y + 200} w={800} size={46}>Which grouping gives the highest score?</Box>
      </div>
      <div style={{opacity: answer, transform: `translateY(${(1 - answer) * 14}px)`}}>
        <Box x={1010} y={FRAC_Y + 200} w={800} size={46}>
          Everyone in one group gives the highest score. The score says nothing about the network.
        </Box>
      </div>
    </Frame>
  );
};
