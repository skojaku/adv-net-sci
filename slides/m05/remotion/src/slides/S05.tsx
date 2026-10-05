import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {betweenStages, prog, smooth} from '../lib/anim';
import {Network, toCanvas} from '../lib/network';
import {stackDots} from '../lib/dotstack';
import {KARATE_EDGES, KARATE_FOUR, KARATE_LOUVAIN_Q, KARATE_POS, KARATE_THREE} from '../data/data';

/**
 * 0: the club in four groups, Q = 0.407.
 * 1: the colours change to three groups (grey joins red, node 9 moves to blue), Q = 0.402.
 * 2: the club goes; the 16 Q values of 400 Louvain runs sit on a number line.
 */
export const marks = [60, 110, 172];

const POS = toCanvas(KARATE_POS, 160, 205, 900, 760);
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

  // the club, stages 0 and 1
  const club = 1 - prog(frame, marks[1], marks[1] + 14);
  const nodeOp = (i: number) => prog(frame, 0.4 * i, 0.4 * i + 10);
  const edgeOp = (i: number) => prog(frame, 6 + 0.28 * i, 6 + 0.28 * i + 10);
  const paint = smooth(frame, 26, 46); // all nodes alike to four groups
  const merge = smooth(frame, 66, 94); // four groups to three
  const pulse = prog(frame, 62, 72) * (1 - prog(frame, 90, 106));
  const ring = CHANGED.map((c) => (c && pulse > 0.02 ? `rgba(0, 0, 0, ${pulse.toFixed(3)})` : null));

  const cap0 = betweenStages(frame, marks, 0, 0);
  const capIn0 = prog(frame, 40, 58);
  const cap1 = betweenStages(frame, marks, 1, 1);

  // the number line, stage 2
  const axis = prog(frame, 116, 132);
  const dotOp = (i: number) => prog(frame, 128 + 2 * i, 128 + 2 * i + 8);
  const capA = prog(frame, 124, 142);
  const capB = prog(frame, 150, 168);

  return (
    <Frame n={5} title="Similar Q, different groups">
      <Canvas>
        <Network
          pos={POS}
          edges={EDGES}
          look={merge > 0 ? LOOK_FOUR : LOOK[0]}
          lookTo={merge > 0 ? LOOK_THREE : LOOK_FOUR}
          t={merge > 0 ? merge : paint}
          nodeD={46}
          nodeOp={nodeOp}
          edgeOp={edgeOp}
          ring={ring}
          ringW={7}
          opacity={club}
        />
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

      {/* stages 0 and 1: the captions */}
      <Fade o={cap0 * capIn0} dy={16}>
        <Tag x={1470} y={440}>Q = 0.407</Tag>
        <Cap x={1470} y={528} w={600}>four groups</Cap>
      </Fade>
      <Fade o={cap1} dy={16}>
        <Tag x={1470} y={440}>Q = 0.402</Tag>
        <Cap x={1470} y={528} w={600}>three groups</Cap>
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
