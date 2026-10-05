import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {KARATE_EDGES, KARATE_FOUR, KARATE_POS, KARATE_REAL, KARATE_THREE} from '../data/data';
import {Network, toCanvas} from '../lib/network';
import {ari, nmi} from '../lib/metrics';

/**
 * Three drawings of the same club, side by side, so the splits can be compared by eye:
 * 0: the real split (Mr. Hi's side and the Officer's side).
 * 1: the four-group split (Q = 0.407) and its two scores against the real split.
 * 2: the three-group split (Q = 0.402) and its scores.
 * 3: the larger score of each pair in red: NMI prefers four groups, ARI prefers three.
 * 4: the two found splits against each other: NMI 0.768, ARI 0.626.
 * The colours of one drawing mean nothing in another: a group's name is arbitrary.
 */
export const marks = [50, 105, 160, 210, 260];

// ---- numbers, all computed from the data
const f3 = (x: number) => x.toFixed(3);
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
  if (f3(v) !== s) throw new Error(`S21: score ${v} should print as ${s}`);
});
if (!(NMI4 > NMI3) || !(ARI3 > ARI4)) throw new Error('S21: NMI and ARI no longer disagree');

// ---- the three drawings
const SLOT_W = 540;
const SLOT_X = [120, 690, 1260];
const TOP = 232;
const SLOT_H = 440;
const CAP_Y = 692;
const CLUBS = SLOT_X.map((x) => toCanvas(KARATE_POS, x + 15, TOP + 15, SLOT_W - 30, SLOT_H - 30));
const EDGES = KARATE_EDGES as unknown as ReadonlyArray<readonly [number, number]>;
const D = 30;
const LOOKS = [KARATE_REAL.map((g) => LOOK[g]), KARATE_FOUR.map((g) => LOOK[g]), KARATE_THREE.map((g) => LOOK[g])];
const CX = SLOT_X.map((x) => x + SLOT_W / 2);

const RedNum: React.FC<{hot: number; children: React.ReactNode}> = ({hot, children}) => (
  <span style={{color: hot > 0.5 ? C.red : C.ink, fontWeight: hot > 0.5 ? 700 : 400}}>{children}</span>
);

export const S21: React.FC = () => {
  const frame = useCurrentFrame();

  const club = (n: number, start: number) => prog(frame, start, start + 16);
  const realIn = club(0, 0);
  const fourIn = club(1, marks[0] + 2);
  const threeIn = club(2, marks[1] + 2);
  const nodeIn = (start: number) => (i: number) => prog(frame, start + i * 0.5, start + 14 + i * 0.5);

  const capReal = prog(frame, 22, 38);
  const capFour = prog(frame, marks[0] + 18, marks[0] + 34);
  const scoreFour = prog(frame, marks[0] + 32, marks[0] + 46);
  const capThree = prog(frame, marks[1] + 18, marks[1] + 34);
  const scoreThree = prog(frame, marks[1] + 32, marks[1] + 46);
  const hot = prog(frame, marks[2] + 10, marks[2] + 26);
  const note = betweenStages(frame, marks, 3, 3);
  const vs = fromStage(frame, marks, 4, 16);

  return (
    <Frame n={21} title="Which split is closer to the real one?">
      <Canvas>
        <Network pos={CLUBS[0]} edges={EDGES} look={LOOKS[0]} nodeD={D} edgeW={2.5} opacity={realIn} nodeOp={nodeIn(0)} />
        <Network pos={CLUBS[1]} edges={EDGES} look={LOOKS[1]} nodeD={D} edgeW={2.5} opacity={fourIn} nodeOp={nodeIn(marks[0] + 2)} />
        <Network pos={CLUBS[2]} edges={EDGES} look={LOOKS[2]} nodeD={D} edgeW={2.5} opacity={threeIn} nodeOp={nodeIn(marks[1] + 2)} />
        {/* the key to the real split */}
        <g opacity={capReal}>
          <circle cx={CX[0] - 120} cy={CAP_Y + 128} r={15} fill={LOOK[0].fill} />
          <circle cx={CX[0] - 120} cy={CAP_Y + 178} r={15} fill={LOOK[1].fill} />
        </g>
        {/* a thin rule between the real split and the found ones */}
        <line x1={675} y1={TOP} x2={675} y2={CAP_Y + 230} stroke={C.rule} strokeWidth={3} opacity={fourIn} />
      </Canvas>

      {/* captions under each drawing */}
      <Fade o={capReal} dy={12}>
        <Cap x={CX[0]} y={CAP_Y} w={SLOT_W}>the real split</Cap>
        <Box x={CX[0] - 90} y={CAP_Y + 100} w={420} size={36}>
          Mr. Hi&apos;s side: 17
        </Box>
        <Box x={CX[0] - 90} y={CAP_Y + 150} w={420} size={36}>
          the Officer&apos;s side: 17
        </Box>
      </Fade>
      <Fade o={capFour} dy={12}>
        <Cap x={CX[1]} y={CAP_Y} w={SLOT_W}>four groups, Q = 0.407</Cap>
      </Fade>
      <Fade o={scoreFour} dy={12}>
        <Box x={CX[1]} y={CAP_Y + 90} w={SLOT_W} align="center" size={45}>
          <RedNum hot={hot}>NMI {f3(NMI4)}</RedNum>
        </Box>
        <Box x={CX[1]} y={CAP_Y + 150} w={SLOT_W} align="center" size={45}>
          ARI {f3(ARI4)}
        </Box>
      </Fade>
      <Fade o={capThree} dy={12}>
        <Cap x={CX[2]} y={CAP_Y} w={SLOT_W}>three groups, Q = 0.402</Cap>
      </Fade>
      <Fade o={scoreThree} dy={12}>
        <Box x={CX[2]} y={CAP_Y + 90} w={SLOT_W} align="center" size={45}>
          NMI {f3(NMI3)}
        </Box>
        <Box x={CX[2]} y={CAP_Y + 150} w={SLOT_W} align="center" size={45}>
          <RedNum hot={hot}>ARI {f3(ARI3)}</RedNum>
        </Box>
      </Fade>

      {/* stage 3 and 4 */}
      <Fade o={note} dy={12}>
        <Cap x={CX[1] + 285} y={CAP_Y + 235} w={1200}>
          NMI and ARI can disagree
        </Cap>
      </Fade>
      <Fade o={vs} dy={12}>
        <Box x={CX[1] + 285} y={CAP_Y + 225} w={1300} align="center" size={45} style={{fontFamily: F.serif}}>
          four vs three groups: NMI {f3(NMI43)}, ARI {f3(ARI43)}
        </Box>
      </Fade>
    </Frame>
  );
};
