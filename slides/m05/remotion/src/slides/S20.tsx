import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box} from '../components/Text';
import {C, F} from '../theme';
import {LOOK, type Look} from '../lib/look';
import {betweenStages, prog, smooth} from '../lib/anim';
import {KARATE_EDGES, KARATE_FOUR, KARATE_POS, KARATE_REAL, KARATE_THREE} from '../data/data';
import {Network, mix, toCanvas} from '../lib/network';
import {ari, nmi} from '../lib/metrics';

/**
 * 0: the club drawn in its real split (blue: Mr. Hi's side, red: the Officer's side).
 * 1: the colours become the four groups (Q = 0.407); the table of real x found counts and the two scores appear.
 * 2: the colours become the three groups (Q = 0.402); a second table and its scores.
 * 3: the larger score of each pair in red: NMI prefers four groups, ARI prefers three.
 * 4: four groups against three groups: NMI 0.768, ARI 0.626.
 */
export const marks = [45, 105, 165, 210, 255];

// ---- numbers, all computed from the data
const f3 = (x: number) => x.toFixed(3);
type Table = number[][];
const table = (found: ReadonlyArray<number>, cols: number): Table =>
  [0, 1].map((r) => Array.from({length: cols}, (_, c) => KARATE_REAL.filter((v, i) => v === r && found[i] === c).length));
const T4 = table(KARATE_FOUR, 4);
const T3 = table(KARATE_THREE, 3);
const same = (a: number[][], b: number[][]) => JSON.stringify(a) === JSON.stringify(b);
if (!same(T4, [[11, 5, 1, 0], [0, 0, 9, 8]]) || !same(T3, [[11, 5, 1], [1, 0, 16]])) throw new Error(`S20: tables ${JSON.stringify(T4)} ${JSON.stringify(T3)}`);

const NMI4 = nmi(KARATE_REAL, KARATE_FOUR);
const ARI4 = ari(KARATE_REAL, KARATE_FOUR);
const NMI3 = nmi(KARATE_REAL, KARATE_THREE);
const ARI3 = ari(KARATE_REAL, KARATE_THREE);
const NMI43 = nmi(KARATE_FOUR, KARATE_THREE);
const ARI43 = ari(KARATE_FOUR, KARATE_THREE);
const expectScores: Array<[number, string]> = [
  [NMI4, '0.586'],
  [ARI4, '0.450'],
  [NMI3, '0.568'],
  [ARI3, '0.591'],
  [NMI43, '0.768'],
  [ARI43, '0.626'],
];
expectScores.forEach(([v, s]) => {
  if (f3(v) !== s) throw new Error(`S20: score ${v} should print as ${s}`);
});
// the larger of each pair is the one marked in red
const NMI_WINNER_IS_FOUR = NMI4 > NMI3;
const ARI_WINNER_IS_THREE = ARI3 > ARI4;
if (!NMI_WINNER_IS_FOUR || !ARI_WINNER_IS_THREE) throw new Error('S20: NMI and ARI no longer disagree');

// ---- the club
const CLUB = toCanvas(KARATE_POS, 150, 225, 720, 590);
const CLUB_EDGES = KARATE_EDGES as unknown as ReadonlyArray<readonly [number, number]>;
const NODE_D = 44;
// a group is told apart by its fill: solid, hollow, stripes, black (src/lib/look.ts)
const REAL_LOOK = KARATE_REAL.map((g) => LOOK[g]);
const FOUR_LOOK = KARATE_FOUR.map((g) => LOOK[g]);
const THREE_LOOK = KARATE_THREE.map((g) => LOOK[g]);

// ---- the tables on the right
const GX = 1010; // x of the row-header discs
const colX = (j: number) => 1130 + j * 100;
const BLOCK_A = 195;
const BLOCK_B = 480;
const BLOCK_C = 770;
const SCORE_X = 1540;

type BlockProps = {
  y0: number;
  t: Table;
  /** the looks of the found groups, in column order */
  cols: ReadonlyArray<Look>;
  o: number;
  cells: number;
};

