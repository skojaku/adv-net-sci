import React from 'react';
import {C} from '../theme';

/** Fill patterns for groups (see src/lib/look.ts). Rendered once by `Frame`; other SVGs on the slide refer to them by id. */
export const PatternDefs: React.FC = () => (
  <svg width={1} height={1} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
    <defs>
      <pattern id="hatch-brown" width={9} height={9} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <rect width={9} height={9} fill="#fff" />
        <rect width={4.5} height={9} fill={C.brown} />
      </pattern>
      <pattern id="hatch-band" width={16} height={16} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <rect width={16} height={16} fill="#fff" />
        <rect width={7} height={16} fill={C.brownMid} />
      </pattern>
    </defs>
  </svg>
);
