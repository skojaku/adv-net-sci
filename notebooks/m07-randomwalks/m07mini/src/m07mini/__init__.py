"""Data and scoring for the M07 mini-project.

    import m07mini
    edges = m07mini.load_edges()        # {"net1": DataFrame, "net2": ..., "net3": ...}
    groups = m07mini.load_groups()      # the ground truth, same keys
    m07mini.evaluate({"net1": labels})  # NMI per network
"""

import base64
import io
import zlib

import pandas as pd
from sklearn.metrics import normalized_mutual_info_score

from ._data import NETWORKS

__all__ = ["load_edges", "load_groups", "evaluate"]


def _table(name, table):
    text = zlib.decompress(base64.b64decode(NETWORKS[name][table])).decode()
    return pd.read_csv(io.StringIO(text))


def load_edges():
    """Edge table of each network: columns source and target, one row per undirected edge."""
    return {name: _table(name, "edges") for name in NETWORKS}


def load_groups():
    """Ground truth of each network: columns node and group."""
    return {name: _table(name, "groups") for name in NETWORKS}


def evaluate(answer):
    """Score a community detection result.

    answer maps a network name to one group label per node, in node-id order, for
    example {"net1": [0, 0, 1, ...], "net3": [...]}. Any subset of the networks
    may be given. Returns the normalized mutual information with the ground
    truth, per network: 1 for identical groupings, near 0 for unrelated ones.
    """
    unknown = sorted(set(answer) - set(NETWORKS))
    if unknown:
        raise ValueError(f"unknown network {unknown}; the networks are {list(NETWORKS)}")
    scores = {}
    for name, labels in answer.items():
        truth = _table(name, "groups")["group"].to_numpy()
        labels = list(labels)
        if len(labels) != len(truth):
            raise ValueError(f"{name}: expected {len(truth)} labels, got {len(labels)}")
        scores[name] = round(float(normalized_mutual_info_score(truth, labels)), 3)
    return scores
