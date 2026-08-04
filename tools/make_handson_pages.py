#!/usr/bin/env python3
"""Generate the per-module "Hands-on" pages for the lecture note.

Each page is a short guide: what you will build, what to watch for, and a link
to the marimo notebook that holds the actual code. No code lives in the .qmd.

Run from the repository root:  python3 tools/make_handson_pages.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/lecture-note"

MODULES = [
    dict(
        dir="m01-euler_tour",
        var="m01",
        nb="notebooks/m01-euler-tour/coding.ipynb",
        title="Hands-on: Representing and Traversing a Network",
        lead="Königsberg is small enough to solve by staring at it. The point of this notebook is to solve it the way you would solve a network with a million nodes.",
        build=[
            "Store the same network three ways — edge list, adjacency list, adjacency matrix — and convert between them.",
            "Compute degree from each representation and confirm the three agree.",
            "Write checks that decide whether a given sequence is a walk, a trail, or a path.",
            "Find connected components with depth-first search.",
            "Put it together into a function that answers Euler's question for any network.",
        ],
        watch=[
            "The three representations are not interchangeable in cost. Ask, for each operation, which one makes it cheap — that instinct is what the rest of the course runs on.",
            "Your component finder is the same algorithm you will use in Module 3 to measure how much network survives an attack.",
        ],
    ),
    dict(
        dir="m02-small-world",
        var="m02",
        nb="notebooks/m02-small-world/coding.ipynb",
        title="Hands-on: Measuring How Small the World Is",
        lead="You now know what average path length and clustering mean. Here you measure them, on generated networks where you know the answer and on a real one where you do not.",
        build=[
            "Get comfortable with igraph: build graphs, compute shortest paths, extract components.",
            "Compute local, average-local and global clustering, and reconcile them by hand on a small graph.",
            "Generate lattices, random graphs and Watts-Strogatz networks, and compare them.",
            "Compute the small-world index sigma against a random baseline.",
            "Estimate path length by sampling when the network is too large for all-pairs.",
        ],
        watch=[
            "Average local clustering and global clustering will disagree. Work out which nodes cause the gap before reading on.",
            "Sweep the rewiring probability p and plot clustering and path length together. The band where both are favourable is wider than most people guess.",
        ],
    ),
    dict(
        dir="m03-robustness",
        var="m03",
        nb="notebooks/m03-robustness/coding.ipynb",
        title="Hands-on: Breaking Networks on Purpose",
        lead="The theory says scale-free networks shrug off random failure and collapse under targeted attack. Here you make that happen and measure it.",
        build=[
            "Measure connectivity as the fraction of nodes left in the largest component.",
            "Simulate random failure, averaging over many runs to get confidence intervals.",
            "Simulate targeted attack, both with a fixed ranking and with degrees recomputed after every removal.",
            "Plot robustness profiles and reduce each to a single R-index.",
            "Compare network types — random, scale-free, lattice — under both attack modes.",
        ],
        watch=[
            "Run random failure once and it looks smooth; run it fifty times and the variance is the story. Always plot the spread, not just the mean.",
            "Compare adaptive against fixed-order attack on the same network. The gap is the value of information to an attacker.",
            "Check your measured threshold against f_c = 1 - 1/(kappa - 1) from the appendix.",
        ],
    ),
    dict(
        dir="m04-node-degree",
        var="m04",
        nb="notebooks/m04-friendship-paradox/coding.ipynb",
        title="Hands-on: Degree Distributions and the Friendship Paradox",
        lead="Plotting a degree distribution badly is the most common mistake in network analysis. This notebook is mostly about not making it.",
        build=[
            "Generate a scale-free network and plot its degree distribution on linear axes, log-log axes, and as a CCDF.",
            "Estimate the power-law exponent from the CCDF slope — and get the 1 - gamma correction right.",
            "Demonstrate the friendship paradox by sampling edge endpoints rather than nodes.",
            "Compare the degree distribution of nodes with that of their neighbours.",
            "Identify hubs, remove them, and measure the damage.",
            "Measure degree assortativity across different network types.",
        ],
        watch=[
            "Compute the gap between your mean degree and mean friend degree, then check it against Var(k)/<k>. They should match exactly.",
            "Try the same plot with different bin widths. The PDF changes shape; the CCDF does not. That is the whole argument for the CCDF.",
        ],
    ),
    dict(
        dir="m05-clustering",
        var="m05",
        nb="notebooks/m05-clustering/coding.ipynb",
        title="Hands-on: Finding Communities (and Doubting Them)",
        lead="Running a community detection algorithm takes one line. Knowing whether to believe the output is the skill.",
        build=[
            "Run Louvain, Leiden, label propagation and edge betweenness on the same network and compare the partitions.",
            "Implement modularity from its definition and check it against the library's value.",
            "Visualize communities on a network layout.",
            "Score partitions against known labels with NMI and ARI.",
        ],
        watch=[
            "Run Louvain several times with different seeds. The partitions will differ. That instability is the degeneracy problem, not a bug in your code.",
            "Run modularity maximization on an Erdos-Renyi graph with no communities at all. Note the score you get, then reconsider the Q > 0.3 rule of thumb.",
            "Build a network with two cliques joined by one edge, then add a third larger community and re-run. Watch the resolution limit merge the two cliques.",
        ],
    ),
    dict(
        dir="m06-centrality",
        var="m06",
        nb="notebooks/m06-centrality/coding.ipynb",
        title="Hands-on: Who Is Important, and In What Sense",
        lead="Eight centralities on one network, and the interesting part is where they disagree.",
        build=[
            "Compute degree, closeness, harmonic, betweenness, eigenvector, Katz and PageRank on a small social network.",
            "Implement Katz centrality yourself, including choosing a safe value for lambda.",
            "Apply the measures to the Roman road network and map the results geographically.",
            "Compute the correlation matrix between centralities and interpret it.",
        ],
        watch=[
            "Find the node whose betweenness rank is far above its degree rank. Look at where it sits — that is a broker.",
            "Set lambda above 1/lambda_max in your Katz implementation and watch it break. Understanding the failure is the point.",
            "Compute the correlations on a star graph and on a path graph. Near-total agreement in one, near-total disagreement in the other.",
        ],
    ),
    dict(
        dir="m07-random-walks",
        var="m07",
        nb="notebooks/m07-randomwalks/coding.ipynb",
        title="Hands-on: Walking Randomly, on Purpose",
        lead="Simulate the walk, then verify that the theory predicted what you observed.",
        build=[
            "Simulate a random walk and record visit frequencies.",
            "Compare the empirical visit distribution against the theoretical pi_i = k_i / 2m.",
            "Implement PageRank from the transition matrix and check it against the library.",
            "Compute random walk betweenness and compare it with shortest-path betweenness.",
            "Detect communities with Walktrap.",
            "Visualize a single trajectory over the network.",
        ],
        watch=[
            "Watch how many steps convergence takes on a network with two clear communities versus one without. That difference is the spectral gap made visible.",
            "Where random walk betweenness and shortest-path betweenness disagree, ask which one describes what is actually flowing through your network.",
        ],
    ),
    dict(
        dir="m08-embedding",
        var="m08",
        nb="notebooks/m08-network-embedding/coding.ipynb",
        title="Hands-on: Turning a Network into Coordinates",
        lead="Two families of embedding, built from scratch, then judged on the same task.",
        build=[
            "Implement Laplacian eigenmap and PCA on the adjacency matrix, and plot both.",
            "Generate biased random walks with node2vec's p and q parameters.",
            "Train a skip-gram model on those walks.",
            "Factorize network matrices directly and compare with the neural embeddings.",
            "Evaluate everything by link prediction.",
            "Visualize higher-dimensional embeddings with t-SNE.",
        ],
        watch=[
            "Sweep q from below 1 to above 1 and watch which nodes end up near each other. Low q should recover communities, high q should group nodes by role.",
            "Train the same model twice. The coordinates will differ completely while the link prediction score barely moves — embeddings are only defined up to rotation.",
        ],
    ),
    dict(
        dir="m09-graph-neural-networks",
        var="m09",
        nb="notebooks/m09-graph-neural-nets/coding.ipynb",
        title="Hands-on: Building Graph Neural Networks",
        lead="GCN, GraphSAGE and GAT on the same task, plus the failure mode that depth causes.",
        build=[
            "Set up PyTorch Geometric and turn a network into a Data object with node features.",
            "Implement GCN, GAT and GraphSAGE and train them for node classification.",
            "Compare their accuracy on the same train/validation split.",
            "Build a link prediction model on top of the learned representations.",
            "Assemble a graph classification model with a readout layer.",
            "Visualize the learned node embeddings, and the attention weights for GAT.",
        ],
        watch=[
            "Train GCNs with 2, 4, 8 and 16 layers. Accuracy will peak early and then fall — plot it, because over-smoothing is much more convincing when you have caused it yourself.",
            "Replace the node features with all-ones and re-run. Whatever accuracy remains came from topology alone.",
        ],
        extra=[
            ("Image processing preliminaries", "m09_image", "notebooks/m09-graph-neural-nets/image-processing.ipynb",
             "Edge detection, kernels, and the Fourier transform worked through on real images — the concrete version of the theory in the preparation chapter."),
            ("A GCN from scratch", "m09_gcn", "notebooks/m09-graph-neural-nets/gcn-from-scratch.ipynb",
             "Bruna's spectral GCN and ChebNet implemented directly from the equations, without PyTorch Geometric's layers."),
        ],
    ),
]

TEMPLATE = """---
title: "{title}"
---

