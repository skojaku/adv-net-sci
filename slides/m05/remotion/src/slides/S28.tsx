import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {BlockTable} from '../components/BlockTable';
import {Network, mix} from '../lib/network';
import {LOOK, type Look} from '../lib/look';
import {sbmEdges} from '../lib/sbm';
import {arcs8 as circle8} from '../lib/sbmLayout';
import {blockCounts, logLik} from '../lib/loglik';
import {prog, smooth} from '../lib/anim';
import {C, F} from '../theme';

/**
 * 0: the observed network, a guess (odd and even nodes) fills the discs, the table counts edges / pairs of nodes.
 * 1: the score of that guess is a dot on a number line.
 * 2: three more guesses, three more dots.
 * 3: the true grouping has the highest score.
 */
export const marks = [54, 104, 188, 242];

const EDGES = sbmEdges(0.9, 0.1);

type Guess = {name: string; c: number[]; score: number};
const GUESSES: Guess[] = [
  {name: 'odd and even nodes', c: [0, 1, 0, 1, 0, 1, 0, 1], score: -17.5},
  {name: 'one node moved', c: [0, 0, 0, 1, 1, 1, 1, 1], score: -15.5},
  {name: 'more nodes moved', c: [0, 0, 0, 1, 1, 1, 0, 0], score: -18.4},
  {name: 'all in one group', c: [0, 0, 0, 0, 0, 0, 0, 0], score: -19.1},
  {name: 'the true groups', c: [0, 0, 0, 0, 1, 1, 1, 1], score: -6.4},
];

// the scores on the slide are the ones in DECK_SPEC.md; the code must agree with them
const SCORE = GUESSES.map((g) => logLik(EDGES, g.c));
GUESSES.forEach((g, i) => {
  if (Math.abs(SCORE[i] - g.score) > 0.06) throw new Error(`S28: score of "${g.name}" is ${SCORE[i]}, expected ${g.score}`);
});
const COUNTS = GUESSES.map((g) => blockCounts(EDGES, g.c));

const fmt = (x: number) => x.toFixed(1).replace('-', '−');

// layout
const POS = circle8(540, 440, 150);
const TABLE = {x: 990, y: 345, cell: 170};
const NL = {x0: 240, x1: 1620, y: 930, lo: -20, hi: -5};
const nx = (s: number) => NL.x0 + ((s - NL.lo) / (NL.hi - NL.lo)) * (NL.x1 - NL.x0);

// when each guess takes over (the network refills over 10 frames; the true grouping takes 12)
const SWITCH = [0, 104, 132, 160, 188];
const SWITCH_LEN = [0, 10, 10, 10, 12];
// when each dot drops (14 frames), and where its value is written
const DROP = [76, 114, 142, 170, 202];
const VALUE_ABOVE = [true, true, false, true, true];

// how the discs look: group 0 blue, group 1 orange; before the first guess a node has no group (plain grey)
const GREY: Look = {fill: C.faint, stroke: '#fff', sw: 3, text: C.ink};
const looksOf = (c: number[]): Look[] => c.map((g) => LOOK[g]);
const GREYS: Look[] = Array.from({length: 8}, () => GREY);
const GUESS_LOOKS = GUESSES.map((g) => looksOf(g.c));

/** A table for one group only: the same look as BlockTable, one cell. */
const OneCell: React.FC<{x: number; y: number; cell: number; k: number; pairs: number; opacity: number}> = ({x, y, cell, k, pairs, opacity}) => {
  const chip = cell * 0.34;
  const p = k / pairs;
  const sw = LOOK[0].sw;
  return (
    <g opacity={opacity}>
      <circle cx={x + cell} cy={y - chip * 0.9} r={chip / 2 - sw / 2} fill={C.blue} stroke={C.blue} strokeWidth={sw} />
      <circle cx={x - chip * 0.9} cy={y + cell} r={chip / 2 - sw / 2} fill={C.blue} stroke={C.blue} strokeWidth={sw} />
      <rect x={x} y={y} width={cell * 2} height={cell * 2} fill={mix('#ffffff', C.blue, 0.5 * p)} stroke={C.soft} strokeWidth={3} />
      <text x={x + cell} y={y + cell + 15} textAnchor="middle" fontFamily={F.serif} fontSize={40} fill={C.ink}>
        {k} / {pairs}
      </text>
    </g>
  );
};

