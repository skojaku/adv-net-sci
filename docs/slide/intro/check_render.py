#!/usr/bin/env python3
"""Render gate for the course intro deck — thin wrapper around gatelib.

Photographs and the three EngiNet program slides are exempt from in-figure
measurement: they are not figures this deck authored, so their type size and
ink margins are not ours to fix.
"""

import sys, os

sys.path.insert(0, os.path.expanduser("~/.claude/skills/slide"))
from gatelib.check_render import run

run(
    deck="intro.md",
    node_fills=[(0x39, 0x59, 0xA6), (0xB1, 0x44, 0x34), (0x6B, 0x6B, 0x6B)],
    exempt_figures=[
        "airline_routes.jpg", "brain_tracts.jpg", "deadlift.jpg",
        "digesting_duck.jpg", "euler.jpg", "internet_map.jpg", "lehman.jpg",
        "pen_paper.jpg", "von_neumann.jpg", "philosophers.jpg",
    ],
)
