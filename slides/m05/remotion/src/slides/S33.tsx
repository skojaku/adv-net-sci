import React from 'react';
import {Img, useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap} from '../components/Text';
import {C} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import plainPng from '../assets/dcsbm-plain.png';

/**
 * Why the SBM needs a correction: the political blogs (Karrer and Newman 2011, Fig. 2a).
 * The picture is theirs: the largest component of the network of links between blogs about US politics (Adamic and Glance),
 * two groups found by the plain SBM, node size = degree.
 * 0: the picture and the question: what separates the two groups? (no answer on the slide)
 * 1: the answer: blue = the high-degree blogs, yellow = the others; the groups follow degree, not politics.
 * The two colours are those of the picture (blue #3880E5, yellow #E6E679).
 */
export const marks = [64, 124];

const IMG_X = 120;
const IMG_Y = 250;
const IMG_W = 860;
const IMG_H = Math.round((IMG_W * 636) / 818);
const RX = 1060;
const BLUE = '#3880E5';
const YELLOW = '#E6E679';

export const S33: React.FC = () => {
  const frame = useCurrentFrame();

  const img = prog(frame, 0, 24);
  const head = prog(frame, 16, 34);
  const note = prog(frame, 30, 46);
  const ask = betweenStages(frame, marks, 0, 0) * prog(frame, 40, 58);
  const legend1 = fromStage(frame, marks, 1, 16);
  const legend2 = prog(frame, marks[0] + 14, marks[0] + 30);
  const answer = prog(frame, marks[0] + 34, marks[0] + 52);

  return (
    <Frame n={33}>
      <Fade o={img}>
        <Img src={plainPng} style={{position: 'absolute', left: IMG_X, top: IMG_Y, width: IMG_W, height: IMG_H}} />
      </Fade>
      <Fade o={head} dy={14}>
        <Box x={RX} y={270} w={740} size={50}>
          Political blogs, split in two by a plain SBM
        </Box>
      </Fade>
      <Fade o={note} dy={12}>
        <Cap x={RX} y={440} w={740} align="left">node size: degree</Cap>
      </Fade>
      <Fade o={ask} dy={14}>
        <Box x={RX} y={600} w={740} size={50}>
          What separates the two groups?
        </Box>
      </Fade>

      {/* stage 1 */}
      <Canvas>
        <g opacity={legend1}>
          <circle cx={RX + 26} cy={640} r={24} fill={BLUE} stroke={C.ink} strokeWidth={2} />
        </g>
        <g opacity={legend2}>
          <circle cx={RX + 26} cy={720} r={24} fill={YELLOW} stroke={C.ink} strokeWidth={2} />
        </g>
      </Canvas>
      <Fade o={legend1} dy={12}>
        <Box x={RX + 80} y={612} w={680} size={46}>
          the high-degree blogs
        </Box>
      </Fade>
      <Fade o={legend2} dy={12}>
        <Box x={RX + 80} y={692} w={680} size={46}>
          the others
        </Box>
      </Fade>
      <Fade o={answer} dy={14}>
        <Box x={RX} y={800} w={740} size={50}>
          The groups follow degree, not politics.
        </Box>
      </Fade>
      <Fade o={img} dy={0}>
        <Box x={IMG_X} y={IMG_Y + IMG_H + 14} w={860} size={30} color={C.soft}>
          Karrer and Newman (2011)
        </Box>
      </Fade>
    </Frame>
  );
};
