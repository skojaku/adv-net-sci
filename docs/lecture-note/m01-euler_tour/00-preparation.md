---
title: Preparation - Python and Graph Basics
---

## Why Do We Need to Code Graphs?

Imagine you're trying to solve the Königsberg bridge puzzle by hand. You might draw the map, trace different paths with your finger, and keep track of which bridges you've crossed. This works fine for 7 bridges, but what if there were 700 bridges? Or 7,000?

**This is exactly why we need to code graphs**: to let computers solve problems that would be impossible to tackle manually.

When we represent graphs in code, we can:
- **Analyze any size network** - from small puzzles to massive social networks
- **Test algorithms systematically** - try different approaches and compare results
- **Find patterns automatically** - detect Euler paths without manual checking
- **Scale to real problems** - apply the same logic to circuit design, DNA sequencing, or route planning

## Starting Simple: Graphs with Basic Python

```{.tikz}
%%| filename: stick-figure
%%| caption: A Stick Figure

\begin{tikzpicture}
  % Head
  \draw (0,0) circle (1cm);
  % Body
  \draw (0,-1) -- (0,-3);
  % Arms
  \draw (-1,-2) -- (0,-1) -- (1,-2);
  % Legs
  \draw (-1,-4) -- (0,-3) -- (1,-4);
\end{tikzpicture}
```

Before using specialized libraries, let's see how to represent a simple graph using only basic Python data structures. This will help you understand what the libraries are actually doing behind the scenes.

### A Tiny Example: Three Friends

```python
# Let's represent a simple friendship network
# Alice (0) is friends with Bob (1)
# Bob (1) is friends with Charlie (2)
# Charlie (2) is friends with Alice (0)

# Method 1: List of connections
friendships = [(0, 1), (1, 2), (2, 0)]

# Method 2: Dictionary showing who each person knows
friends = {
    0: [1, 2],  # Alice knows Bob and Charlie
    1: [0, 2],  # Bob knows Alice and Charlie
    2: [0, 1]   # Charlie knows Alice and Bob
}

# Now we can ask questions:
print("Who are Alice's friends?", friends[0])
print("How many friends does Bob have?", len(friends[1]))
```

This simple approach works! But as graphs get larger and algorithms get more complex, we need better tools.

### Why Our Simple Approach Has Limits

Let's try to check if our friendship network has an Euler path (visiting every friendship exactly once):

```python
# Using our simple dictionary approach
friends = {0: [1, 2], 1: [0, 2], 2: [0, 1]}

# Count how many friends each person has (their "degree")
degrees = {}
for person in friends:
    degrees[person] = len(friends[person])

print("Degrees:", degrees)  # Should be {0: 2, 1: 2, 2: 2}

# Check Euler's rule: all degrees even = Euler cycle exists
odd_degrees = [person for person, degree in degrees.items() if degree % 2 == 1]
print(f"People with odd number of friends: {len(odd_degrees)}")
print("Has Euler cycle:", len(odd_degrees) == 0)
```

This works for 3 people, but imagine doing this for 1000 people with thousands of friendships. We'd need to write a lot of repetitive code!

## Libraries: Convenient Tools for Graph Work

Now let's see how specialized libraries make this much easier:

```python
# These libraries do the heavy lifting for us
import igraph as ig
import numpy as np  # For numerical calculations
```

### What These Libraries Give Us

**igraph** is like having a graph expert assistant:
- Handles all the tedious bookkeeping (adding/removing connections)
- Provides pre-built algorithms (finding Euler paths, shortest routes, etc.)
- Works efficiently even with millions of connections
- Written in C (fast!) with Python interface (easy to use!)

**NumPy** helps with mathematical calculations:
- Fast operations on lists of numbers (like degrees of all vertices)
- Matrix operations (if you want to represent graphs as grids of numbers)

### Same Problem, Much Easier

Let's solve the same friendship problem using igraph:

```python
import igraph as ig

# Create the same friendship network
g = ig.Graph([(0, 1), (1, 2), (2, 0)])

# Check degrees (one line instead of a loop!)
degrees = g.degree()
print("Degrees:", degrees)

# Check for Euler cycle (built-in logic!)
odd_count = sum(1 for d in degrees if d % 2 == 1)
print("Has Euler cycle:", odd_count == 0)

# Bonus: igraph can even visualize the network!
# ig.plot(g)  # Uncomment to see a picture of your graph
```

**The key insight**: Libraries don't change what we're doing - they just make it much easier and faster!

## Essential igraph Operations

Here are the basic operations you'll need for Euler tour problems:

### Creating Graphs

```python
# Most common way: list who's connected to whom
g = ig.Graph([(0, 1), (1, 2), (2, 0)])  # Triangle

# Alternative: build step by step
g = ig.Graph()
g.add_vertices(3)        # Add 3 vertices: 0, 1, 2
g.add_edges([(0, 1), (1, 2), (2, 0)])  # Connect them
```

### Asking Questions About Your Graph

```python
# How big is my graph?
print(f"Vertices: {g.vcount()}")
print(f"Edges: {g.ecount()}")

# The most important question for Euler tours:
# How many connections does each vertex have?
degrees = g.degree()
print(f"Degrees: {degrees}")

# Count vertices with odd number of connections
odd_count = sum(1 for d in degrees if d % 2 == 1)
print(f"Vertices with odd degree: {odd_count}")
```

### Basic Tools You'll Use

```python
# Get neighbors of a vertex
neighbors = g.neighbors(0)  # Who is vertex 0 connected to?

# Make a copy to experiment with
g_copy = g.copy()

# Simple data structures for building algorithms
path = []           # To store the path we're building
visited = set()     # To remember where we've been
```

## Quick Test: Does This Graph Have an Euler Tour?

```python
# Create a triangle graph
g = ig.Graph([(0, 1), (1, 2), (2, 0)])

# Check each vertex's degree
degrees = g.degree()
print(f"Degrees: {degrees}")

# Apply Euler's rule
odd_count = sum(1 for d in degrees if d % 2 == 1)
print(f"Vertices with odd degree: {odd_count}")

if odd_count == 0:
    print("✓ Has Euler cycle (can start anywhere and return)")
elif odd_count == 2:
    print("✓ Has Euler path (must start at one odd vertex, end at the other)")
else:
    print("✗ No Euler tour possible")
```

::: {.column-margin}
**Euler's simple rule**: If all vertices have an even number of connections, you can tour all edges and return home. If exactly 2 vertices have odd connections, you can tour all edges but must start at one odd vertex and end at the other.
:::

## What's Next?

You're now equipped with the essential tools for Euler tour algorithms. In the next sections, you'll:

1. **Learn** the historical Königsberg bridge problem that started it all
2. **Understand** the mathematical theory behind Eulerian paths
3. **Implement** algorithms to find Euler tours in any graph
4. **Apply** these concepts to real-world problems

The beauty of Euler's insight was seeing that complex geometric problems could be solved with simple rules about connections. Let's discover how this 18th-century breakthrough still powers modern algorithms today.