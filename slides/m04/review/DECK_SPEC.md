# m04 "Count Your Friends" — deck spec

Slide-by-slide plan for `m04-node-degree.md`, expanded from `plan.md`.
Sessions 09/16 (Parts 1–4) and 09/18 (Parts 5–8). **90 slides.**

Every number below printed out of `figures/verify_numbers.py` first. Nothing here was
typed from memory, and the generator imports the same functions rather than repeating a
value — m01 shipped two arithmetic errors *through* a spec, which is what this rule is for.

---

## Non-negotiables (restated from SLIDE_RUBRIC.md — check each slide against these)

- **One point per slide** (P1). Two definitions on one slide is a Blocker.
- **Fragments use `*`, never `-`.** `-` does not animate in Marp.
- **A question slide carries no answer anywhere — including the gray `note`.** The answer
  goes on the *next* slide. This has leaked twice in earlier modules.
- **No tables** (L2), **no code** (L3), **at most one column of text** (L1). `cols` is
  text + figure only.
- **No paragraph below a fragmented list** (L5) — the room reads it before the build runs.
- **Every concept slide has a figure** (N2). Question slides, dividers and the roadmap are
  the only exemptions.
- **Bold marks key terms only.** `strong` renders accent-2 red; stress-bolding kills it.
- **Shallow slides take `<!-- _class: mid -->`** (L6) — most question slides.
- **KaTeX does not run inside `<figcaption>` or `<div class="steps-list">`.** Write the
  symbol as a word there ("k-squared over k"), never `$…$`.
- Max 4 bullets, one list per slide (L4).
- Figures: author at final size (1 bp = 1 slide px), in-figure x-height ≥ 15.5 px on the
  slide, node discs 26–52 px, palette tokens only, **no green, no bar charts**, zero edge
  crossings wherever the graph is planar.

## Containers (read out of `network-science.css`, and confirmed in the rendered HTML)

Marp wraps every figure in a `<p>`, and `section p { max-width: 1080px }` binds before the
1120 px content area — confirmed by counting `<div class="fig…"><p>` in m03's export: 72 of
72. So:

| container | width cap | height cap |
|---|---|---|
| full width | **1080 px** | 380 px (`.fig`), 320 px (`.fig tight`), 190 px (`.fig stack`) |
| `cols` column | **537 px** | same |

Figures are authored at exactly the width cap, so the deck's scale factor is 1.0 and an
in-figure 36 pt label lands at 36 px type / 15.5 px x-height on the slide.
*(m03 authored full-width figures at 1100 bp for a 1120 px container and therefore shipped
them 1.8% under intention; m04 does not repeat that.)*

---

## Verified numbers

### Feld (1991) Figure 1 — the eight girls

Edges (10): Betty–Sue, Sue–Alice, Sue–Pam, Sue–Dale, Alice–Jane, Alice–Pam, Alice–Dale,
Jane–Dale, Pam–Carol, Carol–Tina.

Degrees: Betty 1, Sue 4, Alice 4, Jane 2, Pam 3, Dale 3, Carol 2, Tina 1.
Friends' degree totals: 4, 11, 12, 7, 10, 10, 4, 2.
Friend-means: 4.00, 2.75, 3.00, 3.50, 3.33, 3.33, 2.00, 2.00.

