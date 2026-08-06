# Slide review — m04-node-degree.md, slides 034–065 — round 3, reviewer B

**Verdict:** NEEDS WORK · **Slides:** 32 in range + 6 opened outside it ·
**Blockers: 0** · **Majors: 7** · **Minors: 12**

**The collision gate held.** No text box overlaps another text box, a rule or a curve anywhere in
the range — including the two figures the reviewer expected to fail. Every geometric defect below
is text over a **fill**, which the gate does not check, or a build state that drops a mark.

## The three asks

1. **The derivation build (028–031) is mechanically correct.** Pixel-diffed: each state adds
   exactly one line and everything above it is byte-identical. The algebra closes. ⟨k²⟩ is
   properly introduced. The hole is Var(k) — Major 1.
2. **The rewiring is consistent.** Measured N = 23,133, ⟨k⟩ = 8.086, kmax = 28, Var/⟨k⟩ = 0.987;
   the figure prints all four correctly and they agree with cond-mat on 039/050. The stale
   speaker note is gone. One defect: Minor 11.
3. **Five fixes moved their error rather than removing it** — see Majors 2, 3, 5, 7 and Minor 8.

## Majors

1. **030 — N1/N2 — the one non-obvious step has no words on the slide.** `Var` first appears here,
   the body block is empty, the gloss says "rewrite ⟨k²⟩" (what, not why), and 032 opens "A
   variance cannot be negative" as established. 029 explains ⟨k²⟩ in a body line; 030 should
   match it.
2. **046 — P2/F4 — the build stops accumulating.** 045 draws the nomination as a 4.4bp accent-2
   arrow; on 046 that edge is a plain 2.6bp black stroke. On the slide titled "vaccinate the
   friend, not the volunteer", the mark saying how the friend was reached has been deleted.
   `_acq_base(treated=("H",))` never re-draws the arrow. *(Mine — I kept the ring and lost the
   arrow.)*
3. **052 — F1/F4 — the head-of-distribution annotation is drawn on the tail highlight.** The
   accent-3 band spans x = 588–1157; "78% of 23,133 authors" spans 414–715, so **127px of it sits
   inside the band**, describing k ≤ 10 while lying over k = 43…142. **The collision gate checks
   text against text, rules and curves — not against fills.** Add fills to its blocker set.
4. **054 + 062 — N1 — the deck's two exponents for cond-mat are 0.85 apart where it teaches they
   must be exactly 1.0 apart.** 054 prints slope −2.44 on p(k) and 055 says "slope is −γ", so the
   room leaves with γ = 2.44. The same network's CCDF falls at **−2.29** over the same range;
   065's rule predicts −1.44. Apply the deck's own rule to the deck's own two pictures and you
   get γ = 2.44 and γ = 3.29 — and 067's note calls a gap of one "a different physics".
   `figs_tail.py`'s docstring still quotes −2.571, which the code no longer computes. **Fix:**
   print the fitted CCDF slope on 062 with a line saying it does not reconcile by the +1 rule
   because the tail is not a clean power law — Part Eight's argument arriving where its evidence
   is — or drop 054's printed slope.
5. **059 — F4 — "Nothing was recomputed" is contradicted by the figure above it.** `binned(w)`
   returns raw counts and never divides by w, so widening the bin multiplies every height: the
   leftmost point goes 2,373 at k = 1 to 16,588 at k = 4.5, a 0.85-decade rise on identical axes.
   **Fix:** plot per unit k, or rewrite the sentence.
6. **060 — F4 — the claim is asserted and the number that would show it is computed and thrown
   away.** The visible change across the three panels is that the scatter thins, which reads as
   "wider bins are cleaner" — the opposite of the point. The fitted slopes are **−2.25, −2.90,
   −3.80**; `_fig_binning_panel` computes all three, asserts they differ by 0.3, and prints none.
   Bin width alone moves cond-mat across the γ = 3 boundary.
7. **063 — F4/N1 — the comparison changes two things at once and says so out loud.** Panel titles
   read "CDF · linear y" and "CCDF · log y". A student can correctly answer "the left one is bad
   because you used the wrong axis" and the slide has no reply. R1 B-2 asked for the ruler change
   to be *stated*; it was stated rather than removed. **Fix:** draw the CDF on the same log y.

## Minors

1. **031** — the gloss names an operation on lines 1–3 and a result on line 4, so the step most
   needing a "how" has none. 2. **035→036** — the shared figure jumps 66px between question and
   answer, and its label changes colour. 3. **036** — caption restates the figure's printed values.
   4. **039** — still the only bar in the deck; 040's bars were rebuilt into discs and this was
   left. 5. **040** — Twitter's 98% is claimed in gray text and the caption but not drawn.
   6. **048** — one strategy under three names ("nominated" / "named" / "naming a friend"), and
   "targeted" alone carries no end value. 7. **050** — the title promises "the variance" and the
   figure prints Var/⟨k⟩ = 14.0; Var(k) is 112.9. 8. **056 + 058** — the same scatter, same window,
   same count, two slides apart, so the three-state build opens on a beat that reveals nothing.
   9. **061** — the figcaption is the stale layer ("count everybody above the line"); the caliper
   still sits in the gutter rather than against the two dots it measures; "1 edge" is the deck's
   only use of that word for what it calls "an end" elsewhere. 10. **065** — the figure says the
   slope "goes from −γ to 1 − γ" and the speaker note says the exponent is "one smaller"; opposite,
   on the slide about the most common error in this material. `fig_slope_derivation`'s only
   assertion compares a value with itself. 11. **073** — the headline says "largest degree 28" and
   the drawn CCDF's rightmost point is k = 21, because `ccdf()` evaluates only at observed degrees.
   12. **039, 050, 052, 058, 059, 060** — figcaptions restating numbers the drawing prints; 052 says
   the same sentence twice ~120px apart. The fix for this class was applied by slide list in round
   2 and never run over Parts Four and Five.

## Clean — do not re-run

Collision gate (no overlaps in range). Arithmetic on 034, 036, 039, 040, 042, 050, 052, 058–060,
061, 066, 067 — all correct against the data. N4 on 038, 041, 043, 047, 051, 057, 064, each with a
visible beat. F2 on 035, 036, 042, 044–046. Discs 40px (28px on 061, now full width). Palette clean,
accent-3 only as a fill. L1–L4 clean; 048 fragmented. L6 on eleven slides. Landed since R2:
`fb-twitter` as discs, `sampling-bias` at 28px with both fractions, `immunization-curves`' y title
and log mark, `slope-worksheet`'s "a different network", `slope-answer`'s fully gray strike,
`ccdf-def` full width, the binning build split with ticks on all three.
