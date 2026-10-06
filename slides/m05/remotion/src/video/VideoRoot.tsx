import React from 'react';
import {Composition} from 'remotion';
import {slides} from '../slides';
import {ProseContext} from '../components/Text';
import {FPS} from './timeline';
import {NarratedDeck, timeline} from './NarratedDeck';
import {SoundSampler, sampler} from './SoundSampler';

/** One composition per slide that reports its sentences (scripts/collect_prose.mjs renders it at the end of every stage). */
const Collect: React.FC<{n: number}> = ({n}) => {
  const Comp = slides[n - 1].Component;
  return (
    <ProseContext.Provider value="collect">
      <Comp />
    </ProseContext.Provider>
  );
};

export const VideoRoot: React.FC = () => (
  <>
    <Composition id="M05-narrated" component={NarratedDeck} durationInFrames={timeline.total} fps={FPS} width={1920} height={1080} />
    <Composition id="M05-sampler" component={SoundSampler} durationInFrames={sampler.total} fps={FPS} width={1920} height={1080} />
    {slides.map((s) => (
      <Composition
        key={s.n}
        id={`Collect-S${String(s.n).padStart(2, '0')}`}
        component={Collect}
        defaultProps={{n: s.n}}
        durationInFrames={s.marks[s.marks.length - 1] + 1}
        fps={FPS}
        width={1920}
        height={1080}
      />
    ))}
  </>
);
