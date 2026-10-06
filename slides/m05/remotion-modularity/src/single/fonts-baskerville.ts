// The single-file build (scripts/build_single.mjs) swaps @remotion/google-fonts/LibreBaskerville for this file, so that the
// fonts are inside the HTML file and nothing is fetched from the network.
import '@fontsource/libre-baskerville/latin-400.css';
import '@fontsource/libre-baskerville/latin-700.css';

export const loadFont = (..._args: unknown[]) => ({fontFamily: 'Libre Baskerville'});