export const S28: React.FC = () => {
  const frame = useCurrentFrame();

  // g runs from 0 (first guess) to 4 (true groups); before frame 104 the discs go from grey to the first guess
  const grey = 1 - prog(frame, 28, 42);
  const g = SWITCH.slice(1).reduce((s, t, j) => s + smooth(frame, t, t + SWITCH_LEN[j + 1]), 0);
  const lo = Math.min(3, Math.floor(g));
  const f = g - lo;
  const fromGrey = frame < SWITCH[1];
  const look = fromGrey ? GREYS : GUESS_LOOKS[lo];
  const lookTo = fromGrey ? GUESS_LOOKS[0] : GUESS_LOOKS[lo + 1];
  const t = fromGrey ? 1 - grey : f;
  // the table of guess j: out first, then in, so two never overlap
  const own = (j: number) => Math.max(0, Math.min(1, 1 - 2 * Math.abs(g - j)));
  const tab = prog(frame, 36, 52);
  const nodes = (i: number) => prog(frame, i * 1.2, i * 1.2 + 12);
  const edges = prog(frame, 6, 24);

  // one line of text at a time under the figure: the task, then the definition of the score
  const task = prog(frame, 40, 54) * (1 - prog(frame, 54, 62));
  const defn = prog(frame, 60, 74);
  const axis = prog(frame, 58, 72);
  const cap3 = prog(frame, 222, 240);

  return (
    <Frame n={28} title="Finding the groups is inference">
      <Canvas>
        <Network
          pos={POS}
          edges={EDGES}
          edgeOp={() => edges}
          look={look}
          lookTo={lookTo}
          t={t}
          nodeD={60}
          edgeW={4.5}
          nodeOp={nodes}
          label={POS.map((_, i) => String(i + 1))}
          labelSize={34}
        />
        {/* the table of the current guess */}
        {GUESSES.map((gs, j) => {
          const cells = COUNTS[j];
          const op = own(j) * tab;
          if (cells.length === 1) return <OneCell key={j} x={TABLE.x} y={TABLE.y} cell={TABLE.cell} k={cells[0].k} pairs={cells[0].pairs} opacity={op} />;
          const [a, b, c] = cells;
          return (
            <BlockTable
              key={j}
              x={TABLE.x}
              y={TABLE.y}
              cell={TABLE.cell}
              p={[
                [a.k / a.pairs, b.k / b.pairs],
                [b.k / b.pairs, c.k / c.pairs],
              ]}
              text={[
                [`${a.k} / ${a.pairs}`, `${b.k} / ${b.pairs}`],
                [`${b.k} / ${b.pairs}`, `${c.k} / ${c.pairs}`],
              ]}
              opacity={op}
              fontSize={40}
            />
          );
        })}
        {/* the number line, with an arrow toward higher scores */}
        <g opacity={axis}>
          <line x1={NL.x0} y1={NL.y} x2={NL.x1 + 120} y2={NL.y} stroke={C.soft} strokeWidth={4} strokeLinecap="round" />
          <path d={`M${NL.x1 + 108} ${NL.y - 14} L${NL.x1 + 134} ${NL.y} L${NL.x1 + 108} ${NL.y + 14}`} fill="none" stroke={C.soft} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" />
          {[-20, -15, -10, -5].map((s) => (
            <g key={s}>
              <line x1={nx(s)} y1={NL.y} x2={nx(s)} y2={NL.y + 12} stroke={C.soft} strokeWidth={3} />
              <text x={nx(s)} y={NL.y + 54} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>
                {fmt(s).replace('.0', '')}
              </text>
            </g>
          ))}
          <text x={NL.x1 + 70} y={NL.y - 24} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>
            higher
          </text>
        </g>
        {GUESSES.map((gs, j) => {
          const d = prog(frame, DROP[j], DROP[j] + 14);
          const lab = prog(frame, DROP[j] + 4, DROP[j] + 18);
          const best = j === 4;
          const x = nx(gs.score);
          return (
            <g key={j}>
              <circle cx={x} cy={NL.y - (1 - d) * 46} r={16} fill={best ? C.ink : C.blue} stroke="#fff" strokeWidth={3} opacity={d} />
              <text
                x={x}
                y={VALUE_ABOVE[j] ? NL.y - 34 : NL.y + 62}
                textAnchor="middle"
                fontFamily={F.serif}
                fontSize={36}
                fontWeight={best ? 700 : 400}
                fill={best ? C.red : C.ink}
                opacity={lab}
              >
                {fmt(gs.score)}
              </text>
            </g>
          );
        })}
      </Canvas>
      <Fade o={task} dy={14}>
        <Cap y={742}>Guess the groups. Count edges / pairs of nodes.</Cap>
      </Fade>
      <Fade o={defn} dy={14}>
        <Box x={960} y={742} w={1680} align="center" size={45} style={{whiteSpace: 'nowrap'}}>
          <Term>score</Term>: log of the probability of this network
        </Box>
      </Fade>
      <Fade o={cap3} dy={14}>
        <Cap x={1410} y={360} w={390} align="left">
          We choose the
          <br />
          highest score.
        </Cap>
      </Fade>
    </Frame>
  );
};
