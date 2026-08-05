# Tutor module review

Review a tutor-prototype module and iterate fixes until the review passes.

All substance lives in `tutor-prototype/TUTOR_REVIEW_RUBRIC.md` (repo root
relative) so any agent — Claude, pi, Cursor — runs the same review. This
command is only a dispatcher:

1. Resolve the module dir: the argument if given, else
   `tutor-prototype/m02-small-world`.
2. Read `tutor-prototype/TUTOR_REVIEW_RUBRIC.md` and follow its
   "How to run a review" and "Iteration protocol" sections exactly. Cursor
   has no subagents — use the rubric's "Runner portability" fallback: run
   the review in a fresh chat (or complete the entire findings report before
   fixing anything), fixes at the rubric's fix targets only, E2E gate before
   the final PASS.
3. Relay each round's findings to the user; finish with PASS/not-PASS,
   iterations used, and remaining Minors.
