"""Two helpers for the M07 mini-project. Use them, change them, or ignore them."""

import numpy as np
import scipy.sparse as sp


def to_adjacency(edges):
    """Edge table (columns source, target; each edge listed once) -> sparse
    symmetric adjacency matrix A, with A[i, j] = 1 if i and j are linked."""
    n = int(edges[["source", "target"]].to_numpy().max()) + 1
    A = sp.coo_matrix(
        (np.ones(len(edges)), (edges["source"], edges["target"])), shape=(n, n)
    )
    return (A + A.T).tocsr()


def random_walk(A, start, length, rng=None):
    """The nodes visited by one random walk: `start`, then `length` steps.
    At each step the walker moves to a neighbour chosen uniformly at random."""
    rng = rng if rng is not None else np.random.default_rng()
    walk = [start]
    for _ in range(length):
        v = walk[-1]
        neighbors = A.indices[A.indptr[v] : A.indptr[v + 1]]
        walk.append(int(rng.choice(neighbors)))
    return walk


def transition_matrix(A):
    """P[i, j] = probability that a walker at i moves to j in one step.
    Row i of A divided by the degree of i, so every row of P sums to 1."""
    degree = np.asarray(A.sum(axis=1)).ravel()
    return sp.diags(1.0 / degree) @ A