{lead}

::: {{.callout-note title="Where the code lives"}}
This course keeps its lecture note free of runnable code. Everything you
execute lives in a marimo notebook, so it stays interactive and reactive
instead of being a wall of output frozen into a web page.

[Open the notebook in molab]({{{{< var molab.{var} >}}}})

Prefer to work locally? The same notebook is in the repository at
[`{nb}`](https://github.com/skojaku/adv-net-sci/blob/main/{nb}).
Run it with `marimo edit {nb_py}`.
:::

## What you will build

{build}

## What to watch for

{watch}
{extra}"""

EXTRA_TEMPLATE = """
## Also in this module

{items}"""


def bullets(items):
    return "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))


def dashes(items):
    return "\n".join(f"- {t}" for t in items)


def main():
    for m in MODULES:
        extra = ""
        if m.get("extra"):
            items = "\n\n".join(
                f"**{name}** — {desc}\n\n[Open in molab]({{{{< var molab.{var} >}}}}) · "
                f"[source](https://github.com/skojaku/adv-net-sci/blob/main/{nb})"
                for name, var, nb, desc in m["extra"]
            )
            extra = EXTRA_TEMPLATE.format(items=items)
        text = TEMPLATE.format(
            title=m["title"],
            lead=m["lead"],
            var=m["var"],
            nb=m["nb"],
            nb_py=m["nb"].replace(".ipynb", ".py"),
            build=bullets(m["build"]),
            watch=dashes(m["watch"]),
            extra=extra,
        )
        out = NOTE / m["dir"] / "02-coding.qmd"
        out.write_text(text)
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
