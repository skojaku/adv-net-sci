import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {FormulaStack} from '../components/FormulaStack';
import {C, F} from '../theme';
import {HOLLOW, LOOK} from '../lib/look';
import {mix} from '../lib/network';
import {prog} from '../lib/anim';
import {lerp} from '../lib/plot';
import {arcs8} from '../lib/sbmLayout';
import {DC_EDGES, DC_GROUP, THETA} from '../lib/dc8';

/**
 * Maximum likelihood for the degree-corrected SBM, as for the SBM: first c fixed, theta and omega found.
 * 0: the log-likelihood in c, theta and omega (Poisson).
 * 1: fix c (the network is coloured by c): (theta-hat, omega-hat) = argmax over theta and omega.
 * 2: the answer, theta-hat_i = k_i / kappa_{c_i} and omega-hat_rs = m_rs; the nodes take the size theta-hat.
 * (Karrer and Newman: Eqs. 16 to 18. Their Eq. 17 is twice this log-likelihood: scripts/verify_dcsbm.py checks the form used here.)
 */
export const marks = [52, 112, 178];

const POS = arcs8(380, 440, 150);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const D0 = 60; // a node before its size means something
const dTheta = (i: number) => 132 * Math.sqrt(THETA[i]);

const sym = (tex: string, text: string) => (
  <div>
    <Tex tex={tex} style={{fontSize: 40}} />
    <span>: {text}</span>
  </div>
);
const ROWS = [
  {
    group: 0,
    tex: '\\begin{array}{l}\\log L(c,\\theta,\\omega)=\\sum_i k_i\\log\\theta_i\\\\[4pt]\\qquad+\\tfrac12\\sum_{r,s}\\Big(m_{rs}\\log\\omega_{rs}-\\omega_{rs}\\,\\theta_r\\theta_s\\Big)\\end{array}',
    note: (
      <>
        {sym('k_i', 'the degree of node i')}
        {sym('m_{rs}', 'the edges between groups r and s (twice when r = s)')}
        {sym('\\theta_r', 'the sum of \u03b8 over the group r, set to 1')}
      </>
    ),
  },
  {group: 1, tex: '\\text{fix } c:\\quad(\\hat\\theta,\\hat\\omega)=\\arg\\max_{\\theta,\\,\\omega}\\ \\log L(c,\\theta,\\omega)'},
  {group: 2, tex: '\\hat\\theta_i=\\dfrac{k_i}{\\kappa_{c_i}},\\qquad \\hat\\omega_{rs}=m_{rs}', note: sym('\\kappa_r', 'the total degree of group r')},
] as const;

export const S36: React.FC = () => {
  const frame = useCurrentFrame();

  const net = prog(frame, 6, 26);
  const colour = prog(frame, marks[0] + 6, marks[0] + 30);
  const size = prog(frame, marks[1] + 14, marks[1] + 46);
  const cap = prog(frame, marks[1] + 44, marks[1] + 60);

  return (
    <Frame n={36}>
      <Canvas>
        <g opacity={net}>
          {DC_EDGES.map((e, i) => (
            <line key={i} x1={POS[e[0]][0]} y1={POS[e[0]][1]} x2={POS[e[1]][0]} y2={POS[e[1]][1]} stroke={C.ink} strokeWidth={4} opacity={0.7} />
          ))}
          {POS.map((p, i) => {
            const lk = LOOK[DC_GROUP[i]];
            const d = lerp(D0, dTheta(i), size);
            return (
              <g key={i}>
                <circle cx={p[0]} cy={p[1]} r={d / 2 - 2.5} fill={HOLLOW.fill} stroke={HOLLOW.stroke} strokeWidth={5} />
                <circle cx={p[0]} cy={p[1]} r={d / 2 - 1.5} fill={mix('#ffffff', lk.fill, colour)} stroke="#fff" strokeWidth={3} opacity={colour} />
                <text x={p[0]} y={p[1] + 10} textAnchor="middle" fontFamily={F.serif} fontSize={30} fontWeight={700} fill={colour > 0.5 ? lk.text : HOLLOW.text}>
                  {LABELS[i]}
                </text>
              </g>
            );
          })}
        </g>
      </Canvas>
      <Fade o={cap} dy={12}>
        <Cap x={380} y={655} w={520}>node size: its share of the group&apos;s degree</Cap>
      </Fade>

      <FormulaStack rows={ROWS} marks={marks} x={720} y={200} w={1080} big={44} small={36} gap={18} />
    </Frame>
  );
};
