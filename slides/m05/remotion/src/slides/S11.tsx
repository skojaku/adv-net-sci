import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Term} from '../components/Text';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {Frac} from '../lib/eight';
import {N_AGREE, PAIRS8, PairMatrix, TOGETHER} from '../lib/pairmatrix';

/**
 * The 28 pairs of nodes are the cells of a matrix. Nodes 1 to 8 run along both sides: the top shows their true
 * colours, the left shows their found boxes. A pair is never drawn as two nodes joined by a line.
 * 0: the empty matrix. "8 nodes make 28 pairs of nodes".
 * 1: the upper half of every cell: are the two nodes together in the true split (the same colour)?
 * 2: the lower half: together in the found split (the same box)?
 * 3: where the two halves match the pair agrees (check), where they differ it disagrees (cross).
 * 4: Rand index = agreeing pairs of nodes / all pairs of nodes = 21 / 28.
 */
export const marks = [44, 100, 170, 230, 292];

const MX = 340;
const MY = 350;
const CELL = 76;

const reveal = (frame: number, start: number, dur = 12) => (k: number) => prog(frame, start + k * 1.1, start + k * 1.1 + dur);

export const S11: React.FC = () => {
  const frame = useCurrentFrame();

  const head = prog(frame, 0, 16);
  const cap0 = betweenStages(frame, marks, 0, 0);
  const cap1 = betweenStages(frame, marks, 1, 1);
  const cap2 = betweenStages(frame, marks, 2, 2);
  const cap3 = betweenStages(frame, marks, 3, 3);
  const cap4 = fromStage(frame, marks, 4);

  const trueHalf = (k: number) => reveal(frame, 46, 10)(k);
  const foundHalf = (k: number) => reveal(frame, 102, 10)(k);
  const mark = (k: number) => reveal(frame, 172, 10)(k);

  const swatch = (fill: string, y: number, label: string) => (
    <>
      <rect x={1050} y={y} width={52} height={52} fill={fill} stroke={C.soft} strokeWidth={3} />
      <text x={1126} y={y + 40} fontFamily={F.serif} fontSize={40} fill={C.ink}>
        {label}
      </text>
    </>
  );

  return (
    <Frame n={11} title="Rand index: pairs of nodes">
      <Canvas>
        <PairMatrix x={MX} y={MY} c={CELL} headerOp={head} trueHalf={trueHalf} foundHalf={foundHalf} mark={mark} />
        {/* the key to the halves */}
        <g opacity={cap1}>
          {swatch(TOGETHER, 560, 'together: same color')}
          {swatch('#fff', 640, 'apart: different colors')}
        </g>
        <g opacity={cap2}>
          {swatch(TOGETHER, 560, 'together: same box')}
          {swatch('#fff', 640, 'apart: different boxes')}
        </g>
      </Canvas>
      <Fade o={cap0} dy={14}>
        <Box x={1050} y={400} w={740} size={45}>
          8 nodes make 28 pairs of nodes.
        </Box>
        <Box x={1050} y={520} w={740} size={45} color={C.soft}>
          One cell is one pair.
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={1050} y={420} w={740} size={45}>
          Upper half: the true split
        </Box>
      </Fade>
      <Fade o={cap2} dy={14}>
        <Box x={1050} y={420} w={740} size={45}>
          Lower half: the found split
        </Box>
      </Fade>
      <Fade o={cap3} dy={14}>
        <Box x={1050} y={400} w={740} size={45}>
          Both halves alike: <span style={{color: C.blue}}>agree</span>
        </Box>
        <Box x={1050} y={480} w={740} size={45}>
          Halves differ: <Term>disagree</Term>
        </Box>
        <Box x={1050} y={600} w={740} size={45} color={C.soft}>
          {N_AGREE} agree, {PAIRS8.length - N_AGREE} disagree
        </Box>
      </Fade>
      <Fade o={cap4} dy={14}>
        <div style={{position: 'absolute', left: 1030, top: 430, width: 770, background: C.panel, padding: '26px 30px', fontFamily: F.serif, fontSize: 45, lineHeight: 1.5}}>
          <Term>Rand index</Term> ={' '}
          <Frac top="agreeing pairs of nodes" bottom="all pairs of nodes" />
          <div>
            = <Frac top={N_AGREE} bottom={PAIRS8.length} /> = {(N_AGREE / PAIRS8.length).toFixed(2)}
          </div>
        </div>
      </Fade>
    </Frame>
  );
};
