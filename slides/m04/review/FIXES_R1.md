# m04 round 1 — fix spec

Four reviewers read disjoint ranges of the rendered deck and all four returned:
`REVIEW_R1_A.md` (001–023), `_B.md` (024–046), `_C.md` (047–068), `_D.md` (069–090).

**Round 1 totals: 6 Blockers · 38 Majors · 34 Minors. Verdict FAIL.**
`check_render.py` exits 0 throughout, so none of this is gate-visible — every item below is a defect the
gate cannot measure.

Work is split by file so nothing collides. **Touch only your own file.**

---

## Adjudications — read before working

Three findings conflict or need a call; these are the rulings, and they override the reviewer text.

1. **12–13px marks.** Reviewer B filed the tally dots on `sampling-bias.png` (slide 042) as under-size;
   reviewer C measured the same size class in Part Five and showed they are **scatter markers in data
   plots**, which are legitimate and stay. The ruling: **countable objects** the room is asked to count and
   compare — `sampling-bias.png`'s two rows of people — get raised to 26–40px. **Data-plot markers do not
   change.** Do not "fix" a scatter plot because of this item.
2. **The KaTeX line under the derivation figures (029, 030, 031).** Two reviewers independently called it
   redundancy: the panel already sets the equation, the figcaption says it a third time in words, and the
   eye has to compare two typesettings to confirm they match. Delete the KaTeX on all three. Slide 031 then
   needs a body line that is *not* the equation — use the Feld provenance sentence (spec D-9 below).
3. **`feld-friendmeans.png` has its names.** I reported them missing; reviewer A measured the render and
   they are there, each chip nearest its own disc by ≥2.3× and drawn in its disc's colour. No action. I was
   reading a stale copy — the render is the authority, which is the whole point of the playbook rule.

---

## A. `figures/figs_story.py` — figures for slides 001–046

**A-1 · BLOCKER · `rosters.png` (024) reads as a table.** L2. A header row of eight names over eight
equal-width, top-aligned columns: 24 cells on a shared baseline grid. There are no rules, but the alignment
is actively misleading — the third line of Sue's column ("Dale") has nothing to do with the third line of
Alice's ("Pam"), so every horizontal read is noise. Redraw as **eight left-aligned, ragged-right lines**,
one per girl: `Betty: Sue` / `Sue: Alice, Betty, Dale, Pam` / … Keep accent-2 on every occurrence of Sue and
Alice — that mark-up is what makes the point. Also mark Betty's and Tina's single occurrences in accent so
the caption's second clause ("Betty and Tina on one") can be checked (A-2 below covers the caption).

**A-2 · BLOCKER · `fb-twitter.png` (040) carries two points and is a bar chart.** P1 + F4. It draws three
bars — Facebook mean 92.7%, Facebook **median** 83.6%, Twitter >98% — on a common 0–100 scale, so all three
are nearly full and their lengths carry nothing. Worse, mean-vs-median is not introduced until slide 076,
36 slides later, and the word *median* appears nowhere on slide 040. **Cut the median entirely** (slide 076
owns it) and **stop using bars**: draw two strips of 100 small discs, one Facebook one Twitter, with 93 and
98 of them in accent-2 — the object, not a length. Put the population (721 million) on the drawing; it is
the reason the slide is impressive and it currently lives only in the speaker note.

**A-3 · MAJOR · `degree-def.png` (015) draws four edges as two straight lines.** F4. The four neighbours sit
at the corners of a rectangle with the hub at its centre, so both diagonals are collinear through it
(measured slopes 0.489 / 0.484). At reading speed the eye counts two lines on the one slide whose entire job
is "four edges attached, so degree four". Redraw as a genuine star — roughly 60°, 130°, 220°, 310° — so four
separate strokes leave the disc. Assert no two edges are collinear through the hub.

**A-4 · MAJOR · `handshake.png` (020) is the emptiest figure in the deck and its arc reads as an edge.**
F1 + F4. Three isolated discs, one dashed accent-2 arc, one X, and a gray label "3 nodes of odd degree" — no
node carries a degree, there is no network, and the body's argument (degrees sum to even, so odd ones pair
off) appears nowhere in the picture. Every earlier slide draws a line between two discs to mean an edge, so
the arc reads as one. This is the payoff for a two-minute student construction. Redraw: **an actual small
graph** with degrees printed in the discs, the odd-degree nodes in accent-2, a running sum ticked off the
way `sum-ends.png` does it so well, and the last odd node left with nothing to pair with. Distinguish the
pairing from an edge (a bracket or a shaded lasso, not a line) and label it **inside** the drawing.

