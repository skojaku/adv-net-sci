"""Regenerate the static figures for this module.

Extracted from docs/lecture-note/m06-centrality/01-concepts.qmd.
Run from the repository root; writes SVGs into docs/lecture-note/figs/.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
OUT.mkdir(parents=True, exist_ok=True)


def _save(name):
    plt.savefig(OUT / f'{name}.svg', bbox_inches='tight', transparent=True)
    plt.close('all')
    print('wrote', name + '.svg')


# --- cell 0 --------------------------------------------------
import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

# Create the graph
edges = [(0,1), (0,3), (1,2), (1,3), (1,4), (2,4), (2,7), (3,4), (3,5), (4,5), (5,6), (6,8), (8,9)]
g = ig.Graph(edges=edges, directed=False)
g.vs["label"] = range(g.vcount())
layout = g.layout("fr")

# Plotting function
def plot_centrality(g, scores, title):
    fig, ax = plt.subplots(figsize=(4, 3))
    cmap = plt.cm.magma

    # Handle cases where all scores are the same
    min_score, max_score = np.min(scores), np.max(scores)
    if min_score == max_score:
        normalized_scores = np.ones_like(scores)
    else:
        normalized_scores = (np.array(scores) - min_score) / (max_score - min_score)

    vertex_color = [cmap(s) for s in normalized_scores]

    ig.plot(
        g,
        target=ax,
        layout=layout,
        vertex_size=20,
        vertex_color=vertex_color,
        vertex_label_color="black",
        vertex_label_dist=0,
        vertex_label_size=10
    )

    ax.set_title(title, fontsize=12)

    # Add a colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_score, vmax=max_score))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label("Centrality", rotation=270, labelpad=15)

    #return fig

# --- cell 1 --------------------------------------------------
# caption: Closeness Centrality Visualization. Nodes with higher centrality (brighter colors) are closer to all other nodes on average.
scores = g.closeness()
plot_centrality(g, scores, "Closeness Centrality")
_save('closeness')

# --- cell 2 --------------------------------------------------
# caption: Harmonic Centrality Visualization. A variant of closeness that works well with disconnected components.
scores = g.harmonic_centrality()
plot_centrality(g, scores, "Harmonic Centrality")
_save('harmonic')

# --- cell 3 --------------------------------------------------
# caption: Eccentricity Centrality Visualization. High-centrality nodes (brighter colors) have the smallest maximum distance to any other node.
scores = g.eccentricity()
# Eccentricity is a distance, so lower is better. We plot 1/eccentricity for centrality.
plot_centrality(g, [1/e if e > 0 else 0 for e in scores], "Eccentricity Centrality (1/eccentricity)")
_save('eccentricity')

# --- cell 4 --------------------------------------------------
# caption: Betweenness Centrality Visualization. Brighter nodes lie on a larger number of shortest paths between other nodes.
scores = g.betweenness()
plot_centrality(g, scores, "Betweenness Centrality")
_save('betweenness')

# --- cell 5 --------------------------------------------------
# caption: Eigenvector Centrality Visualization. Brighter nodes are connected to other highly central nodes.
scores = g.eigenvector_centrality()
plot_centrality(g, scores, "Eigenvector Centrality")
_save('eigenvector')

# --- cell 6 --------------------------------------------------
# caption: Katz Centrality Visualization. A measure of influence that accounts for both direct and indirect connections.
import numpy as np

# Get adjacency matrix
A = np.array(g.get_adjacency().data)
n = g.vcount()
I = np.identity(n)

# Set parameters for Katz centrality
# Alpha must be less than 1 / largest eigenvalue of A
eigenvalues = np.linalg.eigvals(A)
alpha = 0.9 / np.max(np.abs(eigenvalues))
beta = 1.0

# Calculate Katz centrality scores
scores = np.linalg.inv(I - alpha * A.T) @ np.ones(n) * beta

plot_centrality(g, scores.tolist(), "Katz Centrality")
_save('katz')

# --- cell 7 --------------------------------------------------
# caption: PageRank Centrality Visualization. Brighter nodes have a higher probability of being visited by a random walker.
scores = g.pagerank()
plot_centrality(g, scores, "PageRank")
_save('pagerank')

# --- cell 8 --------------------------------------------------
# caption: Degree Centrality Visualization. The simplest measure: brighter nodes have more direct connections.
scores = g.degree()
plot_centrality(g, scores, "Degree Centrality")
_save('degree')
