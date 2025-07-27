# Random Walks: Exercises and Practice

This section contains all the exercises from the Random Walks module, organized by topic and difficulty level.

## Coding Exercises

### Exercise 01: Basic Random Walk Simulation

Write the following function to simulate the random walk for a given number of steps and return the position for each step.

```python
def random_walk(A, n_steps):
    """
    Simulate the random walk on a graph with adjacency matrix A.

    Args:
        A (np.ndarray): The adjacency matrix of the graph.
        n_steps (int): The number of steps to simulate.

    Returns:
        np.ndarray: The position of the walker after each step.
    """
    # Your code here
    pass
```

**Hints:**
- Initialize the walker at a random starting position
- Use the transition probability matrix P = A / k (where k is the degree vector)
- For each step, randomly choose the next node based on transition probabilities
- Store the position at each step

### Exercise 02: Expected Position Calculation

Write a function to compute the expected position of the walker at time $t$ using the formula $\mathbb{E}[x(t)] = x(0) P^t$:

```python
def expected_position(A, x_0, t):
    """
    Compute the expected position of the walker at time t.

    Args:
        A (np.ndarray): The adjacency matrix of the graph.
        x_0 (np.ndarray): The initial position of the walker.
        t (int): The number of steps to simulate.

    Returns:
        np.ndarray: The expected position distribution at time t.
    """
    # Your code here
    pass
```

**Hints:**
- Compute the transition matrix P from adjacency matrix A
- Use matrix power P^t to get multi-step transition probabilities
- Apply the initial distribution x_0 to get the expected position

### Exercise 03: Convergence Analysis

Plot each element of $x(t)$ as a function of $t$ for $t=0,1,2,\ldots, 1000$. Try different initial positions and compare the results!

**Steps:**
1. Define the initial position of the walker
2. Compute the expected position of the walker at time $t$ using the function from Exercise 02
3. Draw a line for each element of $x(t)$, totaling 5 lines for a 5-node network
4. Create multiple such plots for different initial positions and compare them

**Questions to explore:**
- Do all initial positions converge to the same stationary distribution?
- How long does it take to converge?
- What does the stationary distribution tell us about the network structure?

### Exercise 04: Community Detection through Random Walks

1. **Stochastic Block Model Analysis:**
   - Generate a network of 100 nodes with 4 communities using a stochastic block model
   - Set inter-community edge probability to $0.05$ and intra-community edge probability to $0.2$
   - Compute the expected position of the walker starting from node zero after $x$ steps
   - Plot the results for $x = 0, 5, 10, 1000$

2. **Parameter Sensitivity:**
   - Increase the inter-community edge probability to $0.15$ and repeat the simulation
   - Compare the results with the previous simulation
   - What happens to community detection when communities become more connected?

**Implementation hints:**
```python
import numpy as np
from sklearn.datasets import make_blobs
import networkx as nx

# Example stochastic block model generation
def generate_sbm(n_nodes_per_community, p_within, p_between):
    """Generate a stochastic block model network"""
    # Your implementation here
    pass
```

## Theoretical Exercises

### Exercise 05: HITS Centrality Analysis

If the original network is *undirected*, is the HITS centrality equivalent to the eigenvector centrality? If so or not, explain why.

**Solution Framework:**
- Consider the HITS equations for undirected networks
- Compare with eigenvector centrality equation
- Use the symmetry property of undirected networks
- Show the mathematical relationship between the two measures

### Exercise 06: Degree-Normalized HITS

Consider the case where the graph is undirected and we normalize the hub centrality by the degree $d_j$ of the authority:

$$
x_i = \sum_j \frac{A_{ji}}{d_j} y_j,\quad y_i = \sum_j A_{ij} x_j
$$

Show that the hub centrality becomes equivalent to the degree centrality by substituting $x_i = d_i$.

**Steps to verify:**
1. Substitute $x_i = d_i$ into the first equation
2. Show that this satisfies the system of equations
3. Interpret the result in terms of network centrality

## Mathematical Derivation Exercises

### Exercise 07: Katz Centrality Solution

Derive the solution of the Katz centrality equation:

$$
c_i = \beta + \lambda \sum_{j} A_{ij} c_j
$$

**Solution steps:**
- Write the equation in matrix form
- Rearrange to isolate the centrality vector
- Find the matrix inverse solution
- Verify the solution satisfies the original equation

### Exercise 08: Random Walk Interpretation of PageRank

Show that PageRank can be written as the stationary distribution of a modified random walk with teleportation.

**Starting equation:**
$$
c_i = (1-\beta) \sum_j A_{ji}\frac{c_j}{d^{\text{out}}_j} + \beta \cdot \frac{1}{N}
$$

