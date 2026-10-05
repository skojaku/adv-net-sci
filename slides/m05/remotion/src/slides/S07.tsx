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
import {lerp} from '../lib/plot';
import {NOISE100_Q, NOISE34_Q, NOISE_EDGES, NOISE_LEVELS, NOISE_POS} from '../data/data';

/**
 * 0: Louvain runs on the random network: grey, then its first groups, then the final 5. Q = 0.346.
 * 1: the network goes; the Q of 200 random networks of the same size on a number line, and the 0.3 rule.
 * 2: the karate club's 0.420 as a red line, outside the cloud.
 * 3: a second row for 100-node random networks; the red line goes through it.
 */
export const marks = [86, 150, 200, 258];

// ---- the network (stage 0)
const POS = toCanvas(NOISE_POS, 160, 205, 900, 760);
const EDGES = NOISE_EDGES as unknown as [number, number][];
const LEVELS = NOISE_LEVELS as unknown as number[][];
const FINAL = LEVELS[LEVELS.length - 1];

// ---- the number lines
const X0 = 200;
const X1 = 1780;
const Q0 = 0.3;
const Q1 = 0.48;
const xOf = (q: number) => X0 + ((q - Q0) / (Q1 - Q0)) * (X1 - X0);
const DOT = 16;
const PITCH = 18;
const D34 = stackDots(NOISE34_Q, xOf, PITCH);
const D100 = stackDots(NOISE100_Q, xOf, PITCH);
const BASE1 = 700; // baseline of the first row while it is alone
const BASE1_UP = 525; // and with the second row
const BASE2 = 790;
const TOP_ABOVE = 320; // how far a vertical line rises above the first baseline
const TICKS = [0.3, 0.35, 0.4, 0.45];

const Axis: React.FC<{y: number}> = ({y}) => (
  <g>
    <line x1={X0 - 20} y1={y} x2={X1 + 20} y2={y} stroke={C.soft} strokeWidth={3} />
    {TICKS.map((q) => (
      <g key={q}>
        <line x1={xOf(q)} y1={y} x2={xOf(q)} y2={y + 12} stroke={C.soft} strokeWidth={3} />
        <text x={xOf(q)} y={y + 54} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>
          {q.toFixed(2)}
        </text>
      </g>
    ))}
    <text x={X1 + 20} y={y + 12} textAnchor="start" fontFamily={F.hand} fontSize={45} fill={C.soft}>
      Q
    </text>
  </g>
);

