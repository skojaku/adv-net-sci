import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {prog} from '../lib/anim';
import {H_GIVEN, H_TRUE, I_TF, f3} from '../lib/entropy8';

/**
 * 0: the number of questions before the hint (1.000) and after it (0.451), joined by an arrow.
 * 1: I = 1.000 - 0.451 = 0.549: mutual information, the questions saved.
 */
export const marks = [50, 100];

const LX = 480; // centre of the "before" block
const RX = 1440; // centre of the "after" block
const NUM_Y = 330;

const Block: React.FC<{x: number; label: string; value: string; op: number}> = ({x, label, value, op}) => (
  <Fade o={op} dy={14}>
    <Box x={x} y={NUM_Y - 70} w={760} align="center" size={45} color={C.soft} hand>
      {label}
    </Box>
    <Box x={x} y={NUM_Y} w={760} align="center" size={120} style={{lineHeight: 1.1}}>
      {value}
    </Box>
    <Box x={x} y={NUM_Y + 140} w={760} align="center" size={40} color={C.soft}>
      questions
    </Box>
  </Fade>
);

export const S17: React.FC = () => {
  const frame = useCurrentFrame();

  const before = prog(frame, 0, 18);
  const arrow = prog(frame, 14, 32);
  const after = prog(frame, 26, 44);
  const eq = prog(frame, 56, 76);
  const saved = prog(frame, 76, 94);

  const ax0 = LX + 330;
  const ax1 = RX - 330;
  const ay = NUM_Y + 80;
  const ax = ax0 + (ax1 - ax0) * arrow;

  return (
    <Frame n={17} title="Mutual information: questions saved">
      <Canvas>
        <g opacity={arrow}>
          <line x1={ax0} y1={ay} x2={ax} y2={ay} stroke={C.blue} strokeWidth={9} strokeLinecap="round" />
          <path d={`M ${ax - 30} ${ay - 30} L ${ax + 4} ${ay} L ${ax - 30} ${ay + 30}`} fill="none" stroke={C.blue} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
        </g>
      </Canvas>
      <Block x={LX} label="without the found groups" value={f3(H_TRUE)} op={before} />
      <Block x={RX} label="with the found groups" value={f3(H_GIVEN)} op={after} />
      <Fade o={eq} dy={14}>
        <div style={{position: 'absolute', left: 120, top: 640, width: 1680, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 44, fontFamily: F.serif}}>
          <span style={{fontSize: 52}}>
            <Term>mutual information</Term>
          </span>
          <Tex tex={`I = ${f3(H_TRUE)} - ${f3(H_GIVEN)} = ${f3(I_TF)}`} style={{fontSize: 64}} />
        </div>
      </Fade>
      <Fade o={saved} dy={12}>
        <Cap x={960} y={790} w={1400}>
          questions saved
        </Cap>
      </Fade>
    </Frame>
  );
};
