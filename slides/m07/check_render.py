#!/usr/bin/env python3
"""Render gate for this deck — thin wrapper around gatelib. All the actual
logic lives in ~/.claude/skills/slide/gatelib/check_render.py. This
file carries only this deck's own constants.

Copy this file into your deck's directory alongside deck.md and adjust the
constants below.
"""

import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/slide"))
from gatelib.check_render import run

run(
    deck="m07-random-walks.md",  # your deck's filename

    # Only set this if the deck draws circular node-link diagrams (network
    # or graph figures) and you want their disc size checked (26-52px band).
    # Leave unset for any other kind of deck.
    # node_fills=[(0x39, 0x59, 0xA6), (0xB1, 0x44, 0x34)],

    # Figure height caps by `.fig` modifier class, if you use them
    # (see theme.css: .fig, .fig.tight, .fig.stack, .fig.tall).
    # the theme lets L-b show 480 px and L-g 600 px (L-a stays under 380 by authoring); the gate keys caps by modifier only
    fig_h={"": 600, "tight": 320, "stack": 190, "tall": 400},

    # Filenames to skip measurement on (historical photos, screenshots, etc.)
    exempt_figures=["qr-sim.png", "eigvec2.png"],   # eigvec2 is shown at 756 px beside a sentence   # a QR code is shown at a fixed 440 px
)
