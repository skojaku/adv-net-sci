# Quiz 7 — Opinions and a knight

**Draft.** An in-class quiz on M07 (random walks), 20 minutes, 10 points, one page.
Students answer on their own paper, one page per question, and upload one photo
per question to a Google Form (QR square on the sheet).

1. **Opinions on a network** (6 pts), the DeGroot model on five friends (a triangle
   A, B, C with a tail C–D–E). Each round a person takes the average of their
   friends' opinions; opinions are in [0, 1]. (a) One round, and the sum of the
   opinions is not conserved (1). (b) Weights w_i = k_i with Σ w_i x_i conserved, and
   the proof (2). (c) The final opinion, 0.56 (1); the plain mean 0.6 is the trap.
   (d) The eigenvalues are given (1, 0.654, −0.298, −0.500, −0.857); the rate is
   set by −0.857, not by the second eigenvalue 0.654 (2).
2. **A knight on a chessboard** (4 pts). (a) From a1 the probability of a dark
   square is 0, 1, 0, 1 for t = 1..4, so p(t) does not converge to π (1). (b) −1 is an
   eigenvalue; the eigenvector is +1 on dark squares and −1 on light squares (2).
   (c) With a stay probability ½ the eigenvalues become (1 + λ)/2, so −1 becomes 0
   and p(t) converges (1).

**The point of the pair.** The two questions are about the lecture's two claims, the
stationary distribution (the left eigenvector of eigenvalue 1) and the speed of
convergence. Both are used in a setting where the textbook sentence needs a
second look: in DeGroot the weights act on opinions from the other side, and in both
questions the speed is set by the eigenvalue with the largest absolute value, which is
not the second largest eigenvalue when a negative eigenvalue is bigger in size.
The lecturer walks through the model and this difference before the quiz.

Every number in the key was computed with numpy (see the header of `solutions.tex`).

## Files

| File | What it is |
|---|---|
| `quiz07.tex` / `quiz07.pdf` | The sheet handed out. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. |
| `quizkit.tex` | Shared preamble, Quiz 6's with the numbers changed. |
| `quiz07-form-qr.png` | The QR square. Encodes `go.skojaku.com/ans-quiz07`. |

Build the PDFs (xelatex, twice):

```sh
xelatex -interaction=nonstopmode quiz07.tex
xelatex -interaction=nonstopmode solutions.tex
```

## Not done

The Google Form (copy Quiz 6's `build_form.py`), the Caddy short link
`go.skojaku.com/ans-quiz07` (the QR square already points at it), and the
Brightspace quiz entry.
