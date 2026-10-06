import React, {useContext, useLayoutEffect, useRef} from 'react';
import {C, F, S} from '../theme';
import {Tex} from './Tex';

/**
 * What a slide does with its sentences. 'show' (the default: the deck, the review stills, the student html) draws everything. The narrated
 * video (src/video/) wraps the slides in 'hide', which leaves out every sentence (a Box, Cap or Tag with at least five words and no formula; numbers and short labels are not sentences), and
 * scripts/collect_prose.mjs wraps them in 'collect', which reports each visible sentence to the browser log: the video types those words
 * in the chat instead. Labels (fewer than five words), numbers, figures and formulas always stay on the slide.
 */
export type ProseMode = 'show' | 'hide' | 'collect';
export const ProseContext = React.createContext<ProseMode>('show');

const hasTex = (node: React.ReactNode): boolean => {
  if (Array.isArray(node)) return node.some(hasTex);
  if (!React.isValidElement(node)) return false;
  if (node.type === Tex) return true;
  return hasTex((node.props as {children?: React.ReactNode}).children);
};
const textOf = (node: React.ReactNode): string => {
  if (node === null || node === undefined || typeof node === 'boolean') return '';
  if (typeof node === 'string' || typeof node === 'number') return String(node);
  if (Array.isArray(node)) return node.map(textOf).join('');
  if (React.isValidElement(node)) return node.type === 'br' ? ' ' : textOf((node.props as {children?: React.ReactNode}).children);
  return '';
};
/** a sentence of the slide that the video moves into the chat */
const proseOf = (children: React.ReactNode): string | null => {
  if (hasTex(children)) return null;
  const text = textOf(children).replace(/\s+/g, ' ').trim();
  return (text.match(/[A-Za-z]{2,}/g)?.length ?? 0) >= 5 ? text : null;
};

/** Reports a visible sentence (its words, and where it is) to the browser console, for scripts/collect_prose.mjs. */
const useReport = (mode: ProseMode, text: string | null) => {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    if (mode !== 'collect' || !text || !ref.current) return;
    let o = 1;
    for (let el: HTMLElement | null = ref.current; el; el = el.parentElement) o *= Number(getComputedStyle(el).opacity);
    const r = ref.current.getBoundingClientRect();
    // eslint-disable-next-line no-console
    console.log('PROSE ' + JSON.stringify({text, visible: o > 0.5, x: Math.round(r.left), y: Math.round(r.top)}));
  });
  return ref;
};

/** A key term: red and bold, exactly like `strong` in the Marp theme. */
export const Term: React.FC<{children: React.ReactNode}> = ({children}) => (
  <span style={{color: C.red, fontWeight: 700}}>{children}</span>
);

type BoxProps = {
  x: number;
  y: number;
  w?: number;
  size?: number;
  color?: string;
  align?: 'left' | 'center' | 'right';
  hand?: boolean;
  style?: React.CSSProperties;
  children: React.ReactNode;
};

/** Positioned text. `x` is the left edge (or the centre / right edge when `align` says so). */
export const Box: React.FC<BoxProps> = ({x, y, w = 1680, size = S.body, color = C.ink, align = 'left', hand, style, children}) => {
  const mode = useContext(ProseContext);
  const prose = mode === 'show' ? null : proseOf(children);
  const ref = useReport(mode, prose);
  if (mode === 'hide' && prose) return null;
  const left = align === 'left' ? x : align === 'center' ? x - w / 2 : x - w;
  return (
    <div
      ref={ref}
      style={{
        position: 'absolute',
        left,
        top: y,
        width: w,
        textAlign: align,
        fontSize: size,
        lineHeight: 1.35,
        color,
        fontFamily: hand ? F.hand : F.serif,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** A caption under a figure, in the deck's grey handwriting. */
export const Cap: React.FC<{x?: number; y: number; w?: number; align?: 'left' | 'center'; style?: React.CSSProperties; children: React.ReactNode}> = ({
  x = 960,
  y,
  w = 1560,
  align = 'center',
  style,
  children,
}) => (
  <Box x={align === 'center' ? x : x} y={y} w={w} align={align} size={S.hand} color={C.soft} hand style={style}>
    {children}
  </Box>
);

/** A number tag such as "Q = 0.650". */
export const Tag: React.FC<{x: number; y: number; hot?: boolean; children: React.ReactNode; style?: React.CSSProperties}> = ({x, y, hot, children, style}) => {
  const mode = useContext(ProseContext);
  const prose = mode === 'show' ? null : proseOf(children);
  const ref = useReport(mode, prose);
  if (mode === 'hide' && prose) return null;
  return (
  <div
    ref={ref}
    style={{
      position: 'absolute',
      left: x,
      top: y,
      transform: 'translateX(-50%)',
      fontFamily: F.serif,
      fontSize: 48,
      fontWeight: hot ? 700 : 400,
      color: hot ? C.red : C.ink,
      padding: '6px 26px',
      background: C.panel,
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
  );
};
