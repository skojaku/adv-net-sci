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
   dark square is 0, 1, 0, 1 for t = 1..4, so p(t) does not converge to π (1). (b) why p(t) does not converge, from the
   spectrum and the structure of P (not numerically): with the squares ordered by colour,
   P = [[0, B], [C, 0]], so −1 is an eigenvalue (eigenvector +1 on dark, −1 on light) (3).

The sheet was cut down on 2026-11-05: the first version had four parts in Question 1
and three in Question 2, and the lecturer reduced them to one and two. The speed of
convergence (eigenvalue −0.857, not the second eigenvalue 0.654) and the lazy walk
are in the key as "not asked".

**What the pair tests.** Question 1 uses the stationary distribution (the left
eigenvector of eigenvalue 1) as the weights of the final opinion. Question 2 shows a
walk whose eigenvalue −1 stops p(t) from converging. In both, the speed of
convergence depends on the eigenvalue with the largest absolute value, which can be a
negative one and not the second largest. The lecturer explains the model before the quiz.

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

## Form and links (2026-11-05)

- Form: id in `build_form.py`; made by `--create` (the first attempt failed with a Drive storage quota error, the second worked). Two upload questions, "Question 1" and "Question 2".
- Responder URL: https://docs.google.com/forms/d/e/1FAIpQLScbLLq5eW3iuSQdGj-AbdgFJBKO_IRvU50Gc8bDbvNfgiztVA/viewform
- `go.skojaku.com/ans-quiz07` redirects to it (Caddy on `ssh digitalocean`).

Not done: the Brightspace quiz entry.