**A-5 · MAJOR · `pk-def.png` (021) shows counts where the slide defines a fraction.** F4. The body says
p(k) is "the fraction of nodes whose degree is exactly k"; the figure's y-axis is labelled **"nodes"** and
the piles are 2, 5, 4, 1 for a 12-node network that appears nowhere else in the deck. No denominator is
stated. Rebuild the piles **from the eight girls** — they are the deck's running example and slide 022 is
already their labelled version — label the axis "fraction of nodes", and print the fraction under each pile.

**A-6 · MAJOR · `qk-formula.png` (028) redraws the previous slide instead of the new idea.** F4. It is 20
tallies with 4 in accent-2; slide 027's `bag-of-hands.png` is 20 discs with 4 in accent-2 — same count, same
colour meaning, same fraction, different glyph — while the slide's actual content (the draw probability
being *proportional to k*) has no visual at all. Redraw as **all eight girls' hand-counts side by side**
(Betty 1, Sue 4, Alice 4, Jane 2, Pam 3, Dale 3, Carol 2, Tina 1) so the reader sees the chance of being
drawn rise with k. Keep the edge-end glyph identical to slide 027's and 034's — reviewer B measured the same
object at 8×63px on 028 and 4×39px on 034, in a deck that otherwise keeps its objects stable. **One tick
geometry for edge ends across the module**; put it in a module-level constant.

**A-7 · MAJOR · `acquaintance.png` (044) is a three-panel strip shown at once, at the range's smallest
discs.** F4 + F1 + F3. The three panels are the same five-node graph and differ only by a small ring moving
and an arrow appearing, so the reader has to diff three near-identical drawings. **Emit three files**
(`acquaintance-1/2/3.png`) for three consecutive slides — the deck already does this well at 029–031, and
the deck agent is adding the two extra slides (D-6). Raise the discs from 28px to 40px to match every other
graph figure in the range, and state the two marks in-panel ("picked" / "immunised") — nothing currently
says that a ring means chosen and a fill means immunised.

**A-8 · MAJOR · `sampling-bias.png` (042) draws its countable objects at 13px** against 40px node discs in
its own left panel. F3. The arithmetic is right (1 of 7 against 6 of 18 = 2.3×) and the point is good, but
the room is asked to compare two red fractions in marks a third the minimum size. Raise the tally dots to
26–40px, wrapping the 18 onto two rows if the width will not take them. **See adjudication 1: this applies
to this figure only.**

**A-9 · MAJOR · `feld-degrees.png` (008) changes the graph's scale mid-build.** F4. Measured on the render,
the eight-girl drawing spans 830×200px on slides 006, 010, 011 and 017 and **431×104px on 008** — 52% on
both axes — because 008 puts it in a `cols` column. The discs stay 39–40px, so the edges halve against
unchanged discs and the Sue–Pam–Alice triangle knots up. The deck agent is moving slide 008 to a full-width
layout (D-2); **re-emit `feld-degrees.png` at `container="full"`** to match, and assert its drawn width
equals the other four.

**A-10 · MINOR · `timeline-1961.png` (005) and `pk-def.png` (021) sit exactly on the type floor.** F3.
"30 years" measures 15–17px x-height and the rotated "nodes" axis label 15–16px, where every other label in
the range measures 16–17px. Bump both one step so a re-scale cannot push them under.

**A-11 · MINOR · `feld-worksheet.png` (010): Jane's ring is unexplained.** F1. Hers is the only disc with a
60px accent-2 ring and nothing says why. Add a two-word in-drawing label beside it ("e.g. Jane").

**A-12 · MINOR · `bag-of-hands.png` (027): unexplained initials, and a colour that changed meaning.** F1.
The 20 discs are lettered B/S/A/J/P/D/C/T with nothing saying these are the girls' initials, and accent-2
meant "the two degree-4 hubs" on slide 024 but means "Sue only" here, so Alice's four discs go blue one
slide after she was red. Spell two or three names out in full inside their discs, and either keep Alice red
or say in the annotation why she is not.

