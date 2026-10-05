import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {BlockTable} from '../components/BlockTable';
import {Network} from '../lib/network';
import {C} from '../theme';
import {HOLLOW} from '../lib/look';
import {betweenStages, prog, stageStart} from '../lib/anim';
import {SBM_GROUP, SBM_LOOK, sbmEdges} from '../lib/sbm';
import {arcs8} from '../lib/sbmLayout';
import {blocksOf} from '../lib/sbmscore';

/**
 * Maximum likelihood, step 1: for a fixed grouping c, what is p?
 * The formulas of the last slide stay, small, in the panel at the top (nothing is deleted).
 * 0: given the network, find the c and p that make it most likely: maximize the likelihood.
 * 1: fix c: the network is coloured by c, the edges m and pairs of nodes n of every block are known.
 * 2: the derivative of log L with respect to p_rs, set to 0.
 * 3: the answer p_rs = m_rs / n_rs, in the table.
 */
export const marks = [48, 108, 168, 228];

const EDGES = sbmEdges(0.9, 0.1);
const COLOURED = SBM_GROUP.map((g) => SBM_LOOK[g]);
const PLAIN = SBM_GROUP.map(() => HOLLOW);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const POS = arcs8(400, 520, 150);

// the blocks of the grouping, computed
const {m: M, n: NN} = blocksOf(SBM_GROUP);
const fmt2 = (x: number) => x.toFixed(2);
const P = (r: number, s: number) => M[Math.min(r, s)][Math.max(r, s)] / NN[Math.min(r, s)][Math.max(r, s)];
if (M[0][0] !== 5 || NN[0][0] !== 6 || M[1][1] !== 6 || NN[1][1] !== 6 || M[0][1] !== 1 || NN[0][1] !== 16) throw new Error('S30: unexpected blocks');

const counts: [[string, string], [string, string]] = [
  [`${M[0][0]} / ${NN[0][0]}`, `${M[0][1]} / ${NN[0][1]}`],
  [`${M[0][1]} / ${NN[0][1]}`, `${M[1][1]} / ${NN[1][1]}`],
];
const probs: [[string, string], [string, string]] = [
  [fmt2(P(0, 0)), fmt2(P(0, 1))],
  [fmt2(P(1, 0)), fmt2(P(1, 1))],
];
const pMat: [[number, number], [number, number]] = [
  [P(0, 0), P(0, 1)],
  [P(1, 0), P(1, 1)],
];

// the recap of the last slide, small, and the new formulas
const RECAP1 = 'L(c,p)=\\prod_{r\\le s}p_{rs}^{\\,m_{rs}}\\,\\big(1-p_{rs}\\big)^{n_{rs}-m_{rs}}';
const RECAP2 = '\\log L(c,p)=\\sum_{r\\le s}\\Big[m_{rs}\\log p_{rs}+\\big(n_{rs}-m_{rs}\\big)\\log\\big(1-p_{rs}\\big)\\Big]';
const FX = 800;
const ITEMS = [
  {y: 360, h: 70, tex: '(\\hat c,\\hat p)=\\arg\\max_{c,\\,p}\\ \\log L(c,p)'},
  {y: 455, h: 70, tex: '\\text{fix } c:\\qquad \\hat p=\\arg\\max_{p}\\ \\log L(c,p)'},
  {y: 560, h: 120, tex: '\\dfrac{\\partial \\log L}{\\partial p_{rs}}=\\dfrac{m_{rs}}{p_{rs}}-\\dfrac{n_{rs}-m_{rs}}{1-p_{rs}}=0'},
  {y: 725, h: 100, tex: '\\hat p_{rs}=\\dfrac{m_{rs}}{n_{rs}}'},
] as const;

const TX = 230;
const TY = 760;
const CELL = 90;

export const S30: React.FC = () => {
  const frame = useCurrentFrame();

  const recap = prog(frame, 0, 18);
  const net = prog(frame, 6, 26);
  const colour = prog(frame, marks[0] + 6, marks[0] + 30);
  const item = (k: number) => prog(frame, stageStart(marks, k) + 4, stageStart(marks, k) + 22);
  const bar = (k: number) => betweenStages(frame, marks, k, k);
  const tableIn = prog(frame, marks[0] + 24, marks[0] + 42);
  const swap = prog(frame, marks[2] + 6, marks[2] + 24);

  return (
    <Frame n={30}>
      {/* what we have so far, docked at the top */}
      <Fade o={recap} dy={10}>
        <div style={{position: 'absolute', left: 120, top: 186, width: 1680, background: C.panel, padding: '8px 24px', fontSize: 32, lineHeight: 1.25}}>
          <div><Tex tex={RECAP1} /></div>
          <div><Tex tex={RECAP2} /></div>
        </div>
      </Fade>

      <Canvas>
        <Network pos={POS} edges={EDGES} look={PLAIN} lookTo={COLOURED} t={colour} nodeD={54} edgeW={4} label={LABELS} labelSize={30} opacity={net} />
        <g opacity={tableIn}>
          <g opacity={1 - swap}>
            <BlockTable x={TX} y={TY} cell={CELL} fontSize={30} p={pMat} text={counts} />
          </g>
          <g opacity={swap}>
            <BlockTable x={TX} y={TY} cell={CELL} fontSize={34} p={pMat} text={probs} />
          </g>
        </g>
      </Canvas>

      {ITEMS.map((it, k) => (
        <React.Fragment key={k}>
          <Fade o={item(k)} dy={14}>
            <Box x={FX} y={it.y} w={1000} size={40}>
              <Tex tex={it.tex} />
            </Box>
          </Fade>
          <Fade o={bar(k) * item(k)}>
            <div style={{position: 'absolute', left: FX - 22, top: it.y + 4, width: 7, height: it.h, background: C.blue}} />
          </Fade>
        </React.Fragment>
      ))}
    </Frame>
  );
};
