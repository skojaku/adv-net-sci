---
title: Preparation - Python and Graph Basics
filters:
  - marimo-team/marimo
  - tikz
tikz:
  cache: false
  save-tex: true  # Enable saving intermediate .tex files
  tex-dir: tikz-tex  # Optional: Specify directory to save .tex files
---

## Why Do We Need to Code Graphs?

In 2009, the H1N1 influenza pandemic spread around the world in a pattern that surprised scientists. Geographic distance couldn't explain why some distant cities were infected early while nearby ones remained safe for weeks. The breakthrough came when researchers realized that **disease spread follows network connections - air travel routes - not physical distance**. 

But analyzing a global air travel network with thousands of airports and millions of flight connections by hand? Impossible.

**This is exactly why we need to code graphs**: to let computers solve problems that would be impossible to tackle manually.

When we represent networks in code, we can:
- **Analyze massive real-world networks** - like global air travel (25,000+ airports) or social media (billions of connections)
- **Find hidden patterns automatically** - discover why diseases spread the way they do
- **Test algorithms systematically** - try different approaches and compare results
- **Apply the same logic everywhere** - from pandemic tracking to circuit design, DNA sequencing, or route planning

The same computational tools that helped scientists understand pandemic spread can help us solve the classic Königsberg bridge puzzle - and thousands of similar problems in engineering, biology, and computer science.

```{.tikz}
%%| caption: Network Connections vs Geographic Distance - Why computational tools matter

\begin{tikzpicture}[scale=1.5]
  % Geographic view (left side)
  \node[rectangle, draw, fill=red!10, text width=4cm, align=center] at (-3, 3) {
    \textbf{Geographic Thinking}\\
    Disease spreads to nearby places first
  };
  
  % Cities with geographic layout
  \node[circle, draw, fill=blue!20] (mexico) at (-4, 1) {Mexico};
  \node[circle, draw, fill=blue!20] (usa) at (-3, 2) {USA};
  \node[circle, draw, fill=blue!20] (guatemala) at (-4.5, 0.5) {Guatemala};
  \node[circle, draw, fill=blue!20] (japan) at (-1, 1.5) {Japan};
  
  % Geographic distance arrows
  \draw[dashed, gray] (mexico) -- (usa);
  \draw[dashed, gray] (mexico) -- (guatemala);
  \draw[dashed, gray] (mexico) -- (japan);
  
  \node[red] at (-3, 0) {❌ Poor prediction};
  
  % Network view (right side)
  \node[rectangle, draw, fill=green!10, text width=4cm, align=center] at (3, 3) {
    \textbf{Network Thinking}\\
    Disease follows flight connections
  };
  
  % Same cities with network layout
  \node[circle, draw, fill=green!20] (mexico2) at (2, 1) {Mexico};
  \node[circle, draw, fill=green!20] (usa2) at (3, 2) {USA};
  \node[circle, draw, fill=green!20] (guatemala2) at (1.5, 0.5) {Guatemala};
  \node[circle, draw, fill=green!20] (japan2) at (4, 1.5) {Japan};
  
  % Flight connections (thicker = more flights)
  \draw[thick, blue] (mexico2) -- (usa2);
  \draw[very thick, blue] (mexico2) -- (japan2);
  \draw[thin, blue] (mexico2) -- (guatemala2);
  
  \node[green!70!black] at (3, 0) {✓ Accurate prediction};
  
  % Arrow between views
  \draw[->, ultra thick, purple] (0, 2) -- (0, 1.5);
  \node[purple, align=center] at (0, 0.8) {Computational\\analysis\\needed!};
\end{tikzpicture}
```

## Starting Simple: Graphs with Basic Python

Before using specialized libraries, let's see how to represent a simple graph using only basic Python data structures. This will help you understand what the libraries are actually doing behind the scenes.

