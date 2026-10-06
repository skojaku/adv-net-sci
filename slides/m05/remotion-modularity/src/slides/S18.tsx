import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {C} from '../theme';
import {caption, fromStage, prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {LOOK} from '../lib/look';
import {Network, type Pt} from '../lib/network';
import {CLUB_L, q3} from '../lib/club';
import {FINAL, MERGE_PAIR, Q_FINAL, Q_STUCK} from '../data/data';
import {EDGES, FINAL_LOOKS, groupEdgeLook, groupEdgeOp, STUCK_LOOKS} from '../lib/c_trace';
import {CENTRES, discD, DIRS, GROUPS, LOOP_COUNT, MERGED, PAIRS, SIZES, SuperNet, type SDisc, type SLine, type SLoop} from '../lib/c_super';

/**
 * Opens on the network of groups that S18 ends with.
 * 0: the same picture; the local moves run again, now on the 5 supernodes.
 * 1: the second level (L1_MOVES): one supernode joins another; Q = 0.420.
 * 2: the supernodes open up again: the 34 nodes in the 4 final groups.
 */
export const marks = [28, 100, 164];

const [G1, G2] = MERGE_PAIR;
const REST = [0, 1, 2, 3, 4].filter((g) => g !== G1 && g !== G2);
const LOOKS = [0, 1, 2, 3, 4].map((g) => STUCK_LOOKS[GROUPS[g][0]]);

export const S18: React.FC = () => {
  const frame = useCurrentFrame();
  const t = smooth(frame, 40, 82);
  const ringO = prog(frame, 28, 38) * (1 - prog(frame, 44, 56));
  const hot = prog(frame, 72, 88);
  const open = prog(frame, 100, 122); // the supernodes open up into the nodes
  const superO = 1 - open;

  const at = (g: number): Pt => (g === G1 || g === G2 ? ([lerp(CENTRES[g][0], MERGED.c[0], t), lerp(CENTRES[g][1], MERGED.c[1], t)] as const) : CENTRES[g]);
  const fadeOld = 1 - prog(t, 0, 0.6);
  const old = (g: number) => g === G1 || g === G2;

  const discs: SDisc[] = [
    ...REST.map((g) => ({c: CENTRES[g], size: SIZES[g], look: LOOKS[g], op: superO})),
    ...[G1, G2].map((g) => ({c: at(g), size: SIZES[g], look: LOOKS[g], op: superO * (1 - prog(t, 0.55, 1))})),
    {c: MERGED.c, size: MERGED.size, look: LOOK[1], op: superO * prog(t, 0.45, 1)},
  ];
  const lines: SLine[] = [
    ...PAIRS.map((e) => ({a: at(e.a), b: at(e.b), count: e.count, op: superO * (old(e.a) || old(e.b) ? fadeOld : 1)})),
    ...MERGED.to.map((e) => ({a: CENTRES[e.g], b: MERGED.c, count: e.count, op: superO * prog(t, 0.5, 1)})),
  ];
  const loops: SLoop[] = [
    ...REST.map((g) => ({c: CENTRES[g], size: SIZES[g], dir: DIRS[g], count: LOOP_COUNT[g], op: superO})),
    ...[G1, G2].map((g) => ({c: at(g), size: SIZES[g], dir: DIRS[g], count: LOOP_COUNT[g], op: superO * fadeOld})),
    {c: MERGED.c, size: MERGED.size, dir: MERGED.dir, count: MERGED.loop, op: superO * prog(t, 0.5, 1)},
  ];
  const r1 = discD(SIZES[G1]) / 2 + 10;
  const opN = groupEdgeOp(FINAL, FINAL_LOOKS);

  return (
    <Frame n={18}>
      <Canvas>
        <SuperNet discs={discs} lines={lines} loops={loops} />
        <circle cx={CENTRES[G1][0]} cy={CENTRES[G1][1]} r={r1} fill="none" stroke={C.ink} strokeWidth={7} opacity={ringO} />
        <Network
          pos={CLUB_L}
          edges={EDGES}
          look={FINAL_LOOKS}
          nodeD={46}
          nodeOp={(i) => prog(frame, 100 + 0.35 * i, 112 + 0.35 * i)}
          edgeOp={(i, e) => open * opN(i, e)}
          edgeLook={groupEdgeLook(FINAL, FINAL_LOOKS)}
        />
      </Canvas>
      <Fade o={1 - hot}>
        <Tag x={1385} y={290} style={{fontSize: 64}}>
          Q = {q3(Q_STUCK)}
        </Tag>
      </Fade>
      <Fade o={hot}>
        <Tag x={1385} y={290} hot style={{fontSize: 64}}>
          Q = {q3(Q_FINAL)}
        </Tag>
      </Fade>
      <Fade o={caption(frame, marks, 0)} dy={14}>
        <Box x={1010} y={450} w={770}>
          Run the same local moves, now on the supernodes.
        </Box>
      </Fade>
      <Fade o={caption(frame, marks, 1)} dy={14}>
        <Box x={1010} y={450} w={770}>
          Two groups merge into one node.
        </Box>
      </Fade>
      <Fade o={fromStage(frame, marks, 2, 16)} dy={14}>
        <Cap x={1385} y={450} w={700}>
          4 groups
        </Cap>
      </Fade>
    </Frame>
  );
};
