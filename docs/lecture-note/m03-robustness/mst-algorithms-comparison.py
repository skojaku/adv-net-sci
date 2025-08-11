# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.5",
#     "networkx==3.4.2",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
# ]
# ///
import marimo

__generated_with = "0.9.14"
app = marimo.App(
    app_title="MST Algorithms: Kruskal vs Prim Comparison",
    width="full"
)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Minimum Spanning Tree Algorithms: Kruskal vs Prim

        This interactive demonstration shows the key differences between **Kruskal's Algorithm** and **Prim's Algorithm** for finding minimum spanning trees.

        Both algorithms solve the same problem but with fundamentally different approaches:
        - **Kruskal's**: Global perspective - sorts all edges, builds forest, prevents cycles
        - **Prim's**: Local growth - starts from one node, grows tree by adding cheapest connections

        Use the controls below to explore different graphs and see how each algorithm constructs the MST step by step.
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    import networkx as nx
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.patches import FancyBboxPatch
    import random
    return FancyBboxPatch, mo, np, nx, pd, plt, random


@app.cell
def __(mo):
    # Create controls for the interactive demo
    graph_selector = mo.ui.dropdown(
        options=["Simple 5-node", "Grid 3x3", "Random 8-node", "Power Grid Example"],
        value="Simple 5-node",
        label="Choose Graph Type"
    )
    
    show_step_by_step = mo.ui.checkbox(
        label="Show Step-by-Step Construction", 
        value=True
    )
    
    algorithm_choice = mo.ui.radio(
        options=["Both", "Kruskal Only", "Prim Only"],
        value="Both",
        label="Algorithm Display"
    )
    
    mo.vstack([
        mo.md("## Interactive Controls"),
        mo.hstack([graph_selector, show_step_by_step]),
        algorithm_choice
    ])
    return algorithm_choice, graph_selector, show_step_by_step


@app.cell
def __(graph_selector, np, nx, random):
    def create_graph(graph_type):
        """Create different types of graphs for demonstration"""
        random.seed(42)  # For reproducible results
        np.random.seed(42)
        
        if graph_type == "simple":
            # Simple 5-node graph - good for understanding basics
            G = nx.Graph()
            edges = [
                ('A', 'B', 4), ('A', 'C', 2), ('A', 'D', 7),
                ('B', 'C', 1), ('B', 'E', 5),
                ('C', 'D', 3), ('C', 'E', 6),
                ('D', 'E', 8)
            ]
            G.add_weighted_edges_from(edges)
            pos = {'A': (0, 1), 'B': (1, 2), 'C': (1, 0), 'D': (2, 0), 'E': (2, 2)}
            
        elif graph_type == "grid":
            # 3x3 grid with random weights
            G = nx.grid_2d_graph(3, 3)
            pos = {node: node for node in G.nodes()}
            # Add random weights
            for edge in G.edges():
                G[edge[0]][edge[1]]['weight'] = random.randint(1, 10)
                
        elif graph_type == "random":
            # Random connected graph
            G = nx.erdos_renyi_graph(8, 0.4, seed=42)
            # Ensure connectivity
            if not nx.is_connected(G):
                components = list(nx.connected_components(G))
                for i in range(len(components) - 1):
                    node1 = list(components[i])[0]
                    node2 = list(components[i+1])[0]
                    G.add_edge(node1, node2)
            
            # Add random weights
            for edge in G.edges():
                G[edge[0]][edge[1]]['weight'] = random.randint(1, 15)
            pos = nx.spring_layout(G, seed=42)
            
        elif graph_type == "power_grid":
            # Example inspired by power grid connections
            G = nx.Graph()
            edges = [
                ('PowerPlant', 'SubstationA', 12), ('PowerPlant', 'SubstationB', 8),
                ('SubstationA', 'TownA', 5), ('SubstationA', 'TownB', 7),
                ('SubstationB', 'TownC', 6), ('SubstationB', 'TownD', 4),
                ('TownA', 'TownB', 3), ('TownB', 'TownC', 9),
                ('TownC', 'TownD', 2), ('TownA', 'SubstationB', 11)
            ]
            G.add_weighted_edges_from(edges)
            pos = {
                'PowerPlant': (0, 1),
                'SubstationA': (1, 2), 'SubstationB': (1, 0),
                'TownA': (2, 2.5), 'TownB': (2, 1.5),
                'TownC': (2, 0.5), 'TownD': (2, -0.5)
            }
            
        return G, pos

    # Create the selected graph - map display names to internal values
    graph_type_map = {
        "Simple 5-node": "simple",
        "Grid 3x3": "grid", 
        "Random 8-node": "random",
        "Power Grid Example": "power_grid"
    }
    graph, pos = create_graph(graph_type_map[graph_selector.value])
    return create_graph, graph, pos


