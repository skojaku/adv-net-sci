import React from 'react';
import {C, F} from '../theme';
import {TRUTH8} from './metrics';
import {lerp} from './plot';
import {BAND_SOLID, HOLLOW, LOOK, type Look} from './look';

// The eight-node example drawn as two rows (the true groups on top, the found groups below as boxes).
// Used by S09, S10, S12 and S19. Node i (0-based) is labelled i + 1.
// True groups: nodes 1 to 4 are group 0 (blue), nodes 5 to 8 group 1 (orange).

export const trueLook = (i: number): Look => (TRUTH8[i] === 0 ? LOOK[0] : LOOK[1]);

export type RowGeom = {x0: number; pitch: number; d: number; yTrue: number; yFound: number};
export type Ranges = ReadonlyArray<readonly [number, number]>;

/** The found groups of S09 to S12: A = nodes 1 to 5, B = nodes 6 to 8. */
export const AB: Ranges = [
  [0, 4],
  [5, 7],
];
/** The found split of S19: every node alone. */
export const ALONE: Ranges = [0, 1, 2, 3, 4, 5, 6, 7].map((i) => [i, i] as const);

export const nodeX = (g: RowGeom, i: number): number => g.x0 + i * g.pitch;
export const rowCentre = (g: RowGeom): number => g.x0 + 3.5 * g.pitch;
export const boxPad = (g: RowGeom): number => 0.7 * g.d;

export const mixGeom = (a: RowGeom, b: RowGeom, t: number): RowGeom => ({
  x0: lerp(a.x0, b.x0, t),
  pitch: lerp(a.pitch, b.pitch, t),
  d: lerp(a.d, b.d, t),
  yTrue: lerp(a.yTrue, b.yTrue, t),
  yFound: lerp(a.yFound, b.yFound, t),
});

/** A disc with a node number in it, drawn with a Look. `ring` in [0, 1] draws a black ring around it. */
export const Disc: React.FC<{
  x: number;
  y: number;
  d: number;
  look: Look;
  label?: string | number;
  ring?: number;
  /** colour of the ring (default black) */
  ringColor?: string;
  op?: number;
  scale?: number;
}> = ({x, y, d, look, label, ring = 0, ringColor = C.ink, op = 1, scale = 1}) => {
  const fs = Math.max(34, d * 0.48);
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={op}>
      {ring > 0.001 && <circle r={d / 2 + 9} fill="none" stroke={ringColor} strokeWidth={7} opacity={ring} />}
      <circle r={d / 2 - look.sw / 2} fill={look.fill} stroke={look.stroke} strokeWidth={look.sw} />
      {label != null && (
        <text y={fs * 0.35} textAnchor="middle" fontFamily={F.serif} fontSize={fs} fontWeight={700} fill={look.text}>
          {label}
        </text>
      )}
    </g>
  );
};

/** The found groups as rounded light-blue boxes. `names` writes A and B under the boxes. */
export const FoundBoxes: React.FC<{g: RowGeom; ranges?: Ranges; op?: number; names?: boolean}> = ({g, ranges = AB, op = 1, names = true}) => {
  const pad = boxPad(g);
  return (
    <g opacity={op}>
      {ranges.map(([a, b], k) => {
        const x = nodeX(g, a) - pad;
        const w = nodeX(g, b) - nodeX(g, a) + 2 * pad;
        return (
          <g key={k}>
            <rect x={x} y={g.yFound - pad} width={w} height={2 * pad} rx={0.3 * g.d} fill={BAND_SOLID} stroke={C.blue} strokeWidth={3} />
            {names && (
              <text x={x + w / 2} y={g.yFound + pad + 50} textAnchor="middle" fontFamily={F.hand} fontSize={45} fill={C.soft}>
                {k === 0 ? 'A' : 'B'}
              </text>
            )}
          </g>
        );
      })}
    </g>
  );
};

/**
 * Both rows. `foundT(i)` in [0, 1] is how far node i of the lower row has slid from the true row to
 * its place (so the lower row can be built from copies of the upper one). `under` is drawn between
 * the boxes and the discs.
 */
