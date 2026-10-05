import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {BAND_SOLID} from '../lib/look';
import {trueLook} from '../lib/eight';

/**
 * Two splits of eight nodes, and how they become a matrix.
 * 0: eight nodes in a row, 1 to 4 blue and 5 to 8 orange ("true groups").
 * 1: the same nodes again below, with the found groups as two boxes A and B; node 5 is ringed.
 * 2: the lower row (the found split) turns by 90 degrees and becomes the left side of a matrix, the upper row (the true
 *    split) its top side: every cell is a pair of nodes.
 */
export const marks = [50, 104, 206];

// the two rows
const ROW_X0 = 470;
const PITCH = 140;
const D0 = 80;
const Y_TRUE = 400;
const Y_FOUND = 700;
const PAD = 0.7 * D0;
const RANGES: ReadonlyArray<readonly [number, number]> = [
  [0, 4],
  [5, 7],
];

// the matrix
const CELL = 64;
const MX = 700;
const MY = 372;
const D1 = 50;
const TOP_Y = MY - 0.62 * CELL;
const LEFT_X = MX - 0.62 * CELL;

const rowX = (i: number) => ROW_X0 + i * PITCH;
const topX = (i: number) => MX + (i + 0.5) * CELL;
const leftY = (i: number) => MY + (i + 0.5) * CELL;

const Node: React.FC<{x: number; y: number; d: number; i: number; op?: number; ring?: number}> = ({x, y, d, i, op = 1, ring = 0}) => {
  const lk = trueLook(i);
  return (
    <g opacity={op}>
      {ring > 0.001 && <circle cx={x} cy={y} r={d / 2 + 9} fill="none" stroke={C.ink} strokeWidth={7} opacity={ring} />}
      <circle cx={x} cy={y} r={d / 2 - lk.sw / 2} fill={lk.fill} stroke={lk.stroke} strokeWidth={lk.sw} />
      <text x={x} y={y + d * 0.17} textAnchor="middle" fontFamily={F.serif} fontSize={d * 0.48} fontWeight={700} fill={lk.text}>
        {i + 1}
      </text>
    </g>
  );
};

export const S09: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const popT = (i: number) => prog(frame, 4 + 4 * i, 18 + 4 * i);
  const capTrue = prog(frame, 32, 46);

  // stage 1
  const foundOp = (i: number) => prog(frame, 54 + 2 * i, 60 + 2 * i);
  const drop = (i: number) => smooth(frame, 54 + 2 * i, 72 + 2 * i);
  const boxOp = prog(frame, 82, 98);
  const capFound = prog(frame, 84, 98);
  const ring = prog(frame, 96, 104);

  // stage 2: the turn
  const t = smooth(frame, marks[1] + 2, marks[1] + 46);
  const gridOp = prog(frame, marks[1] + 38, marks[1] + 58);
  const capCell = prog(frame, marks[1] + 60, marks[1] + 76);
  const rowsOut = 1 - t;
  const d = lerp(D0, D1, t);

  // the found row, dropped from the true row, then turned
  const foundPos = (i: number): [number, number] => {
    const yRow = lerp(Y_TRUE, Y_FOUND, drop(i));
    return [lerp(rowX(i), LEFT_X, t), lerp(yRow, leftY(i), t)];
  };
  const truePos = (i: number): [number, number] => [lerp(rowX(i), topX(i), t), lerp(Y_TRUE, TOP_Y, t)];

  return (
    <Frame n={9} zoom={1.15} top={251}>
      <Canvas>
        {/* the matrix frame: one cell is one pair of nodes */}
        <g opacity={gridOp}>
          {Array.from({length: 8}, (_, i) =>
            Array.from({length: 8}, (_, j) => (
              <rect key={`${i}${j}`} x={MX + j * CELL} y={MY + i * CELL} width={CELL} height={CELL} fill="#fff" stroke={C.faint} strokeWidth={2} />
            )),
          )}
        </g>

        {/* the found groups: two boxes that turn with the row */}
        {RANGES.map(([a, b], g) => {
          const [xa, ya] = foundPos(a);
          const [xb, yb] = foundPos(b);
          const cx = (xa + xb) / 2;
          const cy = (ya + yb) / 2;
          const w = lerp(xb - xa + 2 * PAD, D1 + 16, t);
          const h = lerp(2 * PAD, (b - a + 1) * CELL - 10, t);
          return (
            <g key={g} opacity={boxOp}>
              <rect x={cx - w / 2} y={cy - h / 2} width={w} height={h} rx={lerp(38, 16, t)} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
              <text x={cx} y={cy + h / 2 + 46} textAnchor="middle" fontFamily={F.hand} fontSize={45} fill={C.ink} opacity={rowsOut}>
                {g === 0 ? 'A' : 'B'}
              </text>
            </g>
          );
        })}

        {/* the nodes of the two splits */}
        {Array.from({length: 8}, (_, i) => {
          const [x, y] = truePos(i);
          return <Node key={`t${i}`} x={x} y={y} d={d} i={i} op={popT(i)} />;
        })}
        {Array.from({length: 8}, (_, i) => {
          const [x, y] = foundPos(i);
          return <Node key={`f${i}`} x={x} y={y} d={d} i={i} op={foundOp(i)} ring={i === 4 ? ring * rowsOut : 0} />;
        })}

        {/* the names of the two sides of the matrix */}
        <g opacity={gridOp} fontFamily={F.hand} fontSize={50} fill={C.soft} textAnchor="middle">
          <text x={MX + 4 * CELL} y={TOP_Y - D1 / 2 - 28}>true</text>
          <text x={LEFT_X - D1 / 2 - 70} y={TOP_Y + 8}>found</text>
        </g>
      </Canvas>

      <Fade o={capTrue * rowsOut} dy={14}>
        <Box x={rowX(3.5)} y={Y_TRUE - PAD - 80} w={600} align="center" size={45} color={C.soft} hand>
          true groups
        </Box>
      </Fade>
      <Fade o={capFound * rowsOut} dy={14}>
        <Box x={rowX(3.5)} y={Y_FOUND + PAD + 20} w={600} align="center" size={45} color={C.soft} hand>
          found groups
        </Box>
      </Fade>
      <Fade o={capCell} dy={14}>
        <Box x={960} y={905} w={1600} align="center" size={48}>
          One cell is one pair of nodes.
        </Box>
      </Fade>
    </Frame>
  );
};
