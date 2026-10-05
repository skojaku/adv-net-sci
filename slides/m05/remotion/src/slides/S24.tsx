import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Cap} from '../components/Text';
import {Network} from '../lib/network';
import {LOOK} from '../lib/look';
import {C} from '../theme';
import {prog, smooth} from '../lib/anim';
import {SBM_GROUP, SBM_LOOK, sbmEdges} from '../lib/sbm';
import {AdjMatrix, PIC, SORT_STEPS, ring8, slotsAt} from '../lib/matrix';

/**
 * 0: the picture of S23.
 * 1: rows and columns move into group order, one node at a time; two dense blocks appear on the diagonal.
 * 2: black outlines on the blocks, the nodes become solid and hollow.
 */
export const marks = [30, 120, 170];

const POS = ring8(PIC.netCx, PIC.netCy, PIC.netR);
const EDGES = sbmEdges(0.9, 0.1);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const SAME = SBM_GROUP.map(() => LOOK[0]);
const LOOKS = SBM_GROUP.map((g) => SBM_LOOK[g]);
const HALF = 4 * PIC.cell;
const N_STEPS = SORT_STEPS.length - 1;
const SORT0 = 36; // the sort runs from here to SORT0 + SORT_LEN
const SORT_LEN = 78;

export const S24: React.FC = () => {
  const frame = useCurrentFrame();
  const intro = prog(frame, 0, 18);
  // one insertion per step: a node moves into its place, the nodes it passes shift by one
  const per = SORT_LEN / N_STEPS;
  const steps = SORT_STEPS.slice(1).map((_, k) => smooth(frame, SORT0 + per * k, SORT0 + per * (k + 1) - 2));
  const box = prog(frame, 126, 142);
  const paint = prog(frame, 128, 154);
  const cap = prog(frame, 146, 162);

  return (
    <Frame n={24} title="Sort by group, and blocks appear">
      <Canvas>
        <Network pos={POS} edges={EDGES} look={SAME} lookTo={LOOKS} t={paint} nodeD={PIC.nodeD} edgeW={5} label={LABELS} labelSize={36} opacity={intro} />
        <AdjMatrix x={PIC.mx} y={PIC.my} cell={PIC.cell} edges={EDGES} pos={slotsAt(steps)} look={SAME} lookTo={LOOKS} t={paint} opacity={intro} />
        <g opacity={box} fill="none" stroke={C.ink} strokeWidth={9}>
          <rect x={PIC.mx} y={PIC.my} width={HALF} height={HALF} />
          <rect x={PIC.mx + HALF} y={PIC.my + HALF} width={HALF} height={HALF} />
        </g>
      </Canvas>
      <Fade o={cap} dy={14}>
        <Cap y={184}>Nothing changed but the order.</Cap>
      </Fade>
    </Frame>
  );
};
