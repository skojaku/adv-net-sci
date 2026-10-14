#!/usr/bin/env python3
"""Magic-move trial: one 11-node network, three slides, the discs resize and recolour between slides.

    python3 morph-demo/build.py     # writes morph-demo/morph-demo.md and morph-demo.html

Each disc carries a fixed view-transition-name (n_E, n_F, ...). Marp CLI's bespoke template runs
document.startViewTransition between slides, so the browser moves and resizes every disc that has
the same name on both slides. Labels and edges never change, so they are not named.
Needs a Chromium-based browser; the PDF/PPTX exports show three still slides.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "figures"))
import smallgraphs as sg  # noqa: E402

G, XY = sg.CA, sg.CA_XY
ORDER = sorted(G)
X0, Y0, SX, SY = 40, 330, 150, 90           # grid units -> px (y flips)
W, H = 1080, 320
BLUE, RED, INK = "#3959A6", "#B14434", "#222222"


def px(u):
    x, y = XY[u]
    return X0 + x * SX, Y0 - y * SY


MEASURES = [
    ("Degree", "How many neighbours?", {u: float(G.degree(u)) for u in G},
     "E has five neighbours and wins."),
    ("Closeness", "How near is everyone?", {u: float(v) for u, v in sg.closeness(G).items()},
     "F, with two neighbours, takes the crown."),
    ("Betweenness", "How many shortest paths pass through?", {u: float(v) for u, v in sg.betweenness(G).items()},
     "E again. F and G tie for second, at 25."),
]


def svg(vals):
    lo, hi = min(vals.values()), max(vals.values())
    winner = max(vals, key=vals.get)
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">']
    for e in G.edges():
        (x1, y1), (x2, y2) = px(e[0]), px(e[1])
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#555" stroke-width="3"/>')
    for u in ORDER:
        x, y = px(u)
        r = 12 + 22 * (vals[u] - lo) / (hi - lo)
        fill = RED if u == winner else BLUE
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{fill}" fill-opacity=".85" '
                   f'stroke="{INK}" stroke-width="2.5" style="view-transition-name:n_{u}"/>')
    for u in ORDER:
        x, y = px(u)
        out.append(f'<text x="{x:.0f}" y="{y + 7:.0f}" text-anchor="middle" font-size="20" '
                   f'font-weight="700" fill="#fff" stroke="{INK}" stroke-width=".6">{u}</text>')
    out.append("</svg>")
    return "\n".join(out)


md = ["""---
marp: true
theme: network-science
transition: fade
---

<style>
::view-transition-group(*) { animation-duration: .8s; animation-timing-function: ease-in-out; }
</style>
"""]
for i, (name, q, vals, line) in enumerate(MEASURES):
    if i:
        md.append("\n---\n")
    md.append(f"## {name}\n\n<hr>\n\n{q} Disc size is the score, rescaled from the smallest to the largest.\n\n"
              f'<div class="fig">\n\n{svg(vals)}\n\n</div>\n\n<div class="cue">\n\n*{line}*\n\n</div>\n')
(HERE / "morph-demo.md").write_text("\n".join(md))

subprocess.run(["marp", "--no-stdin", "--html", "--theme", str(HERE.parent / "network-science.css"),
                "--allow-local-files", str(HERE / "morph-demo.md"), "-o", str(HERE / "morph-demo.html")],
               check=True)
