#!/usr/bin/env python3
"""Build the m01 molab lab notebook from its template.

The notebook is uploaded to molab as a single file and is opened by students
in a lecture hall, so it cannot fetch anything at run time. This script welds
the two things it needs into the file itself, base64-encoded so no quoting or
backslash in the CSS or the JavaScript can break the Python source:

  * the Pair Notebook look  -- notebooks/assets/lecture-hall.css, a vendored
    copy of adv-net-sci-ops/pair-notebook/m01-euler-tour/lecture-hall.css;

  * the walk/trail/path visual -- the same route-namer the m01 deck mounts,
    assembled from lecture-note/assets/anim.{css,js},
    lecture-note/assets/anim/route-namer.js and the #route-namer rules out of
    slides/m01/network-science.css, into one self-contained page.

Run it after touching any of those, or after editing the template:

    python tools/build_m01_lab.py

To refresh the vendored CSS:

    cp ~/Documents/teaching/adv-net-sci-ops/pair-notebook/m01-euler-tour/\
lecture-hall.css notebooks/assets/lecture-hall.css
"""

from __future__ import annotations

import base64
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

TEMPLATE = ROOT / "notebooks/m01-euler-tour/lab.template.py"
OUTPUT = ROOT / "notebooks/m01-euler-tour/pen-and-paper-lab.py"

LECTURE_HALL = ROOT / "notebooks/assets/lecture-hall.css"
ANIM_CSS = ROOT / "lecture-note/assets/anim.css"
ANIM_JS = ROOT / "lecture-note/assets/anim.js"
SCENES_JS = ROOT / "lecture-note/assets/anim/route-namer.js"
DECK_CSS = ROOT / "slides/m01/network-science.css"

STAGE_ID = "route-namer"


def rules_for(css: str, needle: str) -> str:
    """Return every top-level rule whose selector mentions `needle`.

    A hand-rolled scan rather than a CSS parser: walk the text, track brace
    depth, and cut a block whenever depth returns to zero. `@keyframes` nests,
    which is exactly why depth is tracked instead of splitting on '}'.
    """
    out, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                block = css[start : i + 1]
                selector = block.split("{", 1)[0]
                if needle in selector or (
                    selector.lstrip().startswith("@keyframes")
                    and selector.split()[-1].startswith("rn-")
                ):
                    out.append(block.strip())
                start = i + 1
    # The deck scopes every stage under `section`; the notebook iframe has no
    # such wrapper, so drop it.
    return "\n".join(r.replace("section #", "#") for r in out)


SKELETON = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
/* The lab page's paper, so the stage does not look pasted on. Tokens are the
   Pair Notebook's (lecture-hall.css), not repeated here beyond these three. */
html, body {{ margin: 0; padding: 0; background: #FFFDF7; }}
body {{
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue",
               "Noto Sans", Arial, sans-serif;
  color: #1D1E21;
  padding: 4px 6px 10px;
}}
/* --- shared animation kit ------------------------------------------- */
{anim_css}
/* --- this stage only ------------------------------------------------ */
{stage_css}
</style>
</head>
<body>

<figure class="anim-stage" id="{stage_id}">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">&#9664;</button>
    <button class="anim-btn" type="button" data-anim-play>&#9208; Pause</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">&#9654;</button>
    <button class="anim-btn" type="button" data-anim-replay>&#8635; Replay</button>
  </div>
  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-rn-map></div>
    <div data-anim-clear data-rn-side></div>
  </div>
  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script>
{scenes_js}
</script>
<script>
{anim_js}
</script>
</body>
</html>
"""


def main() -> int:
    missing = [p for p in (TEMPLATE, LECTURE_HALL, ANIM_CSS, ANIM_JS, SCENES_JS, DECK_CSS)
               if not p.exists()]
    if missing:
        for p in missing:
            print(f"missing: {p.relative_to(ROOT)}", file=sys.stderr)
        return 1

    stage_css = rules_for(DECK_CSS.read_text(), f"#{STAGE_ID}")
    if not stage_css:
        print(f"no CSS found for #{STAGE_ID} in {DECK_CSS.name}", file=sys.stderr)
        return 1

    page = SKELETON.format(
        anim_css=ANIM_CSS.read_text(),
        stage_css=stage_css,
        stage_id=STAGE_ID,
        scenes_js=SCENES_JS.read_text(),
        anim_js=ANIM_JS.read_text(),
    )

    def b64(text: str) -> str:
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    built = TEMPLATE.read_text()
    for marker, payload in (
        ("%%LECTURE_HALL_CSS_B64%%", b64(LECTURE_HALL.read_text())),
        ("%%ANIM_HTML_B64%%", b64(page)),
    ):
        if marker not in built:
            print(f"marker {marker} not in template", file=sys.stderr)
            return 1
        built = built.replace(marker, payload)

    header = (
        "# BUILT FILE -- do not edit.\n"
        "# Source: notebooks/m01-euler-tour/lab.template.py\n"
        "# Rebuild: python tools/build_m01_lab.py\n"
    )
    # The template carries its own build note; the built file gets a shorter one
    # at the very top, after the inline script metadata block that uv reads.
    lines = built.splitlines(keepends=True)
    end_of_meta = max(i for i, ln in enumerate(lines[:40]) if ln.startswith("# ///")) + 1
    built = "".join(lines[:end_of_meta]) + header + "".join(lines[end_of_meta:])

    OUTPUT.write_text(built)
    print(f"wrote {OUTPUT.relative_to(ROOT)}  ({len(built) / 1024:.0f} KB)")
    print(f"  stage css : {len(stage_css.splitlines())} lines from {DECK_CSS.name}")
    print(f"  page      : {len(page) / 1024:.0f} KB inlined")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
