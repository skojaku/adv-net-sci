import React from 'react';
import {C, F} from '../theme';
import {LOOK} from '../lib/look';
import {Disc} from '../lib/eight';

/** The 2 x 2 table of S09 to S19: rows are the true groups (blue, orange), columns the found groups A and B, plus margins. */
export const GX = 600;
export const GY = 350;
export const CW = 210;
export const CH = 140;
export const MARG = 170;

export const cellC = (r: number, c: number) => [GX + (c + 0.5) * CW, GY + (r + 0.5) * CH] as const;
export const rowSumC = (r: number) => [GX + 2 * CW + 20 + MARG / 2, GY + (r + 0.5) * CH] as const;
export const colSumC = (c: number) => [GX + (c + 0.5) * CW, GY + 2 * CH + 20 + 60] as const;

/** A number written in a cell. */
export const Num: React.FC<{at: readonly [number, number]; text: string; size?: number; op?: number; bold?: boolean; color?: string}> = ({at, text, size = 60, op = 1, bold, color = C.ink}) => (
  <text x={at[0]} y={at[1] + size * 0.34} textAnchor="middle" fontFamily={F.serif} fontSize={size} fontWeight={bold ? 700 : 400} fill={color} opacity={op}>
    {text}
  </text>
);

/**
 * The frame of the table with its headers. `rowsOp` and `colsOp` fade in the margin cells (where the row sums and
 * column sums go); `hot` outlines cells.
 */
export const ProbGrid: React.FC<{rowsOp?: number; colsOp?: number; hot?: [number, number][]; op?: number}> = ({rowsOp = 0, colsOp = 0, hot = [], op = 1}) => (
  <g opacity={op}>
    {[0, 1].map((r) =>
      [0, 1].map((c) => (
        <rect key={`${r}${c}`} x={GX + c * CW} y={GY + r * CH} width={CW} height={CH} fill="#fff" stroke={C.faint} strokeWidth={3} />
      )),
    )}
    {hot.map(([r, c]) => (
      <rect key={`h${r}${c}`} x={GX + c * CW + 4} y={GY + r * CH + 4} width={CW - 8} height={CH - 8} fill="none" stroke={C.blue} strokeWidth={7} />
    ))}
    {/* the true groups down the left */}
    {[0, 1].map((r) => (
      <Disc key={r} x={GX - 70} y={GY + r * CH + CH / 2} d={64} look={LOOK[r]} />
    ))}
    {/* the found groups across the top */}
    {['A', 'B'].map((l, c) => (
      <g key={l}>
        <rect x={GX + (c + 0.5) * CW - 46} y={GY - 96} width={92} height={70} rx={20} fill={C.blueMid} stroke={C.blue} strokeWidth={3} />
        <text x={GX + (c + 0.5) * CW} y={GY - 46} textAnchor="middle" fontFamily={F.serif} fontSize={48} fontWeight={700} fill={C.ink}>
          {l}
        </text>
      </g>
    ))}
    <g opacity={rowsOp}>
      {[0, 1].map((r) => (
        <rect key={r} x={GX + 2 * CW + 20} y={GY + r * CH} width={MARG} height={CH} fill={C.panel} stroke={C.faint} strokeWidth={3} />
      ))}
    </g>
    <g opacity={colsOp}>
      {[0, 1].map((c) => (
        <rect key={c} x={GX + c * CW} y={GY + 2 * CH + 20} width={CW} height={120} fill={C.panel} stroke={C.faint} strokeWidth={3} />
      ))}
    </g>
  </g>
);
