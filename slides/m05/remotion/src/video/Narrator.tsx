import React from 'react';
import {spring} from 'remotion';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';
import {C} from '../theme';
import {Loafer, LoaferPose} from './Loafer';
import {Bubble, FPS} from './timeline';

const mono = loadMono('normal', {weights: ['400', '500'], subsets: ['latin']});

/**
 * The narrator in the band at the TOP of the video (the slide is shown under it, see NarratedDeck.tsx): a small figure lying down at the left and, to
 * its right, plain terminal lines on the white page (a prompt, the text typed key by key, a block cursor, no frame). A new line starts at the
 * bottom of the two lines and the older lines move up and fade; two lines at most.
 */
const FONT = 31;
const LINE = 46;
const BX = 440; // left edge of the lines
export const BAND = 190; // height of the band at the TOP of the video that holds the figure and the lines; the slide is shown under it
const TOP = 56; // distance of the two lines from the top edge
const WIDTH = 1340;
const FADE = [1, 0.6, 0, 0]; // opacity by age: the newest line, the one before, ...; two lines fit above the bottom margin
const PROMPT = '$';

const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const pop = (frame: number) => spring({frame, fps: FPS, config: {damping: 14, stiffness: 170, mass: 0.6}});

export const Narrator: React.FC<{frame: number; bubbles: Bubble[]; keys: {frame: number; kind: string}[]; fadeFrom?: number}> = ({frame, bubbles, keys, fadeFrom}) => {
  // one continuous talk: the lines that have started so far, the last four at most (the oldest of them is on its way out)
  const started = bubbles.filter((b) => b.start <= frame);
  const shown = started.slice(-4);
  const fadeOut = fadeFrom === undefined ? 1 : clamp01(1 - (frame - fadeFrom) / 24);
  const newest = started[started.length - 1];
  const pNew = newest ? pop(frame - newest.start) : 1;

  // the figure
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
  const typing = age < 12;
  const hit = typing ? clamp01(1 - age / 6) : 0;
  const parity = last % 2 === 0 ? 1 : -1;
  const pose: LoaferPose = {
    nod: hit * 3,
    tilt: parity * hit * 1.6 + 1.2 * Math.sin(frame / 41),
    kickA: 10 * Math.sin(frame / 11) + (typing ? parity * 7 * hit : 0),
    kickB: 10 * Math.sin(frame / 11 + 2.3) + (typing ? -parity * 7 * hit : 0),
    breathe: 1 + 0.025 * Math.sin(frame / 17),
    blink: frame % 112 < 5,
    mouth: typing && age < 4 ? 1 : 0,
    sway: 7 * Math.sin(frame / 23),
  };

  return (
    <>
      <div style={{position: 'absolute', left: 150, top: 22, width: 250, height: 150}}>
        <Loafer pose={pose} width={250} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: BX,
          top: TOP,
          width: WIDTH,
          height: LINE * 2,
          fontFamily: `${mono.fontFamily}, ui-monospace, Menlo, monospace`,
          fontSize: FONT,
          lineHeight: `${LINE}px`,
          color: C.ink,
          opacity: fadeOut,
          whiteSpace: 'pre-wrap',
        }}
      >
        {shown.map((b, i) => {
          const rank = shown.length - 1 - i; // 0 = the newest
          // when a new line starts, every older line moves up one line and fades one step
          const o = rank === 0 ? clamp01(pNew * 2) : lerp(FADE[rank - 1], FADE[rank], pNew);
          if (o < 0.01) return null;
          const shift = rank === 0 ? (1 - pNew) * LINE * 0.6 : (1 - pNew) * LINE;
          let text = '';
          for (const k of b.keys) {
            if (k.frame <= frame) text = k.text;
            else break;
          }
          const isNewest = rank === 0;
          const typingNow = frame >= b.start && frame < b.typedEnd + 2;
          const blinkOn = typingNow || Math.floor(frame / 15) % 2 === 0;
          return (
            <div key={`${b.slide}-${b.stage}-${b.index}`} style={{position: 'absolute', left: 0, bottom: rank * LINE, opacity: o, transform: `translateY(${shift}px)`, whiteSpace: 'pre-wrap'}}>
              <span style={{color: C.blue, fontWeight: 500}}>{PROMPT} </span>
              {text}
              {isNewest && (
                <span style={{display: 'inline-block', width: '0.58em', height: '1.05em', marginLeft: 2, verticalAlign: 'text-bottom', background: blinkOn ? C.ink : 'transparent', opacity: 0.85}} />
              )}
            </div>
          );
        })}
      </div>
    </>
  );
};
