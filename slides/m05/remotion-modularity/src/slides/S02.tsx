import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, FadeG} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {C} from '../theme';
import {prog} from '../lib/anim';
import {LOOK} from '../lib/look';
import {Network} from '../lib/network';
import {BETWEEN, INSIDE} from '../data/data';
import {CLUB_L} from '../lib/club';
import {CountRow, EDGES, FRAC_Y, Fraction, Legend, PANEL_W, PANEL_X, REAL_B, REAL_LOOKS, ROW1_Y, ROW2_Y, clubEdges} from '../lib/a_club';

/**
 * Opens on the picture S01 ends with (same club, same colours).
 * 0: edges inside a group take the group's colour and get thick; edges between groups fade.
 * 1: the counts, and the fraction of edges inside.
 * 2: one edge inside and one between, with rings; the sentence.
 */
export const marks = [54, 120, 196];

// the two edges that get a ring: both ends blue (inside), and a blue end with an orange end (between)
const SAME: [number, number] = [4, 10];
const DIFF: [number, number] = [1, 30];

const SAMPLE_Y = 612;

export const S02: React.FC = () => {
  const frame = useCurrentFrame();

  const p = prog(frame, 6, 44);
  const rows = prog(frame, marks[0] + 4, marks[0] + 22);
  const rows2 = prog(frame, marks[0] + 14, marks[0] + 32);
  const frac = prog(frame, marks[0] + 30, marks[0] + 50);
  const note = prog(frame, marks[0] + 44, marks[0] + 62);
  const ringO = prog(frame, marks[1] + 4, marks[1] + 24);
  const samples = prog(frame, marks[1] + 14, marks[1] + 34);
  const sentence = prog(frame, marks[1] + 28, marks[1] + 50);

  const edgeProps = clubEdges(REAL_B, p);
  const a = CLUB_L[SAME[0]];
  const b = CLUB_L[SAME[1]];
  const c = CLUB_L[DIFF[0]];
  const d = CLUB_L[DIFF[1]];

  return (
    <Frame n={2} zoom={1.07}>
      <Canvas>
        <Network pos={CLUB_L} edges={EDGES} look={REAL_LOOKS} nodeD={46} {...edgeProps} />
        <FadeG o={ringO}>
          <line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={C.ink} strokeWidth={11} strokeLinecap="round" />
          <line x1={c[0]} y1={c[1]} x2={d[0]} y2={d[1]} stroke={C.ink} strokeWidth={11} strokeLinecap="round" />
          {[a, b, c, d].map((q, k) => (
            <g key={k}>
              <circle cx={q[0]} cy={q[1]} r={21.5} fill={k === 3 ? LOOK[1].fill : LOOK[0].fill} stroke="#fff" strokeWidth={3} />
              <circle cx={q[0]} cy={q[1]} r={31} fill="none" stroke={C.ink} strokeWidth={6} />
            </g>
          ))}
        </FadeG>
        <FadeG o={samples}>
          <line x1={PANEL_X + 20} y1={SAMPLE_Y + 30} x2={PANEL_X + 100} y2={SAMPLE_Y + 30} stroke={C.ink} strokeWidth={7} />
          <circle cx={PANEL_X + 20} cy={SAMPLE_Y + 30} r={19} fill={LOOK[0].fill} stroke="#fff" strokeWidth={3} />
          <circle cx={PANEL_X + 100} cy={SAMPLE_Y + 30} r={19} fill={LOOK[0].fill} stroke="#fff" strokeWidth={3} />
          <line x1={PANEL_X + 20} y1={SAMPLE_Y + 100} x2={PANEL_X + 100} y2={SAMPLE_Y + 100} stroke={C.ink} strokeWidth={7} />
          <circle cx={PANEL_X + 20} cy={SAMPLE_Y + 100} r={19} fill={LOOK[0].fill} stroke="#fff" strokeWidth={3} />
          <circle cx={PANEL_X + 100} cy={SAMPLE_Y + 100} r={19} fill={LOOK[1].fill} stroke="#fff" strokeWidth={3} />
        </FadeG>
        <Legend o1={rows} o2={rows2} />
      </Canvas>
      <div style={{opacity: samples}}>
        <Cap x={PANEL_X + 150} y={SAMPLE_Y} w={620} align="left">same colour</Cap>
        <Cap x={PANEL_X + 150} y={SAMPLE_Y + 70} w={620} align="left">different colours</Cap>
      </div>
      <CountRow y={ROW1_Y} label="inside" n={INSIDE} o={rows} />
      <CountRow y={ROW2_Y} label="between" n={BETWEEN} o={rows2} />
      <Fraction inside={INSIDE} m={78} value="0.859" o={frac} />
      <div style={{opacity: note}}>
        <Cap x={PANEL_X + 500} y={FRAC_Y + 62} w={300} align="left">M = 78 edges</Cap>
      </div>
      <div style={{opacity: sentence, transform: `translateY(${(1 - sentence) * 14}px)`}}>
        <Box x={PANEL_X} y={SAMPLE_Y + 150} w={PANEL_W} size={40}>
          Pick one edge at random. Its two ends have the same colour with probability 0.859.
        </Box>
      </div>
    </Frame>
  );
};
