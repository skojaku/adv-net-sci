# m03 FIXES — Round 6 (the reviewer reports)

Three of the four reviewer agents launched before round 1 returned their reports **after**
rounds 1–5 had already landed. They read the pre-R1 render, so every finding was triaged
against the current files before anything was changed. rev-24-46 (slides 24–46) never
reported; that range still has no independent read.

## Already fixed by rounds 1–5 — no action

| finding | round that fixed it |
|---|---|
| rev-1-23 B4 — `loop-waste` / `tree-def` text clipped and garbled | R1 (in-figure prose cut) |
| rev-1-23 M8 — "Znojmo" struck through by its cable | R1 (solver clears all 13 cables) |
| rev-47-69 B1 — slide 56's two yards overlapping | R3 (labels above each grid) |
| rev-47-69 B3 — slide 64's two regimes drawn as one chain | R2 (`fig_molloy_reed` rewritten) |
| rev-47-69 B4 — node discs shrinking with tree depth | R2 (`fan_tree`, one size) |
| rev-47-69 M5/M6/M7 — container mismatches at 48 % and 209 % | R1 |
| rev-47-69 M8 — "came in this way" clipped to "in / ay" | R2 |
| rev-47-69 M11 — 57 % vs 58 % | R4 |
| rev-47-69 m22 — κ = 7/4 under a title saying 1.75 | R3 |
| rev-70-92 B6 — `er1-a` clipped mid-word | R4 |
| rev-70-92 M10 — "no leaf left alone" over two degree-1 towns | R1 |
| rev-70-92 M5/M6 — slides 80, 83, 85, 89 at 48 % / 209 % | R1 |

## Confirmed still live — fixed this round

### Blockers

1. **Weight chips and step badges label the wrong cable** (rev-1-23 B1 + B3, rev-70-92 B3).
   `place_chips` filters a slot against other chips, discs and names — never against the
   *other edges*. With perpendicular offsets up to ±52 a chip lands nearer a cable it does
   not name. Measured by the reviewer: "17" is 4 px from Prostějov–Zlín and 36 px from its
   own cable; "49" is 8 px from Brno–Zlín and 33 px from its own. Slides 11 and 20 ask
   students to add these numbers up, and the same placement is baked into `kruskal.gif`
   and `prim.gif`. **Fixed at the generator:** a slot is rejected unless its centre is
   strictly nearest its own edge, with a 12 bp margin; the same rule now governs badges.

2. **Nine cables priced as "unused" on slide 78** (rev-70-92 B3, second half). `MST_PAIRS`
   stores three tree edges reversed relative to `CABLES` — `('Trebic','Jihlava')` against
   `('Jihlava','Trebic')` — so `[e for e in ALL_CABLES if e not in MST_PAIRS]` returns 9,
   not 6. Three tree cables print a price and four carry none, on the slide that asks the
   room to spend a budget. **Fixed:** compare on `frozenset`, and assert the unused set is
   exactly 6.

3. **Slide 91 "Module 03 in one picture" is a table** (rev-70-92 B9) — four bordered cells,
   header over value: a 2×4 table on a slide titled "in one picture". L2 is a Blocker, and
   N2 wants the visual to teach. **Fixed:** one Moravian drawing carrying the three
   numbers where they happened.

4. **Slide 84's κ = 2 is printed on a graph whose κ is 1.75** (rev-70-92 B5). The figure
   draws the ring *after* the cut — a 5-node chain, degrees 1,2,2,2,1, κ = 7/4, which is
   this deck's own number for "a path" on slide 66. **Fixed:** the figure draws the intact
   ring, which is what κ = 2 describes; the body text already says what one cut does.

### Majors

5. **Roadmap item 05 prints `$\kappa$` and `$f_c$` literally** (rev-1-23 M9). KaTeX does
   not process math inside a raw `<div class="steps-list">`. The gate that exists for this
   missed it: its regex is non-greedy up to the first `</div>\n`, so it only ever scanned
   item 01. **Fixed** in both the deck and `check_render.py`.

6. **Slide 60's ghost arrow** (rev-47-69 B2) — the arrow is drawn 34 bp above the edge it
   annotates, so it floats in white space touching neither node. **Fixed:** the arrowhead
   goes on the highlighted edge.

7. **Accent-3 used as text** (rev-70-92 M2) — gold `#DAB167` on white is 2.0:1, under the
   3:1 floor. **Fixed:** gold stays a stroke colour; its labels are set in ink.

