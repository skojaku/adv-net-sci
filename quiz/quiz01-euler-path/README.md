# Quiz 1 — Euler paths

An in-class quiz, 15 minutes, 10 points. One printed page of questions;
students write by hand and hand in one photo per question.

1. **Even degrees are not enough** (4 pts). Give an *undirected* graph where
   every node has even degree but no Euler path exists, and name the missing
   requirement. The answer is connectivity.
2. **Now the edges have directions** (6 pts). State the condition for an Euler
   path in a *directed* graph, then give one graph that has such a path and one
   that does not.

The sheet carries the questions only — no boxes and no ruled lines. Students
put each question's answer on its own page, then upload one photo per
question.

## Files

| File | What it is |
|---|---|
| `quiz01.tex` / `quiz01.pdf` | The sheet handed out. One page. |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes. **Do not hand out.** |
| `quizkit.tex` | Shared preamble: fonts, the submission link, layout macros. |
| `quiz01-form-qr.png` | The QR square on the sheet. Encodes `go.skojaku.com/ans-quiz01`. |
| `build_form.py` | Builds or re-syncs the Google Form through the `gws` CLI. |

Build the PDFs (xelatex, run twice so the links resolve):

```sh
xelatex -interaction=nonstopmode quiz01.tex
xelatex -interaction=nonstopmode quiz01.tex
xelatex -interaction=nonstopmode solutions.tex
```

## Two short links

The QR square and the printed address are the course's own short links, not
Google's. Paper outlives any one form or file, so swapping either is a line on
the droplet rather than a reprint.

| Link | Goes to |
|---|---|
| `go.skojaku.com/quiz01` | the question PDF on Drive |
| `go.skojaku.com/ans-quiz01` | the Google Form, where the photos go |

Both are `handle` blocks in the `go.skojaku.com` site of
`/etc/caddy/Caddyfile` on `ssh digitalocean`. After editing, run
`caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile`, then
`systemctl reload caddy`.

If the printed link ever changes, rebuild the square and the PDF:

```sh
uvx --from segno segno --output=quiz01-form-qr.png --scale=20 --border=1 \
    --error=m "https://go.skojaku.com/ans-quiz01"
```

and update `\formlink` and `\formshort` in `quizkit.tex`.

## The question PDF on Drive

`quiz01.pdf` is uploaded to the Drive course folder and shared **read-only with
the `binghamton.edu` domain** — link-only, not searchable. Students are signed
in to that account anyway, because the form demands it.

- File id: `19oxyPszM11lZ9-CzStr1Yalog_aR9rkj`
- <https://drive.google.com/file/d/19oxyPszM11lZ9-CzStr1Yalog_aR9rkj/view>

Re-upload after any edit to the sheet, or the link serves a stale quiz:

```sh
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
gws drive files update --params '{"fileId": "19oxyPszM11lZ9-CzStr1Yalog_aR9rkj"}' \
    --upload quiz01.pdf --upload-content-type application/pdf
```

## The Google Form

- **Students:** <https://go.skojaku.com/ans-quiz01>
- **Editing and responses:** <https://docs.google.com/forms/d/1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q/edit>
- Form id: `1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q`
- Owned by the Binghamton account (`~/.config/gws-binghamton`).

The form is a **drop box, not a copy of the quiz**. It links to the PDF and
takes one photo per question. Nothing in it has to stay in step with the sheet,
and there is no typing for the student to do.

Email collection is `VERIFIED`, so respondents sign in with their
`@binghamton.edu` account — which is what maps an uploaded photo back to a
student.

`python3 build_form.py --sync` rewrites the live form from the script. It
deletes every item first, so run it only before responses arrive.

### The upload questions are added by hand

The Forms API refuses to create file-upload questions —
`Creation of file_upload question not supported`. So the two questions that
matter are made in the Forms editor:

| Title | Settings |
|---|---|
| `Question 1` | File upload · images · 1 file · 10 MB · required |
| `Question 2` | File upload · images · 1 file · 10 MB · required |

One box per quiz question is what lets you grade a question across the whole
class in one pass: `gforms_download.py` reads the number out of the title and
names the files `q1-…` and `q2-…`. Keep the titles numbered.

`--sync` cannot put these back, so it refuses while they exist. Pass `--force`
if you really mean to wipe the form, then re-add them in the editor.

## Where the photos go

The course convention lives in `adv-net-sci-ops/tools/quiz-photos/README.md`
and is owned by the Brightspace tooling, not by this folder. In short: uploads
land in the form owner's Drive, and `gforms_download.py` files them under a
per-session folder in the Drive folder `adv-net-sci-ops`
(`1m4ZTV0Lgf7LYXU8mn-l3DHZV96hKU-El`), one subfolder per student email.

This quiz's session folder already exists:

```
adv-net-sci-ops/M01-2026-08-25-EulerPaths/
  student@binghamton.edu/
    q1-IMG_1234.jpg
    q2-IMG_1235.jpg
```

Folder id `1y9ndq4yvLsODnh-Eua9J0wgb-CQYg2FM`.

To pull the photos down after class:

```sh
python3 ~/Documents/teaching/adv-net-sci-ops/tools/quiz-photos/gforms_download.py \
    --form 1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q \
    --session M01-2026-08-25-EulerPaths
```

The Forms API answers normally on these credentials, despite the note in that
README saying it needs switching on — `forms.forms.responses.list` was checked
on 2026-08-25 and returned an empty result rather than a 403.
