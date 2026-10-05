import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {betweenStages, prog} from '../lib/anim';
import {BOX_PAD, GroupBox, HiddenNode, NodeDisc, eightX} from '../lib/entropy8';

/**
 * Yes/no questions as a tree. The hidden node "?" belongs to one of K equal groups of the eight nodes.
 * 0: 2 groups, 1 question.  1: 4 groups, 2 questions.  2: 8 groups (every node alone), 3 questions; entropy defined.
 */
export const marks = [60, 110, 170];

const CX = 960;
const GAP = 150;
const NODE_Y = 730;
const ROOT_Y = 290;
const LEAF_TOP = NODE_Y - BOX_PAD; // where a branch meets a group box
const D = 84;

type Pt = readonly [number, number];

/** The tree for K = 2^depth equal groups of the 8 nodes: edges, small junctions, and a yes/no label on every edge. */
const tree = (depth: number) => {
  const groups = 2 ** depth;
  const size = 8 / groups;
  const centre = (g: number) => (eightX(g * size, CX, GAP) + eightX(g * size + size - 1, CX, GAP)) / 2;
  const levelY = (k: number) => ROOT_Y + 44 + ((LEAF_TOP - ROOT_Y - 44) * k) / depth;
  const edges: {from: Pt; to: Pt; yes: boolean}[] = [];
  const junctions: Pt[] = [];
  // a vertex at level k covers 2^(depth - k) groups, starting at group `first`; the left child is "yes", the right one "no"
  const walk = (k: number, first: number, parent: Pt, yes: boolean) => {
    const span = 2 ** (depth - k);
    const x = (centre(first) + centre(first + span - 1)) / 2;
    const here: Pt = [x, levelY(k)];
    if (k > 0) {
      edges.push({from: parent, to: here, yes});
      if (k < depth) junctions.push(here);
    }
    if (k < depth) {
      const half = span / 2;
      walk(k + 1, first, here, true);
      walk(k + 1, first + half, here, false);
    }
  };
  walk(0, 0, [CX, levelY(0)], true);
  const boxes = Array.from({length: groups}, (_, g) => [g * size, g * size + size - 1] as const);
  return {edges, junctions, boxes};
};
const TREES = [tree(1), tree(2), tree(3)];

const Tree: React.FC<{k: number; op: number}> = ({k, op}) => {
  const t = TREES[k];
  return (
    <g opacity={op}>
      {t.boxes.map(([a, b], i) => (
        <GroupBox key={i} cx={CX} y={NODE_Y} gap={GAP} a={a} b={b} />
      ))}
      {t.edges.map((e, i) => (
        <line key={i} x1={e.from[0]} y1={e.from[1]} x2={e.to[0]} y2={e.to[1]} stroke={C.ink} strokeWidth={4} />
      ))}
      {t.junctions.map((p, i) => (
        <circle key={i} cx={p[0]} cy={p[1]} r={10} fill={C.blue} />
      ))}
      {t.edges.map((e, i) => {
        const mx = (e.from[0] + e.to[0]) / 2;
        const my = (e.from[1] + e.to[1]) / 2;
        return (
          <text key={i} x={mx + (e.yes ? -30 : 30)} y={my + 8} textAnchor={e.yes ? 'end' : 'start'} fontFamily={F.hand} fontSize={40} fill={C.soft}>
            {e.yes ? 'yes' : 'no'}
          </text>
        );
      })}
    </g>
  );
};

export const S14: React.FC = () => {
  const frame = useCurrentFrame();

  const nodes = (i: number) => prog(frame, 2 + i * 1.5, 16 + i * 1.5);
  const root = prog(frame, 8, 24);
  const l0 = betweenStages(frame, marks, 0, 0);
  const l1 = betweenStages(frame, marks, 1, 1);
  const l2 = betweenStages(frame, marks, 2, 2);
  const in0 = prog(frame, 22, 40);
  const cap0 = betweenStages(frame, marks, 0, 0);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = betweenStages(frame, marks, 2, 2);
  const def = prog(frame, 134, 152);

  return (
    <Frame n={14} title="How many yes/no questions?">
      <Canvas>
        <Tree k={0} op={l0 * in0} />
        <Tree k={1} op={l1} />
        <Tree k={2} op={l2} />
        {Array.from({length: 8}, (_, i) => (
          <NodeDisc key={i} x={eightX(i, CX, GAP)} y={NODE_Y} d={D} look={LOOK[0]} label={i + 1} op={nodes(i)} />
        ))}
        <HiddenNode x={CX} y={ROOT_Y} d={D} halo={1} op={root} />
      </Canvas>
      <Fade o={cap0 * in0} dy={12}>
        <Box x={CX + 90} y={ROOT_Y - 36} w={600} size={54}>
          1 question
        </Box>
      </Fade>
      <Fade o={cap1} dy={12}>
        <Box x={CX + 90} y={ROOT_Y - 36} w={600} size={54}>
          2 questions
        </Box>
      </Fade>
      <Fade o={cap2} dy={12}>
        <Box x={CX + 90} y={ROOT_Y - 36} w={600} size={54}>
          3 questions
        </Box>
      </Fade>
      <Fade o={def} dy={14}>
        <Box x={CX} y={860} w={1680} align="center" size={45}>
          <Term>entropy</Term>: the average number of yes/no questions per node
        </Box>
      </Fade>
    </Frame>
  );
};
