import React from 'react';
import {Img} from 'remotion';
import rest from './character/rest.png';
import typeA from './character/typeA.png';
import typeB from './character/typeB.png';
import typeC from './character/typeC.png';
import worry from './character/worry.png';
import shrug from './character/shrug.png';
import size from './character/size.json';
import {Mood, Reaction} from './timeline';

/** width / height of every frame (written by scripts/prep_character.py) */
export const ASPECT = size.width / size.height;

/**
 * The narrator, drawn by Gemini (scripts/gen_character.py, scripts/prep_character.py): five frames of the same boy lying flat on his stomach (side view, feet up, facing right toward the text), the head at
 * the same pixels in all of them. Which frame shows is a pure function of the frame number:
 * - 'rest': hands on the keys, no key pressed;
 * - 'type': while keys are being pressed, typeA / typeC / typeB / typeC follow one another (every two keystrokes), so that both hands strike with the sound;
 * - 'worry' (a troubled face, still at the keys) / 'shrug' (palms up, eyes closed): a reaction (timeline.reactionsOf) between two lines.
 * The groups blend over FADE frames; typeA <-> typeB is a hard cut.
 */
const FADE = 6;
const TYPING_AGE = 12; // frames after a key during which he is still typing
/** the typing frames in turn, one step every two keystrokes: A lifts the far hand, C the near hand, B the far hand higher, so that both hands visibly strike */
const TYPE_SEQ = ['typeA', 'typeC', 'typeB', 'typeC'];

type Group = 'rest' | 'type' | Mood;

export const Character: React.FC<{frame: number; keys: {frame: number}[]; reactions: Reaction[]; width: number}> = ({frame, keys, reactions, width}) => {
  const lastKey = (f: number) => {
    let lo = 0;
    let hi = keys.length - 1;
    let ans = -1;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (keys[mid].frame <= f) {
        ans = mid;
        lo = mid + 1;
      } else hi = mid - 1;
    }
    return ans;
  };
  const groupAt = (f: number): Group => {
    const r = reactions.find((x) => f >= x.from && f < x.to);
    if (r) return r.mood;
    const k = lastKey(f);
    return k >= 0 && f - keys[k].frame < TYPING_AGE ? 'type' : 'rest';
  };

  const weight: Record<Group, number> = {rest: 0, type: 0, worry: 0, shrug: 0};
  for (let i = 0; i < FADE; i++) weight[groupAt(frame - i)] += 1 / FADE;

  const k = lastKey(frame);
  const typeFrame = TYPE_SEQ[Math.floor(Math.max(k, 0) / 2) % TYPE_SEQ.length];
  const opacity: Record<string, number> = {
    rest: weight.rest,
    typeA: typeFrame === 'typeA' ? weight.type : 0,
    typeB: typeFrame === 'typeB' ? weight.type : 0,
    typeC: typeFrame === 'typeC' ? weight.type : 0,
    worry: weight.worry,
    shrug: weight.shrug,
  };
  const age = k >= 0 ? frame - keys[k].frame : 999;
  const bob = age < 4 ? 1.5 * (1 - age / 4) : 0; // the whole figure dips a little with each key
  const breathe = 1 + 0.012 * Math.sin(frame / 17);

  const art: Record<string, string> = {rest, typeA, typeB, typeC, worry, shrug};
  const height = width / ASPECT;
  return (
    <div style={{position: 'relative', width, height, transformOrigin: '50% 100%', transform: `translateY(${bob}px) scaleY(${breathe})`}}>
      {Object.keys(art).map((name) => (
        <Img key={name} src={art[name]} style={{position: 'absolute', left: 0, top: 0, width, height, opacity: opacity[name]}} />
      ))}
    </div>
  );
};
