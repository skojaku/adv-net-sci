# m05 — round 1 fixes

**Coverage warning.** Four subagent reviewers were launched over disjoint ranges and all
four died on a session limit before reporting. This round is therefore one careful pass
over the render by the lead, not four independent ones — weaker coverage than
`REVIEW_PLAYBOOK.md` intends. Slides nobody has looked at closely: 27, 29, 31–32, 34–36,
38, 40–41, 43, 45, 47, 50–52, 54–55, 57–58, 61–63, 65–68, 72–77, 81–86, 88, 91, 93–94,
96–99, 103–105. Next round must start there.

**Verdict this round:** NEEDS WORK · Blockers 0 · Majors 5 · Minors 5

Already landed before this spec was written (found on the render, fixed at the generator):

- `number_line()` placed every label at a fixed offset from its own tick, so two nearby
  marks printed through each other — "the rule of thumbthe real split" (85) and "the real
  split" over "Louvain" (90). Labels now walk outward row by row and take the first free
  row; no free row is a build failure.
- `three-partitions.png` and `best-vs-real.png` were byte-identical while slides 87 and 99
  explained them differently, and 87 claimed to show three answers while showing one.
- `applications` and `recap` alternated the deck's two club colours across groups that
  encode nothing (F1).
- "kept apart" sat on the y-axis tick reading 20 (79).
- Five shallow slides took `_class: mid` (L6).

## Majors

1. **Slide 008 "Your turn" — F4 / N3.** The three student guess-lines span only the middle
   of the drawing and read as stray dashes, not as three ways of cutting the club. And the
   prompt — "who put the middle four people on the left?" — names nobody the room can
   identify on the figure. *Fix:* draw all three lines from the top of the drawing to the
   bottom, in three visibly different dash patterns; change the prompt to one the picture
   can answer.

2. **Slide 021 "Relax it from the other side" — F4.** `kcore-peel.gif`'s first frame is the
   1-core, which is the whole club — pixel-for-pixel the slide-6 figure. Marp renders a
   GIF's first frame into the static export, so in the PDF this slide teaches nothing and
   repeats an earlier picture. *Fix:* lead the loop with the 4-core state (ten people),
   which is what the caption already claims.

3. **Slide 026 "They overlap, they multiply" — F4.** The slide's claim is four
   pattern-groups overlapping and leaving people out. The render shows one gold-ringed set
   of six and a blue/grey split; no student can see four groups or an overlap. *Fix:*
   redraw on a small graph where three named groups can be outlined and their overlap seen.

4. **Slide 046 "The bag holds 2m balls" — F4.** The figcaption says a member with three
   friends drops in three balls; nothing in the drawing connects any ball to any member.
   *Fix:* ring one member in the graph and her three balls in the bag.

5. **Slide 092 "How much does one grouping tell you about the other?" — N1, correctness.**
   The in-figure note reads "they agree about five of the six", which counts label identity
   across two partitions. That is exactly the mistake mutual information and ARI exist to
   avoid, and slide 095 corrects it two slides later. *Fix:* say what is true without
   comparing labels — "one person is in the wrong group".

## Minors

6. **Slide 010 — F3.** The seventy-eight internal friendships are drawn at 0.16 opacity and
   are barely present on the rendered slide. *Fix:* 0.28.
7. **Slide 016 — L4.** The figcaption wraps and orphans the word "short" on its own line.
   *Fix:* shorten it.
8. **Slide 053 — F1.** The winning dot on the Q-versus-K plot is accent-2, which is also
   the fill of the second group in the graph beside it. *Fix:* black dot, labelled "best".
9. **Slide 095 — F1.** "10/15" is drawn in accent, which means Mr. Hi's club on fourteen
   other figures. *Fix:* annotation grey.
10. **Slide 102 — F1.** The three answers are labelled in three different colours that
    encode nothing the slide states. *Fix:* one colour.
