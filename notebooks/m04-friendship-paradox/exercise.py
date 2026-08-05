import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/m04-friendship-paradox/exercise.ipynb">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>
    """)
    return


@app.cell
def _():
    # If you are using Google Colab, uncomment the following line to install igraph
    # !sudo apt install libcairo2-dev pkg-config python3-dev
    # !pip install pycairo cairocffi
    # !pip install igraph
    return


@app.cell
def _():
    import igraph
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    return igraph, np, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hands-on: Degree Distribution

    Let's create a degree-heterogeneous network, Barabasi-Albert network.
    """)
    return


@app.cell
def _(igraph):
    g = igraph.Graph.Barabasi(n=3000, m=10)
    return (g,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's compute the degree of each node. You can use `Graph.degree` to get the degree of each node, or alternatively compute it from the adjacency matrix (via `Graph.get_adjacency`).
    """)
    return


@app.cell
def _(g):
    degree = g.degree()

    # Alternatively, you can compute the degree from the adjacency matrix by
    #A = g.get_adjacency()
    #degree = np.sum(A, axis=1)
    return (degree,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's plot the degree distribution using a simple histogram. To do that, we compute the *frequency* of each degree value.
    """)
    return


@app.cell
def _():
    # Compute degree for each node
    p_deg = ...
    return


@app.cell
def _(plt):
    # Plot
    _fig, _ax = plt.subplots(figsize=(8, 5))
    ...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's plot it in log-log scale.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's plot it in **Complementary Cumulative Distribution Function (CCDF)**.
    """)
    return


@app.cell
def _():
    ccdf_deg = ... # Compute the CCDF
    return (ccdf_deg,)


@app.cell
def _(ccdf_deg, np, plt, sns):
    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax = sns.lineplot(x=np.arange(len(ccdf_deg)), y=ccdf_deg)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    _ax.set_title('CCDF: Smooth Power-Law Visualization')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `seaborn` offers a convenient function to plot the CCDF.
    """)
    return


@app.cell
def _(degree, plt, sns):
    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax = sns.ecdfplot(degree, complementary=True, log_scale=(True, True), ax=_ax)
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    The Barabasi-Albert network is a scale-free network, which means that the degree distribution follows a power law, i.e.,

    $$
    P(k) \propto k^{-\gamma}
    $$

    where $\gamma$ is the power-law exponent. From the figure above, how can we estimate the power-law exponent?  Write your derivation in the markdown cell below, or hand-write it. Then, identify the power-law exponent from the plot.

    **Hint**:

    Derive the analytical form of the CCDF of the power-law distribution and fit it to the data.

    The CCDF is given by $F(k) = P(k' > k)$, i.e., fraction of data points that are greater than $k$. Alternatively, it can be written as

    $$
    F(k) = \int_k^\infty P(k') dk'
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Discussion: What could be wrong?

    While the above method for identifying the power-law exponent is useful to understand the degree heterogeneity, it is not a good practice to use a plot as a way to identify the power-law exponent. Why?
    """)
    return


if __name__ == "__main__":
    app.run()
