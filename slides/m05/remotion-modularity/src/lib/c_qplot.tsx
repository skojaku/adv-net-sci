import React from 'react';
import {C, F} from '../theme';
import {lerp} from './plot';

export type Tick = {v: number; label: string};

/**
 * A small plot of Q: dots joined by a line (never bars). Draw it inside a <Canvas> (canvas coordinates).
 * `shown` is how many points are visible; it may be fractional: the next point is then drawn part of the way.
 * The last visible point is a larger dot.
 */
export const QPlot: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  xs: ReadonlyArray<number>;
  ys: ReadonlyArray<number>;
  shown: number;
  xMin: number;
  xMax: number;
  yMin: number;
  yMax: number;
  xTicks: ReadonlyArray<Tick>;
  yTicks: ReadonlyArray<Tick>;
  xLabel?: string;
  yLabel?: string;
  dotR?: number;
  /** the last point is hollow and the segment to it dashed (a step that changed nothing) */
  lastHollow?: boolean;
  opacity?: number;
  /** a text beside each point, drawn once the point is shown */
  pointLabels?: ReadonlyArray<string>;
  /** the labels of these points go beside the point, level with it, instead of above it */
  labelBelow?: ReadonlyArray<number>;
}> = ({x, y, w, h, xs, ys, shown, xMin, xMax, yMin, yMax, xTicks, yTicks, xLabel, yLabel, dotR = 6, lastHollow, opacity = 1, pointLabels, labelBelow = []}) => {
  const px = (v: number) => x + ((v - xMin) / (xMax - xMin)) * w;
  const py = (v: number) => y + h - ((v - yMin) / (yMax - yMin)) * h;
  const n = xs.length;
  const full = Math.min(n, Math.floor(shown));
  const part = shown - Math.floor(shown);
  const pts: Array<[number, number]> = [];
  for (let i = 0; i < full; i++) pts.push([px(xs[i]), py(ys[i])]);
  let head: [number, number] | null = pts.length ? pts[pts.length - 1] : null;
  if (full < n && part > 0 && pts.length) {
    const [a, b] = [pts[pts.length - 1], [px(xs[full]), py(ys[full])] as [number, number]];
    head = [lerp(a[0], b[0], part), lerp(a[1], b[1], part)];
  }
  const line = [...pts, ...(head && head !== pts[pts.length - 1] ? [head] : [])];
  const lastIdx = pts.length - 1;
  const solidPts = lastHollow && pts.length === n ? line.slice(0, -1) : line;
  const d = (a: Array<[number, number]>) => a.map(([X, Y], i) => `${i === 0 ? 'M' : 'L'}${X.toFixed(1)} ${Y.toFixed(1)}`).join(' ');
  return (
    <g opacity={opacity} fontFamily={F.serif}>
      {yTicks.map((t) => (
        <g key={`y${t.v}`}>
          <line x1={x} x2={x + w} y1={py(t.v)} y2={py(t.v)} stroke={t.v === 0 ? C.faint : C.rule} strokeWidth={t.v === 0 ? 3 : 2} />
          <text x={x - 16} y={py(t.v) + 11} textAnchor="end" fontSize={32} fill={C.soft}>
            {t.label}
          </text>
        </g>
      ))}
      <line x1={x} x2={x} y1={y} y2={y + h} stroke={C.soft} strokeWidth={3} />
      <line x1={x} x2={x + w} y1={y + h} y2={y + h} stroke={C.soft} strokeWidth={3} />
      {xTicks.map((t) => (
        <g key={`x${t.v}`}>
          <line x1={px(t.v)} x2={px(t.v)} y1={y + h} y2={y + h + 10} stroke={C.soft} strokeWidth={3} />
          <text x={px(t.v)} y={y + h + 46} textAnchor="middle" fontSize={32} fill={C.soft}>
            {t.label}
          </text>
        </g>
      ))}
      {xLabel && (
        <text x={x + w} y={y + h + 90} textAnchor="end" fontSize={34} fill={C.soft} fontFamily={F.hand}>
          {xLabel}
        </text>
      )}
      {yLabel && (
        <text x={x - 16} y={y - 22} textAnchor="end" fontSize={38} fill={C.soft} fontStyle="italic">
          {yLabel}
        </text>
      )}
      {solidPts.length > 1 && <path d={d(solidPts)} fill="none" stroke={C.blue} strokeWidth={4.5} strokeLinejoin="round" />}
      {lastHollow && pts.length === n && n > 1 && (
        <path d={d(pts.slice(-2))} fill="none" stroke={C.blue} strokeWidth={4.5} strokeDasharray="10 9" />
      )}
      {pts.map(([X, Y], i) => {
        const hollow = lastHollow && i === n - 1;
        const isHead = i === lastIdx && full < n + 1;
        return (
          <circle
            key={i}
            cx={X}
            cy={Y}
            r={isHead ? dotR * 1.5 : dotR}
            fill={hollow ? '#fff' : C.blue}
            stroke={C.blue}
            strokeWidth={hollow ? 4 : 0}
          />
        );
      })}
      {pointLabels &&
        pts.map(([X, Y], i) => (
          <text key={`l${i}`} x={X + 18} y={labelBelow.includes(i) ? Y + 12 : Y - 18} fontSize={34} fill={C.ink}>
            {pointLabels[i]}
          </text>
        ))}
    </g>
  );
};
