#!/bin/sh
# Render every slide to review/_r/wf.NNN.png and build the red-pen sheets.
cd "$(dirname "$0")/.." || exit 1
# figures/*.png are not committed: restore the ones the deck needs
[ -f figures/m06-decomp-sum.png ] || cp ../m06/figures/decomp-sum.png figures/m06-decomp-sum.png
[ -f figures/grain.png ] || cp ~/.claude/skills/slide/house/grain.png figures/grain.png
python3 review/make_wireframe.py &&
mkdir -p review/_r && rm -f review/_r/wf.*.png &&
/opt/homebrew/bin/marp deck.md --theme-set theme.css --html --allow-local-files --no-stdin --images png --image-scale "${1:-1}" -o review/_r/wf.png < /dev/null 2>&1 | tail -1 &&
python3 review/make_sheets.py
