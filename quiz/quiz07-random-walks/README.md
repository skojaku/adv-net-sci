# Quiz 7 — Opinions and a knight

**Draft.** An in-class quiz on M07 (random walks), 20 minutes, 10 points, one page.
Students answer on their own paper, one page per question, and upload one photo
per question to a Google Form (QR square on the sheet).

1. **Opinions on a network** (6 pts), the DeGroot model on five friends (a triangle
   A, B, C with a tail C–D–E); the opinions are written on the nodes. Each round a
   person takes the average of their friends' opinions. One question: the final opinion
   of each person, 0.56 for all. The plain mean 0.6 is the trap. The key marks
   consensus (1), weights proportional to the degree (2), the proof that the
   weighted sum is conserved (2) and the value (1).
2. **A knight on a chessboard** (4 pts). Two small boards show the knight's jumps
   (from d4, from a1) and the dark and light squares. (a) From a1 the probability of a
   dark square is 0, 1, 0, 1 for t = 1..4, so p(t) does not converge to π (1). (b) −1 is
   an eigenvalue; the eigenvector is +1 on dark squares and −1 on light squares (3).

The sheet was cut down on 2026-11-05: the first version had four parts in Question 1
and three in Question 2, and the lecturer reduced them to one and two. The speed of
convergence (eigenvalue −0.857, not the second eigenvalue 0.654) and the lazy walk
are in the key as "not asked".

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
