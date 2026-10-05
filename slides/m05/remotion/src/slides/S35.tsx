import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {C} from '../theme';
import {LOOK} from '../lib/look';
import {fromStage, prog} from '../lib/anim';
import {KARATE_EDGES, KARATE_POS, KARATE_REAL} from '../data/data';
import {Network, toCanvas} from '../lib/network';

/**
 * The punchline. Fitted to the karate club, graph-tool's Bayesian SBM (degree-corrected, the shortest description)
 * returns ONE group (Peixoto 2019; the graph-tool mailing list, "Inference for the karate network"): the two groups we
 * have looked at all along are no stronger than what a random network with the same degrees gives.
 * 0: the club in its real split, the groups so far.
 * 1: the same club in graph-tool's answer: one group.
 * 2: the punchline.
 */
export const marks = [50, 108, 164];

const POS_L = toCanvas(KARATE_POS, 135, 285, 750, 540);
const POS_R = toCanvas(KARATE_POS, 1035, 285, 750, 540);
const EDGES = KARATE_EDGES as unknown as ReadonlyArray<readonly [number, number]>;
const REAL = KARATE_REAL.map((g) => LOOK[g]);
const ONE = KARATE_REAL.map(() => LOOK[0]);

export const S35: React.FC = () => {
  const frame = useCurrentFrame();

  const left = (i: number) => prog(frame, 0.4 * i, 0.4 * i + 12);
  const right = (i: number) => prog(frame, marks[0] + 2 + 0.4 * i, marks[0] + 2 + 0.4 * i + 12);
  const edgeL = (i: number) => prog(frame, 6 + 0.28 * i, 6 + 0.28 * i + 10);
  const edgeR = (i: number) => prog(frame, marks[0] + 8 + 0.28 * i, marks[0] + 8 + 0.28 * i + 10);
  const capL = prog(frame, 18, 36);
  const capR = prog(frame, marks[0] + 18, marks[0] + 36);
  const punch = fromStage(frame, marks, 2, 16);

  return (
    <Frame n={35} title="The karate club, once more">
      <Canvas>
        <Network pos={POS_L} edges={EDGES} look={REAL} nodeD={40} edgeW={2.5} nodeOp={left} edgeOp={edgeL} />
        <Network pos={POS_R} edges={EDGES} look={ONE} nodeD={40} edgeW={2.5} nodeOp={right} edgeOp={edgeR} />
        <line x1={960} y1={285} x2={960} y2={830} stroke={C.rule} strokeWidth={3} opacity={prog(frame, marks[0], marks[0] + 12)} />
      </Canvas>
      <Fade o={capL} dy={14}>
        <Cap x={510} y={212} w={800}>the groups so far</Cap>
      </Fade>
      <Fade o={capR} dy={14}>
        <Cap x={1410} y={212} w={800}>graph-tool: 1 group</Cap>
      </Fade>
      <Fade o={punch} dy={14}>
        <Box x={960} y={860} w={1680} align="center" size={50}>
          The two groups are no stronger than in a random network.
        </Box>
        <Cap x={960} y={940} w={1680}>degree-corrected SBM, the shortest description</Cap>
      </Fade>
    </Frame>
  );
};
