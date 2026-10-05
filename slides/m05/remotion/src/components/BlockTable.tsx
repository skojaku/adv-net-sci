import React from 'react';
import {C, F} from '../theme';
import {mix} from '../lib/network';
import {LOOK} from '../lib/look';

/**
 * A 2 x 2 table of block probabilities for two groups (blue, orange). The fill of a cell is blue in
 * proportion to its value. `text` overrides the printed value (for example "5 / 6"). `hot` marks cells with an outline.
 */
export const BlockTable: React.FC<{
  x: number;
  y: number;
  cell?: number;
  p: [[number, number], [number, number]];
  text?: [[string, string], [string, string]];
  hot?: [[boolean, boolean], [boolean, boolean]];
  opacity?: number;
  fontSize?: number;
}> = ({x, y, cell = 150, p, text, hot, opacity = 1, fontSize = 44}) => {
  const chip = cell * 0.34;
  return (
    <g opacity={opacity}>
      {[0, 1].map((k) => (
        <g key={k}>
          <circle cx={x + cell * (k + 0.5)} cy={y - chip * 0.9} r={chip / 2 - LOOK[k].sw / 2} fill={LOOK[k].fill} stroke="#fff" strokeWidth={LOOK[k].sw} />
          <circle cx={x - chip * 0.9} cy={y + cell * (k + 0.5)} r={chip / 2 - LOOK[k].sw / 2} fill={LOOK[k].fill} stroke="#fff" strokeWidth={LOOK[k].sw} />
        </g>
      ))}
      {[0, 1].map((r) =>
        [0, 1].map((c) => (
          <g key={`${r}${c}`}>
            <rect
              x={x + c * cell}
              y={y + r * cell}
              width={cell}
              height={cell}
              fill={mix('#ffffff', C.blue, 0.5 * Math.min(1, p[r][c]))}
              stroke={hot?.[r][c] ? C.ink : C.soft}
              strokeWidth={hot?.[r][c] ? 8 : 3}
            />
            <text
              x={x + (c + 0.5) * cell}
              y={y + (r + 0.5) * cell + fontSize * 0.34}
              textAnchor="middle"
              fontFamily={F.serif}
              fontSize={fontSize}
              fill={C.ink}
            >
              {text ? text[r][c] : p[r][c].toFixed(2).replace(/0$/, '')}
            </text>
          </g>
        )),
      )}
    </g>
  );
};
