---
name: tutor-review
description: >-
  Review a tutor-prototype module (notebook artifact, curriculum scripts,
  session logs, live E2E tutor behavior) against the tutor rubric, then drive
  a fix-and-re-review loop until the review passes. Use when asked to review,
  QA, or harden a tutor module. Argument - path to the module dir (default
  tutor-prototype/m02-small-world).
---

# Tutor module review

All substance lives in `tutor-prototype/TUTOR_REVIEW_RUBRIC.md` (repo root
relative) so any agent — Claude, pi, Cursor — can run the same review. This
skill is only a dispatcher:

1. Resolve the module dir: the argument if given, else
   `tutor-prototype/m02-small-world`.
2. Read `tutor-prototype/TUTOR_REVIEW_RUBRIC.md` and follow its
   "How to run a review" and "Iteration protocol" sections exactly:
   reviewer isolated from fixer (subagent here — see the rubric's Runner
   portability for other harnesses), fresh reviewer every round, fixes at
   the rubric's fix targets only, E2E gate before the final PASS.
3. **Loop until a round returns zero Blockers and zero Majors** — there is
   no iteration cap. Only the rubric's step-6 cases (same finding surviving
   two fixes, an instructor's content decision, contradictory rounds) pause
   the loop to ask the user.
4. Run the Part D E2E gate in a **subagent on Sonnet or Haiku**, never from
   the main loop — it is mostly blocking waits, and the transcript is not
   worth the caller's context. The tutor under test still runs the course
   model.
5. Relay each round's findings to the user; finish with PASS/not-PASS,
   rounds used, and remaining Minors.
