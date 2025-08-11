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
    from matplotlib.patches import FancyBboxPatch
    return FancyBboxPatch, mo, pd, plt


@app.cell
def _(mo):
    # Control for edge weight uniqueness
    unique_weights = mo.ui.checkbox(
        label="Use unique edge weights (when unchecked, some edges have same weight)", 
        value=True
    )
    
    # Time step slider - fixed to accommodate MST (max 6 edges for 7 nodes)
    time_step = mo.ui.slider(
        start=0, 
        stop=6,  # Fixed max for power grid (7 nodes = 6 MST edges)
        step=1, 
        value=6,  # Start at final state
        label="Algorithm Time Step (0=start, 6=complete MST)"
    )

    mo.vstack([
        mo.md("## Controls"),
        unique_weights,
        time_step,
        mo.md("**Instructions**: Move the slider to see how each algorithm builds the MST step by step.")
    ])
    return time_step, unique_weights


@app.cell
def _(unique_weights):
    def create_power_grid_graph(use_unique_weights=True):
        """Create power grid graph with nodes and edges"""

        # Define nodes with positions
        nodes = {
            'PowerPlant': (0, 1),
            'SubstationA': (1, 2), 
            'SubstationB': (1, 0),
            'TownA': (2, 2.5), 
            'TownB': (2, 1.5),
            'TownC': (2, 0.5), 
            'TownD': (2, -0.5)
        }

        if use_unique_weights:
            # All weights are unique
            edges = [
                ('PowerPlant', 'SubstationA', 12),
                ('PowerPlant', 'SubstationB', 8),
                ('SubstationA', 'TownA', 5),
                ('SubstationA', 'TownB', 7),
                ('SubstationB', 'TownC', 6),
                ('SubstationB', 'TownD', 4),
                ('TownA', 'TownB', 3),
                ('TownB', 'TownC', 9),
                ('TownC', 'TownD', 2),
                ('TownA', 'SubstationB', 11)
            ]
        else:
            # Some weights are the same - multiple MSTs possible
            edges = [
                ('PowerPlant', 'SubstationA', 12),
                ('PowerPlant', 'SubstationB', 8),
                ('SubstationA', 'TownA', 5),
                ('SubstationA', 'TownB', 7),
                ('SubstationB', 'TownC', 5),  # Same as SubstationA-TownA
                ('SubstationB', 'TownD', 4),
                ('TownA', 'TownB', 3),
                ('TownB', 'TownC', 9),
                ('TownC', 'TownD', 2),
                ('TownA', 'SubstationB', 7)  # Same as SubstationA-TownB
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

        def find(x):
            if x not in parent:
                parent[x] = x
                rank[x] = 0
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
                steps.append({
                    'edge': (u, v),
                    'weight': weight,
                    'action': 'added',
                    'reason': f'Connects {u} and {v} without creating cycle'
                })
            else:
                steps.append({
                    'edge': (u, v),
                    'weight': weight,
                    'action': 'skipped',
                    'reason': f'Would create cycle between {u} and {v}'
                })

            if len(mst_edges) == len(nodes_dict) - 1:
                break

        return mst_edges, steps

    def prim_algorithm(nodes_dict, edges_list, start_node='PowerPlant'):
        """Prim's algorithm implementation without networkx"""

        # Create adjacency list
        adj = {node: [] for node in nodes_dict}
        for u, v, weight in edges_list:
            adj[u].append((v, weight))
            adj[v].append((u, weight))

        visited = {start_node}
        mst_edges = []
        steps = []

        steps.append({
            'node': start_node,
            'action': 'start',
            'reason': f'Starting from {start_node}'
        })

        while len(visited) < len(nodes_dict):
            min_weight = float('inf')
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
                steps.append({
                    'edge': (u, v),
                    'weight': weight,
                    'action': 'added',
                    'reason': f'Cheapest connection from visited set to {v}'
                })

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
    max_steps = len([s for s in kruskal_steps if s['action'] == 'added'])

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
    - **Edges Selected**: {len(kruskal_mst)} edges connecting {len(nodes)} nodes
    - **Method**: Sort all edges globally, add cheapest without creating cycles

    ### Prim's Algorithm (Local Growth)
    - **Total MST Weight**: {prim_weight}  
    - **Edges Selected**: {len(prim_mst)} edges connecting {len(nodes)} nodes
    - **Method**: Start from PowerPlant, grow tree by adding cheapest connections

    ### Comparison
    - **Total Weights Match**: {weight_match}
    - **MST Uniqueness**: {
        "Unique MST guaranteed when all edge weights are different" if weight_match == "✅ Same" 
        else "Multiple MSTs possible when some edge weights are equal"
    }

    ---

    **💡 Tip**: Use the time step slider above to see how each algorithm builds the MST step by step. 
    Connected nodes are shown in **green**, unconnected nodes in **blue**.
    """)

    results
    return


@app.cell
def _(FancyBboxPatch, edges, kruskal_steps, nodes, plt, prim_steps, time_step):
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
            if step['action'] == 'added':
                u, v = step['edge']
                weight = step['weight']
                kruskal_edges_to_show.append((u, v, weight))

        # For Prim: edges added in order they appear in steps  
        prim_edges_to_show = []
        for i, step in enumerate(prim_steps[1:], 1):  # Skip the 'start' step
            if i > current_step:
                break
            if step['action'] == 'added':
                u, v = step['edge']
                weight = step['weight']
                prim_edges_to_show.append((u, v, weight))

        algorithms = [
            (ax1, "Kruskal's Algorithm (Global Approach)", kruskal_edges_to_show),
            (ax2, "Prim's Algorithm (Local Growth)", prim_edges_to_show)
        ]

        for ax, title, edges_to_show in algorithms:
            ax.clear()

            # Draw all possible edges in light gray
            for u, v, weight in edges:
                x1, y1 = nodes[u]
                x2, y2 = nodes[v]
                ax.plot([x1, x2], [y1, y2], 'lightgray', linewidth=1, alpha=0.3)

                # Add edge weight labels
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax.text(mid_x, mid_y, str(weight), fontsize=8, 
                       bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))

            # Draw MST edges built so far in red
            for u, v, weight in edges_to_show:
                x1, y1 = nodes[u]
                x2, y2 = nodes[v]
                ax.plot([x1, x2], [y1, y2], 'red', linewidth=3, alpha=0.8)

            # Draw nodes - color differently based on connection status
            connected_nodes = set()
            if 'Prim' in title:
                # For Prim, start with PowerPlant always connected
                connected_nodes.add('PowerPlant')
                for u, v, _ in edges_to_show:
                    connected_nodes.add(u)
                    connected_nodes.add(v)
            else:
                # For Kruskal, find connected components
                for u, v, _ in edges_to_show:
                    connected_nodes.add(u)
                    connected_nodes.add(v)

            for node, (x, y) in nodes.items():
                color = 'lightgreen' if node in connected_nodes else 'lightblue'
                circle = plt.Circle((x, y), 0.1, color=color, alpha=0.9, zorder=5)
                ax.add_patch(circle)
                ax.text(x, y, node.replace('Substation', 'Sub').replace('PowerPlant', 'Plant'), 
                       ha='center', va='center', fontsize=8, fontweight='bold', zorder=6)

            # Update title with current step info
            total_steps = len([s for s in (kruskal_steps if 'Kruskal' in title else prim_steps) if s['action'] == 'added'])
            step_info = f" (Step {current_step}/{total_steps})"
            ax.set_title(title + step_info, fontsize=14, fontweight='bold', pad=20)
            ax.set_aspect('equal')
            ax.axis('off')

            # Set axis limits with padding
            x_coords = [x for x, y in nodes.values()]
            y_coords = [y for x, y in nodes.values()]
            ax.set_xlim(min(x_coords) - 0.3, max(x_coords) + 0.3)
            ax.set_ylim(min(y_coords) - 0.3, max(y_coords) + 0.3)

            # Add algorithm description box with current action
            if 'Kruskal' in title:
                description = "1. Sort all edges by weight\n2. Add cheapest edge if no cycle\n3. Repeat until tree complete"
                if current_step > 0 and current_step <= len(kruskal_steps):
                    current_action = kruskal_steps[current_step-1]
                    if current_action['action'] == 'added':
                        description += f"\n\nCurrent: Adding {current_action['edge'][0]}-{current_action['edge'][1]} (weight {current_action['weight']})"
                    elif current_action['action'] == 'skipped':
                        description += f"\n\nCurrent: Skipping {current_action['edge'][0]}-{current_action['edge'][1]} (creates cycle)"
            else:
                description = "1. Start from PowerPlant\n2. Add cheapest edge to new node\n3. Grow tree incrementally"
                if current_step > 0 and current_step < len(prim_steps):
                    current_action = prim_steps[current_step]
                    if current_action['action'] == 'added':
                        description += f"\n\nCurrent: Adding {current_action['edge'][0]}-{current_action['edge'][1]} (weight {current_action['weight']})"

            bbox = FancyBboxPatch((0.02, 0.02), 0.25, 0.2, 
                                boxstyle="round,pad=0.01", 
                                transform=ax.transAxes,
                                facecolor='wheat', alpha=0.8, edgecolor='black')
            ax.add_patch(bbox)
            ax.text(0.03, 0.03, description, transform=ax.transAxes, 
                   fontsize=8, verticalalignment='bottom')

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
    kruskal_df = pd.DataFrame([
        {
            'Step': i+1,
            'Edge': f"{step['edge'][0]}-{step['edge'][1]}" if 'edge' in step else "N/A",
            'Weight': step.get('weight', '-'),
            'Action': step['action'].title(),
            'Reason': step['reason']
        }
        for i, step in enumerate(kruskal_steps)
    ])

    step_displays.append(
        mo.vstack([
            mo.md("### Kruskal's Algorithm - Step by Step"),
            mo.md("**Key Insight**: Kruskal considers ALL edges globally, always picking the cheapest available edge that doesn't create a cycle."),
            mo.ui.table(kruskal_df, selection=None)
        ])
    )

    # Prim steps  
    prim_df = pd.DataFrame([
        {
            'Step': i+1,
            'Node/Edge': (step.get('node', 'N/A') if 'node' in step 
                         else f"{step['edge'][0]}-{step['edge'][1]}" if 'edge' in step 
                         else 'N/A'),
            'Weight': step.get('weight', '-'),
            'Action': step['action'].title(),
            'Reason': step['reason']
        }
        for i, step in enumerate(prim_steps)
    ])

    step_displays.append(
        mo.vstack([
            mo.md("### Prim's Algorithm - Step by Step"),
            mo.md("**Key Insight**: Prim grows the tree locally, always expanding from the current connected component to the nearest unconnected node."),
            mo.ui.table(prim_df, selection=None)
        ])
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
