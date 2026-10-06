import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {prog} from '../lib/anim';
import {Narrator} from './Narrator';
import {SAMPLER_PACKS, samplerTimeline} from './sampler';

export const sampler = samplerTimeline();

/** The listening test: each Mechvibes pack's name, then the same sentence typed with its sound. */
export const SoundSampler: React.FC = () => {
  const frame = useCurrentFrame();
  const seg = [...sampler.segments].reverse().find((s) => frame >= s.from) ?? sampler.segments[0];
  const local = frame - seg.from;
  const a = prog(local, 0, 14);
  const idx = SAMPLER_PACKS.indexOf(seg.pack);
  return (
    <AbsoluteFill style={{background: C.paper, color: C.ink, fontFamily: F.serif}}>
      <div style={{position: 'absolute', left: 140, top: 250, opacity: a, transform: `translateY(${(1 - a) * 14}px)`}}>
        <div style={{fontSize: 92, letterSpacing: '-0.02em'}}>{seg.pack.name}</div>
        <div style={{fontFamily: F.hand, fontSize: 56, color: C.soft, marginTop: 20}}>{seg.pack.feel}</div>
        <div style={{fontSize: 34, color: C.soft, marginTop: 40}}>
          {idx + 1} of {SAMPLER_PACKS.length}
        </div>
      </div>
      <Narrator frame={frame} bubbles={sampler.bubbles.filter((b) => b.start >= seg.from && b.start < seg.from + 400)} keys={sampler.keys} />
      <Audio src={staticFile('sampler.wav')} volume={0.9} />
    </AbsoluteFill>
  );
};
