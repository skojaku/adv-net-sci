# m06 review round 3 (v3 deck): brief for reviewers

The deck `slides/m06/m06-centrality.md` (82 slides) was rebuilt after the lecturer's review of
v2. Rendered slides: `slides/m06/review/slide.NNN.png` (NNN = 001..082, the PDF/PNG export,
which shows the LAST frame of every build). A build's frames: `slides/m06/figures/frames/<name>/
NN.png`; the slide's figure is `<div class="fig scrub">`, and in the presentation the lecturer
steps from frame 00 to the last. Spec: `review/DECK_SPEC.md`. Style: `review/FIG_BRIEF_v3.md`.

## What the lecturer asked for (his words, translated)

- "The cognitive cost grows like n² in the amount n of new information": consecutive slides
  must differ by little. The same drawing stays at the same place and gains one thing.
- The figure fixed in the right half, a few short bullets on the left, revealed one by one.
- A two-graph question becomes two one-graph questions (Q1, A1, Q2, A2).
- Figures over text; cut what the lecture does not use. Very little text, in figures too.
- His figure style: hand-drawn nodes with a dark (not pure black) outline, grain, brush
  strokes for routes and underlines, MesloLGS NF, muted colours with saturation only on what
  matters (orange = the point, sky blue = second emphasis).
- No autoplay: builds are stepped (frames).

## Review every slide in your range. Open every PNG with Read; never judge from the source.

For a slide with a build, also open frames 00 and the last of its frames directory, and check
that frame 00 is the same picture as the previous slide where the spec says so.

Report, per finding: slide number, severity (Blocker / Major / Minor), what is wrong, and a
concrete fix. Look for:

1. **Diff size.** Does the picture jump between consecutive slides that share a drawing
   (compare the two PNGs: same position, same size)? Does a slide add more than one new thing
   at once? Is there a slide that could be split, or two that could be one?
2. **Layout.** Figure right, bullets left where the spec says so. Anything clipped, overflowing
   the frame (content must end above y = 660 of 720), overlapping, or too small to read.
3. **Correctness.** Every number in a figure must match the bullets and the speaker notes, and
   the marked winner must be the right node (the notes give the values; `figures/smallgraphs.py`
   computes them). The quiz trick: the node drawn in the middle (or the hub) must NOT win.
   A question slide must not show its answer.
4. **Figure readability.** Labels touching discs or edges, a value that could belong to two
   nodes, an underline under the wrong thing, colours used against the rule (orange on
   something that is not the point), pure black.
5. **Text.** Wordy bullets, a bullet that repeats the figure, prose in a figure. Bullets are
   telegraphic; one idea each.

Do not fix anything; do not edit files. Write your report to the path you are given, then
return a summary of the Blockers and Majors.
