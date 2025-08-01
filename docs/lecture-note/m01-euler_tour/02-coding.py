# /// script
# [tool.marimo.display]
# default_width = "full"
# [tool.marimo.formatting]
# line_length = 120
# ///

import marimo

__generated_with = "0.14.13"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Coding Networks in Python


    Now that you understand the conceptual foundation from Euler's work, let's explore how to represent and analyze networks computationally. We'll work through both general network representations and apply them specifically to the Königsberg bridge problem.

    ## Network Representations: From Pictures to Data Structures

    Consider this network with 5 nodes and 6 edges:


    ![](https://www.tandfonline.com/cms/asset/2820b951-1747-4621-802c-8d04263f106c/tcon_a_1707286_f0001_oc.jpg)

    How do we represent this graph in a format that a computer can understand and manipulate? Just as Euler needed to abstract Königsberg's bridges, we need data structures that capture the network's essential connectivity while enabling efficient analysis.

    The choice of representation can dramatically affect computational efficiency. For sparse networks (few edges), adjacency lists are memory-efficient. For dense networks or matrix operations, adjacency matrices are preferred.

    Let's explore three fundamental approaches that form the backbone of all network algorithms.

    ### Edge Table: The Direct Approach

    The edge table directly lists connections as pairs—the most intuitive way to store network data.

    Edge tables are also called "edge lists" and are the most common format for storing large-scale network data in files. Social media platforms like Twitter and Facebook store billions of connections this way.
    """
    )
    return


@app.cell
def _():
    # Each row represents one edge (connection between two nodes)
    edges = [
        (0, 1),  # Node 0 connects to Node 1
        (0, 2),  # Node 0 connects to Node 2
        (1, 2),  # Node 1 connects to Node 2
        (1, 3),  # Node 1 connects to Node 3
        (2, 4),  # Node 2 connects to Node 4
        (3, 4)   # Node 3 connects to Node 4
    ]

    print(f"Network has {len(edges)} edges")
    print("Edge list:", edges)
    return (edges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This mirrors how we'd naturally describe the network: "Node 0 connects to nodes 1 and 2, node 1 connects to nodes 0, 2, and 3..." It's the digital equivalent of Euler's original approach—simply listing which bridges connect which landmasses.

    ### Adjacency List: The Neighborhood Map

    The adjacency list stores each node's neighbors in a dictionary—like a social network where each person has a list of friends.

    Most graph algorithms prefer adjacency lists because they allow fast iteration over a node's neighbors. This is crucial for algorithms like breadth-first search or computing clustering coefficients.
    """
    )
    return


@app.cell
def _():
    # Define adjacency list directly as a dictionary
    neighbors = {
        0: [1, 2],     # Node 0 connects to nodes 1 and 2
        1: [0, 2, 3],  # Node 1 connects to nodes 0, 2, and 3
        2: [0, 1, 4],  # Node 2 connects to nodes 0, 1, and 4
        3: [1, 4],     # Node 3 connects to nodes 1 and 4
        4: [2, 3]      # Node 4 connects to nodes 2 and 3
    }

    print("Adjacency list representation:")
    for node, neighbor_list in neighbors.items():
        print(f"Node {node}: {neighbor_list}")
    return (neighbors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Adjacency Matrix: The Mathematical Grid

    The adjacency matrix uses a grid where entry (i,j) = 1 if nodes are connected—the mathematician's favorite representation.

    Adjacency matrices enable powerful mathematical operations. Matrix multiplication reveals paths of different lengths, and eigenvalue analysis can uncover community structure. Google's PageRank algorithm fundamentally relies on matrix operations.
    """
    )
    return


@app.cell
def _():
    # Define adjacency matrix directly
    import numpy as np

    matrix = np.array([
        [0, 1, 1, 0, 0],  # Node 0 connects to nodes 1, 2
        [1, 0, 1, 1, 0],  # Node 1 connects to nodes 0, 2, 3
        [1, 1, 0, 0, 1],  # Node 2 connects to nodes 0, 1, 4
        [0, 1, 0, 0, 1],  # Node 3 connects to nodes 1, 4
        [0, 0, 1, 1, 0]   # Node 4 connects to nodes 2, 3
    ])

    print("Adjacency matrix:")
    print(matrix)
    return matrix, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Notice the symmetry: if node i connects to node j, then node j connects to node i (for undirected networks). This symmetry disappears in directed networks, where relationships can be one-way.

    ## Counting Node Degrees: Euler's Key Insight

    The degree of a node is the number of edges connected to it. This simple concept was central to Euler's proof—he realized that a valid bridge walk requires each landmass to have an even degree (except possibly the starting and ending points).

    In Königsberg, all four landmasses had odd degree, making the bridge walk impossible. This insight—that global properties emerge from local structure—remains fundamental to network analysis today.

    Here's how to compute degrees using each representation:

    ### From Edge Table: Counting Appearances

    Count how many times each node appears in the edge list.
    """
    )
    return


