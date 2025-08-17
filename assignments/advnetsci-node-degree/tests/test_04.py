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
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assignment.assignment import sample_degree_biased_nodes

# %% Test ------------
print("=" * 50)
print("Testing Task 4: sample_degree_biased_nodes")
print("=" * 50)

# ------------------------------------------------------------
# Test 1: Star graph bias test
# ------------------------------------------------------------
print("\n[Test 1] Star graph degree bias")
np.random.seed(42)
g_star = igraph.Graph.Star(5, mode="undirected")

# Sample many nodes to test bias
num_samples = 10000
sampled_nodes = sample_degree_biased_nodes(g_star, num_samples)

print(f"Sampled {len(sampled_nodes)} nodes from star graph")

# Count how often each node is sampled
sample_counts = Counter(sampled_nodes)
print(f"Sample counts: {dict(sample_counts)}")

# In star graph: node 0 has degree 4, nodes 1-4 have degree 1
# Node 0 should be sampled ~4x more often than other nodes
center_samples = sample_counts[0]
leaf_samples = [sample_counts[i] for i in range(1, 5)]
avg_leaf_samples = np.mean(leaf_samples)

bias_ratio = center_samples / avg_leaf_samples
print(f"Center node samples: {center_samples}")
print(f"Average leaf samples: {avg_leaf_samples:.1f}")
print(f"Bias ratio: {bias_ratio:.2f} (expected ~4.0)")

# Center should be sampled roughly 4x more (within statistical tolerance)
assert bias_ratio > 3.0, f"Bias ratio too low: {bias_ratio}, expected > 3.0"
assert bias_ratio < 5.0, f"Bias ratio too high: {bias_ratio}, expected < 5.0"
print("✓ Star graph bias test passed")

# ------------------------------------------------------------
# Test 2: Complete graph (no bias)
# ------------------------------------------------------------
print("\n[Test 2] Complete graph (uniform sampling)")
np.random.seed(42)
g_complete = igraph.Graph.Full(4)

num_samples = 8000  # Multiple of 4 for clean expected counts
sampled_nodes = sample_degree_biased_nodes(g_complete, num_samples)

sample_counts = Counter(sampled_nodes)
print(f"Sample counts: {dict(sample_counts)}")

# All nodes have same degree, so should be sampled roughly equally
expected_per_node = num_samples / 4
for node in range(4):
    count = sample_counts[node]
    deviation = abs(count - expected_per_node) / expected_per_node
    print(f"Node {node}: {count} samples (deviation: {deviation:.3f})")
    assert deviation < 0.1, f"Too much deviation for node {node}: {deviation}"

print("✓ Complete graph uniform test passed")

# ------------------------------------------------------------
# Test 3: Sample count correctness
# ------------------------------------------------------------
print("\n[Test 3] Sample count correctness")
g_test = igraph.Graph.Erdos_Renyi(n=20, p=0.1)

num_samples = 100
sampled_nodes = sample_degree_biased_nodes(g_test, num_samples)

print(f"Requested {num_samples} samples, got {len(sampled_nodes)}")
assert len(sampled_nodes) == num_samples, f"Wrong number of samples: {len(sampled_nodes)} vs {num_samples}"

# All sampled nodes should be valid node indices
assert all(0 <= node < g_test.vcount() for node in sampled_nodes), "Invalid node indices in sample"
print("✓ Sample count test passed")

# ------------------------------------------------------------
# Test 4: Degree bias correlation
# ------------------------------------------------------------
print("\n[Test 4] Degree bias correlation")
np.random.seed(123)
g_ba = igraph.Graph.Barabasi(n=100, m=2)  # Scale-free network

num_samples = 20000
sampled_nodes = sample_degree_biased_nodes(g_ba, num_samples)

# Count sampling frequency for each node
sample_counts = Counter(sampled_nodes)
degrees = g_ba.degree()

# Calculate correlation between node degree and sampling frequency
nodes_with_samples = list(sample_counts.keys())
node_degrees = [degrees[node] for node in nodes_with_samples]
sample_frequencies = [sample_counts[node] for node in nodes_with_samples]

# Compute correlation coefficient
correlation = np.corrcoef(node_degrees, sample_frequencies)[0, 1]
print(f"Correlation between degree and sample frequency: {correlation:.3f}")

# Should be strong positive correlation (> 0.8)
assert correlation > 0.8, f"Correlation too weak: {correlation}, expected > 0.8"
print("✓ Degree bias correlation test passed")

# ------------------------------------------------------------
# Test 5: Edge-based sampling property
# ------------------------------------------------------------
print("\n[Test 5] Edge-based sampling verification")
g_test = igraph.Graph.Erdos_Renyi(n=50, p=0.1, seed=42)

if g_test.ecount() > 0:  # Only test if graph has edges
    num_samples = 5000
    sampled_nodes = sample_degree_biased_nodes(g_test, num_samples)
    
    # Calculate theoretical expected frequency for each node
    # In edge-based sampling, P(sample node i) = degree(i) / (2 * num_edges)
    total_degree = sum(g_test.degree())
    expected_frequencies = {}
    for node in range(g_test.vcount()):
        if g_test.degree(node) > 0:  # Only nodes with edges can be sampled
            expected_frequencies[node] = g_test.degree(node) / total_degree
    
    # Calculate actual frequencies
    sample_counts = Counter(sampled_nodes)
    actual_frequencies = {}
    for node in sample_counts:
        actual_frequencies[node] = sample_counts[node] / num_samples
    
    # Check that nodes with degree 0 are never sampled
    isolated_nodes = [i for i in range(g_test.vcount()) if g_test.degree(i) == 0]
    for node in isolated_nodes:
        assert node not in sample_counts, f"Isolated node {node} was sampled"
    
    print(f"Isolated nodes correctly excluded: {len(isolated_nodes)} nodes")
    print("✓ Edge-based sampling verification passed")
else:
    print("⚠ Graph has no edges, skipping edge-based sampling test")

print("\n" + "=" * 50)
print("All Task 4 tests passed! ✓")
print("=" * 50)