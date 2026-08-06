# Review of IMPROVEMENT_PLAN.md

Written 2026-08-06 against the plan as it stood that day, and checked against the review
records under `m0*/review/` (35 documents, 6,356 lines), the six copies of
`check_render.py`, and the shipped decks themselves.

**Verdict.** The diagnosis is sound and matches the record. The prescriptions do not
follow from it. Section A automates the defect classes that have already stopped
happening; Section B removes the only mechanism that has ever caught the ones that have
not; Section E leaves out the two rules the record says cost the most. And the largest
recurring failure in this pipeline is not in the plan at all.

Everything below is checkable from the repository. Where a claim rests on a count, the
command that produces it is given.

## The plan does not name the reason m03 inherited m02's inert gate

`check_render.py` is not a module. It is copied into each module directory and edited
there, and checks written in one module have been silently lost in the next:

    $ for m in m01 m02 m03 m04 m05 m06; do grep -oE '^def [a-z_]+' $m/check_render.py; done

| module | lines | functions | delta |
|---|---|---|---|
| m01 | 326 | 6 | — |
| m02 | 564 | 11 | `+figure_containers +caption_colours +figcaption_math +_flood_from_border +_generated` |
| m03 | 453 | 9 | **`−caption_colours −_flood_from_border −_generated`** `+em_dashes` |
| m04 | 530 | 9 | **`−em_dashes`** `+_flood_from_border` (restored) |
| m05 | 509 | 9 | — |
| m06 | 521 | 9 | — |

`caption_colours` was written for m02 and has never run since. `em_dashes` was written for
m03 and has never run since. `_flood_from_border` was written for m02, lost in m03, and
rebuilt in m04.

This is the mechanism behind the playbook's own entry that "Module 03 inherited the same
inert gate and it stayed inert for that whole build too." That was recorded as a fact
about m03's authors. It is a fact about the packaging: a gate that is copied cannot
inherit a fix, and nothing in the build reports what was dropped.

Section A adds **a second per-module file with fourteen new checks**. On the current
packaging those fourteen checks will decay across module boundaries exactly as the five
above did, and the decay will be twice as wide and no more visible.

**Do this before Section A, not after.** Move the gate to a shared
`docs/slide/new/gatelib/` imported by a thin per-module `check_render.py` that carries
only the module's constants. It is a smaller change than `check_deck.py` and it is
load-bearing for it. Recover `caption_colours` and `em_dashes` on the way through.

## The new source-level checks aim at defects that stopped happening

Blockers in each module's first review round:

    m01: 29 → m02: 16 → m03: 3 → m04: 6 → m05: 0 → m06: 0

The pipeline works. What survives into a mature module is narrow and specific:

- **m05 R1** — 0 Blockers, 5 Majors (F4 ×4, N1 ×1), 5 Minors (F3, L4, F1 ×3)
- **m06 R1** — 0 Blockers, 2 Majors (F2, S5), 3 Minors

Every Major in both is a judgment criterion — the exact set Section B moves to Tier 1 and
then reviews at 18% of current coverage. Of the fourteen new Tier 0 checks, the number
that would have fired on any m05 or m06 R1 finding is approximately zero.

The plan's "catches ~60% of historical findings" does not survive a count either. Tallying
criterion codes across the findings documents:

    $ grep -ohE '\b(P[1-3]|F[1-5]|L[1-6]|N[1-4]|S[1-5])\b' m0*/review/FIXES_*.md m0*/review/REVIEW*.md \
        | sed 's/[0-9]//' | sort | uniq -c

    242 F · 86 N · 72 P · 64 L · 39 S      (503 total)

Structurally checkable: F3 (55) plus the whole L family (64) is 119, under a quarter — and
F3 and container mismatch are **already** automated, so the net addition is smaller again.
The count also overstates itself: many L mentions are reviewers attesting cleanliness
("L1–L4 clean", `m04/review/REVIEW_R2_B.md:60`), not findings.

## The three L-violations that survived m01 are inside PNGs

This is the sharpest form of the point above, and it is worth checking before writing
A.4, A.6, A.5.

**No deck in this repository contains markdown table syntax:**

    $ grep -lE '^\|.*\|' m0*/m0*-*.md        # returns nothing

An L2 detector reading the markdown source would have returned zero on every deck ever
shipped. Meanwhile L2 was violated twice after m01, and both were figures:

- `m03/review/FIXES_R6.md:45` — slide 91 "Module 03 in one picture" **is** a table: four
  bordered cells, header over value, drawn into a PNG.
- `m04/review/FIXES_R1.md:35` — `rosters.png` (024), Blocker: "a header row of eight names
  over eight rows" — again, drawn.

L1 the same: `m04/review/FIXES_R2.md:130` — `exercise-card.png` (067) is "a picture of a
text column" beside a text column, so the slide is two columns of text. Nothing in the
markdown says so.

So the surviving violations of L1/L2/L3 live where a regex over the source cannot reach,
and the thing that has caught all three of them is a reviewer looking at the render. A.4
and A.6 as specified are checks that are green by construction; adding them and then
cutting the review that actually catches these is a net loss of coverage that will read as
a gain.

If these checks are wanted, they have to run **on the render** — a text-grid detector on
the figure, not a pipe-character grep on the deck.

## An automated answer-leak check already exists, and already certified a leak

Category 3 gives the root cause of question-slide leaks as "No automated leak check", and
A.1 and E.8 propose building one and codifying N5 as "a Blocker with automated check".

m04 had one. It scanned the figure for banned strings, and round 1 certified "no leak" on
its strength. The leak was that the "here is preferential attachment" slide drew, node for
node and ringed hub and all, the answer to a quiz two slides later — the room could answer
by matching pictures. A graphical leak walks through a textual assertion without touching
it.

