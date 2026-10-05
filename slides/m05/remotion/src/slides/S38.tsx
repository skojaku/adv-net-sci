import React from 'react';
import {Img, staticFile, useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {fromStage, prog} from '../lib/anim';

/**
 * Back to the political blogs (Karrer and Newman 2011, Fig. 2): the plain SBM and the degree-corrected SBM side by side.
 * 0: the two divisions, with the same node sizes (degree).
 * 1: the groups are found despite heterogeneous degrees: the normalized mutual information with the known labels
 *    (liberal, conservative) is 0.0001 for the plain SBM and 0.72 for the degree-corrected SBM (the values of the paper).
 */
export const marks = [64, 128];

const W = 740;
const H = Math.round((W * 636) / 818);
const PY = 262;
const X = [140, 1040];

export const S38: React.FC = () => {
  const frame = useCurrentFrame();

  const a = prog(frame, 0, 22);
  const b = prog(frame, 14, 36);
  const capA = prog(frame, 22, 38);
  const capB = prog(frame, 34, 50);
  const top = fromStage(frame, marks, 1, 18);
  const tagA = prog(frame, marks[0] + 14, marks[0] + 30);
  const tagB = prog(frame, marks[0] + 28, marks[0] + 44);

  return (
    <Frame n={38}>
      <Fade o={a}>
        <Img src={staticFile('dcsbm-plain.png')} style={{position: 'absolute', left: X[0], top: PY, width: W, height: H}} />
      </Fade>
      <Fade o={b}>
        <Img src={staticFile('dcsbm-corrected.png')} style={{position: 'absolute', left: X[1], top: PY, width: W, height: H}} />
      </Fade>
      <Fade o={capA} dy={12}>
        <Cap x={X[0] + W / 2} y={PY + H + 8} w={W}>plain SBM</Cap>
      </Fade>
      <Fade o={capB} dy={12}>
        <Cap x={X[1] + W / 2} y={PY + H + 8} w={W}>degree-corrected SBM</Cap>
      </Fade>
      <Fade o={top} dy={14}>
        <Box x={120} y={190} w={1680} size={42}>
          Degree correction finds the groups despite heterogeneous degrees.
        </Box>
      </Fade>
      <Fade o={tagA} dy={12}>
        <Tag x={X[0] + W / 2} y={PY + H + 72} style={{fontSize: 40}}>NMI with the known labels: 0.0001</Tag>
      </Fade>
      <Fade o={tagB} dy={12}>
        <Tag x={X[1] + W / 2} y={PY + H + 72} hot style={{fontSize: 40}}>NMI with the known labels: 0.72</Tag>
      </Fade>
    </Frame>
  );
};
