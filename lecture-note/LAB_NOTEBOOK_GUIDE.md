# The lab notebook a sheet hands off to

How the marimo notebook at the end of a pen-and-paper sheet is built, and the
two things about molab that will otherwise cost an afternoon. The sheet itself
is `.claude/skills/pen-and-paper/SKILL.md`; this file is the notebook half of
the same deliverable.

A sheet's last part sends the student to a marimo notebook that runs, by
machine, the thing they have just done in pencil. The working example is
Module 1:

- `lecture-note/m01-euler_tour/pen-and-paper/lab.py` — the student's copy
- `lecture-note/m01-euler_tour/pen-and-paper/lecture-hall.css` — the look,
  copied verbatim from the mini-project's `assignment/lecture-hall.css`
- `lecture-note/m01-euler_tour/pen-and-paper/lab-solutions.py` — generated
- `tools/build_m01_lab_notebooks.py` — generates it, and welds the CSS in

The sheet reaches it by a short printed URL (`\molaburl` in the `.tex`), typed
by hand from paper, pointing at the notebook uploaded to
[molab](https://molab.marimo.io). **molab is the deployment target, and it is
what constrains the file.**

---

## molab constraints, and how each one is handled

**One file arrives, and nothing is fetched at run time.** A student opens the
URL in a lecture hall on bad wifi. Anything the notebook needs must be inside
the notebook: no sibling data files, no CDN, no `open("something.csv")`.
`__file__` is also missing in some hosted runtimes, so never build a path from
it without a fallback.

**`css_file` is ignored** — [marimo-team/marimo#8467](https://github.com/marimo-team/marimo/issues/8467).
Setting `marimo.App(css_file="lecture-hall.css")` styles the notebook locally
and silently does nothing on molab, which is the worst kind of bug: it looks
fixed on the machine where you wrote it.

The workaround marimo's maintainer gives in that issue is a `<style>` tag in
the first cell — stylesheets are global, so one tag dresses the whole notebook,
in the editor, in `marimo run`, and in molab. So the CSS travels inside the
file:

```python
app = marimo.App(width="medium")          # no css_file

with app.setup(hide_code=True):
    import base64
    LECTURE_HALL_CSS_B64 = ""  # BUILT     <- one long line, written by the tool
    LECTURE_HALL_CSS = base64.b64decode(LECTURE_HALL_CSS_B64).decode("utf-8")


@app.cell(hide_code=True)
def _():
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return
```

Base64, not a triple-quoted string: no quote or backslash in the CSS can then
break the Python. `tools/build_m01_lab_notebooks.py` rewrites the `# BUILT`
line from the `.css` file, so the stylesheet stays editable as CSS and the
notebook stays self-contained. Run it after touching either.

Verify it actually landed, rather than trusting the local render:

```sh
uvx marimo export html --sandbox lab.py -o /tmp/lab.html
python3 -c "print('\"text/html\": \"<style>' in open('/tmp/lab.html').read())"
```

The output must be stored as **`text/html`**, not `text/plain` — that is the
difference between a live `<style>` element and the CSS printed on the page as
text.

---

## The shape of the notebook

Modelled on the mini-project's `assignment.py`; keep the two recognisably the
same page.

- **A hidden `app.setup` kit**: colours, the SVG drawing functions, `mo.md`
  helpers, `plain_adjacency`, `is_connected`, the `*_ready` predicates. Headed
  "Nothing here is yours to edit."
- **`✍️` on every cell the student touches**, and nothing else. Three to six of
  them is the budget; the rest of the notebook runs itself.
- **An in-line check under every ✍️ cell**, which names the mistake rather than
  saying "wrong": *"Ithaca touches 2 of your roads, not 3 — the counts are
  Question 3 on the sheet."*
- **A waiting card, not an exception**, for anything downstream of a blank:
  `if not ready: _out = WAITING`. A red traceback on an untouched notebook
  reads as "this is broken", not "your turn".
- **Animations run from the moment it opens.** They build their own matrices
  from the kit, never from student code.

## The teaching figure is not the student's task

The mistake worth not repeating: the Module 1 animation first walked the sheet's
own map and printed its edge list, and the next cell then asked the student to
type that list in. The answer was on the screen.

So the worked example is a **different, smaller network** — a village on a
river, three places, four bridges — and it carries the awkward case on purpose
(two bridges between the same pair, so the write-the-pair-twice rule is met and
named before it is needed). The student's own map appears as a picture above
the ✍️ cell, with its nodes numbered, and **no cell anywhere prints its edge
list**. The same rule applies to the checks: `to_adjacency` is checked on the
village, because a grid of the right answer is that edge list in another
notation.

## The answer copy

`lab-solutions.py` is generated, never edited. Every answer in
`tools/build_m01_lab_notebooks.py` is anchored to a string that must appear in
`lab.py` **exactly once**; if a blank moves or a hint is reworded, the script
stops rather than writing an answer copy that is a version behind. It also
asserts no `TASK` survives, and stamps a do-not-edit banner into the output.

## Checking a notebook before calling it done

```sh
uvx marimo export script lab.py > /dev/null          # syntax and the reactive DAG
uvx marimo export html --sandbox lab.py -o /tmp/a.html   # actually runs every cell
```

Then, on `/tmp/a.html`:

- `Traceback` count is 0.
- With the blanks blank: the waiting cards appear, the checks read "not yet",
  and the animations have already drawn.
- With the blanks filled in a scratch copy: every check reads green, and the
  numbers agree with the answer key.

The exported HTML embeds each cell's output, so grepping it for the strings the
checks emit is a real test, not a proxy.
