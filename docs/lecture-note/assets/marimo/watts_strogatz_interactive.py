"""
Interactive Watts-Strogatz Small-World Network Explorer

This Marimo notebook provides an interactive exploration of the Watts-Strogatz model,
with precomputed network states for instant visualization.

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

    This notebook demonstrates the Watts-Strogatz model with precomputed network states.
    All possible networks from p=0 to p=1 are computed once, then instantly displayed.

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
        start=30,
        stop=1000,
        step=2,
        value=50,
        show_value=True,
        label="Number of Nodes (N)",
        full_width=True,
    )

    k_slider = mo.ui.slider(
        start=2,
        stop=20,
        step=1,
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
            mo.md("**Adjust the parameters to explore precomputed networks:**"),
            N_slider,
            k_slider,
            p_slider,
        ]
    )
    return N_slider, k_slider, p_slider


@app.cell(hide_code=True)
def _(mo):
    mo.md("""## Network Visualization (Precomputed States)""")
    return


@app.cell
def _(C_chart, L_chart, mo, network_chart, sigma_chart, sigma_naive_chart):
    mo.hstack(
        [
            network_chart,
            mo.vstack(
                [
                    mo.hstack([C_chart, L_chart]),
                    mo.hstack([sigma_chart, sigma_naive_chart]),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(N_slider, k_slider, np, nx):
    def precompute_all_network_states(N, k, num_steps=21, seed=42):
        """Precompute all network states and metrics for all p values from 0 to 1"""
        # Start with ring lattice (p=0)
        np.random.seed(seed)
        G = nx.watts_strogatz_graph(N, k, 0, seed=seed)
        original_edges = list(G.edges())
        total_edges = len(original_edges)

        # Create all p values from 0 to 1
        p_values = np.linspace(0, 1, num_steps)

        # Store all network states and metrics
        network_states = {}
        all_metrics = []

        # Pre-determine complete rewiring order
        edges_to_rewire_order = np.random.choice(
            total_edges, size=total_edges, replace=False
        )
        edges_rewired_so_far = 0

        for p_val in p_values:
            target_rewires = int(p_val * total_edges)

            # Rewire additional edges to reach target_rewires
            while edges_rewired_so_far < target_rewires:
                edge_idx = edges_to_rewire_order[edges_rewired_so_far]
                u, v = original_edges[edge_idx]

                if G.has_edge(u, v):  # Only rewire if edge still exists
                    G.remove_edge(u, v)

                    # Find valid rewiring target
                    possible_targets = [
                        node
                        for node in G.nodes()
                        if node != u and not G.has_edge(u, node)
                    ]

                    if possible_targets:
                        new_target = np.random.choice(possible_targets)
                        G.add_edge(u, new_target)
                    else:
                        # If no valid target, restore original edge
                        G.add_edge(u, v)

                edges_rewired_so_far += 1

            # Store network state (deep copy to preserve each state)
            network_states[p_val] = G.copy()

            # Compute network metrics
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

            # Unnormalized small-world index (naive approach)
            unnormalized_sigma = C_temp / L_temp if L_temp > 0 else 0

            all_metrics.append(
                {
                    "p": p_val,
                    "edges_rewired": edges_rewired_so_far,
                    "C": C_temp,
                    "L": L_temp,
                    "C_normalized": C_temp / C_random_temp,
                    "L_normalized": L_temp / L_random_temp,
                    "sigma": sigma_temp,
                    "sigma_unnormalized": unnormalized_sigma,
                }
            )

        return network_states, all_metrics, p_values


    # Precompute all network states
    network_states, all_metrics, all_p_values = precompute_all_network_states(
        N_slider.value, k_slider.value
    )
    return all_metrics, all_p_values, network_states


@app.cell(hide_code=True)
def _(all_p_values, network_states, p_slider):
    def find_closest_p(target_p, p_values_list):
        """Find the closest precomputed p value to the target"""
        return min(p_values_list, key=lambda x: abs(x - target_p))


    # Get the network state closest to current p slider value
    closest_p = find_closest_p(p_slider.value, all_p_values)
    current_network = network_states[closest_p]
    return closest_p, current_network


@app.cell(hide_code=True)
def _(N_slider, current_network, k_slider, np, pd):
    def create_network_data(G, N, k):
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


    # Create network data for current state
    all_nodes, all_edges = create_network_data(
        current_network, N_slider.value, k_slider.value
    )
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
        network = (
            (edges_chart + nodes_chart)
            .properties(
                width=400,
                height=400,
                title=f"Precomputed Network (N={N_slider.value}, k={k_slider.value}, p={p_slider.value:.2f})",
            )
            .resolve_scale(color="independent")
        )

        return network


    network_chart = create_network_chart()
    network_chart = mo.ui.altair_chart(network_chart)
    return (network_chart,)


@app.cell(hide_code=True)
def _(all_metrics, closest_p):
    # Find current metrics from precomputed data
    current_metrics = next(m for m in all_metrics if m["p"] == closest_p)

    C = current_metrics["C"]
    L = current_metrics["L"]
    sigma = current_metrics["sigma"]
    sigma_unnormalized = current_metrics["sigma_unnormalized"]
    edges_rewired = current_metrics["edges_rewired"]
    return C, L, edges_rewired, sigma, sigma_unnormalized


@app.cell(hide_code=True)
def _(all_metrics, p_slider):
    # Get data up to current p value for progressive display
    current_p = p_slider.value
    progressive_data = [m for m in all_metrics if m["p"] <= current_p]
    return (progressive_data,)


@app.cell(hide_code=True)
def _(alt, mo, p_slider, pd, progressive_data):
    # Create properties plot
    def create_properties_chart():
        # Prepare clustering data
        C_data = []
        for data_point in progressive_data:
            C_data.extend(
                [
                    {
                        "p": data_point["p"],
                        "value": data_point["C"],
                        "metric": "C(p) - Raw",
                    },
                    {
                        "p": data_point["p"],
                        "value": data_point["C_normalized"],
                        "metric": "C(p) / C(random)",
                    },
                ]
            )

        C_df = pd.DataFrame(C_data)

        # Clustering chart
        properties_chart = (
            alt.Chart(C_df)
            .mark_line(point=True, strokeWidth=2.5)
            .encode(
                x=alt.X(
                    "p:Q",
                    title="Rewiring Probability (p)",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                y=alt.Y("value:Q", title="Clustering Values"),
                color=alt.Color(
                    "metric:N",
                    scale=alt.Scale(
                        domain=["C(p) - Raw", "C(p) / C(random)"],
                        range=["steelblue", "lightblue"],
                    ),
                    legend=alt.Legend(title="Clustering"),
                ),
                tooltip=["p:Q", "value:Q", "metric:N"],
            )
            .properties(
                width=175,
                height=160,
                title="Clustering Coefficient",
            )
        )

        # Add vertical line at current p
        current_p_line = (
            alt.Chart(pd.DataFrame({"p": [p_slider.value]}))
            .mark_rule(color="gray", strokeDash=[5, 5], strokeWidth=2)
            .encode(x="p:Q")
        )

        return properties_chart + current_p_line


    C_chart = mo.ui.altair_chart(create_properties_chart())
    return (C_chart,)


@app.cell(hide_code=True)
def _(alt, mo, p_slider, pd, progressive_data):
    # Create path length chart
    def create_path_length_chart():
        # Prepare path length data
        L_data = []
        for data_point in progressive_data:
            L_data.extend(
                [
                    {
                        "p": data_point["p"],
                        "value": data_point["L"],
                        "metric": "L(p) - Raw",
                    },
                    {
                        "p": data_point["p"],
                        "value": data_point["L_normalized"],
                        "metric": "L(p) / L(random)",
                    },
                ]
            )

        L_df = pd.DataFrame(L_data)

        # Path length chart
        path_length_chart = (
            alt.Chart(L_df)
            .mark_line(point=True, strokeWidth=2.5)
            .encode(
                x=alt.X(
                    "p:Q",
                    title="Rewiring Probability (p)",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                y=alt.Y("value:Q", title="Path Length Values"),
                color=alt.Color(
                    "metric:N",
                    scale=alt.Scale(
                        domain=["L(p) - Raw", "L(p) / L(random)"],
                        range=["red", "orange"],
                    ),
                    legend=alt.Legend(title="Path Length"),
                ),
                tooltip=["p:Q", "value:Q", "metric:N"],
            )
            .properties(
                width=175,
                height=160,
                title="Average Path Length",
            )
        )

        # Add vertical line at current p
        current_p_line = (
            alt.Chart(pd.DataFrame({"p": [p_slider.value]}))
            .mark_rule(color="gray", strokeDash=[5, 5], strokeWidth=1)
            .encode(x="p:Q")
        )

        return path_length_chart + current_p_line


    L_chart = mo.ui.altair_chart(create_path_length_chart())
    return (L_chart,)


@app.cell(hide_code=True)
def _(alt, mo, p_slider, pd, progressive_data):
    # Create small-world coefficient plot
    def create_sigma_chart():
        sigma_data = [{"p": d["p"], "sigma": d["sigma"]} for d in progressive_data]
        sigma_df = pd.DataFrame(sigma_data)

        sigma_chart = (
            alt.Chart(sigma_df)
            .mark_line(point=True, color="green", strokeWidth=2.5)
            .encode(
                x=alt.X(
                    "p:Q",
                    title="Fraction of Edges Rewired (p)",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                y=alt.Y("sigma:Q", title="Small-World Coefficient (σ)"),
                tooltip=["p:Q", "sigma:Q"],
            )
            .properties(
                width=175,
                height=160,
                title="Small-World Coefficient σ",
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
def _(alt, mo, p_slider, pd, progressive_data):
    # Create unnormalized small-world coefficient plot
    def create_sigma_naive_chart():
        # Prepare unnormalized sigma data
        sigma_naive_data = [
            {"p": d["p"], "sigma_unnormalized": d["sigma_unnormalized"]}
            for d in progressive_data
        ]
        sigma_naive_df = pd.DataFrame(sigma_naive_data)

        # Unnormalized sigma chart
        sigma_naive_chart = (
            alt.Chart(sigma_naive_df)
            .mark_line(point=True, color="purple", strokeWidth=2.5)
            .encode(
                x=alt.X(
                    "p:Q",
                    title="Rewiring Probability (p)",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                y=alt.Y("sigma_unnormalized:Q", title="σ_naive = C/L"),
                tooltip=["p:Q", "sigma_unnormalized:Q"],
            )
            .properties(
                width=175,
                height=160,
                title="Unnormalized σ_naive",
            )
        )

        # Add vertical line at current p
        current_p_line = (
            alt.Chart(pd.DataFrame({"p": [p_slider.value]}))
            .mark_rule(color="gray", strokeDash=[5, 5], strokeWidth=1)
            .encode(x="p:Q")
        )

        return sigma_naive_chart + current_p_line


    sigma_naive_chart = mo.ui.altair_chart(create_sigma_naive_chart())
    return (sigma_naive_chart,)


@app.cell(hide_code=True)
def _(
    C,
    L,
    N_slider,
    edges_rewired,
    k_slider,
    mo,
    np,
    p_slider,
    sigma,
    sigma_unnormalized,
):
    # Calculate reference values for display
    C_random_display = k_slider.value / (N_slider.value - 1)
    L_random_display = np.log(N_slider.value) / np.log(k_slider.value)
    total_edges = (
        N_slider.value * k_slider.value // 2
    )  # Total edges in ring lattice

    mo.md(
        f"""
    ## Understanding the Small-World Effect

    **Current rewiring level: {p_slider.value:.2f}** (precomputed network state)
    - **{edges_rewired} out of {total_edges} edges rewired** ({int(p_slider.value * 100):.0f}%)
    - **{total_edges - edges_rewired} original ring edges remain**

    ### Current Network Metrics:
    | Metric | Value | Random Reference | Ratio/Index |
    |--------|-------|------------------|-------------|
    | **Clustering (C)** | {C:.4f} | {C_random_display:.4f} | {C / max(C_random_display, 0.001):.2f} |
    | **Path Length (L)** | {L:.4f} | {L_random_display:.4f} | {L / max(L_random_display, 0.001):.2f} |
    | **Small-world σ** | {sigma:.4f} | - | {"Strong" if sigma > 1 else "Weak"} |
    | **Unnormalized σ_naive** | {sigma_unnormalized:.4f} | - | C/L ratio |

    ### Key Insights:
    1. **Precomputed approach**: All network states computed once → instant visualization
    2. **Analytical references**: C_random = k/(n-1), L_random = ln(n)/ln(k) 
    3. **Small-world regime**: σ > 1 means high clustering + short paths
    4. **Visual feedback**: Blue edges = original ring, Red edges = rewired shortcuts

    ### Understanding the Transition:
    - **p = 0**: Regular ring lattice (high clustering, long paths)
    - **Small p** (0.01-0.2): Sweet spot where clustering stays high but paths shorten
    - **Large p** (0.5-1.0): Approaches random graph (short paths but low clustering)

    **Notice**: Even rewiring just {int(0.1 * total_edges)} edges (10%) creates dramatic shortcuts!
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ## Mathematical Background

    We compute both **normalized** and **unnormalized** small-world measures:

    **1. Normalized Small-World Coefficient (σ):**
    $$σ = \\frac{C/C_{\\text{random}}}{L/L_{\\text{random}}} = \\frac{C \\cdot L_{\\text{random}}}{L \\cdot C_{\\text{random}}}$$

    **2. Unnormalized Small-World Index (σ_naive):**
    $$σ_{\\text{naive}} = \\frac{C}{L}$$

    **Analytical Reference Values:**
    - $C_{\\text{random}} = \\frac{k}{n-1}$ (exact for Erdős-Rényi graphs)
    - $L_{\\text{random}} = \\frac{\\ln n}{\\ln k}$ (approximation for connected random graphs)

    **Why Both Measures Matter:**
    - **σ_naive**: Simple ratio but can be misleading (doesn't account for network size/density)
    - **σ**: Normalized against random networks, provides meaningful comparison baseline
    - **Raw C(p), L(p)**: Show actual network properties without normalization

    **Interpretation:**
    - σ >> 1: Strong small-world property (high clustering relative to random + short paths relative to lattice)
    - σ ≈ 1: Similar to random networks  
    - σ < 1: Regular/lattice-like behavior
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
