import {loadFont as loadBaskerville} from '@remotion/google-fonts/LibreBaskerville';
import {loadFont as loadCaveat} from '@remotion/google-fonts/Caveat';

// The Marp deck's palette (slides/m05/network-science.css) and type, at 1.5x:
// the Marp slide is 1280 x 720, this canvas is 1920 x 1080.
export const C = {
  paper: '#ffffff',
  ink: '#000000',
  soft: '#6b6b6b', // annotations
  faint: '#bdbcbf',
  rule: '#dddddd',
  panel: '#f7f4f1', // formula panel
  page: '#b3b3b3', // page number
  blue: '#3959A6', // everything that is drawn: nodes, bands, lines
  blueSoft: '#e7ecf7',
  blueMid: '#cdd7ee',
  brown: '#8B5E34', // a group colour, and the colour of stripes
  orange: '#E69F00', // group colour
  purple: '#6A3D9A', // group colour
  gray5: '#3a3a3a', // fifth group colour
  brownMid: '#dcc7ad',
  red: '#B14434', // emphasised text only (key terms, the higher value). Never a fill or a group.
} as const;

const baskerville = loadBaskerville('normal', {weights: ['400', '700'], subsets: ['latin']});
const caveat = loadCaveat('normal', {weights: ['500', '600'], subsets: ['latin']});

export const F = {
  serif: `${baskerville.fontFamily}, Georgia, serif`,
  hand: `${caveat.fontFamily}, cursive`,
  mono: 'ui-monospace, "SF Mono", Menlo, Consolas, monospace',
} as const;

/** Marp sizes x 1.5. */
/** Groups are told apart by how they are filled, not by hue: see src/lib/look.ts. */
export const S = {
  body: 45,
  note: 40,
  hand: 45,
  title: 60,
  part: 100,
  page: 24,
  margin: 120,
  ruleY: 154,
  bodyTop: 190,
  bodyBottom: 990,
  nodeMin: 39, // disc diameter floor (26px x 1.5)
} as const;
