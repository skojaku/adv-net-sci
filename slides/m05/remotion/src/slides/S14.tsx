import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {betweenStages, prog, smooth} from '../lib/anim';
import {CX, NodeTable, T2, T3} from '../lib/nodetable';

/**
 * The table of nodes (S13): can we simply count the nodes on the diagonal? Only if each found group is matched with a
 * true group, and the names and the order of the found groups are arbitrary.
 * 0: match A with blue and B with orange: the diagonal holds 4 + 3 = 7 of 8 nodes.
 * 1: the same split, the columns in another order: the diagonal holds 0 + 1 = 1 of 8.
 * 2: three found groups against two true groups: no diagonal at all.
 * 3: what we need: a score that ignores the names and the order.
 */
export const marks = [50, 112, 172, 226];

export const S14: React.FC = () => {
  const frame = useCurrentFrame();

  // the table is already there when the slide opens: S13 ends with it
  const head = prog(frame, 6, 22);
  const t2 = 1 - prog(frame, marks[1], marks[1] + 12);
  const diag = prog(frame, 22, 40);
  const t3 = betweenStages(frame, marks, 2, 3);
  const slide = smooth(frame, 56, 84);
  const sum0 = betweenStages(frame, marks, 0, 0);
  const sum1 = betweenStages(frame, marks, 1, 1);
  const sum2 = betweenStages(frame, marks, 2, 2);
  const need = prog(frame, marks[2] + 12, marks[2] + 28);

  return (
    <Frame n={14} zoom={1.15} top={245}>
      <Canvas>
        <NodeTable counts={T2} cols={2} order={[[0, 1], [1, 0]]} slide={slide} diag={diag} op={t2} />
        <NodeTable counts={T3} cols={3} order={[[0, 1, 2], [0, 1, 2]]} slide={0} diag={false} op={t3} />
      </Canvas>
      <Fade o={sum0 * head} dy={14}>
        <Box x={CX} y={690} w={1500} align="center" size={64}>
          4 + 3 = 7 of 8 nodes
        </Box>
        <Cap x={CX} y={800} w={1500}>
          match A with blue, B with orange
        </Cap>
      </Fade>
      <Fade o={sum1} dy={14}>
        <Box x={CX} y={690} w={1500} align="center" size={64}>
          0 + 1 = 1 of 8 nodes
        </Box>
        <Cap x={CX} y={800} w={1500}>
          same split, columns in another order
        </Cap>
      </Fade>
      <Fade o={sum2} dy={14}>
        <Box x={CX} y={690} w={1500} align="center" size={56}>
          3 found groups, 2 true groups
        </Box>
        <Cap x={CX} y={790} w={1500}>
          no diagonal to count
        </Cap>
      </Fade>
      {/* stage 3: the table stays; what we need */}
      <Fade o={need * betweenStages(frame, marks, 3, 3)} dy={14}>
        <Box x={CX} y={800} w={1500} align="center" size={52}>
          We need a score that ignores the names and the order.
        </Box>
      </Fade>
    </Frame>
  );
};
