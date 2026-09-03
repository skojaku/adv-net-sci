# Quiz 2 — Small-world networks

An in-class quiz, 15 minutes, 10 points. One printed page of questions;
students write by hand and hand in one photo per question. Held **2026-09-03**,
covering the M02 (small-world) module.

1. **Measure this network** (6 pts). A 6-node network — A is a hub joined to
   all five others, plus the two extra edges B–F and C–E. Compute the *global*
   clustering coefficient (3 pts) and the average path length (3 pts).
   Answers: `C = 3/7 ≈ 0.43` and `⟨ℓ⟩ = 23/15 ≈ 1.53`.
2. **A tempting index** (4 pts). Define small-worldness as `S = C / ⟨ℓ⟩` and
   ask what is wrong with it — **with a concrete case** (2 pts), then repair it
   and say why the repair works (2 pts). The defect is that `S` has no baseline
   and that its two halves do not scale together: `C ∈ [0,1]` while `⟨ℓ⟩` grows
   with `n`, so `S` drifts with size, is maximised by the complete graph, and
   cannot compare two networks at all. The repair is
   `σ = (C/C_rand)/(⟨ℓ⟩/⟨ℓ⟩_rand)` against a same-`n`, same-degree
   randomization, and it works because the size dependence cancels.

   Both halves are graded on two things each, and in both the second thing is
   the *reasoning*: a case with no stated defect, or a correct `σ` with no
   explanation, is half marks.

The formula for the global clustering coefficient is **printed on the sheet**.
Without it the likely answer is the average *local* coefficient, which for this
network is `0.7` — a different number, and the rubric treats it as such.

The sheet carries the questions only — no boxes and no ruled lines. Students
put each question's answer on its own page, then upload one photo per
question.

## Files

| File | What it is |
|---|---|
| `quiz02.tex` / `quiz02.pdf` | The sheet handed out. One page. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. **Do not hand out.** |
| `quizkit.tex` | Shared preamble: fonts, the submission link, layout macros. |
| `quiz02-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz02`. |
| `build_form.py` | Builds or re-syncs the Google Form through the `gws` CLI. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz02.tex
xelatex -interaction=nonstopmode quiz02.tex
xelatex -interaction=nonstopmode solutions.tex
```

The marking rubric the grader actually reads is **not here** — it is
`adv-net-sci-ops/grading/quiz/rubrics/M02-2026-09-03-SmallWorld/`
(`session.json`, `q1.md`, `q2.md`). `solutions.pdf` is the human-readable copy
of the same answers; keep the two in step.

## Two short links

The QR square and the printed address are the course's own short links, not
Google's. Paper outlives any one form or file, so swapping either is a line on
the droplet rather than a reprint.

| Link | Goes to |
|---|---|
| `go.skojaku.com/quiz02` | the question PDF on Drive |
| `go.skojaku.com/ans-quiz02` | the Google Form, where the photos go |

Both are live as of 2026-09-03. They are `handle` blocks in the
`go.skojaku.com` site of `/etc/caddy/Caddyfile` on `ssh digitalocean`, beside
the `quiz01` pair. After editing, run
`caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile`, then
`systemctl reload caddy`.

If the printed link ever changes, rebuild the square and the PDF:

```sh
uvx --from segno segno --output=quiz02-form-qr.png --scale=20 --border=1 \
    --error=m "https://go.skojaku.com/ans-quiz02"
```

and update `\formlink` and `\formshort` in `quizkit.tex`.

## The question PDF on Drive

`quiz02.pdf` is uploaded to the Drive course folder and shared **read-only with
the `binghamton.edu` domain** — link-only, not searchable. Students are signed
in to that account anyway, because the form demands it.

- File id: `18BJ17P8Pgq6cUAeoekuZXUY3k5F8jqLc`
- <https://drive.google.com/file/d/18BJ17P8Pgq6cUAeoekuZXUY3k5F8jqLc/view>

Re-upload after any edit to the sheet, or the link serves a stale quiz:

```sh
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
gws drive files update --params '{"fileId": "18BJ17P8Pgq6cUAeoekuZXUY3k5F8jqLc"}' \
    --upload quiz02.pdf --upload-content-type application/pdf
