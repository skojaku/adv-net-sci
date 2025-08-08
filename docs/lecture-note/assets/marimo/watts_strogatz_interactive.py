"""
Interactive Watts-Strogatz Small-World Network Explorer

This Marimo notebook provides an interactive exploration of the Watts-Strogatz model,
allowing users to adjust the rewiring probability and observe how network properties change.

Author: Network Science Course
"""

import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Interactive Watts-Strogatz Small-World Network Explorer

    This notebook demonstrates the Watts-Strogatz model, which shows how small-world networks 
    can emerge from the interpolation between regular lattices and random graphs.

    ## Key Concepts:
    - **Regular Lattice** (p=0): High clustering, long paths
    - **Random Graph** (p=1): Low clustering, short paths  
    - **Small-World** (0 < p < 1): High clustering AND short paths
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Rewiring probability slider
    p_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.01,
        value=0.1,
        show_value=True,
        label="Rewiring Probability (p)",
        full_width=True,
    )

    # Network size slider
    N_slider = mo.ui.slider(
        start=10,
        stop=50,
        step=5,
        value=20,
        show_value=True,
        label="Number of Nodes (N)",
        full_width=True,
    )

    # Degree slider
    k_slider = mo.ui.slider(
        start=2,
        stop=8,
        step=2,
        value=4,
        show_value=True,
        label="Node Degree (k)",
        full_width=True,
    )

    # Display controls in a nice layout
    mo.vstack(
        [
            mo.md(
                "**Adjust the parameters to explore different network configurations:**"
            ),
            p_slider,
            N_slider,
            k_slider,
        ]
    )
    return N_slider, k_slider, p_slider


@app.cell(hide_code=True)
def _(mo):
    mo.md("""## Network Visualization""")
    return


@app.cell(hide_code=True)
def _(
    G_random,
    G_ws,
    N_slider,
    alt,
    k_slider,
    mo,
    np,
    nx,
    p_slider,
    pd,
):
    def create_network_data(G, network_type, N, k, p_value):
        """Create network data for Altair visualization"""
        # Create circular layout
        pos = {}
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
        for i, node in enumerate(G.nodes()):
            pos[node] = (np.cos(angles[i]), np.sin(angles[i]))
        
        # Create nodes dataframe
        nodes_data = []
        for node in G.nodes():
            x, y = pos[node]
            nodes_data.append({
                'node': node,
                'x': x,
                'y': y,
                'network_type': network_type
            })
        
        # Create edges dataframe
        edges_data = []
        for edge in G.edges():
            i, j = edge
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            
            # Determine edge type for WS network
            edge_type = "Regular"
            if network_type == "Watts-Strogatz":
                ring_distance = min(abs(i - j), N - abs(i - j))
                if ring_distance > k // 2:
                    edge_type = "Rewired"
            
            edges_data.append({
                'source': i,
                'target': j,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'edge_type': edge_type,
                'network_type': network_type
            })
        
        return pd.DataFrame(nodes_data), pd.DataFrame(edges_data)
    
    # Create network data
    N = N_slider.value
    k = k_slider.value
    p_val = p_slider.value
    
    nodes_ws, edges_ws = create_network_data(G_ws, "Watts-Strogatz", N, k, p_val)
    nodes_rand, edges_rand = create_network_data(G_random, "Random", N, k, p_val)
    
    # Combine data
    all_nodes = pd.concat([nodes_ws, nodes_rand], ignore_index=True)
    all_edges = pd.concat([edges_ws, edges_rand], ignore_index=True)
    
    return all_edges, all_nodes


