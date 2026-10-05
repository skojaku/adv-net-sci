import React from 'react';
import {C, F} from '../theme';
import {LOOK, type Look} from './look';
import {FOUND8, TRUTH8, entropy, mutualInfo} from './metrics';

/**
 * Shared by S13 to S17: the eight-node example drawn as one row, with the found groups as boxes.
 * Palette: black, white, blue. True group 0 (nodes 1 to 4) is SOLID, true group 1 (nodes 5 to 8) is HOLLOW.
 */

export const NODE8_D = 84;
/** distance from a disc's centre to the box around it */
export const BOX_PAD = 58;

export const TRUE_LOOK8: ReadonlyArray<Look> = TRUTH8.map((g) => LOOK[g]);
export const SOLID_ALL8: ReadonlyArray<Look> = TRUTH8.map(() => LOOK[0]);

/** x of node i (0-based) in a row centred at cx. */
export const eightX = (i: number, cx: number, gap: number) => cx + (i - 3.5) * gap;

/** The found groups of the example as contiguous index ranges: A = nodes 1 to 5, B = nodes 6 to 8. */
export const AB_RANGES: ReadonlyArray<readonly [number, number]> = [
  [0, 4],
  [5, 7],
];

/** Every node alone: eight boxes of one node each. */
export const ALONE_RANGES: ReadonlyArray<readonly [number, number]> = [0, 1, 2, 3, 4, 5, 6, 7].map((i) => [i, i] as const);

/** One node: a disc in a Look, with its number. `halo` in [0, 1] draws a light-blue halo behind it (a node that is lit). */
export const NodeDisc: React.FC<{x: number; y: number; d?: number; look: Look; label?: string | number; halo?: number; op?: number; fs?: number}> = ({
  x,
  y,
  d = NODE8_D,
  look,
  label,
  halo = 0,
  op = 1,
  fs,
}) => (
  <g opacity={op}>
    {halo > 0.001 && <circle cx={x} cy={y} r={d / 2 + 16} fill={C.blueMid} opacity={halo} />}
    <circle cx={x} cy={y} r={d / 2 - look.sw / 2} fill={look.fill} stroke={look.stroke} strokeWidth={look.sw} />
    {label != null && (
      <text x={x} y={y + d * 0.17} textAnchor="middle" fontFamily={F.serif} fontSize={fs ?? Math.max(36, d * 0.46)} fontWeight={700} fill={look.text}>
        {label}
      </text>
    )}
  </g>
);

/** The node whose group we do not know: black, with a white question mark. */
export const HiddenNode: React.FC<{x: number; y: number; d?: number; halo?: number; op?: number}> = ({x, y, d = 96, halo = 1, op = 1}) => (
  <NodeDisc x={x} y={y} d={d} look={LOOK[3]} label="?" halo={halo} op={op} fs={d * 0.62} />
);

type Num = number | ((i: number) => number);
const at = (v: Num | undefined, i: number, dflt: number) => (v === undefined ? dflt : typeof v === 'number' ? v : v(i));

/** A rounded box around nodes a to b (0-based, inclusive) of a row. */
export const GroupBox: React.FC<{cx: number; y: number; gap: number; a: number; b: number; op?: number; hot?: number}> = ({cx, y, gap, a, b, op = 1, hot = 0}) => {
  const x0 = eightX(a, cx, gap) - BOX_PAD;
  const x1 = eightX(b, cx, gap) + BOX_PAD;
  return (
    <g opacity={op}>
      {hot > 0.001 && <rect x={x0} y={y - BOX_PAD} width={x1 - x0} height={2 * BOX_PAD} rx={38} fill={C.blueSoft} opacity={hot} />}
      <rect x={x0} y={y - BOX_PAD} width={x1 - x0} height={2 * BOX_PAD} rx={38} fill="none" stroke={C.soft} strokeWidth={4} />
    </g>
  );
};

/** Eight numbered nodes in a row, with rounded boxes around groups of neighbours. SVG, canvas coordinates. */
export const Row8: React.FC<{
  cx: number;
  y: number;
  gap?: number;
  d?: number;
  looks?: ReadonlyArray<Look>;
  boxes?: ReadonlyArray<readonly [number, number]>;
  boxOp?: number;
  nodeOp?: Num;
  /** halo of each node, 0 to 1 */
  lit?: Num;
  /** fill of box k, 0 to 1 (a box that holds the hidden node) */
  boxHot?: Num;
}> = ({cx, y, gap = 150, d = NODE8_D, looks = TRUE_LOOK8, boxes, boxOp = 1, nodeOp, lit, boxHot}) => (
  <g>
    {boxes && boxOp > 0.001 && boxes.map(([a, b], k) => <GroupBox key={k} cx={cx} y={y} gap={gap} a={a} b={b} op={boxOp} hot={at(boxHot, k, 0)} />)}
    {looks.map((lk, i) => {
      const o = at(nodeOp, i, 1);
      if (o <= 0.001) return null;
      return <NodeDisc key={i} x={eightX(i, cx, gap)} y={y} d={d} look={lk} label={i + 1} halo={at(lit, i, 0)} op={o} />;
    })}
  </g>
);

/** Three-decimal text. */
export const f3 = (x: number) => x.toFixed(3);

/** The numbers of S15 to S18, computed once from the example. */
export const H_TRUE = entropy(TRUTH8);
export const H_FOUND = entropy(FOUND8);
export const I_TF = mutualInfo(TRUTH8, FOUND8);
export const H_GIVEN = H_TRUE - I_TF;

/** The same H(true given found), straight from the definition: the entropy of the true groups inside each found group, weighted by the group's size. */
const members = (g: number) => TRUTH8.filter((_, i) => FOUND8[i] === g);
const compo = (g: number) => ({n: members(g).length, h: entropy(members(g)), solid: members(g).filter((t) => t === 0).length, hollow: members(g).filter((t) => t === 1).length});
export const GROUP_A = compo(0);
export const GROUP_B = compo(1);
const hDirect = (GROUP_A.n / 8) * GROUP_A.h + (GROUP_B.n / 8) * GROUP_B.h;

if (Math.abs(hDirect - H_GIVEN) > 1e-9) throw new Error(`H(true given found): ${hDirect} vs ${H_TRUE} - ${I_TF}`);
if (f3(H_TRUE) !== '1.000' || f3(H_FOUND) !== '0.954' || f3(I_TF) !== '0.549' || f3(H_GIVEN) !== '0.451') {
  throw new Error(`entropy8: unexpected numbers ${f3(H_TRUE)} ${f3(H_FOUND)} ${f3(I_TF)} ${f3(H_GIVEN)}`);
}
if (f3(GROUP_A.h) !== '0.722' || GROUP_B.h !== 0 || GROUP_A.solid !== 4 || GROUP_A.hollow !== 1 || GROUP_B.hollow !== 3) {
  throw new Error('entropy8: unexpected group compositions');
}
