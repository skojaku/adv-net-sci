# Talk playbook: from a topic to a signed-off talk deck (IPE seminar @ HKUST(GZ), 2026-10-17 to 2026-10-21)

How the 92-slide, 40-minute talk "Ideas Lost, Late, and Found" was made, and what the lecturer signed off:
「今回のスライドは出来がとても良いです。背景や色使い、文字の大きさ、そして僕らが行ったような添削と修正もとても良かったです。
図の作り方やアニメーションの作り方もすべて良かった」(2026-10-21). Seven things were praised: **background, colours, type size,
the red-pen review-and-fix loop, how figures are made, how animations are made**. Do all seven the same way next time.

Read `HOUSE_STYLE.md` first (the look and the layouts). This file adds the *process* and the techniques that deck introduced.
Where the two disagree, this file is newer for a **talk**; HOUSE_STYLE section 10 (story) still decides the beats.

The deck is the reference implementation, kept as a snapshot in `house/ipe-seminar-2026/` (code only; the assets are not
copied, so it does not run alone) and live in `~/Documents/projects/talk-ipe-honkong-2027/` (generator `review/make_wireframe.py`).
Reusable pieces were pulled out: `house/sketch_kit.py` (hand-drawn SVG and call-outs), `house/washi-scan.jpg` (the paper),
`house/grain.png`, and `theme-house.css` (which now has the paper background).

## 1. The order of work: five stages, each ending in a red-pen round

| stage | what exists at the end | the lecturer's move |
|---|---|---|
| 0 Story | the spine (F sentences), the arc of each part, minutes per part, the beat of every slide | reads the spine aloud, changes the story here |
| 1 Wireframe | **every slide exists**, with dashed grey boxes where figures will go; each box says what goes in it and where it comes from | red pen on contact sheets (round 1, 2, 3 ...) |
| 2 Real figures | boxes replaced by drawn sketches, cropped paper figures, photos | red pen again |
| 3 Animation | GIFs and videos where a slide is about motion | watches `deck.html`, says what to change |
| 4 Polish | split dense slides into builds, enlarge, trim, align, re-word | final read |

The wireframe is stage 1 *on purpose*: the lecturer fixes the story, the order and the beats on boxes, which cost nothing
to move, before any figure is drawn. 45 slides at v1 became 92 after four wireframe rounds; slides were added, deleted
and split freely. The git log of the deck is 52 commits between 17 and 19 October, one per round or per batch of fixes.

Never draw a real figure for a slide whose place in the story is not yet settled.

The wording is final from the wireframe on: titles are literal (N9). A wireframe title such as "One walk, three worlds" is
sent back, because the title is the one thing a wireframe does contain.

## 2. The deck is generated from one Python slide list

`review/make_wireframe.py` holds `S(cls, title, ..., beat, src, note, key, ft, body, fig, bg)` calls in talk order. It writes
`deck.md` **and** `review/DECK_SPEC.md` (time plan, spine, arcs, footers, a table of every slide with its layout, title, beat,
figure and source). Why generate:

- renumbering is free: slides are added and deleted every round, and the numbers in the spec, the sheets and the speaker
  notes follow automatically;
- the spine, the time plan (seconds per slide per part) and the cut candidates are computed, not maintained by hand;
- the same CSS, footers and helper functions apply to all slides.

Fields that earned their place:

- `beat`: what this slide is *for* ("hook: a circle", "result (drift, 1/2)", "method (3b/4): the objective"). The lecturer and
  the workers refer to slides by beat, because numbers shift. A beat with `(k/n)` marks a build.
- `src`: where the figure comes from (paper and figure number, file path, URL). The lecturer reads it on the sheet.
- `note`: the speaker note, which starts with `[#N] beat: ...`; it also records **how the red-pen note was read** and what
  to say. The sheets take their captions from these `[#N] beat:` lines.
