import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {Tex} from '../components/Tex';
import {C} from '../theme';
import {caption, fromStage, prog} from '../lib/anim';
import {HOLLOW, LOOK} from '../lib/look';
import {TOY_STUB_NODE} from '../data/data';
import {ToyDisc} from '../lib/a_toy';

/**
 * The 14 stubs of the small example in a row, grouped by node. Node 3 is i, node 4 is j.
 * 0: the row of stubs, the nodes, the labels i and j.
 * 1: one stub of i is joined to one of the other 13 stubs: 13 arcs, all equally likely.
 * 2: k_j of those 13 stubs belong to j.
 */
export const marks = [60, 130, 200];

const I = 2; // node i (the third node of the drawing, numbered 3)
const J = 3; // node j (numbered 4)
const SLOT = 92;
const GAP = 70;
const ROW_Y = 470;
const STUB_D = 46;
const NODE_Y = 590;
const NODE_D = 72;

// x of every stub, and the middle of every group
const stubX: number[] = [];
const groupX: number[] = [];
{
  let x = 960 - (TOY_STUB_NODE.length * SLOT + 5 * GAP) / 2;
  let last = -1;
  TOY_STUB_NODE.forEach((n, s) => {
    if (n !== last && last >= 0) x += GAP;
    stubX[s] = x + SLOT / 2;
    x += SLOT;
    last = n;
  });
  for (let n = 0; n < 6; n++) {
    const xs = stubX.filter((_, s) => TOY_STUB_NODE[s] === n);
    groupX[n] = (xs[0] + xs[xs.length - 1]) / 2;
  }
}

const CHOSEN = TOY_STUB_NODE.indexOf(I); // the first stub of i
const OTHERS = TOY_STUB_NODE.map((_, s) => s).filter((s) => s !== CHOSEN);
const arc = (s: number): string => {
  const x1 = stubX[CHOSEN];
  const x2 = stubX[s];
  const y = ROW_Y - STUB_D / 2 - 4;
  const c = Math.min(400, 0.45 * Math.abs(x2 - x1) + 70);
  return `M ${x1} ${y} Q ${(x1 + x2) / 2} ${y - c} ${x2} ${y}`;
};

const stubFill = (n: number) => (n === I ? LOOK[0].fill : n === J ? LOOK[1].fill : '#fff');
const stubStroke = (n: number) => (n === I ? LOOK[0].fill : n === J ? LOOK[1].fill : C.soft);

export const S06: React.FC = () => {
  const frame = useCurrentFrame();

  const row = (s: number) => prog(frame, 2 * s, 2 * s + 14);
  const nodes = prog(frame, 24, 44);
  const tags = prog(frame, 36, 54);
  const label = prog(frame, 40, 58) * caption(frame, marks, 0);
  const arcIn = (r: number) => prog(frame, marks[0] + 6 + 3 * r, marks[0] + 6 + 3 * r + 18);
  const focus = prog(frame, marks[1] + 4, marks[1] + 28); // the arcs to j stay, the others fade
  const s1 = caption(frame, marks, 1);
  const s2 = fromStage(frame, marks, 2, 16);

  return (
    <Frame n={6}>
      <Canvas>
        {/* a stub belongs to its node */}
        {TOY_STUB_NODE.map((n, s) => (
          <line key={`l${s}`} x1={stubX[s]} y1={ROW_Y + STUB_D / 2} x2={groupX[n]} y2={NODE_Y - NODE_D / 2 + 2} stroke={C.faint} strokeWidth={3} opacity={nodes} />
        ))}
        {/* the arcs from one stub of i */}
        {OTHERS.map((s, r) => {
          const toJ = TOY_STUB_NODE[s] === J;
          const o = arcIn(r) * (toJ ? 1 : 1 - 0.8 * focus);
          return (
            <path key={`a${s}`} d={arc(s)} fill="none" stroke={toJ && focus > 0.5 ? LOOK[1].fill : C.ink} strokeWidth={toJ ? 3.5 + 3 * focus : 3} opacity={o * (toJ ? 1 : 0.45)} />
          );
        })}
        {TOY_STUB_NODE.map((n, s) => (
          <g key={`s${s}`} opacity={row(s)}>
            <circle cx={stubX[s]} cy={ROW_Y} r={STUB_D / 2} fill={stubFill(n)} stroke={stubStroke(n)} strokeWidth={4} />
          </g>
        ))}
        {/* the stub that picks a partner */}
        <circle cx={stubX[CHOSEN]} cy={ROW_Y} r={STUB_D / 2 + 8} fill="none" stroke={C.ink} strokeWidth={5} opacity={arcIn(0)} />
        <g opacity={nodes}>
          {[0, 1, 2, 3, 4, 5].map((n) => (
            <ToyDisc key={n} p={[groupX[n], NODE_Y]} d={NODE_D} look={n === I ? LOOK[0] : n === J ? LOOK[1] : HOLLOW} label={n + 1} size={34} />
          ))}
        </g>
      </Canvas>
      <div style={{opacity: tags}}>
        <Box x={groupX[I]} y={NODE_Y + 44} w={120} align="center" size={56}><Tex tex="i" /></Box>
        <Box x={groupX[J]} y={NODE_Y + 44} w={120} align="center" size={56}><Tex tex="j" /></Box>
      </div>
      <div style={{opacity: label}}>
        <Cap x={960} y={NODE_Y + 130} w={700}>2M = 14 stubs</Cap>
      </div>
      <div style={{opacity: s1}}>
        <Box x={960} y={760} w={1500} align="center" size={46}>A stub of i joins one of the other 2M − 1 stubs. Each one is equally likely.</Box>
      </div>
      <div style={{opacity: s2}}>
        <Box x={960} y={730} w={1500} align="center" size={46}>
          <Tex tex="k_j" /> of the other stubs belong to <Tex tex="j" />.
        </Box>
        <Box x={960} y={805} w={1500} align="center" size={56}>
          <Tex tex="\dfrac{k_j}{2M-1}\approx\dfrac{k_j}{2M}" />
        </Box>
      </div>
    </Frame>
  );
};
