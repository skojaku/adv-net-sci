/**
 * The place of each dot in a dot plot on a number line, so that no two dots overlap.
 * A dot goes in the column (bin of width `binW` px) its value falls in, and stacks on the dots
 * that came before it in that column (data order). `binW` must be at least the dot diameter plus a gap.
 * x is the centre of the column; `row` 0 is the bottom of the stack.
 */
export const stackDots = (values: ReadonlyArray<number>, xOf: (v: number) => number, binW: number): {x: number; row: number}[] => {
  const count = new Map<number, number>();
  return values.map((v) => {
    const b = Math.floor(xOf(v) / binW);
    const row = count.get(b) ?? 0;
    count.set(b, row + 1);
    return {x: (b + 0.5) * binW, row};
  });
};
