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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assignment.assignment import compute_degree_ccdf, compute_degree_distribution

# %% Test ------------
print("=" * 50)
print("Testing Task 3: compute_degree_ccdf")
print("=" * 50)

# ------------------------------------------------------------
# Test 1: Simple known distribution
# ------------------------------------------------------------
print("\n[Test 1] Simple degree distribution")
# Test with degree distribution [0, 0.5, 0.3, 0.2] for degrees [0,1,2,3]
deg_dist = np.array([0.0, 0.5, 0.3, 0.2])
ccdf = compute_degree_ccdf(deg_dist)

# CCDF(k) = P(degree > k)
# CCDF(0) = P(degree > 0) = 0.5 + 0.3 + 0.2 = 1.0
# CCDF(1) = P(degree > 1) = 0.3 + 0.2 = 0.5  
# CCDF(2) = P(degree > 2) = 0.2
# CCDF(3) = P(degree > 3) = 0.0
expected_ccdf = np.array([1.0, 0.5, 0.2, 0.0])

print(f"Input distribution: {deg_dist}")
print(f"Computed CCDF: {ccdf}")
print(f"Expected CCDF: {expected_ccdf}")

assert len(ccdf) == len(expected_ccdf), f"Wrong CCDF length: {len(ccdf)} vs {len(expected_ccdf)}"
assert np.allclose(ccdf, expected_ccdf), f"CCDF mismatch: {ccdf} vs {expected_ccdf}"
print("✓ Simple distribution test passed")

# ------------------------------------------------------------
# Test 2: Star graph CCDF
# ------------------------------------------------------------
print("\n[Test 2] Star graph CCDF")
g_star = igraph.Graph.Star(5, mode="undirected")
deg_dist = compute_degree_distribution(g_star)
ccdf = compute_degree_ccdf(deg_dist)

# Star has distribution [0, 0.8, 0, 0, 0.2] for degrees [0,1,2,3,4]
# CCDF should be [1.0, 0.2, 0.2, 0.2, 0.0]
expected_ccdf = np.array([1.0, 0.2, 0.2, 0.2, 0.0])

print(f"Star degree distribution: {deg_dist}")
print(f"Computed CCDF: {ccdf}")
print(f"Expected CCDF: {expected_ccdf}")

assert np.allclose(ccdf, expected_ccdf), f"Star CCDF mismatch: {ccdf} vs {expected_ccdf}"
print("✓ Star graph CCDF test passed")

# ------------------------------------------------------------
# Test 3: Monotonicity property
# ------------------------------------------------------------
print("\n[Test 3] CCDF monotonicity")
g_random = igraph.Graph.Erdos_Renyi(n=100, p=0.05)
deg_dist = compute_degree_distribution(g_random)
ccdf = compute_degree_ccdf(deg_dist)

print(f"CCDF length: {len(ccdf)}")
print(f"First few CCDF values: {ccdf[:min(10, len(ccdf))]}")

# CCDF should be monotonically decreasing
for i in range(len(ccdf) - 1):
    assert ccdf[i] >= ccdf[i+1], f"CCDF not monotonic at index {i}: {ccdf[i]} < {ccdf[i+1]}"

print("✓ Monotonicity test passed")

# ------------------------------------------------------------
# Test 4: Boundary conditions
# ------------------------------------------------------------
print("\n[Test 4] CCDF boundary conditions")

# First value should be ≤ 1.0 (fraction cannot exceed 1)
assert ccdf[0] <= 1.0, f"CCDF[0] exceeds 1.0: {ccdf[0]}"

# Last value should be 0.0 (no nodes have degree greater than max degree)
assert np.isclose(ccdf[-1], 0.0), f"CCDF[-1] should be 0.0: {ccdf[-1]}"

# All values should be non-negative
assert np.all(ccdf >= 0), f"CCDF has negative values: {ccdf[ccdf < 0]}"

print(f"CCDF[0] = {ccdf[0]:.6f} (≤ 1.0)")
print(f"CCDF[-1] = {ccdf[-1]:.6f} (≈ 0.0)")
print(f"All values ≥ 0: {np.all(ccdf >= 0)}")
print("✓ Boundary conditions test passed")

# ------------------------------------------------------------
# Test 5: Relationship to CDF
# ------------------------------------------------------------
print("\n[Test 5] CCDF = 1 - CDF relationship")
cdf = np.cumsum(deg_dist)
# CCDF should equal 1 - CDF[:-1] (excluding last CDF element which is 1.0)
expected_ccdf_from_cdf = 1.0 - cdf[:-1]

print(f"CCDF from function: {ccdf[:5]}")
print(f"1 - CDF[:-1]: {expected_ccdf_from_cdf[:5]}")

assert np.allclose(ccdf, expected_ccdf_from_cdf), f"CCDF ≠ 1 - CDF relationship violated"
print("✓ CDF relationship test passed")

print("\n" + "=" * 50)
print("All Task 3 tests passed! ✓")
print("=" * 50)