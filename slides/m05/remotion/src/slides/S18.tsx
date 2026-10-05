import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Tag} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {betweenStages, prog, smooth} from '../lib/anim';
import {lerp} from '../lib/plot';
import {H_FOUND, H_GIVEN, H_TRUE, I_TF, f3} from '../lib/entropy8';
import {FOUND8, TRUTH8, nmi} from '../lib/metrics';
import {distanceForOverlap, lensArea, lensAreaByIntegration} from '../lib/lens';

/**
 * 0: two discs whose areas are the entropies: H(true) = 1.000 and H(found) = 0.954.
 * 1: they slide together until the overlap has area I = 0.549; the rest of the true disc is H(true given found) = 0.451.
 * 2: NMI = 2I / (H(true) + H(found)) = 0.562.
 * 3: three states side by side: identical splits (NMI = 1), this example (0.562), unrelated splits (NMI = 0).
 */
export const marks = [50, 110, 165, 215];

// ---- geometry: the area of a disc is its entropy, so r = K sqrt(H) and one bit is the area pi K^2
const K = 200;
const R_T = K * Math.sqrt(H_TRUE);
const R_F = K * Math.sqrt(H_FOUND);
const UNIT = Math.PI * K * K;
const D_FINAL = distanceForOverlap(R_T, R_F, I_TF * UNIT);

// the overlap on screen must be I, in the same units as the two entropies
{
  const byFormula = lensArea(R_T, R_F, D_FINAL) / UNIT;
  const byIntegral = lensAreaByIntegration(R_T, R_F, D_FINAL) / UNIT;
  if (Math.abs(byFormula - I_TF) > 1e-3 * H_TRUE || Math.abs(byIntegral - I_TF) > 1e-3 * H_TRUE) {
    throw new Error(`S18: overlap ${byFormula} (formula), ${byIntegral} (integral), wanted ${I_TF}`);
  }
  const crescent = (Math.PI * R_T * R_T - lensArea(R_T, R_F, D_FINAL)) / UNIT;
  if (Math.abs(crescent - H_GIVEN) > 1e-3 * H_TRUE) throw new Error(`S18: crescent ${crescent}, wanted ${H_GIVEN}`);
}

const CT = 330; // centre of the true disc
const CY = 590;
const D_APART = 480;

// ---- the three small states of stage 3: same construction, half the size
const K2 = 110;
const ODD8 = [0, 1, 0, 1, 0, 1, 0, 1] as const; // independent of TRUTH8
const NMI_SAME = nmi(TRUTH8, TRUTH8);
const NMI_EX = nmi(TRUTH8, FOUND8);
const NMI_NONE = nmi(TRUTH8, ODD8);
const nmiText = (v: number) => (Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v)) : f3(v));
if (nmiText(NMI_SAME) !== '1' || nmiText(NMI_EX) !== '0.562' || nmiText(NMI_NONE) !== '0') throw new Error('S18: unexpected NMI values');

const COLS = [350, 960, 1570];
const SMALL_Y = 560;
const R2_T = K2 * Math.sqrt(H_TRUE);
const R2_F = K2 * Math.sqrt(H_FOUND);
const STATES = [
  {name: 'identical splits', r1: K2, r2: K2, d: 0, nmi: NMI_SAME},
  {name: 'this example', r1: R2_T, r2: R2_F, d: D_FINAL / 2, nmi: NMI_EX},
  {name: 'unrelated splits', r1: K2, r2: K2, d: 2 * K2 + 12, nmi: NMI_NONE},
];

/** The overlap of two discs (a lens) as a path; null when the discs do not touch. */
const lensPath = (x1: number, y: number, r1: number, x2: number, r2: number): string | null => {
  const d = x2 - x1;
  if (d >= r1 + r2) return null;
  const a = (d * d + r1 * r1 - r2 * r2) / (2 * d);
  const h = Math.sqrt(Math.max(0, r1 * r1 - a * a));
  const px = x1 + a;
  // right edge: the arc of disc 1; left edge: the arc of disc 2
  return `M ${px} ${y - h} A ${r1} ${r1} 0 ${a < 0 ? 1 : 0} 1 ${px} ${y + h} A ${r2} ${r2} 0 ${a - d > 0 ? 1 : 0} 1 ${px} ${y - h} Z`;
};

/** Two discs and their overlap. True disc: light blue with a blue outline. Found disc: white with a black outline. Overlap: blue stripes with a blue outline. */
const Pair: React.FC<{x1: number; y: number; r1: number; x2: number; r2: number; sw?: number}> = ({x1, y, r1, x2, r2, sw = 6}) => {
  const lens = x2 - x1 < 1e-6 ? null : lensPath(x1, y, r1, x2, r2);
  return (
    <g>
      <circle cx={x1} cy={y} r={r1} fill={C.blueSoft} />
      <circle cx={x2} cy={y} r={r2} fill="#fff" />
      {x2 - x1 < 1e-6 ? <circle cx={x1} cy={y} r={r1} fill="url(#hatch-blue)" /> : lens && <path d={lens} fill="url(#hatch-blue)" stroke={C.blue} strokeWidth={sw * 0.7} strokeLinejoin="round" />}
      <circle cx={x1} cy={y} r={r1} fill="none" stroke={C.blue} strokeWidth={sw} />
      <circle cx={x2} cy={y} r={r2} fill="none" stroke={C.ink} strokeWidth={sw * 0.7} />
    </g>
  );
};

