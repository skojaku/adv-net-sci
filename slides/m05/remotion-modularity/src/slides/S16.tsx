import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {C} from '../theme';
import {caption, prog} from '../lib/anim';
import {LOOK, type Look} from '../lib/look';
import {mix, Network} from '../lib/network';
import {CLUB_L, q3} from '../lib/club';
import {MERGE_PAIR, MOVE_NODE, Q_MERGED, Q_STUCK, STUCK} from '../data/data';
import {EDGES, groupEdgeLook, groupEdgeOp, NODES, STUCK_HUE, STUCK_LOOKS} from '../lib/c_trace';
import {Band} from '../lib/c_super';

/**
 * The state that label switching stops in: 5 groups, Q = 0.399.
 * 0: no single node can move to raise Q.
 * 1: one node of group 2 (MOVE_NODE) takes the label of group 1: Q goes down to 0.386.
 * 2: the node goes back; then one soft band around the whole groups 1 and 2 (they are not recoloured, so that S18 opens on this picture): Q would go up to 0.420.
 */
export const marks = [40, 100, 172];

const [NODE, TO] = [MOVE_NODE[0], MOVE_NODE[1]];
const MERGED_NODES = STUCK.map((g, v) => (MERGE_PAIR.includes(g) ? v : -1)).filter((v) => v >= 0);
const TARGET: Look = LOOK[STUCK_HUE[TO]]; // the hue of group 1 (orange)

export const S16: React.FC = () => {
  const frame = useCurrentFrame();

  // the colour of the node that moves: (stage 1) it goes over, (stage 2) it goes back
  const tA = prog(frame, 50, 70);
  const tB = prog(frame, 102, 120);
  const t = tA - tB;
  const moving = new Set([NODE]);
  const ringAll = prog(frame, 128, 150); // the band around the two groups that would be one
  const lookTo = STUCK_LOOKS.map((l, i) => (moving.has(i) ? TARGET : l));
  const looksNow = t > 0.5 ? lookTo : STUCK_LOOKS;
  const lab = STUCK.map((g, i) => (moving.has(i) && t > 0.5 ? TO : g));

  const ring = Array.from({length: NODES}, (_, i) =>
    i === NODE ? mix('#ffffff', C.ink, prog(frame, 42, 54) * (1 - prog(frame, 112, 124))) : null,
  );

  // the Q tag: 0.399, then 0.386, back to 0.399, then 0.420
  const b = prog(frame, 56, 68) - prog(frame, 112, 124);
  const c = prog(frame, 144, 158);
  const a = Math.max(0, 1 - b - c);

  return (
    <Frame n={16}>
      <Canvas>
        <Band pts={MERGED_NODES.map((v) => CLUB_L[v])} pad={24} color="#e4e4e8" opacity={ringAll} />
        <Network
          pos={CLUB_L}
          edges={EDGES}
          look={STUCK_LOOKS}
          lookTo={lookTo}
          t={t}
          nodeD={46}
          edgeOp={groupEdgeOp(lab, looksNow)}
          edgeLook={groupEdgeLook(lab, looksNow)}
          ring={ring}
          ringW={7}
        />
      </Canvas>
      <Fade o={a}>
        <Tag x={1385} y={290} style={{fontSize: 64}}>
          Q = {q3(Q_STUCK)}
        </Tag>
      </Fade>
      <Fade o={b}>
        <Tag x={1385} y={290} style={{fontSize: 64}}>
          Q = {q3(MOVE_NODE[2])}
        </Tag>
      </Fade>
      <Fade o={c}>
        <Tag x={1385} y={290} hot style={{fontSize: 64}}>
          Q = {q3(Q_MERGED)}
        </Tag>
      </Fade>
      <Fade o={caption(frame, marks, 0)} dy={14}>
        <Box x={1010} y={450} w={770}>
          No node can move to raise Q.
        </Box>
      </Fade>
      <Fade o={caption(frame, marks, 1)} dy={14}>
        <Box x={1010} y={450} w={770}>
          Moving one node lowers Q.
        </Box>
      </Fade>
      <Fade o={caption(frame, marks, 2)} dy={14}>
        <Box x={1000} y={450} w={800} size={42}>
          Merging two whole groups raises Q.
          <br />
          One node at a time cannot see it.
        </Box>
      </Fade>
    </Frame>
  );
};