@app.cell
def __(graph, nx):
    def kruskal_algorithm(G):
        """
        Kruskal's algorithm implementation with step tracking
        Returns: MST edges and step-by-step construction
        """
        edges = []
        for u, v, data in G.edges(data=True):
            edges.append((data['weight'], u, v))
        
        # Step 1: Sort edges by weight (global perspective)
        edges.sort()
        
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
        
        for weight, u, v in edges:
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
                
            if len(mst_edges) == len(G.nodes()) - 1:
                break
                
        return mst_edges, steps

    def prim_algorithm(G, start_node=None):
        """
        Prim's algorithm implementation with step tracking
        Returns: MST edges and step-by-step construction
        """
        if start_node is None:
            start_node = list(G.nodes())[0]
            
        visited = {start_node}
        mst_edges = []
        steps = []
        
        steps.append({
            'node': start_node,
            'action': 'start',
            'reason': f'Starting from node {start_node}'
        })
        
        while len(visited) < len(G.nodes()):
            min_weight = float('inf')
            min_edge = None
            
            # Find cheapest edge from visited to unvisited nodes
            for node in visited:
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        weight = G[node][neighbor]['weight']
                        if weight < min_weight:
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
    kruskal_mst, kruskal_steps = kruskal_algorithm(graph)
    prim_mst, prim_steps = prim_algorithm(graph)
    
    # Verify they produce the same total weight
    kruskal_weight = sum(w for _, _, w in kruskal_mst)
    prim_weight = sum(w for _, _, w in prim_mst)
    
    return (
        kruskal_algorithm, kruskal_mst, kruskal_steps, kruskal_weight,
        prim_algorithm, prim_mst, prim_steps, prim_weight
    )


@app.cell
def __(
    algorithm_choice,
    graph,
    kruskal_mst,
    kruskal_steps,
    kruskal_weight,
    mo,
    pos,
    prim_mst,
    prim_steps,
    prim_weight,
):
    # Display algorithm results
    results_display = []
    
    if algorithm_choice.value in ["Both", "Kruskal Only"]:
        results_display.append(
            mo.md(f"""
            ### Kruskal's Algorithm Results
            - **Total MST Weight**: {kruskal_weight}
            - **Approach**: Global edge sorting, cycle prevention
            - **Edges in MST**: {len(kruskal_mst)} edges connecting {len(graph.nodes())} nodes
            """)
        )
    
    if algorithm_choice.value in ["Both", "Prim Only"]:
        results_display.append(
            mo.md(f"""
            ### Prim's Algorithm Results  
            - **Total MST Weight**: {prim_weight}
            - **Approach**: Local growth from starting node
            - **Edges in MST**: {len(prim_mst)} edges connecting {len(graph.nodes())} nodes
            """)
        )
    
    if algorithm_choice.value == "Both":
        weight_match = "✅ Same" if kruskal_weight == prim_weight else "❌ Different"
        results_display.append(
            mo.md(f"""
            ### Comparison
            - **Total Weights Match**: {weight_match}
            - **Both algorithms find optimal MST**: When edge weights are unique, both algorithms produce identical results
            """)
        )
    
    mo.vstack(results_display)
    return results_display, weight_match


