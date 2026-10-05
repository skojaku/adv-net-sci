import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {prog, stageStart} from '../lib/anim';
import {lerp} from '../lib/plot';

/**
 * The likelihood of a network, built up one formula at a time (the lecturer explains each one).
 * p_rs is NOT given: the formulas use p_rs and 1 - p_rs in general form.
 * 0: the definitions, and L(c, p) = P(A | c, p).
 * 1: one pair of nodes: an edge with probability p, no edge with probability 1 - p.
 * 2: the same in one expression, its = under the = of the line above.
 * 3: the product over all pairs of nodes: the likelihood.
 * 4: the pairs grouped by block (r, s): m_rs edges and n_rs pairs of nodes.
 * 5: the log-likelihood (on two lines, to be large enough).
 * No formula is removed: they all stay on the slide to the end. The newest formula is large, the older ones a little smaller
 * (no marker). Lines 1 and 2 are one step and change size together, so that their = signs stay one under the other.
 */
export const marks = [44, 96, 148, 204, 268, 328];

const FX = 640; // left edge of the formulas
const TOP0 = 196;
const NEW = 50; // size of the newest formula
const OLD = 40; // size of the older ones
const GAP = 20;

const LHS = 'P(A_{ij}\\mid c,p)';
const ROWS = [
  {group: 0, tex: 'L(c,p)=P(A\\mid c,p)'},
  {group: 1, tex: `${LHS}=\\begin{cases}p_{c_ic_j} & A_{ij}=1\\\\[2pt] 1-p_{c_ic_j} & A_{ij}=0\\end{cases}`},
  {group: 1, tex: `\\phantom{${LHS}}=p_{c_ic_j}^{\\,A_{ij}}\\,\\big(1-p_{c_ic_j}\\big)^{1-A_{ij}}`},
  {group: 2, tex: 'L(c,p)=\\prod_{i<j}p_{c_ic_j}^{\\,A_{ij}}\\,\\big(1-p_{c_ic_j}\\big)^{1-A_{ij}}'},
  {group: 3, tex: 'L(c,p)=\\prod_{r\\le s}p_{rs}^{\\,m_{rs}}\\,\\big(1-p_{rs}\\big)^{n_{rs}-m_{rs}}'},
  {
    group: 4,
    tex: '\\begin{aligned}\\textstyle\\log L(c,p)&\\textstyle=\\sum_{r\\le s}\\Big[m_{rs}\\log p_{rs}\\\\&\\textstyle\\qquad+\\big(n_{rs}-m_{rs}\\big)\\log\\big(1-p_{rs}\\big)\\Big]\\end{aligned}',
  },
] as const;

const DEFS = [
  {y: 215, from: 0, sym: 'A_{ij}', text: '1 if nodes i and j are connected, 0 if not'},
  {y: 345, from: 0, sym: 'c_i', text: 'the group of node i'},
  {y: 445, from: 0, sym: 'p_{rs}', text: 'the probability of an edge between groups r and s'},
  {y: 620, from: 4, sym: 'm_{rs}', text: 'the number of edges between groups r and s'},
  {y: 750, from: 4, sym: 'n_{rs}', text: 'the number of pairs of nodes between groups r and s'},
] as const;

export const S29: React.FC = () => {
  const frame = useCurrentFrame();

  const item = (k: number) => prog(frame, stageStart(marks, k) + (k === 0 ? 6 : 4), stageStart(marks, k) + (k === 0 ? 24 : 22));
  const def = (from: number) => prog(frame, stageStart(marks, from) + (from === 0 ? 14 : 4), stageStart(marks, from) + (from === 0 ? 32 : 22));
  // a step is large from the moment its first line appears until the first line of the next step appears
  const first = (g: number) => ROWS.findIndex((r) => r.group === g);
  const big = (g: number) => {
    const next = first(g + 1);
    return next < 0 ? 1 : 1 - prog(frame, stageStart(marks, next) + 4, stageStart(marks, next) + 22);
  };

  return (
    <Frame n={29}>
      {/* the symbols, in a column of their own */}
      {DEFS.map((d) => (
        <Fade key={d.sym} o={def(d.from)} dy={12}>
          <Box x={120} y={d.y} w={470} size={34}>
            <Tex tex={d.sym} style={{fontSize: 40}} />
            <span style={{color: C.soft}}>: {d.text}</span>
          </Box>
        </Fade>
      ))}
      {/* the formulas, each added under the last; the lines below move as the ones above change size */}
      <div style={{position: 'absolute', left: FX, top: TOP0, width: 1180, fontFamily: F.serif, color: C.ink, lineHeight: 1.3}}>
        {ROWS.map((r, k) => (
          <div key={k} style={{opacity: item(k), marginBottom: GAP, fontSize: lerp(OLD, NEW, big(r.group)), transform: `translateY(${(1 - item(k)) * 14}px)`}}>
            <Tex tex={r.tex} />
          </div>
        ))}
      </div>
    </Frame>
  );
};
