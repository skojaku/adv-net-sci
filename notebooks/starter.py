# /// script
# dependencies = [
#     "matplotlib==3.10.6",
#     "numpy==2.3.2",
#     "pandas==2.3.2",
#     "python-igraph==0.11.9",
#     "scipy==1.16.1",
#     "seaborn==0.13.2",
# ]
# [tool.marimo.display]
# default_width = "full"
# [tool.marimo.formatting]
# line_length = 120
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App()


@app.cell
def _():


    return


@app.cell
def _():


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# Libraries""")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import igraph as ig
    import pandas as pd
    import numpy as np
    import scipy
    import matplotlib.pyplot as plt
    import seaborn as sns
    return


if __name__ == "__main__":
    app.run()
