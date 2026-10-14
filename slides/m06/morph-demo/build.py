#!/usr/bin/env python3
"""Magic-move trial: one 11-node network, five slides. Discs resize and recolour (1-3, 4),
then the network splits and the two pieces slide apart (5).

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

G = sg.CA
ORDER = sorted(G)
X0, Y0, SX, SY = 40, 345, 150, 90           # grid units -> px (y flips)
W, H = 1080, 335
BLUE, RED, INK = "#3959A6", "#B14434", "#222222"

# Slide 5: the road E-F closes and the pieces drift apart (left piece west, right piece east).
XY = dict(sg.CA_XY)
XY_APART = {u: (x - 0.35, y) if u in "ABCDE" else (x + 0.6, y) for u, (x, y) in XY.items()}


def vals(d):
    return {u: float(v) for u, v in d.items()}


# (title, question, graph, positions, scores, size scale, one-line cue, transition directive)
#  size scale: None = smallest..largest on this slide, number = score / number (shared across slides)
SLIDES = [
    ("Degree", "How many neighbours?", G, XY, vals({u: G.degree(u) for u in G}), None,
     "E has five neighbours and wins.", "fade"),
    ("Closeness", "How near is everyone?", G, XY, vals(sg.closeness(G)), None,
     "F, with two neighbours, takes the crown.", "fade"),
    ("Betweenness", "How many shortest paths pass through?", G, XY, vals(sg.betweenness(G)), None,
     "E again. F and G tie for second, at 25.", "fade"),
    ("Harmonic", "Add 1/distance over everyone. Size is the score on one common scale.", G, XY,
     vals(sg.harmonic(G)), 6.75, "E wins, 6.75.", "fade"),
    ("The road E\u2013F closes", "The two pieces drift apart, and every score drops.", sg.CA_CUT, XY_APART,
     vals(sg.harmonic(sg.CA_CUT)), 6.75, "G takes over, 4.5. The discs slide; the closed road fades.",
     "fade 1.6s"),
]


def svg(graph, xy, sc, scale):
    def px(u):
        x, y = xy[u]
        return X0 + x * SX, Y0 - y * SY

    lo, hi = min(sc.values()), max(sc.values())
    winner = max(sc, key=sc.get)
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">']
    for a, b in sorted(tuple(sorted(e)) for e in graph.edges()):
        (x1, y1), (x2, y2) = px(a), px(b)
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#555" '
                   f'stroke-width="3" style="view-transition-name:e_{a}{b}"/>')
    for u in ORDER:
        x, y = px(u)
        r = 8 + 26 * sc[u] / scale if scale else 12 + 22 * (sc[u] - lo) / (hi - lo)
        fill = RED if u == winner else BLUE
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{fill}" fill-opacity=".85" '
                   f'stroke="{INK}" stroke-width="2.5" style="view-transition-name:n_{u}"/>')
        out.append(f'<text x="{x:.0f}" y="{y + 7:.0f}" text-anchor="middle" font-size="20" '
                   f'font-weight="700" fill="#fff" stroke="{INK}" stroke-width=".6" '
                   f'style="view-transition-name:t_{u}">{u}</text>')
    out.append("</svg>")
    return "\n".join(out)


md = ["""---
marp: true
theme: network-science
transition: fade
---

<style>
/* 0.8s unless the slide's own `transition: fade 1.6s` asks for longer; Marp exposes it as this variable (-1s when unset) */\n::view-transition-group(*) { animation-duration: max(.8s, var(--marp-bespoke-transition-animation-duration)); animation-timing-function: ease-in-out; }
</style>
"""]
for i, (name, q, graph, xy, sc, scale, line, trans) in enumerate(SLIDES):
    if i:
        md.append("\n---\n")
    md.append(f"<!-- _transition: {trans} -->\n")
    md.append(f"## {name}\n\n<hr>\n\n{q}" + (" Disc size is the score, rescaled from the smallest to the largest." if not scale else "")
              + f'\n\n<div class="fig">\n\n{svg(graph, xy, sc, scale)}\n\n</div>\n\n<div class="cue">\n\n*{line}*\n\n</div>\n')
(HERE / "morph-demo.md").write_text("\n".join(md))

subprocess.run(["marp", "--no-stdin", "--html", "--theme", str(HERE.parent / "network-science.css"),
                "--allow-local-files", str(HERE / "morph-demo.md"), "-o", str(HERE / "morph-demo.html")],
               check=True)
