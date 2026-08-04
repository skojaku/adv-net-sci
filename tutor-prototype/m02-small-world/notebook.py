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
    Your AI tutor will build it with you, step by step, in the terminal
    window next to this one.

    **How this works:**

    - 💬 The **terminal** is where you and your tutor talk.
    - 📓 This **notebook** is your shared whiteboard. Questions and
      experiments will appear here as you go.
    - ✏️ You can answer in the notebook *or* just type your answer in the
      terminal — whichever feels easier. Both always work.
    - 🧭 Ask anything, anytime. Detours are encouraged.

    No programming experience needed. Say hello in the terminal to begin!
    """)
    return


if __name__ == "__main__":
    app.run()