/** A found group as a circle chip. */
const Chip: React.FC<{x: number; y: number; look: Look}> = ({x, y, look}) => (
  <circle cx={x} cy={y} r={NODE_D / 2 - look.sw / 2} fill={look.fill} stroke={look.stroke} strokeWidth={look.sw} />
);

/** A real group as a square chip: solid or hollow. */
const SquareChip: React.FC<{x: number; y: number; look: Look}> = ({x, y, look}) => {
  const h = 25;
  return <rect x={x - h + look.sw / 2} y={y - h + look.sw / 2} width={2 * h - look.sw} height={2 * h - look.sw} rx={6} fill={look.fill} stroke={look.stroke} strokeWidth={look.sw} />;
};

/** A 2 x k table of counts. Rows: the real split (square chips); columns: the found groups (circle chips, same fill as in the club). */
const BlockSvg: React.FC<BlockProps> = ({y0, t, cols, o, cells}) => {
  const yh = y0 + 100;
  const rows = [y0 + 160, y0 + 220];
  const right = colX(cols.length - 1) + 50;
  return (
    <g opacity={o}>
      {cols.map((c, j) => (
        <Chip key={j} x={colX(j)} y={yh} look={c} />
      ))}
      {[LOOK[0], LOOK[1]].map((l, r) => (
        <SquareChip key={r} x={GX} y={rows[r]} look={l} />
      ))}
      <line x1={GX + 40} y1={yh + 36} x2={right} y2={yh + 36} stroke={C.rule} strokeWidth={3} />
      {t.map((row, r) =>
        row.map((v, j) => {
          const k = r * cols.length + j;
          const a = prog(cells, k * 0.08, k * 0.08 + 0.4);
          return (
            <text key={`${r}-${j}`} x={colX(j)} y={rows[r] + 16} textAnchor="middle" fontFamily={F.serif} fontSize={45} fill={v === 0 ? C.soft : C.ink} opacity={a}>
              {v}
            </text>
          );
        }),
      )}
    </g>
  );
};

const Score: React.FC<{x: number; y: number; label: string; v: number; hot: number}> = ({x, y, label, v, hot}) => (
  <Box x={x} y={y} w={300} size={45} style={{color: mix(C.ink, C.red, hot), whiteSpace: 'nowrap'}}>
    {label} {f3(v)}
  </Box>
);

