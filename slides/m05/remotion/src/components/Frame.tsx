import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, F, S} from '../theme';
import {prog} from '../lib/anim';

export const TOTAL = 23;

/** A content slide: title, the rule under it, the page number. Same as the Marp theme at 1.5x. */
export const Frame: React.FC<{n: number; title: string; children: React.ReactNode}> = ({n, title, children}) => {
  const frame = useCurrentFrame();
  const a = prog(frame, 0, 14);
  return (
    <AbsoluteFill style={{background: C.paper, color: C.ink, fontFamily: F.serif}}>
      <div
        style={{
          position: 'absolute',
          left: S.margin,
          right: S.margin,
          top: 60,
          fontSize: S.title,
          fontWeight: 700,
          lineHeight: 1.12,
          letterSpacing: '-0.02em',
          opacity: a,
        }}
      >
        {title}
      </div>
      <div style={{position: 'absolute', left: S.margin, right: S.margin, top: S.ruleY, height: 3, background: C.rule}} />
      {children}
      <div style={{position: 'absolute', right: S.margin, bottom: 36, fontSize: S.page, color: C.page}}>{n}</div>
    </AbsoluteFill>
  );
};

/** A section divider: blue band across the top, large title, one line under it. */
export const Part: React.FC<{band: string; count: string; title: string; sub: string}> = ({band, count, title, sub}) => {
  const frame = useCurrentFrame();
  const a = prog(frame, 0, 16);
  const b = prog(frame, 8, 24);
  return (
    <AbsoluteFill style={{background: C.paper, color: C.ink, fontFamily: F.serif, justifyContent: 'center'}}>
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          background: C.blue,
          color: '#fff',
          padding: '54px 120px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
          fontSize: 36,
          letterSpacing: '0.2em',
          textTransform: 'uppercase',
        }}
      >
        <span>{band}</span>
        <span style={{opacity: 0.72, letterSpacing: '0.1em'}}>{count}</span>
      </div>
      <div
        style={{
          margin: '0 120px',
          fontSize: S.part,
          fontWeight: 400,
          lineHeight: 1.08,
          letterSpacing: '-0.03em',
          maxWidth: 1500,
          opacity: a,
          transform: `translateY(${(1 - a) * 16}px)`,
        }}
      >
        {title}
      </div>
      <div
        style={{
          margin: '48px 120px 0',
          fontSize: 46,
          lineHeight: 1.4,
          color: '#1a1a1a',
          maxWidth: 1350,
          opacity: b,
          transform: `translateY(${(1 - b) * 16}px)`,
        }}
      >
        {sub}
      </div>
    </AbsoluteFill>
  );
};
