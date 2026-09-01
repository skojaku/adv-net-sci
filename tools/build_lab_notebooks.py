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
# The worked copy differs from lab.py by the answers and the title, and by
# nothing else. Two of those answers are whole function bodies (ring_edges and
# local_clustering, both blank in lab.py), three are the igraph one-liners of
# section 3, one is the block of pencil answers off the sheet, and one is
# igraph's own clustering call on Ringville.
# ---------------------------------------------------------------------------
M02 = [
    # The town, as a rule rather than thirty-two typed pairs. lab.py gives the
    # loop over people and the empty list; the body inside it is the answer.
    (
        """    for i in range(n):  # each person in turn
        # ✍️ your code here — append the pair (i, j) for each of the `half`
        #    people who sit clockwise from i.
        ...""",
        """    for i in range(n):  # each person in turn
        # ✍️ your code here — append the pair (i, j) for each of the `half`
        #    people who sit clockwise from i.
        for j in range(i + 1, i + 1 + half):
            _j = j % n  # ONE answer of several; `if _j >= n: _j -= n` is the
                        # same thing said longer, and is as good
            edges.append((i, _j))""",
    ),
    # Section 3, three cells to play in. Nothing here is marked; the worked
    # copy carries them so that the answer to "what does it print" is on the
    # page rather than in the instructor's head.
    (
        """    # ✍️ Compute the neighbors of node 3, 5, and 0
    g.neighbors(3)""",
        """    # ✍️ Compute the neighbors of node 3, 5, and 0
    g.neighbors(3), g.neighbors(5), g.neighbors(0)""",
    ),
    (
        """    # ✍️ Construct the graph by igraph.Graph(edges=[(0, 1), (0, 2)]), and check the number of nodes
    ...""",
        """    # ✍️ Construct the graph by igraph.Graph(edges=[(0, 1), (0, 2)]), and check the number of nodes
    g_no_n = igraph.Graph(edges=[(0, 1), (0, 2)])
    g_no_n.vcount()  # 3, not 7 -- igraph saw three people in those two pairs""",
    ),
    (
        """    # ✍️ Construct the graph by igraph.Graph(n=DEMO_N, edges=DEMO_EDGES + [(0, 1)]), and check the number of edges
    ...""",
        """    # ✍️ Construct the graph by igraph.Graph(n=DEMO_N, edges=DEMO_EDGES + [(0, 1)]), and check the number of edges
    g_twice = igraph.Graph(n=DEMO_N, edges=DEMO_EDGES + [(0, 1)])
    g_twice.ecount()  # 10, not 9 -- both copies of (0, 1) are kept""",
    ),
    # Question 1(c) with igraph, written from nothing. The marking cell holds
    # no answer of its own -- it compares against Q1C in the hidden kit -- so
    # this is the only place the worked code exists.
    (
        """    # ✍️ Write your igraph code here. Use as many lines as you like; the
    #    three variables below are what gets marked.

    answer_total = ...  # ✍️ every handshake count from person 0, added up
    answer_average = ...  # ✍️ that total shared among the other 15 people
    answer_worst = ...  # ✍️ the biggest of those counts""",
        """    g_town = igraph.Graph(n=TOWN_N, edges=ring_edges(TOWN_N, TOWN_HALF))
    counts = g_town.distances(source=0)[0]

    answer_total = sum(counts)  # person 0's own 0 adds nothing
    answer_average = sum(counts) / (TOWN_N - 1)  # shared among the other 15
    answer_worst = max(counts)""",
    ),
    # The fraction of a person's friend-pairs who are friends. lab.py hands
    # the student the docstring and nothing else, so the whole body is the
    # answer -- including the pairing loop, which the prose no longer gives.
    (
        """    # ✍️ Your code here
    ...
    return ...""",
        """    nbrs = g.neighbors(i)  # the list of people i is friends with
    k = len(nbrs)
    if k < 2:  # fewer than two friends, so no pairs
        return 0.0

    links = 0
    for x in range(k):  # each of i's friends,
        for y in range(x + 1, k):  # paired with each LATER one, so that
            a, b = nbrs[x], nbrs[y]  # every pair comes up exactly once
            if g.are_adjacent(a, b):  # True when a and b are friends
                links += 1

    return links / (k * (k - 1) / 2)""",
    ),
    # The same quantity, straight out of igraph, on Ringville.
    (
        """    # ✍️ Create Ringville. After finishing 1, put DEMO_EDGES back in.
    g_clust = ...

    # ✍️ Compute the transitivity
    transitivity = ...""",
        """    # ✍️ Create Ringville. After finishing 1, put DEMO_EDGES back in.
    g_clust = igraph.Graph(n=TOWN_N, edges=ring_edges(TOWN_N, TOWN_HALF))

    # ✍️ Compute the transitivity
    transitivity = g_clust.transitivity_local_undirected(mode="zero")""",
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
