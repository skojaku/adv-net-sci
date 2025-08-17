# Test Suite for Node Degree Assignment

This directory contains comprehensive tests for all four assignment tasks. Each test file validates different aspects of the implementations to ensure correctness and robustness.

## Test Files Overview

### `test_01.py` - Degree Distribution Tests
Tests for `compute_degree_distribution(g)` function:

- **Simple graphs**: Star graphs, complete graphs with known degree sequences
- **Edge cases**: Graphs with isolated nodes, empty graphs
- **Mathematical properties**: Distribution normalization (sums to 1.0)
- **Consistency checks**: Relationship between degrees and distribution values

### `test_02.py` - Friendship Paradox Statistics Tests  
Tests for `compute_friendship_paradox_stats(g)` function:

- **Classic examples**: Star graphs showing strong friendship paradox
- **Uniform cases**: Complete graphs with no paradox effect
- **Inequality verification**: Friends have higher average degree
- **Edge consistency**: Node averages match graph edge counts

### `test_03.py` - CCDF Calculation Tests
Tests for `compute_degree_ccdf(degree_dist)` function:

- **Known distributions**: Hand-calculated examples with verified CCDF values
- **Mathematical properties**: Monotonicity, boundary conditions
- **Relationship verification**: CCDF = 1 - CDF consistency
- **Range validation**: Values between 0 and 1, proper endpoints

### `test_04.py` - Degree-Biased Sampling Tests
Tests for `sample_degree_biased_nodes(g, num_samples)` function:

- **Bias verification**: High-degree nodes sampled more frequently
- **Statistical correlation**: Strong correlation between degree and sampling frequency
- **Edge cases**: Isolated nodes never sampled, uniform sampling for regular graphs
- **Sample size accuracy**: Returns exactly the requested number of samples

## Running Tests

### Individual Test Files
```bash
python test_01.py  # Degree distribution tests
python test_02.py  # Friendship paradox tests
python test_03.py  # CCDF tests
python test_04.py  # Sampling tests
```

### All Tests Together
```bash
for test in test_*.py; do python "$test"; done
```

## Test Design Philosophy

### Canonical Examples
Each test starts with simple, well-understood examples (star graphs, complete graphs) where the correct answers can be calculated by hand. This ensures implementations work correctly on basic cases.

### Mathematical Properties
Tests verify that implementations satisfy fundamental mathematical properties:
- Probability distributions sum to 1.0
- CCDFs are monotonically decreasing
- Sampling produces the correct number of outputs
- Statistical relationships hold (friendship paradox inequality)

### Edge Cases
Tests include boundary conditions and edge cases:
- Graphs with isolated nodes
- Empty graphs or distributions
- Single-node graphs
- Very sparse or very dense networks

### Statistical Validation
For probabilistic functions (especially sampling), tests use:
- Large sample sizes for statistical reliability
- Correlation analysis for bias verification
- Multiple random seeds for reproducibility
- Tolerance ranges for statistical fluctuations

## Understanding Test Failures

### Common Issues and Solutions

**"Distribution doesn't sum to 1"**
- Check normalization in `compute_degree_distribution`
- Ensure you're dividing by total number of nodes

**"CCDF not monotonic"**
- Verify CCDF calculation: should be `1 - np.cumsum(distribution)[:-1]`
- Don't include the final cumulative sum value (always 1.0)

**"Friendship paradox violated"**
- Ensure you're sampling through edges, not nodes directly
- Use edge endpoints for degree-biased sampling

**"Wrong number of samples"**
- Return exactly `num_samples` elements
- Handle edge case where graph has no edges

**"Correlation too weak"**
- Implement true degree-proportional sampling
- Higher-degree nodes should appear more frequently

## Test Data Characteristics

### Network Types Used
- **Star graphs**: Extreme degree heterogeneity, clear friendship paradox
- **Complete graphs**: Uniform degrees, no sampling bias
- **Random graphs**: Moderate heterogeneity, statistical properties
- **Scale-free networks**: Power-law distributions, strong bias effects

### Statistical Parameters
- Sample sizes: 1,000 to 20,000 for reliable statistics
- Correlation thresholds: > 0.8 for degree-biased sampling
- Tolerance levels: Account for random fluctuations
- Multiple random seeds: Ensure reproducible results

## Debugging Tips

### Print Intermediate Values
Add debug prints to see what your functions are computing:
```python
print(f"Degrees: {degrees}")
print(f"Distribution: {distribution}")
print(f"Sum: {np.sum(distribution)}")
```

### Visualize Results
Create simple plots to understand your data:
```python
import matplotlib.pyplot as plt
plt.bar(range(len(distribution)), distribution)
plt.show()
```

### Check Against Simple Cases
Test your functions on tiny examples you can verify by hand:
```python
# 3-node path: degrees [1, 2, 1]
g = igraph.Graph([(0,1), (1,2)])
print(compute_degree_distribution(g))  # Should be [0, 2/3, 1/3]
```

## Expected Test Execution Time

- `test_01.py`: < 1 second (deterministic tests)
- `test_02.py`: < 2 seconds (includes some graph generation)  
- `test_03.py`: < 1 second (pure mathematical operations)
- `test_04.py`: 3-5 seconds (statistical sampling tests)

Total test suite runtime: < 10 seconds

## Test Coverage

The test suite provides comprehensive coverage of:
- ✅ Function correctness on canonical examples
- ✅ Mathematical property verification  
- ✅ Edge case and boundary condition handling
- ✅ Statistical behavior validation
- ✅ Error condition testing
- ✅ Performance characteristics

This ensures student implementations are robust, correct, and ready for real-world network analysis tasks.