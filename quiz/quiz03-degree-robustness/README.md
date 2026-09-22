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

`quiz03.tex` is plain `quizkit` at 12pt, like Quiz 1 and 2. `solutions.tex`
sets 11pt and tighter margins — it is an instructor document and runs long.

There is no `build_form.py` here yet. Copy `../quiz02-small-world/build_form.py`
and change the title, the description and the PDF link when the form is made.

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

## Still to do before this can be given and graded

The sheet and the key are finished. The plumbing is not — none of it exists yet
for `quiz03`, and each line below is the same step the `quiz02` README
documents in full.

- [ ] **The Google Form.** Copy `build_form.py` from `quiz02-small-world`, run
      `python3 build_form.py --sync`, then add the two file-upload questions
      **by hand** in the Forms editor (titled `Question 1` and `Question 2`;
      images, 1 file, 10 MB, required). The Forms API refuses to create
      file-upload questions, and `grader.run check` stops without them. Set
      email collection to `VERIFIED` — that is what maps a photo back to a
      student.
- [ ] **Arm the rubric.** The ops repo holds
      `rubrics/M04-2026-09-22-DegreeRobustness/session.json.pending`. Put the
      new form id in it and rename it to `session.json`. It is `.pending`
      precisely so that the nightly grader does not trip over a session with no
      form — see the note inside the file.
- [ ] **The two short links** on the droplet (`/etc/caddy/Caddyfile`,
      `go.skojaku.com` block), beside the `quiz02` pair:
      `go.skojaku.com/quiz03` → the question PDF on Drive, and
      `go.skojaku.com/ans-quiz03` → the Google Form. The QR square already
      encodes the second one. Then
      `caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile` and
      `systemctl reload caddy`.
- [ ] **Upload `quiz03.pdf`** to the Drive course folder, shared read-only with
      the `binghamton.edu` domain, and point `go.skojaku.com/quiz03` at it.
- [ ] **Print the sheet.**
- [ ] **In Brightspace:** a grade item named **`m04-0922`**, 10 points
      (*Grades → Manage Grades → New*), and a quiz object named **`Q3`** for
      the deadline row in `tools/brightspace/course/deadlines.yaml`.

## Where the photos go

Unchanged from Quiz 2 — the convention lives in
`adv-net-sci-ops/tools/quiz-photos/README.md`. Uploads land in the form owner's
Drive; `gforms_download.py` files them under a per-session folder in the Drive
folder `adv-net-sci-ops` (`1m4ZTV0Lgf7LYXU8mn-l3DHZV96hKU-El`), one subfolder
per student email:

```
adv-net-sci-ops/M04-2026-09-22-DegreeRobustness/
  student@binghamton.edu/
    q1-IMG_1234.jpg
    q2-IMG_1235.jpg
```

That session folder does not exist yet; `gforms_download.py` creates it, or the
nightly grader does it for you once `session.json` is armed.
