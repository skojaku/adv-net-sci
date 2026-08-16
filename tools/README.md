# Build tooling

Everything here turns source in this repo into something the lecture note or
the slides need. Nothing here touches student repositories, Classroom, or
grades — that tooling lives in the private `adv-net-sci-ops` repo.

| Script | What it does |
|--------|--------------|
| `build_figures.sh` | Runs `lecture-note/figs/src/*.py` to produce `lecture-note/figs/*.svg`. The `.svg` are **not** committed, so run this before `quarto render`. |
| `make_handson_pages.py` | Generates the hands-on pages in the lecture note from the notebooks. |
| `qmd_code.py` | Extracts code blocks out of `.qmd` sources. |
| `add_deps_header.py` | Writes the dependency header into a notebook. |
| `figures-requirements.txt` | The small package subset `build_figures.sh` needs — not the full course environment. |

```sh
python3 -m pip install -r tools/figures-requirements.txt
bash tools/build_figures.sh
quarto render lecture-note
```
