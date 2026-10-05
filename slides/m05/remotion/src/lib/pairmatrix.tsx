import React from 'react';
import {C, F} from '../theme';
import {BAND_SOLID} from './look';
import {FOUND8, TRUTH8, randIndex} from './metrics';
import {Disc, trueLook} from './eight';

/**
 * The 28 pairs of the eight-node example as the cells of a matrix (nodes 1 to 8 along both sides, one cell
 * for each pair i < j). A pair is never drawn as two nodes joined by a line: a line reads as a network edge.
 */
export const PAIRS8: {i: number; j: number; k: number; trueSame: boolean; foundSame: boolean; agree: boolean}[] = [];
for (let i = 0; i < 8; i++) {
  for (let j = i + 1; j < 8; j++) {
    const trueSame = TRUTH8[i] === TRUTH8[j];
    const foundSame = FOUND8[i] === FOUND8[j];
    PAIRS8.push({i, j, k: PAIRS8.length, trueSame, foundSame, agree: trueSame === foundSame});
  }
}
export const N_AGREE = PAIRS8.filter((p) => p.agree).length;
if (PAIRS8.length !== 28 || N_AGREE !== 21 || Math.abs(N_AGREE / 28 - randIndex(TRUTH8, FOUND8)) > 1e-9) {
  throw new Error('pairmatrix: unexpected pair counts');
}

/** Cell half: blue tint when the pair is together, white when it is apart. */
export const TOGETHER = '#9db1de';

/** The found groups of the example as ranges of rows: nodes 1 to 5 (A) and nodes 6 to 8 (B). */
const BOXES: ReadonlyArray<readonly [number, number]> = [
  [0, 4],
  [5, 7],
];

/**
 * The matrix. (x, y) is the top-left corner of the cell area, `c` the size of a cell. The top side lists the
 * nodes with their true colours; the left side lists them inside their found boxes.
 * `trueHalf(k)`, `foundHalf(k)` and `mark(k)` give, for the pair with index k, the opacity of its upper half
 * (the true split), its lower half (the found split) and its check or cross.
 */
export const PairMatrix: React.FC<{
  x: number;
  y: number;
  c?: number;
  trueHalf?: (k: number) => number;
  foundHalf?: (k: number) => number;
  mark?: (k: number) => number;
  /** pair indices to outline in black */
  hot?: number[];
  /** nodes to ring in the headers */
  ringNodes?: number[];
  headerOp?: number;
  labels?: boolean;
  /** draw the found boxes around the nodes on the left */
  boxes?: boolean;
}> = ({x, y, c = 76, trueHalf, foundHalf, mark, hot = [], ringNodes = [], headerOp = 1, labels = true, boxes = true}) => {
  const d = 0.7 * c;
  const topY = y - 0.62 * c;
  const leftX = x - 0.62 * c;
  const cx = (j: number) => x + (j + 0.5) * c;
  const cy = (i: number) => y + (i + 0.5) * c;
  return (
    <g>
      {/* the cells below the diagonal and the diagonal repeat the pairs above it: left empty */}
      {Array.from({length: 8}, (_, i) =>
        Array.from({length: 8}, (_, j) =>
          j <= i ? <rect key={`e${i}${j}`} x={x + j * c} y={y + i * c} width={c} height={c} fill="#f4f4f4" /> : null,
        ),
      )}
      {PAIRS8.map((p) => {
        const x0 = x + p.j * c;
        const y0 = y + p.i * c;
        const t = trueHalf?.(p.k) ?? 0;
        const f = foundHalf?.(p.k) ?? 0;
        const m = mark?.(p.k) ?? 0;
        const s = c * 0.17;
        const gx = x0 + c / 2;
        const gy = y0 + c / 2;
        return (
          <g key={p.k}>
            <rect x={x0} y={y0} width={c} height={c} fill="#fff" stroke={C.faint} strokeWidth={2} />
            {t > 0.001 && <polygon points={`${x0},${y0} ${x0 + c},${y0} ${x0 + c},${y0 + c}`} fill={p.trueSame ? TOGETHER : '#fff'} opacity={t} />}
            {f > 0.001 && <polygon points={`${x0},${y0} ${x0},${y0 + c} ${x0 + c},${y0 + c}`} fill={p.foundSame ? TOGETHER : '#fff'} opacity={f} />}
            {m > 0.001 && (
              <g opacity={m}>
                <circle cx={gx} cy={gy} r={c * 0.3} fill="#fff" stroke={p.agree ? C.blue : C.red} strokeWidth={3} />
                {p.agree ? (
                  <path d={`M${gx - s} ${gy + s * 0.05} L${gx - s * 0.3} ${gy + s * 0.8} L${gx + s} ${gy - s * 0.7}`} fill="none" stroke={C.blue} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
                ) : (
                  <path d={`M${gx - s * 0.8} ${gy - s * 0.8} L${gx + s * 0.8} ${gy + s * 0.8} M${gx + s * 0.8} ${gy - s * 0.8} L${gx - s * 0.8} ${gy + s * 0.8}`} fill="none" stroke={C.red} strokeWidth={6} strokeLinecap="round" />
                )}
              </g>
            )}
            {hot.includes(p.k) && <rect x={x0 + 3} y={y0 + 3} width={c - 6} height={c - 6} fill="none" stroke={C.ink} strokeWidth={7} />}
          </g>
        );
      })}
      <g opacity={headerOp}>
        {/* top: the nodes in their true colours */}
        {Array.from({length: 8}, (_, j) => (
          <Disc key={`t${j}`} x={cx(j)} y={topY} d={d} look={trueLook(j)} label={j + 1} ring={ringNodes.includes(j) ? 1 : 0} />
        ))}
        {/* left: the nodes inside their found boxes */}
        {boxes && BOXES.map(([a, b], n) => (
          <rect key={`b${n}`} x={leftX - d / 2 - 12} y={cy(a) - c / 2 + 6} width={d + 24} height={(b - a + 1) * c - 12} rx={20} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
        ))}
        {Array.from({length: 8}, (_, i) => (
          <Disc key={`l${i}`} x={leftX} y={cy(i)} d={d} look={trueLook(i)} label={i + 1} ring={ringNodes.includes(i) ? 1 : 0} />
        ))}
        {labels && (
          <g fontFamily={F.hand} fontSize={45} fill={C.soft} textAnchor="middle">
            <text x={x + 4 * c} y={topY - d / 2 - 22}>true</text>
            <text x={leftX - d / 2 - 70} y={topY + 8}>found</text>
          </g>
        )}
      </g>
    </g>
  );
};

