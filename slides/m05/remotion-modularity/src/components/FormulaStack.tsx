import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {Tex} from './Tex';
import {prog, stageStart} from '../lib/anim';
import {lerp} from '../lib/plot';

export type StackRow = {
  /** rows of one group are large together and become small together (so that their = signs stay one under the other) */
  group: number;
  tex: string;
  /** a short name in a column to the left of the formula */
  label?: string;
  /** small grey text under the formula (definitions); it moves with the rows and has a size of its own */
  note?: React.ReactNode;
};

/**
 * Formulas added one per stage (row k appears in stage k), each under the last. The newest group is large, the older ones a
 * little smaller; no marker. The rows are in normal flow, so the rows below move as the ones above change size.
 * Nothing is removed: every formula stays to the end.
 */
export const FormulaStack: React.FC<{
  rows: ReadonlyArray<StackRow>;
  marks: number[];
  x: number;
  y: number;
  w: number;
  big: number;
  small: number;
  gap?: number;
  labelW?: number;
}> = ({rows, marks, x, y, w, big, small, gap = 20, labelW = 0}) => {
  const frame = useCurrentFrame();
  const enter = (k: number) => prog(frame, stageStart(marks, k) + (k === 0 ? 6 : 4), stageStart(marks, k) + (k === 0 ? 24 : 22));
  const first = (g: number) => rows.findIndex((r) => r.group === g);
  // a group is large from the moment its first row appears until the first row of the next group appears
  const bigness = (g: number) => {
    const next = first(g + 1);
    return next < 0 ? 1 : 1 - prog(frame, stageStart(marks, next) + 4, stageStart(marks, next) + 22);
  };
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, fontFamily: F.serif, color: C.ink, lineHeight: 1.3}}>
      {rows.map((r, k) => {
        const o = enter(k);
        return (
          <div
            key={k}
            style={{
              opacity: o,
              marginBottom: gap,
              fontSize: lerp(small, big, bigness(r.group)),
              transform: `translateY(${(1 - o) * 14}px)`,
            }}
          >
            <div style={{display: 'flex', alignItems: 'center'}}>
              {labelW > 0 && <span style={{width: labelW, flex: 'none', fontFamily: F.hand, fontSize: 40, lineHeight: 1.1, color: C.soft}}>{r.label}</span>}
              <Tex tex={r.tex} />
            </div>
            {r.note && <div style={{fontSize: 34, lineHeight: 1.4, color: C.soft, marginLeft: labelW, marginTop: 4}}>{r.note}</div>}
          </div>
        );
      })}
    </div>
  );
};
