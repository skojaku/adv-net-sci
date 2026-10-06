# Remotion deck guide

How to build an **animated, click-through concept deck** in Remotion (the Module 05 deck in `slides/m05/remotion/` is the worked example:
41 slides, about 120 stages). The Marp decks (`DECK_BUILD_GUIDE.md`) stay the main teaching decks; this is for the few ideas that a
picture has to *move* to explain (a matrix turning, nodes flowing into a table, a formula built up line by line). The judgment files
(`SLIDE_RUBRIC.md`, `FIGURE_GUIDE.md`) still apply to every slide. Written so that any agent can follow it: shell commands and file paths only.

Files that live next to the code: `slides/m05/remotion/DECK_SPEC.md` (the plan, one table per slide, and the numbers that were checked),
`BUILD_NOTES.md` (how to build and run), `README.md`. The narrated video made from the deck is in `NARRATED_VIDEO_GUIDE.md`.

## Use model

- The lecturer clicks. A slide has **stages**; one click plays one stage and stops. `export const marks = [48, 108, ...]` in every
  slide file: `marks[i]` is the frame where stage `i` is finished. Stage 0 starts at frame 0 and plays when the slide opens.
- **The last frame of a stage is the complete picture** (going back lands on it). Everything a stage adds is done by its mark.
- A slide is a **pure function of the frame** (`useCurrentFrame()`): no `Date`, no `Math.random`, no React state. That is what makes
  stills, reverse playback (the app plays back at 2x) and video export work. Randomness is generated once, in `scripts/make_data.py`.
- Telegraphic text, density from motion: one short caption per stage at most, name the unit (pairs of nodes, or nodes), a question
  slide carries **no answer**. The lecturer says the rest.

## Order of work that succeeded

1. **Propose in a table first** (`DECK_SPEC.md`): per slide and stage, what appears and what picture is left at the end. Get the
   lecturer's yes before drawing anything.
2. **Numbers before pictures.** `scripts/make_data.py` writes `src/data/data.ts` (graphs, seeds, shuffles); `scripts/verify_numbers.py`
   recomputes every number that is quoted on a slide and asserts it. A number on a slide that no script computed is a bug. Standard
   library only where possible (`scripts/verify_dcsbm.py`), so it runs without a venv.
3. Build the slides with the shared parts (below). One slide per file `src/slides/S01.tsx ...`, registered in `src/slides/index.ts`
   (`{n, id, marks, Component}`); `TOTAL` in `src/components/Frame.tsx` is the slide count.
4. `npm run review`: a still at the end of every stage (`out/review/S12-s3.png`), plus `index.html`. **Look at every still.** Then
   `python3 scripts/check_bottom.py`.
5. Iterate with the lecturer's remarks; commit after every round (only `slides/m05/remotion`).
6. Update `DECK_SPEC.md` rows when a slide changes: it goes stale fast.

## Writing a slide (the parts)

- `Frame` (`src/components/Frame.tsx`): page number, and an optional `title` (normally none). Without a title the content, laid out
  for a canvas with a heading (content region x 120 to 1800, y 190 to 990), is moved up and enlarged: `zoom` (default 1.08) and `top`
  (the layout y that lands at y = 50). **The band below y = 920 stays empty** for subtitles and the narrator; `check_bottom.py`
  fails a still that reaches below it or comes within 40 px of an edge. A slide with room takes a bigger `zoom`, a crowded one a smaller one.
- Helpers in `src/lib/anim.ts`: `prog` (ease-out 0 to 1 between two frames), `smooth` (ease-in-out), `stageStart(marks, i)`,
  `betweenStages`, `fromStage`. `Fade` (a full-canvas layer with opacity and slide-up), `Canvas` (an SVG layer), `Box`, `Cap` (grey
  handwriting), `Tag`, `Term` (red bold) in `src/components/`.
- **Formulas build up one at a time** (`src/components/FormulaStack.tsx`): row `k` appears in stage `k`, the newest group is large
  (about 50 px) and older ones smaller (40 px), no marker bar, nothing is ever deleted (move formulas aside, shrink them). Rows of one
  `group` change size together, so an aligned `=` stays aligned (`\phantom{LEFT SIDE}=...`). `note` puts grey definitions under a row.
  If the formulas do not fit, shrink or dock them; **never remove one**.
- Math is KaTeX (`src/components/Tex.tsx`). Inline `aligned` is display style: put `\textstyle` in each cell for a small sum.
- **Continuity across the cut**: a slide that follows another opens on the picture the other ends with (same coordinates; use a shared
  constant, e.g. `G_ARI` in `src/lib/eight.tsx`), and the first slide's end state is a `Frame` with the same `zoom` and `top`, or the
  zoom eases between the two. A table that appears at frame 0 of the next slide must not fade in.
