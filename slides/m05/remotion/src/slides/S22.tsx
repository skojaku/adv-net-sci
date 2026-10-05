import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {Tex} from '../components/Tex';
import {BlockTable} from '../components/BlockTable';
import {Network} from '../lib/network';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {SBM_GROUP, SBM_LOOK, SBM_PAIRS, pairIndex, sbmEdges} from '../lib/sbm';
import {SBM_U} from '../data/data';
import {PIC, ring8} from '../lib/matrix';

/**
 * 0: eight nodes in two groups (solid and hollow), no edges.
 * 1: the definition and the table of probabilities.
 * 2: nodes 1 and 2 (same group): p = 0.9, u = 0.72, so the edge is drawn.
 * 3: nodes 1 and 6 (different groups): p = 0.1, u = 0.59, so no edge.
 * 4: the other pairs of nodes are processed one by one and the network is complete.
 */
export const marks = [50, 100, 160, 210, 300];

const P_IN = 0.9;
const P_OUT = 0.1;
const LOOKS = SBM_GROUP.map((g) => SBM_LOOK[g]);
const LABELS = Array.from({length: 8}, (_, i) => String(i + 1));
const EDGES = sbmEdges(P_IN, P_OUT);

// the two worked examples: nodes 1 and 2 (same group), nodes 1 and 6 (different groups)
const A = [0, 1] as const;
const B = [0, 5] as const;
const KA = pairIndex(A[0], A[1]);
const KB = pairIndex(B[0], B[1]);
const UA = SBM_U[KA];
const UB = SBM_U[KB];

// the sweep of stage 4: every other pair, in the order of SBM_PAIRS
const REST = SBM_PAIRS.map((_, k) => k).filter((k) => k !== KA && k !== KB);
const ORDER = new Map(REST.map((k, j) => [k, j] as const));
const SW0 = 218;
const PER = 2.6;

// the number line of stages 2 and 3
const NL0 = 1060;
const NL1 = 1760;
const NLY = 790;
const nlx = (v: number) => NL0 + v * (NL1 - NL0);

const TX = 1040; // left edge of the right-hand column
const TY = 385; // top of the probability table
const CELL = 120;

const num = (v: number) => String(v);
const u2 = (v: number) => v.toFixed(2);

