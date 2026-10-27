# Quiz 6 — Four centers

**Draft.** An in-class quiz on M06 (centrality), one question, 10 points. Page 1
is the question and a box to draw in; page 2 is a work page with a table.

**The question.** One page, one question, 10 points, no definitions and no work
page: the sheet explains what a BCDE graph is, says "at most 12 nodes", and leaves
blank space (no answer box). Students look up the four measures themselves. Marks (in the key,
not on the sheet): the graph is valid, 2; each measure's most central node, named
correctly on the student's own graph with no tie, 2 each (no working is asked for). Answers are photographed and
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
- [x] **Two short links on the droplet**, 2026-10-27, beside the `quiz05`
      pair. Validated and reloaded; both answer 302. The pre-edit Caddyfile is
      `/etc/caddy/Caddyfile.bak-2026-10-27-quiz06` (`ssh digitalocean`).
      - `go.skojaku.com/ans-quiz06` → the responder URL above
      - `go.skojaku.com/quiz06` → the PDF on Drive
- [x] **`quiz06.pdf` on Drive**, in the `adv-net-sci-ops` folder beside Quiz 5's,
      uploaded 2026-10-27. File id `18L_K6dql4RQICp6ii2avo6nOx-FAXrwU`.
      **Not shared yet**: Quiz 5's is read-only to the `binghamton.edu` domain,
      link-only, and `hq drive share` has no domain option, so set it in Drive
      (General access → Binghamton University, Viewer). Until then
      `go.skojaku.com/quiz06` does not open for students. Re-upload after any edit:

      ```sh
      GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
      GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file \
      gws drive files update --params '{"fileId": "18L_K6dql4RQICp6ii2avo6nOx-FAXrwU"}' \
          --upload quiz06.pdf --upload-content-type application/pdf
      ```
- [x] **The file-responses folders** exist: `Quiz 6 — Four centers (File
      responses)` with `Question 1 (File responses)` inside, made by Google, as
      for Quiz 5. They arrived in the Drive root and were moved to
      `SSIE 641 Advanced Topics in Network Science/Submission/` on 2026-10-27,
      beside Quiz 5's.
- [x] **The form is published and accepting responses** since 2026-10-27
      (`setPublishSettings`; the copy had arrived unpublished). Not tested with a
      real submission.
- [x] **Brightspace**, 2026-10-27: grade item `m06-1027` (id 664768, 10 points,
      category Quiz); quiz `m06-1027` (id 93507, active, unlimited attempts,
      2026-10-27 09:40 to **2026-11-15 23:59**, the Sunday after two weeks), its
      description linking `go.skojaku.com/ans-quiz06` and `go.skojaku.com/quiz06`;
      the row in `adv-net-sci-ops/brightspace/course/deadlines.yaml`
      (`sync-deadlines` shows no drift). The PDF is also a page, `Quiz 6 — Find a
      BCDE graph`, in the module **M06**, which is **still hidden**, so students
      cannot see that page until the module is shown.
- [ ] The rubric in `adv-net-sci-ops/grading/quiz/rubrics/`, kept in step with
      `solutions.tex` (the grader maps the upload question `Question 1`).
- [ ] **The time.** The sheet says 20 minutes. Finding a graph is quick with a
      template; checking four centralities on 12 nodes, eigenvector above all,
      is not. If it is done in class, 20 minutes may be tight.
- [ ] Print the sheet.
