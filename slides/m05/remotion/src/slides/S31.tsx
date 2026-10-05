import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame} from '../components/Frame';
import {Canvas, Fade} from '../components/Fade';
import {Box, Cap, Term} from '../components/Text';
import {Tex} from '../components/Tex';
import {C, F} from '../theme';
import {betweenStages, fromStage, prog} from '../lib/anim';
import {BEST_BAYES} from '../lib/sbmscore';

/**
 * Peixoto's Bayesian SBM, in its simplest form.
 * 0: maximum likelihood against the Bayesian posterior: the block probabilities p are integrated out.
 * 1: the Bayesian score of the 8-node network, best grouping for each K: it peaks at K = 2.
 * 2: what the full model adds: K is inferred, groups within groups, uneven degrees.
 */
export const marks = [64, 134, 196];

const X0 = 230;
const X1 = 1130;
const Y0 = 835; // score -24
const Y1 = 300; // score -17
const px = (k: number) => X0 + ((k - 1) / 7) * (X1 - X0);
const py = (v: number) => Y0 - ((v + 24) / 7) * (Y0 - Y1);
const PEAK = BEST_BAYES.indexOf(Math.max(...BEST_BAYES));
if (PEAK !== 1) throw new Error('S31: the Bayesian score should peak at K = 2');

export const S31: React.FC = () => {
  const frame = useCurrentFrame();

  const left = betweenStages(frame, marks, 0, 0) * prog(frame, 6, 24);
  const right = betweenStages(frame, marks, 0, 0) * prog(frame, 26, 46);
  const plot = betweenStages(frame, marks, 1, 1);
  const dot = (i: number) => prog(frame, marks[0] + 8 + i * 4, marks[0] + 20 + i * 4);
  const peak = prog(frame, marks[0] + 52, marks[0] + 66);
  const full = fromStage(frame, marks, 2, 14);

  return (
    <Frame n={31} title="Bayesian SBM">
      {/* stage 0 */}
      <Fade o={left} dy={14}>
        <Cap x={120} y={250} w={760} align="left">maximum likelihood</Cap>
        <Box x={120} y={350} w={780} size={50}>
          <Tex tex={'\\max_{c,\\,p}\\ \\log P(A \\mid c, p)'} />
        </Box>
        <Box x={120} y={470} w={780} size={45} color={C.soft}>
          more groups always fit better
        </Box>
      </Fade>
      <Fade o={right} dy={14}>
        <Cap x={1000} y={250} w={800} align="left">Bayesian</Cap>
        <Box x={1000} y={350} w={820} size={36}>
          <Tex tex={'P(c \\mid A) \\propto P(c)\\int P(A \\mid c, p)\\,P(p)\\,dp'} />
        </Box>
        <Box x={1000} y={470} w={800} size={45} color={C.soft}>
          <Tex tex="p" /> is integrated out: more groups must pay for themselves
        </Box>
      </Fade>
      <Fade o={(left + right) / 2} dy={10}>
        <Box x={120} y={840} w={1680} size={38} color={C.soft}>
          <Tex tex="A" />: the network. <Tex tex="c" />: the groups. <Tex tex="p" />: the probabilities in the table.
        </Box>
      </Fade>

      {/* stage 1 */}
      <Canvas>
        <g opacity={plot}>
          <line x1={X0} y1={Y0} x2={X1 + 30} y2={Y0} stroke={C.soft} strokeWidth={3} />
          <line x1={X0} y1={Y1 - 20} x2={X0} y2={Y0} stroke={C.soft} strokeWidth={3} />
          {BEST_BAYES.map((_, i) => (
            <g key={i}>
              <line x1={px(i + 1)} y1={Y0} x2={px(i + 1)} y2={Y0 + 10} stroke={C.soft} strokeWidth={3} />
              <text x={px(i + 1)} y={Y0 + 52} textAnchor="middle" fontFamily={F.serif} fontSize={38} fill={C.soft}>
                {i + 1}
              </text>
            </g>
          ))}
          {[-24, -22, -20, -18].map((v) => (
            <g key={v}>
              <line x1={X0 - 10} y1={py(v)} x2={X0} y2={py(v)} stroke={C.soft} strokeWidth={3} />
              <text x={X0 - 20} y={py(v) + 13} textAnchor="end" fontFamily={F.serif} fontSize={38} fill={C.soft}>
                {`−${-v}`}
              </text>
            </g>
          ))}
          <text x={X1 + 30} y={Y0 + 112} textAnchor="end" fontFamily={F.hand} fontSize={45} fill={C.soft}>
            number of groups K
          </text>
          <text x={120} y={Y1 - 50} textAnchor="start" fontFamily={F.hand} fontSize={45} fill={C.soft}>
            Bayesian score
          </text>
          {BEST_BAYES.slice(1).map((v, i) => (
            <line key={i} x1={px(i + 1)} y1={py(BEST_BAYES[i])} x2={px(i + 2)} y2={py(v)} stroke={C.blue} strokeWidth={5} opacity={Math.min(dot(i), dot(i + 1))} />
          ))}
          {BEST_BAYES.map((v, i) => (
            <circle key={i} cx={px(i + 1)} cy={py(v)} r={15} fill={C.blue} stroke="#fff" strokeWidth={3} opacity={dot(i)} />
          ))}
          <circle cx={px(PEAK + 1)} cy={py(BEST_BAYES[PEAK])} r={26} fill="none" stroke={C.ink} strokeWidth={7} opacity={peak} />
        </g>
      </Canvas>
      <Fade o={plot * peak} dy={14}>
        <Box x={1230} y={380} w={580} size={50}>
          The score peaks at <Tex tex="K = 2" />
        </Box>
        <Cap x={1230} y={520} w={580} align="left">uniform priors, 8 nodes</Cap>
      </Fade>

      {/* stage 2 */}
      <Fade o={full} dy={14}>
        <Box x={260} y={290} w={1400} size={54}>
          <Term>K</Term> is inferred
        </Box>
        <Box x={260} y={410} w={1400} size={54}>
          groups within groups: <Term>nested</Term> SBM
        </Box>
        <Box x={260} y={530} w={1400} size={54}>
          uneven degrees: <Term>degree-corrected</Term> SBM
        </Box>
        <Box x={260} y={730} w={1400} size={40} color={C.soft}>
          Tiago Peixoto (2014, 2017, 2019)
        </Box>
      </Fade>
    </Frame>
  );
};
