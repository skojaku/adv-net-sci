import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {caption, fromStage, prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {Network, type Pt} from '../lib/network';
import {CLUB_L, q3} from '../lib/club';
import {Q_STUCK, STUCK} from '../data/data';
import {EDGES, groupEdgeLook, groupEdgeOp, NODES, STUCK_LOOKS} from '../lib/c_trace';
import {Band, CENTRES, DIRS, GROUPS, LOOP_COUNT, PAIRS, SIZES, SuperNet, tint} from '../lib/c_super';

/**
 * Opens on the stuck partition of S17 (same coordinates).
 * 0: a soft band around each of the 5 groups.
 * 1: each group collapses into one disc (its size = the number of nodes); the edges inside a group become a loop, the edges between two groups one thick line (each with its number).
 * 2: the network of groups has the same Q.
 */
export const marks = [30, 112, 156];

export const S17: React.FC = () => {
  const frame = useCurrentFrame();
  const bands = prog(frame, 0, 16);
  const c = smooth(frame, 32, 72);
  const pos: Pt[] = CLUB_L.map((p, v) => [lerp(p[0], CENTRES[STUCK[v]][0], c), lerp(p[1], CENTRES[STUCK[v]][1], c)] as const);
  const discOp = prog(c, 0.55, 1);
  const parts = prog(frame, 66, 90);
  const edgeFade = 1 - Math.min(1, c * 2.2);
  const looks = STUCK_LOOKS;
  const opE = groupEdgeOp(STUCK, looks);

  const hot = fromStage(frame, marks, 2, 14);

  return (
    <Frame n={17}>
      <Canvas>
        <defs>
          <clipPath id="s18-clip">
            <rect x={112} y={0} width={1808} height={1080} />
          </clipPath>
        </defs>
        <g clipPath="url(#s18-clip)">
          {GROUPS.map((g, i) => (
            <Band key={i} pts={g.map((v) => pos[v])} pad={34} color={tint(looks[g[0]])} opacity={bands * (1 - prog(c, 0.6, 1))} />
          ))}
        </g>
        <Network
          pos={pos}
          edges={EDGES}
          look={looks}
          nodeD={46}
          nodeOp={() => 1 - prog(c, 0.45, 0.9)}
          edgeOp={(i, e) => edgeFade * opE(i, e)}
          edgeLook={groupEdgeLook(STUCK, looks)}
        />
        <SuperNet
          discs={CENTRES.map((p, g) => ({c: p, size: SIZES[g], look: looks[GROUPS[g][0]], op: discOp}))}
          lines={PAIRS.map((e) => ({a: CENTRES[e.a], b: CENTRES[e.b], count: e.count, op: parts}))}
          loops={CENTRES.map((p, g) => ({c: p, size: SIZES[g], dir: DIRS[g], count: LOOP_COUNT[g], op: parts}))}
        />
      </Canvas>
      <Fade o={1 - hot}>
        <Tag x={1385} y={290} style={{fontSize: 64}}>
          Q = {q3(Q_STUCK)}
        </Tag>
      </Fade>
      <Fade o={hot}>
        <Tag x={1385} y={290} hot style={{fontSize: 64}}>
          Q = {q3(Q_STUCK)}
        </Tag>
      </Fade>
      <Fade o={caption(frame, marks, 1)} dy={14}>
        <Box x={1010} y={450} w={770}>
          Each disc counts nodes. Each loop and line counts edges.
        </Box>
      </Fade>
      <Fade o={caption(frame, marks, 2)} dy={14}>
        <Box x={1010} y={450} w={770}>
          The network of groups has the same Q.
        </Box>
      </Fade>
    </Frame>
  );
};
