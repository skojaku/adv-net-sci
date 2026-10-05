import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {prog} from '../lib/anim';
import {Network, toCanvas} from '../lib/network';
import {stackDots} from '../lib/dotstack';
import {KARATE_EDGES, KARATE_FOUR, KARATE_LOUVAIN_Q, KARATE_POS, KARATE_THREE} from '../data/data';

/**
 * 0: the club in four groups, Q = 0.407.
 * 1: the same club in three groups beside it, Q = 0.402: both colourings are on the screen at once, so they can be
 *    compared. The nodes whose group differs (the purple group joins brown, one node moves to blue) are ringed in both.
 * 2: the clubs go; the 16 Q values of 400 Louvain runs sit on a number line.
 */
export const marks = [60, 110, 172];

const POS_L = toCanvas(KARATE_POS, 135, 285, 750, 540);
const POS_R = toCanvas(KARATE_POS, 1035, 285, 750, 540);
const EDGES = KARATE_EDGES as unknown as [number, number][];
const LOOK_FOUR = KARATE_FOUR.map((g) => LOOK[g]);
const LOOK_THREE = KARATE_THREE.map((g) => LOOK[g]);
const CHANGED = KARATE_FOUR.map((g, i) => g !== KARATE_THREE[i]);

// the number line of stage 2
const X0 = 180;
const X1 = 1740;
const LY = 640;
const Q0 = 0.38;
const Q1 = 0.42;
const xOf = (q: number) => X0 + ((q - Q0) / (Q1 - Q0)) * (X1 - X0);
const DOT = 38;
const PITCH = 42;
const DOTS = stackDots(KARATE_LOUVAIN_Q, xOf, PITCH);

export const S05: React.FC = () => {
  const frame = useCurrentFrame();

  // the two clubs, stages 0 and 1
  const clubs = 1 - prog(frame, marks[1], marks[1] + 14);
  const leftIn = (i: number) => prog(frame, 0.4 * i, 0.4 * i + 12);
  const rightIn = (i: number) => prog(frame, marks[0] + 2 + 0.4 * i, marks[0] + 2 + 0.4 * i + 12);
  const edgeL = (i: number) => prog(frame, 6 + 0.28 * i, 6 + 0.28 * i + 10);
  const edgeR = (i: number) => prog(frame, marks[0] + 8 + 0.28 * i, marks[0] + 8 + 0.28 * i + 10);
  const pulse = prog(frame, marks[0] + 40, marks[0] + 50);
  const ring = CHANGED.map((c) => (c && pulse > 0.02 ? `rgba(0, 0, 0, ${pulse.toFixed(3)})` : null));

  const capL = prog(frame, 18, 36) * clubs;
  const capR = prog(frame, marks[0] + 18, marks[0] + 36) * clubs;

  // the number line, stage 2
  const axis = prog(frame, 116, 132);
  const dotOp = (i: number) => prog(frame, 128 + 2 * i, 128 + 2 * i + 8);
  const capA = prog(frame, 124, 142);
  const capB = prog(frame, 150, 168);

  return (
    <Frame n={5} zoom={1.04}>
      <Canvas>
        <Network pos={POS_L} edges={EDGES} look={LOOK_FOUR} nodeD={40} edgeW={2.5} nodeOp={leftIn} edgeOp={edgeL} ring={ring} ringW={6} opacity={clubs} />
        <Network pos={POS_R} edges={EDGES} look={LOOK_THREE} nodeD={40} edgeW={2.5} nodeOp={rightIn} edgeOp={edgeR} ring={ring} ringW={6} opacity={clubs} />
        <g opacity={axis}>
          <line x1={X0 - 20} y1={LY} x2={X1 + 20} y2={LY} stroke={C.soft} strokeWidth={3} />
          {[0.38, 0.39, 0.4, 0.41, 0.42].map((q) => (
            <g key={q}>
              <line x1={xOf(q)} y1={LY} x2={xOf(q)} y2={LY + 12} stroke={C.soft} strokeWidth={3} />
              <text x={xOf(q)} y={LY + 58} textAnchor="middle" fontFamily={F.serif} fontSize={38} fill={C.soft}>
                {q.toFixed(2)}
              </text>
            </g>
          ))}
          <text x={X1 + 20} y={LY + 118} textAnchor="end" fontFamily={F.hand} fontSize={45} fill={C.soft}>
            Q
          </text>
        </g>
        {DOTS.map((d, i) => (
          <circle key={i} cx={d.x} cy={LY - DOT / 2 - 6 - d.row * PITCH} r={DOT / 2} fill={C.blue} stroke="#fff" strokeWidth={2} opacity={dotOp(i)} />
        ))}
      </Canvas>

      {/* stages 0 and 1: under each club */}
      <Fade o={capL} dy={16}>
        <Cap x={510} y={212} w={800}>four groups</Cap>
        <Tag x={510} y={850}>Q = 0.407</Tag>
      </Fade>
      <Fade o={capR} dy={16}>
        <Cap x={1410} y={212} w={800}>three groups</Cap>
        <Tag x={1410} y={850}>Q = 0.402</Tag>
      </Fade>

      {/* stage 2 */}
      <Fade o={capA} dy={14}>
        <Cap y={232} w={1600}>400 Louvain runs, 16 different splits</Cap>
      </Fade>
      <Fade o={capB} dy={14}>
        <Box x={960} y={820} w={1500} align="center" size={45}>
          Different splits, almost the same Q.
        </Box>
      </Fade>
    </Frame>
  );
};
