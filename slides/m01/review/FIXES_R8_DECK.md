# Round-8, part 2 — deck-side findings from the round-7 verification

Round 7 totals: 4 Blockers, 20 Majors. The figure-geometry items are being handled by the
`Circle` refactor (`FIXES_R8_CIRCLE.md`), which also closes the node-radius spread, the
ring-weight violations, and the edge/arrowhead boundary defects. **This list is the deck
markdown only.** Everything here lives in `m01-euler-tour.md`.

## Correctness

1. **Slide 046 "The directed Euler condition" states the wrong theorem.** The rule reads
   "Euler's condition, directed: in-degree equals out-degree, at every node" — that is the
   **circuit** condition, not the general one. The deck was careful to split these cases:
   slide 023 gives ≤2 odd → path, slide 025 gives all even → circuit. Two slides later, 048
   draws A→B→C, which **has** an Eulerian trail and yet fails 046's stated rule.
   **Fix:** qualify it as the closed-tour condition, and add the trail case — one node with
   out − in = 1 (the start), one with in − out = 1 (the end), all others balanced.

2. **Slide 046 also omits connectivity.** Directed Euler tours require *strong*
   connectivity, which the very next slides define and which is never tied back.
   **Fix:** one clause, the same way slide 023 handles it in plain language.

3. **Slide 046's figcaption contradicts its own figure.** The figure prints
   `in 0 / out 2` and `in 2 / out 0` — in-first on both nodes, matching slide 045 — while
   the caption reads "A: out 2, in 0 — B: in 2, out 0", out-first for A and in-first for B.
   **Fix:** match the figure's order on both.

## Structure

4. **Part Five is misfiled the same way Part Four was.** Its banner reads
   "Connectivity — Euler's theorem quietly assumed you can get everywhere", but four of its
   twelve slides (043–046) introduce directed graphs, in/out-degree and a new Euler
   condition before connectivity resumes on 047. Round 7 fixed exactly this class of
   misfiling for Part Four. **Fix:** add a divider before 043, or retitle Part Five so the
   banner covers what the part actually teaches.

5. **Part Six's banner vs its content.** The banner reads "How a computer holds a network",
   yet slides 055/056 teach $A^k$ walk-counting, interrupting the
   edge-list → adjacency-list → matrix → memory → CSR arc. **Fix:** either move the $A^k$
   pair, or widen the banner.

## Question/answer integrity

6. **Slide 055's prompt points at the wrong graph.** "Try it on the graph from the previous
   slide" resolves to 054's two-node multigraph, but 056 answers with $A^2$ of the five-node
   graph, last seen on 053. The 30-second beat is spent on a graph the answer never
   mentions. **Fix:** name the five-node graph explicitly, or move the multigraph slide ahead
   of 053.

7. **Slide 037 resolves slide 035's question using the wrong word.** 035 asks for a *trail*;
   037 answers in terms of a *path*. **Fix:** answer in the same term the question used.

8. **Slide 030's note contrasts "path" with "trail" one slide before 031 defines "path".**
   **Fix:** defer the contrast to 031, where both terms exist.

## Claims that cannot be checked from the slide

9. **Slide 061 — the 7,700× headline is unverifiable.** CSR at n = 100,000 is given as
   1,300,001 numbers, which requires 4m + n + 1 = 1,300,001, i.e. m = 300,000, i.e. mean
   degree 6 — stated nowhere on the slide. **Fix:** print "100,000 nodes, average degree 6"
   beside that bar pair.

10. **Slide 012 asserts a count its figure cannot show.** The body says "so A touches five
    bridges in all" directly beside a figure that draws A with exactly two edges. **Fix:** move
    the sentence to the slide that draws all seven, or add "the other three you counted on
    the previous slide".

## Density and layout

11. **Slide 040 — the $O(N+M)$ note is a second new claim, unfragmented, and it overflows.**
    Its glyphs reach y=717 in a 720px frame — every other slide in the range stops at
    629–685 — and it sits below both the figcaption and the page number. **Fix:** cut it, or
    give the cost its own slide.

12. **Slide 030 — P2.** Final state is figure + caption + two paragraphs + a four-line note,
    all landing at once with no `*` fragments. **Fix:** fragment the note.

13. **Slide 053 — P2, and it is the only figure slide in its range with no figcaption at
    all.** A previous round deleted the baked-in caption *and* the deck's figcaption. The
    slide also lands a cases formula, a body block and a four-line note together, and the
    note alone carries three claims on the slide that first defines the matrix.
    **Fix:** restore a figcaption that says something the body does not; fragment the note or
    give "degree, three ways" its own slide.

## Wording

14. **Slide 065's caption says "① and ②" but the figure draws bare 1 and 2.**
15. **Slide 070's caption calls a node-link diagram "the same map"** — "map" has meant the
    engraving or the sketch since slide 004. **Fix:** "the same graph".
16. **Slide 071's fourth bullet breaks the math mid-expression**, rendering as "O(m +" /
    "n)". **Fix:** keep $O(m+n)$ unbreakable, or shorten the bullet so it does not wrap.

## Standing rules — must not regress

No tables, no fenced code blocks, no inline backtick code, no `cols3`;
`<div class="cols">` is text + figure only; argument-revealing lists use `*` markers;
question slides contain no answer; exactly one plain-prose notebook pointer.

## Verify before reporting done

    grep -c '|---' m01-euler-tour.md     # 0
    grep -c '```' m01-euler-tour.md      # 0
    grep -c 'cols3' m01-euler-tour.md    # 0
    grep -c 'notebook' m01-euler-tour.md # 1
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

The figure generator is being refactored in parallel, so figures may change under you —
verify structure and text on the render, not figure content.
