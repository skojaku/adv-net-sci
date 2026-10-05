import React from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

/** Inline KaTeX, black, at the size of the surrounding text. */
export const Tex: React.FC<{tex: string; display?: boolean; style?: React.CSSProperties}> = ({tex, display, style}) => (
  <span
    style={style}
    dangerouslySetInnerHTML={{__html: katex.renderToString(tex, {throwOnError: true, displayMode: !!display})}}
  />
);
