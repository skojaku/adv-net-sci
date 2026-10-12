#!/usr/bin/env python3
"""m06 render gate — thin wrapper around gatelib."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gatelib.check_render import run

run(
    deck="m06-centrality.md",
    node_fills=[(0x39, 0x59, 0xA6), (0xB1, 0x44, 0x34)],
    fig_h={"": 380, "tight": 320, "stack": 190, "tall": 400},
    # Photographs, and maps that draw hundreds of dots rather than discs a student
    # reads one by one (figlib.emit(..., nodes=False) for the same figures).
    exempt_figures=["caesar.jpg", "augustus.jpg", "milliarium.jpg", "aesop.jpg",
                    "roma-basemap.png", "ny-overview.png", "ny-degree.png", "ny-closeness.png",
                    "ny-eccentricity.png", "ny-betweenness.png", "ny-eigenvector.png",
                    "ny-five.png"],
    content_bottom=660,
)