@app.cell(hide_code=True)
def _(all_edges, all_nodes, alt, mo, N_slider, k_slider, p_slider):
    # Create network visualization with Altair
    def create_network_chart():
        # Base chart for edges
        edge_base = alt.Chart(all_edges).add_selection(
            alt.selection_single()
        )
        
        # WS network edges
        ws_edges = edge_base.transform_filter(
            alt.datum.network_type == 'Watts-Strogatz'
        ).mark_rule(
            strokeWidth=1.5,
            opacity=0.7
        ).encode(
            x=alt.X('x1:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            y=alt.Y('y1:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            x2='x2:Q',
            y2='y2:Q',
            color=alt.Color(
                'edge_type:N',
                scale=alt.Scale(
                    domain=['Regular', 'Rewired'], 
                    range=['steelblue', 'red']
                ),
                legend=alt.Legend(title="Edge Type", orient="top-right")
            ),
            tooltip=['source:O', 'target:O', 'edge_type:N']
        ).properties(
            width=250,
            height=250,
            title=f"Watts-Strogatz Network (N={N_slider.value}, k={k_slider.value}, p={p_slider.value:.3f})"
        )
        
        # WS network nodes
        ws_nodes = alt.Chart(all_nodes).transform_filter(
            alt.datum.network_type == 'Watts-Strogatz'
        ).mark_circle(
            size=100,
            stroke='black',
            strokeWidth=1
        ).encode(
            x=alt.X('x:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            fill=alt.value('lightblue'),
            tooltip=['node:O']
        )
        
        # Random network edges
        rand_edges = edge_base.transform_filter(
            alt.datum.network_type == 'Random'
        ).mark_rule(
            strokeWidth=1,
            opacity=0.5,
            color='gray'
        ).encode(
            x=alt.X('x1:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            y=alt.Y('y1:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            x2='x2:Q',
            y2='y2:Q',
            tooltip=['source:O', 'target:O']
        ).properties(
            width=250,
            height=250,
            title="Random Network (same N, similar density)"
        )
        
        # Random network nodes
        rand_nodes = alt.Chart(all_nodes).transform_filter(
            alt.datum.network_type == 'Random'
        ).mark_circle(
            size=100,
            stroke='black',
            strokeWidth=1
        ).encode(
            x=alt.X('x:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
            fill=alt.value('lightcoral'),
            tooltip=['node:O']
        )
        
        # Combine networks
        ws_network = (ws_edges + ws_nodes)
        rand_network = (rand_edges + rand_nodes)
        
        return alt.hconcat(ws_network, rand_network).resolve_scale(
            color='independent'
        )
    
    # Display networks
    network_chart = create_network_chart()
    mo.ui.altair_chart(network_chart)
    return (network_chart,)


@app.cell(hide_code=True) 
def _(alt, clustering_ws, mo, p_slider, p_values, path_length_ws, pd, sigma_values):
    # Create line plots with Altair
    def create_line_plots():
        # Prepare data for line plots
        C_initial = clustering_ws[0] if clustering_ws[0] > 0 else 1
        L_initial = path_length_ws[0] if path_length_ws[0] > 0 else 1
        
        # Create dataframe for properties vs p
        props_data = []
        for i, p in enumerate(p_values):
            props_data.extend([
                {
                    'p': p,
                    'value': clustering_ws[i] / C_initial,
                    'metric': 'C(p) / C(0)',
                    'type': 'Clustering'
                },
                {
                    'p': p,
                    'value': path_length_ws[i] / L_initial,
                    'metric': 'L(p) / L(0)',
                    'type': 'Path Length'
                }
            ])
        
        props_df = pd.DataFrame(props_data)
        
        # Create dataframe for sigma vs p
        sigma_data = []
        for i, p in enumerate(p_values):
            sigma_data.append({
                'p': p,
                'sigma': sigma_values[i]
            })
        
        sigma_df = pd.DataFrame(sigma_data)
        
        # Properties plot
        properties_plot = alt.Chart(props_df).mark_line(
            point=True,
            strokeWidth=2.5
        ).encode(
            x=alt.X('p:Q', title='Rewiring Probability (p)', scale=alt.Scale(domain=[0, 1])),
            y=alt.Y('value:Q', title='Normalized Values'),
            color=alt.Color(
                'metric:N',
                scale=alt.Scale(
                    domain=['C(p) / C(0)', 'L(p) / L(0)'],
                    range=['steelblue', 'red']
                ),
                legend=alt.Legend(title="Metric")
            ),
            tooltip=['p:Q', 'value:Q', 'metric:N']
        ).properties(
            width=350,
            height=200,
            title="Network Properties vs Rewiring Probability"
        )
        
        # Add current p line to properties plot
        current_p_line = alt.Chart(pd.DataFrame({'p': [p_slider.value]})).mark_rule(
            color='gray',
            strokeDash=[5, 5],
            strokeWidth=2
        ).encode(
            x='p:Q',
            tooltip=alt.value(f'Current p = {p_slider.value:.3f}')
        )
        
        properties_with_line = properties_plot + current_p_line
        
        # Sigma plot
        sigma_plot = alt.Chart(sigma_df).mark_line(
            point=alt.OverlayMarkDef(shape='diamond', size=60),
            color='green',
            strokeWidth=2.5
        ).encode(
            x=alt.X('p:Q', title='Rewiring Probability (p)', scale=alt.Scale(domain=[0, 1])),
            y=alt.Y('sigma:Q', title='Small-World Coefficient (σ)'),
            tooltip=['p:Q', 'sigma:Q']
        ).properties(
            width=350,
            height=200,
            title="Small-World Property vs Rewiring Probability"
        )
        
        # Add sigma = 1 baseline
        baseline = alt.Chart(pd.DataFrame({'y': [1]})).mark_rule(
            color='red',
            strokeDash=[3, 3]
        ).encode(
            y='y:Q',
            tooltip=alt.value('σ = 1 (Random baseline)')
        )
        
        # Add current p line to sigma plot
        sigma_p_line = alt.Chart(pd.DataFrame({'p': [p_slider.value]})).mark_rule(
            color='gray',
            strokeDash=[5, 5],
            strokeWidth=2
        ).encode(
            x='p:Q',
            tooltip=alt.value(f'Current p = {p_slider.value:.3f}')
        )
        
        # Highlight max sigma
        max_sigma_idx = sigma_values.index(max(sigma_values))
        max_point = alt.Chart(pd.DataFrame([{
            'p': p_values[max_sigma_idx], 
            'sigma': sigma_values[max_sigma_idx]
        }])).mark_circle(
            size=150,
            color='gold',
            stroke='black',
            strokeWidth=2
        ).encode(
            x='p:Q',
            y='sigma:Q',
            tooltip=alt.value(f'Max σ = {sigma_values[max_sigma_idx]:.2f} at p = {p_values[max_sigma_idx]:.2f}')
        )
        
        sigma_with_annotations = sigma_plot + baseline + sigma_p_line + max_point
        
        return alt.vconcat(
            properties_with_line,
            sigma_with_annotations
        ).resolve_scale(color='independent')
    
    # Display line plots
    line_plots = create_line_plots()
    mo.ui.altair_chart(line_plots)
    return (line_plots,)


@app.cell(hide_code=True)
def _(mo, p_slider):
    mo.md(
        f"""
    ## Understanding the Small-World Effect

    **Current rewiring probability: {p_slider.value:.3f}**

    The Watts-Strogatz model demonstrates how a small amount of randomness can dramatically change network properties:

    - **p = 0**: Regular ring lattice - high clustering, long paths
    - **p = 0.01-0.1**: Small-world regime - high clustering AND short paths  
    - **p = 1**: Random graph - low clustering, short paths

    ### Key Insights:
    1. **Small p values** (0.01-0.1) create the most interesting small-world behavior
    2. **Clustering drops slowly** while **path length drops rapidly** as p increases
    3. **σ > 1** indicates true small-world behavior (high C relative to random, low L relative to regular)

    ### Try This:
    - Start with p = 0 and slowly increase to see the transition
    - Notice how just a few rewired edges (red) dramatically reduce path lengths
    - Observe that clustering remains high even with moderate rewiring
    - Watch the line plots below to see how the current p value compares to the full transition

    ### Understanding the Line Plots:

    **Left Plot - Normalized Properties:**
    - **Blue line (C(p)/C(0))**: Shows how clustering decreases as p increases (normalized by initial value)
    - **Red line (L(p)/L(0))**: Shows how path length decreases rapidly even for small p (normalized by initial value)
    - The **small-world regime** occurs where clustering remains high but path length drops dramatically

    **Right Plot - Small-World Coefficient:**
    - **Green line**: Shows σ(p) across all rewiring probabilities
    - **Gold dot**: Highlights the maximum small-world effect (optimal p value)
    - **Gray vertical line**: Your current p setting
    - Values **σ > 1** indicate true small-world behavior
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ## Mathematical Background

    The **small-world coefficient** σ quantifies the small-world property:

    $$σ = \\frac{C/C_{\\text{random}}}{L/L_{\\text{random}}} = \\frac{C \\cdot L_{\\text{random}}}{L \\cdot C_{\\text{random}}}$$

    Where:
    - C = clustering coefficient of the network
    - L = average path length of the network
    - C_random, L_random = metrics for equivalent random graph

    **Interpretation:**
    - σ >> 1: Strong small-world property
    - σ ≈ 1: Similar to random networks  
    - σ < 1: Regular/lattice-like behavior

    This normalization ensures we're comparing against meaningful baselines rather than absolute values.
    """
    )
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import networkx as nx
    import numpy as np
    import pandas as pd
    import altair as alt
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.collections import LineCollection
    import warnings

    warnings.filterwarnings("ignore")
    alt.data_transformers.enable('json')
    return alt, mo, np, nx, patches, pd, plt


@app.cell(hide_code=True)
def _(N_slider, k_slider, nx, p_slider):
    def generate_networks(N, k, p, seed=42):
        """Generate Watts-Strogatz network and equivalent random graph"""
        # Generate Watts-Strogatz network
        G_ws = nx.watts_strogatz_graph(N, k, p, seed=seed)

        # Generate random network with same number of edges
        num_edges = G_ws.number_of_edges()
        prob_random = num_edges / (
            N * (N - 1) / 2
        )  # Probability for same edge density
        G_random = nx.erdos_renyi_graph(N, prob_random, seed=seed)

        return G_ws, G_random


    def compute_metrics(G):
        """Compute clustering coefficient and average path length"""
        try:
            C = nx.average_clustering(G)
            if nx.is_connected(G):
                L = nx.average_shortest_path_length(G)
            else:
                # For disconnected graphs, use the largest component
                largest_cc = max(nx.connected_components(G), key=len)
                G_sub = G.subgraph(largest_cc)
                L = nx.average_shortest_path_length(G_sub)
        except:
            C = 0
            L = float("inf")
        return C, L


    def compute_small_world_coefficient(C, L, C_random, L_random):
        """Compute the Watts-Strogatz small-world coefficient σ"""
        if C_random > 0 and L_random > 0 and L != float("inf"):
            sigma = (C / C_random) / (L / L_random)
        else:
            sigma = 0
        return sigma


    # Generate networks with current parameters
    G_ws, G_random = generate_networks(
        N_slider.value, k_slider.value, p_slider.value
    )
    return G_random, G_ws, compute_metrics, compute_small_world_coefficient


@app.cell(hide_code=True)
def _(G_random, G_ws, compute_metrics, compute_small_world_coefficient):
    # Compute metrics for both networks
    C_ws, L_ws = compute_metrics(G_ws)
    C_random, L_random = compute_metrics(G_random)
    sigma = compute_small_world_coefficient(C_ws, L_ws, C_random, L_random)

    # Store metrics for display
    metrics = {
        "C_ws": C_ws,
        "L_ws": L_ws,
        "C_random": C_random,
        "L_random": L_random,
        "sigma": sigma,
    }
    return (metrics,)


@app.cell(hide_code=True)
def _(N_slider, k_slider, np, nx):
    def compute_metrics_for_p_range(N, k, p_values, seed=42):
        """Compute metrics for different values of p to show the transition"""
        clustering_ws = []
        path_length_ws = []
        sigma_values = []
        clustering_random = []
        path_length_random = []

        for p in p_values:
            # Generate Watts-Strogatz network
            G_ws = nx.watts_strogatz_graph(N, k, p, seed=seed)

            # Generate equivalent random network
            num_edges = G_ws.number_of_edges()
            prob_random = num_edges / (N * (N - 1) / 2)
            G_random = nx.erdos_renyi_graph(N, prob_random, seed=seed)

            # Compute clustering
            C_ws = nx.average_clustering(G_ws)
            C_random = nx.average_clustering(G_random)

            # Compute path length
            if nx.is_connected(G_ws):
                L_ws = nx.average_shortest_path_length(G_ws)
            else:
                largest_cc = max(nx.connected_components(G_ws), key=len)
                G_sub = G_ws.subgraph(largest_cc)
                L_ws = nx.average_shortest_path_length(G_sub)

            if nx.is_connected(G_random):
                L_random = nx.average_shortest_path_length(G_random)
            else:
                largest_cc = max(nx.connected_components(G_random), key=len)
                G_sub = G_random.subgraph(largest_cc)
                L_random = nx.average_shortest_path_length(G_sub)

            # Compute small-world coefficient
            if C_random > 0 and L_random > 0:
                sigma = (C_ws / C_random) / (L_ws / L_random)
            else:
                sigma = 0

            clustering_ws.append(C_ws)
            path_length_ws.append(L_ws)
            clustering_random.append(C_random)
            path_length_random.append(L_random)
            sigma_values.append(sigma)

        return (
            clustering_ws,
            path_length_ws,
            clustering_random,
            path_length_random,
            sigma_values,
        )


    # Compute metrics across p values
    p_values = np.linspace(0, 1, 21)  # 21 points from 0 to 1
    (
        clustering_ws,
        path_length_ws,
        clustering_random,
        path_length_random,
        sigma_values,
    ) = compute_metrics_for_p_range(N_slider.value, k_slider.value, p_values)
    return clustering_ws, p_values, path_length_ws, sigma_values


@app.cell(hide_code=True)
def _(metrics, mo):
    # Display current metrics
    mo.md(f"""
    ## Current Network Metrics

    | Metric | Watts-Strogatz | Random | Ratio |
    |--------|----------------|---------|-------|
    | **Clustering (C)** | {metrics["C_ws"]:.4f} | {metrics["C_random"]:.4f} | {metrics["C_ws"] / max(metrics["C_random"], 0.001):.2f} |
    | **Path Length (L)** | {metrics["L_ws"]:.4f} | {metrics["L_random"]:.4f} | {metrics["L_ws"] / max(metrics["L_random"], 0.001):.2f} |
    | **Small-world σ** | {metrics["sigma"]:.4f} | - | {"Strong" if metrics["sigma"] > 1 else "Weak"} |
    """)
    return


if __name__ == "__main__":
    app.run()
