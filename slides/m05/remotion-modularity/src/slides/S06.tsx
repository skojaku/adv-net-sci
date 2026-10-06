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
 * The 12 stubs of the small example in a row, grouped by node. Node 1 (the hub, 3 stubs) is i, node 5 (2 stubs) is j.
 * 0: the row of stubs, the nodes, the labels i and j. Every stub is equally likely to join any other stub.
 * 1: the stubs of i (k_i) and of j (k_j) are marked: the expected number of edges between i and j is proportional to k_i and to k_j (never called a probability).
 * (Lecturer: the derivation is one straight line, so there are no arcs and no 2M - 1.)
 */
export const marks = [60, 130];

const I = 0; // node i (the hub, numbered 1 in the drawing)
const J = 4; // node j (numbered 5)
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

const stubFill = (n: number) => (n === I ? LOOK[0].fill : n === J ? LOOK[1].fill : '#fff');
const stubStroke = (n: number) => (n === I ? LOOK[0].fill : n === J ? LOOK[1].fill : C.soft);

export const S06: React.FC = () => {
  const frame = useCurrentFrame();

  const row = (s: number) => prog(frame, 2 * s, 2 * s + 14);
  const nodes = prog(frame, 24, 44);
  const tags = prog(frame, 36, 54);
  const label = prog(frame, 40, 58) * caption(frame, marks, 0);
  const s0 = caption(frame, marks, 0);
  const s1 = fromStage(frame, marks, 1, 16);
  const brace = prog(frame, marks[0] + 4, marks[0] + 26);

  return (
    <Frame n={6}>
      <Canvas>
        {/* a stub belongs to its node */}
        {TOY_STUB_NODE.map((n, s) => (
          <line key={`l${s}`} x1={stubX[s]} y1={ROW_Y + STUB_D / 2} x2={groupX[n]} y2={NODE_Y - NODE_D / 2 + 2} stroke={C.faint} strokeWidth={3} opacity={nodes} />
        ))}
        {TOY_STUB_NODE.map((n, s) => (
          <g key={`s${s}`} opacity={row(s)}>
            <circle cx={stubX[s]} cy={ROW_Y} r={STUB_D / 2} fill={stubFill(n)} stroke={stubStroke(n)} strokeWidth={4} />
          </g>
        ))}
        {/* a bracket over the stubs of i and over the stubs of j */}
        {[I, J].map((n) => {
          const xs = stubX.filter((_, k) => TOY_STUB_NODE[k] === n);
          const x1 = xs[0] - STUB_D / 2;
          const x2 = xs[xs.length - 1] + STUB_D / 2;
          const y = ROW_Y - STUB_D / 2 - 14;
          return <path key={`b${n}`} d={`M ${x1} ${y + 12} V ${y} H ${x2} V ${y + 12}`} fill="none" stroke={n === I ? LOOK[0].fill : LOOK[1].fill} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" opacity={brace} />;
        })}
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
        <Cap x={960} y={NODE_Y + 130} w={700}>2M = {TOY_STUB_NODE.length} stubs</Cap>
      </div>
      <div style={{opacity: brace}}>
        <Box x={groupX[I]} y={ROW_Y - 128} w={160} align="center" size={52} color={LOOK[0].fill}><Tex tex="k_i" /></Box>
        <Box x={groupX[J]} y={ROW_Y - 128} w={160} align="center" size={52} color={LOOK[1].fill}><Tex tex="k_j" /></Box>
      </div>
      <div style={{opacity: s0}}>
        <Box x={960} y={810} w={1500} align="center" size={46}>Every stub is equally likely to join any other stub.</Box>
      </div>
      <div style={{opacity: s1}}>
        <Box x={960} y={790} w={1640} align="center" size={44}>So the expected edges between i and j are proportional to their stubs.</Box>
        <Box x={960} y={870} w={1500} align="center" size={58}>
          <Tex tex="\text{expected edges}\ \propto\ k_i\,k_j" />
        </Box>
      </div>
    </Frame>
  );
};
