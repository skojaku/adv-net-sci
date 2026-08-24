# Quiz 1 — Euler paths

An in-class quiz, 15 minutes, 10 points. One printed page of questions;
answers go into a Google Form.

1. **Even degrees are not enough** (4 pts). Give an *undirected* graph where
   every node has even degree but no Euler path exists, and name the missing
   requirement. The answer is connectivity.
2. **Now the edges have directions** (6 pts). State the condition for an Euler
   path in a *directed* graph, then give one graph that has such a path and one
   that does not.

The sheet carries the questions only — no boxes and no ruled lines. Students
think on the back or on scratch paper, type their graphs into the form as edge
lists, and photograph their working for the upload question at the end.

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

## The Google Form

- **Students:** <https://go.skojaku.com/ans-quiz01>
- **Editing and responses:** <https://docs.google.com/forms/d/1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q/edit>
- Form id: `1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q`
- Owned by the Binghamton account (`~/.config/gws-binghamton`).

The form carries the full text of both questions, in the same order as the
sheet. Each graph is typed as an edge list — `A - B` one per line for
Question 1, `A -> B` for Question 2.

Quiz mode is on and the point values match the sheet (3 / 1 and 3 / 2 / 1).
Google Forms only takes whole-number points. Email collection is `VERIFIED`, so
respondents sign in with their `@binghamton.edu` account — which is also what
maps an uploaded photo back to a student.

`python3 build_form.py --sync` rewrites the live form's questions from the
script. It deletes every item first, so run it only before responses arrive.

### One question is added by hand

The Forms API refuses to create file-upload questions —
`Creation of file_upload question not supported`. So the photo-upload question
in the closing "Your working" section is added in the Forms editor:

> File upload · allow images and PDF · 2 files · 10 MB · required

Do that once, in the editor link above, and re-add it after any `--sync`.

## Where the photos go

The course convention lives in `~/Downloads/teaching/adv-net-sci-ops/README.md`
and is owned by the Brightspace tooling, not by this folder. In short: uploads
land in the form owner's Drive, and `gforms_download.py` files them under a
per-session folder in the Drive folder `adv-net-sci-ops`
(`1m4ZTV0Lgf7LYXU8mn-l3DHZV96hKU-El`), one subfolder per student email.

This quiz's session folder already exists:

```
adv-net-sci-ops/M01-2026-08-25-EulerPaths/   (1y9ndq4yvLsODnh-Eua9J0wgb-CQYg2FM)
```

To pull the photos down after class:

```sh
python3 ~/Downloads/teaching/adv-net-sci-ops/gforms_download.py \
    --form 1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q \
    --session M01-2026-08-25-EulerPaths
```

That step needs the Forms API switched on in the GCP project
`formal-precinct-489402-s5`; the folder-creating half works without it.

## The short link

The QR square and the printed address are both `go.skojaku.com/ans-quiz01`, not
the form's own URL. Paper outlives any one form: Caddy on the course droplet
sends that path to the current Google Form, so swapping forms is a line on the
server rather than a reprint.

```
ssh digitalocean
# /etc/caddy/Caddyfile, block go.skojaku.com
	handle /ans-quiz01* {
		redir https://docs.google.com/forms/d/e/1FAIpQLSfUFOW3jdXvEPvhac3tFVz865TkEaX4YOprQQnq7oV77r4lOA/viewform 302
	}
```

After editing: `caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile`
then `systemctl reload caddy`.

If the printed link itself ever changes, rebuild the square and the PDF:

```sh
uvx --from segno segno --output=quiz01-form-qr.png --scale=20 --border=1 \
    --error=m "https://go.skojaku.com/ans-quiz01"
```

and update `\formlink` and `\formshort` in `quizkit.tex`.
