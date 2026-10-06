import React from 'react';
import {C} from '../theme';
import {LOOK, type Look} from './look';
import {KARATE_EDGES, KARATE_REAL} from '../data/data';
import type {Edge} from './network';
import {Canvas, FadeG} from '../components/Fade';
import {Box} from '../components/Text';
import {Tex} from '../components/Tex';

/** Shared by S01 to S03: the karate club in its two real groups, the edges coloured inside or between, and the right-hand panel of counts. */

export const EDGES = KARATE_EDGES as unknown as ReadonlyArray<Edge>;
export const REAL_LOOKS: Look[] = KARATE_REAL.map((g) => LOOK[g]);

type RGB = [number, number, number];
const rgb = (c: string): RGB => [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];
const blend = (a: RGB, b: RGB, t: number): RGB => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const css = (c: RGB): string => `rgb(${Math.round(c[0])}, ${Math.round(c[1])}, ${Math.round(c[2])})`;

const INK = rgb(C.ink);
const FAINT = rgb(C.faint);
const BLUE = rgb(LOOK[0].fill);
const ORANGE = rgb(LOOK[1].fill);

/** A disc between group 1 (orange, b = 0) and group 0 (blue, b = 1). */
export const discLook = (b: number): Look => ({...LOOK[0], fill: css(blend(ORANGE, BLUE, b))});

/** b[i] = 1 for a node of group 0 (blue), 0 for a node of group 1 (orange); in between while a node changes group. */
export const REAL_B: number[] = KARATE_REAL.map((g) => (g === 0 ? 1 : 0));

/**
 * Edge looks for the club. `b` says how blue each node is (see `discLook`); `p` goes from 0 (every edge plain, as in S01) to 1
 * (an edge inside a group has the colour of the group and is thick, an edge between groups is faint and thin).
 */
export const clubEdges = (b: ReadonlyArray<number>, p: number) => ({
  edgeLook: (_i: number, e: Edge) => {
    const s = 1 - Math.abs(b[e[0]] - b[e[1]]);
    const inside = blend(ORANGE, BLUE, (b[e[0]] + b[e[1]]) / 2);
    const target = blend(FAINT, inside, s);
    return {color: css(blend(INK, target, p)), w: 3.5 + (3 + 4 * s - 3.5) * p};
  },
  edgeOp: (_i: number, e: Edge) => 1 - 0.35 * p * Math.abs(b[e[0]] - b[e[1]]),
});

/** Layout of the right-hand panel (S02 and S03 share it, so S03 opens on the picture S02 ends with). */
export const PANEL_X = 1010;
export const ROW1_Y = 240;
export const ROW2_Y = 320;
export const FRAC_Y = 410;
export const PANEL_W = 800;

/** the two legend lines: inside edges (blue and orange) and edges between groups (faint) */
export const Legend: React.FC<{o1: number; o2: number}> = ({o1, o2}) => (
  <Canvas>
    <FadeG o={o1}>
      <line x1={PANEL_X} y1={ROW1_Y + 40} x2={PANEL_X + 38} y2={ROW1_Y + 40} stroke={LOOK[0].fill} strokeWidth={7} strokeLinecap="round" />
      <line x1={PANEL_X + 46} y1={ROW1_Y + 40} x2={PANEL_X + 84} y2={ROW1_Y + 40} stroke={LOOK[1].fill} strokeWidth={7} strokeLinecap="round" />
    </FadeG>
    <FadeG o={o2}>
      <line x1={PANEL_X} y1={ROW2_Y + 40} x2={PANEL_X + 84} y2={ROW2_Y + 40} stroke={C.faint} strokeWidth={3} strokeLinecap="round" />
    </FadeG>
  </Canvas>
);

/** "inside: 67" and "between: 11" (labels: they stay on the slide in the video) */
export const CountRow: React.FC<{y: number; label: string; n: number; o: number}> = ({y, label, n, o}) => (
  <div style={{opacity: o}}>
    <Box x={PANEL_X + 112} y={y} w={PANEL_W - 112} size={56}>
      {label}: <b>{n}</b>
    </Box>
  </div>
);

/** the fraction of edges inside: inside / M = value */
export const Fraction: React.FC<{inside: number; m: number; value: string; red?: boolean; o: number}> = ({inside, m, value, red, o}) => (
  <div style={{opacity: o}}>
    <Box x={PANEL_X} y={FRAC_Y} w={PANEL_W} size={68}>
      <Tex tex={`\\dfrac{${inside}}{${m}}=${red ? `\\textcolor{#B14434}{\\mathbf{${value}}}` : value}`} />
    </Box>
  </div>
);
