import React from 'react';
import {AbsoluteFill, Audio, Freeze, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {slides} from '../slides';
import {BAND, Narrator} from './Narrator';
import {ProseContext} from '../components/Text';
import {MOODS} from './moods';
import {Prose, SKIP, SlideSeg, buildTimeline, reactionsOf} from './timeline';
import proseData from './prose.json';
import {narration} from './narration';

/**
 * The deck as a video: each slide plays stage by stage as in the click-through deck, the picture is held while the narrator types,
 * then the next stage starts. The slides themselves are not touched: this file only plays them (a Sequence that starts at a negative
 * frame makes a slide play from the middle; a Freeze holds the end of a stage).
 */
/** The slide is shown under the narrator band. Its own free band (the last 160 px, kept empty for subtitles) is cut off, so the first 920 px fill the room that is left. */
const SLIDE_SCALE = (1080 - BAND) / 920;

export const timeline = buildTimeline(
  slides.map((s) => s.marks),
  narration,
  proseData as Prose,
  SKIP,
);

export const reactions = reactionsOf(timeline, MOODS);

const SlidePlay: React.FC<{seg: SlideSeg}> = ({seg}) => {
  const Comp = slides[seg.n - 1].Component;
  return (
    <>
      {seg.stages.map((st) => (
        <React.Fragment key={st.k}>
          <Sequence from={st.from - seg.from} durationInFrames={Math.max(1, st.anim)}>
            <Sequence from={-st.slideFrom}>
              <Comp />
            </Sequence>
          </Sequence>
          <Sequence from={st.from - seg.from + st.anim} durationInFrames={Math.max(1, st.hold)}>
            <Freeze frame={st.slideTo}>
              <Comp />
            </Freeze>
          </Sequence>
        </React.Fragment>
      ))}
    </>
  );
};

export const NarratedDeck: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: '#ffffff'}}>
      {/* the slides' sentences are not drawn: the narrator types them in the chat */}
      <div style={{position: 'absolute', left: 0, top: BAND, width: 1920, height: 1080 - BAND, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '50% 0', transform: `scale(${SLIDE_SCALE})`}}>
          <ProseContext.Provider value="hide">
            {timeline.slides.map((seg) => (
              <Sequence key={seg.n} from={seg.from} durationInFrames={seg.dur}>
                <SlidePlay seg={seg} />
              </Sequence>
            ))}
          </ProseContext.Provider>
        </div>
      </div>
      <Narrator frame={frame} bubbles={timeline.bubbles} keys={timeline.keys} reactions={reactions} fadeFrom={timeline.total - 80} />
      <Audio src={staticFile('typing.wav')} volume={0.9} />
    </AbsoluteFill>
  );
};
