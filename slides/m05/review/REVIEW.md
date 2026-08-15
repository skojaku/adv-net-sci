# Slide review — slides/m05/m05-clustering.md — 2026-08-06 (round 2)

**Verdict:** PASS with recorded gaps · **Slides:** 106 · **Blockers:** 0 · **Majors:** 0 outstanding · **Minors:** 0 outstanding

`python3 check_render.py` exits 0 on the current render, and the render is current
(`find figures -newer review/slide.001.png` returns 0).

**This verdict is weaker than it looks — read the coverage note.**

## Coverage note (REVIEW_PLAYBOOK: "if a subagent review does not arrive, say so")

Four reviewers were launched on Opus over disjoint slide ranges (1–27, 28–53, 54–80,
81–106 plus the structure pass). **All four died on a session limit before reporting.**
Both rounds were therefore driven by the lead's own pass over the render plus the checker
— one pair of eyes, not five. Round 1 covered roughly forty slides closely; round 2 covered
the ones round 1 had not reached. Slides that have still had only a quick look:

    27 · 29 · 31–32 · 34–35 · 38 · 40 · 44–45 · 48 · 51 · 54–55 · 57 · 59 · 61–62
    65–68 · 72–76 · 81–84 · 86 · 88 · 91 · 93 · 96–99 · 103

**The next round must start there**, with independent reviewers.

## Milestones (structure pass, S5)

| part | interactive element |
|---|---|
| 1 · The club that broke in two | **yes** — draw the dividing line on paper, then hands up (slide 8) |
| 2 · What counts as a group? | **yes** — peel the club to its 4-core, counting aloud, on the GIF (slide 21) |
| 3 · Cut it | **yes** — live demo, `graphcut × two-cliques` (slide 31) |
| 4 · More than chance | **yes** — compute Q by hand on two triangles (slide 51) |
| 5 · Climbing Q | **yes** — Louvain run live in the notebook, different seed, different answer (slide 72 pointer) |
| 6 · Turn it around | **yes** — reorder the adjacency matrix until the blocks appear (slide 71) |
| 7 · Three ways modularity lies | **yes** — two live demos, `two-cliques-big-clique` (77) and `random-net` (84) |
| 8 · How would you know? | **yes** — score six people by hand, NMI then pairs (slide 94) |
| 9 · Where this lands | recap only — no demo needed |

## Four-act arc

- **S1 story** — Part 1: Wayne Zachary, 1970–1972, a named karate club, a dated split.
- **S2 maths of *that* story** — Parts 2–3: cliques and cores counted in that club;
  Zachary's own min cut reproduced on it, 33 of 34.
- **S3 generalization** — Parts 4–6: modularity from the balls-and-strings game, Louvain
  and Leiden, the SBM.
- **S4 edge cases as questions** — Parts 7–8. Every one of the six limitations opens as a
  question slide with the answer on the next slide: does modularity separate two cliques
  (74→75), what if a third group is added (76→78), is there one best grouping (81→82),
  what does it return on a random network (83→85), how do you fix a score chance already
  passes (96→97).

## Fixed this round (all verified on the re-render, not on the source)

**Round 1 — five Majors.** The k-core GIF led with the untouched club, so the static
export repeated slide 6; "four overlapping pattern-groups" was unreadable on 34
intermingled discs; the bag figure claimed a member's three balls and connected none of
them; three student guess-lines stopped short and read as stray marks; and slide 92's
figure said "they agree about five of the six", which counts label identity across two
partitions — the exact mistake NMI and ARI exist to prevent, three slides before the deck
introduces them.

**Round 2 — four more.** accent-2 marked both "the officers' group" and "this string
matches" in one figure; the deck quoted "two crossings out of thirty" where the drawing has
sixteen friendships; the Q worksheet's answer floated over the bridge edge with no boundary
drawn; and fourteen balls scattered with `rng.uniform` merged into blobs.

**Found by the gates before any human looked:** two byte-identical figures on slides that
explained them differently; number-line labels printing through each other on two slides;
96px and 88px discs against a 26–52px band; and — from the disc-overlap gate added this
round — two stacked five-cliques whose facing members sat 20bp apart with 32bp discs.

## Known and accepted

- **The club is drawn with 79 edge crossings.** 34 nodes and 78 edges is not planar, so F2's
  "draw it planar" has no answer. `layout.py` anneals under three hard constraints instead
  (discs ≥46bp apart, no edge within 20bp of a disc it does not end at, nothing off the
  page) and every mechanism figure is held to zero crossings.
- **Colour changes meaning twice**, on slides 87 and 99, where accent and accent-2 mark
  Louvain's groups rather than the two clubs. Both figcaptions say so.
- `check_render.py` reports "smallest ink measures 3px x-height" on nine data figures.
  Those are axis ticks and hyphens, not glyphs — the checker says as much in the warning.