**A-13 · MINOR · `coauthor-gap.png` (039) prints 82.8% where the body says "nearly 83%"** and 8.1/22.1 where
the caption says "eight … twenty-two". Derive both occurrences of each number from one value; the deck agent
is matching the prose (D-8).

---

## B. `figures/figs_tail.py` — figures for slides 047–074

**B-1 · BLOCKER · `ccdf-def.png` (055) never says what one dot is, and its two counting stories disagree.**
F1. Each column is a node and each dot one unit of its degree, but nothing states that. The figcaption says
"count everybody above the line"; the ink above the dashed k=3 line is **11 dots**, while the in-figure text
prints "above the cut / 5 of 20 = 0.25". And accent-2 marks whole *columns*, so **26 red dots are drawn and
15 of them sit below** the line the label says they are above. The y-axis is titled "degree" with no tick
values; the x-axis is unlabelled. Fix all three: put a "one node" bracket under one column and a "1 edge"
caliper beside one dot, give the y-axis its ticks, and make the counted quantity match what is red —
**"5 of 20 nodes sit above k = 3"**, with only those five columns in accent-2.

**B-2 · BLOCKER · `cdf-vs-ccdf.png` (057) puts one shared y-axis title over two different axes.** F1.
"share of authors" is drawn once at the far left, but the left panel is linear (0, 0.5, 1) and the right is
logarithmic (1, 10⁻², 10⁻⁴). Nothing says so — and the unlabelled log transform is exactly what produces
the difference in shape the slide asks the room to read, so the comparison is confounded by a change nobody
mentioned. Give each panel its own y title, mark each panel's scale in its frame ("linear" / "log"), and
state the real reason in the drawing: the CDF's values run to 1, which a log axis cannot spread; the CCDF's
run to 0, which it can.

**B-3 · MAJOR · `linear-axes.png` (047): the caption's claim is not what is drawn.** F1. The figure draws
**122 dots**, one per distinct degree, at height p(k) — no author is plotted individually. The deck agent is
rewriting the caption (D-11); your side is to make sure the figure states its own unit, and to **print
cond-mat's `Var(k)/⟨k⟩` on this figure** — the title promises the variance, slide 045 ends by asking for it,
and no variance number appears anywhere in Part Five (C-minor 22). Print the same quantity beside the 1.00
on `poisson-ccdf.png` (067) so the two can be compared; that closes the loop Part Four opened.

**B-4 · MAJOR · binning is asked about before it exists.** N1 + F4 + P2. Slides 050/051 plot one point per
observed degree, unbinned (`condmat_pdf()`: "One point per observed degree, no bins"), yet slide 050's
caption says "identical **bins**" and slide 053 asks "That plot had bins. What happens if I choose different
ones?" — then 054 answers with a *different* construction (histogram densities over k ≥ 10 at widths 1, 8,
32). Emit a new figure, **`binned-once.png`**, re-expressing the same tail as counts in width-1 bins, for
the new slide the deck agent is inserting before 053 (D-12). Then in `binning.png`: **emit it as three
files** (`binning-1/2/3.png`) for a three-slide build, and **put y tick labels on every panel** — panels 2
and 3 currently have none, so the shared vertical scale the whole comparison rests on cannot be verified.

**B-5 · MAJOR · `slope-derivation.png` (059) contains no drawing.** N2 + F4. Three numbered text lines and a
gray gloss column is not a visual. Draw the thing being integrated: the p(k) power law with the region above
k shaded, and that shaded mass re-plotted as one point on a CCDF beside it. The deck agent is deleting the
duplicate KaTeX line (D-4).