@app.cell
def __(
    FancyBboxPatch,
    algorithm_choice,
    graph,
    kruskal_mst,
    mo,
    nx,
    plt,
    pos,
    prim_mst,
):
    def visualize_algorithms():
        """Create visualization comparing both algorithms"""
        
        if algorithm_choice.value == "Both":
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            axes = [ax1, ax2]
            titles = ["Kruskal's Algorithm (Global Approach)", "Prim's Algorithm (Local Growth)"]
            msts = [kruskal_mst, prim_mst]
        else:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            axes = [ax]
            if algorithm_choice.value == "Kruskal Only":
                titles = ["Kruskal's Algorithm (Global Approach)"]
                msts = [kruskal_mst]
            else:
                titles = ["Prim's Algorithm (Local Growth)"] 
                msts = [prim_mst]
        
        for idx, (ax, title, mst) in enumerate(zip(axes, titles, msts)):
            ax.clear()
            
            # Draw all edges in light gray
            nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='lightgray', width=1, alpha=0.3)
            
            # Draw MST edges in red
            mst_edges = [(u, v) for u, v, w in mst]
            nx.draw_networkx_edges(graph, pos, edgelist=mst_edges, ax=ax, 
                                 edge_color='red', width=3, alpha=0.8)
            
            # Draw nodes
            nx.draw_networkx_nodes(graph, pos, ax=ax, node_color='lightblue', 
                                 node_size=1000, alpha=0.9)
            
            # Draw labels
            nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10, font_weight='bold')
            
            # Draw edge weights
            edge_labels = nx.get_edge_attributes(graph, 'weight')
            nx.draw_networkx_edge_labels(graph, pos, edge_labels, ax=ax, font_size=8)
            
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.axis('off')
            
            # Add algorithm description box
            if idx == 0 and algorithm_choice.value in ["Both", "Kruskal Only"]:
                description = "1. Sort all edges by weight\n2. Add cheapest edge if no cycle\n3. Repeat until tree complete"
            elif (idx == 1 and algorithm_choice.value == "Both") or (idx == 0 and algorithm_choice.value == "Prim Only"):
                description = "1. Start from any node\n2. Add cheapest edge to new node\n3. Grow tree incrementally"
            
            bbox = FancyBboxPatch((0.02, 0.02), 0.25, 0.15, 
                                boxstyle="round,pad=0.01", 
                                transform=ax.transAxes,
                                facecolor='wheat', alpha=0.8, edgecolor='black')
            ax.add_patch(bbox)
            ax.text(0.03, 0.03, description, transform=ax.transAxes, 
                   fontsize=9, verticalalignment='bottom')
        
        plt.tight_layout()
        return fig

    # Create and display the visualization
    fig = visualize_algorithms()
    fig
    return fig, visualize_algorithms


@app.cell
def __(
    algorithm_choice,
    kruskal_steps,
    mo,
    pd,
    prim_steps,
    show_step_by_step,
):
    # Show step-by-step construction if requested
    if show_step_by_step.value:
        step_displays = []
        
        if algorithm_choice.value in ["Both", "Kruskal Only"]:
            # Kruskal steps
            kruskal_df = pd.DataFrame([
                {
                    'Step': i+1,
                    'Edge': f"{step['edge'][0]}-{step['edge'][1]}" if 'edge' in step else "Start",
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
        
        if algorithm_choice.value in ["Both", "Prim Only"]:
            # Prim steps  
            prim_df = pd.DataFrame([
                {
                    'Step': i+1,
                    'Node/Edge': step.get('node', f"{step['edge'][0]}-{step['edge'][1]}") if 'node' in step else f"{step['edge'][0]}-{step['edge'][1]}",
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
    else:
        mo.md("*Enable 'Show Step-by-Step Construction' to see detailed algorithm execution.*")
    return kruskal_df, prim_df, step_displays


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Key Algorithmic Differences

        | Aspect | Kruskal's Algorithm | Prim's Algorithm |
        |--------|-------------------|------------------|
        | **Perspective** | Global - considers all edges | Local - grows from one point |
        | **Initial Step** | Sort ALL edges by weight | Choose starting node |
        | **Edge Selection** | Pick globally cheapest edge | Pick cheapest edge to unvisited node |
        | **Data Structure** | Union-Find (for cycle detection) | Priority queue + visited set |
        | **Growth Pattern** | May build multiple disconnected trees initially | Always maintains single connected tree |
        | **Cycle Prevention** | Explicit cycle checking with Union-Find | Implicit - only connects to unvisited nodes |
        | **Implementation** | More complex (Union-Find structure) | More intuitive (local expansion) |
        | **Parallelization** | Better suited for parallel processing | Sequential by nature |

        ## When to Use Which Algorithm?

        - **Kruskal's Algorithm**: 
          - When you can sort edges efficiently
          - For sparse graphs (few edges)
          - When parallel processing is possible
          - When dealing with disconnected components

        - **Prim's Algorithm**:
          - When you have a natural starting point
          - For dense graphs (many edges) 
          - When step-by-step visualization is important
          - When memory usage needs to be minimized

        ## Mathematical Guarantee

        Both algorithms are **guaranteed to produce the same result** when all edge weights are unique. This demonstrates the mathematical principle that the minimum spanning tree is unique under these conditions, regardless of the construction method used.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Try Different Graphs!

        Use the dropdown above to explore different graph types:

        - **Simple 5-node**: Perfect for understanding the basic concepts
        - **Grid 3x3**: See how algorithms handle regular structures  
        - **Random 8-node**: Test performance on irregular networks
        - **Power Grid Example**: Real-world inspired infrastructure network

        Each graph type reveals different aspects of how these algorithms work and why both approaches lead to the same optimal solution.
        """
    )
    return


if __name__ == "__main__":
    app.run()
