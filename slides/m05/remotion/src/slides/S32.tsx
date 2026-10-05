import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {BEST_LIK} from '../lib/sbmscore';

/**
 * The best log L over all groupings into K groups, K = 1 to 8, for the 8-node network.
 * 0: it never decreases as K grows.
 * 1: more groups, more parameters, a better fit: from K = 5 on the fit is perfect (log L = 0).
 * 2: a large K overfits: K = 8 (every node alone) is a perfect fit and finds no groups.
 */
export const marks = [70, 126, 180];

const X0 = 230;
const X1 = 1130;
const Y0 = 835; // log L = -20
const Y1 = 290; // log L = 1
const px = (k: number) => X0 + ((k - 1) / 7) * (X1 - X0);
const py = (v: number) => Y0 - ((v + 20) / 21) * (Y0 - Y1);
const PTS = BEST_LIK.map((v, i) => [px(i + 1), py(v)] as const);

export const S32: React.FC = () => {
  const frame = useCurrentFrame();

  const axes = prog(frame, 0, 16);
  const dot = (i: number) => prog(frame, 14 + i * 5, 26 + i * 5);
  const cap0 = betweenStages(frame, marks, 0, 0) * prog(frame, 50, 66);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = fromStage(frame, marks, 2, 14);
  const flat = fromStage(frame, marks, 1, 14);
  const last = fromStage(frame, marks, 2, 14);

  return (
    <Frame n={32} title="More groups always fit better">
      <Canvas>
        <g opacity={axes}>
          <line x1={X0} y1={Y0} x2={X1 + 30} y2={Y0} stroke={C.soft} strokeWidth={3} />
          <line x1={X0} y1={Y1 - 20} x2={X0} y2={Y0} stroke={C.soft} strokeWidth={3} />
          {BEST_LIK.map((_, i) => (
            <g key={i}>
              <line x1={px(i + 1)} y1={Y0} x2={px(i + 1)} y2={Y0 + 10} stroke={C.soft} strokeWidth={3} />
              <text x={px(i + 1)} y={Y0 + 52} textAnchor="middle" fontFamily={F.serif} fontSize={38} fill={C.soft}>
                {i + 1}
              </text>
            </g>
          ))}
          {[-20, -15, -10, -5, 0].map((v) => (
            <g key={v}>
              <line x1={X0 - 10} y1={py(v)} x2={X0} y2={py(v)} stroke={C.soft} strokeWidth={3} />
              <text x={X0 - 20} y={py(v) + 13} textAnchor="end" fontFamily={F.serif} fontSize={38} fill={C.soft}>
                {v === 0 ? '0' : `−${-v}`}
              </text>
            </g>
          ))}
          <text x={X1 + 30} y={Y0 + 112} textAnchor="end" fontFamily={F.hand} fontSize={45} fill={C.soft}>
            number of groups K
          </text>
          <text x={120} y={Y1 - 50} textAnchor="start" fontFamily={F.hand} fontSize={45} fill={C.soft}>
            best log L
          </text>
        </g>
        {/* the line through the points */}
        {PTS.slice(1).map(([x, y], i) => (
          <line key={i} x1={PTS[i][0]} y1={PTS[i][1]} x2={x} y2={y} stroke={C.blue} strokeWidth={5} opacity={Math.min(dot(i), dot(i + 1))} />
        ))}
        {PTS.map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r={15} fill={C.blue} stroke="#fff" strokeWidth={3} opacity={dot(i)} />
        ))}
        {/* from K = 5 on, a perfect fit */}
        <g opacity={flat}>
          <line x1={px(5) - 24} y1={py(0)} x2={px(8) + 24} y2={py(0)} stroke={C.ink} strokeWidth={4} strokeDasharray="12 10" />
        </g>
        {/* K = 8: every node alone */}
        <g opacity={last}>
          <circle cx={PTS[7][0]} cy={PTS[7][1]} r={26} fill="none" stroke={C.ink} strokeWidth={7} />
        </g>
      </Canvas>
      <Fade o={cap0} dy={14}>
        <Box x={1230} y={380} w={580} size={50}>
          <Tex tex="\log L" /> never decreases as <Tex tex="K" /> grows
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={1230} y={380} w={580} size={50}>
          More groups, more parameters, a better fit
        </Box>
      </Fade>
      <Fade o={cap2} dy={14}>
        <Box x={1230} y={380} w={580} size={50}>
          A large <Tex tex="K" /> overfits: the groups mean nothing
        </Box>
        <Box x={1230} y={600} w={580} size={42} color={C.soft}>
          <Tex tex="K = 8" />: every node alone, a perfect fit
        </Box>
      </Fade>
    </Frame>
  );
};
