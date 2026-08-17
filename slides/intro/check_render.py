#!/usr/bin/env python3
"""Render gate for the course intro deck — thin wrapper around gatelib.

Photographs and the three EngiNet program slides are exempt from in-figure
measurement: they are not figures this deck authored, so their type size and
ink margins are not ours to fix.
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gatelib.check_render import run

# The deck palette, and the only colours a figcaption here may name. Keep in
# step with figures/make_figures.py and theme.css.
PURPLE = (0x59, 0x31, 0x96)
RED = (0xC2, 0x41, 0x0C)
GREY = (0x76, 0x75, 0x7C)

run(
    deck="intro.md",
    node_fills=[PURPLE, RED, GREY],
    exempt_figures=[
        "airline_routes.jpg", "brain_tracts.jpg", "deadlift.jpg",
        "digesting_duck.jpg", "euler.jpg", "internet_map.jpg", "lehman.jpg",
        "pen_paper.jpg", "von_neumann.jpg", "philosophers.jpg",
        "flue-01.png", "flue-02.png", "xkcd_dependency.png",
    ],
    colour_words={"purple": PURPLE, "red": RED, "gray": GREY, "grey": GREY},
)