```{.tikz}
%%| caption: A Simple Friendship Network - Three people all connected to each other

\begin{tikzpicture}[scale=1.5]
  % Define nodes
  \node[circle, draw, fill=lightblue, minimum size=1cm] (alice) at (0,2) {Alice};
  \node[circle, draw, fill=lightgreen, minimum size=1cm] (bob) at (-1.5,0) {Bob};
  \node[circle, draw, fill=lightcoral, minimum size=1cm] (charlie) at (1.5,0) {Charlie};
  
  % Draw edges (friendships)
  \draw[thick, blue] (alice) -- (bob);
  \draw[thick, blue] (bob) -- (charlie);
  \draw[thick, blue] (charlie) -- (alice);
  
  % Add labels for the connections
  \node[above left, small] at (-0.75,1) {friends};
  \node[below, small] at (0,0) {friends};
  \node[above right, small] at (0.75,1) {friends};
\end{tikzpicture}
```

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

```{.tikz}
%%| caption: Understanding Degrees - Each person's number of friendships determines if an Euler tour is possible

\begin{tikzpicture}[scale=1.8]
  % Define nodes with degree labels
  \node[circle, draw, fill=lightblue, minimum size=1.2cm] (alice) at (0,2) {\begin{tabular}{c}Alice\\degree: 2\end{tabular}};
  \node[circle, draw, fill=lightgreen, minimum size=1.2cm] (bob) at (-1.5,0) {\begin{tabular}{c}Bob\\degree: 2\end{tabular}};
  \node[circle, draw, fill=lightcoral, minimum size=1.2cm] (charlie) at (1.5,0) {\begin{tabular}{c}Charlie\\degree: 2\end{tabular}};
  
  % Draw edges with numbers
  \draw[thick, blue] (alice) -- (bob) node[midway, above left] {1};
  \draw[thick, blue] (bob) -- (charlie) node[midway, below] {2};
  \draw[thick, blue] (charlie) -- (alice) node[midway, above right] {3};
  
  % Add Euler rule explanation
  \node[rectangle, draw, fill=yellow!20, text width=4cm, align=center] at (0,-2) {
    All degrees are even (2)\\
    $\Rightarrow$ Euler cycle exists!\\
    Can start anywhere and return
  };
\end{tikzpicture}
```

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

```{.tikz}
%%| caption: Manual vs Library Approach - Same result, much less work!

\begin{tikzpicture}[scale=1.2]
  % Manual approach box
  \node[rectangle, draw, fill=red!10, text width=5.5cm, align=left] at (-3,2) {
    \textbf{Manual Approach:}\\
    \texttt{degrees = \{\}}\\
    \texttt{for person in friends:}\\
    \texttt{\ \ degrees[person] = len(friends[person])}\\
    \texttt{odd\_degrees = [person for person, degree}\\
    \texttt{\ \ \ \ \ \ \ \ \ \ \ \ \ in degrees.items()}\\
    \texttt{\ \ \ \ \ \ \ \ \ \ \ \ \ if degree \% 2 == 1]}\\
    \\
    \textcolor{red}{Many lines of code!}
  };
  
  % Library approach box
  \node[rectangle, draw, fill=green!10, text width=5cm, align=left] at (3,2) {
    \textbf{Library Approach:}\\
    \texttt{g = ig.Graph([(0,1), (1,2), (2,0)])}\\
    \texttt{degrees = g.degree()}\\
    \texttt{odd\_count = sum(1 for d in degrees}\\
    \texttt{\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ if d \% 2 == 1)}\\
    \\
    \\
    \textcolor{green!70!black}{Clean and simple!}
  };
  
  % Arrow pointing from manual to library
  \draw[->, thick, blue] (-0.5,2) -- (0.5,2);
  \node[above] at (0,2.2) {\textcolor{blue}{Libraries handle the details}};
  
  % Result box
  \node[rectangle, draw, fill=blue!10, text width=6cm, align=center] at (0,-1) {
    \textbf{Both approaches give the same result:}\\
    Degrees: [2, 2, 2]\\
    Odd vertices: 0\\
    Has Euler cycle: True
  };
\end{tikzpicture}
```

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