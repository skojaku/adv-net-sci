# Node Degree and the Friendship Paradox Assignment

## Overview

This assignment focuses on understanding and implementing fundamental concepts related to node degrees in networks and the fascinating friendship paradox phenomenon. You'll implement functions to compute degree distributions, calculate friendship paradox statistics, and visualize heavy-tailed distributions.

## Learning Objectives

By completing this assignment, you will:

1. **Understand degree distributions**: Learn how to compute and interpret the distribution of node degrees in networks
2. **Implement the friendship paradox**: Understand why "your friends have more friends than you do" through computational implementation
3. **Master visualization techniques**: Learn proper methods for visualizing heavy-tailed distributions using CCDF plots
4. **Apply degree-biased sampling**: Implement sampling mechanisms that demonstrate how network structure affects observation

## Assignment Tasks

### Task 1: Degree Distribution (25 points)
Implement `compute_degree_distribution(g)` to calculate the probability mass function of node degrees.

**Key concepts:**
- Degree sequence extraction
- Probability normalization
- Handling networks with isolated nodes

### Task 2: Friendship Paradox Statistics (25 points)
Implement `compute_friendship_paradox_stats(g)` to compute average degrees for nodes vs. friends.

**Key concepts:**
- Edge-based sampling creates degree bias
- Mathematical proof of the friendship paradox
- Practical implications for network analysis

### Task 3: CCDF Calculation (25 points)
Implement `compute_degree_ccdf(degree_dist)` to calculate the complementary cumulative distribution function.

**Key concepts:**
- CCDF vs. PDF for heavy-tailed distributions
- Monotonicity properties
- Log-log visualization benefits

### Task 4: Degree-Biased Sampling (25 points)
Implement `sample_degree_biased_nodes(g, num_samples)` to perform sampling proportional to node degree.

**Key concepts:**
- Edge-based sampling mechanism
- Relationship to friendship paradox
- Statistical bias in network sampling

## Interactive Visualization

The assignment includes an interactive dashboard that lets you:
- Test your implementations on different network types
- Compare degree distributions across network models
- Visualize the friendship paradox effect
- Explore sampling bias through degree-heterogeneous networks

## Files Structure

```
assignment/
├── assignment.py          # Main marimo notebook with tasks and visualization
└── README.md             # This file

tests/
├── test_01.py            # Tests for degree distribution
├── test_02.py            # Tests for friendship paradox stats
├── test_03.py            # Tests for CCDF calculation
└── test_04.py            # Tests for degree-biased sampling
```

## Running the Assignment

1. **Open the notebook**: Run `marimo edit assignment.py` in the assignment directory
2. **Implement functions**: Complete the four `@app.function` implementations
3. **Test interactively**: Use the dashboard to test your implementations
4. **Verify with tests**: Run the test files to ensure correctness

## Testing Your Implementation

Each task has comprehensive tests that check:
- Correctness on known examples (star graphs, complete graphs)
- Mathematical properties (probability sums, monotonicity)
- Boundary conditions and edge cases
- Statistical properties and correlations

Run tests individually:
```bash
python tests/test_01.py  # Task 1 tests
python tests/test_02.py  # Task 2 tests
python tests/test_03.py  # Task 3 tests
python tests/test_04.py  # Task 4 tests
```

## Common Pitfalls

1. **Array indexing**: Remember that degree k corresponds to index k in arrays
2. **Probability normalization**: Ensure distributions sum to 1.0
3. **CCDF calculation**: Exclude the last CDF element to avoid log(0) in visualizations
4. **Edge sampling**: Sample edges uniformly, then take endpoints for degree bias

## Network Types in Dashboard

The interactive dashboard tests your implementations on:
- **Scale-free networks**: Show strong friendship paradox and power-law distributions
- **Random networks**: Demonstrate Poisson-like degree distributions
- **Small-world networks**: Combine high clustering with short paths
- **Regular networks**: Show minimal degree heterogeneity

## Grading Criteria

- **Correctness (70%)**: Functions produce correct outputs on test cases
- **Implementation quality (20%)**: Clean, efficient code following best practices
- **Understanding (10%)**: Proper handling of edge cases and boundary conditions

## Academic Integrity

- Write your own implementations
- You may discuss concepts but not share code
- Cite any external resources used
- AI assistance must be acknowledged in comments

## Resources

- Course lecture notes on node degree and friendship paradox
- Interactive games for exploring concepts
- Network science literature on degree distributions and sampling bias