**B-6 · MAJOR · `slope-worksheet.png` / `slope-answer.png` (060/061): the data is synthetic and the slide
does not say so.** N1 + F1. It arrives after nine consecutive slides of cond-mat, and the only tell is that
x reaches 1000 where cond-mat stopped at 279. A student who reads it as the same network gets **γ = 2.3
here against the γ = 2.44 fitted on slide 051** — two answers, on the slide that teaches the two routes
agree. Title the panel in-figure: **"a different network"**. (Do not switch to cond-mat: the exact −1.3 is
what the exercise needs, and the generator's own comment says so.) On `slope-answer.png`, **strike the wrong
answer in annotation gray**: accent-2 currently sets both γ = 2.3 (the right answer) and the strike-through
cancelling γ = 1.3, so red means two opposite things 90px apart.

**B-7 · MAJOR · `exercise-card.png` (062) encodes nothing.** F4. A rounded rectangle containing the words
the left column already says — a text column beside a picture of a text column. Replace it with the four
thumbnail plots the *Data Visualization* handout actually asks students to compare, so the room can see what
it is being asked to look at. If those four are not reconstructable, say so and the deck agent will cut the
figure and let the prose stand.

**B-8 · MAJOR · `hubs-share.png` (064) introduces a rank axis that the deck never introduces.** N1. Every
plot in the preceding seventeen slides is p(k) or P(k′>k) against k, and the word "rank" appears nowhere in
the deck's prose. Make the point **on the CCDF that is already on screen**: mark the top 65 points and shade
their share. Keep the number honest — the figure says "33.8% of all 25,144 edge ends" and the deck's caption
says "34% of all connections"; use **edge ends** in both (the deck agent has the caption, D-13).

**B-9 · MAJOR · `universality.png` (065): the "physicists" label is nearer a curve it does not name.** F3.
Measured on the render: 50px to the physicists curve, 55px to the Internet curve, **23px to the yeast
curve** — only its colour resolves it. The generator moved it there to stop it lying across its own tail,
trading one defect for another. Fix it in the solver, not by hand: give it the *other* curves as blockers
with a clearance floor and its own curve as the attractor, and assert that each label's nearest curve is the
one it names. The blue curve's k ≈ 30 stretch has clear space directly above it.

**B-10 · MAJOR · accent-2 flips from exemplar to counterexample across 065 → 067 → 068.** F5 + F1. Red is
"the Internet, the hub-rich real network" on 065 and "the random graph, the one with no hubs" on 067 and
068; blue is the physicists on 065 and a BA model labelled "power law" on 068. Fix a **deck-wide role from
Part Six on: accent = has hubs, accent-2 = does not**, and recolour accordingly. On 068, either name the
blue curve for what it is (a growing network) or use the cond-mat CCDF, which is already computed.

**B-11 · MAJOR · `poisson-ccdf.png` (067): "the same average" never says as what.** N1 + F1. The only number
on the slide is ⟨k⟩ = 4.0, which is neither cond-mat's **8.08** nor the Internet's **3.88**. Name the
comparison in the drawing and use the real mean, not a rounded 4.

**B-12 · MAJOR · the growth layouts have 20 and 21 edge crossings** (`growth_pos`, used by `ba-growth.gif`,
`quiz.png`, `quiz-answer.png`). F2. Both graphs are non-planar at 24 nodes and 45 edges so some crossings
are forced, but 20 is far above the minimum, and these discs are 29px — the smallest in the deck against
39–40px elsewhere. The result is that slide 072 asks the room to tell two hairballs apart. Add a
crossing-minimising pass to `growth_pos` and **assert a crossing budget**; if that will not come down far
enough, drop to ~14 nodes so the hub is traceable. Raise the discs while you are there.

**B-13 · MAJOR · `quiz.png` (072) and `quiz-answer.png` (073) conflate two different networks.** F1, and on
073 it is a **Blocker**: the deck prints "largest degree 315 with preference, 29 without" directly beneath a
drawing whose busiest node has **15** edges, because the sketches are the n=24 growth graphs while the CCDFs
and the numbers 315/29 come from n=20 000 runs. Slide 071 prints "largest 15 edges" over that same drawing,
so the deck states two maxima for one picture. Put the switch **in the drawing** — a line under the sketches
reading "sketches: 24 nodes · tails: 20 000 nodes" — on both figures. (The deck agent is fixing the captions
too, D-14, but the figure must carry it: a caption is not where a student looks when counting spokes.)

**B-14 · MINOR · `fat-tail-reveal.png` (049): the accent-3 band starts at k = 96, not 100.** F1. Its left
edge lands 23px left of the "100" tick that the annotation above it names, and its top edge encodes nothing.
Derive the band's left edge from the annotation's threshold instead of hardcoding it.

**B-15 · MINOR · `loglog-line.png` (051): "R² = 0.93" is printed in accent-2 and never used.** It is the
only inferential statistic in Part Five and nothing on the slide or after it says what to do with it. Cut it
(the deck agent will not reintroduce it).

**B-16 · MINOR · curves that leave the bottom of a log axis terminate on the axis line** — the γ = 3.5 curve
on `powerlaw-def.png` (052) at k ≈ 50, and the lattice wall on `three-ccdfs.png` (068) at k = 4. On a log
scale the floor is 10⁻⁵, not zero, so both read as "the distribution ends here". Stop the stroke a few px
above the axis, or fade it.

---

## C. `figures/figs_edge.py` — figures for slides 075–090

**C-1 · MAJOR · `directed.png` (080) does not show the point.** F4. Two panels of one 6-node digraph
labelled with in- and out-degrees, annotated "8 arrows = 8 in = 8 out". Nothing compares a node to the nodes
at the other end of its arrows, which is what "tilt" means — so the body's claim is asserted, not shown. And
the arrow-conservation line is a different idea the slide never uses. **Compute the comparison from the
drawn graph and print it under each panel** — "you: 1.3 · the account at the other end of an arrow: 2.7",
computed and asserted, not typed — and cut the conservation annotation.

**C-2 · MAJOR · `assortativity.png` (082) and `assortativity-real.png` (083): `r` is never defined and the
axis has no title.** F1. Slide 082 names **assortativity** in bold but gives no symbol, no number and no
range, so on 083 the dot positions encode an unnamed quantity and a student cannot judge whether +0.226 is
large. Title 083's axis "assortativity $r$" and mark −1 / +1. On 082, **print the three r values on the
three schematics** — computed from the graphs as drawn they are **+0.30 / −0.70 / 0.00**, which is exactly
the story the slide is telling and is currently invisible. Compute them; do not type them.

**C-3 · MAJOR · `lognormal-trap.png` (086): the deck claims three decades and the figure shows 2.3.** F4.
The data runs about 5 to 1000 and the fit window is `ccdf_fit(..., 3, 500)` — 2.2 decades. Either widen the
drawn and fitted range until three decades is true, or print the real span on the figure and tell the deck
agent, who will change the sentence (D-16). Do not leave the sentence ahead of the figure.
`verify_numbers.lognormal_degrees`'s docstring repeats the same wrong claim — flag it, do not edit that file.

**C-4 · MAJOR · `scale-free-debate.png` (087): the 2019 dot carries no content.** F4. The title promises a
statistical test, the figure is a bare 1999/2011/2019 chronology, and the punchline — Broido & Clauset
fitting 927 networks and finding strong scale-free evidence in about 4% — sits only in the speaker notes.
Put **"927 networks, fitted properly · strong evidence in 4%"** under the 2019 dot. That single addition
makes the timeline earn its title and fills a slide whose ink currently stops 130px above its neighbours'.

**C-5 · MAJOR · `consequences.png` (088) asserts a result the course never derived.** N1. The third branch,
"spreading, ⟨k⟩/⟨k²⟩ = 0.045", names no module because no module covers the epidemic threshold — while the
caption calls all three "results we have already proved". Mark that branch as forthcoming in the drawing
(the deck agent is changing the caption, D-17). Also **name the network**: `f_c = 0.95` and
⟨k⟩/⟨k²⟩ = 0.045 are cond-mat, last seen 32 slides earlier, and the figure says neither.

**C-6 · MAJOR · `individual-vs-average.png` (076) is being split.** P1. The deck agent is splitting slide
076 into two — the hub reversal, then mean-vs-median — because the slide currently teaches a network of
eight girls and a 721-million-user dataset at once. **Emit two figures**: `individual-vs-average.png` keeps
only the eight girls sorted 5 / 2 / 1, and a new `mean-vs-median.png` carries Facebook's 92.7% / 83.6% pair.
On the first, fix the ambiguity reviewer D flagged: "5 have fewer" never says fewer *than what* — write
"than their friends have, on average" on the drawing. On the second, the axis title currently renders as
"% below their friends'" with a dangling apostrophe that reads as clipped text; finish it.

**C-7 · MINOR · `vanishing.png` (078) prints Var(k) = 0 four times.** L4/F4. Once under each panel and again
in the body. Print it once, centred under the row.

**C-8 · MINOR · `recap.png` (089) recolours the eight girls against the key the deck taught.** F1. It draws
them **5 red + 3 gray** under "5 of 8 below", where slide 076 draws 5 red / 2 blue / 1 gray with gray
meaning *equal* — so a student holding that key reads three ties. Red also changes meaning inside this one
figure: "below" in panel 1, "the gap the variance buys" in panel 2. Keep 076's 5/2/1 colouring, and draw the
identity's gap segment in gray. The figure also drops all of Part Seven, which slide 090 then opens with —
add assortativity to the recap.

---

## D. `m04-node-degree.md` — the deck

**D-1 · BLOCKER · split slide 076.** P1. It teaches the hub reversal *and* mean-vs-median, on two different
datasets, and the body needs an "and" to state it. Make it two slides: the eight girls and the hub reversal
first, then mean-vs-median with its own question beat — it is the more surprising of the two (nine million
Facebook users sit in that gap) and currently gets a third of a slide. Figures come from C-6.

**D-2 · MAJOR · lay slide 008 out full width.** F4. Move its two paragraphs above the figure so the
eight-girl graph never changes scale across the 006 → 008 → 010 → 011 → 017 build. Use `![w:1080]` and the
plain `<div class="fig">`; figure re-emitted by A-9.

**D-3 · MAJOR · fragment slides 008 and 012.** P2. Both land two paragraphs plus a gray note plus a
captioned figure in one flash, and slides 001–023 contain **zero** fragment markers (m03's deck used 16). On
012 the punchline "2.5 → 3.0", the disclaimer and the figure all arrive together right after two slides of
student work. Fragment with `*` so the number lands first and the caveat second.

**D-4 · MAJOR · delete the duplicate KaTeX under the derivation figures (029, 030, 031) and under 059.**
See adjudication 2. On 031, replace it with the provenance sentence rather than nothing: *"Feld writes this
line out himself, on page 1470."* — a fact the figure does not carry.

**D-5 · MAJOR · slide 029 skips a step.** N1. The panel jumps from `Σ k q(k)` to `⟨k²⟩/⟨k⟩`; the
substitution `Σ k · k p(k)/⟨k⟩` is never shown and `⟨k²⟩` has not appeared anywhere earlier in the deck.
Ask the figs_tail agent for a fourth panel state — no: this figure is `figs_story`'s. Coordinate by leaving
the request here: **`derivation-1.png` gains a line** so the build is substitute-then-name, one new idea per
line. File it against A as A-14 when you dispatch.

**D-6 · MAJOR · split slide 044 into three.** F4. `acquaintance.png` is three near-identical panels shown at
once; A-7 emits `acquaintance-1/2/3.png`. Three consecutive slides, one step each: pick at random → ask for
one name → immunise the named person.

**D-7 · MAJOR · split slide 045.** N4 + S5. The milestone demo is run on top of its own answer: the speaker
note says to let two students play random against nomination *before* showing the curves, and the slide
already prints "At random, 88% … By naming a friend, 2%" and both labelled curves. Make a prompt slide
("random or nominated — which wins, and by how much?") and keep this as the reveal.

**D-8 · MAJOR · slide 045's body and figure disagree.** The curve is labelled "random 87%" and the body says
"At random, **88%**". Take the figure's value and write it in the body, both derived from
`immunization_curves()`. While there: slide 039's body says "nearly 83%" against the figure's 82.8% — use
82.8% in both, and "8.1 … 22.1" in the caption instead of "eight … twenty-two".

**D-9 · MAJOR · slide 045's y-axis is unnamed and secretly logarithmic** — ticks 100/10/1/0.1% at even
spacing with no title and no note of the scale, **five slides before Part Five's whole argument is that an
unannounced change of ruler misleads you.** The axis title and scale label are B's work if the figure is
`figs_tail`'s and A's if it is `figs_story`'s — it is `figs_story`'s (`immunization-curves.png`), so file it
as A-15: title the axis "largest component remaining" and mark the log scale.

**D-10 · MAJOR · put a thinking beat on every question slide.** N4. Slides 016, 048, 053, 058, 060 and 066
pose the question and stop; the beat exists only in the speaker note, where the room cannot see it, so the
lecturer has to remember to create the pause six separate times. Add one visible line each — "Take 30
seconds", "Hands up: 1.3 or 2.3?", "Predict the shape first". Slides 007, 019 and 023 already do this and
are the model.

**D-11 · MAJOR · fix the captions that describe something the figure does not draw.**
- 047: "every one of 23,133 authors, plotted by how many coauthors they have" → the figure draws 122 dots,
  one per distinct degree. Rewrite: "the 122 distinct coauthor counts among 23,133 authors, and how common
  each one is".
- 050: "identical data, identical **bins**" → there are no bins. "identical data, identical points — only
  the ruler changed".
- 049: "78% of authors sit in the first ten **columns**" → it is a dot plot, and its own annotation says
  "k ≤ 10".
- 024: "Betty and Tina on one" → only checkable once A-1 marks those two occurrences.
- 056: "one point per distinct degree" was already true of the histogram, so it does not distinguish the
  CCDF. Say the real distinction: "no width to choose — every node counted at every k".

**D-12 · MAJOR · introduce binning before asking about it.** N1. Insert one slide before 053 that
re-expresses the same tail as counts in width-1 bins (figure `binned-once.png`, B-4), so the question "what
happens if I choose different ones?" has a referent.

**D-13 · MINOR · slide 064's caption says "34% of all connections"** where the figure says "33.8% of all
25,144 edge ends" — in a deck that taught the 2M distinction eight parts ago. Use "edge ends" and 33.8%.

**D-14 · MAJOR · slides 072 and 073 captions claim the drawn networks are the plotted ones.** F1. 072: "two
networks, same size, same average degree — and their two tails"; 073: "largest degree 315 with preference,
29 without" over a drawing whose busiest node has 15 edges. Name the switch: "sketches: 24 nodes · tails:
20 000 nodes". Figure carries it too (B-13).

**D-15 · MINOR · slide 069's headline reads "What is real networks doing"** — subject-verb disagreement at
40px on the slide that pivots the whole part. "What **are** real networks doing…".

**D-16 · MAJOR · slide 086 claims three decades** where the figure shows 2.3 (C-3). Change to two decades
unless the figure agent widens the range; coordinate before writing.

**D-17 · MAJOR · slide 088's caption says "three results we have already proved"** where the third,
spreading, was never derived in this course (C-5). "two results we proved, and one to come".

**D-18 · MINOR · centre the shallow slides.** L6, measured bottom-most ink out of 720: **012 → 441**,
**028 → 416**, **032 → 478**, **050 → 533**, **052 → 533**, **056 → 534**, **062 → 471**, **087 → 495**,
**089 → 487**. Add `<!-- _class: mid -->` to each.

**D-19 · MINOR · slide 077 names no builder and shows no link.** S5. "Open the builder and try" — the path
(`friendship-paradox-game.html`) lives only in the speaker note. If students open it on their own machines,
put it on the slide.

**D-20 · MINOR · stop saying the same thing three times.** P3. On 017 the count appears as the in-figure
"10 lines, 20 ends", again in the figcaption, and again in the body, all within 130px; 013 repeats its three
in-figure labels verbatim in its caption; 061 states γ = 2.3 in the title, the figure, the caption and the
body. Let the figure's own label carry the count and use the figcaption for what the drawing does not say.

**D-21 · MINOR · cut slide 015's second paragraph.** N1. "the spread of degrees says how centralised the
thing is" uses the degree distribution six slides before it arrives, and "exposure" and "centralised" each
appear exactly once in the whole deck and are never defined or picked up.

**D-22 · MINOR · fold slide 009 into 010.** P3. They give one instruction across two slides and 009's final
state is a formula box plus one line with 245px of dead space. Move 009's framing line ("Same eight girls.
Same ten lines. A different question.") above 010's worksheet.

**D-23 · MINOR · slide 068's title names one third of its figure.** F4. "And a lattice is narrower still"
over three curves; retitle to the point the figure actually makes.

**D-24 · MINOR · put the figure's key above or inside the drawing** where the figcaption *is* the key —
006, 011, 017, 020, 022. P3/reading order: the caption sits in small gray script directly above a black body
line, and the black line wins the eye, so the key is read second or not at all. Slide 011's caption is the
entire colour legend.

---

## E. `figures/make_animations.py` — mine, already understood

**E-1 · MAJOR · accent-2 carries two meanings on `ba-growth.gif`'s frame.** F1. In the drawing it marks the
node that just arrived; at the right edge, in the same red, sits the counter "largest / 15 edges" — so the
eye reads *that little node has 15 edges*, and the real hub sits unmarked in plain accent. Draw the counter
in annotation gray like the "24 nodes / 45 edges" one, and put an accent-3 ring on the current
maximum-degree node so the counter has a referent. (accent-3 is legal as a ring; it is only banned as text
and as a thin stroke.)
