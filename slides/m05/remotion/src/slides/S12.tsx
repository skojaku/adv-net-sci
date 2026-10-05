import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag, Term} from '../components/Text';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {clamp, lerp} from '../lib/plot';
import {EXPECTED_RAND, SHUFFLES, SHUFFLE_RAND} from '../data/data';
import {NDOT, NodeDot, dotCentre} from '../lib/dots30';
import {FOUND8, TRUTH8, ari, choose2, expectedRand, randIndex} from '../lib/metrics';
import {EightRows, Frac, RowGeom} from '../lib/eight';

/**
 * 0: the 40 shuffles replay; each Rand index drops as a dot on a 0 to 1 number line and stacks.
 * 1: why they sit near 0.71: most pairs of nodes are apart in both splits.
 * 2: ARI = (Rand - expected Rand) / (1 - expected Rand); the axis becomes ARI and the dots slide to it.
 * 3: back to the eight nodes: Rand 0.75, expected 0.51, ARI 0.49.
 */
export const marks = [92, 134, 216, 288];

const E = EXPECTED_RAND;

// the number line
const AX0 = 200;
const AX1 = 1720;
const AXY = 900;
const KR = AX1 - AX0; // px per unit of Rand index (axis 0 to 1)
const KA = KR / 1.5; // px per unit of ARI (axis -0.5 to 1)
const xRand = (r: number) => AX0 + r * KR;
const xAri = (a: number) => AX1 - (1 - a) * KA;
const BIN = 26; // a bin is as wide as a dot, so dots in one column stack and never overlap
const DOT_D = 22;
const DOT_STEP = 23;

const NS = SHUFFLE_RAND.length;
const BIN_OF = SHUFFLE_RAND.map((v) => Math.floor((v * KR) / BIN));
const DOTS = SHUFFLE_RAND.map((_, k) => {
  const b = BIN_OF[k];
  const rc = ((b + 0.5) * BIN) / KR; // the Rand index at the centre of the bin
  const stack = BIN_OF.slice(0, k).filter((x) => x === b).length;
  return {x0: xRand(rc), x1: xAri((rc - E) / (1 - E)), y: AXY - 14 - stack * DOT_STEP};
});

// replay: shuffle k starts at S(k); the replay gets faster
const S = (k: number) => 4 + 62 * Math.pow(k / NS, 0.75);
const FALL = 12;
const FALL_FROM = 410;

// the mini picture of the 30 dots
const MX0 = 140;
const MY0 = 292;
const MPITCH = 46;
const MSTRIDE = 152;

// stage 3
const G3: RowGeom = {x0: 540, pitch: 120, d: 70, yTrue: 350, yFound: 550};

const PAIRS_ALL = choose2(NDOT);
const PAIRS_APART = PAIRS_ALL - 5 * choose2(6);
const R8 = randIndex(TRUTH8, FOUND8);
const E8 = expectedRand(TRUTH8, FOUND8);
const A8 = ari(TRUTH8, FOUND8);

