import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {C} from '../theme';
import {caption, fromStage, prog, smooth} from '../lib/anim';
import {HOLLOW, LOOK} from '../lib/look';
import {mix} from '../lib/network';
import {TOY_EDGES, TOY_LAB, TOY_REWIRED, TOY_STUB_NODE, TOY_STUB_PAIRS} from '../data/data';
import {DegLabels, STUB_OTHER, STUB_EDGE, ToyDisc, lerp, lerpPos, toyPos} from '../lib/a_toy';

/**
 * The small example, cut and reconnected.
 * 0: the network, a degree label for every node.
 * 1: every edge is cut in the middle: 14 stubs.
 * 2: the stubs are joined again at random (TOY_STUB_PAIRS); every node keeps its degree.
 * 3: the original and the reconnected network side by side, with the groups coloured: 6 of 7 edges inside, then 2 of 7.
 */
export const marks = [64, 124, 226, 312];

const BIG = toyPos(360, 215, 1200, 700);
const LEFT = toyPos(130, 300, 770, 460);
const RIGHT = toyPos(1020, 300, 770, 460);
const D_BIG = 84;
const D_SMALL = 70;
const STUB_FRAC = 0.34; // how far a stub reaches along its old edge
const INK_W = 5;
const LINE = C.gray5; // plain edge colour (a little lighter than black, drawn opaque so that the two halves of an edge do not show a seam)

const groupLook = (i: number) => LOOK[TOY_LAB[i]];

export const S05: React.FC = () => {
  const frame = useCurrentFrame();

  const nodeIn = (i: number) => prog(frame, 3 * i, 3 * i + 14);
  const edgeIn = (k: number) => prog(frame, 20 + 3 * k, 20 + 3 * k + 12);
  const degIn = prog(frame, 40, 56);
  const cut = prog(frame, marks[0] + 4, marks[0] + 40);
  const pairE = (k: number) => smooth(frame, marks[1] + 4 + 7 * k, marks[1] + 4 + 7 * k + 38);
  const move = smooth(frame, marks[2] + 4, marks[2] + 50);
  const colour = prog(frame, marks[2] + 20, marks[2] + 56);

  const pos = lerpPos(BIG, RIGHT, move);
  const d = lerp(D_BIG, D_SMALL, move);

  // the pair of each stub (its partner), and the edge that the pair becomes
  const pairOf: number[] = [];
  TOY_STUB_PAIRS.forEach(([a, b], k) => {
    pairOf[a] = k;
    pairOf[b] = k;
  });

  const cap0 = caption(frame, marks, 0);
  const cap1 = caption(frame, marks, 1);
  const cap2 = caption(frame, marks, 2);
  const outsideCaps = fromStage(frame, marks, 3, 18);

  // a stub: a line from its node to its tip
  const stubs = TOY_STUB_NODE.map((n, s) => {
    const p = pos[n];
    const q = pos[STUB_OTHER[s]];
    const f = 0.5 - (0.5 - STUB_FRAC) * cut;
    const tip0: [number, number] = [p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f];
    const k = pairOf[s];
    const [a, b] = TOY_STUB_PAIRS[k];
    const mid: [number, number] = [(pos[TOY_STUB_NODE[a]][0] + pos[TOY_STUB_NODE[b]][0]) / 2, (pos[TOY_STUB_NODE[a]][1] + pos[TOY_STUB_NODE[b]][1]) / 2];
    const e = pairE(k);
    const tip: [number, number] = [lerp(tip0[0], mid[0], e), lerp(tip0[1], mid[1], e)];
    // colour: plain until the groups appear
    const [u, v] = TOY_REWIRED[k];
    const inside = TOY_LAB[u] === TOY_LAB[v];
    const target = inside ? LOOK[TOY_LAB[u]].fill : C.faint;
    const stroke = e < 1 ? LINE : mix(LINE, target, colour);
    const w = e < 1 ? INK_W : INK_W + (inside ? 2 : -1.5) * colour;
    const o = edgeIn(STUB_EDGE[s]) * (e < 1 ? 1 : 1 - 0.35 * colour * (inside ? 0 : 1));
    return {p, tip, stroke, w, o, dot: cut * (1 - e)};
  });

  // the original network (left panel, stage 3)
  const orig = TOY_EDGES.map((e) => {
    const inside = TOY_LAB[e[0]] === TOY_LAB[e[1]];
    return {a: LEFT[e[0]], b: LEFT[e[1]], stroke: inside ? LOOK[TOY_LAB[e[0]]].fill : C.faint, w: inside ? 7 : 3.5};
  });

  return (
    <Frame n={5} zoom={1.08} top={200}>
      <Canvas>
        {/* the original network, only in stage 3 */}
        <g opacity={move}>
          {orig.map((e, k) => (
            <line key={k} x1={e.a[0]} y1={e.a[1]} x2={e.b[0]} y2={e.b[1]} stroke={e.stroke} strokeWidth={e.w} strokeLinecap="round" opacity={0.8} />
          ))}
          {LEFT.map((p, i) => (
            <ToyDisc key={i} p={p} d={D_SMALL} look={groupLook(i)} label={i + 1} size={34} />
          ))}
        </g>
        {/* the stubs: before the cut they meet in the middle and look like the edges */}
        {stubs.map((s, k) => (
          <g key={k} opacity={s.o}>
            <line x1={s.p[0]} y1={s.p[1]} x2={s.tip[0]} y2={s.tip[1]} stroke={s.stroke} strokeWidth={s.w} strokeLinecap="round" />
            <circle cx={s.tip[0]} cy={s.tip[1]} r={8} fill={LINE} opacity={s.dot} />
          </g>
        ))}
        {pos.map((p, i) => (
          <g key={i} opacity={nodeIn(i)}>
            <ToyDisc p={p} d={d} look={HOLLOW} label={i + 1} size={d * 0.48} />
            <ToyDisc p={p} d={d} look={groupLook(i)} label={i + 1} size={d * 0.48} o={colour} />
          </g>
        ))}
      </Canvas>
      <DegLabels pos={pos} d={d} size={d * 0.52} o={degIn} />
      <DegLabels pos={LEFT} d={D_SMALL} size={D_SMALL * 0.52} o={move} />
      <div style={{opacity: cap0}}>
        <Cap x={960} y={880}>7 edges, 14 edge ends</Cap>
      </div>
      <div style={{opacity: cap1}}>
        <Cap x={960} y={880}>14 stubs</Cap>
      </div>
      <div style={{opacity: cap2 * (1 - move)}}>
        <Box x={960} y={870} w={1500} align="center" size={46}>Every node keeps its degree. The number of edges stays 7.</Box>
      </div>
      <div style={{opacity: outsideCaps}}>
        <Cap x={515} y={236} w={600}>original</Cap>
        <Cap x={1405} y={236} w={600}>rewired</Cap>
        <Cap x={515} y={780} w={700}>6 of 7 edges inside</Cap>
        <Cap x={1405} y={780} w={700}>2 of 7 edges inside</Cap>
        <Cap x={960} y={868} w={1700}>Like a power strip: each device keeps its sockets, only the wiring is shuffled.</Cap>
      </div>
    </Frame>
  );
};
