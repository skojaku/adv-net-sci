import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {betweenStages, prog, stageStart} from '../lib/anim';

/**
 * The likelihood of a network, built up one formula at a time (the lecturer explains each one).
 * p_rs is NOT given: the formulas use p_rs and 1 - p_rs in general form.
 * 0: the definitions, and L(c, p) = P(A | c, p).
 * 1: one pair of nodes: an edge with probability p, no edge with probability 1 - p.
 * 2: the same in one expression.
 * 3: the product over all pairs of nodes: the likelihood.
 * 4: the pairs grouped by block (r, s): m_rs edges and n_rs pairs of nodes.
 * 5: the log-likelihood.
 * No formula is removed: they all stay on the slide to the end.
 */
export const marks = [44, 96, 148, 204, 268, 328];

const FX = 640; // left edge of the formulas
const FS = 36;
const ITEMS = [
  {y: 205, h: 70, tex: 'L(c,p)=P(A\\mid c,p)'},
  {y: 295, h: 130, tex: 'P(A_{ij}\\mid c,p)=\\begin{cases}p_{c_ic_j} & A_{ij}=1\\\\[2pt] 1-p_{c_ic_j} & A_{ij}=0\\end{cases}'},
  {y: 440, h: 80, tex: '=\\;p_{c_ic_j}^{\\,A_{ij}}\\,\\big(1-p_{c_ic_j}\\big)^{1-A_{ij}}'},
  {y: 540, h: 100, tex: 'L(c,p)=\\prod_{i<j}p_{c_ic_j}^{\\,A_{ij}}\\,\\big(1-p_{c_ic_j}\\big)^{1-A_{ij}}'},
  {y: 660, h: 100, tex: 'L(c,p)=\\prod_{r\\le s}p_{rs}^{\\,m_{rs}}\\,\\big(1-p_{rs}\\big)^{n_{rs}-m_{rs}}'},
  {y: 790, h: 120, tex: '\\log L(c,p)=\\sum_{r\\le s}\\Big[m_{rs}\\log p_{rs}+\\big(n_{rs}-m_{rs}\\big)\\log\\big(1-p_{rs}\\big)\\Big]'},
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
  const bar = (k: number) => betweenStages(frame, marks, k, k);
  const def = (from: number) => prog(frame, stageStart(marks, from) + (from === 0 ? 14 : 4), stageStart(marks, from) + (from === 0 ? 32 : 22));

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
      {/* the formulas, each added under the last */}
      {ITEMS.map((it, k) => (
        <React.Fragment key={k}>
          <Fade o={item(k)} dy={14}>
            <Box x={FX} y={it.y} w={1160} size={FS}>
              <Tex tex={it.tex} />
            </Box>
          </Fade>
          {/* a blue bar marks the formula that was just added */}
          <Fade o={bar(k) * item(k)}>
            <div style={{position: 'absolute', left: FX - 22, top: it.y + 4, width: 7, height: it.h, background: C.blue}} />
          </Fade>
        </React.Fragment>
      ))}
    </Frame>
  );
};
