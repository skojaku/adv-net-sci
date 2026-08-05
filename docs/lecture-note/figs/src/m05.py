"""Regenerate the static figures for this module.

Extracted from docs/lecture-note/m05-clustering/01-concepts.qmd.
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


def _sbm(n, pref_matrix, block_sizes):
    """Build an SBM across python-igraph versions.

    python-igraph 1.0 dropped the leading `n` argument from Graph.SBM, since
    the block sizes already determine the vertex count.
    """
    try:
        return igraph.Graph.SBM(pref_matrix, block_sizes)          # >= 1.0
    except TypeError:
        return igraph.Graph.SBM(n, pref_matrix, block_sizes)       # < 1.0



# --- cell 0 --------------------------------------------------
# caption: Adjacency Matrix of Stochastic Block Model
import numpy as np
import matplotlib.pyplot as plt

import igraph

# Generate SBM
n, k = 900, 3

# Create block sizes (equal for simplicity)
block_sizes = [n // k] * k

# Create diverse pref matrix
pref_matrix = [
    [0.3, 0.05, 0.1],
    [0.05, 0.4, 0.02],
    [0.1, 0.02, 0.35]
]

# Generate SBM using igraph
g = _sbm(n, pref_matrix, block_sizes)

# Convert to adjacency matrix for visualization
A = np.array(g.get_adjacency().data)

# Plot
plt.figure(figsize=(8, 8))
plt.imshow(A, cmap='binary')
plt.title("Adjacency Matrix of Stochastic Block Model")
plt.xlabel("Node Index")
plt.ylabel("Node Index")
plt.tight_layout()
plt.show()
_save('sbm-adjacency-matrix')

# --- cell 1 --------------------------------------------------
# caption: Schematic of Likelihood Function (Concave)
import numpy as np
import matplotlib.pyplot as plt

def concave_function(x):
    return -(x - 0.5)**2 + 0.25

x = np.linspace(0, 1, 100)
y = concave_function(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Schematic of Likelihood Function (Concave)')
plt.xlabel('Edge Probability p_c,c\'')
plt.ylabel('Likelihood')
plt.axvline(x=0.5, color='r', linestyle='--', label='Maximum')
plt.annotate('Global Maximum', xy=(0.5, 0.25), xytext=(0.6, 0.2),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend()
plt.grid(True)
plt.show()
_save('likelihood-function')

# --- cell 2 --------------------------------------------------
# caption: Adjacency Matrix of Stochastic Block Model
import numpy as np
import matplotlib.pyplot as plt
import igraph

# Generate SBM
n, k = 900, 3

# Create block sizes (equal for simplicity)
block_sizes = [n // k] * k

# Create diverse pref matrix
pref_matrix = [
    [0.3, 0.05, 0.1],
    [0.05, 0.4, 0.02],
    [0.1, 0.02, 0.35]
]

# Generate SBM using igraph
g = _sbm(n, pref_matrix, block_sizes)

# Convert to adjacency matrix for visualization
A = np.array(g.get_adjacency().data)

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Plot the adjacency matrix
ax.matshow(A, cmap='binary')
mask = np.triu(np.ones_like(A, dtype=bool), k=1)

# Highlight the upper triangle with yellow overlay
ax.matshow(np.ma.masked_array(np.ones_like(A), ~mask), cmap='Reds_r', alpha=0.3)

# Add a title
plt.title("Adjacency Matrix with Highlighted Upper Triangle")

plt.show()
_save('adjacency-matrix')
