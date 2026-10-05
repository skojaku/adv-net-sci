import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {FormulaStack} from '../components/FormulaStack';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {prog} from '../lib/anim';
import {arcs8} from '../lib/sbmLayout';
import {DC_EDGES, DC_GROUP, FROM_DEGREES, M2, THETA} from '../lib/dc8';

/**
 * The degree-corrected SBM, step 2: put theta-hat and omega-hat back; only c is left.
 * 0: a formula in c alone: log L(c) = 1/2 sum m_rs log(m_rs / (kappa_r kappa_s)) + const. On the left: the edges seen
 *    in each block against the edges the degrees alone would give, kappa_r kappa_s / 2m (10, 1, 1, 12 against 5.04, 5.96, 5.96, 7.04).
 * 1: the same is m times the mutual information I(c) of the groups at the two ends of an edge (plus a constant).
 * 2: I(c) with p(r, s) = m_rs / 2m and p(r) = kappa_r / 2m: the joint over the marginals, as for the NMI.
 * 3: all that is left: maximize over c.
 * (Karrer and Newman print the sum without the factor 1/2: an unnormalized log-likelihood; scripts/verify_dcsbm.py checks the factor.)
 */
export const marks = [58, 118, 178, 232];

const POS = arcs8(380, 360, 120);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const dTheta = (i: number) => 112 * Math.sqrt(THETA[i]);

const hand = (text: string) => <span style={{fontFamily: F.hand, fontSize: 40}}>{text}</span>;
const ROWS = [
  {group: 0, tex: '\\log L(c)=\\tfrac12\\sum_{r,s}m_{rs}\\log\\dfrac{m_{rs}}{\\kappa_r\\,\\kappa_s}+\\text{const}'},
  {
    group: 0,
    tex: '\\phantom{\\log L(c)}=m\\,I(c)+\\text{const}',
    note: hand('m times the mutual information between the groups at the two ends of an edge'),
  },
  {
    group: 1,
    tex: 'I(c)=\\sum_{r,s}p(r,s)\\,\\log\\dfrac{p(r,s)}{p(r)\\,p(s)}',
    note: <Tex tex={'p(r,s)=\\dfrac{m_{rs}}{2m},\\qquad p(r)=\\dfrac{\\kappa_r}{2m}'} style={{fontSize: 44}} />,
  },
  {group: 2, tex: '\\hat c=\\arg\\max_{c}\\ \\log L(c)', note: hand('all that is left: maximize over c')},
] as const;

const TC = 100; // cell width of the small tables
const TH = 80; // cell height
const TY = 640;
const T1 = 170;
const T2 = 440;

/** A 2 x 2 table of numbers, rows and columns named by the two group colours. */
const Table: React.FC<{x: number; text: [[string, string], [string, string]]; op: number}> = ({x, text, op}) => (
  <g opacity={op}>
    {[0, 1].map((r) =>
      [0, 1].map((c) => (
        <g key={`${r}${c}`}>
          <rect x={x + c * TC} y={TY + r * TH} width={TC} height={TH} fill="#fff" stroke={C.faint} strokeWidth={3} />
          <text x={x + c * TC + TC / 2} y={TY + r * TH + TH * 0.64} textAnchor="middle" fontFamily={F.serif} fontSize={34} fill={C.ink}>
            {text[r][c]}
          </text>
        </g>
      )),
    )}
    {[0, 1].map((k) => (
      <g key={k}>
        <circle cx={x + k * TC + TC / 2} cy={TY - 22} r={13} fill={LOOK[k].fill} />
        <circle cx={x - 22} cy={TY + k * TH + TH / 2} r={13} fill={LOOK[k].fill} />
      </g>
    ))}
  </g>
);

const SEEN: [[string, string], [string, string]] = [
  [String(M2[0][0]), String(M2[0][1])],
  [String(M2[1][0]), String(M2[1][1])],
];
const EXPECTED: [[string, string], [string, string]] = [
  [FROM_DEGREES[0][0].toFixed(2), FROM_DEGREES[0][1].toFixed(2)],
  [FROM_DEGREES[1][0].toFixed(2), FROM_DEGREES[1][1].toFixed(2)],
];

export const S37: React.FC = () => {
  const frame = useCurrentFrame();

  const net = prog(frame, 4, 22);
  const t1 = prog(frame, 26, 44);
  const t2 = prog(frame, 40, 58);
  const tcap = prog(frame, marks[0] + 4, marks[0] + 22);

  return (
    <Frame n={37}>
      <Canvas>
        <g opacity={net}>
          {DC_EDGES.map((e, i) => (
            <line key={i} x1={POS[e[0]][0]} y1={POS[e[0]][1]} x2={POS[e[1]][0]} y2={POS[e[1]][1]} stroke={C.ink} strokeWidth={4} opacity={0.7} />
          ))}
          {POS.map((p, i) => {
            const lk = LOOK[DC_GROUP[i]];
            return (
              <g key={i}>
                <circle cx={p[0]} cy={p[1]} r={dTheta(i) / 2 - 1.5} fill={lk.fill} stroke="#fff" strokeWidth={3} />
                <text x={p[0]} y={p[1] + 10} textAnchor="middle" fontFamily={F.serif} fontSize={30} fontWeight={700} fill={lk.text}>
                  {LABELS[i]}
                </text>
              </g>
            );
          })}
        </g>
        <Table x={T1} text={SEEN} op={t1} />
        <Table x={T2} text={EXPECTED} op={t2} />
      </Canvas>
      <Fade o={t1} dy={10}>
        <Cap x={T1 + TC} y={540} w={260}>seen</Cap>
      </Fade>
      <Fade o={t2} dy={10}>
        <Cap x={T2 + TC} y={540} w={260}>expected</Cap>
      </Fade>
      <Fade o={t2} dy={10}>
        <Box x={120} y={812} w={600} size={34} color={C.soft}>
          expected: <Tex tex="\kappa_r\kappa_s/2m" />, the edges the degrees alone would give
        </Box>
      </Fade>
      <Fade o={tcap} dy={12}>
        <Cap x={120} y={905} w={760} align="left">more edges inside the groups than expected</Cap>
      </Fade>

      <FormulaStack rows={ROWS} marks={marks} x={780} y={200} w={1020} big={46} small={38} gap={20} />
    </Frame>
  );
};
