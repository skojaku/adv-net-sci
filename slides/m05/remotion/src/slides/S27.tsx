import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {BlockTable} from '../components/BlockTable';
import {Network} from '../lib/network';
import {SBM_GROUP, SBM_LOOK, SBM_PAIRS, sbmEdges, sbmInside} from '../lib/sbm';
import {arcs8 as circle8} from '../lib/sbmLayout';
import {SBM_U} from '../data/data';
import {prog, smooth} from '../lib/anim';
import {clamp} from '../lib/plot';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';

/**
 * 0: probabilities 0.9 inside, 0.1 between, and the network they give. Q of the true groups.
 * 1: a dial turns inside to 0.1 and between to 0.9; edges fade out and in.
 * 2: both go to 0.45: a random network.
 * 3: the three states side by side, with the one model behind them.
 */
export const marks = [56, 124, 188, 244];

// the three states: probability for two nodes in the same group, in different groups, and Q of the true groups (checked below)
const STATES = [
  {pIn: 0.9, pOut: 0.1, q: 0.413},
  {pIn: 0.1, pOut: 0.9, q: -0.436},
  {pIn: 0.45, pOut: 0.45, q: 0.0},
] as const;

/** Modularity of the blue / red split of the sampled edges: sum over groups of e_c / m - (K_c / 2m)^2. */
const modularity = (edges: ReadonlyArray<readonly [number, number]>): number => {
  const m = edges.length;
  const e = [0, 0];
  const K = [0, 0];
  for (const [a, b] of edges) {
    K[SBM_GROUP[a]] += 1;
    K[SBM_GROUP[b]] += 1;
    if (SBM_GROUP[a] === SBM_GROUP[b]) e[SBM_GROUP[a]] += 1;
  }
  return [0, 1].reduce((s, c) => s + e[c] / m - (K[c] / (2 * m)) ** 2, 0);
};

const Q = STATES.map((s) => modularity(sbmEdges(s.pIn, s.pOut)));
STATES.forEach((s, i) => {
  if (Math.abs(Q[i] - s.q) > 5e-4) throw new Error(`S27: Q of state ${i} is ${Q[i]}, expected ${s.q}`);
});

const qText = (q: number) => (Math.abs(q) < 5e-4 ? '0.000' : q.toFixed(3).replace('-', '−'));

// the fade of one edge while the dial turns from state `a` to state `b`; s is the dial position, 0 to 1.
// An edge whose pair has u between the two probabilities flips near the dial position where p = u. The flip is kept
// inside [0.1, 0.9] of the turn, so the state before the turn and the state after it are exactly sbmEdges().
const HALF = 0.1;
const edgeFade = (k: number, pa: number, pb: number, s: number): number => {
  const u = SBM_U[k];
  const onA = u < pa;
  const onB = u < pb;
  if (onA === onB) return onA ? 1 : 0;
  const star = clamp((u - pa) / (pb - pa), HALF, 1 - HALF);
  const t = clamp(0.5 + (s - star) / (2 * HALF), 0, 1);
  return onB ? t : 1 - t;
};

const MAIN = {cx: 540, cy: 520, r: 220, d: 64};
const MAIN_POS = circle8(MAIN.cx, MAIN.cy, MAIN.r);
const LOOKS = SBM_GROUP.map((g) => SBM_LOOK[g]);

// the dial: one line and one handle for each probability
const TX0 = 1220;
const TX1 = 1620;
const Slider: React.FC<{y: number; p: number}> = ({y, p}) => (
  <g>
    <line x1={TX0} y1={y} x2={TX1} y2={y} stroke={C.soft} strokeWidth={4} strokeLinecap="round" />
    <text x={TX0 - 26} y={y + 13} textAnchor="end" fontFamily={F.serif} fontSize={36} fill={C.soft}>0</text>
    <text x={TX1 + 26} y={y + 13} textAnchor="start" fontFamily={F.serif} fontSize={36} fill={C.soft}>1</text>
    <circle cx={TX0 + p * (TX1 - TX0)} cy={y} r={20} fill={C.ink} stroke="#fff" strokeWidth={4} />
  </g>
);

