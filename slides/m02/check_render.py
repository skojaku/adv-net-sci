#!/usr/bin/env python3
"""m02 render gate — thin wrapper around gatelib."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gatelib.check_render import run

run(
    deck="m02-small-world.md",
    node_fills=[(0x39, 0x59, 0xA6)],
    fig_h={"": 380, "tight": 320, "stack": 190},
    # Photographs. The aspect and x-height checks both measure how far a
    # *generated* drawing's type has been scaled, which a film poster does not have.
    exempt_figures=["konigsberg-map.png", "six-degrees-poster.jpg"],
    content_bottom=660,
)
