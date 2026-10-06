import {C} from '../theme';

/**
 * How a group's discs look. Groups are told apart by hue: blue, orange, brown, purple, dark grey.
 * Red is never a group colour: it is for emphasised text only.
 * Stripes (brown, `hatch-brown`) are not a group look; they fill bands and overlaps (see BAND_HATCH, S18).
 */
export type Look = {fill: string; stroke: string; sw: number; /** colour for a label written on the disc */ text: string};

const disc = (fill: string, text: string): Look => ({fill, stroke: '#fff', sw: 3, text});

export const LOOK: readonly Look[] = [
  disc(C.blue, '#fff'), // 0
  disc(C.orange, C.ink), // 1
  disc(C.brown, '#fff'), // 2
  disc(C.purple, '#fff'), // 3
  disc(C.gray5, '#fff'), // 4
];

/** A node that belongs to no group (yet), or an unknown one ("?"): black. */
export const UNKNOWN: Look = {fill: C.ink, stroke: '#fff', sw: 3, text: '#fff'};
/** A plain white node with a blue edge: not a group, just "a node". */
export const HOLLOW: Look = {fill: '#fff', stroke: C.blue, sw: 5, text: C.blue};

/** The fill of a band that surrounds a group: solid light blue, or light-brown stripes. */
export const BAND_SOLID = C.blueMid;
export const BAND_HATCH = 'url(#hatch-band)';
