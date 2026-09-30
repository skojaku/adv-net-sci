# m05 DECK_SPEC: *Community Detection* (rebuilt 2026-09-30)

The deck follows the lecturer's hand-drawn sketches of 2026-09-30 (three sheets, about
forty boxes). The previous 100-slide deck, *The Club That Broke in Two*, is in git history
(`git log -- slides/m05/m05-clustering.md`); `plan.md` and `FIGURE_SPEC.md` describe that
version.

## Voice (the lecturer's instruction for this deck)

Few words and one image per slide. "Let's …" and "We …". Direct, concise, plain English,
no rhetoric. No em-dash anywhere.

## Non-negotiables (from SLIDE_RUBRIC.md)

- one new concept per slide; question and answer on separate slides
- `*` fragments for a build; no paragraph below a fragmented list
- no tables, no code; `cols` is text + figure
- no `$…$` inside `figcaption`
- a figure's container in the generator matches the deck (`col` 537, `full` 1080,
  `tight` 320 high)

## Decisions taken while turning the sketches into slides

| sketch | slides | decision |
|---|---|---|
| "What do u see" (crossed out) | 2 | title "Let's look at a network"; the question is spoken |
| "What is the strongest community structure?" + clique | 4, 5 | question slide, then the clique as the answer |
| "Is the problem done? Bye!" | 6 | kept as written: "Done. Bye!" |
| "3 dimensions" + Density / Distance / Degree | 8-11 | ρ-dense, n-clique, k-plex; k-core, n-clan, n-club and k-truss go to speaker notes |
| "Q1 This is a ___ ? × 3" | 12-17 | one group (a triangular prism) asked three ways: 0.6-dense, a 2-clique, a 3-plex |
| "Works?" + "we don't like it: 1 vs rest" | 22, 23 | split into a question slide and an answer slide |
| "Zachary's karate club: Cut, RCut, NCut" | 27-29 | three slides, one method each: three club drawings side by side put the discs under the 26px floor |
| "Game: find a cut that minimizes ___" | 30 | the graph-cut game on the club, linked on the slide |
| "Modularity limitation" (crossed out) | none | dropped |
| "I need a slide to explain modularity" | 35 | the formula with each term as a fragment, and the worked value for the small club |
| "Turn it around" (crossed out) | none | SBM dropped |
| "Resolution limit: ring of cliques, n ~ √2m" | 39, 40 | ring of triangles: question, then 4 vs 10 triangles |
| "Karate: similar Q, different partition" | 41, 42 | two local maxima of Q, one per slide |

## Numbers on the slides, all asserted in `figures/figs_sketch.py`

- small club (9 nodes, 15 edges): Cut = 2 balanced, 1 for the lone node; ratio cut 1/10
  against 1/8; volumes 16 and 14; normalized cut 1/112 against 1/29
- 13 edges inside; configuration-model expectation (16² + 14²)/60 = 7.53; Q = 0.36
- karate club, unweighted: minimum cut 1 (node 12 alone); ratio cut 4 edges, 5 against 29;
  normalized cut 10 edges, 17 against 17, 32 of 34 on their recorded side (0-indexed 8 and
  9 swapped). Each is the best found by a 400-restart local search.
- ring of n triangles: apart Q = 3/4 − 1/n, pairs Q = 7/8 − 2/n; tie at n = 8 = √(2m)
- two local maxima of Q on the club: 0.407 (four groups) and 0.402 (three groups);
  best known 0.420 (also the target in the modularity game)
