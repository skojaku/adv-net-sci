#!/usr/bin/env bash
# Render the PDF / PNG review of the deck with the animations frozen on one frame.
# Marp's PDF and PNG export do not load an <iframe>, so this builds a copy of the deck in which every iframe
# is replaced by a screenshot (headless Chrome, ?still=N) of the same page, renders it, and removes the copy.
#   figures/render_print.sh pdf|png        (run from slides/m08)
set -euo pipefail
mode="${1:-pdf}"
here="$(pwd)"
tmp="m08-embedding-print.md"
CH="${SLIDE_MATH_CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
python3 - "$here" "$tmp" "$CH" <<'PY'
import re, subprocess, sys
here, tmp, ch = sys.argv[1:4]
s = open("m08-embedding.md").read()
still = {"skipgram": "?still=240", "growth": "?still=60", "reconstruct": ""}
def shot(m):
    name, w, h = m.group(1), int(m.group(2)), int(m.group(3))
    out = f"{here}/figures/still-{name}.png"
    subprocess.run([ch, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}", "--virtual-time-budget=3000",
                    f"--screenshot={out}", f"file://{here}/anim/{name}.html{still[name]}"], check=True, capture_output=True)
    return f"\n\n![w:{w}](figures/still-{name}.png)\n\n"
s = re.sub(r'<iframe class="anim" src="anim/(\w+)\.html" width="(\d+)" height="(\d+)"></iframe>', shot, s)
open(tmp, "w").write(s)
PY
trap 'rm -f "$tmp"' EXIT
~/.claude/skills/slide-math/tools/render.sh "$tmp" "$mode"
if [ "$mode" = pdf ]; then mv -f m08-embedding-print.pdf m08-embedding.pdf; fi
if [ "$mode" = png ]; then
  for f in review/png/m08-embedding-print.*.png; do mv -f "$f" "${f/-print/}"; done
fi
