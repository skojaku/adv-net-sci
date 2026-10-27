# Quiz 6 — Four centers

**Draft.** An in-class quiz on M06 (centrality), one question, 10 points. Page 1
is the question and a box to draw in; page 2 is a work page with a table.

**The question.** One page, one question, 10 points, no definitions and no work
page: the sheet explains what a BCDE graph is, says "at most 12 nodes", and leaves
a blank box. Students look up the four measures themselves. Marks (in the key,
not on the sheet): the graph is valid, 2; each measure's most central node with
the evidence that nothing ties with it, 2 each. Answers are photographed and
uploaded to a Google Form (QR square on the sheet).

This is the "distinct singleton centers" problem of Brandes and Hildenbrand,
*Smallest graphs with distinct singleton centers*, Network Science 2(3),
416–418 (2014). The paper calls these graphs **BCDE** (Betweenness, Closeness, Degree,
Eigenvector), and so does the sheet. ("ABCD", said on 2026-10-27, was a slip.)
The sheet explains what a BCDE graph is and leaves the definitions of the four
measures to the students. Their findings, for reference:

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
| `quiz06.tex` / `quiz06.pdf` | The sheet handed out: one page. |
| `solutions.tex` / `solutions.pdf` | Answer key: a 12-node, 13-edge model graph with every value, and marking notes. |
| `quizkit.tex` | Shared preamble: Quiz 5's, with the form link for Quiz 6. |
| `build_form.py` | Makes the Google Form by copying Quiz 4's (the API cannot make upload questions), keeping one upload question; `--info` rewrites its words only. |
| `quiz06-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz06`. |
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

## The plumbing

- [x] **The Google Form** made 2026-10-27 with `build_form.py --create`: a Drive
      copy of Quiz 4's form with its second upload question deleted, so one
      upload question (`Question 1`: images, 1 file, 10 MB, required) is left,
      then the title, description and text item rewritten. Email collection
      `VERIFIED`. Not checked: whether the copy arrives published and accepting
      responses (Quiz 5's did, since 2026-10-12), and the file-responses folder,
      which Google makes when the upload question is first opened in the editor
      (move it under `SSIE 641 Advanced Topics in Network Science/Submission/`,
      beside Quiz 5's; the upload question still points at it).
      - Responder: <https://docs.google.com/forms/d/e/1FAIpQLScYKKqDkybxGbCmuo9y0__oCWbFLvw7iWf4bmiMtfckhgKitQ/viewform>
      - Editor: <https://docs.google.com/forms/d/1eccy9rko9kDemSq8dwgDsN0ubT8gekQOHOnrCrVpdlI/edit>
- [ ] **Three short links on the droplet**, as for Quiz 5. The QR square and
      the form's description already point at them, so **they are dead until
      these exist**:
      - `go.skojaku.com/quiz06` → the PDF on Drive
      - `go.skojaku.com/ans-quiz06` → the responder URL above
- [ ] `quiz06.pdf` on Drive, in the `adv-net-sci-ops` folder, read-only to the
      `binghamton.edu` domain, link-only.
- [ ] The date, and so the Brightspace quiz name (`m06-<date>`).
- [ ] The rubric in `adv-net-sci-ops/grading/quiz/rubrics/`, kept in step with
      `solutions.tex` (the grader maps the upload question `Question 1`).
- [ ] The Brightspace quiz and grade item, and the `deadlines.yaml` row.
- [ ] **The time.** The sheet says 20 minutes. Finding a graph is quick with a
      template; checking four centralities on 12 nodes, eigenvector above all,
      is not. If it is done in class, 20 minutes may be tight.
- [ ] Print the sheet.