8. **Slide 80 carries five principles and a figure that teaches none of them**
   (rev-70-92 B4, m5). **Fixed:** four principles, fragmented, with the figure carrying
   the one the drawing actually shows.

## Live and NOT fixed this round — recorded, not silently dropped

- **P2 progressive disclosure, deck-wide** (rev-1-23 M10, rev-47-69 M15, rev-70-92 M8).
  Fragments now appear on the slides that stack two body blocks, but this is a
  slide-by-slide judgement across 92 slides and only the worst ~10 were done.
- **`section.mid` bottom-anchoring** (rev-47-69 m17, rev-70-92 M13). `.formula:last-child
  { margin-bottom: 0 }` has equal specificity to `section.mid > :last-child {
  margin-bottom: auto }` and wins on order, so `mid` slides ending in a formula panel hang
  their content low and the page number can print inside the panel. The theme is shared
  with m01 and m02; changing it moves those decks too, so it is flagged for the lecturer
  rather than changed here.
- **Slide 7 is pixel-identical to slide 5** (rev-1-23 M5) — the "erase the map" slide
  erases nothing because slide 5 never drew a map. The honest fix is to draw a real map
  for slide 5, which is a new figure, not an edit.
- **Slides 14–15 show Part Two's answer before Part Two asks for it** (rev-1-23 B2). The
  Kruskal-order badges are gone (R3), but slide 15 still prints 292 km before slide 20's
  worksheet. This is a deck-structure decision — whether the MST definition may use the
  solved example — and belongs to the lecturer.
- **Yard aspect ratio vs the p_c claim** (rev-47-69 M13) — a 46×12 strip never shows a
  spanning cluster at p just above p_c, so "one puddle owns the yard" is not what the
  picture does. Needs a squarer yard and a tighter assertion.
- **Slides 24–46 have no independent read at all.**

---

# Round 7 — closing the unreviewed range (slides 24–46)

rev-24-46 never reported, so this range was read here, slide by slide, on the current
render. Four findings, all fixed:

1. **Slide 27 — F3** — "any cut" sat at y=330 on a 350bp canvas, so the page sliced its
   glyphs in half. Caught by the new clipping gate, along with seven other figures.
2. **Slide 31 — F3** — the Borůvka opening frame drew "every town is its own island"
   straight through the word "Znojmo". Notes carry numbers now, and a note that runs into
   a town name fails the build.
3. **Slide 39 — F1** — removing Brno leaves 3 + 3 + 1, so **two** pieces tie for largest;
   the figure ringed whichever one `max()` happened to return, telling the room it was the
   bigger. Both are highlighted now, and the tie is asserted.
4. **Slides 30, 37, 39, 81 — typography** — straight quotes; **slide 43** — "order" bolded
   for stress rather than as a term.

All 23 slides in the range have now been read individually.

## Coverage as it stands

| range | read by |
|---|---|
| 1–23 | rev-1-23 (full report) + spot checks here |
| 24–46 | **this session, slide by slide** (rev-24-46 never reported) |
| 47–69 | rev-47-69 (full report) |
| 70–92 | rev-70-92 (full report) |

Every slide has now been read by someone. What remains open is listed under "Live and NOT
fixed this round" above, minus the CSS item, which the lecturer authorised and which is
fixed: `section.mid` now out-specifies `.formula:last-child`, so question slides centre
their body instead of hanging it on the floor.

---

# Round 8 — the remaining reviewer findings

1. **Slide 15 showed 292 km before slide 20 asked for it** (rev-1-23 B2). Resolved without
   restructuring: the MST definition still *shows* which tree is cheapest; only the number
   waits for slide 21. The definition keeps its job and the worksheet gets its answer back.
2. **Slide 87 ringed the degree-2 bridge — the answer to slide 88** (rev-70-92 M1). The
   ring now appears only on the answer.
3. **Slide 53 printed "scattered pools" at p ≈ 0.9** (rev-47-69 M12), over the region its
   own sentence says one puddle owns. Moved to the flat left half.
4. **Slide 68's f_c annotation printed on top of the 0.75 axis tick** (rev-47-69 M9),
   making the one number the slide teaches unreadable.
