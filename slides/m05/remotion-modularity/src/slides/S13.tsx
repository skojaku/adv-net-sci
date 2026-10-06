import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {HOLLOW, LOOK, type Look} from '../lib/look';
import {Network, toCanvas} from '../lib/network';
import {prog, stageStart} from '../lib/anim';
import {q3} from '../lib/club';
import {FINAL, KARATE_EDGES, KARATE_POS, KARATE_REAL, Q_ONE, Q_REAL, Q_FINAL, Q_SINGLES} from '../data/data';

/**
 * Four partitions of the karate club side by side, one per stage, each with its Q.
 * 0: everyone alone (34 groups, Q = -0.050).  1: everyone together (1 group, Q = 0.000).
 * 2: the two real factions (Q = 0.358).        3: four groups (Q = 0.420).
 * 4: the number of groups is not an input.
 */
export const marks = [52, 102, 152, 202, 252];

const EDGES = KARATE_EDGES as unknown as ReadonlyArray<readonly [number, number]>;
const PW = 380;
const PX = [140, 560, 980, 1400];
const PY = 340;
const PH = 300;
const POS = PX.map((x) => toCanvas(KARATE_POS, x, PY, PW, PH));

type Panel = {label: string; q: number; look: ReadonlyArray<Look>; hot?: boolean};
const PANELS: ReadonlyArray<Panel> = [
  {label: '34 groups', q: Q_SINGLES, look: KARATE_REAL.map(() => HOLLOW)},
  {label: '1 group', q: Q_ONE, look: KARATE_REAL.map(() => LOOK[0])},
  {label: '2 groups', q: Q_REAL, look: KARATE_REAL.map((g) => LOOK[g])},
  {label: '4 groups', q: Q_FINAL, look: FINAL.map((g) => LOOK[g]), hot: true},
];

export const S13: React.FC = () => {
  const frame = useCurrentFrame();
  const say = prog(frame, stageStart(marks, 4) + 6, stageStart(marks, 4) + 28);

  return (
    <Frame n={13} top={190}>
      <Canvas>
        {PANELS.map((p, k) => {
          const s = stageStart(marks, k);
          const node = (i: number) => prog(frame, s + 2 + 0.35 * i, s + 14 + 0.35 * i);
          const edge = (i: number) => prog(frame, s + 6 + 0.25 * i, s + 16 + 0.25 * i);
          return (
            <Network key={k} pos={POS[k]} edges={EDGES} look={p.look} nodeD={24} edgeW={2.4} nodeOp={(i) => node(i)} edgeOp={(i) => edge(i)} />
          );
        })}
      </Canvas>
      {PANELS.map((p, k) => {
        const s = stageStart(marks, k);
        const lab = prog(frame, s + 4, s + 22);
        const tag = prog(frame, s + 26, s + 42);
        return (
          <React.Fragment key={k}>
            <Fade o={lab} dy={12}>
              <Box x={PX[k] + PW / 2} y={PY - 90} w={PW} align="center" size={46}>{p.label}</Box>
            </Fade>
            <Fade o={tag} dy={12}>
              <Tag x={PX[k] + PW / 2} y={PY + PH + 50} hot={p.hot}>Q = {q3(p.q)}</Tag>
            </Fade>
          </React.Fragment>
        );
      })}
      <Fade o={say} dy={14}>
        <Box x={960} y={PY + PH + 170} w={1600} align="center" size={46}>
          We did not choose the number of groups. Maximizing Q chooses it.
        </Box>
      </Fade>
    </Frame>
  );
};