@app.cell
def _(edges):
    _degrees = [0] * 5
    for node1, node2 in edges:
        _degrees[node1] += 1
        _degrees[node2] += 1
    print("Degrees from edge list:", _degrees)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We increment the degree counter for both nodes in each edge because every edge contributes to two nodes' degrees. This is why the total degree always equals twice the number of edges.

    ### From Adjacency List: Counting Friends

    Count the length of each node's neighbor list—the most direct approach.
    """
    )
    return


@app.cell
def _(neighbors):
    _degrees = [len(neighbors[i]) for i in range(5)]
    print("Degrees from adjacency list:", _degrees)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### From Adjacency Matrix: Linear Algebra Power

    Sum each row (or column) of the matrix—leveraging vectorized operations.
    """
    )
    return


@app.cell
def _(matrix):
    _degrees = matrix.sum(axis=1)  # Sum rows
    print("Degrees from adjacency matrix:", _degrees)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    For undirected networks, row sums equal column sums. For directed networks, row sums give out-degree (outgoing connections) while column sums give in-degree (incoming connections).

    ## The Königsberg Bridge Problem in Code

    ![](https://towardsdatascience.com/wp-content/uploads/2024/05/15n0gkvpktkGYtAase5oYuw-1.png)

    Now let's apply these concepts to the original Königsberg bridge problem. The network has 4 nodes (landmasses) and 7 edges (bridges).

    ### Representing the Königsberg Network

    The Königsberg graph can be represented by a list of edges. Note that some bridges appear twice because there were multiple bridges between the same landmasses.
    """
    )
    return


@app.cell
def _():
    # Königsberg bridge network
    koenigsberg_edges = [(0,1), (0, 1), (0, 3), (1, 2), (1, 2), (1, 3), (2, 3)]
    print("Königsberg edges:", koenigsberg_edges)
    print("Total bridges:", len(koenigsberg_edges))
    return (koenigsberg_edges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Building the Adjacency Matrix

    Let's create the adjacency matrix for the Königsberg network:
    """
    )
    return


@app.cell
def _(koenigsberg_edges, np):
    # Create adjacency matrix for Königsberg
    A = np.zeros((4, 4))
    for i, j in koenigsberg_edges:
        A[i][j] += 1
        A[j][i] += 1

    print("Königsberg adjacency matrix:")
    print(A.astype(int))  # Convert to int for cleaner display
    return (A,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// admonition | Note

    In the Königsberg graph, the edges are *undirected*, meaning edge (i,j) is the same as edge (j,i), which is why we increment both entries $(i,j)$ and $(j,i)$ in the for loop. If the edges are *directed*, we treat (i,j) and (j,i) as two different edges, and increment only (i,j).

    ///

    ### Analyzing the Network

    Let's use our computational tools to analyze the Königsberg network:
    """
    )
    return


@app.cell
def _(A, np):
    # Count total edges
    _total_edges = np.sum(A) / 2  # Divide by 2 because each edge is counted twice
    print(f"Total edges: {_total_edges}")

    # Compute node degrees
    degrees = np.sum(A, axis=1)
    print("Node degrees:", degrees.astype(int))

    # Check for odd degrees
    _is_odd = degrees % 2 == 1
    _num_odd_nodes = np.sum(_is_odd)
    print(f"Nodes with odd degree: {_num_odd_nodes}")
    print(f"Odd degree nodes: {np.where(_is_odd)[0]}")
    return (degrees,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// attention | Important

    The number of edges connected to a node is called the ***degree*** of the node.

    ///

    ### Applying Euler's Theorem Computationally

    Now we can implement Euler's theorem as code:
    """
    )
    return


@app.cell
def _(degrees, matrix, np):
    def has_euler_path(degrees):
        """
        Check if a graph has an Euler path based on node degrees.

        Euler's theorem: A graph has an Euler path if and only if:
        - All nodes have even degree, OR
        - Exactly two nodes have odd degree
        """
        odd_count = np.sum(degrees % 2 == 1)

        if odd_count == 0:
            return True, "Euler circuit exists (all nodes have even degree)"
        elif odd_count == 2:
            return True, "Euler path exists (exactly 2 nodes have odd degree)"
        else:
            return False, f"No Euler path ({odd_count} nodes have odd degree)"

    # Test on Königsberg
    _has_path, _reason = has_euler_path(degrees)
    print(f"Königsberg network: {_has_path}")
    print(f"Reason: {_reason}")

    # Test on our simple example network
    _simple_degrees = matrix.sum(axis=1)
    _has_path_simple, _reason_simple = has_euler_path(_simple_degrees)
    print(f"\nSimple network: {_has_path_simple}")
    print(f"Reason: {_reason_simple}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// admonition | Tip

    The `np.sum(A, axis = 1)` computes the row sum of `A`. Alternatively, `np.sum(A, axis = 0)` computes the column sum of `A`.
    Check out the numpy [documentation](https://numpy.org/doc/stable/reference/generated/numpy.sum.html) for more details.

    ///


    ## Summary: From Euler's Insight to Modern Computation

    You now understand how to:

    1. **Represent networks** using edge lists, adjacency lists, and adjacency matrices
    2. **Convert between representations** as needed for different algorithms
    3. **Compute node degrees** efficiently using different data structures
    4. **Apply Euler's theorem** computationally to determine if Euler paths exist
    5. **Handle large networks** using sparse matrix representations

    These computational tools, built on Euler's 300-year-old insight, now power everything from GPS navigation systems to social media algorithms. The fundamental principle remains the same: ***abstract the essential structure, then apply mathematical reasoning to solve concrete problems***.

    The next step is to practice these concepts with real network data and explore more advanced network analysis techniques!
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
