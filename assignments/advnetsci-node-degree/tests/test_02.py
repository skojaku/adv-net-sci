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

from assignment.assignment import compute_friendship_paradox_stats

# %% Test ------------
print("=" * 50)
print("Testing Task 2: compute_friendship_paradox_stats")
print("=" * 50)

# ------------------------------------------------------------
# Test 1: Star graph - classic friendship paradox example
# ------------------------------------------------------------
print("\n[Test 1] Star graph friendship paradox")
g_star = igraph.Graph.Star(5, mode="undirected")

avg_node_deg, avg_friend_deg = compute_friendship_paradox_stats(g_star)

# Star: 1 center (degree 4), 4 leaves (degree 1)
# Average node degree = (4 + 1 + 1 + 1 + 1) / 5 = 1.6
expected_node_avg = 1.6

# All edges connect leaves to center, so all "friends" have degree 4
expected_friend_avg = 4.0

print(f"Average node degree: {avg_node_deg:.3f} (expected: {expected_node_avg})")
print(f"Average friend degree: {avg_friend_deg:.3f} (expected: {expected_friend_avg})")

assert np.isclose(avg_node_deg, expected_node_avg), f"Node average mismatch: {avg_node_deg} vs {expected_node_avg}"
assert np.isclose(avg_friend_deg, expected_friend_avg), f"Friend average mismatch: {avg_friend_deg} vs {expected_friend_avg}"
print("✓ Star graph test passed")

# ------------------------------------------------------------
# Test 2: Complete graph - no friendship paradox
# ------------------------------------------------------------
print("\n[Test 2] Complete graph (no paradox)")
g_complete = igraph.Graph.Full(4)

avg_node_deg, avg_friend_deg = compute_friendship_paradox_stats(g_complete)

# In complete graph, all nodes have same degree, so no paradox
# All nodes have degree 3
expected_both = 3.0

print(f"Average node degree: {avg_node_deg:.3f} (expected: {expected_both})")
print(f"Average friend degree: {avg_friend_deg:.3f} (expected: {expected_both})")

assert np.isclose(avg_node_deg, expected_both), f"Node average mismatch: {avg_node_deg} vs {expected_both}"
assert np.isclose(avg_friend_deg, expected_both), f"Friend average mismatch: {avg_friend_deg} vs {expected_both}"
print("✓ Complete graph test passed")

# ------------------------------------------------------------
# Test 3: Friendship paradox property
# ------------------------------------------------------------
print("\n[Test 3] Friendship paradox inequality")
# Test on a scale-free network which should show strong paradox
np.random.seed(42)
g_ba = igraph.Graph.Barabasi(n=1000, m=2)

avg_node_deg, avg_friend_deg = compute_friendship_paradox_stats(g_ba)

print(f"Average node degree: {avg_node_deg:.3f}")
print(f"Average friend degree: {avg_friend_deg:.3f}")
print(f"Paradox ratio: {avg_friend_deg/avg_node_deg:.3f}")

# Friends should have higher average degree (friendship paradox)
assert avg_friend_deg > avg_node_deg, f"Friendship paradox violated: {avg_friend_deg} <= {avg_node_deg}"

# The ratio should be substantial for scale-free networks
paradox_ratio = avg_friend_deg / avg_node_deg
assert paradox_ratio > 1.2, f"Paradox ratio too small for scale-free network: {paradox_ratio}"
print("✓ Friendship paradox inequality test passed")

# ------------------------------------------------------------
# Test 4: Edge consistency check
# ------------------------------------------------------------
print("\n[Test 4] Edge count consistency")
g_test = igraph.Graph.Erdos_Renyi(n=50, p=0.1)

avg_node_deg, avg_friend_deg = compute_friendship_paradox_stats(g_test)

# Average node degree should equal 2 * edges / nodes
expected_node_avg = 2.0 * g_test.ecount() / g_test.vcount()

print(f"Computed node average: {avg_node_deg:.6f}")
print(f"Expected from edge count: {expected_node_avg:.6f}")

assert np.isclose(avg_node_deg, expected_node_avg), f"Node degree inconsistent with edge count: {avg_node_deg} vs {expected_node_avg}"
print("✓ Edge consistency test passed")

print("\n" + "=" * 50)
print("All Task 2 tests passed! ✓")
print("=" * 50)