# Quiz 4 — Your friends' degree, on log–log paper

An in-class quiz, 20 minutes, 10 points, calculator allowed. Two printed
pages: the table and the questions on page 1, four copies of the same
log–log graph paper on page 2. Students write on the sheet and hand in one
photo per page. Covers M04 (node degree).

The sheet gives the degree counts `n_k` of a 10,000-person network at ten
degrees, `k = 1, 2, 4, …, 512`. Nobody has any other degree, so every answer
is exact. The counts were built from `p(k) ~ k^-2.5`.

1. **The people** (5 pts). Compute the CCDF `P(K > k)` (2), plot it (1), read
   the slope and give γ (2). Answer: slope ≈ −1.5, so γ ≈ 2.5. Reporting
   γ = 1.5 (the slope read as −γ) is the expected slip.
2. **The friends** (5 pts). A friend is the second entry of a random
   (person, friend) pair. Compute the friend's CCDF (2), plot it on the same
   grid (1), read its slope and say why it differs (2). Answer: weight each row
   by `k`, divide by `2M = 26,228`; slope ≈ −0.55, shallower by about 1,
   because `q(k) = k p(k)/⟨k⟩`.

**The sheet does not give the route.** The `k n_k` weighting, the slope
`1 − γ` and the friend slope `2 − γ` are what the student has to produce.

Page 2 has four grids so a student who spoils one can start again; they cross
out the ones they do not want marked. One decade is the same length on both
axes, so a slope measured with a ruler is the slope.

The friend CCDF bends down over its last three points, because nobody has
more than 512 friends. The key accepts a slope from −0.4 to −0.8 for that
reason.

## Files

| File | What it is |
|---|---|
| `quiz04.tex` / `quiz04.pdf` | The sheet handed out. Two pages. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. **Do not hand out.** |
| `quizkit.tex` | Shared preamble, Quiz 3's plus the `\loggrid` graph paper. |
| `build_form.py` | Builds or re-syncs the Google Form through the `gws` CLI. |
| `quiz04-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz04`. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz04.tex
xelatex -interaction=nonstopmode quiz04.tex
xelatex -interaction=nonstopmode solutions.tex
```

## The plumbing

Each step is the one the `quiz02` README documents in full.

- [x] **The Google Form** — made 2026-09-28 (`build_form.py` payload applied
      with `--sync`). Description set; email collection `VERIFIED`.
      - Students: <https://go.skojaku.com/ans-quiz04> →
        <https://docs.google.com/forms/d/e/1FAIpQLSe2D_Hvftpb-a3-XlCpeYFdPrsBuiwtmkEmfIRDSZ--1hbxYQ/viewform>
      - Editor: <https://docs.google.com/forms/d/1Znenf2k9Z8EuXIgcckcGP3xiaMiC_bIsYepmzd2Njs4/edit>
- [ ] **The two upload questions**, by hand in the Forms editor (the API
      refuses them). One per *page*, not per question, because both
      questions are on both pages:

      | Title | Settings |
      |---|---|
      | `Page 1` | File upload · images · 1 file · 10 MB · required |
      | `Page 2` | File upload · images · 1 file · 10 MB · required |

      `gforms_download.py` names the files `q1-` (page 1) and `q2-` (page 2).
- [ ] **The file-responses folder** moved out of Drive root into
      `SSIE 641 Advanced Topics in Network Science/Submission/`, once the
      upload questions exist and Google has made it.
- [ ] **The rubric** in `adv-net-sci-ops/grading/quiz/rubrics/`. Each photo
      holds parts of both questions, so the rubric reads both photos for both
      questions.
- [x] **The two short links** on the droplet, 2026-09-28, beside the `quiz03`
      pair. Validated and reloaded; both answer 302. The pre-edit Caddyfile is
      `/etc/caddy/Caddyfile.bak-2026-09-28-quiz04`.
- [x] **`quiz04.pdf` on Drive**, in the `adv-net-sci-ops` folder beside
      quiz03's, read-only to the `binghamton.edu` domain, link-only.
      `go.skojaku.com/quiz04` points at it. File id
      `15gdZmamHfXxP5EwrKashZPBtbHQiv59N`. Re-upload after any edit:

      ```sh
      GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
      gws drive files update --params '{"fileId": "15gdZmamHfXxP5EwrKashZPBtbHQiv59N"}' \
          --upload quiz04.pdf --upload-content-type application/pdf
      ```
- [ ] Brightspace.
- [ ] Print the sheet.