export const S07: React.FC = () => {
  const frame = useCurrentFrame();

  // ---- stage 0: the network
  const net = 1 - prog(frame, marks[0], marks[0] + 12);
  // each final group changes look in turn
  const turn = (g: number) => smooth(frame, 12 + 11 * g, 28 + 11 * g);
  const tag = prog(frame, 64, 80);

  // ---- stage 1: row 1
  const s1 = marks[0];
  const axis1 = prog(frame, s1 + 8, s1 + 22);
  const dot1 = (i: number) => prog(frame, s1 + 16 + 0.2 * i, s1 + 16 + 0.2 * i + 6);
  const rule = prog(frame, s1 + 40, s1 + 56);
  const lab1 = prog(frame, s1 + 14, s1 + 30);

  // ---- stage 2: the club
  const s2 = marks[1];
  const club = prog(frame, s2 + 4, s2 + 24);
  const capA = betweenStages(frame, marks, 2, 2);
  const capAIn = prog(frame, s2 + 22, s2 + 42);

  // ---- stage 3: row 2
  const s3 = marks[2];
  const up = smooth(frame, s3 + 2, s3 + 26);
  const axis2 = prog(frame, s3 + 14, s3 + 28);
  const dot2 = (i: number) => prog(frame, s3 + 22 + 0.22 * i, s3 + 22 + 0.22 * i + 6);
  const lab2 = prog(frame, s3 + 20, s3 + 36);
  const ext = prog(frame, s3 + 24, s3 + 44);
  const capB = prog(frame, s3 + 40, s3 + 58);

  const base1 = lerp(BASE1, BASE1_UP, up);
  const dy1 = base1 - BASE1;
  const xClub = xOf(0.42);
  const xRule = xOf(0.3);
  const rowY = (base: number, row: number) => base - DOT / 2 - 6 - row * PITCH;

  return (
    <Frame n={7} zoom={1.03} top={185}>
      {/* stage 0 */}
      <Canvas>
        <Network pos={POS} edges={EDGES} nodeD={46} opacity={net} />
        {[1, 2, 3, 4].map((g) => (
          <Network
            key={g}
            pos={POS}
            edges={[]}
            look={LOOK[0]}
            lookTo={FINAL.map(() => LOOK[g])}
            t={turn(g)}
            nodeOp={(i) => (FINAL[i] === g ? 1 : 0)}
            nodeD={46}
            opacity={net}
          />
        ))}
      </Canvas>
      <Fade o={net * tag} dy={16}>
        <Tag x={1470} y={480}>Q = 0.346</Tag>
      </Fade>

      {/* stages 1 to 3 */}
      <Canvas>
        {/* row 1 */}
        <g transform={`translate(0 ${dy1})`}>
          <g opacity={axis1}>
            <Axis y={BASE1} />
          </g>
          {D34.map((d, i) => (
            <circle key={i} cx={d.x} cy={rowY(BASE1, d.row)} r={DOT / 2} fill={C.blue} opacity={dot1(i)} />
          ))}
          <g opacity={rule}>
            <line x1={xRule} y1={BASE1 - TOP_ABOVE} x2={xRule} y2={BASE1} stroke={C.ink} strokeWidth={4} strokeDasharray="12 9" />
            <text x={xRule + 16} y={BASE1 - TOP_ABOVE + 40} fontFamily={F.hand} fontSize={45} fill={C.ink}>
              rule of thumb:
            </text>
            <text x={xRule + 16} y={BASE1 - TOP_ABOVE + 92} fontFamily={F.hand} fontSize={45} fill={C.ink}>
              Q &gt; 0.3
            </text>
          </g>
          <g opacity={lab1}>
            <text x={790} y={BASE1 - 200} fontFamily={F.hand} fontSize={45} fill={C.soft}>
              200 random networks
            </text>
          </g>
        </g>
        {/* row 2 */}
        <g opacity={axis2}>
          <Axis y={BASE2} />
        </g>
        {D100.map((d, i) => (
          <circle key={i} cx={d.x} cy={rowY(BASE2, d.row)} r={DOT / 2} fill={C.blue} opacity={dot2(i)} />
        ))}
        <g opacity={lab2}>
          <text x={240} y={BASE2 - 70} fontFamily={F.hand} fontSize={45} fill={C.soft}>
            100 random networks
          </text>
        </g>
        {/* the club's line: stage 2, and through both rows in stage 3 */}
        <g opacity={club}>
          <line
            x1={xClub}
            y1={BASE1 - TOP_ABOVE + dy1}
            x2={xClub}
            y2={lerp(BASE1 + dy1, BASE2, ext)}
            stroke={C.ink}
            strokeWidth={5}
          />
          <text x={xClub + 16} y={BASE1 - TOP_ABOVE + dy1 + 40} fontFamily={F.hand} fontSize={45} fill={C.red}>
            karate club: Q = 0.420
          </text>
        </g>
      </Canvas>

      {/* captions */}
      <Fade o={capA * capAIn} dy={14}>
        <Cap y={880} w={1560}>We compare Q with random networks of the same size.</Cap>
      </Fade>
      <Fade o={capB} dy={14}>
        <Cap y={900} w={1560}>A random network with 100 nodes scores as high as the club.</Cap>
      </Fade>
    </Frame>
  );
};
