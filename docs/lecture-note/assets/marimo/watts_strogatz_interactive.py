"""
Interactive Watts-Strogatz Small-World Network Explorer

This Marimo notebook provides an interactive exploration of the Watts-Strogatz model,
with progressive edge rewiring to demonstrate how network properties change.

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

    This notebook demonstrates the Watts-Strogatz model through progressive edge rewiring.
    Starting from a regular ring lattice (p=0), edges are rewired one by one as you increase p.

    ## Key Concepts:
    - **Regular Lattice** (p=0): High clustering, long paths
    - **Progressive Rewiring** (0 < p < 1): Gradual transition to small-world
    - **Random Graph** (p=1): Low clustering, short paths
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Network parameters
    N_slider = mo.ui.slider(
        start=10,
        stop=30,
        step=2,
        value=20,
        show_value=True,
        label="Number of Nodes (N)",
        full_width=True,
    )

    k_slider = mo.ui.slider(
        start=2,
        stop=6,
        step=2,
        value=4,
        show_value=True,
        label="Node Degree (k)",
        full_width=True,
    )

    # Rewiring control - now represents fraction of edges rewired
    p_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.05,
        value=0.1,
        show_value=True,
        label="Fraction of Edges Rewired (p)",
        full_width=True,
    )

    # Display controls
    mo.vstack(
        [
            mo.md("**Adjust the parameters to explore progressive rewiring:**"),
            N_slider,
            k_slider,
            p_slider,
        ]
    )
    return N_slider, k_slider, p_slider


@app.cell(hide_code=True)
def _(mo):
    mo.md("""## Progressive Rewiring Visualization""")
    return


@app.cell
def _(CL_chart, mo, network_chart, sigma_chart):
    mo.hstack([network_chart, mo.vstack([CL_chart, sigma_chart])])
    return


@app.cell(hide_code=True)
def _(N_slider, k_slider, nx, p_slider):
    def create_progressive_ws_network(N, k, p, seed=42):
        """Create Watts-Strogatz network with progressive rewiring"""
        # Start with regular ring lattice
        G = nx.watts_strogatz_graph(N, k, 0, seed=seed)
        
        # Get all edges in the original lattice
        original_edges = list(G.edges())
        
        # Calculate how many edges to rewire based on p
        num_to_rewire = int(p * len(original_edges))
        
        if num_to_rewire == 0:
            return G
            
        # Create a copy to modify
        G_rewired = G.copy()
        
        # Rewire edges progressively
        np.random.seed(seed)
        edges_to_rewire = np.random.choice(len(original_edges), size=num_to_rewire, replace=False)
        
        for edge_idx in edges_to_rewire:
            u, v = original_edges[edge_idx]
            
            # Remove the original edge
            if G_rewired.has_edge(u, v):
                G_rewired.remove_edge(u, v)
                
                # Find a new target that doesn't create self-loop or duplicate edge
                possible_targets = [node for node in G_rewired.nodes() 
                                  if node != u and not G_rewired.has_edge(u, node)]
                
                if possible_targets:
                    new_target = np.random.choice(possible_targets)
                    G_rewired.add_edge(u, new_target)
                else:
                    # If no valid target, keep the original edge
                    G_rewired.add_edge(u, v)
        
        return G_rewired

    # Generate the network with current parameters
    G_ws = create_progressive_ws_network(
        N_slider.value, k_slider.value, p_slider.value
    )
    
    return G_ws,


@app.cell(hide_code=True)
def _(G_ws, N_slider, k_slider, np, p_slider, pd):
    def create_network_data(G, N, k, p_value):
        """Create network data for Altair visualization"""
        # Create circular layout
        pos = {}
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
        for idx, node in enumerate(G.nodes()):
            pos[node] = (np.cos(angles[idx]), np.sin(angles[idx]))

        # Create nodes dataframe
        nodes_data = []
        for node in G.nodes():
            x, y = pos[node]
            nodes_data.append({"node": node, "x": x, "y": y})

        # Create edges dataframe
        edges_data = []
        for edge in G.edges():
            node_i, node_j = edge
            x1, y1 = pos[node_i]
            x2, y2 = pos[node_j]

            # Determine if edge is original (regular) or rewired
            # Original edges are between neighbors in ring lattice
            ring_distance = min(abs(node_i - node_j), N - abs(node_i - node_j))
            edge_type = "Regular" if ring_distance <= k // 2 else "Rewired"

            edges_data.append(
                {
                    "source": node_i,
                    "target": node_j,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "edge_type": edge_type,
                }
            )

        return pd.DataFrame(nodes_data), pd.DataFrame(edges_data)

    # Create network data
    N = N_slider.value
    k = k_slider.value
    p_val = p_slider.value

    all_nodes, all_edges = create_network_data(G_ws, N, k, p_val)
    return all_edges, all_nodes


