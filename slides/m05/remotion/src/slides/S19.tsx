import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag} from '../components/Text';
import {C} from '../theme';
import {betweenStages, prog} from '../lib/anim';
import {SHUFFLES} from '../data/data';
import {ALONE8, TRUTH8, ari, nmi, randIndex} from '../lib/metrics';
import {ALONE, EightRows, RowGeom} from '../lib/eight';
import {NodeDot, TRUE30, dotCentre} from '../lib/dots30';

/**
 * 0: the eight nodes with the found split "every node alone" (8 boxes).
 * 1: Rand 0.57, NMI 0.50, ARI 0.00: this split says nothing about the groups.
 * 2: back to the 30 nodes with random labels: NMI is not zero for them, ARI is about 0.
 */
export const marks = [50, 100, 160];

// ---- numbers: the eight-node ones come from metrics.ts
const RAND = randIndex(TRUTH8, ALONE8);
const NMI = nmi(TRUTH8, ALONE8);
const ARI = ari(TRUTH8, ALONE8);
const f2 = (x: number) => (Math.abs(x) < 5e-3 ? '0.00' : x.toFixed(2));
if (f2(RAND) !== '0.57' || f2(NMI) !== '0.50' || f2(ARI) !== '0.00') throw new Error(`S19: ${RAND} ${NMI} ${ARI}`);

// ---- the shuffled nodes. The mean NMI of 0.215 is over 2000 shuffles (scripts/verify_numbers.py asserts it);
// data.ts keeps 40 shuffles, whose mean must land close to it.
const mean = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;
const MEAN_NMI_2000 = 0.215;
{
  const nmi40 = mean(SHUFFLES.map((s) => nmi(TRUE30, s)));
  const ari40 = mean(SHUFFLES.map((s) => ari(TRUE30, s)));
  if (Math.abs(nmi40 - MEAN_NMI_2000) > 5e-3) throw new Error(`S19: mean NMI of the stored shuffles is ${nmi40}`);
  if (Math.abs(ari40) > 1e-2) throw new Error(`S19: mean ARI of the stored shuffles is ${ari40}`);
}
const RANDOM_LABELS = SHUFFLES[0];

// ---- layout
const G: RowGeom = {x0: 470, pitch: 140, d: 80, yTrue: 300, yFound: 500};

const D30 = 46;
const PITCH30 = 58;
const STRIDE30 = 250;
const X30 = 402;
const Y30_TOP = 285;
const Y30_BOT = 480;
const ROW = [...Array(30).keys()];

export const S19: React.FC = () => {
  const frame = useCurrentFrame();

  // stages 0 and 1
  const eight = betweenStages(frame, marks, 0, 1);
  const labels = prog(frame, 6, 22);
  const boxes = prog(frame, 28, 44);
  const alone = prog(frame, 36, 50);
  const t1 = prog(frame, 56, 70);
  const t2 = prog(frame, 64, 78);
  const t3 = prog(frame, 72, 86);
  const says = prog(frame, 84, 98);

  // stage 2
  const nodes = betweenStages(frame, marks, 2, 2);
  const tag1 = prog(frame, 132, 146);
  const tag2 = prog(frame, 136, 150);
  const last = prog(frame, 144, 158);

  return (
    <Frame n={19} title="Many tiny groups">
      <Canvas>
        <g opacity={eight}>
          <EightRows
            g={G}
            found={ALONE}
            names={false}
            boxOp={boxes}
            trueOp={(i) => prog(frame, i * 1.5, i * 1.5 + 14)}
            foundOp={(i) => prog(frame, 12 + i * 1.5, 26 + i * 1.5)}
          />
        </g>
        <g opacity={nodes}>
          {ROW.map((j) => {
            const [x, y] = dotCentre(j, X30, Y30_TOP, PITCH30, STRIDE30);
            return <NodeDot key={`a${j}`} x={x} y={y} d={D30} g={TRUE30[j]} op={prog(frame, 106 + j * 0.4, 118 + j * 0.4)} />;
          })}
          {ROW.map((j) => {
            const [x, y] = dotCentre(j, X30, Y30_BOT, PITCH30, STRIDE30);
            return <NodeDot key={`b${j}`} x={x} y={y} d={D30} g={RANDOM_LABELS[j]} op={prog(frame, 116 + j * 0.4, 128 + j * 0.4)} />;
          })}
        </g>
      </Canvas>

      {/* stages 0 and 1 */}
      <Fade o={eight * labels} dy={10}>
        <Box x={120} y={G.yTrue - 30} w={260} size={45} color={C.soft} hand>true</Box>
        <Box x={120} y={G.yFound - 30} w={260} size={45} color={C.soft} hand>found</Box>
      </Fade>
      <Fade o={eight * alone} dy={12}>
        <Cap x={960} y={G.yFound + 56 + 22} w={1000}>
          every node alone
        </Cap>
      </Fade>
      <Fade o={eight * t1} dy={14}>
        <Tag x={540} y={700}>Rand {f2(RAND)}</Tag>
      </Fade>
      <Fade o={eight * t2} dy={14}>
        <Tag x={960} y={700}>NMI {f2(NMI)}</Tag>
      </Fade>
      <Fade o={eight * t3} dy={14}>
        <Tag x={1380} y={700} hot>ARI {f2(ARI)}</Tag>
      </Fade>
      <Fade o={eight * says} dy={14}>
        <Cap x={960} y={830} w={1300}>
          This split says nothing about the groups.
        </Cap>
      </Fade>

      {/* stage 2 */}
      <Fade o={nodes * tag1} dy={14}>
        <Tag x={700} y={660}>average NMI {MEAN_NMI_2000.toFixed(3)}</Tag>
      </Fade>
      <Fade o={nodes * tag2} dy={14}>
        <Tag x={1270} y={660}>average ARI about 0</Tag>
      </Fade>
      <Fade o={nodes * last} dy={14}>
        <Cap x={960} y={800} w={1500}>
          NMI is not zero for random labels.
        </Cap>
      </Fade>
    </Frame>
  );
};
