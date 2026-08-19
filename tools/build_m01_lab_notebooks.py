#!/usr/bin/env python3
"""Weld the stylesheet into the m01 lab notebook, then write the worked copy.

    python tools/build_m01_lab_notebooks.py

Two jobs, both of which keep a generated thing next to the thing it is
generated from:

  * lecture-hall.css goes into lab.py as base64. The notebook is uploaded to
    molab on its own, and molab ignores a notebook's css_file setting
    (marimo-team/marimo#8467), so the only stylesheet that survives the trip
    is one the file carries itself.

  * lab-solutions.py is lab.py with every blank filled in. Each answer is
    anchored to text that must appear in lab.py exactly once, so a blank that
    moves, or a hint that gets reworded, stops this script rather than quietly
    leaving the answer copy a version behind.

Run it after editing either lab.py or lecture-hall.css, and commit what it
touches together.
"""

from __future__ import annotations

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPER = ROOT / "lecture-note/m01-euler_tour/pen-and-paper"
LAB = PAPER / "lab.py"
CSS = PAPER / "lecture-hall.css"
OUT = PAPER / "lab-solutions.py"

CSS_LINE = re.compile(r'^(\s*LECTURE_HALL_CSS_B64 = )".*"(  # BUILT)$', re.MULTILINE)

BANNER = """#
# GENERATED FILE -- do not edit. Run
#
#     python tools/build_m01_lab_notebooks.py
#
# which fills in every blank of lab.py and writes this. The student's copy is
# lab.py; edit that one.
"""

SUBSTITUTIONS = [
    # The seven roads, read off the map.
    (
        """    ROADS = [
        (0, 1),  # NY-13, Ithaca -- Syracuse
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
    ]""",
        """    ROADS = [
        (0, 1),  # NY-13, Ithaca -- Syracuse
        (0, 1),  # NY-34, Ithaca -- Syracuse, the other way round
        (0, 2),  # NY-79, Ithaca -- Binghamton
        (1, 2),  # I-81,  Syracuse -- Binghamton
        (1, 3),  # I-90,  Syracuse -- Albany
        (2, 3),  # I-88,  Binghamton -- Albany
        (2, 3),  # NY-7,  Binghamton -- Albany, the other way round
    ]""",
    ),
    # Add, do not set, and fill both cells of the mirror.
    (
        """    for i, j in edges:
        ...  # TASK
        ...  # TASK
    return A""",
        """    for i, j in edges:
        A[i, j] += 1
        A[j, i] += 1
    return A""",
    ),
    # Degree is a row, added up.
    (
        '''    TASK: one line, no loop. Every road at city i left a count somewhere in
    row i.
    """
    ...''',
        '''    One line, no loop: every road at city i left a count somewhere in row i.
    """
    return np.asarray(A).sum(axis=1)''',
    ),
    # Connectivity first, then parity.
    (
        '''    TASK: the rule is the table above. The two things you have are
    `degrees(A)` and `is_connected(A)`.
    """
    ...''',
        '''    Connectivity first, then the parity of the odd count: a map in two
    pieces has no tour however even every one of its degrees is.
    """
    if not is_connected(A):
        return "impossible"
    odd = int(np.sum(np.asarray(degrees(A)) % 2 == 1))
    if odd == 0:
        return "circuit"
    if odd == 2:
        return "path"
    return "impossible"''',
    ),
    # Two triangles: all even, and no tour.
    (
        """    CHALLENGE = [
        (0, 1),
        (1, 2),
        (2, 0),
    ]""",
        """    CHALLENGE = [
        (0, 1),
        (1, 2),
        (2, 0),
        (3, 4),  # a second triangle, with no road to the first
        (4, 5),
        (5, 3),
    ]""",
    ),
    # Say on the page which copy this is.
    (
        """    # Part 4 · Hand the map to the machine

    **On your own**, with the sheet next to the laptop.""",
        """    # Part 4 · Hand the map to the machine — worked copy

    **Every ✍️ cell below is filled in.** The blank one, the one the students
    open, is `lab.py` next to this file.""",
    ),
    (
        "    Cells marked ✍️ are yours. Everything else runs itself.",
        "    The route of 1(a) is one of several; any of them starts at Ithaca\n"
        "    and finishes at Albany.",
    ),
]


def embed_css() -> bool:
    """Put the current lecture-hall.css into lab.py. True if the file changed."""
    before = LAB.read_text(encoding="utf-8")
    blob = base64.b64encode(CSS.read_bytes()).decode("ascii")
    after, n = CSS_LINE.subn(lambda m: f'{m.group(1)}"{blob}"{m.group(2)}', before)
    if n != 1:
        print(
            f"lab.py has {n} lines ending in '# BUILT' for the stylesheet, "
            "expected 1",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if after != before:
        LAB.write_text(after, encoding="utf-8")
        print(f"embedded {CSS.name} ({len(blob)} chars) into {LAB.name}")
    return after != before


def main() -> int:
    embed_css()
    text = LAB.read_text(encoding="utf-8")
    for old, new in SUBSTITUTIONS:
        found = text.count(old)
        if found != 1:
            print(
                f"lab.py has {found} copies of this anchor, expected 1:\n"
                f"---\n{old}\n---",
                file=sys.stderr,
            )
            return 1
        text = text.replace(old, new)

    if "TASK" in text:
        print("a TASK is still unanswered in the built copy", file=sys.stderr)
        return 1

    marker = "# ///\n"
    head, sep, tail = text.partition(marker)
    if not sep:
        print("lab.py has no PEP 723 header to hang the banner off", file=sys.stderr)
        return 1
    OUT.write_text(head + sep + BANNER + tail, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
