import React from 'react';
import {spring} from 'remotion';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';
import {C} from '../theme';
import {ASPECT, Character} from './Character';
import {Bubble, FPS, IntroSeg, Reaction, introMove} from './timeline';

const mono = loadMono('normal', {weights: ['400', '500'], subsets: ['latin']});

/**
 * The narrator in the band at the TOP of the video (the slide is shown under it, see NarratedDeck.tsx): a small figure lying down at the left (Character.tsx) and, to
 * its right, plain terminal lines on the white page (a prompt, the text typed key by key, a block cursor, no frame). A new line starts at the
 * bottom of the two lines and the older lines move up and fade; two lines at most.
 */
const FONT = 34;
const LINE = 50;
const BX = 520; // left edge of the lines
export const BAND = 228; // height of the band at the TOP of the video that holds the figure and the lines; the slide is shown under it
const TOP = 85; // distance of the two lines from the top edge (they are centred on the figure)
const WIDTH = 1390; // the longest line is 63 characters + the prompt + the cursor = 66.7 characters of 34 px mono = 1360 px: it must not wrap
const FIG_H = 166; // height of the figure; its width follows from the aspect of the frames
const FIG_W = Math.round(FIG_H * ASPECT);
const FADE = [1, 0.6, 0, 0, 0, 0]; // opacity by age: the newest line, the one before, ...; two lines fit in the band
const BOTTOM = TOP + 2 * LINE; // the lines grow upward from here
// The introduction: the narrator in the middle of the screen under the title (IntroTitle.tsx), bigger, with more lines; it moves into the band (the layout above) at `intro.transFrom`.
// Lecturer (modularity video): the typed lines above, the narrator below them at the bottom of the screen: the chat grows up from the narrator toward the title.
const INTRO = {figW: 440, figTop: 700, textLeft: 180, bottom: 650, font: 40, line: 62, fade: [1, 0.8, 0.62, 0.46, 0.3, 0]};
const PROMPT = '$';

const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const pop = (frame: number) => spring({frame, fps: FPS, config: {damping: 14, stiffness: 170, mass: 0.6}});

export const Narrator: React.FC<{frame: number; bubbles: Bubble[]; keys: {frame: number; kind: string}[]; reactions: Reaction[]; intro?: IntroSeg; fadeFrom?: number}> = ({frame, bubbles, keys, reactions, intro, fadeFrom}) => {
  // one continuous talk: the lines that have started so far, the last six at most (the older ones fade out)
  const started = bubbles.filter((b) => b.start <= frame);
  const shown = started.slice(-6);
  // 0 = the introduction layout (middle of the screen), 1 = the band at the top; without an introduction it is always the band. The figure moves before the lines (introMove).
  const move = introMove(frame, intro);
  const ef = move.figure;
  const e = move.text;
  const figW = lerp(INTRO.figW, FIG_W, ef);
  const figH = figW / ASPECT;
  const font = lerp(INTRO.font, FONT, e);
  const line = lerp(INTRO.line, LINE, e);
  const bottom = lerp(INTRO.bottom, BOTTOM, e);
  const fadeOut = fadeFrom === undefined ? 1 : clamp01(1 - (frame - fadeFrom) / 24);
  const newest = started[started.length - 1];
  const pNew = newest ? pop(frame - newest.start) : 1;

  return (
    <>
      <div style={{position: 'absolute', left: lerp((1920 - INTRO.figW) / 2, 120, ef), top: lerp(INTRO.figTop, 52, ef), width: figW, height: figH, opacity: fadeOut}}>
        <Character frame={frame} keys={keys} reactions={reactions} width={figW} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: lerp(INTRO.textLeft, BX, e),
          top: 0,
          width: WIDTH,
          height: 1080,
          fontFamily: `${mono.fontFamily}, ui-monospace, Menlo, monospace`,
          fontSize: font,
          lineHeight: `${line}px`,
          color: C.ink,
          opacity: fadeOut,
          whiteSpace: 'pre',
        }}
      >
        {shown.map((b, i) => {
          const rank = shown.length - 1 - i; // 0 = the newest
          // when a new line starts, every older line moves up one line and fades one step
          const fadeAt = (r: number) => lerp(INTRO.fade[r], FADE[r], e);
          const o = rank === 0 ? clamp01(pNew * 2) : lerp(fadeAt(rank - 1), fadeAt(rank), pNew);
          if (o < 0.01) return null;
          const shift = rank === 0 ? (1 - pNew) * line * 0.6 : (1 - pNew) * line;
          let text = '';
          for (const k of b.keys) {
            if (k.frame <= frame) text = k.text;
            else break;
          }
          const isNewest = rank === 0;
          const typingNow = frame >= b.start && frame < b.typedEnd + 2;
          const blinkOn = typingNow || Math.floor(frame / 15) % 2 === 0;
          return (
            <div key={`${b.slide}-${b.stage}-${b.index}`} style={{position: 'absolute', left: 0, top: bottom - (rank + 1) * line, height: line, opacity: o, transform: `translateY(${shift}px)`, whiteSpace: 'pre'}}>
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
