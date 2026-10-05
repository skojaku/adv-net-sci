import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {BlockTable} from '../components/BlockTable';
import {Network} from '../lib/network';
import {C} from '../theme';
import {prog, stageStart} from '../lib/anim';
import {SBM_GROUP, SBM_LOOK, sbmEdges} from '../lib/sbm';
import {arcs8} from '../lib/sbmLayout';
import {blocksOf} from '../lib/sbmscore';

/**
 * Maximum likelihood, step 2: with p_rs = m_rs / n_rs put back, only c is left.
 * The formulas so far stay, small, in the panel at the top (nothing is deleted).
 * 0: put p back into log L(c, p): a formula in c alone.
 * 1: the number for this c: log L = -2.70 - 3.74 + 0 = -6.44.
 * 2: all that is left is to maximize over c.
 */
export const marks = [56, 116, 172];

const EDGES = sbmEdges(0.9, 0.1);
const LOOKS = SBM_GROUP.map((g) => SBM_LOOK[g]);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const POS = arcs8(400, 520, 150);

const {m: M, n: NN} = blocksOf(SBM_GROUP);
const fmt2 = (x: number) => x.toFixed(2).replace('-', '\u2212');
const term = (r: number, s: number) => {
  const m = M[r][s];
  const n = NN[r][s];
  return m === 0 || m === n ? 0 : m * Math.log(m / n) + (n - m) * Math.log(1 - m / n);
};
const T = [term(0, 0), term(0, 1), term(1, 1)];
const TOTAL = T[0] + T[1] + T[2];
if (fmt2(TOTAL) !== '\u22126.44') throw new Error(`S31: log L is ${TOTAL}`);
const P = (r: number, s: number) => M[Math.min(r, s)][Math.max(r, s)] / NN[Math.min(r, s)][Math.max(r, s)];
const pMat: [[number, number], [number, number]] = [
  [P(0, 0), P(0, 1)],
  [P(1, 0), P(1, 1)],
];
const terms: [[string, string], [string, string]] = [
  [fmt2(T[0]), fmt2(T[1])],
  ['', T[2] === 0 ? '0' : fmt2(T[2])],
];

const RECAP1 = '\\log L(c,p)=\\sum_{r\\le s}\\Big[m_{rs}\\log p_{rs}+\\big(n_{rs}-m_{rs}\\big)\\log\\big(1-p_{rs}\\big)\\Big]';
const RECAP2 = '\\hat p_{rs}=\\dfrac{m_{rs}}{n_{rs}}';
const FX = 800;
const ITEMS = [
  {y: 350, h: 230, tex: '\\begin{aligned}\\log L(c)&=\\sum_{r\\le s}\\Big[m_{rs}\\log\\dfrac{m_{rs}}{n_{rs}}\\\\&\\qquad+\\big(n_{rs}-m_{rs}\\big)\\log\\Big(1-\\dfrac{m_{rs}}{n_{rs}}\\Big)\\Big]\\end{aligned}'},
  {y: 665, h: 70, tex: `\\log L=${fmt2(T[0]).replace('\u2212', '-')}\\ ${fmt2(T[1]).replace('\u2212', '-')}\\ +\\,0\\ =\\ ${fmt2(TOTAL).replace('\u2212', '-')}`.replace('\\ -', '\\ -\\,')},
  {y: 770, h: 70, tex: '\\hat c=\\arg\\max_{c}\\ \\log L(c)'},
] as const;

const TX = 230;
const TY = 760;
const CELL = 90;

export const S31: React.FC = () => {
  const frame = useCurrentFrame();

  const recap = prog(frame, 0, 18);
  const net = prog(frame, 4, 22);
  const item = (k: number) => prog(frame, stageStart(marks, k) + 4, stageStart(marks, k) + 24);
  const tableIn = prog(frame, marks[0] + 6, marks[0] + 24);
  const only = prog(frame, marks[0] + 8, marks[0] + 24) * (1 - prog(frame, marks[1], marks[1] + 10));
  const last = prog(frame, marks[1] + 8, marks[1] + 26);

  return (
    <Frame n={31}>
      <Fade o={recap} dy={10}>
        <div style={{position: 'absolute', left: 120, top: 186, width: 1680, background: C.panel, padding: '8px 24px', fontSize: 32, lineHeight: 1.25}}>
          <div><Tex tex={RECAP1} /></div>
          <div><Tex tex={RECAP2} /></div>
        </div>
      </Fade>

      <Canvas>
        <Network pos={POS} edges={EDGES} look={LOOKS} nodeD={54} edgeW={4} label={LABELS} labelSize={30} opacity={net} />
        <g opacity={tableIn}>
          <BlockTable x={TX} y={TY} cell={CELL} fontSize={34} p={pMat} text={terms} />
        </g>
      </Canvas>

      {ITEMS.map((it, k) => (
        <React.Fragment key={k}>
          <Fade o={item(k)} dy={14}>
            <Box x={FX} y={it.y} w={1000} size={40}>
              <Tex tex={it.tex} />
            </Box>
          </Fade>
        </React.Fragment>
      ))}
      <Fade o={only} dy={12}>
        <Cap x={FX} y={590} w={900} align="left">a formula in c alone</Cap>
      </Fade>
      <Fade o={last} dy={12}>
        <Cap x={FX} y={860} w={900} align="left">all that is left: maximize over c</Cap>
      </Fade>
    </Frame>
  );
};
