import type {Pt} from './network';

/**
 * The 8 nodes of the block model on a circle, two arcs: nodes 1 to 4 (the first group) on the right, 5 to 8 on the
 * left, with the same gap between the arcs at the top and at the bottom. (circle8 in sbm.ts leaves a 15 degree gap
 * at the top, so its nodes 8 and 1 touch at a size of 60 px or more.)
 */
export const arcs8 = (cx: number, cy: number, r: number): Pt[] => {
  const step = 38; // degrees between neighbours in a group; the gap between the groups is then 66
  const deg = (i: number) => (i < 4 ? -1.5 * step + i * step : 180 - 1.5 * step + (i - 4) * step);
  return Array.from({length: 8}, (_, i) => {
    const t = (deg(i) * Math.PI) / 180;
    return [cx + r * Math.cos(t), cy + r * Math.sin(t)] as const;
  });
};
