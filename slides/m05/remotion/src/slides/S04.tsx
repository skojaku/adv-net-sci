import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Tag, Term} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog, stepped} from '../lib/anim';
import {NODE_D, Ring, qApart, qPairs} from '../lib/ring';
import {clamp} from '../lib/plot';

/**
 * 0: two groupings of a ring of 10 triangles, with their Q.
 * 1: two neighbouring triangles: 1 edge observed, 0.8 expected by chance.
 * 2: n runs from 4 to 16; the expected number falls and the winner flips at n = 8.
 * 3: the crossing is n = 8 = sqrt(2m).
 */
export const marks = [56, 112, 202, 252];

const ALL = Array.from({length: 16}, () => 1);

// the plot of stages 2 and 3
const PX0 = 1030;
const PX1 = 1740;
const PY_TOP = 490; // Q = 0.8
const PY_BOT = 800; // Q = 0.3
const px = (n: number) => PX0 + ((n - 4) / 12) * (PX1 - PX0);
const py = (q: number) => PY_BOT - ((q - 0.3) / 0.5) * (PY_BOT - PY_TOP);
const curve = (f: (n: number) => number) =>
  Array.from({length: 49}, (_, i) => {
    const n = 4 + i * 0.25;
    return `${i === 0 ? 'M' : 'L'}${px(n).toFixed(1)} ${py(f(n)).toFixed(1)}`;
  }).join(' ');

// the zoomed pair of stage 1
const ZS = 54; // half the base
const ZH = Math.sqrt(3) * ZS;
const ZY = 430;
const zoomTri = (cx: number) => ({
  a: [cx - ZS, ZY + ZH / 3] as const,
  b: [cx + ZS, ZY + ZH / 3] as const,
  c: [cx, ZY - (2 * ZH) / 3] as const,
});
const ZL = zoomTri(620);
const ZR = zoomTri(1300);

const Zoom: React.FC<{op: number}> = ({op}) => {
  const tri = (t: ReturnType<typeof zoomTri>, key: string) => (
    <g key={key}>
      <g opacity={0.3}>
        {[[t.a, t.b], [t.b, t.c], [t.a, t.c]].map(([p, q], i) => (
          <line key={i} x1={p[0]} y1={p[1]} x2={q[0]} y2={q[1]} stroke={C.blue} strokeWidth={120} strokeLinecap="round" />
        ))}
        {[t.a, t.b, t.c].map((p, i) => (
          <circle key={i} cx={p[0]} cy={p[1]} r={60} fill={C.blue} />
        ))}
      </g>
      {[[t.a, t.b], [t.b, t.c], [t.a, t.c]].map(([p, q], i) => (
        <line key={i} x1={p[0]} y1={p[1]} x2={q[0]} y2={q[1]} stroke={C.ink} strokeWidth={5} opacity={0.8} />
      ))}
    </g>
  );
  const disc = (p: readonly [number, number], deg: number, key: string) => (
    <g key={key}>
      <circle cx={p[0]} cy={p[1]} r={36} fill={C.blue} stroke="#fff" strokeWidth={3} />
      <text x={p[0]} y={p[1] + 13} textAnchor="middle" fontFamily={F.serif} fontSize={36} fontWeight={700} fill="#fff">
        {deg}
      </text>
    </g>
  );
  return (
    <g opacity={op}>
      <line x1={ZL.a[0]} y1={ZL.a[1]} x2={ZL.a[0] - 90} y2={ZL.a[1]} stroke={C.soft} strokeWidth={4} strokeDasharray="10 8" />
      <line x1={ZR.b[0]} y1={ZR.b[1]} x2={ZR.b[0] + 90} y2={ZR.b[1]} stroke={C.soft} strokeWidth={4} strokeDasharray="10 8" />
      {tri(ZL, 'l')}
      {tri(ZR, 'r')}
      <line x1={ZL.b[0]} y1={ZL.b[1]} x2={ZR.a[0]} y2={ZR.a[1]} stroke={C.ink} strokeWidth={5} opacity={0.8} />
      {disc(ZL.a, 3, 'la')}
      {disc(ZL.b, 3, 'lb')}
      {disc(ZL.c, 2, 'lc')}
      {disc(ZR.a, 3, 'ra')}
      {disc(ZR.b, 3, 'rb')}
      {disc(ZR.c, 2, 'rc')}
    </g>
  );
};

