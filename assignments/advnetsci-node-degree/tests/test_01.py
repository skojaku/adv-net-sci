# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6", 
#     "python-igraph==0.11.9",
#     "scipy",
# ]
# ///

# %% Import
import numpy as np
import sys
import os
import igraph
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assignment.assignment import compute_degree_distribution

# %% Test ------------
# Test with known degree sequences
print("=" * 50)
print("Testing Task 1: compute_degree_distribution")
print("=" * 50)

# ------------------------------------------------------------
# Test 1: Simple star graph
# ------------------------------------------------------------
print("\n[Test 1] Star graph with 5 nodes")
g_star = igraph.Graph.Star(5, mode="undirected")
deg_dist = compute_degree_distribution(g_star)

# Expected: 1 center node (degree 4), 4 leaf nodes (degree 1)
# Distribution should be [0, 4/5, 0, 0, 1/5] for degrees [0,1,2,3,4]
expected_star = np.array([0.0, 0.8, 0.0, 0.0, 0.2])

print(f"Computed: {deg_dist}")
print(f"Expected: {expected_star}")
assert len(deg_dist) == len(expected_star), f"Wrong length: {len(deg_dist)} vs {len(expected_star)}"
assert np.allclose(deg_dist, expected_star), f"Star distribution mismatch: {deg_dist} vs {expected_star}"
print("✓ Star graph test passed")

# ------------------------------------------------------------  
# Test 2: Complete graph
# ------------------------------------------------------------
print("\n[Test 2] Complete graph with 4 nodes")
g_complete = igraph.Graph.Full(4)
deg_dist = compute_degree_distribution(g_complete)

# All nodes have degree 3
expected_complete = np.array([0.0, 0.0, 0.0, 1.0])

print(f"Computed: {deg_dist}")
print(f"Expected: {expected_complete}")
assert np.allclose(deg_dist, expected_complete), f"Complete graph distribution mismatch: {deg_dist} vs {expected_complete}"
print("✓ Complete graph test passed")

# ------------------------------------------------------------
# Test 3: Graph with isolated nodes
# ------------------------------------------------------------
print("\n[Test 3] Graph with isolated nodes")
g_isolated = igraph.Graph(6)  # 6 nodes, no edges
g_isolated.add_edges([(0, 1), (2, 3)])  # Add 2 edges

deg_dist = compute_degree_distribution(g_isolated)

# 2 isolated nodes (degree 0), 4 connected nodes (degree 1)
expected_isolated = np.array([2.0/6.0, 4.0/6.0])

print(f"Computed: {deg_dist}")
print(f"Expected: {expected_isolated}")
assert np.allclose(deg_dist, expected_isolated), f"Isolated nodes distribution mismatch: {deg_dist} vs {expected_isolated}"
print("✓ Isolated nodes test passed")

# ------------------------------------------------------------
# Test 4: Sum to 1 property
# ------------------------------------------------------------
print("\n[Test 4] Distribution sums to 1")
g_random = igraph.Graph.Erdos_Renyi(n=100, p=0.05)
deg_dist = compute_degree_distribution(g_random)

total_prob = np.sum(deg_dist)
print(f"Sum of probabilities: {total_prob}")
assert np.isclose(total_prob, 1.0), f"Distribution should sum to 1: {total_prob}"
print("✓ Probability sum test passed")

print("\n" + "=" * 50)
print("All Task 1 tests passed! ✓")
print("=" * 50)