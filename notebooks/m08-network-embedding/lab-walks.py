# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = [
#     "marimo>=0.23",
#     "gensim>=4.3",
#     "networkx>=3.0",
#     "numpy>=1.26",
#     "pandas>=2.0",
#     "scikit-learn>=1.3",
#     "altair>=5.0",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random
    import pandas as pd
    import networkx as nx
    import altair as alt
    from gensim.models import Word2Vec
    from sklearn.decomposition import PCA

    return PCA, Word2Vec, alt, mo, nx, pd, random


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab: random walks make embeddings

    Run random walkers on a network, treat each walk as a sentence, and train Word2Vec on the sentences.
    The network is the co-appearance network of *Les Misérables* (77 characters; two characters are linked if they appear in the same scene).
    """)
    return


@app.cell
def _(nx, pd):
    BASE = "https://raw.githubusercontent.com/skojaku/adv-net-sci/main/lecture-note/assets/data/lesmis/"


    def read_lesmis(name):
        """Read a csv from the repo (relative path), else from GitHub (molab)."""
        try:
            return pd.read_csv(f"../../lecture-note/assets/data/lesmis/{name}")
        except FileNotFoundError:
            return pd.read_csv(BASE + name)


    nodes, edges = read_lesmis("node_table.csv"), read_lesmis("edge_table.csv")
    names = dict(zip(nodes["node_id"], nodes["name"]))

    G = nx.Graph()
    G.add_nodes_from(nodes["name"])
    G.add_weighted_edges_from(
        (names[s], names[t], w) for s, t, w in zip(edges["src"], edges["trg"], edges["weight"])
    )
    G
    return (G,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The walk simulator

    A walker sits on a node and moves to a uniformly random neighbour at every step (edge weights are ignored).
    We start `walks_per_node` walkers from every node, and each walker's list of visited nodes is one sentence.
    """)
    return


@app.cell
def _(G):
    def random_walk(G, start, length, rng):
        """One plain random walk: a list of `length` node names. `rng` is a random.Random."""
        walk = [start]
        while len(walk) < length:
            walk.append(rng.choice(list(G[walk[-1]])))
        return walk


    def simulate_walks(G, walks_per_node, length, rng):
        return [random_walk(G, v, length, rng) for v in G for _ in range(walks_per_node)]

    return random_walk, simulate_walks


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Word2Vec on the walks

    Skip-gram with negative sampling: a node must predict the nodes that appear within 5 steps of it in a walk (`sample=0` keeps every visit, because a restarting walk visits its start very often).
    Nodes that share many walk-neighbours end up with similar vectors.
    """)
    return


@app.cell
def _(Word2Vec):
    def embed(walks, dim=32):
        """Train skip-gram (sg=1) with negative sampling; return the node vectors."""
        model = Word2Vec(
            walks, vector_size=dim, window=5, min_count=1,
            sg=1, hs=0, negative=5, epochs=20, sample=0, workers=1, seed=0,
        )
        return model.wv

    return (embed,)


@app.cell
def _(G, mo):
    fav = mo.ui.dropdown(sorted(G.nodes), value="Valjean", label="Favourite character")
    length = mo.ui.slider(10, 100, 10, value=40, label="Walk length")
    mo.hstack([fav, length], justify="start")
    return fav, length


@app.cell
def _(G, embed, length, random, simulate_walks):
    plain_walks = simulate_walks(G, 10, length.value, random.Random(0))
    wv_plain = embed(plain_walks)
    plain_walks[0][:8]
    return (wv_plain,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Look at the embedding

    PCA squeezes the 32-dimensional vectors into 2-D. Red is your favourite, blue are its 10 nearest characters by cosine similarity.
    """)
    return


@app.cell
def _(PCA, alt, fav, pd):
    def show(wv, title):
        """2-D PCA scatter of an embedding; characters never visited by a walk are not in `wv`."""
        xy = PCA(2, random_state=0).fit_transform(wv.vectors)
        near = [n for n, _ in wv.most_similar(fav.value, topn=10)]
        df = pd.DataFrame(xy, columns=["x", "y"])
        df["name"] = wv.index_to_key
        df["who"] = ["favourite" if n == fav.value else "nearest 10" if n in near else "others" for n in df["name"]]
        return (
            alt.Chart(df, title=title).mark_circle(size=70)
            .encode(
                x=alt.X("x", axis=None), y=alt.Y("y", axis=None), tooltip="name",
                color=alt.Color("who", legend=None, scale=alt.Scale(
                    domain=["favourite", "nearest 10", "others"],
                    range=["#d62728", "#4c78a8", "#c8c8c8"])),
            )
            .properties(width=380, height=300)
        )

    return (show,)


@app.cell
def _(show, wv_plain):
    show(wv_plain, "Plain random walks")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Your turn: personalized PageRank walks

    A PPR walker belongs to one favourite character. At every step, with probability `alpha` it jumps back to `start`; otherwise it moves to a random neighbour.
    Fill in `ppr_walk`, then see how the embedding around your favourite changes. The stub below ignores `alpha`, so everything runs before you edit it.
    """)
    return


@app.cell
def _(mo):
    mo.accordion({
        "Hints": mo.md(
            "- Draw `rng.random()`; if it is below `alpha`, the next node is `start`.\n"
            "- Otherwise take a random neighbour of the current node, as in `random_walk`.\n"
            "- A restart still counts as a step: append `start` to the walk."
        )
    })
    return


@app.cell
def _(random_walk):
    def ppr_walk(G, start, length, alpha, rng):
        """A walk of `length` nodes from `start` that restarts at `start` with probability `alpha` at every step."""
        # TODO: replace this plain walk (it ignores alpha) with a restarting walk.
        return random_walk(G, start, length, rng)

    return (ppr_walk,)


@app.cell
def _(mo):
    alpha = mo.ui.slider(0.05, 0.9, 0.05, value=0.3, label="Restart probability alpha")
    alpha
    return (alpha,)


@app.cell
def _(G, alpha, embed, fav, length, ppr_walk, random):
    rng = random.Random(0)
    ppr_walks = [ppr_walk(G, fav.value, length.value, alpha.value, rng) for _ in range(1000)]
    wv_ppr = embed(ppr_walks)
    f"{len(wv_ppr)} of {G.number_of_nodes()} characters were visited"
    return (wv_ppr,)


@app.cell
def _(fav, mo, pd, show, wv_plain, wv_ppr):
    # Characters the walks never reach are missing from the vocabulary, so a large alpha gives a small map.
    def nearest(wv):
        return [n for n, _ in wv.most_similar(fav.value, topn=10)]


    table = pd.DataFrame({"plain walks": nearest(wv_plain), "PPR walks": nearest(wv_ppr)}, index=range(1, 11))
    mo.hstack([show(wv_ppr, "PPR walks"), table], align="center")
    return


if __name__ == "__main__":
    app.run()
