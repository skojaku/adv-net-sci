# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
#     "scipy",
#     "pandas",
# ]
# ///

# %% Import
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from assignment.assignment import estimate_platform_distribution
from simulator import run_multiple_simulations, estimate_naive_platform_distribution
import numpy as np

np.random.seed(42)
estimation_result_tables, error_table = run_multiple_simulations(
    estimate_naive_platform_distribution, estimate_platform_distribution, n_simulations=10
)



# %% Test ------------
print("=" * 50)
print("Testing Task 2: degree_based_vaccination_strategy")
print("=" * 50)

# ------------------------------------------------------------
# Test 1: Star graph - should select center node first
# ------------------------------------------------------------
error_naive = error_table.query("estimator == 'naive'").sort_values("sample_id")["MSE"].values
error_corrected = error_table.query("estimator == 'corrected'").sort_values("sample_id")["MSE"].values

success_rate = np.mean(error_naive > error_corrected)

if success_rate > 0.7:
    print(f"✓ Test PASSED: Corrected estimator outperformed naive estimator in {success_rate*100:.1f}% of simulations.")
    print("Great job! Your degree-corrected estimator is more accurate than the naive estimator in the majority of simulation runs.")
    print("This means your implementation is successfully reducing the bias introduced by the network sampling process.")
    print("For full credit, try to achieve >70% success rate. If you are below this, consider revisiting your weighting logic.")
    print()
    mean_naive = np.mean(error_naive)
    mean_corrected = np.mean(error_corrected)
    improvement_factor = mean_naive / mean_corrected if mean_corrected > 0 else float('inf')
    print(f"Mean MSE (Naive):     {mean_naive:.4e}")
    print(f"Mean MSE (Corrected): {mean_corrected:.4e}")
    print(f"Improvement factor (Naive/Corrected): {improvement_factor:.2f}x")
    print()
    print("Sample of MSEs for first 5 simulations:")
    print("Sim\tNaive MSE\tCorrected MSE\tImprovement factor")
    for i in range(min(5, len(error_naive))):
        factor = error_naive[i] / error_corrected[i] if error_corrected[i] > 0 else float('inf')
        print(f"{i}\t{error_naive[i]:.4e}\t{error_corrected[i]:.4e}\t{factor:.2f}x")
else:
    print(f"✗ Test FAILED: Corrected estimator only outperformed naive estimator in {success_rate*100:.1f}% of simulations. Aim for >80%.")
    print("Your corrected estimator did not consistently outperform the naive estimator.")
    print("This suggests your degree-based correction may not be implemented correctly, or is not sufficiently reducing the bias.")
    print("Check that you are weighting each participant's response by the inverse of their degree, and that your normalization is correct.")
    print("Review the simulation setup and your estimator logic, then try again.")
    print()
    mean_naive = np.mean(error_naive)
    mean_corrected = np.mean(error_corrected)
    improvement_factor = mean_naive / mean_corrected if mean_corrected > 0 else float('inf')
    print(f"Mean MSE (Naive):     {mean_naive:.4e}")
    print(f"Mean MSE (Corrected): {mean_corrected:.4e}")
    print(f"Improvement factor (Naive/Corrected): {improvement_factor:.2f}x")
    print()
    print("Sample of MSEs for first 5 simulations:")
    print("Sim\tNaive MSE\tCorrected MSE\tImprovement factor")
    for i in range(min(5, len(error_naive))):
        factor = error_naive[i] / error_corrected[i] if error_corrected[i] > 0 else float('inf')
        print(f"{i}\t{error_naive[i]:.4e}\t{error_corrected[i]:.4e}\t{factor:.2f}x")

    raise AssertionError("Test failed")