export const EightRows: React.FC<{
  g: RowGeom;
  found?: Ranges;
  trueOp?: (i: number) => number;
  foundOp?: (i: number) => number;
  foundT?: (i: number) => number;
  boxOp?: number;
  names?: boolean;
  ringTrue?: (i: number) => number;
  ringFound?: (i: number) => number;
  ringColor?: (i: number) => string;
  under?: React.ReactNode;
}> = ({g, found = AB, trueOp = () => 1, foundOp = () => 1, foundT = () => 1, boxOp = 1, names = true, ringTrue, ringFound, ringColor, under}) => {
  const idx = [0, 1, 2, 3, 4, 5, 6, 7];
  return (
    <g>
      {boxOp > 0.001 && <FoundBoxes g={g} ranges={found} op={boxOp} names={names} />}
      {under}
      {idx.map((i) => {
        const o = trueOp(i);
        return o > 0.001 ? (
          <Disc key={`t${i}`} x={nodeX(g, i)} y={g.yTrue} d={g.d} look={trueLook(i)} label={i + 1} ring={ringTrue?.(i) ?? 0} ringColor={ringColor?.(i)} op={o} scale={0.7 + 0.3 * o} />
        ) : null;
      })}
      {idx.map((i) => {
        const o = foundOp(i);
        return o > 0.001 ? (
          <Disc key={`f${i}`} x={nodeX(g, i)} y={lerp(g.yTrue, g.yFound, foundT(i))} d={g.d} look={trueLook(i)} label={i + 1} ring={ringFound?.(i) ?? 0} ringColor={ringColor?.(i)} op={o} />
        ) : null;
      })}
    </g>
  );
};

/**
 * A pair of nodes as an icon: two white discs joined by a black line, centred on (x, y). The verdict is the
 * edge (outline) of the two discs: blue when the two splits agree about the pair, red when they disagree.
 * Without `agree` the discs are plain white nodes with a blue edge. Pass `looks` to draw the nodes in their true looks.
 */
export const PairIcon: React.FC<{x: number; y: number; agree?: boolean; a?: number; b?: number; looks?: boolean; d?: number; gap?: number}> = ({x, y, agree, a = 0, b = 0, looks = false, d = 26, gap = 42}) => (
  <g>
    <line x1={x - gap / 2} y1={y} x2={x + gap / 2} y2={y} stroke={C.ink} strokeWidth={4} />
    {[
      [a, -gap / 2],
      [b, gap / 2],
    ].map(([i, dx]) => {
      const lk = looks ? trueLook(i) : HOLLOW;
      const edge = agree === undefined ? (lk.stroke === '#fff' ? C.blue : lk.stroke) : agree ? C.blue : C.red;
      const sw = agree === undefined ? Math.min(lk.sw, 4) : 7;
      return <circle key={dx} cx={x + dx} cy={y} r={d / 2 - sw / 2} fill={agree === undefined ? lk.fill : '#fff'} stroke={edge} strokeWidth={sw} />;
    })}
  </g>
);

/** A check (blue) or a cross (red), drawn, so it does not depend on a font. */
export const Glyph: React.FC<{kind: 'check' | 'cross'; size: number}> = ({kind, size}) => (
  <svg width={size} height={size} viewBox="0 0 40 40" style={{display: 'block'}}>
    {kind === 'check' ? (
      <path d="M5 21 L15 31 L35 9" fill="none" stroke={C.blue} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
    ) : (
      <path d="M7 7 L33 33 M33 7 L7 33" fill="none" stroke={C.red} strokeWidth={6} strokeLinecap="round" />
    )}
  </svg>
);

/** "agree" in blue with a check, or "disagree" in red with a cross (emphasised text), centred on x. */
export const Verdict: React.FC<{x: number; y: number; agree: boolean; size?: number}> = ({x, y, agree, size = 54}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      transform: 'translateX(-50%)',
      display: 'flex',
      alignItems: 'center',
      gap: size * 0.25,
      fontFamily: F.serif,
      fontSize: size,
      lineHeight: 1.2,
      color: agree ? C.blue : C.red,
      whiteSpace: 'nowrap',
    }}
  >
    <Glyph kind={agree ? 'check' : 'cross'} size={size * 0.8} />
    <span>{agree ? 'agree' : 'disagree'}</span>
  </div>
);

/** A stacked fraction made of text. */
export const Frac: React.FC<{top: React.ReactNode; bottom: React.ReactNode}> = ({top, bottom}) => (
  <span style={{display: 'inline-flex', flexDirection: 'column', alignItems: 'center', lineHeight: 1.25, margin: '0 4px'}}>
    <span style={{padding: '0 10px 4px'}}>{top}</span>
    <span style={{alignSelf: 'stretch', height: 3, background: C.ink}} />
    <span style={{padding: '4px 10px 0'}}>{bottom}</span>
  </span>
);