const texTrue = `H(\\text{true}) = ${f3(H_TRUE)}`;
const texFound = `H(\\text{found}) = ${f3(H_FOUND)}`;
const texI = `I = ${f3(I_TF)}`;
const texGiven = `H(\\text{true given found}) = ${f3(H_GIVEN)}`;
const texNmi = `\\displaystyle\\begin{aligned}\\mathrm{NMI} &= \\dfrac{2I}{H(\\text{true}) + H(\\text{found})} \\\\[8pt] &= \\dfrac{2 \\times ${f3(I_TF)}}{${f3(H_TRUE)} + ${f3(H_FOUND)}} = \\color{#B14434}{\\mathbf{${f3(NMI_EX)}}}\\end{aligned}`;

export const S18: React.FC = () => {
  const frame = useCurrentFrame();

  const big = betweenStages(frame, marks, 0, 2, 9);

  // stage 0
  const discs = prog(frame, 0, 18);
  const names = prog(frame, 12, 30);
  const o0 = betweenStages(frame, marks, 0, 0);
  const note = prog(frame, 28, 46);

  // stage 1
  const slide = smooth(frame, 54, 92);
  const cF = CT + lerp(D_APART, D_FINAL, slide);
  const regions = prog(frame, 88, 100);
  const leg1 = prog(frame, 92, 104);
  const leg2 = prog(frame, 98, 110);

  // stage 2
  const panel = prog(frame, 114, 134);

  // stage 3
  const small = prog(frame, 168, 186);
  const tags = prog(frame, 192, 208);

  // where the numbers sit once the discs overlap
  const xTrueCrescent = (CT - R_T + (CT + D_FINAL - R_F)) / 2;
  const xLens = (CT + D_FINAL - R_F + (CT + R_T)) / 2;

  return (
    <Frame n={18} title="Normalized mutual information">
      <Canvas>
        <g opacity={big * discs}>
          <Pair x1={CT} y={CY} r1={R_T} x2={cF} r2={R_F} />
        </g>
        <g opacity={big * regions}>
          <text x={xTrueCrescent} y={CY + 13} textAnchor="middle" fontFamily={F.serif} fontSize={38} fill={C.ink} stroke="#fff" strokeWidth={9} paintOrder="stroke">
            {f3(H_GIVEN)}
          </text>
          <text x={xLens} y={CY + 13} textAnchor="middle" fontFamily={F.serif} fontSize={38} fontWeight={700} fill={C.ink} stroke="#fff" strokeWidth={9} paintOrder="stroke">
            {f3(I_TF)}
          </text>
        </g>
        {/* legend swatches of stage 1 */}
        <g opacity={big * leg1}>
          <rect x={850} y={246} width={52} height={52} fill="url(#hatch-blue)" stroke={C.blue} strokeWidth={3} />
        </g>
        <g opacity={big * leg2}>
          <rect x={850} y={346} width={52} height={52} fill={C.blueSoft} stroke={C.blue} strokeWidth={3} />
        </g>
        {/* stage 3 */}
        <g opacity={small}>
          {STATES.map((s, k) => {
            const x1 = COLS[k] - (s.r1 + s.d + s.r2) / 2 + s.r1;
            return <Pair key={k} x1={x1} y={SMALL_Y} r1={s.r1} x2={x1 + s.d} r2={s.r2} sw={5} />;
          })}
        </g>
      </Canvas>

      {/* stages 0 to 2 */}
      <Fade o={big * names} dy={12}>
        <Box x={CT} y={228} w={420} align="center" size={45} color={C.blue} hand>
          true groups
        </Box>
        <Box x={CT} y={288} w={520} align="center" size={44}>
          <Tex tex={texTrue} />
        </Box>
        <Box x={cF} y={806} w={420} align="center" size={45} color={C.soft} hand>
          found groups
        </Box>
        <Box x={cF} y={866} w={520} align="center" size={44}>
          <Tex tex={texFound} />
        </Box>
      </Fade>
      <Fade o={o0 * note} dy={14}>
        <Box x={1120} y={500} w={640} size={54}>
          area = entropy
        </Box>
      </Fade>
      <Fade o={big * leg1} dy={12}>
        <Box x={930} y={236} w={850} size={54} style={{whiteSpace: 'nowrap'}}>
          <Tex tex={texI} />
        </Box>
      </Fade>
      <Fade o={big * leg2} dy={12}>
        <Box x={930} y={336} w={850} size={54} style={{whiteSpace: 'nowrap'}}>
          <Tex tex={texGiven} />
        </Box>
      </Fade>
      <Fade o={big * panel} dy={14}>
        <div style={{position: 'absolute', left: 840, top: 470, width: 940, background: C.panel, padding: '24px 44px 28px', fontFamily: F.serif, fontSize: 52}}>
          <Tex tex={texNmi} style={{fontSize: 52}} />
        </div>
      </Fade>
      {/* stage 3 */}
      <Fade o={small} dy={12}>
        {STATES.map((s, k) => (
          <Box key={k} x={COLS[k]} y={318} w={520} align="center" size={45} color={C.soft} hand>
            {s.name}
          </Box>
        ))}
      </Fade>
      <Fade o={tags} dy={14}>
        {STATES.map((s, k) => (
          <Tag key={k} x={COLS[k]} y={760}>
            NMI = {nmiText(s.nmi)}
          </Tag>
        ))}
      </Fade>
    </Frame>
  );
};