- Pictures from a paper or a file: put them in `src/assets/` and `import png from '../assets/x.png'`, then `<Img src={png} />`.
  (Not `public/` + `staticFile`: the single-file build cannot inline those.)
- Simulate nothing at run time: a diagram of a random process uses seeds fixed in `data.ts` and "10 tickets, draw one", never a random number.

## Style decided by the lecturer (treat as final)

Few words. No em dash. No rhetoric (no "pay for themselves", no build-up; plain sentences; one idea per sentence). Name the unit.
**Red (#B14434) is for emphasised text only**: never a fill, a group colour or a line (a black cross, not a red one, marks "disagree").
Groups are told apart by hue: blue, orange, brown, purple, dark grey; brown stripes only for bands and overlaps. No green. No bar charts
(dot plots instead). Never draw a pair of nodes as two nodes joined by a line (it reads as an edge): use cells of a matrix. Draw full
matrices, diagonal included. Use "description length", not "Bayesian score". Show two partitions of one network side by side so they
can be compared. Give formulas incrementally and **do not give a parameter before it is derived** (p_rs is not given first). A figure
taken from a paper is credited on the slide. Figure tools: TikZ / Altair / seaborn, not matplotlib (`FIGURE_GUIDE.md`).

## Review tools

- `npm run review`: stills of every stage (`out/review/`), `index.html` (full size) and `artifact.html` (self-contained, half size,
  to share). Delete `out/review/S*-s*.*` first when stage counts shrank, or old stills linger.
- `node scripts/frames.mjs <composition id> 0,30,60 <dir>`: frames between the stage ends, for judging an animation.
- Contact sheets (many stills on one image with Pillow) make a 41-slide pass quick; add a guide line at y = 920 to see the free band.
- A keyboard smoke test: start `npx vite --port 5199`, drive headless Chrome over the DevTools protocol (the binary is
  `node_modules/.remotion/chrome-headless-shell/<platform>/.../chrome-headless-shell` after the first render), send ArrowRight/ArrowLeft,
  read the "slide n/N" label, collect console errors.

## Single html file for students

`npm run build:single` writes `out/m05-community-detection.html` (about 2.3 MB, opens from the file system, no network). See `BUILD_NOTES.md`:
fonts from `@fontsource` (woff2 only), KaTeX woff2 only, images imported, one script and one stylesheet pasted into the html. Test it
with headless Chrome on a `file://` URL: fonts loaded, picture shown, no request leaves the file. Rebuild after every change (`out/` is not committed).

## Where it trips (collected the hard way)

- **zsh does not split unquoted variables**: `set -- $spec`, `for x in $list` silently do nothing. Write explicit commands, a `for` over
  literal words, or `${=var}`.
- **macOS sed**: `sed -i 's/a/b/' file` takes the script as the backup suffix and fails; use `sed -i '' ...` or edit with Python. There is
  no `timeout` command either.
- **Case-insensitive file system**: `Narration.tsx` and `narration.ts` are one file to macOS and TypeScript reports TS1149. Name
  components and data files differently.
- **Copying a project**: `rsync --exclude dist` also removes `node_modules/*/dist` and breaks every package. Copy without `node_modules`
  and run `npm install`.
- **Remotion basics**: `useCurrentFrame()` is relative to the nearest `Sequence`; a `Sequence` with a negative `from` starts its child in the middle
  of its animation; `Freeze` holds one frame. `staticFile` needs a `public/` folder. `npx remotion ffmpeg` and `ffprobe` are bundled: no system ffmpeg.
- **The browser-automation tools time out** on this app; use headless Chrome over the DevTools protocol (a 60-line node script) instead.
- **KaTeX fonts**: the css lists woff2, woff and ttf and a naive inline triples the file. The hand font (Caveat) has no Greek and no
  combining hat: write symbols with `Tex` or in the serif face.
- **networkx karate club carries edge weights**: `nx.community.modularity` uses them by default (Q = 0.434 instead of 0.407); pass `weight=None`.
- **Numbers from a paper**: read the PDF (`pdftotext`, or `pdftoppm` and look at the page); a web fetch tool cannot read a PDF. The printed Eqs. (17), (21) and (23)
  of Karrer and Newman are twice the log-likelihood used on the slides (their Eq. 16 gives the factor 1/2); the maximizing c is the same.
- Stale `out/review` stills, stale `DECK_SPEC.md` rows, and a slide whose `marks` changed (the video's timeline and audio then change too) are the usual
  sources of "it looked right yesterday".