// one panel of stage 3
const Panel: React.FC<{cx: number; pIn: number; pOut: number; opacity: number}> = ({cx, pIn, pOut, opacity}) => (
  <g opacity={opacity}>
    <Network pos={circle8(cx, 335, 112)} edges={sbmEdges(pIn, pOut)} look={LOOKS} nodeD={46} edgeW={4} />
    <BlockTable
      x={cx - 116}
      y={545}
      cell={116}
      p={[
        [pIn, pOut],
        [pOut, pIn],
      ]}
      fontSize={40}
    />
  </g>
);

export const S27: React.FC = () => {
  const frame = useCurrentFrame();

  // stages 0 to 2: one network and one table, driven by the dial
  const main = 1 - prog(frame, 188, 196);
  const tab = prog(frame, 6, 22);
  const built = prog(frame, 16, 34);
  const dialOp = prog(frame, 58, 70);
  const s1 = smooth(frame, 72, 112);
  const s2 = smooth(frame, 130, 170);
  const pIn = STATES[0].pIn + (STATES[1].pIn - STATES[0].pIn) * s1 + (STATES[2].pIn - STATES[1].pIn) * s2;
  const pOut = STATES[0].pOut + (STATES[1].pOut - STATES[0].pOut) * s1 + (STATES[2].pOut - STATES[1].pOut) * s2;
  const edgeOp = (k: number) => {
    const inside = sbmInside(SBM_PAIRS[k][0], SBM_PAIRS[k][1]);
    const P = (i: number) => (inside ? STATES[i].pIn : STATES[i].pOut);
    return built * (frame <= marks[1] ? edgeFade(k, P(0), P(1), s1) : edgeFade(k, P(1), P(2), s2));
  };

  // the captions of stages 0 to 2 take turns at one place: out at the start of the next stage, in at the end of their own
  const cap0 = prog(frame, 36, 52) * (1 - prog(frame, 56, 66));
  const cap1 = prog(frame, 112, 124) * (1 - prog(frame, 124, 134));
  const cap2 = prog(frame, 176, 188) * (1 - prog(frame, 188, 196));
  const cap3 = prog(frame, 224, 244);

  return (
    <Frame n={27}>
      <Canvas>
        <g opacity={main}>
          <Network
            pos={MAIN_POS}
            edges={SBM_PAIRS}
            edgeOp={(k) => edgeOp(k)}
            look={LOOKS}
            nodeD={MAIN.d}
            edgeW={5}
            nodeOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)}
            label={MAIN_POS.map((_, i) => String(i + 1))}
            labelSize={38}
          />
          <BlockTable
            x={1130}
            y={275}
            cell={170}
            p={[
              [pIn, pOut],
              [pOut, pIn],
            ]}
            opacity={tab}
            fontSize={44}
          />
          <g opacity={dialOp}>
            <Slider y={722} p={pIn} />
            <Slider y={827} p={pOut} />
          </g>
        </g>
        <Panel cx={400} pIn={STATES[0].pIn} pOut={STATES[0].pOut} opacity={prog(frame, 192, 206)} />
        <Panel cx={960} pIn={STATES[1].pIn} pOut={STATES[1].pOut} opacity={prog(frame, 199, 213)} />
        <Panel cx={1520} pIn={STATES[2].pIn} pOut={STATES[2].pOut} opacity={prog(frame, 206, 220)} />
      </Canvas>
      <Fade o={dialOp * main}>
        <Box x={TX0} y={652} w={640} size={40} color={C.soft}>inside a group</Box>
        <Box x={TX0} y={757} w={640} size={40} color={C.soft}>between groups</Box>
      </Fade>
      <Fade o={cap0} dy={14}>
        <Cap y={890}>Q of the true groups: {qText(Q[0])}</Cap>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Cap y={890}>Q of the true groups: {qText(Q[1])}</Cap>
      </Fade>
      <Fade o={cap2} dy={14}>
        <Cap y={890}>A random network. Q of the true groups: {qText(Q[2])}</Cap>
      </Fade>
      <Fade o={cap3} dy={14}>
        <Cap y={830}>One model: a table of probabilities.</Cap>
      </Fade>
    </Frame>
  );
};
