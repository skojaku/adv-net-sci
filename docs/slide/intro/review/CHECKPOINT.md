# Checkpoint

## Round 1

- Tier 0 gate: **pass** (`python3 -m gatelib review .` exit 0, 52 slides, 0 blockers/majors/minors;
  two 3px-ink warnings on slides 11 and 19 are arrowheads, not glyphs).
- Committed as `e17d8363`.
- Tier 1/2 LLM review dispatched to three sonnet agents over slides 1-18, 19-35, 36-52.

### Lead's own findings, to fold into FIXES_R1

- Slide 29 (philosophers): the montage's names are set in DejaVu Sans while the whole deck is
  serif. Redraw with DejaVu Serif.
- Slide 43 (grading): the figure labels the third block "Homework", but slide 41 is titled
  "Assignments". Same thing, two names.

### Known deviations from the archive deck (intended, not findings)

- Exam week and every final-project date are TBD placeholders.
- No bonus points.
- No AI-tutor slide, no LLM Dojo, no Network of the Week.
- The three scanned EngiNet slides were reset as text: at slide scale the scans are unreadable.
  Staff names come from the 2024 scan and should be confirmed before teaching.

## Infrastructure note

`~/.claude/skills/slide/gatelib/cli.py` invoked `marp` without `--no-stdin`, so every render
hung forever instead of finishing (25 minutes on the first run). Patched in place; the flag is
what `REVIEW_PLAYBOOK.md` already prescribes.
