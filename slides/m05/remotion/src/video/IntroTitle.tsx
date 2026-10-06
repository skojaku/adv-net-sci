import React from 'react';
import {F, C} from '../theme';
import config from './video.config.json';
import {IntroSeg, introMove} from './timeline';

/**
 * The title of the introduction, large at the top of the screen (the narrator is in the middle, see Narrator.tsx). It fades in at the start and is the first to leave
 * when the narrator moves up into the band (`introMove` in timeline.ts): it moves up a little and fades out. What it says is `intro` of video.config.json: kicker (small, above), title (large), subtitle (below).
 */
const clamp01 = (x: number) => Math.min(1, Math.max(0, x));

export const IntroTitle: React.FC<{frame: number; intro: IntroSeg}> = ({frame, intro}) => {
  const text = (config as {intro?: {kicker?: string; title?: string; subtitle?: string}}).intro;
  if (!text) return null;
  const appear = clamp01(frame / 30);
  const leave = introMove(frame, intro).title;
  const opacity = appear * (1 - leave);
  if (opacity < 0.005) return null;
  const dy = (1 - appear) * 24 - leave * 60;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, textAlign: 'center', opacity, transform: `translateY(${dy}px)`}}>
      {text.kicker && <div style={{position: 'absolute', top: 58, width: 1920, fontFamily: F.serif, fontSize: 40, letterSpacing: '0.14em', textTransform: 'uppercase', color: C.blue}}>{text.kicker}</div>}
      {text.title && <div style={{position: 'absolute', top: 108, width: 1920, fontFamily: F.serif, fontSize: 126, lineHeight: 1.1, fontWeight: 700, color: C.ink}}>{text.title}</div>}
      {text.subtitle && <div style={{position: 'absolute', top: 262, width: 1920, fontFamily: F.serif, fontSize: 38, color: C.soft}}>{text.subtitle}</div>}
    </div>
  );
};
