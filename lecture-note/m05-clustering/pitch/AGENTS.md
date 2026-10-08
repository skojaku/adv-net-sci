# M05 pitch: from a hand-drawn seating chart to `seats.csv`

What this directory is: a class activity in which 4 groups pitch a community partition of
the class's own seating network. Students open `pitch-seats.ipynb` (QR code on
`pitch-sheet.pdf`). The notebook reads `seats.csv` from a fixed GitHub address. This file is
the procedure for turning the lecturer's paper into that `seats.csv`. Read it before touching
anything here.

## Files

| File | What it is |
|---|---|
| `seats.csv` | `id,x,y`, one row per person. **The only file that changes in class.** Row `i` is node `i` in the notebook. |
| `seats-example.csv` | An invented 15-person room, for rehearsal. Do not delete. |
| `pitch-seats.ipynb` | The student notebook. **Generated** by `tools/build_m05_pitch_notebook.py`; never edit by hand. |
| `pitch-sheet.tex` / `.pdf` | The one two-sided handout. The PDF is not committed (`*.pdf` is gitignored). |
| `pitch-seats-qr.png` | The QR code on the sheet. It encodes the Colab URL of this notebook on `main`. |
| `read_seats.py` | Photo of hand-drawn circles to `seats.csv` and an overlay to check by eye. |
| `exact_cuts.py` | Exact best two-way split by brute force (the lecturer's answer key for group 2). |
| `pitch.py`, `lecture-hall.css`, `m05pitch-qr.png` | The earlier karate-club version (marimo). Not used. |

## Steps

### 1. Get the photo

Ask the lecturer for a photo of the paper (give them the tips below) and for its path.

- Dark pen on white paper, one circle per person, roughly the same size, none touching.
- No numbers or writing inside or next to the circles. Words elsewhere on the page are
  tolerated (they are rejected by size) but a word next to a circle is not.
- Straight from above. The front of the room is at the top of the picture.

### 2. Read the circles

```sh
cd lecture-note/m05-clustering/pitch
uv run read_seats.py /path/to/photo.jpg seats.csv overlay.png
```

It thresholds the ink locally (shadows are fine), takes each closed shape as a circle if
its area is within 0.4 to 2.2 times the median and it is round enough, and writes the
centres. Coordinates are scaled so that the usual distance to a nearest neighbour is 1,
and `y` points up, so the picture in the notebook has the same orientation as the paper.
Ids are `A, B, C, ...` from left to right.

The k-nearest-neighbour graph depends only on who is nearer than whom, so the scale does not
matter. The ids are not names. Keep them anonymous: the repository is public.

### 3. Check the overlay by eye

Open `overlay.png` with the Read tool. Blue dots with letters are accepted circles; shapes
outlined in red were rejected. Count the circles on the paper and compare:

- A circle missing: it was probably open (a gap too wide), touching a neighbour, or much
  smaller or larger than the rest. Fix `seats.csv` by hand, or ask the lecturer to redraw.
- A dot where there is no circle: delete that row.
- Two circles merged: split by hand.

Do not push a `seats.csv` whose count you have not compared with the paper. Report the count
to the lecturer ("17 circles found, you said 17 students").

`overlay.png` is a check, not a deliverable. Do not commit it (it contains a photo of the
classroom).

### 4. Look at the network and choose K

Row order is node order: `labels[i]` in the notebook is the group of row `i`.

K is a variable in the notebook, so students may change it. The generator sets its starting
value (`--k`, default 3). Check what K = 2 and K = 3 do on the real room:

```sh
uv run exact_cuts.py seats.csv 3
uv run exact_cuts.py seats.csv 2
```

K = 2 can leave the network in pieces; then the best cut is 0 (put a piece on either side),
which is a fact worth telling the lecturer. Keep the default 3 unless the lecturer says
otherwise. `exact_cuts.py` prints the exact smallest Ratio cut and Normalized cut: that is
the answer key for group 2. Tell the lecturer; do not put it in the notebook or on the sheet.

### 5. Publish

```sh
git add seats.csv
git commit -m "m05 pitch: the class's seats"
git push
```

The course's CLAUDE.md says to commit and push after an edit. GitHub's raw address caches for
up to 5 minutes. Check that the notebook will see the new file:

```sh
curl -s https://raw.githubusercontent.com/skojaku/adv-net-sci/<branch>/lecture-note/m05-clustering/pitch/seats.csv | head
```

`<branch>` is `main`: the notebook was generated with `--branch main` (the name is in its `SEATS_URL`).
If you ever move the activity to another branch, regenerate with
`python tools/build_m05_pitch_notebook.py --branch <branch>` and rebuild the QR code (below).

### 6. Test it the way a student sees it

Open the Colab link printed by `python tools/build_m05_pitch_notebook.py`. Run Setup and
check that the first line says the right number of people and that the "REHEARSAL DATA"
banner is **absent**. (The banner appears only when `seats.csv` cannot be read; the invented
test room is not flagged, so look at the picture: it must be the lecturer's room.)

To test without Colab, the notebook runs in any Jupyter with `python-igraph`, `numpy`,
`pandas`, `matplotlib`. Replace `SEATS_URL` by a `file://` path in a copy, never in the
generated file.

## If the branch or the notebook changes

- `python tools/build_m05_pitch_notebook.py [--branch main] [--k 3]` rewrites the notebook.
  The QR code on the sheet encodes the Colab URL it prints, so rebuild the QR when the branch
  changes:

  ```sh
  uvx --from segno segno --output=pitch-seats-qr.png --scale=14 --border=4 --error=l "<the Colab URL>"
  uvx --with opencv-python-headless --with numpy python -c "
  import cv2; print(cv2.QRCodeDetector().detectAndDecode(cv2.imread('pitch-seats-qr.png'))[0])"
  xelatex -interaction=nonstopmode pitch-sheet.tex   # twice
  ```

  Check what the second command prints, not that the file exists. A short link would make
  the QR smaller and survive branch changes; it needs a line in the Caddy config on the
  course droplet (`LAB_NOTEBOOK_GUIDE.md`, "Getting a room full of people into it"). That
  is the lecturer's server: ask first.
- Code on the sheet (boxes 3 and 4) is code that was run against the notebook's `show`,
  `graph` and `graph_tool`. If you rename any of them, change the sheet and run the sheet's
  code again.

## Facts worth knowing

- graph-tool has no Windows build. Group 4 installs it on first use (1 to 3 minutes) into a
  temp folder and runs it in its own process; condacolab is not used because it only works
  in Colab. Windows students should use Colab.
- On a 15-node network graph-tool often answers "one group" (the description length does not
  justify more). That is the method working as designed, and the sheet tells group 4 to
  force `B_min = B_max = 2` if they want two. Do not "fix" it.
- Not tested on Colab as of the last edit to this file: the whole notebook, including
  group 4's graph-tool install. Everything else was run end to end locally.
