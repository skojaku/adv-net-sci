# Checkpoint

## Round 2 — clean

- Deck: 51 slides. Tier 0 gate: **pass** (`python3 -m gatelib review .`, exit 0).
  Three 3px-ink warnings (slides 11, 19, 43) are arrowheads and square outlines, not glyphs.
- Tier 1/2 LLM review by three sonnet agents over slides 1-18, 19-35, 36-51:
  **0 blockers, 0 majors, 0 minors** in every range.
- Round 1 had 3 blockers-equivalent (1 blocker, 9 majors, 4 minors); all fixed and re-verified.

### Round 1 findings and what was done

| Finding | Fix |
|---|---|
| N4a — the pollinator figcaption answered the slide's own question | caption reduced to what a line means |
| N2 — xz detection slide, Part 2 payoff, "knowing the parts" all had no visual | three new figures: `xz_3`, `same_shape`, `parts_vs_relations` |
| F1/F3/F4 — the three past-project screenshots (unexplained node sizes, yellow callouts, an EEG head diagram, unreadable labels) | the three slides became one slide naming the projects in words |
| S4 — the last movement was pure logistics | new "Before you go" question slide reaching back to the Part 2 activity |
| FACT — Mexico City to Madrid is ~9,090 km | "nine thousand kilometres" |
| FACT — Descartes gave a method, not a substance | "four attempts to reduce the world to something simpler" |
| P3/F3 — thin EngiNet title slide, phone number wrapping mid-digits | title set as `lead`; numbers on their own bullet |
| naming — grading figure said "Homework", the slide says "Assignments" | figure relabelled |
| L6 — pen-and-paper slide hung with slack below | `_class: mid` |

### Still open, for the instructor

- Exam week and every final-project date are **TBD** placeholders.
- The EngiNet contact slide's staff names come from the 2024 scan; confirm before teaching.
- The three EngiNet program slides were reset as text because the scans are unreadable at
  slide scale. The original scans are in `docs/slide/archive/intro/enginet-intro-slide/`.

## Infrastructure notes

- `~/.claude/skills/slide/gatelib/cli.py` invoked `marp` without `--no-stdin`, so every render
  hung instead of finishing (25 minutes on the first run). Patched in place; the flag is what
  `REVIEW_PLAYBOOK.md` already prescribes.
- Delete `review/slide.*.png` before re-rendering a deck that lost slides: a round-2 render left
  `slide.052.png` behind from the 52-slide version and the gate happily checked the stale file.
- The render gate reads a figure narrower than ~3000px as authored for a `cols` column, and its
  scale arithmetic assumes 4 px per bp. Figures here are authored accordingly.