Rebuilding that check is fine. Codifying it as *the* check for N5 repeats the failure the
playbook calls "a gate that cannot fire is worse than no gate", because a green textual
scan is then read as coverage of a graphical property. If it ships, its output must name
its own scope — "no banned string in figure text; figure content not examined" — so the
next round cannot mistake it for a verdict on the leak.

## "Only review slides that changed" is the assumption three regressions broke

The playbook's entry *After changing a figure, check every slide that uses it — and every
claim about it* records three regressions, and all three are unchanged slides broken by a
changed figure:

- a matrix added for one slide appeared on a slide 41 earlier, with unexplained colours,
  before the matrix was defined;
- making nodes uniform hid the ring-lattice edges, so no triangle was visible — on the
  slide whose claim is high clustering;
- fixing a badge overlap on an answer slide left the question slide correct and broke the
  answer.

Separately, m01's Blocker count ran 29 → 7 → 4 → 7 → **9** → 3 → 4 → **11**, and the
playbook attributes the bumps partly to reviewers getting more forensic: later rounds
found defects on slides earlier rounds had passed over. "Unchanged" and "reviewed" are
different claims, and Tier 1 as written treats them as one.

**The fix is small and keeps the saving.** Define the changed set on the *render*, not the
source: hash `review/slide.NNN.png` between rounds and review the slides whose hash moved.
A figure edit then propagates to every slide that uses it, a CSS edit propagates
deck-wide, and both happen without anyone maintaining a dependency map. This is cheaper
than a markdown diff and it is correct.

## Tokens are not the unit this pipeline pays in

The plan's own Category 1 prices its failures in rounds — "3+ full rounds", "1 round
each", "2 full builds". A round is the expensive object. Section B's 82% saving on PNG
reads is recovered by a single missed F1 or F4 that adds one round, and F1 and F4 are the
two largest families in the record (75 and 83) and the ones still live in m05 and m06.

The metrics to optimise are rounds-to-PASS and the severity class of R1 findings, both of
which the record already tracks and both of which are improving. Token cost per module is
worth measuring; it is not worth trading coverage for while the round count is still the
binding constraint.

Two smaller notes on C:

- **C.1 (inject guides into briefs)** targets 370K of a claimed 3.5M — the smallest line
  item gets the most structural change. It also introduces two failure modes: an excerpt
  goes stale when the guide is edited, and the lead's blind spot becomes the fixer's blind
  spot, because the lead chooses the excerpt. Splitting `FIGURE_GUIDE.md` (494 lines) so a
  fixer reads the 40 it needs gets most of the saving and keeps every agent reading the
  current file, which is the property that lets a non-Claude agent run this pipeline at
  all.
- **C.2 (cheap model for fixers)** is already the documented policy — `REVIEW_PLAYBOOK.md`,
  "Roles". Not a change.

C.4 — fix specs carrying exact old→new strings rather than intentions — is right, and is
the correct response to m04's fixer substituting a different fix and recording it only in
a docstring.

## What Section E is missing

Three rules, each with a cost already paid.

1. **Ban private helpers that bypass the shared drawing primitive** (grep gate). m04 had
   three gate blind spots that were one gap: the collision gate could not see a `fill_poly`,
   could not see a rectangle border, and the node gate could not see a gray or hollow disc.
   m06 paid it again — a ring drawn around a node was measured *as* the node. The playbook
   already states the corollary ("a private helper that bypasses the shared primitive is a
   hole in every gate built on it") after `figs_story.py` kept its own `rect()`. E.4's
   known-bad self-test does not catch this class: it only fires if the known-bad input
   happens to contain the primitive the gate is blind to.

2. **The ground-truth side of an assertion must be able to be wrong independently of the
   code under test.** Category 3 lists this as "Structural, needs rule" and then Section E
   proposes no rule. It is the most expensive content defect in the record — a colour-map
   dict written two lines above the assertion that checked it kept an inverted polarity
   alive through five rounds of review while reporting the polarity verified.

3. **Delete a figure's PNG before regenerating it.** Category 1 prescribes "Post-fix render
   + gate" for "fix reported landed but render contradicts". That does not address the
   mechanism m04 actually found: two `make_figures.py` processes writing the same directory,
   one from a session nobody had held. A process reports success for the write it performed;
   the bytes that survive can be the other one's. If the file is absent and the build is
   green, the file on disk is the file the code describes. The post-fix render cannot
   distinguish this case.

## What is right

- Categories 1–3 match an independent pass over the same history.
- **D is the most underrated section.** Eight mid-build crashes is real damage and
  per-gate-pass atomic commits is the correct primitive. One correction: "which agents were
  running" is not recoverable state. A round is fully described by `FIXES_Rn.md`, the gate's
  own exit status, and a commit — write those three and resumption is mechanical.
- E.5 (deck before figures, as a hard gate) is right and consistent with
  `DECK_BUILD_GUIDE.md:175`, which already says it and was violated anyway. A gate is the
  right response to a rule that exists and does not hold.
- C.4, above.

## Suggested order

1. **Share the gate** (§1). Nothing else in Section A is durable without it.
2. **Section E**, with the three additions above. Pure rules, no coverage traded.
3. **Section A, restricted** to checks that fire on the render or on properties that
   actually recur — L4, L5, L6, S5a, KaTeX-in-HTML, fragment syntax. Drop the
   markdown-source table/column/code detectors or move them onto the render.
4. **Section D.**
5. **Then measure.** On the next module's R1, record what fraction of findings Tier 0
   caught. Set Tier 1's scope from that number rather than from 60%.

Landing A, B and C together makes a quality regression unattributable. B is the one that
can lose coverage, and it is the one whose premise is least tested.
