import React from 'react';
import {C, F} from '../theme';

export type LoopBox = {text: string; w: number};

/** x of the left edge of box i in a row that starts at x */
export const boxLeft = (x: number, boxes: ReadonlyArray<LoopBox>, gap: number, i: number): number =>
  x + boxes.slice(0, i).reduce((s, b) => s + b.w + gap, 0);

/** width of the whole row */
export const loopWidth = (boxes: ReadonlyArray<LoopBox>, gap: number): number => boxes.reduce((s, b) => s + b.w, 0) + gap * (boxes.length - 1);

const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; o: number}> = ({x1, y1, x2, y2, o}) => {
  const a = Math.atan2(y2 - y1, x2 - x1);
  const L = 22;
  const wing = (s: number): string => `${x2 - L * Math.cos(a + s * 0.42)},${y2 - L * Math.sin(a + s * 0.42)}`;
  return (
    <g opacity={o}>
      <line x1={x1} y1={y1} x2={x2 - 10 * Math.cos(a)} y2={y2 - 10 * Math.sin(a)} stroke={C.ink} strokeWidth={4} />
      <polygon points={`${x2},${y2} ${wing(1)} ${wing(-1)}`} fill={C.ink} />
    </g>
  );
};

/**
 * A row of boxes joined by arrows, with an arrow that goes back under the row (the loop). Draw it inside a <Canvas>.
 * Box i and the arrow into it appear with appear[i] (0 to 1). The back arrow appears with back.appear.
 * The text of a box has fewer than five words, so it stays on the slide in the narrated video.
 */
export const LoopDiagram: React.FC<{
  x: number;
  y: number;
  boxes: ReadonlyArray<LoopBox>;
  appear: ReadonlyArray<number>;
  gap?: number;
  h?: number;
  font?: number;
  /** a small label above the arrow into box i (i >= 1) */
  arrowLabels?: ReadonlyArray<string | undefined>;
  back?: {from: number; to: number; label: string; appear: number};
}> = ({x, y, boxes, appear, gap = 90, h = 110, font = 38, arrowLabels, back}) => {
  const cy = y + h / 2;
  return (
    <g fontFamily={F.serif}>
      {boxes.map((b, i) => {
        const bx = boxLeft(x, boxes, gap, i);
        const o = appear[i] ?? 1;
        return (
          <g key={i} opacity={o} transform={`translate(0 ${(1 - o) * 14})`}>
            {i > 0 && <Arrow x1={bx - gap + 6} y1={cy} x2={bx - 8} y2={cy} o={1} />}
            {i > 0 && arrowLabels?.[i] && (
              <text x={bx - gap / 2} y={y + h / 2 - 22} textAnchor="middle" fontSize={32} fontFamily={F.hand} fill={C.soft}>
                {arrowLabels[i]}
              </text>
            )}
            <rect x={bx} y={y} width={b.w} height={h} rx={16} fill={C.panel} stroke={C.blue} strokeWidth={4} />
            <text x={bx + b.w / 2} y={cy + font * 0.34} textAnchor="middle" fontSize={font} fill={C.ink}>
              {b.text}
            </text>
          </g>
        );
      })}
      {back && (
        <g opacity={back.appear}>
          {(() => {
            const a = boxLeft(x, boxes, gap, back.from) + boxes[back.from].w / 2;
            const z = boxLeft(x, boxes, gap, back.to) + boxes[back.to].w / 2;
            const yb = y + h + 62;
            const r = 26;
            const d = `M${a} ${y + h + 6} L${a} ${yb - r} Q${a} ${yb} ${a - r} ${yb} L${z + r} ${yb} Q${z} ${yb} ${z} ${yb - r} L${z} ${y + h + 20}`;
            return (
              <>
                <path d={d} fill="none" stroke={C.ink} strokeWidth={4} />
                <polygon points={`${z},${y + h + 8} ${z - 12},${y + h + 30} ${z + 12},${y + h + 30}`} fill={C.ink} />
                <text x={(a + z) / 2} y={yb + 44} textAnchor="middle" fontSize={34} fontFamily={F.hand} fill={C.soft}>
                  {back.label}
                </text>
              </>
            );
          })()}
        </g>
      )}
    </g>
  );
};
