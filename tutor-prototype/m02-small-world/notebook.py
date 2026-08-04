# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "networkx",
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🌍 The Small-World Puzzle

    *Advanced Network Science — Module 02*

    This notebook starts almost empty — **that's on purpose.**

    - 💬 Your tutor talks with you in the **terminal**. Questions and answers
      happen there.
    - 📓 This notebook is the **whiteboard**: pictures, interactive
      experiments, and photo uploads will appear here when they're needed.
    - ✅ When a step here shows a **Done button**, click it when you're
      finished — your tutor will notice and pick it up from there.

    No programming experience needed. Say hello in the terminal to begin!
    """)
    return


@app.cell(hide_code=True)
def _():
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np

    return nx, np, plt


@app.cell(hide_code=True)
def _():
    from pathlib import Path as _Path

    def notify_tutor(checkpoint: str):
        """Signal the terminal tutor that notebook input is ready."""
        _Path("session_artifacts").mkdir(exist_ok=True)
        (_Path("session_artifacts") / "student_signal.txt").write_text(checkpoint)

    return (notify_tutor,)


if __name__ == "__main__":
    app.run()
