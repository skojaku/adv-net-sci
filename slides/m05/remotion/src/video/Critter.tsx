import React from 'react';

/**
 * A small cream-coloured animal with a tan patch over one ear and eye (our own drawing). Everything about its pose is an argument,
 * so the picture is a pure function of the frame. Lines are wobbled a little by a turbulence filter, as if drawn by hand.
 */
export type Pose = {
  /** 0 closed, 1 open */
  mouth: number;
  /** how far each paw is raised, 0 to 1 */
  pawL: number;
  pawR: number;
  /** vertical offset of the whole body in px (a hop is negative) */
  lift: number;
  /** squash and stretch of the body, 1 = rest */
  breathe: number;
  blink: boolean;
  /** ears tilt out a little, 0 to 1 */
  ear: number;
  /** 0, 1 or 2: the seed of the wobble */
  wobble: number;
};

const INK = '#4a3226';
const CREAM = '#fff4e2';
const TAN = '#c98b57';
const PINK = '#f4a79f';
const MOUTH = '#e0605f';
const W = 4.2;

const outline = {stroke: INK, strokeWidth: W, strokeLinejoin: 'round' as const, strokeLinecap: 'round' as const};

export const Critter: React.FC<{pose: Pose; size?: number}> = ({pose, size = 190}) => {
  const {mouth, pawL, pawR, lift, breathe, blink, ear, wobble} = pose;
  const mouthRy = 3 + 10 * mouth;
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" style={{overflow: 'visible'}}>
      <defs>
        <filter id="wobble" x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed={wobble + 2} result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="3.4" />
        </filter>
        <clipPath id="headClip">
          <ellipse cx="100" cy="88" rx="63" ry="52" />
        </clipPath>
      </defs>
      <g filter="url(#wobble)" transform={`translate(0 ${lift})`}>
        {/* tail */}
        <path d="M146 154 C180 156 192 122 172 106" fill="none" stroke={INK} strokeWidth={17} strokeLinecap="round" />
        <path d="M146 154 C180 156 192 122 172 106" fill="none" stroke={CREAM} strokeWidth={9} strokeLinecap="round" />
        {/* feet */}
        <ellipse cx="78" cy="187" rx="21" ry="9.5" fill={CREAM} {...outline} />
        <ellipse cx="124" cy="187" rx="21" ry="9.5" fill={CREAM} {...outline} />
        {/* body (squashes a little as it breathes) */}
        <g transform={`translate(100 184) scale(${1 + (1 - breathe) * 0.6} ${breathe}) translate(-100 -184)`}>
          <ellipse cx="100" cy="146" rx="43" ry="42" fill={CREAM} {...outline} />
          {/* arms (paws) */}
          <g transform={`rotate(${-8 - pawL * 62} 62 132)`}>
            <ellipse cx="50" cy="140" rx="12" ry="19" fill={CREAM} {...outline} transform="rotate(14 50 140)" />
          </g>
          <g transform={`rotate(${8 + pawR * 62} 138 132)`}>
            <ellipse cx="150" cy="140" rx="12" ry="19" fill={CREAM} {...outline} transform="rotate(-14 150 140)" />
          </g>
        </g>
        {/* ears */}
        <g transform={`rotate(${-ear * 9} 66 52)`}>
          <path d="M44 62 L52 12 L92 40 Z" fill={TAN} {...outline} />
          <path d="M55 40 L58 24 L72 34 Z" fill={PINK} opacity="0.75" />
        </g>
        <g transform={`rotate(${ear * 9} 134 52)`}>
          <path d="M156 62 L148 12 L108 40 Z" fill={CREAM} {...outline} />
          <path d="M145 40 L142 24 L128 34 Z" fill={PINK} opacity="0.75" />
        </g>
        {/* head */}
        <ellipse cx="100" cy="88" rx="63" ry="52" fill={CREAM} {...outline} />
        <g clipPath="url(#headClip)">
          <ellipse cx="66" cy="70" rx="42" ry="34" fill={TAN} />
        </g>
        <ellipse cx="100" cy="88" rx="63" ry="52" fill="none" {...outline} />
        {/* face */}
        <ellipse cx="57" cy="104" rx="10" ry="7" fill={PINK} opacity="0.7" />
        <ellipse cx="143" cy="104" rx="10" ry="7" fill={PINK} opacity="0.7" />
        {blink ? (
          <>
            <path d="M68 88 Q76 93 84 88" fill="none" {...outline} strokeWidth={3.6} />
            <path d="M116 88 Q124 93 132 88" fill="none" {...outline} strokeWidth={3.6} />
          </>
        ) : (
          <>
            <ellipse cx="76" cy="88" rx="5.6" ry="8" fill={INK} />
            <ellipse cx="124" cy="88" rx="5.6" ry="8" fill={INK} />
            <circle cx="78" cy="84.5" r="2.1" fill="#fff" />
            <circle cx="126" cy="84.5" r="2.1" fill="#fff" />
          </>
        )}
        <path d="M94 101 Q100 96 106 101 Q100 107 94 101 Z" fill={INK} stroke={INK} strokeWidth={2} strokeLinejoin="round" />
        {mouth < 0.15 ? (
          <path d="M91 110 Q95.5 117 100 110 Q104.5 117 109 110" fill="none" {...outline} strokeWidth={3.4} />
        ) : (
          <g>
            <ellipse cx="100" cy={112 + mouthRy * 0.35} rx={10.5} ry={mouthRy} fill={MOUTH} {...outline} strokeWidth={3.4} />
            <ellipse cx="100" cy={112 + mouthRy * 0.75} rx={5.5} ry={mouthRy * 0.45} fill="#f59a96" />
          </g>
        )}
        {/* whiskers */}
        <path d="M44 98 L28 94 M44 104 L27 106 M156 98 L172 94 M156 104 L173 106" fill="none" stroke={INK} strokeWidth={2.4} strokeLinecap="round" opacity="0.7" />
      </g>
    </svg>
  );
};