@app.cell(hide_code=True)
def _(N_slider, all_edges, all_nodes, alt, k_slider, mo, p_slider):
    # Create network visualization with Altair
    def create_network_chart():
        # Edges
        edges_chart = (
            alt.Chart(all_edges)
            .mark_rule(strokeWidth=1.5, opacity=0.7)
            .encode(
                x=alt.X("x1:Q", scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
                y=alt.Y("y1:Q", scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
                x2="x2:Q",
                y2="y2:Q",
                color=alt.Color(
                    "edge_type:N",
                    scale=alt.Scale(
                        domain=["Regular", "Rewired"], range=["steelblue", "red"]
                    ),
                    legend=alt.Legend(title="Edge Type", orient="top-right"),
                ),
                tooltip=["source:O", "target:O", "edge_type:N"],
            )
        )

        # Nodes
        nodes_chart = (
            alt.Chart(all_nodes)
            .mark_circle(size=100, stroke="black", strokeWidth=1)
            .encode(
                x=alt.X("x:Q", scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
                y=alt.Y("y:Q", scale=alt.Scale(domain=[-1.2, 1.2]), axis=None),
                fill=alt.value("lightblue"),
                tooltip=["node:O"],
            )
        )

        # Combine
        network = (edges_chart + nodes_chart).properties(
            width=400,
            height=400,
            title=f"Watts-Strogatz Network (N={N_slider.value}, k={k_slider.value}, p={p_slider.value:.2f})",
        )

        return network

    network_chart = create_network_chart()
    network_chart = mo.ui.altair_chart(network_chart)
    return (network_chart,)


@app.cell(hide_code=True)
def _(G_ws, N_slider, k_slider, np, nx):
    def compute_network_metrics(G, N, k):
        """Compute clustering, path length, and small-world coefficient"""
        # Compute actual network metrics
        C = nx.average_clustering(G)
        
        if nx.is_connected(G):
            L = nx.average_shortest_path_length(G)
        else:
            # Use largest connected component
            largest_cc = max(nx.connected_components(G), key=len)
            G_sub = G.subgraph(largest_cc)
            L = nx.average_shortest_path_length(G_sub)
        
        # Analytical reference values for random network
        C_random = k / (N - 1)  # Average clustering for random graph
        L_random = np.log(N) / np.log(k)  # Average path length for random graph
        
        # Small-world coefficient
        if C_random > 0 and L_random > 0:
            sigma = (C / C_random) / (L / L_random)
        else:
            sigma = 0
            
        return C, L, C_random, L_random, sigma

    # Compute metrics for current network
    C, L, C_random, L_random, sigma = compute_network_metrics(
        G_ws, N_slider.value, k_slider.value
    )
    
    return C, L, C_random, L_random, sigma


@app.cell(hide_code=True)
def _(C, C_random, L, L_random, N_slider, k_slider, np, nx, p_slider, sigma):
    def compute_progressive_metrics(N, k, num_steps=21, seed=42):
        """Compute metrics for progressive rewiring from p=0 to current p"""
        p_values = np.linspace(0, p_slider.value, num_steps)
        metrics_data = []
        
        for p_val in p_values:
            # Create network at this rewiring level
            G = nx.watts_strogatz_graph(N, k, 0, seed=seed)  # Start with ring
            
            if p_val > 0:
                # Progressive rewiring
                original_edges = list(G.edges())
                num_to_rewire = int(p_val * len(original_edges))
                
                if num_to_rewire > 0:
                    np.random.seed(seed)
                    edges_to_rewire = np.random.choice(len(original_edges), 
                                                     size=num_to_rewire, replace=False)
                    
                    for edge_idx in edges_to_rewire:
                        u, v = original_edges[edge_idx]
                        
                        if G.has_edge(u, v):
                            G.remove_edge(u, v)
                            
                            possible_targets = [node for node in G.nodes() 
                                              if node != u and not G.has_edge(u, node)]
                            
                            if possible_targets:
                                new_target = np.random.choice(possible_targets)
                                G.add_edge(u, new_target)
                            else:
                                G.add_edge(u, v)  # Keep original if no valid target
            
            # Compute metrics
            C_temp = nx.average_clustering(G)
            
            if nx.is_connected(G):
                L_temp = nx.average_shortest_path_length(G)
            else:
                largest_cc = max(nx.connected_components(G), key=len)
                G_sub = G.subgraph(largest_cc)
                L_temp = nx.average_shortest_path_length(G_sub)
            
            # Analytical reference values
            C_random_temp = k / (N - 1)
            L_random_temp = np.log(N) / np.log(k)
            
            # Small-world coefficient
            if C_random_temp > 0 and L_random_temp > 0:
                sigma_temp = (C_temp / C_random_temp) / (L_temp / L_random_temp)
            else:
                sigma_temp = 0
            
            metrics_data.append({
                'p': p_val,
                'C': C_temp,
                'L': L_temp,
                'C_normalized': C_temp / (k / (N - 1)),  # Normalized by initial clustering
                'L_normalized': L_temp / (np.log(N) / np.log(k)),  # Normalized by random path length
                'sigma': sigma_temp
            })
        
        return metrics_data

    # Compute progressive metrics
    progressive_data = compute_progressive_metrics(N_slider.value, k_slider.value)
    
    return (progressive_data,)


@app.cell(hide_code=True)
def _(alt, k_slider, mo, N_slider, pd, progressive_data, p_slider):
    # Create properties plot
    def create_properties_chart():
        # Prepare data for line plots
        props_data = []
        for data_point in progressive_data:
            props_data.extend([
                {
                    'p': data_point['p'],
                    'value': data_point['C_normalized'],
                    'metric': 'C(p) / C(random)'
                },
                {
                    'p': data_point['p'],
                    'value': data_point['L_normalized'],
                    'metric': 'L(p) / L(random)'
                }
            ])
        
        props_df = pd.DataFrame(props_data)
        
        # Properties chart
        properties_chart = (
            alt.Chart(props_df)
            .mark_line(point=True, strokeWidth=2.5)
            .encode(
                x=alt.X("p:Q", title="Fraction of Edges Rewired (p)", 
                       scale=alt.Scale(domain=[0, 1])),
                y=alt.Y("value:Q", title="Normalized Values"),
                color=alt.Color(
                    "metric:N",
                    scale=alt.Scale(
                        domain=["C(p) / C(random)", "L(p) / L(random)"],
                        range=["steelblue", "red"],
                    ),
                    legend=alt.Legend(title="Metric"),
                ),
                tooltip=["p:Q", "value:Q", "metric:N"],
            )
            .properties(
                width=350,
                height=200,
                title="Network Properties vs Edge Rewiring",
            )
        )

        # Add vertical line at current p
        current_p_line = (
            alt.Chart(pd.DataFrame({"p": [p_slider.value]}))
            .mark_rule(color="gray", strokeDash=[5, 5], strokeWidth=2)
            .encode(x="p:Q")
        )

        return properties_chart + current_p_line

    CL_chart = mo.ui.altair_chart(create_properties_chart())
    return (CL_chart,)


@app.cell(hide_code=True)
def _(alt, mo, pd, progressive_data, p_slider):
    # Create small-world coefficient plot
    def create_sigma_chart():
        sigma_data = [{'p': d['p'], 'sigma': d['sigma']} for d in progressive_data]
        sigma_df = pd.DataFrame(sigma_data)
        
        sigma_chart = (
            alt.Chart(sigma_df)
            .mark_line(point=True, color="green", strokeWidth=2.5)
            .encode(
                x=alt.X("p:Q", title="Fraction of Edges Rewired (p)", 
                       scale=alt.Scale(domain=[0, 1])),
                y=alt.Y("sigma:Q", title="Small-World Coefficient (σ)"),
                tooltip=["p:Q", "sigma:Q"],
            )
            .properties(
                width=350,
                height=200,
                title="Small-World Coefficient vs Edge Rewiring",
            )
        )

        # Add vertical line at current p
        current_p_line = (
            alt.Chart(pd.DataFrame({"p": [p_slider.value]}))
            .mark_rule(color="gray", strokeDash=[5, 5], strokeWidth=2)
            .encode(x="p:Q")
        )

        return sigma_chart + current_p_line

    sigma_chart = mo.ui.altair_chart(create_sigma_chart())
    return (sigma_chart,)


@app.cell(hide_code=True)
def _(C, C_random, L, L_random, mo, p_slider, sigma):
    mo.md(
        f"""
    ## Understanding the Small-World Effect

    **Current rewiring level: {p_slider.value:.2f}** ({int(p_slider.value * 100):.0f}% of edges rewired)

    ### Current Network Metrics:
    | Metric | Value | Random Reference | Ratio |
    |--------|-------|------------------|-------|
    | **Clustering (C)** | {C:.4f} | {C_random:.4f} | {C/max(C_random, 0.001):.2f} |
    | **Path Length (L)** | {L:.4f} | {L_random:.4f} | {L/max(L_random, 0.001):.2f} |
    | **Small-world σ** | {sigma:.4f} | - | {"Strong" if sigma > 1 else "Weak"} |

    ### Key Insights:
    1. **Progressive rewiring** shows how small-world properties emerge gradually
    2. **Analytical references** use exact formulas: C_random = k/(n-1), L_random = ln(n)/ln(k)
    3. **Small-world regime** occurs when σ > 1 (high clustering + short paths)
    4. **Just a few rewired edges** (red) can dramatically reduce path lengths

    ### Understanding the Transition:
    - **p = 0**: Regular ring lattice with high clustering but long paths
    - **Small p** (0.01-0.2): Sweet spot where clustering stays high but paths shorten
    - **Large p** (0.5-1.0): Approaches random graph with short paths but low clustering
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

    **Analytical Reference Values:**
    - $C_{\\text{random}} = \\frac{k}{n-1}$ (exact for Erdős-Rényi graphs)
    - $L_{\\text{random}} = \\frac{\\ln n}{\\ln k}$ (approximation for connected random graphs)

    **Interpretation:**
    - σ >> 1: Strong small-world property
    - σ ≈ 1: Similar to random networks  
    - σ < 1: Regular/lattice-like behavior

    This progressive approach shows how small-world properties emerge naturally from the balance between local organization and random connections.
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
    import warnings

    warnings.filterwarnings("ignore")
    alt.data_transformers.enable("csv")
    return alt, mo, np, nx, pd


if __name__ == "__main__":
    app.run()