---
name: tutor-review
description: Review a tutor-prototype module (notebook artifact, curriculum scripts, session logs, live E2E tutor behavior) against the tutor rubric, then drive a fix-and-re-review loop until the review passes. Use when asked to review, QA, or harden a tutor module. Argument: path to the module dir (default: tutor-prototype/m02-small-world).
---

# Tutor module review

All substance lives in `tutor-prototype/TUTOR_REVIEW_RUBRIC.md` (repo root
relative) so any agent — not just Claude — can run the same review. This
skill is only a dispatcher for the rubric's "Iteration protocol":

1. Resolve the module dir: the argument if given, else
   `tutor-prototype/m02-small-world`.
2. Spawn a **read-only reviewer subagent** (fresh context, no findings from
   previous rounds) with this task: "Read
   `tutor-prototype/TUTOR_REVIEW_RUBRIC.md` and run its static pass
   (Parts S, C, P) on `<module dir>`. Render the notebook before judging
   figures. Report findings in the rubric's format, ordered by severity.
   Fix nothing." Relay its findings to the user each round.
3. Fix Blockers and Majors yourself at the rubric's fix targets (never touch
   `session_artifacts/`), then go back to step 2 with a fresh subagent.
4. When a static pass is clean, run the rubric's Part D E2E gate (a subagent
   may drive `tutor-prototype/review/` — it needs Bash). E2E findings → fix →
   back to step 2.
5. PASS = zero Blockers/Majors in both the static pass and the E2E gate.
   Report: PASS, iterations used, remaining Minors.
6. Guards (from the rubric): max 5 iterations; a finding that survives two
   fixes, or needs a content decision, goes to the user instead of another
   round. Never weaken a rubric item to make the review pass.
