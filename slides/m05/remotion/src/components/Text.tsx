import React from 'react';
import {C, F, S} from '../theme';

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
  const left = align === 'left' ? x : align === 'center' ? x - w / 2 : x - w;
  return (
    <div
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
export const Tag: React.FC<{x: number; y: number; hot?: boolean; children: React.ReactNode; style?: React.CSSProperties}> = ({x, y, hot, children, style}) => (
  <div
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
      background: hot ? C.redSoft : C.panel,
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
);