```

## The Google Form

- **Students:** <https://go.skojaku.com/ans-quiz02> →
  <https://docs.google.com/forms/d/e/1FAIpQLSd0UZm_8Kk5kLCcUaJuQYu6YKnraycDTSsnXEvnqhTzCRdVTA/viewform>
- **Editing and responses:** <https://docs.google.com/forms/d/106JO7K2xBvgDFcr7FeO0vaX8i-VhcHAiU_VgYv8S75I/edit>
- Form id: `106JO7K2xBvgDFcr7FeO0vaX8i-VhcHAiU_VgYv8S75I`
- Owned by the Binghamton account (`~/.config/gws-binghamton`).

The form is a **drop box, not a copy of the quiz**. It links to the PDF and
takes one photo per question. Nothing in it has to stay in step with the sheet,
and there is no typing for the student to do.

Email collection is `VERIFIED`, so respondents sign in with their
`@binghamton.edu` account — which is what maps an uploaded photo back to a
student.

`python3 build_form.py --sync` rewrites the live form from the script. It
deletes every item first, so run it only before responses arrive.

### The upload questions are added by hand

The Forms API refuses to create file-upload questions —
`Creation of file_upload question not supported`, checked again on 2026-09-03
against this form. So the two questions that matter are made in the Forms
editor:

| Title | Settings |
|---|---|
| `Question 1` | File upload · images · 1 file · 10 MB · required |
| `Question 2` | File upload · images · 1 file · 10 MB · required |

One box per quiz question is what lets you grade a question across the whole
class in one pass: `gforms_download.py` reads the number out of the title and
names the files `q1-…` and `q2-…`. Keep the titles numbered.

`--sync` cannot put these back, so it refuses while they exist. Pass `--force`
if you really mean to wipe the form, then re-add them in the editor.

## Where the photos go

The course convention lives in `adv-net-sci-ops/tools/quiz-photos/README.md`.
Uploads land in the form owner's Drive, and `gforms_download.py` files them
under a per-session folder in the Drive folder `adv-net-sci-ops`
(`1m4ZTV0Lgf7LYXU8mn-l3DHZV96hKU-El`), one subfolder per student email.

This quiz's session folder already exists, beside the M01 one and beside both
question PDFs:

```
adv-net-sci-ops/M02-2026-09-03-SmallWorld/
  student@binghamton.edu/
    q1-IMG_1234.jpg
    q2-IMG_1235.jpg
```

Folder id `1X_4vDI22hVSXFQe2_3fK5vPgHFgnrnYG`.

To pull the photos down after class:

```sh
python3 ~/Documents/teaching/adv-net-sci-ops/tools/quiz-photos/gforms_download.py \
    --form 106JO7K2xBvgDFcr7FeO0vaX8i-VhcHAiU_VgYv8S75I \
    --session M02-2026-09-03-SmallWorld
```

Or just let the nightly grader do it —
`grading/quiz/.venv/bin/python -m grader.run check --grade` downloads what is
missing and grades it, reading the form id out of `session.json`.

## Still to do before class

- [ ] Add the two file-upload questions in the Forms editor (above). Until
      this is done, `grader.run check` stops with
      `form … has no file-upload question titled ['Question 1', 'Question 2']`.
- [x] The `quiz02` and `ans-quiz02` handles are on the droplet and answer 302.
- [ ] Print the sheet.
- [ ] In Brightspace: a grade item named **`m02-0903`**, 10 points
      (*Grades → Manage Grades → New*), and a quiz object named **`Q2`** for
      the deadline row in `tools/brightspace/course/deadlines.yaml`.
