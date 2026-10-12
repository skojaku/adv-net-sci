# Quiz 5 — Cores and blocks

**Draft.** An in-class quiz, 20 minutes, 10 points. Page 1 is every question;
page 2, printed on the back, is hints for Question 2. Students answer in their
own notebook, one page per question, and upload one photo per question.
Covers M05 (clustering).

1. **Peel the network** (4 pts), last year's k-core item on an 11-node
   network. (a) The largest k with a non-empty k-core, its nodes, and the
   removal order (2). Answer: k = 3, {A, B, C, D}; removed I, J, K → H → G →
   E, F. (b) Every node's shell (2). Answer: A–D 3, E–H 2, I–K 1. H has the
   most neighbors but shell 2: three of its five neighbors are leaves.
   The network is built so that two shortcuts fail: "every node of degree ≥ 3"
   (A–H) and "every node of degree ≥ 4" (B, D, F, H, not a 4-core).
2. **The likelihood of the degree-corrected block model** (6 pts), the
   Karrer–Newman (2011) derivation. (a) The log-likelihood in c, θ, w,
   self-loops included, simplified until no sum over node pairs is left (2):
   `Σ_i k_i log θ_i + ½ Σ_rs (m_rs log w_rs − w_rs)`. (b) θ̂_i and ŵ_rs for a
   fixed c (2): `k_i / κ_{c_i}` and `m_rs`. (c) Substitute back (2):
   `½ Σ_rs m_rs log(m_rs / κ_r κ_s)` + const.

**The self-loops are written exactly as in the paper, and the sheet warns
about them.** A_ii is twice the number of self-loops at i, and that number is
Poisson with mean ½ θ_i² w. With this convention the pair terms and the
self-loop terms merge into one sum ½ Σ_i Σ_j, exactly, and the normalization
`Σ_{i in r} θ_i = 1` collapses `Σ θ_i θ_j w` to `Σ_rs w_rs`, exactly. Without
the normalization, θ and w trade scale and the estimates are not unique.

**Page 2 gives the route as moves, not results**: the Poisson pmf and the
self-loop identity `Σ_{i<j} F_ij + ½ Σ_i F_ii = ½ Σ_i Σ_j F_ij`; pair terms
versus node terms (a node term leaves the inner sum as a coefficient); the
adjacency matrix ordered by group, cut into blocks, and one block framed with
the rest faded (w is a constant inside it); and Lagrange multipliers, with the
general formula. θ̂ and ŵ are printed nowhere.

**The course assistant is allowed.** The quiz is practice, so the back of the
sheet tells a stuck student to run `pi --model netsci/assistant` and point it
at `go.skojaku.com/quiz05-text`, which is this folder's `quiz05.tex` on GitHub.
The assistant reads the sheet's own definitions from there, because copying
text out of the PDF garbles the formulas, and since 2026-10-12 its system
prompt (on the droplet) says to help with a weekly quiz without giving the
answer and to judge a student's line against the sheet, not the textbook.
`quiz05.tex`'s header comment therefore names no answers; keep them in
`solutions.tex`.

## Files

| File | What it is |
|---|---|
| `quiz05.tex` / `quiz05.pdf` | The sheet handed out. Questions on page 1; hints and the assistant box on page 2. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. |
| `quizkit.tex` | Shared preamble, Quiz 4's without the log–log grid. |
| `build_form.py` | Builds the Google Form by copying Quiz 4's (the API cannot make upload questions); `--info` rewrites its words only. |
| `quiz05-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz05`. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz05.tex
xelatex -interaction=nonstopmode quiz05.tex
xelatex -interaction=nonstopmode solutions.tex
```

## The plumbing

Each step is the one the `quiz02` and `quiz04` READMEs document in full.

- [x] **The Google Form** — made 2026-10-12 with `build_form.py --create`: a
      Drive copy of Quiz 4's form, so the two upload questions (`Question 1`,
      `Question 2`: images, 1 file, 10 MB, required) came with it, then the
      title, description and text item rewritten. Email collection
      `VERIFIED`. The copy arrived unpublished; published and accepting
      responses since 2026-10-12. No responses yet.
      - Students: <https://go.skojaku.com/ans-quiz05> →
        <https://docs.google.com/forms/d/e/1FAIpQLScH20NuJi9agoEN41TRt6N0SqIMOEMe-EKNxqOvTxqypSjbMg/viewform>
      - Editor: <https://docs.google.com/forms/d/1O_sID_M5DdjbxegnPpCnQ0dZZ_FAw38SiLhpsYcZh84/edit>
- [x] **The file-responses folder** `Quiz 5 — Cores and blocks (File
      responses)` (made by Google when the upload questions were first opened
      in the editor; the copy had none) moved out of Drive root into
      `SSIE 641 Advanced Topics in Network Science/Submission/`, 2026-10-12,
      beside Quiz 4's. The form's upload questions still point at it.
- [x] **Three short links** on the droplet, 2026-10-12, beside the `quiz04`
      pair. Validated and reloaded; all answer 302. The pre-edit Caddyfile is
      `/etc/caddy/Caddyfile.bak-2026-10-12-quiz05`.
      - `go.skojaku.com/quiz05` → the PDF on Drive
      - `go.skojaku.com/ans-quiz05` → the form
      - `go.skojaku.com/quiz05-text` → `quiz05.tex` on GitHub `main`, for the
        course assistant (exact match; `/quiz05*` would otherwise catch it)
- [x] **`quiz05.pdf` on Drive**, in the `adv-net-sci-ops` folder beside
      Quiz 4's, read-only to the `binghamton.edu` domain, link-only. File id
      `1HqAuL2qP3oC7aO80LDeT4fDz2iEOvE9o`. Re-upload after any edit:

      ```sh
      GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
      gws drive files update --params '{"fileId": "1HqAuL2qP3oC7aO80LDeT4fDz2iEOvE9o"}' \
          --upload quiz05.pdf --upload-content-type application/pdf
      ```
- [ ] The date. The next class after fall break is Tue 2026-10-20, which
      would make the grade item and quiz `m05-1020`.
- [ ] The rubric in `adv-net-sci-ops/grading/quiz/rubrics/M05-<date>-.../`
      (`session.json` with the form id above, `q1.md`, `q2.md`), kept in step
      with `solutions.tex`.
- [ ] The Brightspace grade item and quiz, and the `deadlines.yaml` row.
- [ ] Print the sheet, double-sided.