export const S22: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(UA < P_IN) || UB < P_OUT) throw new Error('S22: the worked examples no longer give "edge" and "no edge"');

  // the ring opens in the middle of the slide and moves left when the table comes in
  const cx = lerp(960, PIC.netCx, smooth(frame, marks[0] + 2, marks[0] + 32));
  const POS = ring8(cx, PIC.netCy, PIC.netR);

  const nodeOp = (i: number) => prog(frame, 4 + 3 * i, 16 + 3 * i);

  // stage 1
  const defO = prog(frame, 54, 72);
  const tableO = prog(frame, 70, 88);
  const capO = prog(frame, 84, 98) * (1 - prog(frame, 100, 108));

  // stage 2
  const ringA = prog(frame, 100, 112) * (1 - prog(frame, 160, 168));
  const lineO = prog(frame, 108, 120) * (1 - prog(frame, 210, 220));
  const grow = prog(frame, 108, 124);
  const dropA = prog(frame, 124, 140) * (1 - prog(frame, 160, 168));
  const resA = prog(frame, 140, 152) * (1 - prog(frame, 160, 168));
  const edgeA = prog(frame, 142, 154);

  // stage 3
  const ringB = prog(frame, 160, 172) * (1 - prog(frame, 210, 218));
  const pCur = lerp(P_IN, P_OUT, smooth(frame, 160, 174));
  const dropB = prog(frame, 176, 190) * (1 - prog(frame, 210, 218));
  const resB = prog(frame, 192, 204) * (1 - prog(frame, 210, 218));
  const noEdge = prog(frame, 194, 206) * (1 - prog(frame, 210, 218));

  // stage 4
  const j = Math.floor((frame - SW0) / PER);
  const cur = j >= 0 && j < REST.length ? SBM_PAIRS[REST[j]] : null;
  const finalO = prog(frame, 282, 296);

  const hotA = frame >= marks[1] + 2 && frame < marks[2] + 2;
  const hotB = frame >= marks[2] + 2 && frame < marks[3] + 2;
  const hot: [[boolean, boolean], [boolean, boolean]] = hotA ? [[true, false], [false, false]] : hotB ? [[false, true], [true, false]] : [[false, false], [false, false]];

  const edgeOp = (_: number, e: readonly [number, number]) => {
    const k = pairIndex(e[0], e[1]);
    if (k === KA) return edgeA;
    const jj = ORDER.get(k);
    return jj === undefined ? 0 : prog(frame, SW0 + jj * PER, SW0 + jj * PER + 5);
  };

  const mid = [(POS[B[0]][0] + POS[B[1]][0]) / 2, (POS[B[0]][1] + POS[B[1]][1]) / 2] as const;
  const ringCircle = (i: number, o: number) =>
    o > 0.001 ? <circle key={i} cx={POS[i][0]} cy={POS[i][1]} r={PIC.nodeD / 2 + 10} fill="none" stroke={C.ink} strokeWidth={7} opacity={o} /> : null;

  const marker = (v: number, drop: number) => (
    <g opacity={drop} transform={`translate(${nlx(v)}, ${NLY - (1 - drop) * 40})`}>
      <polygon points="-17,-44 17,-44 0,-8" fill={C.ink} />
    </g>
  );

  return (
    <Frame n={22} title="Groups first, then edges">
      {/* the definition: stage 1 on */}
      <Fade o={defO} dy={14}>
        <Box x={120} y={192} w={1680} size={45}>
          Nodes <Tex tex="i" /> and <Tex tex="j" /> connect with probability <Tex tex="p_{c_i c_j}" style={{fontSize: 52}} />
        </Box>
      </Fade>

      <Canvas>
        {/* the pair under the pointer in stage 4 */}
        {cur && (
          <line
            x1={POS[cur[0]][0]}
            y1={POS[cur[0]][1]}
            x2={POS[cur[1]][0]}
            y2={POS[cur[1]][1]}
            stroke={C.blueMid}
            strokeWidth={30}
            strokeLinecap="round"
          />
        )}
        {/* the pair that was rejected in stage 3 */}
        <g opacity={noEdge}>
          <line x1={POS[B[0]][0]} y1={POS[B[0]][1]} x2={POS[B[1]][0]} y2={POS[B[1]][1]} stroke={C.soft} strokeWidth={4} strokeDasharray="10 9" />
          <g stroke={C.ink} strokeWidth={8} strokeLinecap="round">
            <line x1={mid[0] - 20} y1={mid[1] - 20} x2={mid[0] + 20} y2={mid[1] + 20} />
            <line x1={mid[0] - 20} y1={mid[1] + 20} x2={mid[0] + 20} y2={mid[1] - 20} />
          </g>
        </g>
        <Network pos={POS} edges={EDGES} look={LOOKS} nodeD={PIC.nodeD} nodeOp={nodeOp} edgeOp={edgeOp} edgeW={5} label={LABELS} labelSize={36} />
        {A.map((i) => ringCircle(i, ringA))}
        {B.map((i) => ringCircle(i, ringB))}
        {cur && [cur[0], cur[1]].map((i) => ringCircle(i, 1))}

        <BlockTable x={TX} y={TY} cell={CELL} fontSize={40} p={[[P_IN, P_OUT], [P_OUT, P_IN]]} hot={hot} opacity={tableO} />

        {/* the number line of stages 2 and 3: an edge appears when u falls in the blue part */}
        <g opacity={lineO}>
          <line x1={nlx(0)} y1={NLY} x2={nlx(1)} y2={NLY} stroke={C.soft} strokeWidth={3} />
          <line x1={nlx(0)} y1={NLY} x2={nlx(Math.max(0.001, pCur * grow))} y2={NLY} stroke={C.blue} strokeWidth={18} strokeLinecap="round" />
          <line x1={nlx(0)} y1={NLY - 12} x2={nlx(0)} y2={NLY + 12} stroke={C.soft} strokeWidth={3} />
          <line x1={nlx(1)} y1={NLY - 12} x2={nlx(1)} y2={NLY + 12} stroke={C.soft} strokeWidth={3} />
          <text x={nlx(0)} y={NLY + 52} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>0</text>
          <text x={nlx(1)} y={NLY + 52} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.soft}>1</text>
          <g opacity={grow}>
            <line x1={nlx(pCur)} y1={NLY - 16} x2={nlx(pCur)} y2={NLY + 16} stroke={C.ink} strokeWidth={5} />
            <text x={nlx(pCur)} y={NLY + 52} textAnchor="middle" fontFamily={F.serif} fontSize={36} fill={C.ink}>
              {frame < 167 ? num(P_IN) : num(P_OUT)}
            </text>
          </g>
          {marker(UA, dropA)}
          {marker(UB, dropB)}
        </g>
      </Canvas>

      {/* stage 1 caption, next to the table */}
      <Fade o={capO} dy={14}>
        <Cap x={TX + CELL * 2 + 50} y={TY + 20} w={470} align="left">one probability per block</Cap>
      </Fade>

      {/* the drawn number u and the result */}
      <Fade o={lineO * dropA} dy={-30}>
        <Box x={nlx(UA)} y={NLY - 108} w={300} align="center" size={40}>
          <Tex tex={`u = ${u2(UA)}`} />
        </Box>
      </Fade>
      <Fade o={lineO * dropB} dy={-30}>
        <Box x={nlx(UB)} y={NLY - 108} w={300} align="center" size={40}>
          <Tex tex={`u = ${u2(UB)}`} />
        </Box>
      </Fade>
      <Fade o={resA} dy={14}>
        <Box x={TX} y={880} w={760} size={45}>
          <Tex tex={`u < ${num(P_IN)}`} />: <Term>draw the edge</Term>
        </Box>
      </Fade>
      <Fade o={resB} dy={14}>
        <Box x={TX} y={880} w={760} size={45}>
          <Tex tex={`u \\ge ${num(P_OUT)}`} />: <Term>no edge</Term>
        </Box>
      </Fade>

      {/* stage 4 */}
      <Fade o={finalO} dy={14}>
        <Box x={TX} y={700} w={760} size={45}>
          {EDGES.length} edges
        </Box>
      </Fade>
    </Frame>
  );
};
