import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {fromStage, prog} from '../lib/anim';
import {HOLLOW} from '../lib/look';
import {Network} from '../lib/network';
import {CLUB_L} from '../lib/club';
import {EDGES, REAL_LOOKS} from '../lib/a_club';

/**
 * The karate club.
 * 0: nodes, then edges.
 * 1: the nodes take the two colours of the real split; the question (no answer).
 */
export const marks = [84, 140];

export const S01: React.FC = () => {
  const frame = useCurrentFrame();

  const node = (i: number) => prog(frame, 0.4 * i, 0.4 * i + 12);
  const edge = (i: number) => prog(frame, 14 + 0.3 * i, 14 + 0.3 * i + 12);
  const cap = prog(frame, 50, 70);
  const colour = prog(frame, marks[0] + 4, marks[0] + 30);
  const question = fromStage(frame, marks, 1, 16);

  return (
    <Frame n={1} zoom={1.07}>
      <Canvas>
        <Network
          pos={CLUB_L}
          edges={EDGES}
          look={HOLLOW}
          lookTo={REAL_LOOKS}
          t={colour}
          nodeD={46}
          nodeOp={(i) => node(i)}
          edgeOp={(i) => edge(i)}
        />
      </Canvas>
      <div style={{opacity: cap}}>
        <Cap x={530} y={872}>34 nodes, 78 edges</Cap>
      </div>
      <div style={{opacity: question, transform: `translateY(${(1 - question) * 14}px)`}}>
        <Box x={1010} y={440} w={780} size={56}>Is each colour a strong community?</Box>
      </div>
    </Frame>
  );
};
