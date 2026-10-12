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