export const S12: React.FC = () => {
  const frame = useCurrentFrame();
  const out = 1 - prog(frame, marks[2], marks[2] + 10); // everything of stages 0 to 2 leaves

  // stage 0
  let cur = 0;
  for (let k = 0; k < NS; k++) if (S(k) <= frame) cur = k;
  const cap0 = prog(frame, 70, 86);

  // stage 1
  const cap1 = prog(frame, 96, 114);
  const capsGone = 1 - prog(frame, marks[1], marks[1] + 10);

  // stage 2
  const form = prog(frame, 138, 156);
  const expl = prog(frame, 148, 164);
  const dash = prog(frame, 156, 166);
  const m = smooth(frame, 170, 204);
  const cap2 = prog(frame, 200, 214);

  // stage 3
  const s3 = prog(frame, marks[2] + 8, marks[2] + 24);
  const t1 = prog(frame, marks[2] + 26, marks[2] + 40);
  const t2 = prog(frame, marks[2] + 38, marks[2] + 52);
  const t3 = prog(frame, marks[2] + 50, marks[2] + 64);

  const randTicks = [0, 0.25, 0.5, 0.75, 1];
  const ariTicks = [-0.5, 0, 0.5, 1];
  const fmt = (v: number) => (v < 0 ? '−' : '') + Math.abs(v).toString();

  return (
    <Frame n={12} title="Adjusted Rand index">
      {/* stages 0 to 2 */}
      <Canvas>
        <g opacity={out}>
          {/* the 30 dots, recoloured by each shuffle */}
          {[...Array(NDOT).keys()].map((i) => {
            const [x, y] = dotCentre(i, MX0, MY0, MPITCH, MSTRIDE);
            return <NodeDot key={i} x={x} y={y} d={40} g={SHUFFLES[cur][i]} />;
          })}
          {/* the axis */}
          <line x1={AX0} y1={AXY} x2={AX1 + 14} y2={AXY} stroke={C.soft} strokeWidth={3} />
          <g opacity={1 - m}>
            {randTicks.map((r) => (
              <g key={r}>
                <line x1={xRand(r)} y1={AXY} x2={xRand(r)} y2={AXY + 10} stroke={C.soft} strokeWidth={3} />
                <text x={xRand(r)} y={AXY + 52} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>
                  {fmt(r)}
                </text>
              </g>
            ))}
          </g>
          <g opacity={m}>
            {ariTicks.map((a) => (
              <g key={a}>
                <line x1={xAri(a)} y1={AXY} x2={xAri(a)} y2={AXY + 10} stroke={C.soft} strokeWidth={3} />
                <text x={xAri(a)} y={AXY + 52} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>
                  {fmt(a)}
                </text>
              </g>
            ))}
          </g>
          {/* expected Rand: the line the dots are measured from */}
          <g opacity={dash}>
            <line
              x1={lerp(xRand(E), xAri(0), m)}
              y1={AXY}
              x2={lerp(xRand(E), xAri(0), m)}
              y2={518}
              stroke={C.ink}
              strokeWidth={3}
              strokeDasharray="10 8"
            />
          </g>
          {/* one dot per shuffle */}
          {DOTS.map((d, k) => {
            if (frame < S(k)) return null;
            const p = clamp((frame - S(k)) / FALL, 0, 1);
            const x = lerp(d.x0, d.x1, m);
            const y = lerp(FALL_FROM, d.y, p * p);
            return <circle key={k} cx={x} cy={y} r={DOT_D / 2} fill={C.blue} stroke="#fff" strokeWidth={2} opacity={clamp((frame - S(k)) / 3, 0, 1)} />;
          })}
        </g>
      </Canvas>
      <Fade o={out * (1 - m)}>
        <Box x={AX0} y={826} w={800} size={45} color={C.soft} hand>
          Rand index, one dot per shuffle
        </Box>
      </Fade>
      <Fade o={out * m}>
        <Box x={AX1} y={826} w={800} align="right" size={45} color={C.soft} hand>
          ARI, one dot per shuffle
        </Box>
      </Fade>
      <Fade o={out * cap0 * capsGone} dy={14}>
        <Box x={200} y={470} w={900} size={45} color={C.soft} hand>
          Random labels: about 0.71
        </Box>
      </Fade>
      <Fade o={out * cap1 * capsGone} dy={14}>
        <Box x={200} y={556} w={900} size={45} color={C.soft} hand>
          Most pairs of nodes are apart in both splits: {PAIRS_APART} of {PAIRS_ALL}.
        </Box>
      </Fade>

      {/* stage 2 */}
      <Fade o={out * form} dy={14}>
        <div style={{position: 'absolute', left: 930, top: 290, background: C.panel, padding: '16px 34px 18px', fontSize: 45, fontFamily: F.serif, display: 'flex', alignItems: 'center', gap: 16, whiteSpace: 'nowrap'}}>
          <Term>ARI</Term> =
          <Frac top="Rand − expected Rand" bottom="1 − expected Rand" />
        </div>
      </Fade>
      <Fade o={out * expl} dy={14}>
        <Box x={930} y={458} w={820} size={45}>expected Rand = {E.toFixed(3)}</Box>
      </Fade>
      <Fade o={out * cap2} dy={14}>
        <Box x={930} y={580} w={820} size={45} color={C.soft} hand>
          0 = chance, 1 = identical
        </Box>
      </Fade>

      {/* stage 3: back to the eight nodes */}
      <Canvas>
        <g opacity={s3}>
          <EightRows g={G3} names={false} />
        </g>
      </Canvas>
      <Fade o={t1} dy={16}>
        <Tag x={430} y={760}>Rand {R8.toFixed(2)}</Tag>
      </Fade>
      <Fade o={t2} dy={16}>
        <Tag x={960} y={760}>expected {E8.toFixed(2)}</Tag>
      </Fade>
      <Fade o={t3} dy={16}>
        <Tag x={1470} y={760} hot>ARI {A8.toFixed(2)}</Tag>
      </Fade>
    </Frame>
  );
};
