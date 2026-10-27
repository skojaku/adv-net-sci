# Quiz 6 — Four centers

**Draft.** An in-class quiz on M06 (centrality), one question, 10 points. Page 1
is the question and a box to draw in; page 2 is a work page with a table.

**The question.** Draw a connected graph with **at most 12 nodes** in which
betweenness, closeness, degree and eigenvector centrality each have exactly one
most central node, and the four nodes are all different. Part (a), the drawing,
is 2 points; part (b), naming each center and showing it beats every other node,
is 8 (2 per measure).

This is the "distinct singleton centers" problem of Brandes and Hildenbrand,
*Smallest graphs with distinct singleton centers*, Network Science 2(3),
416–418 (2014). The paper calls these graphs **BCDE** (Betweenness, Closeness,
Degree, Eigenvector). The lecturer's name for them was "ABCD"; the sheet uses
neither and names the four measures in full, so no letter can be mistaken for a
node. Their findings, for reference:

- no graph with fewer than **10** nodes works; there are seven with 10 nodes
  (and 14 to 16 edges);
- the smallest by nodes plus edges has 11 nodes and 11 edges (unique);
- Krackhardt's kite (10 nodes, 18 edges) is *not* one: its closeness center is
  two nodes, and degree and eigenvector pick the same node;
- the smallest *trees* have 15 nodes.

## Why 12

Decided with the lecturer on 2026-10-27, from two measurements
(`check_bcde.py`'s test, run on random connected graphs):

| nodes | random connected graphs that are BCDE | found by flipping edges at random (48 runs, 4000 flips) |
|---|---|---|
| ≤ 9 | 0 (none exist) | 0 / 48 |
| 10 | 0 of 40 000 (seven exist among 11.7 million) | 3 / 48 |
| 11 | 0.010 % | 12 / 48 |
| 12 | 0.015 % | 11 / 48 |
| 13 | 0.040 % | 14 / 48 |
| 15 | 0.095 % | 9 / 48 |

11 leaves almost nothing to find, 13 is Everett's published answer and leaves
room. 12 is in between. These are computer searches, not students at a desk, and
48 runs per row is noisy: read the order, not the digits. The limit is "at most
12", so a student who finds 10 or 11 is not penalised.

**The sheet does not say whether to use code, and does not forbid it** (lecturer's
call, 2026-10-27: by hand is better, and a student who wants code will ask).

## Files

| File | What it is |
|---|---|
| `quiz06.tex` / `quiz06.pdf` | The sheet handed out. |
| `solutions.tex` / `solutions.pdf` | Answer key: a 12-node, 13-edge model graph with every value, and marking notes. |
| `quizkit.tex` | Shared preamble, Quiz 5's without the form link. |
| `check_bcde.py` | Checks a student's edge list: values, each center, ties, and the verdict. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz06.tex
xelatex -interaction=nonstopmode quiz06.tex
xelatex -interaction=nonstopmode solutions.tex
```

Check a student's graph:

```sh
uv run --with networkx --with numpy check_bcde.py "1-2 1-3 1-4 2-6"   # any edge list
uv run --with networkx --with numpy check_bcde.py --demo              # the model graph
```

Exit 0 means four different unique centers. Ties in betweenness and eigenvector
are decided to 1e-9; closeness is decided on the exact integer sum of distances.

## Still to do

Nothing below has been made. The quiz is a PDF and a key, and nothing else.

- [ ] The date, and so the Brightspace quiz name (`m06-<date>`).
- [ ] How students hand it in. Quiz 5 used a Google Form with two photo uploads
      (`build_form.py` there copies Quiz 4's form). This sheet has no QR square
      or form address yet.
- [ ] Short links on the droplet, as for Quiz 5 (`quiz06`, `ans-quiz06`).
- [ ] `quiz06.pdf` on Drive, in the `adv-net-sci-ops` folder.
- [ ] The rubric in `adv-net-sci-ops/grading/quiz/rubrics/`, kept in step with
      `solutions.tex`.
- [ ] The Brightspace quiz and grade item, and the `deadlines.yaml` row.
- [ ] **The time.** The sheet says 20 minutes. Finding a graph is quick with a
      template; checking four centralities on 12 nodes, eigenvector above all,
      is not. If it is done in class, 20 minutes may be tight.
- [ ] Print the sheet, double-sided.
