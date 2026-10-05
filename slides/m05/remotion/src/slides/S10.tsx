import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {FOUND8, TRUTH8, choose2, pairCounts, randIndex} from '../lib/metrics';
import {EightRows, Frac, PairIcon, RowGeom, Verdict, nodeX} from '../lib/eight';

/**
 * 0: the two rows of S09, and "8 nodes make 28 pairs of nodes".
 * 1: the pair of nodes 1 and 2: together in both splits, so they agree.
 * 2: the pair of nodes 4 and 5: apart in the true split, together in the found split.
 * 3: all 28 pairs of nodes sort into four piles (together or apart in each split).
 * 4: Rand index = agreeing pairs of nodes / all pairs of nodes.
 */
export const marks = [40, 94, 154, 236, 292];

const G: RowGeom = {x0: 470, pitch: 140, d: 80, yTrue: 340, yFound: 640};
const N = TRUTH8.length;
const PAIRS = [
  [0, 1],
  [3, 4],
].map(([a, b]) => {
  const trueSame = TRUTH8[a] === TRUTH8[b];
  const foundSame = FOUND8[a] === FOUND8[b];
  return {a, b, trueSame, foundSame, agree: trueSame === foundSame, mid: (nodeX(G, a) + nodeX(G, b)) / 2};
});

// stage 3: the piles. Rows: together or apart in the true split. Columns: together or apart in the found split.
const PW = 620;
const PH = 200;
const PG = 20;
const PX0 = 430;
const PY0 = 290;
const pileX = (c: number) => PX0 + c * (PW + PG);
const pileY = (r: number) => PY0 + r * (PH + PG);
const CPX = 86; // chip pitch
const CPY = 46;
const CW_ = 78; // chip width (the icon of a pair)

const PC = pairCounts(TRUTH8, FOUND8);
const ALL = choose2(N);
const AGREE = PC.both + PC.neither;

const CHIPS = (() => {
  const used = [
    [0, 0],
    [0, 0],
  ];
  const out: {a: number; b: number; r: number; c: number; k: number; sx: number; sy: number}[] = [];
  let n = 0;
  for (let i = 0; i < N; i++) {
    for (let j = i + 1; j < N; j++) {
      const r = TRUTH8[i] === TRUTH8[j] ? 0 : 1;
      const c = FOUND8[i] === FOUND8[j] ? 0 : 1;
      const k = used[r][c]++;
      // where this chip waits: a 7 x 4 block below the piles
      const sx = PX0 + PW + PG / 2 + (n % 7 - 3) * CPX;
      const sy = 872 + (Math.floor(n / 7) - 1.5) * CPY;
      out.push({a: i, b: j, r, c, k, sx, sy});
      n++;
    }
  }
  return out;
})();
const PILE_N = (r: number, c: number) => CHIPS.filter((ch) => ch.r === r && ch.c === c).length;
const chipTarget = (ch: {r: number; c: number; k: number}): [number, number] => {
  const rows = Math.ceil(PILE_N(ch.r, ch.c) / 4);
  return [pileX(ch.c) + 36 + CW_ / 2 + CPX * (ch.k % 4), pileY(ch.r) + PH / 2 + (Math.floor(ch.k / 4) - (rows - 1) / 2) * CPY];
};
const CHIP_START = (n: number) => marks[2] + 20 + 1.3 * n;
const CHIP_LEN = 20;

