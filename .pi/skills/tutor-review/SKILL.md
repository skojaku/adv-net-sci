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
   reviewer isolated from fixer (use the `pi-subagents` skill if available —
   see the rubric's Runner portability otherwise), fresh reviewer every
   round, fixes at the rubric's fix targets only, E2E gate before the final
   PASS.
3. Relay each round's findings to the user; finish with PASS/not-PASS,
   iterations used, and remaining Minors.