**Tasks:**
1. Identify the transition probabilities in this equation
2. Show that this represents a Markov chain
3. Prove that the solution is a stationary distribution
4. Interpret the teleportation parameter $\beta$

## Pen and Paper Exercises

### Exercise 09: Manual Calculations

- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)

These exercises include:
- Hand calculation of transition matrices for small networks
- Manual computation of stationary distributions
- Step-by-step random walk simulations
- Eigenvalue calculations for simple graphs

## Interactive Exercises

### Exercise 10: Ladder Lottery Analysis

Using the [Ladder Lottery Game! 🎮✨](vis/amida-kuji.html), explore:

1. **Strategy Development:**
   - Is there a strategy to maximize the probability of winning?
   - How does the starting position affect winning probability?

2. **Parameter Effects:**
   - How does the probability of winning change as the number of horizontal lines increases?
   - What happens with different numbers of vertical lines?

3. **Connection to Random Walks:**
   - How does this game relate to random walks on networks?
   - What type of transition matrix would represent this game?

### Exercise 11: Random Walk Simulation

Using the [Random Walk Simulator! 🎮✨](vis/random-walks/index.html), investigate:

1. **Short-term vs. Long-term behavior:**
   - When the random walker makes many steps, where does it tend to visit most frequently?
   - When the walker makes only a few steps, where does it tend to visit?

2. **Network Structure Analysis:**
   - Does the behavior of the walker inform us about centrality of the nodes?
   - Does the behavior of the walker inform us about communities in the network?

3. **Parameter Exploration:**
   - Try different network topologies (star, ring, complete graph)
   - Observe how network structure affects random walk behavior

## Advanced Exercises

### Exercise 12: Mixing Time Analysis

1. **Theoretical Calculation:**
   - For a given network, compute the second-largest eigenvalue
   - Calculate the theoretical mixing time bound
   - Compare with empirical convergence time

2. **Network Comparison:**
   - Compare mixing times across different network types
   - How does community structure affect mixing time?
   - What about scale-free vs. random networks?

### Exercise 13: Modularity and Random Walks

1. **Derivation Verification:**
   - Verify the random walk interpretation of modularity step by step
   - Show that high modularity corresponds to slow mixing between communities

2. **Empirical Validation:**
   - Generate networks with known community structure
   - Compute modularity using both traditional and random walk approaches
   - Compare the results and interpretation

### Exercise 14: Custom Centrality Measures

Design your own centrality measure based on random walks:

1. **Design Phase:**
   - Choose a specific aspect of random walk behavior to capture
   - Define your measure mathematically
   - Justify why it captures important network properties

2. **Implementation:**
   - Implement your measure in Python
   - Test on various network types
   - Compare with existing centrality measures

3. **Validation:**
   - Evaluate on networks where you know the "ground truth"
   - Analyze computational complexity
   - Discuss practical applications

## Challenge Problems

### Exercise 15: Multi-layer Networks

Extend random walks to multi-layer networks:

1. **Model Development:**
   - How would you define transition probabilities between layers?
   - What does the stationary distribution represent?

2. **Implementation:**
   - Code a multi-layer random walk simulator
   - Analyze convergence properties
   - Compare with single-layer results

### Exercise 16: Dynamic Networks

Consider random walks on time-varying networks:

1. **Theoretical Framework:**
   - How do you handle changing adjacency matrices?
   - What is the appropriate notion of stationary distribution?

2. **Simulation Study:**
   - Implement random walks on temporal networks
   - Study how network dynamics affect walker behavior
   - Develop time-dependent centrality measures

## Assessment Guidelines

### For Instructors

**Beginner Level (Exercises 1-6):**
- Focus on understanding basic concepts
- Emphasize coding implementation
- Check mathematical derivations step-by-step

**Intermediate Level (Exercises 7-11):**
- Require deeper mathematical understanding
- Expect connections between theory and practice
- Look for creative interpretations

**Advanced Level (Exercises 12-16):**
- Demand original thinking and research
- Expect novel implementations
- Require critical analysis and comparison

### Grading Rubric

**Code Quality (40%):**
- Correctness of implementation
- Efficiency and elegance
- Documentation and comments

**Mathematical Understanding (30%):**
- Correct derivations
- Clear explanations
- Proper use of notation

**Analysis and Interpretation (30%):**
- Insightful discussion of results
- Connections to network science concepts
- Critical thinking about limitations and extensions

## Additional Resources

- **Datasets:** Use networks from SNAP, NetworkX, or create synthetic ones
- **Visualization:** Consider using NetworkX, igraph, or D3.js for interactive plots
- **Further Reading:** Consult papers on spectral graph theory and Markov chain analysis
- **Software:** Explore specialized tools like graph-tool or GTNA for large-scale analysis