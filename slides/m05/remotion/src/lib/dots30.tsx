import React from 'react';
import {LOOK} from './look';

// The 30 nodes of S11, S12 and S19: 5 true groups of 6 nodes, each drawn as a block of 3 x 2 nodes.
// The groups are told apart by colour (LOOK[0..4]).

export const NDOT = 30;

/** The true group of node i (0 to 4). Matches SHUFFLES in data.ts, which permute these labels. */
export const TRUE30: ReadonlyArray<number> = Array.from({length: NDOT}, (_, i) => Math.floor(i / 6));

/**
 * Centre of node i. (x0, y0) is the centre of node 0, `pitch` the distance between neighbours in a
 * block, `stride` the distance between the same node of two neighbouring blocks.
 */
export const dotCentre = (i: number, x0: number, y0: number, pitch: number, stride: number): readonly [number, number] => {
  const g = Math.floor(i / 6);
  const k = i % 6;
  return [x0 + g * stride + (k % 3) * pitch, y0 + Math.floor(k / 3) * pitch] as const;
};

/** A start position for node i that looks scattered but is a fixed formula (no randomness at render time). */
export const scatter = (i: number, x: number, y: number, w: number, h: number): readonly [number, number] => {
  const f = (v: number) => v - Math.floor(v);
  return [x + f(i * 0.6180339887 + 0.17) * w, y + f(i * 0.7548776662 + 0.41) * h] as const;
};

/**
 * One node of the 30, drawn with the Look of group `g`. With `gTo` and `t` it cross-fades to the look of
 * group `gTo` (never a blend of colours). The disc is drawn at the origin of a translated group, so a stripe
 * pattern moves with it.
 */
export const NodeDot: React.FC<{x: number; y: number; d: number; g: number; gTo?: number; t?: number; op?: number}> = ({x, y, d, g, gTo, t = 0, op = 1}) => {
  const a = LOOK[g];
  const b = gTo === undefined ? null : LOOK[gTo];
  return (
    <g transform={`translate(${x} ${y})`} opacity={op}>
      <circle r={d / 2 - a.sw / 2} fill={a.fill} stroke={a.stroke} strokeWidth={a.sw} />
      {b && t > 0.001 && <circle r={d / 2 - b.sw / 2} fill={b.fill} stroke={b.stroke} strokeWidth={b.sw} opacity={t} />}
    </g>
  );
};
