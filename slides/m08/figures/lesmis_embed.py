# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["gensim>=4.3", "networkx>=3.0", "numpy>=1.26", "pandas>=2.0", "scikit-learn>=1.3"]
# ///
"""Embed Les Miserables as in the lab notebook and write 2-D PCA coordinates to lesmis_pca.json.
Run once:  uv run figures/lesmis_embed.py   (make_figures.py reads the json)."""
import json, random
from pathlib import Path

import networkx as nx
import pandas as pd
from gensim.models import Word2Vec
from sklearn.decomposition import PCA

D = Path(__file__).resolve().parents[3] / "lecture-note/assets/data/lesmis"
nodes, edges = pd.read_csv(D / "node_table.csv"), pd.read_csv(D / "edge_table.csv")
ids = dict(zip(nodes["node_id"], nodes["name"]))
G = nx.Graph()
G.add_nodes_from(nodes["name"])
G.add_weighted_edges_from((ids[s], ids[t], w) for s, t, w in zip(edges["src"], edges["trg"], edges["weight"]))
rng = random.Random(0)
walks = []
for v in G:
    for _ in range(10):
        w = [v]
        while len(w) < 40:
            w.append(rng.choice(list(G[w[-1]])))
        walks.append(w)
wv = Word2Vec(walks, vector_size=32, window=5, min_count=1, sg=1, hs=0, negative=5, epochs=20, sample=0, workers=1, seed=0).wv
xy = PCA(2, random_state=0).fit_transform(wv.vectors)
out = {k: [float(xy[i][0]), float(xy[i][1])] for i, k in enumerate(wv.index_to_key)}
near = [k for k, _ in wv.most_similar("Valjean", topn=10)]
Path(__file__).with_name("lesmis_pca.json").write_text(json.dumps({"xy": out, "near_valjean": near, "n_edges_total": G.number_of_edges()}))
print(len(out), near)
