import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {betweenStages, prog} from '../lib/anim';
import {Row8} from '../lib/entropy8';
import {CX, NodeTable, T2} from '../lib/nodetable';

/**
 * After the Rand index and the ARI, which count pairs of nodes: why not count nodes instead?
 * 0: one node lights up.
 * 1: the table of nodes: how many nodes are in each (true group, found group) cell.
 */
export const marks = [50, 112];

const ROW_Y = 520;
const GAP = 170;
const D = 96;
const ONE = 2; // node 3

export const S13: React.FC = () => {
  const frame = useCurrentFrame();

  const row = betweenStages(frame, marks, 0, 0);
  const cap0 = prog(frame, 30, 46);
  const table = prog(frame, marks[0] + 6, marks[0] + 24);
  const cap1 = prog(frame, marks[0] + 24, marks[0] + 40);

  return (
    <Frame n={13} zoom={1.15} top={245}>
      <Canvas>
        <g opacity={row}>
          <Row8 cx={CX} y={ROW_Y} gap={GAP} d={D} nodeOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)} lit={(i) => (i === ONE ? prog(frame, 24, 40) : 0)} />
        </g>
        <NodeTable counts={T2} cols={2} order={[[0, 1], [0, 1]]} slide={0} diag={false} op={table} />
      </Canvas>
      <Fade o={row * cap0} dy={14}>
        <Box x={CX} y={730} w={1500} align="center" size={54}>
          Why not count nodes, one at a time?
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={CX} y={690} w={1500} align="center" size={54}>
          Count the nodes in each cell.
        </Box>
      </Fade>
    </Frame>
  );
};
