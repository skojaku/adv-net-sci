#!/usr/bin/env python3
"""m05 render gate — thin wrapper around gatelib."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gatelib.check_render import run

run(
    deck="m05-clustering.md",
    node_fills=[(0x39, 0x59, 0xA6), (0xB1, 0x44, 0x34)],
    fig_h={"": 380, "tight": 320, "stack": 190},
    exempt_figures=["boruvka-portrait.png", "konigsberg-map.png"],
    content_bottom=660,
)
