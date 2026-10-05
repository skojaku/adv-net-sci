import React from 'react';
import {Composition} from 'remotion';
import {FPS} from './timeline';
import {NarratedDeck, timeline} from './NarratedDeck';

export const VideoRoot: React.FC = () => (
  <Composition id="M05-narrated" component={NarratedDeck} durationInFrames={timeline.total} fps={FPS} width={1920} height={1080} />
);
