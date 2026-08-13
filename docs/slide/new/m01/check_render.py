#!/usr/bin/env python3
"""m01 render gate — thin wrapper around gatelib. All logic lives in
docs/slide/new/gatelib/check_render.py. This file carries only m01's constants."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gatelib.check_render import run

run(
    deck="m01-euler-tour.md",
    node_fills=[(0x39, 0x59, 0xA6)],  # accent only (m01 predates multi-fill palette)
    fig_h={"": 380},  # m01 predates fig modifiers
    exempt_figures=["konigsberg-map.png"],
    content_bottom=690,  # m01's theme predates the 660 correction
)
