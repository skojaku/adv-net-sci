# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scipy==1.16.1",
# ]
# ///
import marimo

__generated_with = "0.14.16"
app = marimo.App(
    width="full",
    app_title="MST Algorithms: Kruskal vs Prim Comparison",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Minimum Spanning Tree Algorithms: Kruskal vs Prim

    This interactive demonstration shows the key differences between **Kruskal's Algorithm** and **Prim's Algorithm** 
    for finding minimum spanning trees using a power grid example.

    Both algorithms solve the same problem but with fundamentally different approaches:
    - **Kruskal's**: Global perspective - sorts all edges, builds forest, prevents cycles
    - **Prim's**: Local growth - starts from one node, grows tree by adding cheapest connections
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    return mo, pd, plt, np, csr_matrix, connected_components


@app.cell
def _(mo):
    # Control for edge weight uniqueness
    unique_weights = mo.ui.checkbox(
        label="Use unique edge weights (when unchecked, some edges have same weight)",
        value=True,
    )

    # Time step slider - fixed to accommodate MST (max 6 edges for 7 nodes)
    time_step = mo.ui.slider(
        start=0,
        stop=6,  # Fixed max for power grid (7 nodes = 6 MST edges)
        step=1,
        value=6,  # Start at final state
        label="Algorithm Time Step (0=start, 6=complete MST)",
    )
    return time_step, unique_weights


@app.cell
def _(unique_weights):
    def create_power_grid_graph(use_unique_weights=True):
        """Create power grid graph with nodes and edges"""

        # Define nodes with positions
        nodes = {
            "A": (0, 1),
            "B": (1, 2),
            "C": (1, 0),
            "D": (2, 2.5),
            "E": (2, 1.5),
            "F": (2, 0.5),
            "G": (2, -0.5),
        }

        if use_unique_weights:
            # All weights are unique
            edges = [
                ("A", "B", 8),
                ("A", "C", 12),
                ("B", "D", 5),
                ("B", "E", 7),
                ("C", "F", 6),
                ("C", "G", 4),
                ("D", "E", 3),
                ("E", "F", 9),
                ("F", "G", 2),
                ("D", "C", 11),
            ]
        else:
            # Some weights are the same - multiple MSTs possible
            edges = [
                ("A", "B", 8),
                ("A", "C", 12),
                ("B", "D", 5),
                ("B", "E", 7),
                ("C", "F", 5),  # Same as B-D
                ("C", "G", 4),
                ("D", "E", 3),
                ("E", "F", 9),
                ("F", "G", 2),
                ("D", "C", 7),  # Same as B-E
            ]

        return nodes, edges


    # Create the graph based on current setting
    nodes, edges = create_power_grid_graph(unique_weights.value)
    return edges, nodes


@app.cell
def _(connected_components, csr_matrix, edges, nodes, np):
    def check_connectivity(nodes_dict, edges_subset):
        """Check if the graph formed by edges_subset is connected using scipy"""
        if not edges_subset:
            return len(nodes_dict) == 1, 1  # Single node is connected
        
        # Create node to index mapping
        node_list = list(nodes_dict.keys())
        node_to_idx = {node: i for i, node in enumerate(node_list)}
        n_nodes = len(node_list)
        
        # Build adjacency matrix
        row, col = [], []
        for u, v, _ in edges_subset:
            i, j = node_to_idx[u], node_to_idx[v]
            row.extend([i, j])
            col.extend([j, i])
        
        if not row:  # No edges
            return False, n_nodes
            
        data = [1] * len(row)
        adj_matrix = csr_matrix((data, (row, col)), shape=(n_nodes, n_nodes))
        
        # Check connectivity
        n_components, labels = connected_components(adj_matrix, directed=False)
        is_connected = n_components == 1
        return is_connected, n_components
    
    def kruskal_algorithm(nodes_dict, edges_list):
        """Kruskal's algorithm implementation without networkx"""

        # Step 1: Sort edges by weight (global perspective)
        sorted_edges = sorted(edges_list, key=lambda x: x[2])

        # Initialize Union-Find data structure
        parent = {}
        rank = {}
        
        # Initialize all nodes in Union-Find
        for node in nodes_dict:
            parent[node] = node
            rank[node] = 0

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        mst_edges = []
        steps = []

        for u, v, weight in sorted_edges:
            # Check connectivity before adding edge
            is_connected_before, n_components_before = check_connectivity(nodes_dict, mst_edges)
            
            if union(u, v):
                mst_edges.append((u, v, weight))
                is_connected_after, n_components_after = check_connectivity(nodes_dict, mst_edges)
                steps.append(
                    {
                        "edge": (u, v),
                        "weight": weight,
                        "action": "added",
                        "reason": f"Connects {u} and {v} without creating cycle (components: {n_components_before}→{n_components_after})",
                    }
                )
            else:
                steps.append(
                    {
                        "edge": (u, v),
                        "weight": weight,
                        "action": "skipped",
                        "reason": f"Would create cycle between {u} and {v}",
                    }
                )

            if len(mst_edges) == len(nodes_dict) - 1:
                break

        return mst_edges, steps


    def prim_algorithm(nodes_dict, edges_list, start_node="A"):
        """Prim's algorithm implementation without networkx"""

        # Create adjacency list
        adj = {node: [] for node in nodes_dict}
        for u, v, weight in edges_list:
            adj[u].append((v, weight))
            adj[v].append((u, weight))

        visited = {start_node}
        mst_edges = []
        steps = []

        steps.append(
            {
                "node": start_node,
                "action": "start",
                "reason": f"Starting from {start_node}",
            }
        )

        while len(visited) < len(nodes_dict):
            min_weight = float("inf")
            min_edge = None

            # Find cheapest edge from visited to unvisited nodes
            for node in visited:
                for neighbor, weight in adj[node]:
                    if neighbor not in visited and weight < min_weight:
                        min_weight = weight
                        min_edge = (node, neighbor, weight)

            if min_edge:
                u, v, weight = min_edge
                visited.add(v)
                mst_edges.append((u, v, weight))
                is_connected, n_components = check_connectivity(nodes_dict, mst_edges)
                steps.append(
                    {
                        "edge": (u, v),
                        "weight": weight,
                        "action": "added",
                        "reason": f"Cheapest connection from visited set to {v} ({n_components} components)",
                    }
                )

        return mst_edges, steps


    # Run both algorithms
    kruskal_mst, kruskal_steps = kruskal_algorithm(nodes, edges)
    prim_mst, prim_steps = prim_algorithm(nodes, edges)

    # Calculate total weights
    kruskal_weight = sum(w for _, _, w in kruskal_mst)
    prim_weight = sum(w for _, _, w in prim_mst)
    return (
        kruskal_mst,
        kruskal_steps,
        kruskal_weight,
        prim_mst,
        prim_steps,
        prim_weight,
    )


@app.cell
def _(
    kruskal_mst,
    kruskal_steps,
    kruskal_weight,
    mo,
    nodes,
    prim_mst,
    prim_weight,
    time_step,
):
    # Display algorithm results with current step information
    weight_match = "✅ Same" if kruskal_weight == prim_weight else "❌ Different"

    # Get current step information
    current_step = time_step.value
    max_steps = len([s for s in kruskal_steps if s["action"] == "added"])

    # Current step details
    if current_step == 0:
        step_info = "**Current State**: Initial state - no edges added yet"
    elif current_step <= max_steps:
        step_info = f"**Current State**: Step {current_step}/{max_steps} - Building MST progressively"
    else:
        step_info = (
            f"**Current State**: Complete MST - All {max_steps} edges added"
        )

    results = mo.md(f"""
    ## Algorithm Results

    {step_info}

    ### Kruskal's Algorithm (Global Approach)
    - **Total MST Weight**: {kruskal_weight}
    - **Edges Selected**: {len(kruskal_mst)} edges connecting {len(nodes)} nodes
    - **Method**: Sort all edges globally, add cheapest without creating cycles

    ### Prim's Algorithm (Local Growth)
    - **Total MST Weight**: {prim_weight}  
    - **Edges Selected**: {len(prim_mst)} edges connecting {len(nodes)} nodes
    - **Method**: Start from node A, grow tree by adding cheapest connections

    ### Comparison
    - **Total Weights Match**: {weight_match}
    - **MST Uniqueness**: {
        "Unique MST guaranteed when all edge weights are different"
        if weight_match == "✅ Same"
        else "Multiple MSTs possible when some edge weights are equal"
    }

    ---

    **💡 Tip**: Use the time step slider above to see how each algorithm builds the MST step by step. 
    Connected nodes are shown in **light red**, unconnected nodes in **light blue**.
    """)

    results
    return


@app.cell
def _(mo, time_step, unique_weights):
    mo.vstack(
        [
            mo.md("## Controls"),
            unique_weights,
            time_step,
            mo.md(
                "**Instructions**: Move the slider to see how each algorithm builds the MST step by step."
            ),
        ]
    )
    return


@app.cell
def _(edges, kruskal_steps, nodes, plt, prim_steps, time_step):
    def visualize_both_algorithms():
        """Create side-by-side visualization of both algorithms with time step control"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Get edges to show up to current time step for each algorithm
        current_step = time_step.value

        # For Kruskal: edges added in order they appear in steps
        kruskal_edges_to_show = []
        for i, step in enumerate(kruskal_steps):
            if i >= current_step:
                break
            if step["action"] == "added":
                u, v = step["edge"]
                weight = step["weight"]
                kruskal_edges_to_show.append((u, v, weight))

        # For Prim: edges added in order they appear in steps
        prim_edges_to_show = []
        for i, step in enumerate(prim_steps[1:], 1):  # Skip the 'start' step
            if i > current_step:
                break
            if step["action"] == "added":
                u, v = step["edge"]
                weight = step["weight"]
                prim_edges_to_show.append((u, v, weight))

        algorithms = [
            (ax1, "Kruskal's Algorithm", kruskal_edges_to_show),
            (ax2, "Prim's Algorithm", prim_edges_to_show),
        ]

        for ax, title, edges_to_show in algorithms:
            ax.clear()
            ax.set_facecolor("white")

            # Draw all possible edges - dashed for unconnected
            mst_edge_set = set((u, v) for u, v, _ in edges_to_show) | set(
                (v, u) for u, v, _ in edges_to_show
            )

            for u, v, weight in edges:
                x1, y1 = nodes[u]
                x2, y2 = nodes[v]

                if (u, v) in mst_edge_set or (v, u) in mst_edge_set:
                    # MST edge - solid black line
                    ax.plot(
                        [x1, x2],
                        [y1, y2],
                        "black",
                        linewidth=3,
                        solid_capstyle="round",
                    )
                else:
                    # Non-MST edge - dashed grey line
                    ax.plot(
                        [x1, x2],
                        [y1, y2],
                        "grey",
                        linewidth=2,
                        linestyle="--",
                        alpha=0.7,
                    )

                # Add edge weight labels with larger font
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax.text(
                    mid_x,
                    mid_y,
                    str(weight),
                    fontsize=15,
                    bbox=dict(
                        boxstyle="round,pad=0.2", facecolor="white", alpha=0.9
                    ),
                    ha="center",
                    va="center",
                    fontweight="bold",
                )

            # Draw nodes - color based on connection status
            connected_nodes = set()
            if "Prim" in title:
                # For Prim, start with node A always connected
                connected_nodes.add("A")
                for u, v, _ in edges_to_show:
                    connected_nodes.add(u)
                    connected_nodes.add(v)
            else:
                # For Kruskal, find all nodes in connected components
                if edges_to_show:
                    # Build Union-Find to determine connected components
                    parent = {node: node for node in nodes}
                    
                    def find_root(x):
                        if parent[x] != x:
                            parent[x] = find_root(parent[x])
                        return parent[x]
                    
                    def union_nodes(x, y):
                        px, py = find_root(x), find_root(y)
                        if px != py:
                            parent[py] = px
                    
                    # Apply edges to build connected components
                    for u, v, _ in edges_to_show:
                        union_nodes(u, v)
                    
                    # Find all nodes connected to any component that has edges
                    connected_roots = set()
                    for u, v, _ in edges_to_show:
                        connected_roots.add(find_root(u))
                        connected_roots.add(find_root(v))
                    
                    for node in nodes:
                        if find_root(node) in connected_roots:
                            connected_nodes.add(node)

            for node, (x, y) in nodes.items():
                color = (
                    "#f5cbcc" if node in connected_nodes else "#d0e2f3"
                )  # light red : light blue
                # Draw larger circle with black border
                circle = plt.Circle((x, y), 0.15, color=color, zorder=5)
                ax.add_patch(circle)
                # Add black border
                border_circle = plt.Circle(
                    (x, y),
                    0.15,
                    fill=False,
                    edgecolor="black",
                    linewidth=2,
                    zorder=6,
                )
                ax.add_patch(border_circle)
                # Larger text
                ax.text(
                    x,
                    y,
                    node,
                    ha="center",
                    va="center",
                    fontsize=15,
                    fontweight="bold",
                    zorder=7,
                )

            # Clean title
            ax.set_title(title, fontsize=18, fontweight="bold", pad=20)
            ax.set_aspect("equal")
            ax.axis("off")

            # Set axis limits with padding
            x_coords = [x for x, y in nodes.values()]
            y_coords = [y for x, y in nodes.values()]
            ax.set_xlim(min(x_coords) - 0.3, max(x_coords) + 0.3)
            ax.set_ylim(min(y_coords) - 0.3, max(y_coords) + 0.3)

        plt.tight_layout()
        return fig


    # Create and display the visualization
    fig = visualize_both_algorithms()
    fig
    return


@app.cell
def _(kruskal_steps, mo, pd, prim_steps):
    # Show step-by-step construction
    step_displays = []

    # Kruskal steps
    kruskal_df = pd.DataFrame(
        [
            {
                "Step": i + 1,
                "Edge": f"{step['edge'][0]}-{step['edge'][1]}"
                if "edge" in step
                else "N/A",
                "Weight": step.get("weight", "-"),
                "Action": step["action"].title(),
                "Reason": step["reason"],
            }
            for i, step in enumerate(kruskal_steps)
        ]
    )

    step_displays.append(
        mo.vstack(
            [
                mo.md("### Kruskal's Algorithm - Step by Step"),
                mo.md(
                    "**Key Insight**: Kruskal considers ALL edges globally, always picking the cheapest available edge that doesn't create a cycle."
                ),
                mo.ui.table(kruskal_df, selection=None),
            ]
        )
    )

    # Prim steps
    prim_df = pd.DataFrame(
        [
            {
                "Step": i + 1,
                "Node/Edge": (
                    step.get("node", "N/A")
                    if "node" in step
                    else f"{step['edge'][0]}-{step['edge'][1]}"
                    if "edge" in step
                    else "N/A"
                ),
                "Weight": step.get("weight", "-"),
                "Action": step["action"].title(),
                "Reason": step["reason"],
            }
            for i, step in enumerate(prim_steps)
        ]
    )

    step_displays.append(
        mo.vstack(
            [
                mo.md("### Prim's Algorithm - Step by Step"),
                mo.md(
                    "**Key Insight**: Prim grows the tree locally, always expanding from the current connected component to the nearest unconnected node."
                ),
                mo.ui.table(prim_df, selection=None),
            ]
        )
    )

    mo.vstack(step_displays)
    return


@app.cell
def _(mo, unique_weights):
    if unique_weights.value:
        uniqueness_explanation = mo.md("""
        ### Edge Weight Uniqueness: All Unique ✅

        With all edge weights being unique, both algorithms are **guaranteed to produce identical MSTs**. 
        This demonstrates the mathematical principle that when edge weights are unique, 
        the minimum spanning tree is unique regardless of the construction algorithm.

        **Key Points:**
        - Same total weight for both algorithms
        - Same edges selected (possibly in different order)
        - Demonstrates algorithmic equivalence
        """)
    else:
        uniqueness_explanation = mo.md("""
        ### Edge Weight Uniqueness: Some Duplicate Weights ⚠️

        With some edges having identical weights, **multiple valid MSTs may exist**. 
        Different algorithms might choose different edges of the same weight, 
        leading to different trees with the same total cost.

        **Key Points:**
        - Both algorithms still find optimal solutions
        - Total weights will still match
        - Different edges might be selected when weights are tied
        - Demonstrates that MST uniqueness depends on edge weight uniqueness
        """)

    uniqueness_explanation
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Key Algorithmic Differences

    | Aspect | Kruskal's Algorithm | Prim's Algorithm |
    |--------|-------------------|------------------|
    | **Perspective** | Global - considers all edges | Local - grows from one point |
    | **Initial Step** | Sort ALL edges by weight | Choose starting node (PowerPlant) |
    | **Edge Selection** | Pick globally cheapest edge | Pick cheapest edge to unvisited node |
    | **Data Structure** | Union-Find (for cycle detection) | Adjacency list + visited set |
    | **Growth Pattern** | May build multiple disconnected trees initially | Always maintains single connected tree |
    | **Cycle Prevention** | Explicit cycle checking with Union-Find | Implicit - only connects to unvisited nodes |
    | **Implementation** | More complex (Union-Find structure) | More intuitive (local expansion) |

    ## Power Grid Context

    In our power grid example:
    - **PowerPlant**: Central power generation facility
    - **SubstationA/B**: Distribution substations  
    - **TownA/B/C/D**: End consumers (residential/commercial areas)
    - **Edge weights**: Cable installation costs (in thousands of dollars)

    Both algorithms find the minimum cost to connect all locations while ensuring every town receives power.
    """
    )
    return


if __name__ == "__main__":
    app.run()
