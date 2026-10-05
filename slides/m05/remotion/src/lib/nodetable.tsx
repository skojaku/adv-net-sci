import React from 'react';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {mix} from './network';
import {FOUND8, TRUTH8} from './metrics';
import {Disc} from './eight';

/**
 * The table of nodes: rows are the true groups (blue, orange), columns the found groups (A, B, C), each cell the number of
 * nodes that are in that true group and that found group.
 */
// a found split with three groups: nodes 1 to 3, nodes 4 and 5, nodes 6 to 8
export const FOUND3 = [0, 0, 0, 1, 1, 2, 2, 2] as const;
const count = (found: ReadonlyArray<number>, cols: number) =>
  [0, 1].map((r) => Array.from({length: cols}, (_, c) => TRUTH8.filter((t, i) => t === r && found[i] === c).length));
export const T2 = count(FOUND8, 2); // [[4, 0], [1, 3]]
export const T3 = count(FOUND3, 3); // [[3, 1, 0], [0, 1, 3]]
if (T2.flat().join() !== '4,0,1,3' || T3.flat().join() !== '3,1,0,0,1,3') throw new Error('nodetable: unexpected counts');

export const CW = 200;
export const CH = 150;
export const TOP = 340;
export const CX = 960;
const LETTERS = ['A', 'B', 'C'];

/**
 * One table. `order` lists, for each column slot, which found group stands there; `slide` in [0, 1] moves from the
 * first order to the second (the columns swap places). `diag` shades and outlines the diagonal.
 */
export const NodeTable: React.FC<{
  counts: number[][];
  cols: number;
  order: [number[], number[]];
  slide: number;
  /** true or 1 shades and outlines the diagonal; a number in [0, 1] brings it in gradually */
  diag: boolean | number;
  op: number;
  /** opacity of the counts in the cells (default 1) */
  numOp?: number;
}> = ({counts: tb, cols, order, slide, diag, op, numOp = 1}) => {
  const dg = diag === true ? 1 : diag === false ? 0 : diag;
  const left = CX - (cols * CW) / 2;
  const slot = (g: number) => {
    const a = order[0].indexOf(g);
    const b = order[1].indexOf(g);
    return a + (b - a) * slide;
  };
  return (
    <g opacity={op}>
      {[0, 1].map((r) =>
        Array.from({length: cols}, (_, c) => {
          const d = r === c ? dg : 0;
          return <rect key={`${r}${c}`} x={left + c * CW} y={TOP + r * CH} width={CW} height={CH} fill={mix('#ffffff', C.blueSoft, d)} stroke={mix(C.faint, C.blue, d)} strokeWidth={3 + 4 * d} />;
        }),
      )}
      {[0, 1].map((r) => (
        <Disc key={r} x={left - 70} y={TOP + r * CH + CH / 2} d={64} look={LOOK[r]} />
      ))}
      {Array.from({length: cols}, (_, g) => {
        const x = left + (slot(g) + 0.5) * CW;
        return (
          <g key={g}>
            <rect x={x - 46} y={TOP - 96} width={92} height={70} rx={20} fill={C.blueMid} stroke={C.blue} strokeWidth={3} />
            <text x={x} y={TOP - 46} textAnchor="middle" fontFamily={F.serif} fontSize={48} fontWeight={700} fill={C.ink}>
              {LETTERS[g]}
            </text>
            {[0, 1].map((r) => (
              <text key={r} x={x} y={TOP + r * CH + CH / 2 + 28} textAnchor="middle" fontFamily={F.serif} fontSize={84} fill={C.ink} opacity={numOp}>
                {tb[r][g]}
              </text>
            ))}
          </g>
        );
      })}
    </g>
  );
};
