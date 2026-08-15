# Slide review — slides/m06/m06-centrality.md — 2026-08-05

**Verdict:** NEEDS WORK
**Slides:** 102 · **Blockers:** 0 · **Majors:** 2 · **Minors:** 3

*(Gate re-run after the round's fixes: `checked 102 rendered slides / node diameter 26-52px (spread 2.0x) across 398 discs / all checks pass`, exit 0.)*

`check_render.py` exits 0 on the current render: 102 slides, node diameter
26–52 px across 398 discs, no content below the frame, no container mismatch, no
math inside a figcaption. That is the build gate, not the review.

**Coverage note, per REVIEW_PLAYBOOK:** this round was read by one reviewer (the
build lead), not by the independent Opus reviewers the playbook asks for over
disjoint ranges — the three subagents on this module ran out of session budget
mid-build and the reviewer pass was not dispatched. Roughly 25 of the 102 slides
were read as rendered PNGs; the rest were checked mechanically (question slides
carry no answer, one point per slide, no tables or code, no two-text-column
layouts, no paragraph below a fragmented list, every concept slide has a figure,
containers, frame overflow, caption width, duplicate titles). **The next round
should read the ranges nobody has opened**: 15–20, 28–35, 39–44, 53–59, 67–73,
90–96.

## Milestones (structure pass, S5)

| part | milestone |
|---|---|
| 1 The Golden Milestone | slide 10 — draw the club network from the roster (it is also tonight's handout) |
| 2 Count the roads | slide 15 — count Rome's and Alexandria's roads aloud |
| 3 Close to everything | slide 23 — compute Massilia's closeness by hand |
| 4 The broker | slide 38 — count σ by hand; slide 45 — the handout goes out |
| 5 Known by the company you keep | slide 51 — the power-iteration GIF; slide 58 — "describe a network where this breaks" |
| 6 Everyone gets a floor | slide 66 — predict what raising λ does, then watch it break |
| 7 The Web has direction | slide 74 — pick the hub and the authority by eye |
| 8 Which one should you use? | slides 87 and 96 — "which will you use?" and the star/path prediction |

Every part has one. Part 5's is an animation the lecturer drives rather than a
student activity; see the open item below.

## Majors

1. **Slides 70, 74, 77, 81, 82, 85, 102 — F2 — the eight-page web is drawn with
   avoidable edge crossings.** The long News→Blog arrow crosses Links→Wiki and
   Course→Wiki; News→Wiki crosses Links→Wiki. The underlying undirected graph has
   twelve distinct pairs and `nx.check_planarity` says it is planar, so a
   crossing-free drawing exists — an annealing search finds one in seconds.
   *Fix:* re-lay `WEB_XY` **and** re-place the in-drawing notes and badges in the
   same pass. A crossing-free layout was found and rejected during this build
   because every note in `figs_web.py` is anchored to the current geometry: moving
   the pages put the `A_ij = 1` note on Forum, the authority badge on the
   Links→Forum link, and the teleport arc through Wiki. The reason is recorded in
   a comment above `WEB_XY` so the next attempt starts from it.

2. **Deck — S5 — Part 5's milestone is a demo, not a student activity.** The plan
   asked for a power-iteration slider the lecturer drags. It is not built: a
   slider exists only in the `--html` export, which `check_render.py` never
   exercises, and `DECK_BUILD_GUIDE.md` is explicit that confirming the `<script>`
   survived the export is not confirming that it runs. Shipping an untested widget
   is worse than shipping the GIF. *Fix:* build it against
   `verify_numbers.POWER_TRACE` (the GIF already comes from that array, so the two
   cannot drift), then drive the real control in a browser and read the outcome
   back out of the DOM.

## Minors

3. **Every haloed figure — the render gate's `smallest_text` heuristic reports
   1–3 px "text" on 34 slides.** City names on the Roman map are drawn with a
   white halo so a road can pass behind them, which leaves short black stubs where
   a road enters and leaves a word. The heuristic counts those stubs as glyphs.
   The generator's measured assertion (36 pt → 15.5 px x-height at scale 1.000) is
   the gate that matters here, and it passes on every figure. *Fix, if it is worth
   one:* teach `smallest_text` to ignore components with no same-height
   neighbours within a word's distance.

4. **Web slides — the node-diameter band is unenforced there.** Pages are drawn as
   rounded boxes rather than discs, which is the right choice for pages, but it
   means `node_discs()` finds nothing on those seven slides. Not a defect in the
   deck; recorded so nobody reads the green run as coverage.

5. **Slide 6 — the four mileages are the deck's only hand-entered numbers.**
   Approximate road distances from Rome in Roman miles, from the itineraries
   rather than from the graph. The figcaption now says "roughly" and the numbers
   are recorded in `DECK_SPEC.md`.

## What the round verified

- **Every number on a slide is computed and asserted.** `verify_numbers.py` exits
  0 and holds 60+ assertions, including the ones the prose quotes: Massilia's
  eleven distances (3 at one step, 5 at two, 3 at three; sum 22), Rome's 18, the
  8 % eigenvector gap, λ_max = 3.3461 and the eleven scores that go negative past
  it, the 4992-variant robustness figures, the two-strike attack survivor counts
  (7 against 5), and the personalized-PageRank margin flip (0.009 → 0.125).
- **One geometry across the whole Roman thread.** Twenty-five map figures go
  through `romelib.map_body()` and `assert_same_geometry()` fails the build, by
  city name, if any of them moves a disc.
- **Question slides carry no answers.** All 21 were read as source with their
  speaker notes; none names the answer that follows.
- **No tables, no code, no two-column text, no bullet list over four items,
  no paragraph under a fragmented list, no duplicate slide titles.**
- **Nothing overflows the frame.** Six slides did, and the sentences that came off
  them are in the speaker notes.

## Fixed during this round

- Ten slides failed the 26–52 px node band because a highlight **ring** around a
  disc reads to the gate as one 57 px disc. `figlib.mark()` now marks a node by
  thickening its own border, and `figlib.ring()` refuses to be drawn in a node
  fill colour close to a disc.
- The eigenvalue dots (16 bp) and the purpose thumbnails (26 bp) were being
  counted as undersized nodes; both are drawn at the band's floor now.
- `hits-collapses.png` rendered byte-identical to `roma-eigenvector.png` — which
  is the theorem, not a bug. The Part 7 slide reuses the Part 5 figure and says so.
- Two slides shared a figure with a different explanation; both now have their own.
- A caption claimed two marked edges where the figure marks one; another said three
  walks where the figure draws one of fourteen.
- Two slides landed their caption on the frame's content line, which the render
  crosses or clears depending on a pixel of font variance between runs. Both now
  carry a line less.
- The club summary marked its third student with a blue ring on a blue disc.
- **Slide 9 had no map on it.** It asks the room to point at a city and the map
  was on the slide before. It carries the map now.
- **Slide 10 showed no clubs.** It asks students to join two people who share a
  club and named only the thirteen students and the eight club names — the
  memberships had gone with the roster bullets when the slide went full width, so
  the exercise could not be done from the slide. The clubs are drawn on the figure
  now, as gold hulls. The first version drew a band between every pair of
  clubmates, which is the set of lines the student is being asked to draw; a hull
  says who shares a club and nothing more.
- Ethan and Ava sat 38 bp apart with 40 bp discs — two overlapping circles on both
  club figures. `_assert_club_geometry()` now fails the build on it.
- Slides 10 and 12 share one layout, so what the room draws is the picture the
  answer slide reveals.