export const S10: React.FC = () => {
  const frame = useCurrentFrame();

  // stages 0 to 2
  const rows = prog(frame, 0, 16) * (1 - prog(frame, marks[2], marks[2] + 12));
  const caps = prog(frame, 14, 30);
  // pair 1 shows in stage 1, pair 2 in stage 2
  const p1 = prog(frame, 44, 58) * (1 - prog(frame, marks[1], marks[1] + 12));
  const l1 = prog(frame, 58, 74) * (1 - prog(frame, marks[1], marks[1] + 12));
  const v1 = prog(frame, 74, 90) * (1 - prog(frame, marks[1], marks[1] + 12));
  const p2 = prog(frame, 106, 120) * (1 - prog(frame, marks[2], marks[2] + 12));
  const l2 = prog(frame, 120, 136) * (1 - prog(frame, marks[2], marks[2] + 12));
  const v2 = prog(frame, 136, 150) * (1 - prog(frame, marks[2], marks[2] + 12));
  const pp = [
    {p: p1, l: l1, v: v1},
    {p: p2, l: l2, v: v2},
  ];

  // stage 3
  const chipsIn = prog(frame, marks[2] + 8, marks[2] + 20);
  const frames = prog(frame, marks[2] + 16, marks[2] + 30);
  const heads = prog(frame, marks[2] + 26, marks[2] + 40);
  const landed = (n: number) => smooth(frame, CHIP_START(n), CHIP_START(n) + CHIP_LEN);
  const pileCount = (r: number, c: number) => CHIPS.filter((ch, n) => ch.r === r && ch.c === c && landed(n) >= 0.9).length;

  // stage 4
  const f1 = prog(frame, marks[3] + 2, marks[3] + 16);
  const f2 = prog(frame, marks[3] + 16, marks[3] + 30);
  const f3 = prog(frame, marks[3] + 30, marks[3] + 44);

  const under = (
    <g>
      {PAIRS.map((pr, k) => {
        const x1 = nodeX(G, pr.a);
        const x2 = lerp(x1, nodeX(G, pr.b), pp[k].p);
        return [G.yTrue, G.yFound].map((y) => (
          <line key={`${k}-${y}`} x1={x1} y1={y} x2={x2} y2={y} stroke={C.ink} strokeWidth={12} strokeLinecap="round" opacity={pp[k].p > 0.001 ? 1 : 0} />
        ));
      })}
    </g>
  );
  const ringOf = (i: number) => PAIRS.reduce((m, pr, k) => (i === pr.a || i === pr.b ? Math.max(m, pp[k].p) : m), 0);

  return (
    <Frame n={10} title="Rand index: pairs of nodes">
      {/* stages 0 to 2 */}
      <Canvas>
        <g opacity={rows}>
          <EightRows g={G} names={false} under={under} ringTrue={ringOf} ringFound={ringOf} />
        </g>
      </Canvas>
      <Fade o={rows}>
        <Box x={120} y={G.yTrue - 30} w={260} size={45} color={C.soft} hand>true</Box>
        <Box x={120} y={G.yFound - 30} w={260} size={45} color={C.soft} hand>found</Box>
      </Fade>
      <Fade o={rows * caps} dy={16}>
        <Box x={960} y={850} w={1400} align="center" size={45}>
          {N} nodes make {ALL} pairs of nodes
        </Box>
      </Fade>
      {PAIRS.map((pr, k) => (
        <React.Fragment key={k}>
          <Fade o={pp[k].l} dy={12}>
            <Box x={pr.mid} y={G.yTrue - 40 - 12 - 61} w={520} align="center" size={45} hand>
              {pr.trueSame ? 'together' : 'apart'}
            </Box>
            <Box x={pr.mid} y={G.yFound + 56 + 10} w={520} align="center" size={45} hand>
              {pr.foundSame ? 'together' : 'apart'}
            </Box>
          </Fade>
          <Fade o={pp[k].v} dy={12}>
            <Verdict x={pr.mid} y={452} agree={pr.agree} />
          </Fade>
        </React.Fragment>
      ))}

      {/* stage 3: the piles, each pair of nodes drawn as two nodes joined by a line */}
      <Canvas>
        <g opacity={frames}>
          {[0, 1].map((r) =>
            [0, 1].map((c) => <rect key={`${r}${c}`} x={pileX(c)} y={pileY(r)} width={PW} height={PH} rx={14} fill="none" stroke={C.faint} strokeWidth={4} />),
          )}
        </g>
        {CHIPS.map((ch, n) => {
          const [tx, ty] = chipTarget(ch);
          const p = landed(n);
          return (
            <g key={n} opacity={chipsIn}>
              <PairIcon x={lerp(ch.sx, tx, p)} y={lerp(ch.sy, ty, p)} a={ch.a} b={ch.b} d={32} gap={46} />
            </g>
          );
        })}
        <g opacity={heads}>
          {[0, 1].map((r) =>
            [0, 1].map((c) => (
              <text key={`${r}${c}`} x={pileX(c) + 500} y={pileY(r) + 92} textAnchor="middle" fontFamily={F.serif} fontSize={72} fill={C.ink}>
                {pileCount(r, c)}
              </text>
            )),
          )}
        </g>
      </Canvas>
      <Fade o={heads} dy={12}>
        {['found: together', 'found: apart'].map((t, c) => (
          <Box key={t} x={pileX(c) + PW / 2} y={206} w={PW} align="center" size={45} color={C.soft} hand>
            {t}
          </Box>
        ))}
        {['true: together', 'true: apart'].map((t, r) => (
          <Box key={t} x={PX0 - 20} y={pileY(r) + PH / 2 - 42} w={190} align="right" size={45} color={C.soft} hand style={{lineHeight: 1.05}}>
            {t.split(': ').map((s, j) => (
              <div key={j}>{s + (j === 0 ? ':' : '')}</div>
            ))}
          </Box>
        ))}
        {[0, 1].map((r) =>
          [0, 1].map((c) => <Verdict key={`${r}${c}`} x={pileX(c) + 500} y={pileY(r) + 124} agree={r === c} size={36} />),
        )}
      </Fade>

      {/* stage 4: the formula */}
      <Fade o={f1} dy={14}>
        <div style={{position: 'absolute', left: 0, width: 1920, top: 790, display: 'flex', justifyContent: 'center'}}>
          <div
            style={{
              background: C.panel,
              padding: '12px 44px 14px',
              display: 'flex',
              alignItems: 'center',
              gap: 20,
              fontSize: 45,
              fontFamily: F.serif,
              whiteSpace: 'nowrap',
            }}
          >
            <span>
              <Term>Rand index</Term> = <Frac top="agreeing pairs of nodes" bottom="all pairs of nodes" />
            </span>
            <span style={{opacity: f2}}>
              = <Frac top={`${PC.both} + ${PC.neither}`} bottom={ALL} />
            </span>
            <span style={{opacity: f3}}>= {randIndex(TRUTH8, FOUND8).toFixed(2)}</span>
          </div>
        </div>
      </Fade>
    </Frame>
  );
};
