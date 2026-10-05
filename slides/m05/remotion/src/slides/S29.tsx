import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {BlockTable} from '../components/BlockTable';
import {Network} from '../lib/network';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {SBM_GROUP, SBM_LOOK, sbmEdges} from '../lib/sbm';
import {arcs8} from '../lib/sbmLayout';
import {blocksOf} from '../lib/sbmscore';

/**
 * The SBM estimate, step by step, on the 8-node network.
 * 0: a grouping c.  1: count the edges m and the pairs of nodes n in each block.  2: p = m / n.
 * 3: the probability of the network as a product over the blocks, every factor annotated.
 * 4: the log turns the product into a sum.  5: keep the grouping with the largest log L.
 */
export const marks = [50, 104, 158, 240, 316, 372];

const EDGES = sbmEdges(0.9, 0.1);
const LOOKS = SBM_GROUP.map((g) => SBM_LOOK[g]);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const POS = arcs8(480, 500, 205);

// the blocks of the true grouping, computed
const {m: M, n: NN} = blocksOf(SBM_GROUP);
const fmt2 = (x: number) => x.toFixed(2).replace('-', '−');
const sig2 = (x: number) => Number(x.toPrecision(2)).toString();
const P = (r: number, s: number) => M[Math.min(r, s)][Math.max(r, s)] / NN[Math.min(r, s)][Math.max(r, s)];
/** the probability of one block: p^m (1 - p)^(n - m), with p = m / n and 0^0 = 1 */
const factor = (r: number, s: number) => {
  const m = M[r][s];
  const n = NN[r][s];
  const p = m / n;
  return Math.pow(p, m) * Math.pow(1 - p, n - m);
};
const term = (r: number, s: number) => {
  const m = M[r][s];
  const n = NN[r][s];
  return m === 0 || m === n ? 0 : m * Math.log(m / n) + (n - m) * Math.log(1 - m / n);
};
const FACT = [factor(0, 0), factor(0, 1), factor(1, 1)];
const PROD = FACT[0] * FACT[1] * FACT[2];
const LOGS = [term(0, 0), term(0, 1), term(1, 1)];
const TOTAL_LL = LOGS[0] + LOGS[1] + LOGS[2];
if (M[0][0] !== 5 || NN[0][0] !== 6 || M[1][1] !== 6 || NN[1][1] !== 6 || M[0][1] !== 1 || NN[0][1] !== 16) throw new Error('S29: unexpected blocks');
if (fmt2(TOTAL_LL) !== '−6.44' || Math.abs(Math.log(PROD) - TOTAL_LL) > 1e-9) throw new Error(`S29: log L is ${TOTAL_LL}, product ${PROD}`);
if (sig2(FACT[0]) !== '0.067' || sig2(FACT[1]) !== '0.024' || sig2(FACT[2]) !== '1' || sig2(PROD) !== '0.0016') throw new Error('S29: unexpected factors');

const TX = 1000;
const TY = 410;
const CELL = 140;

// the product, factor by factor, then the sum of the logs
const PROD_TEX =
  'L(c)=\\underbrace{\\prod_{r\\le s}}_{\\text{each block}}\\ \\underbrace{p_{rs}^{\\,m_{rs}}}_{\\text{$m$ pairs with an edge}}\\ \\underbrace{(1-p_{rs})^{\\,n_{rs}-m_{rs}}}_{\\text{$n-m$ pairs with no edge}}';
const LOG_TEX =
  '\\log L(c)=\\underbrace{\\sum_{r\\le s}}_{\\text{each block}}\\Big[\\underbrace{m_{rs}\\log p_{rs}}_{\\text{edges}}+\\underbrace{(n_{rs}-m_{rs})\\log(1-p_{rs})}_{\\text{no edges}}\\Big]';
const PROD_NUM = `L = ${sig2(FACT[0])} \\times ${sig2(FACT[1])} \\times ${sig2(FACT[2])} = ${sig2(PROD)}`;
const SUM_NUM = `\\log L = ${fmt2(LOGS[0]).replace('−', '-')} ${fmt2(LOGS[1]).replace('−', '-')} + 0 = ${fmt2(TOTAL_LL).replace('−', '-')}`.replace('= -', '= -').replace(/ -(\d)/, ' -$1');

