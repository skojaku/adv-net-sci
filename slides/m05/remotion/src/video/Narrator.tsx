import React from 'react';
import {spring} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {C} from '../theme';
import {Critter, Pose} from './Critter';
import {Bubble, FPS} from './timeline';

loadInter('normal', {weights: ['400', '500'], subsets: ['latin']});

/**
 * The narrator at the bottom of the slide: the animal at the left and its speech bubbles to the right, in the free band under the
 * slides (below y = 920). Two bubbles at most; a new bubble pops up at the bottom and pushes the older ones up; text is typed key by key.
 */
const BUBBLE = C.blueSoft;
const FONT = 32;
const PAD_Y = 12;
const PAD_X = 30;
const LINE = Math.round(FONT * 1.28);
const GAP_Y = 8;
const BX = 224; // left edge of the bubbles
const BOTTOM = 20; // distance of the bottom bubble from the bottom edge
const MAX_W = 1180;
const MAX_VISIBLE = 2;
const CPL = 66; // characters per line at this width (an estimate, used for the push-up animation only)

const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
const lines = (text: string) => Math.max(1, Math.ceil(text.length / CPL));
const heightOf = (text: string) => lines(text) * LINE + 2 * PAD_Y;
const pop = (frame: number) => spring({frame, fps: FPS, config: {damping: 11, stiffness: 190, mass: 0.55}});

export const Narrator: React.FC<{frame: number; bubbles: Bubble[]; keys: {frame: number; kind: string}[]; fadeFrom?: number}> = ({frame, bubbles, keys, fadeFrom}) => {
  // one continuous conversation: the bubbles that have popped up so far, the last three at most (the oldest of them is on its way out)
  const started = bubbles.filter((b) => b.start <= frame);
  const shown = started.slice(-3);
  const fadeOut = fadeFrom === undefined ? 1 : clamp01(1 - (frame - fadeFrom) / 24);

  // the animal
  const last = (() => {
    let lo = 0;
    let hi = keys.length - 1;
    let ans = -1;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (keys[mid].frame <= frame) {
        ans = mid;
        lo = mid + 1;
      } else hi = mid - 1;
    }
    return ans;
  })();
  const age = last >= 0 ? frame - keys[last].frame : 999;
  const typing = age < 9;
  const newest = started[started.length - 1];
  const sincePop = newest ? frame - newest.start : 999;
  const hop = sincePop >= 0 && sincePop < 10 ? Math.sin((Math.PI * sincePop) / 10) * 9 : 0;
  const parity = last % 2 === 0;
  const pawPulse = typing ? clamp01(1 - age / 5) : 0;
  const pose: Pose = {
    mouth: typing && age < 3 ? 1 : 0,
    pawL: parity ? pawPulse : 0,
    pawR: parity ? 0 : pawPulse,
    lift: -hop + (typing && age < 2 ? -2 : 0),
    breathe: 1 + 0.014 * Math.sin(frame / 15),
    blink: frame % 104 >= 0 && frame % 104 < 5,
    ear: frame % 197 < 9 ? Math.sin((Math.PI * (frame % 197)) / 9) : 0,
    wobble: Math.floor(frame / 7) % 3,
  };

  return (
    <>
      <div style={{position: 'absolute', left: 34, bottom: 2, width: 164, height: 164}}>
        <Critter pose={pose} size={164} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: BX,
          bottom: BOTTOM,
          width: MAX_W,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          gap: GAP_Y,
          opacity: fadeOut,
        }}
      >
        {shown.map((b, i) => {
          const rank = shown.length - 1 - i; // 0 = the newest
          const third = shown[i + MAX_VISIBLE]; // the bubble that pushes this one out
          const gone = third ? clamp01((frame - third.start) / 8) : 0;
          if (gone >= 1) return null;
          // the bubbles above slide up when a newer one pops in below them
          let shift = 0;
          for (let j = i + 1; j < shown.length; j++) shift += (heightOf(shown[j].text) + GAP_Y) * (1 - pop(frame - shown[j].start));
          const p = pop(frame - b.start);
          const text = (() => {
            let t = '';
            for (const k of b.keys) {
              if (k.frame <= frame) t = k.text;
              else break;
            }
            return t;
          })();
          const typingNow = frame < b.typedEnd + 2 && frame >= b.keys[0].frame;
          const cursor = frame < b.typedEnd + 40 && frame >= b.start + 4 && Math.floor(frame / 9) % 2 === 0;
          return (
            <div
              key={`${b.stage}-${b.index}`}
              style={{
                position: 'relative',
                maxWidth: MAX_W,
                transformOrigin: 'left bottom',
                transform: `translateY(${shift}px) scale(${0.55 + 0.45 * p})`,
                opacity: Math.min(1, p * 1.6) * (1 - gone),
              }}
            >
              <div
                style={{
                  background: BUBBLE,
                  color: C.ink,
                  borderRadius: 36,
                  padding: `${PAD_Y}px ${PAD_X}px`,
                  fontFamily: 'Inter, system-ui, sans-serif',
                  fontWeight: 400,
                  fontSize: FONT,
                  lineHeight: `${LINE}px`,
                  minHeight: LINE,
                  minWidth: 56,
                  overflowWrap: 'anywhere',
                }}
              >
                {text}
                <span style={{display: 'inline-block', width: 3, height: FONT * 0.95, marginLeft: 3, verticalAlign: 'text-bottom', background: cursor || typingNow ? C.ink : 'transparent', opacity: typingNow ? 1 : 0.9}} />
              </div>
              {rank === 0 && (
                <svg width="34" height="30" viewBox="0 0 34 30" style={{position: 'absolute', left: -15, bottom: 4}}>
                  <path d="M34 0 L34 28 Q14 30 0 26 Q20 20 26 4 Z" fill={BUBBLE} />
                </svg>
              )}
            </div>
          );
        })}
      </div>
    </>
  );
};
