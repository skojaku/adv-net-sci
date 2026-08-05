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
    <a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/exercise-m04-friendship-paradox.ipynb">
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Degree distribution

    The degree distribution is crucial to understand the friendship paradox.
    We will first introduce a formal definition of the degree distribution. Then, we will learn how to plot the degree distribution of a network.

    ![](https://barabasi.com/img/6/159.png)

    ## Definition

    The degree of a node $i$, denoted by $d_i$, is the number of edges connected to it. With the adjacency matrix $A$, the degree of node $i$ is given by:

    $$
    d_i = \sum_{j=1}^N A_{ij}.
    $$

    The degree distribution $p(d)$ is the probability that a node has $d$ edges.

    Let us compute the degree distribution of a network. We will create a Barabási-Albert network with $N=10,000$ nodes and $m=1$ edge per node.
    """)
    return


@app.cell
def _():
    import igraph
    g = igraph.Graph.Barabasi(n = 10000, m = 1) # Create a Barabási-Albert network
    return (g,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compute the degree of each node by summing the elements of the adjacency matrix along the rows.
    """)
    return


@app.cell
def _(g):
    import numpy as np
    deg = np.array(g.degree())

    # or using the adjacency matrix
    # deg = np.sum(A, axis=1)
    # deg = deg.flatten()
    return deg, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The degree distribution $p(d)$ can be computed by counting the number of nodes with each degree and dividing by the total number of nodes.
    """)
    return


@app.cell
def _(deg, np):
    p_deg = np.bincount(deg) / len(deg)
    return (p_deg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `np.bincount` returns the number of nodes with each degree. For example, `np.bincount([1, 2, 2, 3, 3, 3])` returns `[0, 1, 2, 3]`, which means there is 1 node with degree 1, 2 nodes with degree 2, and 3 nodes with degree 3.

    Let us plot the degree distribution. This is not as trivial as you might think... 🤔
    """)
    return


@app.cell
def _(np, p_deg):
    import seaborn as sns
    import matplotlib.pyplot as plt
    _ax = sns.lineplot(x=np.arange(len(p_deg)), y=p_deg)
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('Probability')
    return plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    While it clearly shows that most nodes have small degree, it does not show the tail of the distribution clearly, and often it is this tail that is of great interest (e.g., hub nodes). To show the tail of the distribution more clearly, we can use a log-log plot.
    """)
    return


@app.cell
def _(np, p_deg, sns):
    _ax = sns.lineplot(x=np.arange(len(p_deg)), y=p_deg)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_ylim(np.min(p_deg[p_deg > 0]) * 0.01, None)
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('Probability')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We see fluctuations for large degree nodes because of the small number of nodes with large degree.
    One can use "binning" to smooth the plot. Binning involves grouping the data into bins and calculating the fraction of data within each bin. However, selecting an appropriate bin size can be challenging, and even with a well-chosen bin size, some information may be lost.

    A more convenient way is to use cumulative distribution function (CDF) and its complement, the complementary cumulative distribution function (CCDF).
    The CDF at degree $k$ is the probability that a randomly chosen node has degree $k'$ less than or equal to $k$ ($k' \leq k$).

    $$
    \text{CDF}(k) = P(k' \leq k) = \sum_{k'=0}^k p(k')
    $$

    The CCDF at degree $d$ is the probability that a randomly chosen node has degree $d'$ greater than $d$ ($d' > d$).

    $$
    \text{CCDF}(k) = P(k' > k) = \sum_{k'=k+1}^\infty p(k')
    $$

    The benefits of using CDF and CCDF are:
    - CDF is a monotonically increasing function of $k$, and CCDF is a monotonically decreasing function of $k$.
    - CDF and CCDF can be plotted as a smooth curve on a log-log scale without binning.

    ### Exercise 01: Compute the CDF and CCDF 🏋️‍♀️

    1. Plot the CDF and CCDF of the degree distribution using histogram or lineplot. Do not use `sns.ecdfplot` or similar APIs that directly compute the CDF or CCDF from the data. You are the one who computes the CDF and CCDF from the degree distribution.
    2. Provide your estimate of the slope of the CCDF in the log-log plot. (What does the slope tell us about the degree distribution? Check out the lecture note for more details.)

    **CDF**
    """)
    return


