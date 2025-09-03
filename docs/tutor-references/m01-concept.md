# Module 01: Euler Tour - Core Concepts

## The Königsberg Bridge Problem

The module begins with Euler's famous solution to the Königsberg bridge problem from the 18th century. The citizens wanted to know if they could walk through the city crossing each of the seven bridges exactly once and return to the starting point.

### Euler's Key Insights

**Abstraction:** Euler transformed the physical problem into a mathematical one by:
- Converting each landmass into a **node**
- Converting each bridge into an **edge** connecting nodes

**The Degree Concept:** The degree of a node is the number of edges connected to it. This is fundamental to understanding Euler paths:
- Nodes with **even degree**: Can be passed through (equal "in" and "out" bridges)
- Nodes with **odd degree**: Must be start or end points (unmatched bridges)

### Euler's Conditions for Eulerian Paths

An **Eulerian Path** (crossing every edge exactly once) exists if and only if:
1. The graph is **connected**
2. Either:
   - **Zero nodes have odd degree** (Eulerian Circuit - closed loop)
   - **Exactly two nodes have odd degree** (path starts at one odd node, ends at the other)

In Königsberg, all four landmasses had odd degree, making the walk impossible.

## Network Terminology

### Walks, Trails, and Paths

| Term | Definition | Restriction |
|------|------------|-------------|
| **Walk** | Sequence of connected nodes | Can repeat both nodes and edges |
| **Trail** | Walk without repeating edges | Cannot repeat edges, can repeat nodes |
| **Path** | Walk without repeating nodes | Cannot repeat nodes (or edges) |

### Cycles and Circuits

| Term | Definition |
|------|------------|
| **Circuit** | Closed trail (starts and ends at same node) |
| **Cycle** | Closed path (starts and ends at same node) |

### Connectivity

- **Connected graph**: Path exists between any two nodes
- **Disconnected graph**: Contains separate "islands" called **connected components**

For **directed graphs**:
- **Weakly connected**: Connected if edge directions ignored
- **Strongly connected**: Directed path exists from every node to every other node

## Key Mathematical Concepts

### Node Degree
The degree of a node is the number of edges connected to it. This simple concept was central to Euler's breakthrough - he realized that valid bridge walks require specific degree patterns.

### Connectivity Requirements
Euler's theorem requires the graph to be connected. Even with correct degree conditions, disconnected components prevent a single continuous path.

The historical significance extends beyond the puzzle - Euler's abstraction created **graph theory**, now essential for understanding social networks, transportation systems, brain connectivity, and internet topology.

### Giant Component

A giant component is a connected component that contains a significant fraction of the entire graph's nodes.
