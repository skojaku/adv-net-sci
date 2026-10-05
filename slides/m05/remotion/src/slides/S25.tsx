import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {BlockTable} from '../components/BlockTable';
import {Network} from '../lib/network';
import {SBM_GROUP, SBM_LOOK} from '../lib/sbm';
import {arcs8 as circle8} from '../lib/sbmLayout';
import {prog, smooth} from '../lib/anim';
import {C} from '../theme';

/**
 * 0: the two groups of S18 to S26 with no edges; the table swaps to 0.1 inside and 0.9 between; the question.
 * The question has no answer on the slide: no edges are drawn.
 */
export const marks = [66];

const POS = circle8(500, 520, 230);
const LOOKS = SBM_GROUP.map((g) => SBM_LOOK[g]);
const LABEL = POS.map((_, i) => String(i + 1));

export const S25: React.FC = () => {
  const frame = useCurrentFrame();

  const tab = prog(frame, 14, 30);
  // the table of S18 (0.9 inside, 0.1 between) turns into its opposite
  const flip = smooth(frame, 32, 50);
  const pIn = 0.9 - 0.8 * flip;
  const pOut = 0.1 + 0.8 * flip;
  const ask = prog(frame, 50, 66);

  return (
    <Frame n={25} title="What if edges between groups are more likely?">
      <Canvas>
        <Network
          pos={POS}
          edges={[]}
          look={LOOKS}
          nodeD={66}
          nodeOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)}
          label={LABEL}
          labelSize={38}
        />
        <BlockTable
          x={1160}
          y={310}
          cell={190}
          p={[
            [pIn, pOut],
            [pOut, pIn],
          ]}
          opacity={tab}
          fontSize={48}
        />
      </Canvas>
      <Fade o={ask} dy={16}>
        <Box x={960} y={858} w={1500} align="center" size={45} color={C.ink}>
          What does the network look like?
        </Box>
      </Fade>
    </Frame>
  );
};
