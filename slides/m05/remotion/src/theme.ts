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
  blue: '#3959A6', // structure: rules, bands, the object under discussion
  red: '#B14434', // emphasis: key terms, the higher value
  gold: '#DAB167', // fills and rings only, never text or a thin stroke
  purple: '#593196', // fifth group colour (lecture-note kit)
  blueSoft: '#e7ecf7',
  redSoft: '#f8e9e5',
} as const;

/** Group colours, in the deck's order. No green. */
export const GROUP = [C.blue, C.gold, C.red, C.soft, C.purple] as const;

const baskerville = loadBaskerville('normal', {weights: ['400', '700'], subsets: ['latin']});
const caveat = loadCaveat('normal', {weights: ['500', '600'], subsets: ['latin']});

export const F = {
  serif: `${baskerville.fontFamily}, Georgia, serif`,
  hand: `${caveat.fontFamily}, cursive`,
  mono: 'ui-monospace, "SF Mono", Menlo, Consolas, monospace',
} as const;

/** Marp sizes x 1.5. */
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