@app.cell
def _(np, p_deg, sns):
    p_deg_cdf = np.cumsum(p_deg)
    assert np.isclose(p_deg_cdf[-1], 1), p_deg_cdf[-1]
    _ax = sns.lineplot(x=np.arange(len(p_deg_cdf)), y=p_deg_cdf)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('Probability')
    return (p_deg_cdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **CCDF**
    """)
    return


@app.cell
def _(np, p_deg, sns):
    p_deg_ccdf = np.cumsum(p_deg[::-1])[::-1]
    _ax = sns.lineplot(x=np.arange(len(p_deg_ccdf)), y=p_deg_ccdf)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    return (p_deg_ccdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Degree distribution of a friend

    We will now consider the degree distribution of a friend of a node.

    There are two ways to sample a friend of a node.
    1. Sample a node uniformly at random and then sample a friend of the node.
    2. Sample a *friendship* (i.e., edge) uniformly at random and then sample an end node of the edge.

    Let us focus on the second case and leave the first case for interested students as an exercise.
    In the second case, we sample an edge from the network.
    This sampling is biased towards nodes with many edges, i.e., a person with $d$ edges is $d$ times more likely to be sampled than someone with 1 edge.
    Thus, the degree distribution $p'(k)$ of a friend is given by

    $$
    p' (k) = C \cdot k \cdot p(k)
    $$

    The additional term $k$ reflects the fact that a person with $k$ friends is $k$ times more likely to be sampled than someone with 1 friend.
    Term $C$ is the normalization constant that ensures the sum of probabilities $p'(k)$ over all $k$ is 1, which can be easily computed as follows:

    $$
    C = \frac{1}{\sum_{k} k \cdot p(k)} = \frac{1}{\langle k \rangle}
    $$

    where $\langle k \rangle$ is the average degree of the network. Substituting $C$ into $p'(k)$, we get:

    $$
    p' (k) = \frac{k}{\langle k \rangle} p(k)
    $$

    This is the degree distribution of a friend, and it is easy to verify that $p'(k) > p(k)$ for $k \geq \langle k \rangle$, i.e., a friend has a higher chance of having a higher degree than a node. In other words, the friendship paradox 😉.

    ## Exercise 02: Compare the degree distribution of a node and its friend 🏋️‍♀️

    Let us compare the degree distribution of a node and its friend. It consists of the following steps
    -  Get the edges in the network, from which we sample a friend.
    -  Get the degree of each friend.
    - Compute the degree distribution of friends.

    1. Compute the average degree of nodes and friends.
    2. Plot the CCDF and CDF of the degree distribution of nodes and friends in the same plot.
    3. Compare the slope of the CCDF of a node and its friend.

    **Tips:**
    You can get the edges in the network from the adjacency matrix by using `sparse.find`.
    """)
    return


@app.cell
def _(g):
    A = g.get_adjacency() # Get the adjacency matrix
    from scipy import sparse
    src, trg, weight = sparse.find(A)
    return (src,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `sparse.find(A)` returns the source node, target node, and edge weight of the edge.
    - `src` is the source node of the edge
    - `trg` is the target node of the edge
    - `weight` is the edge weight.
    """)
    return


@app.cell
def _(deg, np, p_deg_cdf, plt, sns, src):
    deg_friend = deg[src]  # deg[trg]
    p_deg_friend = np.bincount(deg_friend) / len(deg_friend)
    p_deg_friend_cdf = np.cumsum(p_deg_friend)
    p_deg_friend_ccdf = np.cumsum(p_deg_friend[::-1])[::-1]
    _fig, _ax = plt.subplots(figsize=(7, 5))
    _ax = sns.lineplot(x=np.arange(len(p_deg_friend_cdf)), y=p_deg_friend_cdf, ax=_ax, label='Friend')
    _ax = sns.lineplot(x=np.arange(len(p_deg_friend_ccdf)), y=p_deg_cdf, ax=_ax, label='Original')
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CDF')
    return p_deg_friend_ccdf, p_deg_friend_cdf


@app.cell
def _(np, p_deg_ccdf, p_deg_friend_ccdf, p_deg_friend_cdf, plt, sns):
    _fig, _ax = plt.subplots(figsize=(7, 5))
    _ax = sns.lineplot(x=np.arange(len(p_deg_friend_cdf)), y=p_deg_friend_ccdf, label='Friend', ax=_ax)
    _ax = sns.lineplot(x=np.arange(len(p_deg_friend_cdf)), y=p_deg_ccdf, label='Original', ax=_ax)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```{footbibliography}
    ```
    """)
    return


@app.cell
def _(deg, np, p_deg, p_deg_ccdf, plt, sns):
    p_deg_friend_analytical = p_deg * np.arange(len(p_deg)) / np.mean(deg)
    p_deg_friend_ccdf_analytical = np.cumsum(p_deg_friend_analytical[::-1])[::-1]
    _fig, _ax = plt.subplots(figsize=(7, 5))
    sns.lineplot(x=np.arange(len(p_deg_friend_ccdf_analytical)), y=p_deg_friend_ccdf_analytical, label='Analytical', ax=_ax)
    sns.lineplot(x=np.arange(len(p_deg_ccdf)), y=p_deg_ccdf, label='Empirical', ax=_ax)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    return


if __name__ == "__main__":
    app.run()
