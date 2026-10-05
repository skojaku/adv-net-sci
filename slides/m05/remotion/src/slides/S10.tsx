import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {betweenStages, prog, smooth} from '../lib/anim';
import {FOUND8, TRUTH8} from '../lib/metrics';
import {Disc} from '../lib/eight';

/**
 * Why not count nodes? Count the nodes that sit in the "right" found group. That needs each found group
 * matched with a true group, and the match is arbitrary.
 * 0: the table of S09 (rows: true groups, columns: found groups A and B); match A with blue and B with orange:
 *    the diagonal holds 4 + 3 = 7 of 8 nodes.
 * 1: the same split, the columns in another order: the diagonal holds 0 + 1 = 1 of 8.
 * 2: three found groups against two true groups: there is no diagonal to count.
 * 3: a pair of nodes needs no names: together or apart.
 */
export const marks = [50, 112, 172, 226];

// found split with three groups: nodes 1 to 3, nodes 4 and 5, nodes 6 to 8
const FOUND3 = [0, 0, 0, 1, 1, 2, 2, 2];
const counts = (found: ReadonlyArray<number>, cols: number) =>
  [0, 1].map((r) => Array.from({length: cols}, (_, c) => TRUTH8.filter((t, i) => t === r && found[i] === c).length));
const T2 = counts(FOUND8, 2); // [[4, 0], [1, 3]]
const T3 = counts(FOUND3, 3); // [[3, 1, 0], [0, 1, 3]]
if (T2.flat().join() !== '4,0,1,3' || T3.flat().join() !== '3,1,0,0,1,3') throw new Error('S10: unexpected counts');

const CW = 200;
const CH = 150;
const TOP = 340;
const CX = 960;
const LETTERS = ['A', 'B', 'C'];

/** One table. `order` lists, for each column slot, which found group stands there; `slide` in [0,1] moves from the first order to the second. */
const Table: React.FC<{counts: number[][]; cols: number; order: [number[], number[]]; slide: number; diag: boolean; op: number}> = ({counts: tb, cols, order, slide, diag, op}) => {
  const left = CX - (cols * CW) / 2;
  const slot = (g: number) => {
    const a = order[0].indexOf(g);
    const b = order[1].indexOf(g);
    return a + (b - a) * slide;
  };
  return (
    <g opacity={op}>
      {/* the cells and the diagonal */}
      {[0, 1].map((r) =>
        Array.from({length: cols}, (_, c) => (
          <rect key={`${r}${c}`} x={left + c * CW} y={TOP + r * CH} width={CW} height={CH} fill={diag && r === c ? C.blueSoft : '#fff'} stroke={diag && r === c ? C.blue : C.faint} strokeWidth={diag && r === c ? 7 : 3} />
        )),
      )}
      {/* row headers: the true groups */}
      {[0, 1].map((r) => (
        <Disc key={r} x={left - 70} y={TOP + r * CH + CH / 2} d={64} look={LOOK[r]} />
      ))}
      {/* the counts and the found-group letters travel with their column */}
      {Array.from({length: cols}, (_, g) => {
        const x = left + (slot(g) + 0.5) * CW;
        return (
          <g key={g}>
            <rect x={x - 46} y={TOP - 96} width={92} height={70} rx={20} fill={C.blueMid} stroke={C.blue} strokeWidth={3} />
            <text x={x} y={TOP - 46} textAnchor="middle" fontFamily={F.serif} fontSize={48} fontWeight={700} fill={C.ink}>
              {LETTERS[g]}
            </text>
            {[0, 1].map((r) => (
              <text key={r} x={x} y={TOP + r * CH + CH / 2 + 28} textAnchor="middle" fontFamily={F.serif} fontSize={84} fill={C.ink}>
                {tb[r][g]}
              </text>
            ))}
          </g>
        );
      })}
    </g>
  );
};

export const S10: React.FC = () => {
  const frame = useCurrentFrame();

  const head = prog(frame, 0, 16);
  const t2 = betweenStages(frame, marks, 0, 1);
  const t3 = betweenStages(frame, marks, 2, 2);
  const slide = smooth(frame, 56, 84);
  const sum0 = betweenStages(frame, marks, 0, 0);
  const sum1 = betweenStages(frame, marks, 1, 1);
  const sum2 = betweenStages(frame, marks, 2, 2);
  const fin = betweenStages(frame, marks, 3, 3);

  return (
    <Frame n={10} title="Why not count nodes?">
      <Canvas>
        <Table counts={T2} cols={2} order={[[0, 1], [1, 0]]} slide={slide} diag op={t2 * head} />
        <Table counts={T3} cols={3} order={[[0, 1, 2], [0, 1, 2]]} slide={0} diag={false} op={t3} />
        {/* stage 3: one pair of nodes, no names */}
        <g opacity={fin}>
          <rect x={CX - 200} y={380} width={400} height={170} rx={50} fill={C.blueMid} stroke={C.blue} strokeWidth={4} />
          <Disc x={CX - 90} y={465} d={96} look={LOOK[0]} label={1} />
          <Disc x={CX + 90} y={465} d={96} look={LOOK[0]} label={2} />
        </g>
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
          no one-to-one match
        </Cap>
      </Fade>
      <Fade o={fin} dy={14}>
        <Box x={CX} y={620} w={1500} align="center" size={56}>
          A pair is <Term>together</Term> or <Term>apart</Term>.
        </Box>
        <Box x={CX} y={715} w={1500} align="center" size={50} color={C.soft}>
          No group names to match.
        </Box>
      </Fade>
    </Frame>
  );
};
