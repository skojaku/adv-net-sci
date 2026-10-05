import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {FOUND8, TRUTH8} from '../lib/metrics';
import {Disc, EightRows, RowGeom, boxPad, mixGeom, nodeX, rowCentre, trueLook} from '../lib/eight';
import {BAND_SOLID, LOOK} from '../lib/look';

/**
 * 0: eight nodes in a row, 1 to 4 blue and 5 to 8 orange ("true groups").
 * 1: the same nodes again below, with the found groups as two boxes A and B; node 5 is ringed.
 * 2: the rows shrink to the left; the nodes fly one by one into a 2 x 2 table (true fill x found box); we count nodes.
 */
export const marks = [50, 104, 216];

const BIG: RowGeom = {x0: 470, pitch: 140, d: 80, yTrue: 420, yFound: 760};
const SMALL: RowGeom = {x0: 164, pitch: 104, d: 60, yTrue: 470, yFound: 700};

// the 2 x 2 table (rows: true colour, columns: found box)
const GX0 = 1070;
const GY0 = 370;
const CW = 330;
const CH = 200;
const GG = 20;
const cellX = (c: number) => GX0 + c * (CW + GG);
const cellY = (r: number) => GY0 + r * (CH + GG);

// the place of node i inside its cell: 2 per row
const SLOT: number[] = (() => {
  const used = [
    [0, 0],
    [0, 0],
  ];
  return TRUTH8.map((t, i) => used[t][FOUND8[i]]++);
})();
const CELL_N = (r: number, c: number) => TRUTH8.filter((t, i) => t === r && FOUND8[i] === c).length;
const target = (i: number): [number, number] => {
  const r = TRUTH8[i];
  const c = FOUND8[i];
  const rows = Math.ceil(CELL_N(r, c) / 2);
  return [cellX(c) + 48 + 74 * (SLOT[i] % 2), cellY(r) + CH / 2 + (Math.floor(SLOT[i] / 2) - (rows - 1) / 2) * 74];
};
const FLY_START = (i: number) => 150 + 6 * i;
const FLY_LEN = 20;

export const S09: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const popT = (i: number) => prog(frame, 4 + 4 * i, 18 + 4 * i);
  const capTrue = prog(frame, 32, 46);

  // stage 1
  const foundOp = (i: number) => prog(frame, 54 + 2 * i, 60 + 2 * i);
  const foundT = (i: number) => smooth(frame, 54 + 2 * i, 72 + 2 * i);
  const boxOp = prog(frame, 82, 98);
  const capFound = prog(frame, 84, 98);
  const ringP = prog(frame, 96, 104);

  // stage 2
  const t2 = smooth(frame, marks[1], marks[1] + 28);
  const g = mixGeom(BIG, SMALL, t2);
  const gridOp = prog(frame, 130, 146);
  const capNodes = prog(frame, 176, 192);
  const capsOut = 1 - prog(frame, marks[1], marks[1] + 10);
  const fly = (i: number) => smooth(frame, FLY_START(i), FLY_START(i) + FLY_LEN);
  const count = (r: number, c: number) => TRUTH8.filter((t, i) => t === r && FOUND8[i] === c && fly(i) >= 0.9).length;

  const capY = (y: number) => y - boxPad(g) - 80;

  return (
    <Frame n={9} title="Two splits of eight nodes">
      <Canvas>
        <EightRows
          g={g}
          trueOp={popT}
          foundOp={foundOp}
          foundT={foundT}
          boxOp={boxOp}
          ringFound={(i) => (i === 4 ? ringP : 0)}
        />

        {/* the table */}
        <g opacity={gridOp}>
          {[0, 1].map((c) => (
            <g key={c}>
              <rect x={cellX(c) + CW / 2 - 52} y={GY0 - 100} width={104} height={64} rx={20} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
              <text x={cellX(c) + CW / 2} y={GY0 - 53} textAnchor="middle" fontFamily={F.hand} fontSize={45} fill={C.ink}>
                {c === 0 ? 'A' : 'B'}
              </text>
            </g>
          ))}
          {[0, 1].map((r) => (
            <rect key={r} x={cellX(0) - 28} y={cellY(r)} width={16} height={CH} rx={8} fill={LOOK[r].fill} stroke="none" strokeWidth={0} />
          ))}
          {[0, 1].map((r) =>
            [0, 1].map((c) => {
              const n = count(r, c);
              return (
                <g key={`${r}${c}`}>
                  <rect x={cellX(c)} y={cellY(r)} width={CW} height={CH} rx={14} fill="none" stroke={C.faint} strokeWidth={4} />
                  <text x={cellX(c) + 262} y={cellY(r) + CH / 2 + 25} textAnchor="middle" fontFamily={F.serif} fontSize={72} fill={n > 0 ? C.ink : C.soft}>
                    {n}
                  </text>
                </g>
              );
            }),
          )}
        </g>

        {/* the flying copies */}
        {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
          if (frame < FLY_START(i)) return null;
          const p = fly(i);
          const [tx, ty] = target(i);
          const x0 = nodeX(SMALL, i);
          const y0 = SMALL.yFound;
          const cx = (x0 + tx) / 2;
          const cy = 560; // the arc runs in the gap between the two rows
          const q = 1 - p;
          return (
            <Disc
              key={i}
              x={q * q * x0 + 2 * q * p * cx + p * p * tx}
              y={q * q * y0 + 2 * q * p * cy + p * p * ty}
              d={SMALL.d}
              look={trueLook(i)}
              label={i + 1}
              ring={i === 4 ? 1 : 0}
            />
          );
        })}
      </Canvas>

      <Fade o={capTrue * capsOut} dy={14}>
        <Box x={rowCentre(g)} y={capY(g.yTrue)} w={600} align="center" size={45} color={C.soft} hand>
          true groups
        </Box>
      </Fade>
      <Fade o={capNodes} dy={14}>
        <Box x={cellX(0) + CW + GG / 2} y={GY0 + 2 * CH + GG + 40} w={700} align="center" size={45} color={C.soft} hand>
          nodes in each cell
        </Box>
      </Fade>
      <Fade o={capFound * capsOut} dy={14}>
        <Box x={rowCentre(g)} y={capY(g.yFound)} w={600} align="center" size={45} color={C.soft} hand>
          found groups
        </Box>
      </Fade>
    </Frame>
  );
};
