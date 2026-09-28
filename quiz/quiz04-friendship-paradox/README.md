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
| `quiz04-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz04`. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz04.tex
xelatex -interaction=nonstopmode quiz04.tex
xelatex -interaction=nonstopmode solutions.tex
```

## The plumbing

None of it is done. Each step is the one the `quiz02` README documents.

- [ ] The Google Form (two upload questions: page 1, page 2).
- [ ] The file-responses folder moved into `Submission/`.
- [ ] The rubric in `adv-net-sci-ops/grading/quiz/rubrics/`.
- [ ] The short links `go.skojaku.com/ans-quiz04` and `go.skojaku.com/quiz04`.
      The QR square already points at the first.
- [ ] `quiz04.pdf` on Drive.
- [ ] Brightspace.
- [ ] Print the sheet.
