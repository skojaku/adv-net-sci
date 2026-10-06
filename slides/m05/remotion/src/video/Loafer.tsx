import React from 'react';

/**
 * A small figure lying on its stomach, chin on one hand, feet in the air (our own drawing, thick black lines and flat colours). Everything about its
 * pose is an argument, so the picture is a pure function of the frame.
 */
export type LoaferPose = {
  /** the head dips, in px (positive = down), and tilts, in degrees */
  nod: number;
  tilt: number;
  /** the feet kick, in degrees, one for each leg */
  kickA: number;
  kickB: number;
  /** breathing: 1 = rest */
  breathe: number;
  blink: boolean;
  /** 0 closed smile, 1 small open mouth */
  mouth: number;
  /** the ribbon sways, in degrees */
  sway: number;
};

const INK = '#111';
const SKIN = '#fdebdc';
const HAIR = '#f3f0ea';
const CLOTH = '#ffffff';
const RIBBON = '#cfc6ee';
const SHOE = '#fbe6d4';
const W = 6.5;

/** a limb: a thick black line with a narrower coloured line on top, so that it has an outline */
const Limb: React.FC<{d: string; width: number; fill: string}> = ({d, width, fill}) => (
  <>
    <path d={d} fill="none" stroke={INK} strokeWidth={width + 2 * W} strokeLinecap="round" strokeLinejoin="round" />
    <path d={d} fill="none" stroke={fill} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" />
  </>
);

export const Loafer: React.FC<{pose: LoaferPose; width?: number}> = ({pose, width = 250}) => {
  const {nod, tilt, kickA, kickB, breathe, blink, mouth, sway} = pose;
  return (
    <svg width={width} height={(width * 150) / 250} viewBox="0 0 250 150" style={{overflow: 'visible'}}>
      {/* the legs, bent up at the knee, feet in the air */}
      <g transform={`rotate(${kickB} 192 116)`}>
        <Limb d="M192 116 L228 98" width={16} fill={CLOTH} />
        <circle cx="232" cy="96" r="8" fill={SHOE} stroke={INK} strokeWidth={W - 1.5} />
      </g>
      <g transform={`rotate(${kickA} 188 112)`}>
        <Limb d="M188 112 L224 80" width={16} fill={CLOTH} />
        <circle cx="228" cy="77" r="8" fill={SHOE} stroke={INK} strokeWidth={W - 1.5} />
      </g>
      {/* the body, lying */}
      <g transform={`translate(140 112) scale(1 ${breathe}) translate(-140 -112)`}>
        <Limb d="M96 110 L186 112" width={30} fill={CLOTH} />
        <path d="M138 96 L150 128" stroke={RIBBON} strokeWidth="9" strokeLinecap="round" />
      </g>
      {/* the head, propped on the hand */}
      <g transform={`translate(0 ${nod}) rotate(${tilt} 106 104)`}>
        <ellipse cx="106" cy="68" rx="58" ry="50" fill={SKIN} stroke={INK} strokeWidth={W} />
        {/* the hair, with a straight fringe */}
        <path d="M49 72 C44 -2 168 -2 163 72 L148 58 L130 66 L112 54 L92 66 L72 56 Z" fill={HAIR} stroke={INK} strokeWidth={W - 1} strokeLinejoin="round" />
        {/* a ribbon on the side that sways */}
        <g transform={`rotate(${sway} 160 46)`}>
          <ellipse cx="170" cy="40" rx="13" ry="9" fill={RIBBON} stroke={INK} strokeWidth={W - 2} transform="rotate(-25 170 40)" />
        </g>
        {/* the face */}
        {blink ? (
          <>
            <path d="M82 86 L94 86 M118 86 L130 86" stroke={INK} strokeWidth={4} strokeLinecap="round" />
          </>
        ) : (
          <>
            <ellipse cx="88" cy="86" rx="4.2" ry="6.4" fill={INK} />
            <ellipse cx="124" cy="86" rx="4.2" ry="6.4" fill={INK} />
          </>
        )}
        {mouth < 0.3 ? (
          <path d="M98 101 Q106 109 114 101" fill="none" stroke={INK} strokeWidth={4} strokeLinecap="round" />
        ) : (
          <ellipse cx="106" cy="103" rx="6.5" ry="5" fill={INK} />
        )}
      </g>
      {/* the arm that holds the head up: forearm on the ground, hand at the cheek */}
      <Limb d="M42 130 L70 114" width={14} fill={CLOTH} />
      <circle cx="74" cy="111" r="10" fill={SKIN} stroke={INK} strokeWidth={W - 1.5} />
    </svg>
  );
};
