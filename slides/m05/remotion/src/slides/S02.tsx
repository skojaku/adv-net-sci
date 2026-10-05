import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Cap, Tag} from '../components/Text';
import {prog} from '../lib/anim';
import {Ring} from '../lib/ring';

/**
 * 0: four triangles arrive one at a time and the ring closes.
 * 1: a band around each triangle, Q = 0.500.
 * 2: the same ring on the right, neighbours banded in pairs, Q = 0.375; the left one is higher.
 */
export const marks = [52, 100, 160];

const SCALE = 1.8;
const CY = 505;
const CX_L = 500;
const CX_R = 1420;
const TAG_Y = 812;

export const S02: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0: triangle i arrives at 6 + 9 i
  const w = [0, 1, 2, 3].map((i) => prog(frame, 6 + 9 * i, 20 + 9 * i));

  // stage 1
  const bandL = prog(frame, 56, 78);
  const tagL = prog(frame, 74, 92);

  // stage 2
  const ringR = prog(frame, 102, 118);
  const bandR = prog(frame, 108, 128);
  const tagR = prog(frame, 122, 140);
  const hotL = prog(frame, 130, 146);
  const cap = prog(frame, 138, 156);

  const ones = [1, 1, 1, 1];
  return (
    <Frame n={2} title="A ring of triangles">
      <Canvas>
        <Ring w={w} cx={CX_L} cy={CY} scale={SCALE} apart={bandL} />
        <Ring w={ones} cx={CX_R} cy={CY} scale={SCALE} pairs={bandR} opacity={ringR} />
      </Canvas>
      <Fade o={tagL * (1 - hotL)} dy={20}>
        <Tag x={CX_L} y={TAG_Y}>Q = 0.500</Tag>
      </Fade>
      <Fade o={hotL}>
        <Tag x={CX_L} y={TAG_Y} hot>Q = 0.500</Tag>
      </Fade>
      <Fade o={tagR} dy={20}>
        <Tag x={CX_R} y={TAG_Y}>Q = 0.375</Tag>
      </Fade>
      <Fade o={cap} dy={14}>
        <Cap y={912}>Each triangle alone has the higher Q.</Cap>
      </Fade>
    </Frame>
  );
};