/**
 * A matrix for ONE split: the cell of a pair is shaded when the two nodes are in the same group of that split
 * (`mode` 'true': the same colour, 'found': the same box). Mode 'agree' compares the two: a check where the true
 * and the found matrix are alike (both shaded or both white), a cross where they differ.
 * `reveal(k)` is the opacity of the cell of the pair with index k. Nodes run along both sides; only the 28 pairs
 * above the diagonal are cells.
 */
export const CoMatrix: React.FC<{
  x: number;
  y: number;
  c?: number;
  mode: 'true' | 'found' | 'agree';
  reveal?: (k: number) => number;
  /** opacity of the frame, the headers and the label */
  frame?: number;
  label?: string;
}> = ({x, y, c = 54, mode, reveal, frame = 1, label}) => {
  const d = 0.78 * c;
  const cx = (j: number) => x + (j + 0.5) * c;
  const cy = (i: number) => y + (i + 0.5) * c;
  const s = c * 0.17;
  const head = (px: number, py: number, i: number, key: string) => {
    const lk = trueLook(i);
    return (
      <g key={key}>
        <circle cx={px} cy={py} r={d / 2 - lk.sw / 2} fill={lk.fill} stroke={lk.stroke} strokeWidth={lk.sw} />
        <text x={px} y={py + 9} textAnchor="middle" fontFamily={F.serif} fontSize={26} fontWeight={700} fill={lk.text}>
          {i + 1}
        </text>
      </g>
    );
  };
  return (
    <g>
      <g opacity={frame}>
        {Array.from({length: 8}, (_, i) =>
          Array.from({length: 8}, (_, j) => (j <= i ? <rect key={`e${i}${j}`} x={x + j * c} y={y + i * c} width={c} height={c} fill="#f4f4f4" /> : null)),
        )}
        {PAIRS8.map((p) => (
          <rect key={`f${p.k}`} x={x + p.j * c} y={y + p.i * c} width={c} height={c} fill="#fff" stroke={C.faint} strokeWidth={2} />
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
      {PAIRS8.map((p) => {
        const r = reveal?.(p.k) ?? 0;
        if (r < 0.001) return null;
        const x0 = x + p.j * c;
        const y0 = y + p.i * c;
        if (mode !== 'agree') {
          const together = mode === 'true' ? p.trueSame : p.foundSame;
          return together ? <rect key={p.k} x={x0} y={y0} width={c} height={c} fill={TOGETHER} stroke={C.faint} strokeWidth={2} opacity={r} /> : null;
        }
        const gx = x0 + c / 2;
        const gy = y0 + c / 2;
        return (
          <g key={p.k} opacity={r}>
            <circle cx={gx} cy={gy} r={c * 0.34} fill="#fff" stroke={p.agree ? C.blue : C.red} strokeWidth={3} />
            {p.agree ? (
              <path d={`M${gx - s} ${gy + s * 0.05} L${gx - s * 0.3} ${gy + s * 0.8} L${gx + s} ${gy - s * 0.7}`} fill="none" stroke={C.blue} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
            ) : (
              <path d={`M${gx - s * 0.8} ${gy - s * 0.8} L${gx + s * 0.8} ${gy + s * 0.8} M${gx + s * 0.8} ${gy - s * 0.8} L${gx - s * 0.8} ${gy + s * 0.8}`} fill="none" stroke={C.red} strokeWidth={6} strokeLinecap="round" />
            )}
          </g>
        );
      })}
    </g>
  );
};
