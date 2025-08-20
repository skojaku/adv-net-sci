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
from assignment.assignment import compute_ccdf


np.random.seed(42)
n_nodes = 500
g = igraph.Graph.Barabasi(n=n_nodes, m=2)
degree = np.array(g.degree())

CCDF = compute_ccdf(degree)

# Sort CCDF by x values
sorted_ccdf = sorted(CCDF, key=lambda point: point[0])
x_vals, ccdf_vals = zip(*sorted_ccdf)

# %% Test ------------
print("="*60)
# ------------------------------------------------------------
# Test 1: Check the monotonicity of the CCDF
# ------------------------------------------------------------
ccdf_diffs = np.diff(ccdf_vals)
non_decreasing_indices = np.where(ccdf_diffs >= 0)[0]

assert np.all(ccdf_diffs < 0), (
    f"CCDF must be monotonically decreasing (each value should be smaller than the previous). "
    f"Found {len(non_decreasing_indices)} violations at positions: {non_decreasing_indices}. "
    f"Problematic differences: {ccdf_diffs[non_decreasing_indices]}. "
    f"This usually indicates an error in the CCDF computation logic."
)
print("✓ Subtest 1 PASSED: CCDF is monotonically decreasing")

# ------------------------------------------------------------
# Test 2: Check the CCDF values
# ------------------------------------------------------------
x_test = [0, n_nodes + 1]
y_expected = [1, 0]

degree_sorted = np.sort(degree)
for q in [0.1, 0.3, 0.5, 0.7, 0.9]:
    dth = degree_sorted[int(q * (n_nodes - 1))]
    x_test.append(dth)
    y_expected.append(np.mean(degree > dth))

y_actual = np.interp(x_test, x_vals, ccdf_vals)

errors = []
for i in range(len(x_test)):
    error = abs(y_actual[i] - y_expected[i])
    errors.append(error)
    assert np.allclose(y_actual[i], y_expected[i], atol=1e-6), (
        f"CCDF value mismatch at degree {x_test[i]}: "
        f"Got {y_actual[i]:.6f}, expected {y_expected[i]:.6f} "
        f"(error: {error:.6f}). "
        f"This suggests the CCDF computation is incorrect. "
        f"Remember: CCDF(x) = P(degree > x) = fraction of nodes with degree strictly greater than x."
    )
max_error = max(errors)
print(f"✓ Subtest 2 PASSED: CCDF values correct at {len(x_test)} test points (max error: {max_error:.2e})")

# ------------------------------------------------------------
# Test 3: Check that CCDF is defined as P(X>theta), not P(X>=theta)
# ------------------------------------------------------------
# Find a degree value that appears multiple times in the data
unique_degrees, counts = np.unique(degree, return_counts=True)
repeated_degrees = unique_degrees[counts > 1]

if len(repeated_degrees) > 0:
    # Pick a degree that appears multiple times
    test_degree = repeated_degrees[0]

    # Get CCDF value at this degree
    ccdf_at_degree = np.interp(test_degree, x_vals, ccdf_vals)

    # Correct definition: P(X > theta) - should exclude ties
    expected_correct = np.mean(degree > test_degree)

    # Incorrect definition: P(X >= theta) - would include ties
    expected_incorrect = np.mean(degree >= test_degree)

    # The two should be different if there are ties
    if expected_correct != expected_incorrect:
        # CCDF should match the correct definition (excludes ties)
        error = abs(ccdf_at_degree - expected_correct)
        assert np.allclose(ccdf_at_degree, expected_correct, atol=1e-6), (
            f"CCDF definition error detected! "
            f"\n• Test degree: {test_degree} (appears {counts[unique_degrees == test_degree][0]} times in dataset)"
            f"\n• Your CCDF value: {ccdf_at_degree:.6f}"
            f"\n• Expected (P(X > {test_degree})): {expected_correct:.6f}"
            f"\n• Wrong definition (P(X >= {test_degree})): {expected_incorrect:.6f}"
            f"\n• Error: {error:.6f}"
            f"\n\nYour CCDF appears to be using P(X >= theta) instead of P(X > theta). "
            f"The correct definition excludes ties (nodes with exactly degree {test_degree})."
        )
else:
    print("⚠ Test 3 SKIPPED: No repeated degrees found in the dataset")

if len(repeated_degrees) > 0:
    print("✓ Subtest 3 PASSED: CCDF correctly uses P(X > theta) definition")

print("="*60)
print("🎉 All subtests passed! Your CCDF implementation is correct.")


