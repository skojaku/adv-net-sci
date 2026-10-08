# /// script
# dependencies = ["numpy", "pandas"]
# ///
"""The exact best two-way split of the seat network, for the lecturer's answer key.

    uv run exact_cuts.py seats.csv 3        # seats.csv, K = 3

Tries every split of the nodes into two non-empty groups (2^(N-1) of them; fine up to
about N = 22) and prints the one with the smallest Ratio cut and the one with the smallest
Normalized cut, with the same definitions as the pitch sheet. The network is built the way
the notebook builds it: each person joined to their K nearest people.
"""
import sys

import numpy as np
import pandas as pd

seats = pd.read_csv(sys.argv[1])
K = int(sys.argv[2])
P = seats[["x", "y"]].to_numpy(float)
N = len(P)
D = np.linalg.norm(P[:, None] - P[None], axis=2)
np.fill_diagonal(D, np.inf)
edges = {tuple(sorted((i, int(j)))) for i in range(N) for j in np.argsort(D[i], kind="stable")[:K]}
A = np.zeros((N, N))
for u, v in edges:
    A[u, v] = A[v, u] = 1
deg = A.sum(1)

best = {"Ratio cut": (np.inf, None), "Normalized cut": (np.inf, None)}
for mask in range(1, 2 ** (N - 1)):
    S = np.array([(mask >> i) & 1 for i in range(N)], bool)
    T = ~S
    if not T.any():
        continue
    cut = A[S][:, T].sum()
    ratio = cut / S.sum() + cut / T.sum()
    norm = cut / deg[S].sum() + cut / deg[T].sum() if deg[S].sum() and deg[T].sum() else np.inf
    if ratio < best["Ratio cut"][0] - 1e-12:
        best["Ratio cut"] = (ratio, S.copy())
    if norm < best["Normalized cut"][0] - 1e-12:
        best["Normalized cut"] = (norm, S.copy())
print(f"{N} nodes, {len(edges)} edges, K = {K}")
for name, (value, S) in best.items():
    print(f"{name}: {value:.4f}  group 1 = {[int(i) for i in np.where(S)[0]]}")
