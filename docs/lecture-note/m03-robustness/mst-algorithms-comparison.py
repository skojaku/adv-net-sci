import marimo

__generated_with = "0.14.16"
app = marimo.App(
    width="full",
    app_title="MST Algorithms: Kruskal vs Prim Comparison",
)


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    return mo, pd, plt


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
def _(edges, nodes):
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
            if union(u, v):
                mst_edges.append((u, v, weight))
                steps.append(
                    {
                        "edge": (u, v),
                        "weight": weight,
                        "action": "added",
                        "reason": f"Connects {u} and {v} without creating cycle",
                    }
                )

            # Continue until we have a spanning tree OR all edges are processed
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
                steps.append(
                    {
                        "edge": (u, v),
                        "weight": weight,
                        "action": "added",
                        "reason": f"Cheapest connection from visited set to {v}",
                    }
                )

        return mst_edges, steps


    # Run both algorithms
    kruskal_mst, kruskal_steps = kruskal_algorithm(nodes, edges)
    prim_mst, prim_steps = prim_algorithm(nodes, edges)

    # Calculate total weights
    kruskal_weight = sum(w for _, _, w in kruskal_mst)
    prim_weight = sum(w for _, _, w in prim_mst)
    return kruskal_steps, kruskal_weight, prim_steps, prim_weight


@app.cell
def _(kruskal_steps, kruskal_weight, mo, prim_weight, time_step):
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
        step_info = f"**Current State**: Complete MST - All {max_steps} edges added"

    results = mo.md(f"""
    ## Algorithm Results

    {step_info}

    ### Kruskal's Algorithm (Global Approach)  
    - **Total MST Weight**: {kruskal_weight}
    - **Method**: Sort all edges globally, add cheapest without creating cycles

    ### Prim's Algorithm (Local Growth)
    - **Total MST Weight**: {prim_weight}  
    - **Method**: Start from node A, grow tree by adding cheapest connections

    ### Comparison
    - **Total Weights Match**: {weight_match}

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


if __name__ == "__main__":
    app.run()