export const S29: React.FC = () => {
  const frame = useCurrentFrame();

  const net = prog(frame, 0, 20);
  const s0 = betweenStages(frame, marks, 0, 0) * prog(frame, 20, 36);
  const s1 = betweenStages(frame, marks, 1, 1);
  const s2 = betweenStages(frame, marks, 2, 2);
  const s3 = betweenStages(frame, marks, 3, 3);
  const s4 = betweenStages(frame, marks, 4, 4);
  const s5 = fromStage(frame, marks, 5, 14);
  const tableO = prog(frame, marks[0] + 4, marks[0] + 20);
  const cNum = betweenStages(frame, marks, 1, 1);
  const cP = betweenStages(frame, marks, 2, 2);
  const cF = betweenStages(frame, marks, 3, 3);
  const cT = fromStage(frame, marks, 4, 14);
  const prodO = betweenStages(frame, marks, 3, 3);
  const logO = fromStage(frame, marks, 4, 14);
  const prodNum = betweenStages(frame, marks, 3, 3) * prog(frame, marks[2] + 40, marks[2] + 58);
  const sumNum = fromStage(frame, marks, 4, 14);

  const counts: [[string, string], [string, string]] = [
    [`${M[0][0]} / ${NN[0][0]}`, `${M[0][1]} / ${NN[0][1]}`],
    [`${M[0][1]} / ${NN[0][1]}`, `${M[1][1]} / ${NN[1][1]}`],
  ];
  const probs: [[string, string], [string, string]] = [
    [fmt2(P(0, 0)), fmt2(P(0, 1))],
    [fmt2(P(1, 0)), fmt2(P(1, 1))],
  ];
  const factors: [[string, string], [string, string]] = [
    [sig2(FACT[0]), sig2(FACT[1])],
    ['', sig2(FACT[2])],
  ];
  const terms: [[string, string], [string, string]] = [
    [fmt2(LOGS[0]), fmt2(LOGS[1])],
    ['', LOGS[2] === 0 ? '0' : fmt2(LOGS[2])],
  ];
  const pMat: [[number, number], [number, number]] = [
    [P(0, 0), P(0, 1)],
    [P(1, 0), P(1, 1)],
  ];

  return (
    <Frame n={29} title="The SBM estimate, step by step">
      <Canvas>
        <Network pos={POS} edges={EDGES} look={LOOKS} nodeD={62} edgeW={5} label={LABELS} labelSize={34} opacity={net} />
        <g opacity={tableO}>
          <g opacity={cNum}>
            <BlockTable x={TX} y={TY} cell={CELL} fontSize={40} p={pMat} text={counts} />
          </g>
          <g opacity={cP}>
            <BlockTable x={TX} y={TY} cell={CELL} fontSize={44} p={pMat} text={probs} />
          </g>
          <g opacity={cF}>
            <BlockTable x={TX} y={TY} cell={CELL} fontSize={44} p={pMat} text={factors} />
          </g>
          <g opacity={cT}>
            <BlockTable x={TX} y={TY} cell={CELL} fontSize={44} p={pMat} text={terms} />
          </g>
        </g>
      </Canvas>

      {/* the step, on one line (two at the most) */}
      <Fade o={s0} dy={12}>
        <Box x={TX} y={200} w={800} size={44}>1 &nbsp;A grouping <Tex tex="c" /></Box>
      </Fade>
      <Fade o={s1} dy={12}>
        <Box x={TX} y={200} w={800} size={44}>2 &nbsp;Count edges <Tex tex="m" /> and pairs of nodes <Tex tex="n" /></Box>
      </Fade>
      <Fade o={s2} dy={12}>
        <Box x={TX} y={200} w={800} size={44}>3 &nbsp;<Tex tex="p_{rs} = m_{rs} / n_{rs}" /></Box>
      </Fade>
      <Fade o={s3} dy={12}>
        <Box x={TX} y={200} w={800} size={44}>4 &nbsp;The probability of the network</Box>
      </Fade>
      <Fade o={s4} dy={12}>
        <Box x={TX} y={200} w={800} size={44}>5 &nbsp;Take the log: the product becomes a sum</Box>
      </Fade>
      <Fade o={s5} dy={12}>
        <Box x={TX} y={200} w={800} size={44}>6 &nbsp;Keep the <Tex tex="c" /> with the largest <Tex tex="\log L" />: the most likely grouping</Box>
      </Fade>

      {/* the formula, every factor annotated */}
      <Fade o={prodO} dy={14}>
        <Box x={960} y={768} w={1680} align="center" size={42}>
          <Tex tex={PROD_TEX} />
        </Box>
      </Fade>
      <Fade o={logO} dy={14}>
        <Box x={960} y={768} w={1680} align="center" size={42}>
          <Tex tex={LOG_TEX} />
        </Box>
      </Fade>
      {/* the numbers of the example, under the table */}
      <Fade o={prodNum} dy={12}>
        <Box x={TX} y={694} w={800} size={38}>
          <Tex tex={PROD_NUM} />
        </Box>
      </Fade>
      <Fade o={sumNum} dy={12}>
        <Box x={TX} y={694} w={800} size={38}>
          <Tex tex={SUM_NUM} />
        </Box>
      </Fade>
      <Fade o={net * s0} dy={12}>
        <Cap x={480} y={770} w={700}>the group of each node</Cap>
      </Fade>
    </Frame>
  );
};