- `key`: a name for cross-references in the spec ("the Tshitoyan slide (slide 26)").
- `ft`: a per-slide footer override (the black reference bar), for someone else's work or a photo credit.
- `bg` and `dark`: a dark full-bleed slide (video, big map).

The generator prints warnings the lecturer would otherwise find by eye (titles over 40 characters on L-b and L-a). Add such
checks as they come up.

The spec carries a **"Settled" and a "Still open" list** at the foot of each round, so a decision is never asked twice.
Footers per part: the paper reference of the part (parts 0 and the close have none).

## 3. The red-pen loop (添削と修正), exactly as run

1. **Sheets.** Render every slide to PNG (`marp deck.md --theme-set theme.css --html --allow-local-files --no-stdin --images png
   --image-scale 1 -o review/_r/wf.png < /dev/null`) and run `review/make_sheets.py` (`house/ipe-seminar-2026/review/`):
   `sheets-landscape.pdf` (4 columns x 3 rows, 12 per page) and `sheets-portrait.pdf` (2 x 4, 8 per page). Each slide is
   numbered and captioned in red with its beat. `render.sh` does all of it. He marks the portrait sheets on a tablet and
   sends scans (`h-NN.png`, 200 dpi, one page each). Keep the scans in the scratchpad; crop quarters (`rP_R.png`) to read
   small handwriting.
2. **Read the notes into rules, not into patches.** His notes are short imperatives, sometimes in Japanese, often about the
   *look* of one slide that applies to its siblings. Examples and the rule behind them:
   - 「矢印はかぶらない」: arrows start beside an emoji, never on it, and never cross each other.
   - 「矢印は両方向ける」: when two things are pulled together, both of them get an arrow, pointing at each other.
   - 「前の2点をうすく、1つのこす」: when a slide adds a new item to a previous picture, fade the old ones and keep one solid.
   - 「embedding 大きく!」, 「小さい → 大きく」: the object under discussion is the largest thing on the slide.
   - 「平行にする」: an analogy is drawn as a parallelogram, the parallel arrows exactly parallel.
   - 「ボーダーで囲みたい」: a partition is shown with borders (a Venn diagram), not with shading.
   - 「できれば絵文字で」: use emoji or pictures instead of dots wherever the thing is nameable.
   - 「ベン図のように境界線を引く」, strike out `, too,`: remove the hedging word instead of rewording the sentence.
   - 「split into 4 slides」: one claim per slide (section 6).
   When the handwriting is unclear, choose the reading that fits the story, **write the reading in the slide's note**, and
   mention it in the reply; do not ask.
3. **Workers in parallel (when a round has 30+ notes).** The lead writes `review/tasks/COMMON.md` (project facts, the workflow
   rules, the reply format) and one `TASK_X.md` per worker (`house/ipe-seminar-2026/review/tasks/`). Each worker owns a
   disjoint set of slides, **identified by beat**, and works on a private preview deck:
   `DECK_FILE=deck_a.md python3 review/make_wireframe.py` writes only `deck_a.md`; the worker renders it to `review/_a/`
   and looks at the PNGs. Workers never write `deck.md`, the sheets or the spec, never commit, and add new functions in their
   own `review/sk_a.py` (the lead adds one import line). The lead merges, runs `render.sh`, reads every changed slide, commits.
   The gain is wall-clock, and the disjoint ownership keeps the merge trivial.
