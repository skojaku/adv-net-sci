import React from 'react';

/** A full-canvas layer with an opacity and a slide-up offset. Children are positioned absolutely. */
export const Fade: React.FC<{o: number; dy?: number; children: React.ReactNode}> = ({o, dy = 0, children}) => (
  <div
    style={{
      position: 'absolute',
      left: 0,
      top: 0,
      width: 1920,
      height: 1080,
      opacity: o,
      transform: dy ? `translateY(${(1 - o) * dy}px)` : undefined,
      pointerEvents: 'none',
    }}
  >
    {children}
  </div>
);

/** The same for SVG: a group at canvas coordinates. */
export const FadeG: React.FC<{o: number; children: React.ReactNode}> = ({o, children}) => <g opacity={o}>{children}</g>;

export const Canvas: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
    {children}
  </svg>
);