5. **The yard never did what the text claimed** (rev-47-69 M13). A 46×12 strip is 552
   cells; at p = 0.65 two yards read 24 % and 17 % under the words "the same answer", and
   the assertion (< 0.20) was loose enough to allow it. The yard is now 88×24 = 2112 cells,
   which gives 2 % → 24 % → 59 % → 81 % across p — the sentence the slides actually make —
   and the paired yards sit above the threshold where they agree to two points, asserted
   at < 0.08.
6. **The sweep opened below the still before it** (rev-47-69 m19): p = 0.30 under a title
   reading "turning p up", after slide 51 had shown 0.40. It starts at 0.40 now.
7. **Slide 7 erased a map that was never drawn** (rev-1-23 M5) — slides 5 and 7 were
   pixel-identical but for a corner note. Slide 5 is now an actual map: the Morava and the
   Dyje, the southern border, and towns sized by population. Geography is drawn in
   annotation gray, never accent, so blue still means exactly one thing; slide 7 then takes
   all of it away and the abstraction happens on screen.
8. **`κ = ?`** set with no space before the question mark (rev-47-69 m25).

## Still open

- **P2 progressive disclosure** — fragments are on the slides that stack two body blocks,
  but a full slide-by-slide pass over 92 slides has not been done.
- **Edge crossings on slides 77 and 85** (rev-70-92 M9, m1). Slide 85's forest is planar
  and could be laid out crossing-free; slide 77's C₇(1,2) genuinely is not planar, so some
  crossings are unavoidable there.
- **Speaker notes** are on ~20 of 92 slides. The ones that exist carry the interaction;
  the rest are the lecturer's to write.

---

# Round 9 — the last three open items

1. **Edge crossings on slide 85** (rev-70-92 M9). The graph is a **forest** — three small
   components and four isolated nodes — so it can always be drawn crossing-free; dropping
   it on a circle put its two long chords straight across each other, on a slide about a
   network that has barely any edges. Laid out by component now, with zero crossings and
   disc clearance both asserted.
2. **Progressive disclosure** (rev-1-23 M10, rev-47-69 M15, rev-70-92 M8). Eight slides
   where two *claims* landed at once now build: slides 6, 27, 48, 62, 84, 86, 90, 92. The
   argument arrives, then the consequence it licenses. Question slides were left alone —
   their formula panel already separates setup from question, and `mid` centring fights a
   growing list. L5 re-checked across all 92 slides: no paragraph follows a fragmented
   list.
3. **Speaker notes** — 21 → **45 of 92**. Written only where a slide has a beat to run: a
   question to hold, a poll to collect, a GIF to time, a reveal to land. Slides that just
   state a fact were left without one, on the grounds that a note restating the slide is
   noise and the lecturer's words are his own.

Also: the Part Six divider and its payoff slide carried the same title verbatim
(rev-70-92 m9). The payoff slide is "The same hubs, both ways" and now carries **robust
yet fragile** as its bolded key term, where the phenomenon is actually named.

## Nothing known is open

Every finding from the three reviewer reports is either fixed, or recorded above with the
reason it was not. `check_render.py` exits 0 on 92 slides.

---

# Round 10 — re-verifying on the render that actually ships

The three reviewer reports were written against the **pre-round-1** render. Rounds 1–9
changed most figures, so their ranges had never been re-read on what ships. This round
re-read the slides whose figures changed. Three findings, none of which any earlier pass
could have seen:

1. **Slide 87/88 — the graph had two degree-2 nodes**, and both were cut vertices, so the
   deck's phrase "*the* degree-2 node" was ambiguous and the figure supported either
   reading. The bridge now joins the two hubs directly: exactly one node has degree 2, and
   an assertion says so, because the slide's sentence is singular.
2. **Slides 60 and 62 — an avoidable crossing on a planar graph** (rev-47-69 M14,
   confirmed on the current render). The q(k) layout had `(h,e)` crossing `(c,d)`;
   swapping two nodes makes every non-radial edge a vertical. Zero crossings asserted.
3. Slide 21's step badges now sit on leader lines where the cable is too short to carry
   them — checked, and each badge leads to the cable whose step it names.

## Where this leaves the deck

`check_render.py` exits 0: 92 slides, 370 node discs in a 26–48 px band, nothing past the
content box, no container mismatch, no clipped ink, no math in a figcaption.

Coverage is honest but not uniform: every slide has been read at least once, and the
slides changed since the reviewer reports have been re-read here. A fresh four-way pass on
the current render would still be the right next step before the deck is taught — that is
what the playbook asks for, and it has not been run against this state.
