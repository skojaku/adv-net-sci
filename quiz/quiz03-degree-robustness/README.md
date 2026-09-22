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
- [ ] **Print the sheet.**
- [ ] **In Brightspace**, and neither can be done from here:
      a grade item named **`m04-0922`**, 10 points
      (*Grades → Manage Grades → New* — nothing in `bscli blocks` creates a
      bare grade item), and a quiz object named **`m04-0922`** (`quiz.create`
      makes the shell, but the bscli session was dead on 2026-09-22 and only a
      human at the GUI can refresh it). Then add the `m04-0922` row under
      `quizzes:` in `tools/brightspace/course/deadlines.yaml` with its start,
      end and due — `sync-deadlines` errors on a name Brightspace does not
      have, so the row comes after the object, not before. The session's
      `deadline_key` already points at that row.

## The question PDF on Drive

`quiz03.pdf` is in the Drive course folder and shared **read-only with the
`binghamton.edu` domain** — link-only, not searchable. Students are signed in
to that account anyway, because the form demands it.

- File id: `1CfepsY_wor23gQ_gr6MlyxXpmvPMSshW`
- <https://drive.google.com/file/d/1CfepsY_wor23gQ_gr6MlyxXpmvPMSshW/view>

Re-upload after any edit to the sheet, or the link serves a stale quiz:

```sh
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
gws drive files update --params '{"fileId": "1CfepsY_wor23gQ_gr6MlyxXpmvPMSshW"}' \
    --upload quiz03.pdf --upload-content-type application/pdf
```

## Two short links

The QR square and the printed address are the course's own short links, not
Google's. Paper outlives any one form or file, so swapping either is a line on
the droplet rather than a reprint.

| Link | Goes to |
|---|---|
| `go.skojaku.com/quiz03` | the question PDF on Drive |
| `go.skojaku.com/ans-quiz03` | the Google Form, where the photos go |

Both went live 2026-09-22 as `handle` blocks in the `go.skojaku.com` site of
`/etc/caddy/Caddyfile` on `ssh digitalocean`, beside the `quiz02` pair. The
file before that edit is `Caddyfile.bak-20260922-pre-quiz03` next to it.
After editing, run
`caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile`, then
`systemctl reload caddy`.

## The Google Form

- **Students:** <https://go.skojaku.com/ans-quiz03> →
  <https://docs.google.com/forms/d/e/1FAIpQLSf7TsLd9cfD5olSf483XhbkR5j-xbn4OuShiS8i3XhKvTXUdg/viewform>
- **Editing and responses:**
  <https://docs.google.com/forms/d/1ap27Cku9mpn06gwJrt84i7nRgFFs_WnB8O6puCfOero/edit>
- Form id: `1ap27Cku9mpn06gwJrt84i7nRgFFs_WnB8O6puCfOero`
- Owned by the Binghamton account (`~/.config/gws-binghamton`).

The form is a drop box, not a copy of the quiz. It links to the PDF and takes
one photo per question; nothing in it has to stay in step with the sheet, and
there is no typing for the student to do.

Email collection is `VERIFIED`, so respondents sign in with their
`@binghamton.edu` account — which is what maps an uploaded photo back to a
student.

`python3 build_form.py --sync` rewrites the live form from the script. It
deletes every item first, so run it only before responses arrive, and it
refuses while the hand-made upload questions exist unless you pass `--force`.

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

That session folder exists — `gforms_download.py mkdir`, 2026-09-22, folder id
`1nET4wsXMIXMJkXIL464yxeXYQmBHGp1Z`.

The form's own file-responses folder is a different thing and Google puts it in
the Drive root: `advnetsci-quiz03-degree-robustness (File responses)`, moved on
2026-09-22 into `SSIE 641 Advanced Topics in Network Science/Submission/` where
quiz01's sits. Quiz 2's is still in the root, if you are tidying.
