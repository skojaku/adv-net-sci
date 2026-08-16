"""Static figures for M08 (Embedding).

Run from the repository root; writes SVGs into lecture-note/figs/.
House palette: one ink, one accent (#593196), one contrast (#c2410c). No green.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
OUT.mkdir(parents=True, exist_ok=True)

INK = '#1f2328'
EDGE = '#c9ccd1'
ACCENT = '#593196'
CONTRAST = '#c2410c'


def _save(name):
    plt.savefig(OUT / f'{name}.svg', bbox_inches='tight', transparent=True)
    plt.close('all')
    print('wrote', name + '.svg')


# ---------------------------------------------------------------------------
# 1. The same 34 people, twice: wiring diagram -> map
# ---------------------------------------------------------------------------
G = nx.karate_club_graph()
faction = np.array([0 if G.nodes[i]['club'] == 'Mr. Hi' else 1 for i in G.nodes()])
colors = np.where(faction == 0, ACCENT, CONTRAST)

A = nx.to_numpy_array(G)
deg = A.sum(axis=1)
m = A.sum() / 2
Q = A - np.outer(deg, deg) / (2 * m)
vals, vecs = np.linalg.eigh(Q)
order = np.argsort(-vals)[:2]
xy = vecs[:, order] * np.sqrt(np.abs(vals[order]))

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))

pos = nx.spring_layout(G, seed=7)
nx.draw_networkx_edges(G, pos, ax=axes[0], edge_color=EDGE, width=0.9)
nx.draw_networkx_nodes(G, pos, ax=axes[0], node_color=colors,
                       node_size=110, linewidths=0)
axes[0].set_title('A wiring diagram:\nwho is connected to whom', fontsize=11, color=INK)
axes[0].axis('off')

axes[1].scatter(xy[:, 0], xy[:, 1], c=colors, s=60, linewidths=0)
axes[1].set_title('A map:\ntwo coordinates per person', fontsize=11, color=INK)
axes[1].set_xlabel('dimension 1', fontsize=9, color=INK)
axes[1].set_ylabel('dimension 2', fontsize=9, color=INK)
axes[1].tick_params(labelsize=8, colors=INK)
for s in ('top', 'right'):
    axes[1].spines[s].set_visible(False)
for s in ('left', 'bottom'):
    axes[1].spines[s].set_color(EDGE)

plt.tight_layout()
_save('m08-karate-to-map')


# ---------------------------------------------------------------------------
# 2. node2vec: the two things a walk from u can do
# ---------------------------------------------------------------------------
H = nx.Graph()
H.add_edges_from([
    ('u', 'a'), ('u', 'b'), ('u', 'c'), ('a', 'b'), ('b', 'c'),
    ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'g'), ('a', 'h'), ('h', 'i'),
])
hpos = {
    'u': (0, 0), 'a': (-0.9, 0.8), 'b': (0.0, 1.15), 'c': (0.95, 0.75),
    'd': (1.9, 1.2), 'e': (2.8, 0.8), 'f': (3.6, 1.3), 'g': (4.4, 0.9),
    'h': (-1.8, 1.4), 'i': (-2.6, 0.9),
}

bfs_nodes = ['u', 'a', 'b', 'c']
dfs_path = ['u', 'c', 'd', 'e', 'f', 'g']

fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.4))

for ax, title, marked, kind in [
    (axes[0], 'Large $q$: the walk circles back near $u$\nBFS-like, so $u$\'s vector describes its local role',
     bfs_nodes, 'set'),
    (axes[1], 'Small $q$: the walk keeps pushing outward\nDFS-like, so $u$\'s vector describes its community',
     dfs_path, 'path'),
]:
    nx.draw_networkx_edges(H, hpos, ax=ax, edge_color=EDGE, width=1.2)
    if kind == 'path':
        path_edges = list(zip(dfs_path[:-1], dfs_path[1:]))
        nx.draw_networkx_edges(H, hpos, edgelist=path_edges, ax=ax,
                               edge_color=CONTRAST, width=2.4)
    else:
        near_edges = [(x, y) for x, y in H.edges()
                      if x in marked and y in marked]
        nx.draw_networkx_edges(H, hpos, edgelist=near_edges, ax=ax,
                               edge_color=CONTRAST, width=2.4)
    node_colors = [CONTRAST if n in marked else EDGE for n in H.nodes()]
    nx.draw_networkx_nodes(H, hpos, ax=ax, node_color=node_colors,
                           node_size=330, linewidths=0)
    nx.draw_networkx_nodes(H, hpos, nodelist=['u'], ax=ax,
                           node_color=ACCENT, node_size=430, linewidths=0)
    nx.draw_networkx_labels(H, hpos, ax=ax, font_size=9, font_color='white')
    ax.set_title(title, fontsize=10, color=INK)
    ax.axis('off')

plt.tight_layout()
_save('m08-node2vec-pq')
