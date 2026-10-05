import React from 'react';
import {C, F} from '../theme';
import {BAND_SOLID} from './look';
import {FOUND8, TRUTH8, randIndex} from './metrics';
import {trueLook} from './eight';

/**
 * The pairs of the eight-node example as the cells of a full 8 x 8 matrix (nodes 1 to 8 along both sides).
 * A pair is never drawn as two nodes joined by a line: a line reads as a network edge.
 * Every pair (i, j) with i != j is in two cells ((i, j) and (j, i)) and the diagonal is a node with itself:
 * the diagonal is shown but is not a pair and is not counted.
 */
export const PAIRS8: {i: number; j: number; k: number; trueSame: boolean; foundSame: boolean; agree: boolean}[] = [];
for (let i = 0; i < 8; i++) {
  for (let j = i + 1; j < 8; j++) {
    const trueSame = TRUTH8[i] === TRUTH8[j];
    const foundSame = FOUND8[i] === FOUND8[j];
    PAIRS8.push({i, j, k: PAIRS8.length, trueSame, foundSame, agree: trueSame === foundSame});
  }
}
/** pairs together in both splits (the product of the two matrices is 1), and pairs apart in both (the product of the complements is 1) */
export const N_BOTH = PAIRS8.filter((p) => p.trueSame && p.foundSame).length;
export const N_APART = PAIRS8.filter((p) => !p.trueSame && !p.foundSame).length;
export const N_PAIRS = PAIRS8.length;
if (N_PAIRS !== 28 || N_BOTH !== 9 || N_APART !== 12 || Math.abs((N_BOTH + N_APART) / N_PAIRS - randIndex(TRUTH8, FOUND8)) > 1e-9) {
  throw new Error('pairmatrix: unexpected pair counts');
}

/** Cell shade: blue tint when the pair is together, white when it is apart. */
export const TOGETHER = '#9db1de';

/** The found groups of the example as ranges of rows: nodes 1 to 5 (A) and nodes 6 to 8 (B). */
const BOXES: ReadonlyArray<readonly [number, number]> = [
  [0, 4],
  [5, 7],
];

/**
 * A matrix for ONE split: the cell of a pair is shaded when the two nodes are in the same group of that split
 * (`mode` 'true': the same colour, 'found': the same box). The product of the two: mode 'both' puts a check on the cells
 * shaded in both matrices (the pair is together in both splits); mode 'apart' puts a check on the cells white in both
 * (the pair is apart in both splits). A cell that is not in the class has no mark.
 * `reveal(k)` is the opacity of the cell (row i, column j), k = 8 i + j. `hot` outlines cells, `ringNodes` rings nodes in the headers.
 */
export const CoMatrix: React.FC<{
  x: number;
  y: number;
  c?: number;
  mode: 'true' | 'found' | 'both' | 'apart';
  reveal?: (k: number) => number;
  /** opacity of the frame, the headers and the label */
  frame?: number;
  label?: string;
  hot?: [number, number][];
  ringNodes?: number[];
}> = ({x, y, c = 54, mode, reveal, frame = 1, label, hot = [], ringNodes = []}) => {
  const d = 0.78 * c;
  const cx = (j: number) => x + (j + 0.5) * c;
  const cy = (i: number) => y + (i + 0.5) * c;
  const s = c * 0.17;
  const head = (px: number, py: number, i: number, key: string) => {
    const lk = trueLook(i);
    return (
      <g key={key}>
        {ringNodes.includes(i) && <circle cx={px} cy={py} r={d / 2 + 6} fill="none" stroke={C.ink} strokeWidth={5} />}
        <circle cx={px} cy={py} r={d / 2 - lk.sw / 2} fill={lk.fill} stroke={lk.stroke} strokeWidth={lk.sw} />
        <text x={px} y={py + 9} textAnchor="middle" fontFamily={F.serif} fontSize={26} fontWeight={700} fill={lk.text}>
          {i + 1}
        </text>
      </g>
    );
  };
  const cells: {i: number; j: number; k: number}[] = [];
  for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) cells.push({i, j, k: 8 * i + j});
  const same = (i: number, j: number, m: 'true' | 'found') => (i === j ? true : m === 'true' ? TRUTH8[i] === TRUTH8[j] : FOUND8[i] === FOUND8[j]);
  return (
    <g>
      <g opacity={frame}>
        {cells.map(({i, j, k}) => (
          <rect key={`f${k}`} x={x + j * c} y={y + i * c} width={c} height={c} fill="#fff" stroke={C.faint} strokeWidth={2} />
        ))}
        {mode === 'found' &&
          BOXES.map(([a, b], n) => (
            <g key={`b${n}`}>
              <rect x={x - 0.62 * c - d / 2 - 8} y={cy(a) - c / 2 + 5} width={d + 16} height={(b - a + 1) * c - 10} rx={16} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
              <rect x={cx(a) - c / 2 + 5} y={y - 0.62 * c - d / 2 - 8} width={(b - a + 1) * c - 10} height={d + 16} rx={16} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
            </g>
          ))}
        {Array.from({length: 8}, (_, j) => head(cx(j), y - 0.62 * c, j, `t${j}`))}
        {Array.from({length: 8}, (_, i) => head(x - 0.62 * c, cy(i), i, `l${i}`))}
        {label && (
          <text x={x + 4 * c} y={y - 0.62 * c - d / 2 - 28} textAnchor="middle" fontFamily={F.hand} fontSize={50} fill={C.soft}>
            {label}
          </text>
        )}
      </g>
      {cells.map(({i, j, k}) => {
        const r = reveal?.(k) ?? 0;
        if (r < 0.001) return null;
        const x0 = x + j * c;
        const y0 = y + i * c;
        if (mode === 'true' || mode === 'found') {
          return same(i, j, mode) ? <rect key={k} x={x0} y={y0} width={c} height={c} fill={TOGETHER} stroke={C.faint} strokeWidth={2} opacity={r} /> : null;
        }
        const t = same(i, j, 'true');
        const f = same(i, j, 'found');
        if (mode === 'both' ? !(t && f) : t || f) return null;
        const diag = i === j;
        const col = diag ? C.soft : C.blue;
        const gx = x0 + c / 2;
        const gy = y0 + c / 2;
        return (
          <g key={k} opacity={r}>
            <rect x={x0} y={y0} width={c} height={c} fill={mode === 'both' ? TOGETHER : C.blueSoft} stroke={C.faint} strokeWidth={2} />
            <circle cx={gx} cy={gy} r={c * 0.34} fill="#fff" stroke={col} strokeWidth={3} />
            <path d={`M${gx - s} ${gy + s * 0.05} L${gx - s * 0.3} ${gy + s * 0.8} L${gx + s} ${gy - s * 0.7}`} fill="none" stroke={col} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
          </g>
        );
      })}
      {hot.map(([i, j]) => (
        <rect key={`h${i}${j}`} x={x + j * c + 3} y={y + i * c + 3} width={c - 6} height={c - 6} fill="none" stroke={C.ink} strokeWidth={7} />
      ))}
    </g>
  );
};