export const S04: React.FC = () => {
  const frame = useCurrentFrame();

  // stage 0
  const o0 = betweenStages(frame, marks, 0, 0);
  const band0 = prog(frame, 8, 26);
  const tags0 = prog(frame, 30, 50);

  // stage 1
  const o1 = betweenStages(frame, marks, 1, 1);
  const obs = prog(frame, 70, 84);
  const exp = prog(frame, 84, 100);
  const concl = prog(frame, 98, 110);

  // stages 2 and 3
  const o2 = fromStage(frame, marks, 2);
  const Nf = stepped(frame, 128, 12, 7, [4, 6, 8, 10, 12, 14, 16]);
  const w = ALL.map((_, i) => clamp(Nf - i, 0, 1));
  const toPairs = clamp((Nf - 8) / 2, 0, 1);
  const read = betweenStages(frame, marks, 2, 2);
  const cross = prog(frame, 204, 222);
  const cap2 = prog(frame, 228, 248);

  const dotOp = o2;
  return (
    <Frame n={4}>
      {/* stage 0 */}
      <Canvas>
        <g opacity={o0}>
          <Ring w={ALL.slice(0, 10)} cx={480} cy={565} slot={150} apart={band0} />
          <Ring w={ALL.slice(0, 10)} cx={1340} cy={565} slot={150} pairs={band0} />
        </g>
      </Canvas>
      <Fade o={o0}>
        <Box x={480} y={196} w={700} align="center" size={45} color={C.blue} hand>
          each triangle alone
        </Box>
        <Box x={1340} y={196} w={700} align="center" size={45} color={C.ink} hand>
          neighbors in pairs
        </Box>
      </Fade>
      <Fade o={o0 * tags0} dy={20}>
        <Tag x={480} y={888}>Q = 0.650</Tag>
        <Tag x={1340} y={888} hot>Q = 0.675</Tag>
      </Fade>

      {/* stage 1 */}
      <Canvas>
        <Zoom op={o1} />
      </Canvas>
      <Fade o={o1}>
        <Box x={620} y={560} w={420} align="center" size={40}>3 + 3 + 2 = 8</Box>
        <Box x={1300} y={560} w={420} align="center" size={40}>3 + 3 + 2 = 8</Box>
        <Box x={620} y={606} w={420} align="center" size={36} color={C.soft} hand>sum of degrees</Box>
        <Box x={1300} y={606} w={420} align="center" size={36} color={C.soft} hand>sum of degrees</Box>
      </Fade>
      <Fade o={o1 * obs} dy={16}>
        <Box x={960} y={360} w={520} align="center" size={45}>observed: 1 edge</Box>
      </Fade>
      <Fade o={o1 * exp} dy={16}>
        <div style={{position: 'absolute', left: 330, top: 670, width: 1260, background: C.panel, padding: '14px 36px 16px', fontFamily: F.serif}}>
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 28, fontSize: 45, height: 140}}>
            <span>expected by chance:</span>
            <Tex tex={'\\dfrac{8 \\times 8}{2m} = \\dfrac{64}{80} = 0.8'} style={{fontSize: 54}} />
            <span>edges</span>
          </div>
          <div style={{textAlign: 'center', fontSize: 34, color: C.soft, marginTop: 4}}>m = 40 edges, so 2m = 80</div>
        </div>
      </Fade>
      <Fade o={o1 * concl} dy={16}>
        <Box x={960} y={902} w={1200} align="center" size={45}>1 &gt; 0.8: merging raises Q</Box>
      </Fade>

      {/* stages 2 and 3 */}
      <Canvas>
        <g opacity={o2}>
          <Ring w={w} cx={497} cy={590} apart={1 - toPairs} pairs={toPairs} />
          {/* plot */}
          <line x1={PX0} y1={PY_BOT} x2={PX1 + 20} y2={PY_BOT} stroke={C.soft} strokeWidth={3} />
          <line x1={PX0} y1={PY_TOP - 20} x2={PX0} y2={PY_BOT} stroke={C.soft} strokeWidth={3} />
          {[4, 8, 12, 16].map((n) => (
            <g key={n}>
              <line x1={px(n)} y1={PY_BOT} x2={px(n)} y2={PY_BOT + 10} stroke={C.soft} strokeWidth={3} />
              <text x={px(n)} y={PY_BOT + 50} textAnchor="middle" fontFamily={F.serif} fontSize={38} fill={C.soft}>{n}</text>
            </g>
          ))}
          {[0.4, 0.6, 0.8].map((q) => (
            <g key={q}>
              <line x1={PX0 - 10} y1={py(q)} x2={PX0} y2={py(q)} stroke={C.soft} strokeWidth={3} />
              <text x={PX0 - 18} y={py(q) + 13} textAnchor="end" fontFamily={F.serif} fontSize={38} fill={C.soft}>{q.toFixed(1)}</text>
            </g>
          ))}
          <text x={PX1 + 20} y={PY_BOT + 106} textAnchor="end" fontFamily={F.hand} fontSize={45} fill={C.soft}>triangles in the ring</text>
          <text x={PX0 - 18} y={PY_TOP - 34} textAnchor="end" fontFamily={F.hand} fontSize={45} fill={C.soft}>Q</text>
          <path d={curve(qApart)} fill="none" stroke={C.blue} strokeWidth={6} />
          <path d={curve(qPairs)} fill="none" stroke={C.ink} strokeWidth={6} />
          <circle cx={px(Nf)} cy={py(qApart(Nf))} r={13} fill={C.blue} stroke="#fff" strokeWidth={3} opacity={dotOp} />
          <circle cx={px(Nf)} cy={py(qPairs(Nf))} r={13} fill={C.ink} stroke="#fff" strokeWidth={3} opacity={dotOp} />
          {/* direct labels at the right end of each curve */}
          <text x={PX1} y={py(qPairs(16)) - 30} textAnchor="end" fontFamily={F.serif} fontSize={36} fill={C.ink}>neighbors in pairs</text>
          <text x={PX1} y={py(qApart(16)) + 78} textAnchor="end" fontFamily={F.serif} fontSize={36} fill={C.blue}>each triangle alone</text>
          {/* the crossing */}
          <g opacity={cross}>
            <line x1={px(8)} y1={py(0.625)} x2={px(8)} y2={PY_BOT} stroke={C.ink} strokeWidth={3} strokeDasharray="10 8" />
            <circle cx={px(8)} cy={py(0.625)} r={11} fill="none" stroke={C.ink} strokeWidth={4} />
          </g>
        </g>
      </Canvas>
      <Fade o={o2 * read}>
        <Box x={1030} y={205} w={750} size={45}>n = {Math.round(Nf)} triangles</Box>
        <Box x={1030} y={262} w={780} size={40} color={C.soft}>expected between neighbors: {(8 / Nf).toFixed(2)}</Box>
      </Fade>
      <Fade o={cross}>
        <Box x={px(8) + 22} y={712} w={460} size={45}>
          <Tex tex={'n = 8 = \\sqrt{2m}'} />
        </Box>
      </Fade>
      <Fade o={cap2} dy={14}>
        <Box x={1030} y={210} w={770} size={40}>
          The network got bigger: the <Term>resolution limit</Term>.
        </Box>
      </Fade>
    </Frame>
  );
};
