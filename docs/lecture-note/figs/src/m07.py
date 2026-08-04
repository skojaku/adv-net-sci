"""Regenerate the static figures for this module.

Extracted from docs/lecture-note/m07-random-walks/01-concepts.qmd.
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
import numpy as np
import matplotlib.pyplot as plt
import igraph as ig
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

# Set style
plt.style.use('default')
sns.set_palette("husl")

# Create the larger network
edges = [(0,1), (0,3), (1,2), (1,3), (1,4), (2,4), (2,7), (3,4), (3,5), (4,5), (5,6), (6,8), (8,9)]
n_nodes = 10
G = ig.Graph(n=n_nodes, edges=edges, directed=False)

# Create adjacency matrix
A = np.array(G.get_adjacency().data)

# Calculate degrees
degrees = np.array(G.degree())

# Create transition matrix
P = np.diag(1.0 / degrees) @ A

# Find a node with highest degree for example
max_degree_node = np.argmax(degrees)
_save('m07-fig-00')

# --- cell 1 --------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
ig.plot(G, target=ax, vertex_label=list(range(n_nodes)))
_save('m07-fig-01')

# --- cell 2 --------------------------------------------------
import pandas as pd
plt.figure(figsize=(6,5))
sns.heatmap(P, annot=True, fmt=".2f", cmap="YlGnBu",
            xticklabels=list(range(n_nodes)), yticklabels=list(range(n_nodes)))
plt.title("Transition Matrix Heatmap")
plt.xlabel("To Node")
plt.ylabel("From Node")
plt.show()
_save('m07-fig-02')

# --- cell 3 --------------------------------------------------
# Use the same network and transition matrix from previous example
P2 = P @ P  # Matrix multiplication for 2-step transitions
plt.figure(figsize=(6,5))
sns.heatmap(P2, annot=True, fmt=".2f", cmap="YlGnBu",
            xticklabels=list(range(n_nodes)), yticklabels=list(range(n_nodes)))
plt.title("Transition Matrix Heatmap")
plt.xlabel("To Node")
plt.ylabel("From Node")
plt.show()
_save('m07-fig-03')

# --- cell 4 --------------------------------------------------
# Use the same network and transition matrix from previous example
P100 = np.linalg.matrix_power(P, 10)   # Matrix multiplication for 2-step transitions
plt.figure(figsize=(6,5))
sns.heatmap(P100, annot=True, fmt=".2f", cmap="YlGnBu",
            xticklabels=list(range(n_nodes)), yticklabels=list(range(n_nodes)))
plt.title("Transition Matrix Heatmap")
plt.xlabel("To Node")
plt.ylabel("From Node")
plt.show()
_save('m07-fig-04')

# --- cell 5 --------------------------------------------------
# caption: Transition Matrix after 100 steps
P100 = np.linalg.matrix_power(P, 100)   # Matrix multiplication for 100-step transitions
plt.figure(figsize=(6,5))
sns.heatmap(P100, annot=True, fmt=".2f", cmap="YlGnBu",
            xticklabels=list(range(n_nodes)), yticklabels=list(range(n_nodes)))
plt.title("Transition Matrix Heatmap")
plt.xlabel("To Node")
plt.ylabel("From Node")
plt.show()
_save('long-term-P')

# --- cell 6 --------------------------------------------------
# caption: Spectrum of Transition Matrix $P$
sns.set_style('white')
sns.set(font_scale=1.2)
sns.set_style('ticks')

# Compute the eigenvalues of the transition matrix P
eigenvalues = np.linalg.eigvals(P)

eigenvalues = np.sort(eigenvalues)[::-1]

# Plot the spectrum (distribution of eigenvalues) in the complex plane
fig, ax = plt.subplots(figsize=(6, 6))
sns.pointplot(x=np.arange(len(eigenvalues)), y=eigenvalues, ax=ax)

ax.set_xlabel("Index")
ax.set_ylabel("Eigenvalue")
ax.set_title("Spectrum of Transition Matrix $P$")

sns.despine(ax=ax)
plt.show()
_save('spectrum')
