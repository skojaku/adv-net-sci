# Quiz 3 — Degree bias and robustness

An in-class quiz, 20 minutes, 10 points. One printed page of questions;
students write by hand and hand in one photo per question. Covers the M03
(robustness) and M04 (node degree) modules — the two halves of one idea, so the
sheet carries a shared **Notation** box and both questions live off it.

This one is a **derivation quiz**: no network is drawn and nothing is counted
by hand. Both questions turn on the same quantity, κ = ⟨k²⟩/⟨k⟩ — the average
degree of the node at the end of a random edge. Question 1 calls it the average
friend's degree; Question 2 calls it degree heterogeneity.

1. **Your friends have more friends than you** (5 pts). Given
   `⟨k_f⟩ = (1/2M) Σ_i Σ_{j∈N(i)} k_j` as the definition: prove
   `⟨k⟩ ≤ ⟨k_f⟩` (3 pts), then state and prove the equality condition (2 pts).
   Answer: equality iff every node has the same degree — `G` is regular.
2. **How much can you delete before it falls apart?** (5 pts). In a
   configuration-model network under random node deletion: derive
   `f_c = 1 − 1/(κ−1)` (3 pts), then evaluate it for Poisson and for a power
   law with `2 < γ < 3` (2 pts). Answers: `f_c = 1 − 1/⟨k⟩` and `f_c → 1`.

**The sheet states the setting and asks for the result. It gives no route.**
What a student must produce, none of it printed: `⟨k_f⟩ = ⟨k²⟩/⟨k⟩` and the
variance form of the gap; `q(k) = k p(k)/⟨k⟩`; the branching factor `κ − 1`,
including why the incoming edge is subtracted; the Molloy–Reed criterion
`κ > 2`; the `(1−f)` thinning; and the Poisson second moment
`⟨k²⟩ = ⟨k⟩² + ⟨k⟩`. That last one is the module's standing trap — the lecture
note records `⟨k²⟩ = ⟨k⟩²` as the slip students keep making, and it is the
*regular*-graph case, which is exactly the network Question 1(b) identifies as
the one with no friendship paradox. The two questions fail together, and the
rubric says so.

What *is* given is the setting, because without it the questions are
ill-posed: the definition of `⟨k_f⟩`, the configuration model, local
tree-likeness (they are told to assume it), and what a giant component is.

The 20 minutes (Quiz 1 and 2 were 15) buys the two derivations.

The sheet carries the questions only — no boxes and no ruled lines. Students
put each question's answer on its own page, then upload one photo per
question.

## Files

| File | What it is |
|---|---|
| `quiz03.tex` / `quiz03.pdf` | The sheet handed out. One page. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. **Do not hand out.** |
| `quizkit.tex` | Shared preamble: fonts, the submission link, layout macros. |
| `quiz03-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz03`. |
| `build_form.py` | Builds or re-syncs the Google Form through the `gws` CLI. |

`quiz03.tex` is plain `quizkit` at 12pt, like Quiz 1 and 2. `solutions.tex`
sets 11pt and tighter margins — it is an instructor document and runs long.

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz03.tex
xelatex -interaction=nonstopmode quiz03.tex
xelatex -interaction=nonstopmode solutions.tex
```

The marking rubric the grader actually reads is **not here** — it is
`adv-net-sci-ops/grading/quiz/rubrics/M04-2026-09-22-DegreeRobustness/`
(`session.json`, `q1.md`, `q2.md`). `solutions.pdf` is the human-readable copy
of the same answers; keep the two in step. Both mark the *route*, not the final
formula: `f_c = 1 − 1/(κ−1)` is in the lecture note and can be recalled, so a
bare correct answer with no working scores half a point out of three.

## The plumbing

Everything but the printing and Brightspace is done, on 2026-09-22. Each line
is the same step the `quiz02` README documents in full.

- [x] **The Google Form** — `build_form.py --create`, 2026-09-22. Description
      and `VERIFIED` email collection set; see below.
- [x] **The two upload questions**, added by hand in the Forms editor. The API
      still refuses (`Creation of file_upload question not supported`, checked
      again 2026-09-22 against this very form).
- [x] **The file-responses folder** moved out of Drive root into
      `SSIE 641 Advanced Topics in Network Science/Submission/`, beside
      quiz01's. Forms drops it in the root and nothing moves it back.
- [x] **The rubric is armed** — `session.json` in the ops repo, and
      `grader.run check` reads the form (0 responses, as it should be).
- [x] **The two short links** on the droplet, beside the `quiz02` pair.
      Validated and reloaded; both answer 302.
- [x] **`quiz03.pdf` on Drive**, in the course folder, read-only to the
      `binghamton.edu` domain, link-only. `go.skojaku.com/quiz03` points at it.
- [ ] **Print the sheet.** The last one.
- [x] **Brightspace**, 2026-09-22. Quiz `m04-0922` (id 92607) feeding grade
      item `m04-0922` (id 657786), 10 points, category Quiz, unlimited
      attempts, no time limit, open 09-22 09:40 to 10-04 23:59. Both were made
      in the browser — the grade item because it has to be (`POST /grades/`
      answers 403), the quiz because it came with it — and both were renamed
      from `" m04-0922"`: the leading space would have broken the mark upload,
      which finds the item by the name in `session.json`. The
      `tools/brightspace/course/deadlines.yaml` row is in and
      `sync-deadlines` plans clean.
