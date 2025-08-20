# Module 02: Small-World Networks - Core Concepts

## Milgram's Small-World Experiment

The module centers on Stanley Milgram's groundbreaking 1960s experiment that revealed the surprising connectivity of social networks.

### The Experiment
1. Packets sent to random people in Omaha, Nebraska and Wichita, Kansas
2. Recipients asked to forward to target person in Boston if they knew them personally
3. Otherwise, forward to someone who might know the target
4. Continue until packet reaches target

### Results
- 64 out of 160 packets successfully reached target
- Average chain length: ~6 people
- Coined the phrase "six degrees of separation"
- Demonstrated that large networks can have remarkably short paths

### Modern Confirmations
- **Yahoo email study**: Average chain length ~4 steps
- **Facebook study (2012)**: 721 million users, average shortest path = 4.74

## Why Small-World Networks Are Non-Trivial

### Expected vs. Actual Structure
- **Local connections** alone create high clustering but long path lengths
- **Random connections** alone create short paths but low clustering  
- **Small-world networks** combine both: high clustering AND short paths

### The Key Insight
A few **long-range connections** (shortcuts) dramatically reduce path lengths while preserving local clustering. This combination is mathematically non-trivial and empirically common.

## Quantifying Small-World Properties

### 1. Average Path Length
The mean shortest distance between all pairs of nodes in the network.

**Example calculation** for 4-node network:
- All pairwise distances: [1, 1, 2, 1, 1, 1]
- Average path length = 7/6 ≈ 1.16

### 2. Clustering Coefficients

#### Local Clustering
For node i: **Ci = (triangles involving i) / (possible triangles in i's neighborhood)**

Using adjacency matrix A and degree ki:
```
Ci = Σj Σℓ AijAjℓAℓi / [ki(ki-1)]
```

#### Average Local Clustering
```
C̄ = (1/N) Σi Ci
```

#### Global Clustering (Transitivity)
```
C = 3 × (number of triangles) / (number of connected triplets)
```

**Connected triplets**: Sets of 3 nodes with ≥2 edges (open or closed)

### 3. Small-World Index

Simple ratio is insufficient:
```
s_naive = C̄/L̄
```

**Problem**: High values for trivial networks (e.g., complete graphs)

**Solution**: Normalize against equivalent random networks:
```
σ = (C̄/C̄_random) / (L̄/L̄_random)
```

Where for Erdős–Rényi random graphs:
- C̄_random ≈ ⟨k⟩/(n-1)  
- L̄_random ≈ ln(n)/ln(⟨k⟩)

**Interpretation**:
- σ > 1: Strong small-world property
- σ ≈ 1: Random-like network  
- σ < 1: Anti-small-world (large paths, low clustering)

## Watts-Strogatz Model

### Algorithm
1. **Start**: Regular ring lattice (n nodes, each connected to k nearest neighbors)
2. **Rewire**: For each edge, with probability p:
   - Remove edge and reconnect one endpoint randomly
   - Avoid self-loops and duplicate edges

### Parameter Effects
- **p = 0**: Regular lattice (high clustering, long paths)
- **p = 1**: Random graph (low clustering, short paths)  
- **0 < p < 1**: Small-world (high clustering, short paths)

### Mechanism
Small-world property emerges because even a few random rewirings create shortcuts that dramatically reduce path lengths while preserving most local triangular structures.

## Applications Beyond Social Networks

The small-world property appears across domains:
- **Biological**: Neural networks (local circuits + long-range connections)
- **Technological**: Internet topology (regional clusters + transcontinental links)
- **Transportation**: Road networks, airline routes
- **Scientific**: Citation networks, collaboration networks