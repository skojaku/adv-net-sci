# Advanced Network Science: Node Degree Assignment

## Assignment Overview

This repository contains the **Node Degree and Friendship Paradox** assignment for the Advanced Network Science course. Students will implement fundamental algorithms for analyzing degree distributions and exploring the counterintuitive friendship paradox in networks.

## What Students Will Learn

- **Degree Distribution Analysis**: Compute and interpret probability distributions of node degrees
- **Friendship Paradox**: Understand and implement the mathematical basis for why friends have more friends
- **Heavy-Tailed Visualization**: Master techniques for visualizing power-law and heavy-tailed distributions  
- **Sampling Bias**: Explore how network structure affects sampling and observation

## Assignment Structure

### Core Implementation Tasks
1. **Degree Distribution Calculation** - Compute probability mass functions from network data
2. **Friendship Paradox Statistics** - Calculate and compare node vs. friend average degrees
3. **CCDF Computation** - Implement complementary cumulative distribution functions for visualization
4. **Degree-Biased Sampling** - Perform sampling proportional to node connectivity

### Interactive Components
- Real-time testing dashboard with multiple network types
- Comparative visualizations across network models
- Statistical validation of implemented functions

## Repository Structure

```
advnetsci-node-degree/
├── assignment/
│   ├── assignment.py          # Main marimo notebook with tasks
│   └── README.md             # Detailed assignment instructions
├── tests/
│   ├── test_01.py            # Degree distribution tests
│   ├── test_02.py            # Friendship paradox tests  
│   ├── test_03.py            # CCDF calculation tests
│   └── test_04.py            # Sampling bias tests
├── data/                     # (Reserved for future data files)
├── derived/                  # (For generated outputs)
└── README.md                # This overview file
```

## Getting Started

### Prerequisites
- Python 3.11+
- Required packages: `marimo`, `numpy`, `igraph`, `matplotlib`, `seaborn`, `scipy`

### Running the Assignment
1. Clone this repository
2. Navigate to the `assignment/` directory  
3. Run `marimo edit assignment.py`
4. Implement the required functions
5. Test using the interactive dashboard
6. Validate with provided test suites

### Testing Your Work
Run individual test files to verify implementations:
```bash
python tests/test_01.py  # Degree distribution tests
python tests/test_02.py  # Friendship paradox tests
python tests/test_03.py  # CCDF tests  
python tests/test_04.py  # Sampling tests
```

## Key Concepts Covered

### Degree Distributions
- Probability mass functions for discrete degree sequences
- Handling isolated nodes and edge cases
- Mathematical properties and normalization

### Friendship Paradox
- Edge-based vs. node-based sampling
- Degree bias in network observations
- Applications to epidemiology and social networks

### Heavy-Tailed Distributions
- CCDF vs. PDF for visualization
- Log-log scaling techniques
- Power-law identification methods

### Network Sampling
- Degree-proportional sampling mechanisms
- Statistical bias in network studies
- Implications for real-world network analysis

## Network Models Used

The assignment tests implementations across diverse network types:
- **Barabási-Albert (Scale-free)**: Power-law degree distributions, strong friendship paradox
- **Erdős-Rényi (Random)**: Poisson degree distributions, moderate friendship paradox
- **Watts-Strogatz (Small-world)**: Intermediate degree heterogeneity
- **Regular Lattices**: Minimal degree variance, weak friendship paradox

## Grading and Assessment

### Automated Testing (70%)
- Correctness on canonical examples (star graphs, complete graphs)
- Mathematical property verification (normalization, monotonicity)
- Statistical behavior on random networks
- Edge case handling

### Code Quality (20%)  
- Clean, readable implementations
- Proper use of numpy and igraph APIs
- Efficient algorithms and data structures

### Conceptual Understanding (10%)
- Appropriate handling of boundary conditions
- Correct interpretation of mathematical relationships
- Robust implementation choices

## Academic Integrity

This assignment uses automated similarity detection across all submissions and online repositories. Students must:
- Write original implementations
- Acknowledge any external resources or AI assistance
- Discuss concepts but not share code solutions
- Maintain individual accountability for all submitted work

## Support Resources

### Course Materials
- Lecture notes on degree distributions and friendship paradox
- Interactive visualization games for concept exploration
- Supplementary readings on network sampling methods

### Technical References  
- igraph documentation for Python
- NumPy array manipulation guides
- Network science literature on degree heterogeneity

## Educational Philosophy

This assignment emphasizes **learning through implementation** rather than passive consumption. By coding these fundamental algorithms, students develop:
- Deep understanding of mathematical concepts
- Practical skills in network analysis
- Intuition about sampling bias and statistical artifacts
- Experience with real-world data analysis challenges

The interactive dashboard provides immediate feedback, allowing students to explore parameter spaces and develop intuition about how network structure affects statistical measures.

---

*This assignment is part of the Advanced Network Science course curriculum, designed to build foundational skills in computational network analysis.*