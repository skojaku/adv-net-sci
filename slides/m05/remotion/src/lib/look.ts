import {C} from '../theme';

/**
 * How a group's discs are filled. The palette is black, white and blue, so groups are told apart by
 * the fill, not by hue: solid, hollow, brown stripes, black, blue dots. The pattern ids are defined once per
 * slide by `PatternDefs` (components/Patterns.tsx, rendered by `Frame`).
 */
export type Look = {fill: string; stroke: string; sw: number; /** colour for a label written on the disc */ text: string};

export const LOOK: readonly Look[] = [
  {fill: C.blue, stroke: '#fff', sw: 3, text: '#fff'}, // 0 solid blue
  {fill: '#fff', stroke: C.blue, sw: 5, text: C.blue}, // 1 hollow
  {fill: 'url(#hatch-brown)', stroke: C.brown, sw: 4, text: C.ink}, // 2 brown stripes
  {fill: C.ink, stroke: '#fff', sw: 3, text: '#fff'}, // 3 black
  {fill: 'url(#dots-blue)', stroke: C.blue, sw: 4, text: C.ink}, // 4 dots
];

/** The fill of a band that surrounds a group: solid light blue, or light-brown stripes. */
export const BAND_SOLID = C.blueMid;
export const BAND_HATCH = 'url(#hatch-band)';
