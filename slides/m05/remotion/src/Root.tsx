import React from 'react';
import {Composition} from 'remotion';
import {slides} from './slides';
import {FPS} from './lib/anim';

/**
 * Remotion Studio and video export.
 * Each slide becomes one composition that plays through all its stages without waiting.
 */
export const RemotionRoot: React.FC = () => (
  <>
    {slides.map((s) => (
      <Composition
        key={s.id}
        id={`S${String(s.n).padStart(2, '0')}-${s.id}`}
        component={s.Component}
        durationInFrames={s.marks[s.marks.length - 1] + FPS}
        fps={FPS}
        width={1920}
        height={1080}
      />
    ))}
  </>
);
