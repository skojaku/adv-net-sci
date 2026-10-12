# Quiz 5 — Communities: noise and likelihood

**Draft.** An in-class quiz, 20 minutes, 10 points. Page 1 is every question;
page 2, printed on the back, is hints for Question 2. Students answer in their
own notebook, one page per question, and upload one photo per question.
Covers M05 (clustering).

1. **Communities in pure noise** (4 pts). A trend question: Erdős–Rényi
   networks with N = 10,000 and ⟨k⟩ = 1, 2, 4, …, 128, no communities planted.
   (a) Does the best modularity Q_max go up or down with ⟨k⟩, and where does it
   head at each end (2). Answer: down; toward 1 when very sparse, 0 when
   complete. (b) Why, and what to check before believing Q = 0.45 at
   ⟨k⟩ = 4 (2). Answer: chance is lumpy in sparse networks; compare against
   randomized networks of the same size and density, where noise alone gives
   ≈ 0.56.
2. **The likelihood of the degree-corrected block model** (6 pts), the
   Karrer–Newman (2011) derivation. (a) The log-likelihood in c, θ, w,
   simplified until no sum over node pairs is left (2):
   `Σ_i k_i log θ_i + ½ Σ_rs (m_rs log w_rs − w_rs)`. (b) θ̂_i and ŵ_rs for a
   fixed c (2): `k_i / κ_{c_i}` and `m_rs`. (c) Substitute back (2):
   `½ Σ_rs m_rs log(m_rs / κ_r κ_s)` + const.

**Page 1 gives the model, not the route.** It has to state the normalization
`Σ_{i in r} θ_i = 1` (without it θ and w trade scale and the estimates are not
unique) and the large-N convention `Σ_{i<j} → ½ Σ_i Σ_j` (it removes the
self-pairs). **Page 2 gives the route as moves, not results**: the Poisson
pmf, pulling a one-end factor out of the inner sum, collecting a sum over
pairs by groups, and a Lagrange multiplier per group. θ̂ and ŵ are printed
nowhere.

Q_max values measured with Leiden (igraph), three draws each:

| ⟨k⟩   | 1    | 2    | 4    | 8    | 16   | 32   | 64   | 128  |
|-------|------|------|------|------|------|------|------|------|
| Q_max | 0.99 | 0.85 | 0.56 | 0.36 | 0.24 | 0.17 | 0.11 | 0.08 |

## Files

| File | What it is |
|---|---|
| `quiz05.tex` / `quiz05.pdf` | The sheet handed out. Questions on page 1, hints on page 2. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. **Do not hand out.** |
| `quizkit.tex` | Shared preamble, Quiz 4's without the log–log grid. |
| `quiz05-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz05`. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz05.tex
xelatex -interaction=nonstopmode quiz05.tex
xelatex -interaction=nonstopmode solutions.tex
```

## The plumbing

Each step is the one the `quiz02` and `quiz04` READMEs document in full.
None is done yet.

- [ ] The date. The next class after fall break is Tue 2026-10-20, which
      would make the grade item and quiz `m05-1020`.
- [ ] `build_form.py` and the Google Form, with the two upload questions
      `Question 1` and `Question 2` added by hand.
- [ ] The rubric in `adv-net-sci-ops/grading/quiz/rubrics/M05-<date>-.../`
      (`session.json`, `q1.md`, `q2.md`), kept in step with `solutions.tex`.
- [ ] The two short links on the droplet (`ans-quiz05`, `quiz05`).
- [ ] `quiz05.pdf` on Drive.
- [ ] The Brightspace grade item and quiz, and the `deadlines.yaml` row.
- [ ] Print the sheet, double-sided.