4. **Reply format** (per slide, one line): what changed, and any decision or doubt about how the note was read. Short.
5. **Commit every round**, with a message that names the slides ("Split slides 5 and 10 into builds; Apoha as a 5-step
   build"). Rendered sheets and `deck.html` are committed too, so the lecturer can open them anywhere.
6. **The lecturer's corrections that recurred become rules** (HOUSE_STYLE "Update" blocks). Add the new ones there the same day.

## 4. The look that was approved

**Background.** A real washi paper scan under everything (`house/washi-scan.jpg`, the lecturer's own file, rotated and cropped
to 16:9), on the cream `#FDFBF7`. It is in `theme-house.css`: `background: #FDFBF7 url('figures/washi-scan.jpg') center / cover`.
Copy `washi-scan.jpg` into the deck's `figures/`. Two rules come with it:

- figures multiply into the paper (`section .fig img { mix-blend-mode: multiply }`), so a PNG drawn on white shows no white
  box; photos, faces and dark slides are `normal`. Forgetting the exception darkened the photo slides once (commit ff10ac5);
- dark full-bleed slides (`L-d`) have **no** paper (`background-image: none`).

A generated texture (`make_washi.py`, a PNG of noise and fibres) was tried first and replaced by the scan: it looked fake.

**Colour.** Black ink; red `#B14434` for the point; blue `#3959A6` for the second thing; greys `#6B6B6B` / `#D9D9D9` / `#EEEEEE` for
everything secondary; light blue `#8FA3D6` and light red `#D98A7C` for a third and fourth category. Black must stand out and
secondary things go grey. Frames and separator lines were *removed* in a pen round: no frames on scatter panels or the GIF,
a short dotted divider at most. Use the tokens (`RED`, `BLUE`, `GREY`, `INK`, `CREAM` in `sketch_kit.py`), not new hexes.

**Type size.** Large and few words. The sizes used (px on the 1280 x 720 canvas):

| use | size |
|---|---|
| F slide title (one sentence) | 62; a second, emphasised line 46 |
| title of other layouts | 44 bold, centred |
| body line / list item | 30-36 (lists in a split layout 40-50) |
| take under a figure | 36 bold; 46 on a `big` slide |
| handwritten label, caption, call-out (Caveat) | 30-60; grey `#6B6B6B` |
| equation | KaTeX at 1.15-2.3 em, rows labelled by a Caveat word at 44 |
| footer reference bar | 13.5 on a 26 px black bar; nothing else below 22 |

He asked for bigger on several slides in the pen rounds (「大きく」): when a slide has room, raise the size of the object under
discussion before adding anything.

**Figures as large as possible**, trimmed of white margin (`figures/trim.py`); a figure is capped by the layout CSS, not by
an inline `max-height`. Titles are sentences; most slides have no other text.

**Closing slide, photos, QR codes, footers**: as in HOUSE_STYLE (never "Thank you"; co-author photos on openers, never fetched
from the web; the QR codes are black on white, 165 px, made with `figures/make_qr.py`; get each paper's URL from him).

## 5. How figures are made

Three kinds, chosen by what the slide needs:

**(a) A hand-drawn SVG sketch** for every concept that is not data (a circle zooming to pixels, the rainbow, Apoha's Venn
diagram, tokens in a row, the Darwin map, the potential landscape). Each is a Python function that returns an `<svg>`:

- `sketch_kit.svg(w, h, body)` wraps the shapes in a **rough filter**: `feTurbulence` displaces every stroke a few pixels and
  a second noise layer lays pencil grain on non-paper pixels. This is what makes the figures look drawn, and it is the same
  look as the CCS deck's. Labels are Caveat (`t(...)`), arrows `arrow(...)`; no clip-art.
- the SVG sits in `<div class="fig sk">`; its width is set by CSS (`section .fig.sk svg { width: 100%; max-height: 560px }`),
  a `max-height` in the SVG's style picks a smaller one;
- draw it at the size it will have, put the object of the slide in red or in the largest size, everything else grey;
- two states of one picture (before, after) are two calls of the same function with a parameter (`apoha_build(k)`,
  `concept_mix(f=k/12)`), never two drawings, so nothing moves between the slides.

**(b) A real figure from the paper, the poster or the project page**, cropped to the panels that carry the point (`figures/crop_*.py`
write the crops), trimmed, and annotated with **grey call-outs**:

- `callout(cx, cy, rx, ry, [lines], tx, ty, ax, ay, size, col)` draws a hand-drawn ring around the feature, 1-3 short Caveat
  lines, and an arrow from the text to the ring's edge; `OVL(...)` lays the whole overlay over the slide in *slide pixels*
  (`position:absolute; z-index:6; pointer-events:none`). The text has a cream halo (`paint-order: stroke`) so it is readable
  over the plot.
- in the generator an `OVERLAYS` list maps a substring of the slide's `beat` to its overlay, so the call-out follows the
  slide when it moves;
- **grey** by default; red only for the slide's own claim ("more cited, more new citations"). The note says what the figure
  shows that the audience cannot see alone: "peak at about 5 years", "the most-cited papers get too many citations",
  "D2L beats every other method". Labels in a paper's figure that are not the point are re-drawn in grey (`grey_f1E.py`) rather
  than cropped away, so the figure stays recognisable.
- find the coordinates by rendering and reading the PNG; the ring must be centred on the feature, which usually takes
  two passes. State in the note what the ring marks.
- a test of a model (data vs model) gets the **name of what is tested on the slide** ("Law", "Science") and one sentence of
  interpretation, not just the plot.

**(c) A generated illustration** (PIL, matplotlib or headless Chrome) where it is needed: the emoji cluster GIF, the next-word
GIF, the collaboration benchmark re-plotted from the cluster's CSVs (`fig_collab.py`), QR codes. The script lives in
`figures/` with a docstring that names the input and the output; the deck refers only to the output file.

Rules common to all three: use existing figures first (the paper, the poster, the project page); photos only freely licensed
and credited in `ft`; the same figure on two slides always comes from the same file; no figure is added to a slide that the
spec says is text-only.

## 6. Builds are consecutive slides with identical positions

A build (a list that grows, a claim revealed, a sentence that gets its second line) is written as **n consecutive slides**, not
as Marp fragments. The hidden parts keep their space with `visibility: hidden` (`.vh`), so nothing moves between slides:

```python
for k in range(1, 5):
    rows = "".join(f'<div class="sumrow{"" if n < k else " vh"}">...</div>' for n, ... in enumerate(items))
    S("L-g", beat=f"summary ({k}/4)", body=...)
```

Used for: the 3-step text slide (question; + "Shared vocabulary?"; + the sentence), the Apoha 5-step build (one animal
excluded per step), the 4-claim summary, the two-line circle slide ("click: how do we build the imagination?"), the three
distance slides, the potential slide split into halves. Why not fragments: the PNG/PDF export and the red-pen
sheets show every step, the clicker needs one key, and the lecturer can delete one step by deleting one slide. The speaker
note of step k says "step k of n: rows 1 to k shown". Split a slide as soon as its second claim appears; he asked
for it on two dense slides (5 and 10), the summary and the distance slide.

## 7. Animation

Pick by what moves:

| what moves | asset | how |
|---|---|---|
| dots drifting together, a prediction appearing | **GIF** (`assets/anim/x.gif`) | PIL frames at 2x, downscale with LANCZOS; save `x_first.png` and `x_last.png` for QA; the static export shows the first frame, so make the first frame a readable picture |
| a screen recording (the map over 70 years) | **mp4** (H.264, `yuv420p`) | `<video src poster autoplay loop muted playsinline>`, a poster PNG for the PDF/PNG export |
| a sketch and a web page moving together | **transparent WebM** (VP9 `yuva420p`) | composite frames, then `ffmpeg ... -vf fps=15,format=yuva420p -c:v libvpx-vp9 -crf 32 -b:v 0 -auto-alt-ref 0` |

**Full-bleed video slide (`L-d`, dark).** The video sits in `.vid` (`position:absolute; top:0; height:692px`), the slide's
`bg` is the video's own background colour, and the poster is a frame of the same video. The first attempt used a colour
picked by eye (`#00103E`) and the edge of the video showed against the slide; the fix was to sample the pixel from the
poster / decoded frame (`#001C48`). Two videos side by side: `.vid2`, height 636, gap 4. Trim a clip's dead frames (a still of
the final year) before use.

**Transparent WebM recipe** (`figures/fig_slider_video.py`): the slide "take two papers, ask what lies between" needed a star that
moves from A to B *together with* a slider in a web page. (1) Make the 13 states of the page (screenshots at weight k/12) and
of the sketch (`concept_mix(f=k/12)`); (2) render each sketch with headless Chrome:
`--headless=new --default-background-color=00000000 --force-device-scale-factor=1 --window-size=W,H --virtual-time-budget=2000
--screenshot=out.png`, with the Caveat font loaded through `@font-face` on a `file://` URL; (3) alpha-composite sketch and
page per state; (4) list the frames in an ffmpeg concat file with durations (1.4 s on the two ends, 0.45 s between), play
forward and back (`0..12, 11..1`) so the loop is seamless; (5) encode; (6) save the middle state as the poster.
The transparent video lets the washi show through, which an mp4 cannot.

**Playback.** The PDF and PNG exports show posters only. Export `deck.html` for every round and for the talk itself:
`marp deck.md --theme-set theme.css --html --allow-local-files --no-stdin -o deck.html < /dev/null`. It refers to `assets/`
and `figures/` by relative path, so it works only next to them. Commit it.

Check animations by playing `deck.html` in the browser, not by the PNGs.

**Sending the deck to someone else: one self-contained HTML** (`review/build_standalone.py`, snapshot in `house/ipe-seminar-2026/`).
It renders `deck.md`, then embeds every image, video, poster, the paper texture, Libre Baskerville, Caveat and the KaTeX fonts as
`data:` URIs (fonts are downloaded once into `assets/fonts/embed/` and reused, so a rebuild works offline). Details that matter:
- the plain `deck.html` still loads fonts from Google and jsdelivr, so it breaks offline and on a machine without the fonts;
- **speaker notes are emptied by default**: they hold the red-pen working notes ("Your note: ...") and local file paths; `--keep-notes` for a private copy;
- big opaque PNGs are re-encoded as JPEG (4:4:4, q90, at most 1800 px wide): 20 MB of assets stay about 15 MB; a figure that
  repeats on the slides of a build is stored once and put back by a ten-line script (31.9 MB became 21.9 MB);
- test it by copying the file alone into an empty folder and screenshotting slides with headless Chrome and
  `--host-resolver-rules="MAP * ~NOTFOUND"` (no network); open a video slide, a math slide and the title.
- 22 MB is too large for most e-mail (the attachment is base64 again); send a link (Drive, a web server) or a zip.
Keep the output out of git (`deck-standalone.html` in `.gitignore`).

## 8. Mechanics that cost time

- `marp` needs `--html` (inline `style=` and `<video>` are dropped otherwise), `--allow-local-files`, `--no-stdin < /dev/null`
  when run in the background, and an output path inside the working directory.
- Several workers editing one generator: the Edit tool refuses a stale file; re-read it. Give each worker its own `sk_X.py`.
- Large rendered PNGs and per-worker preview decks go in `.gitignore` (`review/_r/`, `deck_a.md`, `assets/ccm/*.png`); the
  sheets, `deck.html` and the assets the deck needs are tracked.
- A figure that is already on a washi-like background must be trimmed and multiplied; a dark slide must not be multiplied.
- Keep a footer on every slide of a part that reports a paper, and none on the openers and the close.
- An unpublished part (Gravity of Ideas, Doc2LoRA): high level only, no final numbers; say so in the opener's note.

## 9. Before showing a round to the lecturer

1. Rebuild (`render.sh`), look at **every** changed slide's PNG, then the sheets' first page.
2. No text over the footer bar, nothing overlapping, no figure with a white box on the paper.
3. Each note records how a red-pen note was read.
4. The spec's "Settled" and "Still open" lists are updated.
5. `deck.html` re-exported and the videos play.
6. Commit and push with a message that names the slides.

Then a short Japanese report: what changed per slide, what was a judgment call, what is still open.
