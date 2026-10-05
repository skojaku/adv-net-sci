import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {FormulaStack} from '../components/FormulaStack';
import {C} from '../theme';
import {LOOK} from '../lib/look';
import {fromStage} from '../lib/anim';

/**
 * The degree-corrected SBM (Karrer and Newman 2011): every node gets a number theta_i.
 * 0: the SBM: the groups alone decide the probability of an edge.
 * 1: the degree-corrected SBM: the number of edges between i and j is Poisson with mean theta_i theta_j omega_{c_i c_j};
 *    theta_i: how many edges node i tends to make.
 * 2: three pairs of nodes of one group (the area of a disc is theta): two nodes with large theta share more edges than two
 *    with small theta. No numbers on the slide.
 */
export const marks = [56, 112, 172];

const sym = (tex: string, text: string) => (
  <div>
    <Tex tex={tex} style={{fontSize: 40}} />
    <span>: {text}</span>
  </div>
);
const ROWS = [
  {group: 0, label: 'SBM', tex: 'P(A_{ij}=1\\mid c,p)=p_{c_ic_j}'},
  {
    group: 1,
    label: 'degree-corrected SBM',
    tex: 'A_{ij}\\sim\\mathrm{Poisson}\\big(\\theta_i\\,\\theta_j\\,\\omega_{c_ic_j}\\big)',
    note: (
      <>
        {sym('A_{ij}', 'the number of edges between i and j')}
        {sym('\\theta_i', 'how many edges node i tends to make')}
        {sym('\\omega_{rs}', 'how many edges groups r and s tend to share')}
      </>
    ),
  },
] as const;

// three pairs of nodes of one group: the area of a disc is theta
const PAIRS = [
  {x: 480, a: 2, b: 2},
  {x: 960, a: 2, b: 0.5},
  {x: 1440, a: 0.5, b: 0.5},
] as const;
const D1 = 64; // diameter of a disc with theta = 1
const PY = 810;

export const S35: React.FC = () => {
  const frame = useCurrentFrame();

  const pairs = fromStage(frame, marks, 2, 16);

  return (
    <Frame n={35}>
      <FormulaStack rows={ROWS} marks={marks} x={120} y={200} w={1680} big={52} small={42} gap={26} labelW={330} />

      {/* stage 2 */}
      <Canvas>
        <g opacity={pairs}>
          {PAIRS.map((p, k) => {
            const da = D1 * Math.sqrt(p.a);
            const db = D1 * Math.sqrt(p.b);
            const gap = 26;
            const total = da + gap + db;
            const xa = p.x - total / 2 + da / 2;
            const xb = p.x + total / 2 - db / 2;
            return (
              <g key={k}>
                <circle cx={xa} cy={PY} r={da / 2} fill={LOOK[0].fill} stroke="#fff" strokeWidth={3} />
                <circle cx={xb} cy={PY} r={db / 2} fill={LOOK[0].fill} stroke="#fff" strokeWidth={3} />
              </g>
            );
          })}
        </g>
      </Canvas>
      <Fade o={pairs} dy={12}>
        <Box x={960} y={665} w={1500} align="center" size={38} color={C.soft}>
          the area of a disc is <Tex tex="\theta" />: two nodes with a large <Tex tex="\theta" /> share more edges
        </Box>
      </Fade>
    </Frame>
  );
};
