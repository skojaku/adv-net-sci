import React from 'react';
import {Frame} from '../components/Frame';
import {Tex} from '../components/Tex';
import {FormulaStack} from '../components/FormulaStack';

/**
 * The degree-corrected SBM (Karrer and Newman 2011): every node gets a number theta_i.
 * 0: the SBM: the groups alone decide the probability of an edge.
 * 1: the degree-corrected SBM: the number of edges between i and j is Poisson with mean theta_i theta_j omega_{c_i c_j};
 *    theta_i: how many edges node i tends to make.
 */
export const marks = [56, 112];

const sym = (tex: string, text: string) => (
  <div>
    <Tex tex={tex} style={{fontSize: 40}} />
    <span>: {text}</span>
  </div>
);
const ROWS = [
  {group: 0, label: 'SBM', tex: 'P(A_{ij}=1\\mid c,p)=p_{c_ic_j}'},
  {
    group: 1,
    label: 'degree-corrected SBM',
    tex: 'A_{ij}\\sim\\mathrm{Poisson}\\big(\\theta_i\\,\\theta_j\\,\\omega_{c_ic_j}\\big)',
    note: (
      <>
        {sym('A_{ij}', 'the number of edges between i and j')}
        {sym('\\theta_i', 'how many edges node i tends to make')}
        {sym('\\omega_{rs}', 'how many edges groups r and s tend to share')}
      </>
    ),
  },
] as const;

export const S35: React.FC = () => {
  return (
    <Frame n={35} zoom={1.3} top={120}>
      <FormulaStack rows={ROWS} marks={marks} x={300} y={200} w={1380} big={52} small={42} gap={26} labelW={360} />
    </Frame>
  );
};
