import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame, TOP as FRAME_TOP, ZOOM} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {C, F} from '../theme';
import {prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {BAND_SOLID} from '../lib/look';
import {FOUND8, TRUTH8, ari, expectedRand, randIndex} from '../lib/metrics';
import {AB, Disc, EightRows, G_ARI, boxPad, nodeX, trueLook} from '../lib/eight';
import {CH, CW, CX, NodeTable, T2, TOP} from '../lib/nodetable';

/**
 * After the Rand index and the ARI, which count pairs of nodes: why not count nodes instead?
 * The slide starts from the picture S12 ends with (the same rows in the same places), then the nodes flow into a table.
 * 0: the Rand / expected / ARI tags of S12 leave; the boxes are named A and B; node 3 is ringed:
 *    "Why not count nodes, one at a time?"
 * 1: the true row fades; the lower row (nodes coloured by their true group, standing in their found box) glides down
 *    to make room for a 2 x 2 table above it; the nodes fly up, one by one, into the cell (colour, box); the boxes
 *    fade once they are empty; each pile is replaced by its count: 4, 0, 1, 3. "Count the nodes in each cell."
 * The table ends exactly as S14 begins it (same size and place); the slide's zoom eases to S14's.
 */
export const marks = [50, 160];

const G = G_ARI;
const ONE = 2; // node 3
const ROW_DOWN = 800; // y of the lower row while the nodes leave it

// where each node lands: the cell (true group, found group) and its place in the pile
const LEFT = CX - CW; // the table has two columns
const cellCx = (c: number) => LEFT + (c + 0.5) * CW;
const cellCy = (r: number) => TOP + r * CH + CH / 2;
const PILE_D = 50;
const PILE_STEP = 58;
const LANDING = Array.from({length: 8}, (_, i) => {
  const r = TRUTH8[i];
  const c = FOUND8[i];
  const mates = Array.from({length: 8}, (_, j) => j).filter((j) => TRUTH8[j] === r && FOUND8[j] === c);
  const k = mates.indexOf(i);
  const n = mates.length;
  const dx = n === 1 ? 0 : ((k % 2) - 0.5) * PILE_STEP;
  const dy = n <= 2 ? 0 : (Math.floor(k / 2) - 0.5) * PILE_STEP;
  return {x: cellCx(c) + dx, y: cellCy(r) + dy};
});
if (T2.flat().join() !== '4,0,1,3') throw new Error('S13: the table is not the one of the example');

const PAD = boxPad(G);
const R8 = randIndex(TRUTH8, FOUND8);
const E8 = expectedRand(TRUTH8, FOUND8);
const A8 = ari(TRUTH8, FOUND8);

export const S13: React.FC = () => {
  const frame = useCurrentFrame();
  const s = marks[0];

  // stage 0
  const tags = 1 - prog(frame, 4, 18);
  const names = prog(frame, 8, 24);
  const ring = prog(frame, 24, 38);
  const cap0 = prog(frame, 32, 48) * (1 - prog(frame, s + 2, s + 14));

  // stage 1
  const trueGone = 1 - prog(frame, s + 4, s + 18);
  const ringOff = 1 - prog(frame, s + 4, s + 14);
  const down = smooth(frame, s + 4, s + 30);
  const table = prog(frame, s + 16, s + 34);
  const fly = (i: number) => smooth(frame, s + 34 + 5 * i, s + 34 + 5 * i + 22);
  const boxOp = (k: number) => 1 - prog(frame, s + (k === 0 ? 66 : 78), s + (k === 0 ? 80 : 92));
  const numbers = prog(frame, s + 92, s + 106);
  const cap1 = prog(frame, s + 94, s + 108);
  const z = smooth(frame, s + 8, s + 100);

  const rowY = lerp(G.yFound, ROW_DOWN, down);

  return (
    <Frame n={13} zoom={lerp(ZOOM, 1.15, z)} top={lerp(FRAME_TOP, 245, z)}>
      <Canvas>
        <NodeTable counts={T2} cols={2} order={[[0, 1], [0, 1]]} slide={0} diag={false} op={table} numOp={numbers} />

        {/* the true row of S12, and the found boxes with their names */}
        <EightRows g={G} names={false} boxOp={0} trueOp={() => trueGone} foundOp={() => 0} ringTrue={(i) => (i === ONE ? ring * ringOff : 0)} />
        {AB.map(([a, b], k) => {
          const x = nodeX(G, a) - PAD;
          const w = nodeX(G, b) - nodeX(G, a) + 2 * PAD;
          return (
            <g key={k} opacity={boxOp(k)}>
              <rect x={x} y={rowY - PAD} width={w} height={2 * PAD} rx={0.3 * G.d} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
              <text x={x + w / 2} y={rowY + PAD + 50} textAnchor="middle" fontFamily={F.hand} fontSize={45} fill={C.soft} opacity={names}>
                {k === 0 ? 'A' : 'B'}
              </text>
            </g>
          );
        })}
        {/* the nodes of the lower row, flying into the table */}
        {Array.from({length: 8}, (_, i) => {
          const t = fly(i);
          return (
            <Disc
              key={i}
              x={lerp(nodeX(G, i), LANDING[i].x, t)}
              y={lerp(rowY, LANDING[i].y, t)}
              d={lerp(G.d, PILE_D, t)}
              look={trueLook(i)}
              label={i + 1}
              ring={i === ONE ? ring * ringOff : 0}
              op={1 - numbers}
            />
          );
        })}
      </Canvas>

      {/* S12's tags, fading out */}
      <Fade o={tags}>
        <Tag x={430} y={760}>Rand {R8.toFixed(2)}</Tag>
        <Tag x={960} y={760}>expected {E8.toFixed(2)}</Tag>
        <Tag x={1470} y={760} hot>ARI {A8.toFixed(2)}</Tag>
      </Fade>
      <Fade o={cap0} dy={14}>
        <Box x={CX} y={690} w={1500} align="center" size={54}>
          Why not count nodes, one at a time?
        </Box>
      </Fade>
      <Fade o={cap1} dy={14}>
        <Box x={CX} y={690} w={1500} align="center" size={54}>
          Count the nodes in each cell.
        </Box>
      </Fade>
    </Frame>
  );
};
