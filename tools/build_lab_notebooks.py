#!/usr/bin/env python3
"""Weld the stylesheet into a lab notebook, then write its worked copy.

    python tools/build_lab_notebooks.py                 # every module
    python tools/build_lab_notebooks.py m02-small-world # just this one

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

Adding a module: give it an entry in MODULES whose value is the list of
(anchor, answer) pairs. Nothing else here is per-module.
"""

from __future__ import annotations

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS_LINE = re.compile(r'^(\s*LECTURE_HALL_CSS_B64 = )".*"(  # BUILT)$', re.MULTILINE)

BANNER = """#
# GENERATED FILE -- do not edit. Run
#
#     python tools/build_lab_notebooks.py {slug}
#
# which fills in every blank of lab.py and writes this. The student's copy is
# lab.py; edit that one.
"""

# ---------------------------------------------------------------------------
# Module 1 -- four cities, seven highways, Euler's rule.
# ---------------------------------------------------------------------------
M01 = [
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

# ---------------------------------------------------------------------------
# Module 2 -- Ringville, the two shortcuts, and the index that lies.
#
# The worked copy differs from lab.py by the five answers and the title, and by
# nothing else. It used to also carry three notes to the reader -- what the
# notebook is for, the 1-to-16 versus 0-to-15 warning, and a line saying
# my_index has many right answers. All three are gone from both copies: the
# preamble was doing the sheet's job over again, and a student who has the
# sheet beside them does not need to be told twice.
# ---------------------------------------------------------------------------
M02 = [
    # The town, as a rule rather than thirty-two typed pairs. Both loops are
    # already in lab.py; the answer is the one line inside them.
    (
        """            j = ...  # TASK: who sits d seats clockwise from i?""",
        """            j = (i + d) % n  # ONE answer of several; `if j >= n: j -= n` is
                             # the same thing said longer, and is as good""",
    ),
    # No breadth-first search any more: igraph, in the two steps taught above.
    (
        """    g = ...  # TASK: step 1 — a graph of n people with these friendships
    return ...  # TASK: step 2 — the row of handshake counts out of person s""",
        """    g = igraph.Graph(n=n, edges=edges)
    return g.distances(source=s)[0]  # [0] because only one source was asked""",
    ),
    # The pencil answers the student marks themselves. The worked copy carries
    # the sheet's own numbers, so every row of the marking table reads green.
    (
        """    # Question 1(c) — Ringville, as it is in Part 1.
    my_total_1c = None  # every number in the boxes, added up
    my_average_1c = None  # that total shared among the other 15
    my_worst_1c = None  # the biggest number in any box

    # Question 3 — the same town with the two shortcuts of Part 2.
    my_total_3 = None
    my_average_3 = None
    my_worst_3 = None""",
        """    # Question 1(c) — Ringville, as it is in Part 1.
    my_total_1c = 36  # every number in the boxes, added up
    my_average_1c = 2.4  # that total shared among the other 15
    my_worst_1c = 4  # the biggest number in any box

    # Question 3 — the same town with the two shortcuts of Part 2.
    my_total_3 = 27
    my_average_3 = 1.8
    my_worst_3 = 3""",
    ),
    # The fraction of a person's friend-pairs who are friends.
    (
        """        if ...:  # TASK: are these two friends with each other?""",
        """        if A[a, b]:  # 1 when they are friends, 0 when they are not""",
    ),
    (
        """    pairs = ...  # TASK: how many pairs do k friends make?""",
        """    pairs = k * (k - 1) / 2""",
    ),
    # A test with a yardstick at both ends of the range.
    (
        '''    TASK: return one number. The check below never looks at your formula. It
    runs it on four towns and asks two things of the answers.
    """
    ...''',
        '''    One right answer out of many: omega (Telesford et al. 2011), with the
    sign flipped so that bigger is better. Zero is a small world, -1 is a
    lattice and -1 is a hat-drawn graph, and it cannot run away with n
    because each term is a ratio of two like things.
    """
    return -abs(m.L_rand / m.L - m.C / m.C_latt)''',
    ),
    # Say on the page which copy this is. The title carries it; the paragraph
    # of explanation that used to sit under it was cut, along with the rest of
    # the preamble -- see the note above M02.
    (
        """    # Part 5 · Hand the town to the machine""",
        """    # Part 5 · Hand the town to the machine — worked copy""",
    ),
]

MODULES = {
    "m01-euler_tour": M01,
    "m02-small-world": M02,
}


def paper_dir(slug: str) -> pathlib.Path:
    return ROOT / "lecture-note" / slug / "pen-and-paper"


def embed_css(lab: pathlib.Path, css: pathlib.Path) -> None:
    """Put the current lecture-hall.css into lab.py."""
    before = lab.read_text(encoding="utf-8")
    blob = base64.b64encode(css.read_bytes()).decode("ascii")
    after, n = CSS_LINE.subn(lambda m: f'{m.group(1)}"{blob}"{m.group(2)}', before)
    if n != 1:
        raise SystemExit(
            f"{lab}: {n} lines end in '# BUILT' for the stylesheet, expected 1"
        )
    if after != before:
        lab.write_text(after, encoding="utf-8")
        print(f"embedded {css.name} ({len(blob)} chars) into {lab.name}")


def build(slug: str, subs: list[tuple[str, str]]) -> int:
    paper = paper_dir(slug)
    lab, css, out = paper / "lab.py", paper / "lecture-hall.css", paper / "lab-solutions.py"
    for f in (lab, css):
        if not f.exists():
            print(f"{slug}: no {f.relative_to(ROOT)}", file=sys.stderr)
            return 1

    embed_css(lab, css)
    text = lab.read_text(encoding="utf-8")
    for old, new in subs:
        found = text.count(old)
        if found != 1:
            print(
                f"{slug}: lab.py has {found} copies of this anchor, expected 1:\n"
                f"---\n{old}\n---",
                file=sys.stderr,
            )
            return 1
        text = text.replace(old, new)

    if "TASK" in text:
        print(f"{slug}: a TASK is still unanswered in the built copy", file=sys.stderr)
        return 1

    marker = "# ///\n"
    head, sep, tail = text.partition(marker)
    if not sep:
        print(f"{slug}: lab.py has no PEP 723 header for the banner", file=sys.stderr)
        return 1
    out.write_text(head + sep + BANNER.format(slug=slug) + tail, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


def main(argv: list[str]) -> int:
    wanted = argv or sorted(MODULES)
    unknown = [s for s in wanted if s not in MODULES]
    if unknown:
        print(
            f"no lab notebook registered for {', '.join(unknown)}; "
            f"known modules are {', '.join(sorted(MODULES))}",
            file=sys.stderr,
        )
        return 1
    return max(build(slug, MODULES[slug]) for slug in wanted)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
