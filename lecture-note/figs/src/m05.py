"""Regenerate the static figures for this module.

Extracted from lecture-note/m05-clustering/01-concepts.qmd.
Run from the repository root; writes SVGs into lecture-note/figs/.
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

ACCENT = '#593196'
CONTRAST = '#c2410c'
INK = '#2c2a3a'

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, color=ACCENT, linewidth=2.4)
ax.set_xlabel("Edge probability $p_{c,c'}$", color=INK)
ax.set_ylabel('Log-likelihood', color=INK)
ax.axvline(x=0.5, color=CONTRAST, linestyle='--', linewidth=1.4)
ax.annotate('single peak: zero gradient', xy=(0.52, 0.249), xytext=(0.70, 0.225),
            color=INK, ha='left', va='center',
            arrowprops=dict(color=INK, arrowstyle='->', linewidth=1.2))
ax.set_yticks([])
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
for side in ('left', 'bottom'):
    ax.spines[side].set_color(INK)
ax.tick_params(colors=INK)
plt.tight_layout()
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

# Wash the upper triangle - the region the sum over i < j runs over - in the
# course accent, so it reads as one highlighted region rather than a colour map.
accent_wash = matplotlib.colors.ListedColormap(['#593196'])
ax.matshow(np.ma.masked_array(np.ones_like(A), ~mask), cmap=accent_wash, alpha=0.30)

plt.show()
_save('adjacency-matrix')