- N = 8, M = 10, Σk = 20 = 2M, Σk² = 60
- ⟨k⟩ = 2.5 · ⟨k²⟩ = 7.5 · Var(k) = 1.25
- ⟨k²⟩/⟨k⟩ = 60/20 = **3.0** · gap = Var/⟨k⟩ = **0.5** · 2.5 + 0.5 = 3.0 ✓
- below 5 (Betty, Jane, Pam, Dale, Tina) / above 2 (Sue, Alice) / same 1 (Carol)
- mean over *people* of each person's friend-mean = **2.9896** (Feld prints 2.99)
- p(k) = 1/4 for each of k = 1, 2, 3, 4 — flat, which is why Var is small and the gap modest
- **planar** — the deck draws it with zero crossings (Feld's own figure crosses twice)
- Pam's friends are Carol, Sue and **Alice**. Several secondary sources say "Carol, Sue,
  Dale"; that is wrong and breaks the degree sequence. Asserted in the generator.

### Marketville, 146 girls (Feld 1991) — verified against the JSTOR scan

> "Of the 146 girls who have any mutual friends, 80 have fewer friends than the mean
> among their friends while 41 have more; 25 have the same as the mean among their
> friends."

**Wording correction the deck must respect:** 146 is the girls *with at least one mutual
friend*, not every girl in the school. The slide says "146 girls with a friend in the
survey", never "the whole school".

Feld's Figure 3 sub-captions print the two means: "(a) The mean is 2.7." "(b) The mean is
3.4". The degree counts behind them were read off Figure 3 at 400 dpi — 1→29, 2→53, 3→26,
4→20, 5→14, 6→3, 7→1 — and are trusted because they close on their own: they sum to exactly
146, Σk = 388 (194 mutual pairs), Σk² = 1302, and the implied means round to the 2.7 and
3.4 Feld printed. *(Provenance matters: these are reconstructed from the figure, not
printed in the paper. Do not quote them as Feld's own numbers.)*

The theorem then checks on Feld's whole dataset, not just the eight girls:

- ⟨k⟩ = 388/146 = **2.6575** · ⟨k²⟩ = 1302/146 = 8.9178 · ⟨k²⟩/⟨k⟩ = **3.3557**
- Var = 1.8553 · gap = 0.6981 · **2.6575 + 0.6981 = 3.3557** ✓
- 80/146 = **54.8%** are below

Feld states the identity himself on p. 1470: "mean number of friends of friends =
(Σx²)/(Σx) = mean(x) + variance(x)/mean(x)".

Two more facts from the paper the deck uses:

- "The names are fictitious." — say so on the slide that introduces the eight girls.
- "In *The Adolescent Society*, Coleman (1961) collected data on friendships among the
  students in **12 high schools**." Several secondary sources say nine or ten; Feld says
  twelve, and the deck follows Feld.
- Not confirmed: that "Marketville" is Coleman's own pseudonym. Feld only puts it in
  quotes. The deck says **"the school Feld called Marketville"**.
- Feld's Table 1 gives Pam's friends' degrees summing to 10 (mean 3.3), which only works
  for {Carol 2, Sue 4, Alice 4}. The widely-copied "Carol, Sue, Dale" gives 9 and
  contradicts Feld's own table.

### Facebook — Ugander, Karrer, Backstrom & Marlow 2011, arXiv:1111.4503

Every figure read out of the PDF, quoted in `verify_numbers.py`:

- 721 million active users, May 2011; 68.7 billion friendship edges; mean ≈ 190 friends
- median friend count **99**; ⟨k²⟩/⟨k⟩ = **635**
- **92.7%** have fewer friends than the *average* friend count of their friends
- **83.6%** have fewer friends than the *median* friend count of their friends
- degree assortativity r = **+0.226**
- and, in the paper's own words, "there is substantial curvature exhibited in the
  distribution on a log-log scale" — Part 8 rests on this sentence

### Twitter — Hodas, Kooti & Lerman 2013, arXiv:1304.3480

5.8 M users, 193.9 M links; the paradox holds for **>98%** of users; and, being directed,
"everyone you follow or who follows you has more friends and followers than you".

### The deck's real network — arXiv cond-mat coauthorship (SNAP `ca-CondMat`)

**Deviation from plan.md, on a measurement.** The plan named ca-HepTh or ca-AstroPh. Part 5
claims the tail is "roughly a straight line", so the network has to actually be straight:
over 10 ≤ k ≤ 200 the CCDF fits with R² = **0.976** for cond-mat, against 0.920 for hep-th
(whose tail stops at k = 65) and 0.931 for astro-ph (a visible shoulder). Same arXiv
coauthorship family; the honest choice.

- N = 23 133 · M = 93 439 · ⟨k⟩ = 8.08 · max k = 279 · median k = 5
- ⟨k²⟩ = 178.19 · Var = 112.93 · ⟨k²⟩/⟨k⟩ = **22.06** · gap = **13.98**
- **82.8%** of authors have coauthors who average more coauthors than they do
- 78.3% of authors have k ≤ 10; 92.3% have k ≤ 20; 28 authors (0.12%) have k ≥ 100
- CCDF slope over 10–200 = **−2.571**, so γ = **3.57** read that way; R² = 0.976
- top 1% (231 authors) hold 9.4% of all edge ends; top 10% hold 39.1%
- degree assortativity r = **+0.134** (assortative — the Part 7 claim)

### Comparison networks

| network | N | M | ⟨k⟩ | max k | CCDF slope | r |
|---|---|---|---|---|---|---|
| Internet AS (SNAP `as20000102`) | 6 474 | 12 572 | 3.88 | 1 458 | −1.196 (γ 2.20) | **−0.182** |
| yeast protein interactions (Network Repository `bio-yeast`) | 1 458 | 1 948 | 2.67 | 56 | −2.261 (γ 3.26) | **−0.210** |

*(spec table only — the deck draws these, it never prints a table.)*
Internet AS: top 1% (65 nodes) hold **33.8%** of all edge ends; top 5% hold 50.4%.

### Models

- BA(n = 20 000, m = 2): ⟨k⟩ = 4.000, max k = **315**; theory γ = 3
- uniform-attachment growth, same n and m: ⟨k⟩ = 4.000, max k = **29** — same growth,
  no preference, and the tail is gone. This pair is the Part 6 quiz.
- ER ⟨k⟩ = 4: Var = 3.98 ≈ ⟨k⟩ (Poisson), max k = 15
- ring lattice k = 4: every degree 4, Var = 0

### Worksheet graphs (Part 3)

- star, 4 nodes: ⟨k⟩ = 1.5, ⟨k²⟩ = 3, Var = 0.75, gap = **0.5**, friend-mean = 2
- ring, 6 nodes: ⟨k⟩ = 2, Var = 0, gap = **0**, friend-mean = 2
- K₅: ⟨k⟩ = 4, Var = 0, gap = 0

### Immunization (Part 4) — on the Internet AS graph

Chosen over cond-mat because the separation is the point and cond-mat barely shows it
(0.69 vs 0.58 at f = 0.20). Nothing in Part 4 needs the word "scale-free", so no forward
reference is created.

| f immunised | random | acquaintance | degree-targeted (needs the whole map) |
|---|---|---|---|
| 0.02 | 0.947 | 0.541 | 0.271 |
| 0.05 | 0.942 | 0.242 | 0.004 |
| 0.10 | **0.877** | **0.024** | 0.002 |
| 0.20 | 0.723 | 0.001 | 0.001 |

At f = 0.10 random immunisation leaves 88% of the network connected and acquaintance
immunisation leaves **2.4%** — almost the fully-informed result, from nothing but "name a
friend."

### The straight line that is not a power law (Part 8)

**Deviation from plan.md, on a measurement.** The plan asked for a mixture of Poissons.
Measured, it does not draw a line: log-uniform mixing means give CCDF ≈ log(k_max/k),
R² = 0.92, and a handful of discrete components is worse (R² = 0.59–0.87) — visibly bent,
so the slide would have no punch. A **log-normal(μ = 0.6, σ = 2.2)** reaches R² = **0.986**
over 3 ≤ k ≤ 500 with apparent slope −0.99 (apparent γ ≈ 1.99), and is not a power law at
all. It is also the alternative the scale-free literature actually tests (Broido &
Clauset 2019).

---

## Slides

Notation: **[Q]** question slide (no answer anywhere, `mid` class) · **[A]** its answer ·
**[M]** milestone activity · figure names are the PNG the generator emits.

### Front (3)

| # | title | one point | figure |
|---|---|---|---|
| 1 | **Count Your Friends** | title; subtitle *then count theirs* | — (`lead`) |
| 2 | Why do your friends have more friends than you do? **[Q]** | the module's question, unanswered | — (`mid`, formula panel) |
| 3 | Where we are going | four acts, one line each | — (`steps-list`; **no math symbols**) |

Roadmap wording, symbol-free: *Eight girls in 1961* · *Counting ends* · *Reading the
tail* · *Believing the line*.

---

### Part 1 — Marketville, 1961 (divider + 9)

| # | title | one point | figure |
|---|---|---|---|
| 4 | Part 1 · Marketville, 1961 | divider | — |
| 5 | 1961: a sociologist counts friendships | Coleman surveyed 12 American high schools; thirty years later Feld reopened one of them | `timeline-1961.png` |
| 6 | Eight girls | the working network, names only — no numbers yet (*the names are fictitious*, in Feld's words) | `feld-names.png` |
| 7 | How many friends each? **[Q]** | ask the room to count | `feld-names.png` (same file, so the count is possible) |
| 8 | Two and a half **[A]** | ⟨k⟩ = 2.5 | `feld-degrees.png` |
| 9 | Now count *theirs* **[Q]** | the paradox question, posed with no hint | — (`mid`) |
| 10 | Your turn **[M]** | each student takes one girl and averages her friends' counts | `feld-worksheet.png` |
| 11 | What the room found **[A]** | five below, two above, one exactly equal | `feld-friendmeans.png` |
| 12 | Feld's number | girls average 2.5 friends; their friends average 3.0 — **not an insult** | `feld-two-numbers.png` |
| 13 | Were the eight a fluke? | the same school, every girl with a friend in the survey — 146 of them: 80 below, 41 above, 25 equal | `marketville-146.png` |

Slide 7 reuses `feld-names.png` deliberately — same file, same explanation, which is the
only case reuse is safe. Slide 10's figure shows the network with degrees printed **and a
blank line per girl**; it must not print any friend-mean.

`marketville-146.png`: 146 discs in a block, coloured below / above / equal, with the two
means (2.7 and 3.4) as annotated marks. **Not a bar chart.**

---

### Part 2 — Counting ends (divider + 10)

| # | title | one point | figure |
|---|---|---|---|
| 14 | Part 2 · Counting ends | divider | — |
| 15 | Degree | the number of edges at a node — exposure for a person, shape for a network (**c01**) | `degree-def.png` |
| 16 | Add up all eight **[Q]** | what is Σk? | `feld-degrees.png` |
| 17 | Twenty **[A]** | Σk = 2M, because every edge has two ends (**c02**) | `sum-ends.png` |
| 18 | So the average is 2M/N | ⟨k⟩ = 20/8 = 2.5 falls straight out | `mean-degree.png` |
| 19 | Exactly three odd? **[Q][M]** | can a network have exactly three odd-degree nodes? | `odd-three-attempt.png` |
| 20 | No — and Euler knew **[A]** | odd degrees come in pairs (**c03**); this is why M01's condition said "zero or two" | `handshake.png` |
| 21 | From one node to all of them | p(k) = the fraction of nodes with degree exactly k (**c04**) | `pk-def.png` |
| 22 | The eight girls' p(k) | flat: a quarter of them at each of k = 1, 2, 3, 4 | `feld-pk.png` |
| 23 | Why should friends have more? **[Q]** | the mechanism question | — (`mid`) |
| 24 | Because hubs are on every list **[A]** | Sue and Alice appear on four friend lists, Betty and Tina on one (**c06**) | `rosters.png` |

`feld-pk.png`: a column of stacked discs per degree — the actual girls, not bars.
`rosters.png`: eight lists side by side, each name accent-2 where it repeats; a count
strip beneath. Builds one list at a time in the deck (four consecutive `*` fragments is
not enough — this is a figure build, so emit `rosters-1..4.png`? **No** — one file, and
the *slide* is the last step; the build lives in the roster columns being read aloud).

---

### Part 3 — The exact gap (divider + 11)

| # | title | one point | figure |
|---|---|---|---|
| 25 | Part 3 · The exact gap | divider | — |
| 26 | How much more? **[Q]** | intuition is not a number | — (`mid`) |
| 27 | Pick a friend at random | picking a friend = picking one end of one edge; 2M hands in the bag | `bag-of-hands.png` |
| 28 | A hub has more hands | q(k) = k·p(k)/⟨k⟩ — the same bias m03 used to follow an edge (**c06**) | `qk-formula.png` |
| 29 | Its average | ⟨k⟩_friend = Σ k·q(k) = ⟨k²⟩/⟨k⟩ | `derivation-1.png` |
| 30 | Put the variance in | ⟨k²⟩ = Var(k) + ⟨k⟩² | `derivation-2.png` |
| 31 | The theorem | ⟨k⟩_friend = ⟨k⟩ + Var(k)/⟨k⟩ (**c07**) | `derivation-3.png` |
| 32 | Variance is never negative | so it holds in **every** network, with equality only when all degrees are equal | `gap-nonneg.png` |
| 33 | Check it on the eight girls | Var = 1.25, gap = 0.5, 2.5 + 0.5 = 3.0 — the hand count said 60/20 | `feld-check.png` |
| 34 | Which average? | edge-random gives 3.0 (what the theorem claims); person-random gives 2.99 | `two-averages.png` |
| 35 | Your turn **[M]** | predict the gap for a star and a ring from Var/⟨k⟩, then count | `worksheet-star-ring.png` |
| 36 | The gap *is* the variance **[A]** | star 0.5, ring 0 — the closer | `worksheet-answer.png` |

Slide 31 carries a gray `note`: Feld writes the identity out himself on p. 1470, and it
closes on his full 146-girl data too — 2.6575 + 0.6981 = 3.3557.

Slides 29–31 are one figure in three states — same axes, same layout, one line added each
time, so the room sees a build and not three pictures.
Slide 34's distinction is the setup for slide 76 ("does it hold for *you*?"); the figure
must show the two sampling procedures, not just the two numbers.

---

### Part 4 — Using the bias (divider + 8)

| # | title | one point | figure |
|---|---|---|---|
| 37 | Part 4 · Using the bias | divider | — |
| 38 | Only about friendship? **[Q]** | — | — (`mid`) |
| 39 | Your coauthors have more coauthors **[A]** | 23 133 physicists: ⟨k⟩ = 8.1, friends' mean 22.1, and 82.8% of them are below it (**c08**) | `coauthor-gap.png` |
| 40 | Seven hundred million people | Facebook: 92.7% below their friends' mean, 83.6% below the median; Twitter >98% | `fb-twitter.png` |
| 41 | What does that do to your data? **[Q]** | if you sampled by following edges | — (`mid`) |
| 42 | Everything tilts **[A]** | edge-following over-samples hubs and under-samples the edge of the network (**c11**) | `sampling-bias.png` |
| 43 | Find the hubs without the map? **[Q]** | callback to m03's targeted attack, which needed the whole network | — (`mid`) |
| 44 | Name a friend **[A]** | acquaintance immunization: random person → name one friend → vaccinate the friend (**c09**) | `acquaintance.png` |
| 45 | Live demo **[M]** | `vaccination-game.html`; at 10% immunised, random leaves 88% connected, naming a friend leaves 2% (**c10**) — then the cliffhanger | `immunization-curves.png` |

Slide 45 closes day 1 with: *the gap is the variance. So how big is the variance in a real
network?* That is the bridge into Part 5.

---

### Part 5 — Reading the distribution (divider + 16) · day 2 starts here

No recap slide — the part divider restarts the room, same as m03.

| # | title | one point | figure |
|---|---|---|---|
| 46 | Part 5 · Reading the tail | divider | — |
| 47 | Here is that variance | cond-mat degrees on linear axes — everything piles into the first bins (**c13**) | `linear-axes.png` |
| 48 | What can you read off it? **[Q]** | — | `linear-axes.png` |
| 49 | Nothing — and here is why **[A]** | the tail runs to k = 279 and you cannot see it (**c12**) | `fat-tail-reveal.png` |
| 50 | Same data, log axes | change the axes, not the data (**c14**) | `loglog.png` |
| 51 | A line appears | roughly straight over two decades | `loglog-line.png` |
| 52 | A line means a power law | p(k) ~ k^−γ; γ says how fast hubs get rare (**c17**) | `powerlaw-def.png` |
| 53 | Change the bin width? **[Q]** | — | — (`mid`) |
| 54 | The tail changes shape **[A]** | three bin widths, three different tails — none of them wrong (**c15**) | `binning.png` |
| 55 | A quantity with no bins | CCDF(k) = P(k′ > k) — the share of nodes above k (**c16**) | `ccdf-def.png` |
| 56 | The same data, no choices | smooth, and every point is a real node | `ccdf-condmat.png` |
| 57 | Why not the CDF? | the CDF flattens the tail into a wall (**c27**) | `cdf-vs-ccdf.png` |
| 58 | Is that slope γ? **[Q]** | — | — (`mid`) |
| 59 | Integrate and see **[A]** | ∫ k^−γ gives k^−(γ−1), so the CCDF slope is 1 − γ (**c18**) | `slope-derivation.png` |
| 60 | Your turn **[M]** | a CCDF slope of −1.3. What is γ? | `slope-worksheet.png` |
| 61 | 2.3, not 1.3 **[A]** | off-by-one on the exponent is the classic error | `slope-answer.png` |
| 62 | Paper exercise **[M]** | *Data Visualization* — run it here | `exercise-card.png` |

Slides 47–52 are one build over one dataset: same colour, same data, only the axes and the
annotation change. Slide 51 draws the fitted line over the points; slide 52 names it.

---

### Part 6 — Where hubs come from (divider + 10)

| # | title | one point | figure |
|---|---|---|---|
| 63 | Part 6 · Where hubs come from | divider | — |
| 64 | Hubs | the few at the top of the tail, and how much they hold: 1% of Internet nodes carry 34% of all connections (**c22**) | `hubs-share.png` |
| 65 | Everywhere you look | science, the Internet, and a cell's proteins, all on one CCDF panel (**c25**) | `universality.png` |
| 66 | Does every network do this? **[Q]** | what about a random one? | — (`mid`) |
| 67 | Not a random one **[A]** | Poisson: bunched at the mean, hubs effectively absent (**c19**) | `poisson-ccdf.png` |
| 68 | Narrower still | a lattice gives every node the same degree (**c20**) | `three-ccdfs.png` |
| 69 | So where do real hubs come from? **[Q]** | — | — (`mid`) |
| 70 | Growth **[A]** | nodes keep arriving, each bringing m edges (**c21**, half 1) | `ba-growth.png` |
| 71 | And preference | attach with probability k_i/Σk_j — rich get richer; γ = 3 comes out | `ba-growth.gif` |
| 72 | Which one is which? **[Q][M]** | two networks, same size, same ⟨k⟩ = 4 — one preferential, one uniform | `quiz.png` |
| 73 | Preference is the whole difference **[A]** | max degree 315 against 29; neither ingredient works alone (M08 teaser) | `quiz-answer.png` |

`ba-growth.gif` must settle on the exact frame `quiz.png` uses for its preferential panel,
so the loop hands off to the still.

---

### Part 7 — Edge cases (divider + 9) · every one posed as a question

| # | title | one point | figure |
|---|---|---|---|
| 74 | Part 7 · Four awkward questions | divider | — |
| 75 | Does it hold for **you**? **[Q]** | — | — (`mid`) |
| 76 | "On average" is not "for you" **[A]** | five of eight below, two above, one equal; hubs get the reverse; Facebook's 92.7% (mean) against 83.6% (median) | `individual-vs-average.png` |
| 77 | Can you kill the paradox? **[Q][M]** | build a network with no gap — `friendship-paradox-game.html` | `vanishing-blank.png` |
| 78 | Only when everyone is equal **[A]** | Var(k) = 0: the ring, the complete graph, the lattice | `vanishing.png` |
| 79 | What about followers? **[Q]** | directed networks: following is not mutual | — (`mid`) |
| 80 | Both directions tilt **[A]** | in-degree and out-degree split the bias; the accounts you watch are more watched than you | `directed.png` |
| 81 | Same p(k), same network? **[Q]** | — | — (`mid`) |
| 82 | p(k) counts hubs; it does not say who they touch **[A]** | assortative / disassortative / neutral (**c23**) | `assortativity.png` |
| 83 | And it changes m03's answer | Facebook +0.226 and coauthors +0.134 hold a hub core; the Internet −0.182 and proteins −0.210 hang leaves off hubs | `assortativity-real.png` |

---

### Part 8 — A straight line is not a proof (divider + 6)

| # | title | one point | figure |
|---|---|---|---|
| 84 | Part 8 · Do you believe that line? | divider | — |
| 85 | Does the line prove it? **[Q][M]** | show of hands on the Part 5 figure | `loglog-line.png` |
| 86 | No — this one is not a power law **[A]** | a log-normal draws the same straight CCDF, R² = 0.99, and has no exponent at all (**c26**) | `lognormal-trap.png` |
| 87 | So it takes a test, not an eye | 1999 BA · 2011 Facebook reports "substantial curvature" · 2019 Broido & Clauset | `scale-free-debate.png` |
| 88 | The shape still decides everything | p(k) drives robustness (M03), distance (M02), spreading speed (**c24**) | `consequences.png` |
| 89 | Module 04 in one page | the four acts | `recap.png` |
| 90 | Coming up in Module 05 | assortativity started asking *who* connects to *whom*; next, the clumps — and how you know a clump is real | `m05-teaser.png` |

---

## Milestones (S5 — one per part)

| part | milestone | slide |
|---|---|---|
| 1 | Your turn: compute one girl's friend-mean; the room reproduces 5 vs 2 | 10 |
| 2 | Build a network with exactly three odd-degree nodes (nobody can) | 19 |
| 3 | Your turn: predict the star's and ring's gap from Var/⟨k⟩ | 35 |
| 4 | Live demo — `vaccination-game.html` | 45 |
| 5 | Your turn: slope −1.3 → γ; then the *Data Visualization* paper exercise | 60, 62 |
| 6 | Tell-them-apart quiz: preferential against uniform growth | 72 |
| 7 | `friendship-paradox-game.html` — build a network with no paradox | 77 |
| 8 | Show of hands: do you believe that line? | 85 |

Demo files live at `lecture-note/assets/vis/vaccination-game.html` and
`friendship-paradox-game.html`.

## Concept coverage — all 27

P1 c05 · P2 c01 c02 c03 c04 c06 · P3 c06 c07 · P4 c08 c09 c10 c11 ·
P5 c12 c13 c14 c15 c16 c17 c18 c27 · P6 c19 c20 c21 c22 c25 · P7 c23 · P8 c24 c26

## Deviations from plan.md (both measured, both recorded above)

1. **Real network is `ca-CondMat`**, not ca-HepTh / ca-AstroPh — Part 5's "roughly a
   straight line" has to be true, and only cond-mat's is (R² 0.976 vs 0.920 / 0.931).
2. **Part 8's counterexample is a log-normal**, not a mixture of Poissons — the mixture
   measures R² 0.59–0.92, i.e. visibly bent, so the slide would not land. The log-normal
   reaches 0.986 and is the alternative the literature actually tests. Slide 87 adds the
   stronger real-data version: the Facebook paper the deck already quotes says its own
   distribution shows "substantial curvature" on log-log axes.
3. **Immunization figure uses the Internet AS graph**, not the coauthorship network — on
   cond-mat the three strategies barely separate (0.69 / 0.58 at f = 0.20) and the slide's
   whole point is the separation. No forward reference is introduced.