export const S20: React.FC = () => {
  const frame = useCurrentFrame();

  // the club's colours: real, then four groups, then three groups
  const t1 = smooth(frame, marks[0] + 6, marks[0] + 34);
  const t2 = smooth(frame, marks[1] + 6, marks[1] + 34);
  const clubFrom: ReadonlyArray<Look> = frame < marks[1] ? REAL_LOOK : FOUR_LOOK;
  const clubTo: ReadonlyArray<Look> = frame < marks[1] ? FOUR_LOOK : THREE_LOOK;
  const clubT = frame < marks[1] ? t1 : t2;
  const edgeIn = prog(frame, 0, 22);

  // captions under the club
  const cap0 = betweenStages(frame, marks, 0, 0);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = betweenStages(frame, marks, 2, 2);
  const cap3 = betweenStages(frame, marks, 3, 4);
  const legend = betweenStages(frame, marks, 0, 0);

  // stage 1: table A
  const aIn = prog(frame, 60, 76);
  const aCells = prog(frame, 70, 92);
  const aTitle = aIn;
  const aScores = prog(frame, 88, 102);

  // stage 2: table B
  const bIn = prog(frame, 124, 140);
  const bCells = prog(frame, 132, 152);
  const bScores = prog(frame, 148, 162);

  // stage 3: the higher of each pair in red
  const hot = prog(frame, 172, 192);

  // stage 4: four against three
  const cIn = prog(frame, 216, 234);
  const cScores = prog(frame, 230, 248);

  return (
    <Frame n={20} title="Which split is closer to the real one?">
      <Canvas>
        <Network
          pos={CLUB}
          edges={CLUB_EDGES}
          look={clubFrom}
          lookTo={clubTo}
          t={clubT}
          nodeD={NODE_D}
          edgeW={3}
          edgeOp={edgeIn}
          nodeOp={(i) => prog(frame, 2 + i * 0.5, 16 + i * 0.5)}
        />
        {/* legend of stage 0 */}
        <g opacity={legend * prog(frame, 22, 38)}>
          <Chip x={GX + 20} y={450} look={LOOK[0]} />
          <Chip x={GX + 20} y={540} look={LOOK[1]} />
        </g>
        <BlockSvg y0={BLOCK_A} t={T4} cols={[LOOK[0], LOOK[1], LOOK[2], LOOK[3]]} o={aIn} cells={aCells} />
        <BlockSvg y0={BLOCK_B} t={T3} cols={[LOOK[0], LOOK[1], LOOK[2]]} o={bIn} cells={bCells} />
      </Canvas>

      {/* captions under the club */}
      <Fade o={cap0}>
        <Box x={510} y={858} w={800} align="center" size={45} color={C.soft} hand>
          the real split
        </Box>
      </Fade>
      <Fade o={cap1}>
        <Box x={510} y={858} w={800} align="center" size={45} color={C.soft} hand>
          Q = 0.407
        </Box>
      </Fade>
      <Fade o={cap2}>
        <Box x={510} y={858} w={800} align="center" size={45} color={C.soft} hand>
          Q = 0.402
        </Box>
      </Fade>
      <Fade o={cap3}>
        <Box x={510} y={858} w={800} align="center" size={45} color={C.soft} hand>
          NMI and ARI can disagree
        </Box>
      </Fade>

      {/* stage 0: what blue and red mean */}
      <Fade o={legend * prog(frame, 22, 38)} dy={12}>
        <Box x={GX + 70} y={420} w={700} size={45}>
          Mr. Hi&apos;s side: 17
        </Box>
        <Box x={GX + 70} y={510} w={700} size={45}>
          the Officer&apos;s side: 17
        </Box>
      </Fade>

      {/* stage 1: four groups */}
      <Fade o={aTitle} dy={12}>
        <Box x={GX - 20} y={BLOCK_A} w={800} size={45} color={C.soft} hand>
          four groups
        </Box>
        <Box x={GX - 25} y={BLOCK_A + 70} w={120} size={40} color={C.soft} hand>
          real
        </Box>
      </Fade>
      <Fade o={aScores} dy={12}>
        <Score x={SCORE_X} y={BLOCK_A + 128} label="NMI" v={NMI4} hot={hot} />
        <Score x={SCORE_X} y={BLOCK_A + 190} label="ARI" v={ARI4} hot={0} />
      </Fade>

      {/* stage 2: three groups */}
      <Fade o={bIn} dy={12}>
        <Box x={GX - 20} y={BLOCK_B} w={800} size={45} color={C.soft} hand>
          three groups
        </Box>
        <Box x={GX - 25} y={BLOCK_B + 70} w={120} size={40} color={C.soft} hand>
          real
        </Box>
      </Fade>
      <Fade o={bScores} dy={12}>
        <Score x={SCORE_X} y={BLOCK_B + 128} label="NMI" v={NMI3} hot={0} />
        <Score x={SCORE_X} y={BLOCK_B + 190} label="ARI" v={ARI3} hot={hot} />
      </Fade>

      {/* stage 4: four against three */}
      <Fade o={cIn} dy={12}>
        <Box x={GX - 20} y={BLOCK_C} w={800} size={45} color={C.soft} hand>
          four vs three groups
        </Box>
      </Fade>
      <Fade o={cScores} dy={12}>
        <Box x={GX - 20} y={BLOCK_C + 68} w={760} size={45} style={{whiteSpace: 'nowrap'}}>
          NMI {f3(NMI43)}
          <span style={{display: 'inline-block', width: 60}} />
          ARI {f3(ARI43)}
        </Box>
      </Fade>
    </Frame>
  );
};
