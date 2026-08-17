#!/usr/bin/env python3
"""m01 render gate — thin wrapper around gatelib. All logic lives in
slides/gatelib/check_render.py. This file carries only m01's constants."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gatelib.check_render import run

# The deck palette, and the only colours a figcaption here may name. Keep in
# step with figures/make_figures.py and network-science.css.
PURPLE = (0x59, 0x31, 0x96)
RED = (0xC2, 0x41, 0x0C)
GREY = (0x76, 0x75, 0x7C)

run(
    deck="m01-euler-tour.md",
    node_fills=[PURPLE],  # accent only (m01 predates multi-fill palette)
    fig_h={"": 380},  # m01 predates fig modifiers
    exempt_figures=["konigsberg-map.png"],
    content_bottom=690,  # m01's theme predates the 660 correction
    colour_words={"purple": PURPLE, "red": RED, "gray": GREY, "grey": GREY},
)
