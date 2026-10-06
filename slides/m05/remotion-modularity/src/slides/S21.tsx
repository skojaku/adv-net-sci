import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {C} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {LOOK, type Look} from '../lib/look';
import {q3} from '../lib/club';
import {BR_Q, BR_S0, BR_S1} from '../data/data';
import {BridgeScene} from '../lib/c_bridge';

/**
 * A constructed example (BR_*), not a run of Louvain: each Q is computed, and Leiden's paper shows that Louvain can reach such a state.
 * 0: the bridge node (6) sits in the blue group; the other group is orange. Q = 0.222.
 * 1: the bridge moves to the orange group: Q goes up to 0.357.
 * 2: the blue group is in two pieces with no edge between them.
 * 3: Louvain moves a node only to a neighbouring group; what the Leiden paper found.
 */
export const marks = [58, 120, 184, 236];

const BLUE = LOOK[0];
const ORANGE = LOOK[1];
const LOOKS0: Look[] = BR_S0.map((g) => (g === 0 ? BLUE : ORANGE));
const LOOKS1: Look[] = BR_S1.map((g) => (g === 0 ? BLUE : ORANGE));

export const S21: React.FC = () => {
  const frame = useCurrentFrame();
  const t = prog(frame, 68, 90);
  const lookTo = LOOKS0.map((l, i) => (i === 6 ? ORANGE : l));
  const lab = t > 0.5 ? BR_S1 : BR_S0;
  const looksNow = t > 0.5 ? LOOKS1 : LOOKS0;

  const hot = prog(frame, 82, 98);
  const dim = prog(frame, 124, 146);
  const rings = prog(frame, 124, 146);
  const gap = prog(frame, 142, 160);

  return (
    <Frame n={21} zoom={1.08} top={200}>
      <Canvas>
        <BridgeScene
          lab={lab}
          looks={LOOKS0}
          lookTo={lookTo}
          t={t}
          edgeLab={lab}
          edgeLooks={looksNow}
          nodeAppear={(i) => prog(frame, 0.8 * i, 0.8 * i + 12)}
          edgeAppear={(i) => prog(frame, 8 + 0.8 * i, 8 + 0.8 * i + 12)}
          dim={dim}
          bridgeRing={prog(frame, 60, 70) * (1 - prog(frame, 98, 110))}
          bridgeLabel={prog(frame, 30, 44) * (1 - prog(frame, 124, 138))}
          rings={{o: rings, left: C.blue, right: C.blue}}
          gap={gap}
        />
      </Canvas>
      <Fade o={prog(frame, 30, 46) * (1 - hot)}>
        <Tag x={960} y={215} style={{fontSize: 56}}>
          Q = {q3(BR_Q[0])}
        </Tag>
      </Fade>
      <Fade o={hot}>
        <Tag x={960} y={215} hot style={{fontSize: 56}}>
          Q = {q3(BR_Q[1])}
        </Tag>
      </Fade>
      <Fade o={betweenStages(frame, marks, 2, 2)} dy={14}>
        <Box x={960} y={715} w={1680} align="center">
          The blue group is now in two pieces with no edge between them.
        </Box>
      </Fade>
      <Fade o={fromStage(frame, marks, 3, 16)} dy={14}>
        <Box x={960} y={715} w={1680} align="center" size={42}>
          Louvain moves a node only to a neighbouring group.
          <br />
          It cannot split them.
        </Box>
        <Box x={960} y={850} w={1680} align="center" size={42}>
          Up to 25% of the communities are badly connected
          <br />
          and up to 16% are disconnected.
        </Box>
        <Cap x={1460} y={222} w={560}>
          Traag, Waltman, van Eck, 2019
        </Cap>
      </Fade>
    </Frame>
  );
};
