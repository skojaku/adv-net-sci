import type {CSSProperties} from 'react';
import {Easing, interpolate} from 'remotion';

export const FPS = 30;

const outCurve = Easing.bezier(0.22, 1, 0.36, 1);
const inOutCurve = Easing.bezier(0.65, 0, 0.35, 1);

const clampOpts = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** 0 to 1 between frames a and b (a < b), ease-out. */
export const prog = (frame: number, a: number, b: number): number =>
  interpolate(frame, [a, b], [0, 1], {...clampOpts, easing: outCurve});

/** 0 to 1 between frames a and b (a < b), ease-in-out. */
export const smooth = (frame: number, a: number, b: number): number =>
  interpolate(frame, [a, b], [0, 1], {...clampOpts, easing: inOutCurve});

/** Linear 0 to 1 between frames a and b (a < b). */
export const lin = (frame: number, a: number, b: number): number =>
  interpolate(frame, [a, b], [0, 1], clampOpts);

/**
 * Stage i animates from stageStart(i) to marks[i].
 * Stage 0 starts at frame 0. Stage i starts where stage i-1 ends.
 */
export const stageStart = (marks: number[], i: number): number => (i === 0 ? 0 : marks[i - 1]);

/** Opacity of something shown only during stage i. The last stage never fades out. */
export const caption = (frame: number, marks: number[], i: number, fade = 10): number => {
  const s = stageStart(marks, i);
  const fadeIn = prog(frame, s, s + fade);
  const fadeOut = i >= marks.length - 1 ? 0 : prog(frame, marks[i], marks[i] + fade);
  return fadeIn * (1 - fadeOut);
};

/** Opacity of something that appears at stage `from` and stays to the end. */
export const fromStage = (frame: number, marks: number[], from: number, fade = 14): number => {
  const s = stageStart(marks, from);
  return prog(frame, s, s + fade);
};

/** Opacity of something shown from stage `from` up to and including stage `to`. */
export const betweenStages = (frame: number, marks: number[], from: number, to: number, fade = 12): number => {
  const s = stageStart(marks, from);
  const fin = to >= marks.length - 1 ? 0 : prog(frame, marks[to], marks[to] + fade);
  return prog(frame, s, s + fade) * (1 - fin);
};

/** Fade and slide-up style for an element that appears at `start`. */
export const reveal = (frame: number, start: number, dur = 20, dy = 24): CSSProperties => {
  const p = prog(frame, start, start + dur);
  return {opacity: p, transform: `translateY(${(1 - p) * dy}px)`};
};

/**
 * values[j] is reached at frame knots[j]. Eased inside each segment.
 * knots must be strictly increasing.
 */
export const piecewise = (frame: number, knots: number[], values: number[]): number => {
  if (frame <= knots[0]) return values[0];
  for (let j = 1; j < knots.length; j++) {
    if (frame <= knots[j]) {
      const t = (frame - knots[j - 1]) / (knots[j] - knots[j - 1]);
      return values[j - 1] + (values[j] - values[j - 1]) * inOutCurve(t);
    }
  }
  return values[values.length - 1];
};

/**
 * A value that moves through `vals` one step at a time: it holds, then eases to the next
 * value, then holds. Step k starts at start + k * per and takes `move` frames.
 */
export const stepped = (frame: number, start: number, per: number, move: number, vals: number[]): number => {
  const knots: number[] = [start];
  const values: number[] = [vals[0]];
  for (let k = 1; k < vals.length; k++) {
    const t0 = start + (k - 1) * per + (per - move);
    knots.push(t0, t0 + move);
    values.push(vals[k - 1], vals[k]);
  }
  return piecewise(frame, knots, values);
};
