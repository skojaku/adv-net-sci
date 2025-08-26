# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "numpy==2.3.2",
#     "pandas==2.3.1",
#     "python-igraph==0.11.9",
#     "matplotlib==3.10.5",
#     "pyarrow",
#     "openai==1.99.5",
#     "vega-datasets==0.9.0",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App(width="full")

with app.setup(hide_code=True):
    # Initialization code that runs before all other cells
    import numpy as np
    import igraph
    import pandas as pd
    import scipy

@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Network Robustness Assignment: Bond Percolation

    Welcome to the Network Robustness assignment! You'll learn about network resilience through hands-on implementation and develop strategies to attack real-world networks by targeting **edges** (connections) rather than nodes.

    ## What is the Bond Percolation?

    ![Percolation Example](https://upload.wikimedia.org/wikipedia/commons/7/7c/Percolation1.jpg)

    *Image: Visual comparison of site percolation (removing nodes) vs bond percolation (removing edges). Notice how bond percolation can fragment networks more efficiently.*

    **Bond Percolation** focuses on edge removal and proves more realistic for many real-world scenarios than node-based approaches. In communication networks, disruptions typically involve severing communication links between servers rather than destroying entire servers. Transportation systems experience road closures, flight cancellations, and bridge failures that block specific routes while leaving endpoints intact. Power grids suffer transmission line failures more frequently than complete power station shutdowns. Even in cyber attacks, adversaries often target network connections rather than attempting to take down entire devices or servers.

    This assignment will guide you through implementing edge-based attack strategies with real-time visualization and developing your own attack strategy to break networks more effectively than standard approaches.

    ## Bond vs Site Percolation: Why Attack Edges?

    **Site Percolation (Node Attacks)** represents the approach you're likely familiar with from previous network analysis. In site percolation, you remove entire nodes from the network - imagine closing a train station, which eliminates both the station itself and all railway connections that pass through it. This is like removing intersections from a road network where both the intersection and all roads leading to it disappear simultaneously. Site percolation often requires targeting high-impact hub nodes to effectively fragment networks, as removing peripheral nodes typically has minimal impact on overall connectivity.

    **Bond Percolation (Edge Attacks)** forms the focus of today's assignment and represents a fundamentally different approach to network disruption. Instead of removing entire nodes, bond percolation removes individual edges while keeping all nodes intact. Consider the difference: rather than closing an entire train station, you're closing just one railway line between two stations - both stations remain operational, but passengers cannot travel between them via that specific route. This approach is like blocking a single road between two intersections while leaving the intersections themselves fully functional. Remarkably, bond percolation can often fragment networks more efficiently than site percolation, achieving the same level of disconnection with fewer total removals.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 📋 Assignment Instructions & Grading""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "📋 Assignment Tasks": mo.md(
                r"""
            Complete the following tasks and upload your notebook to your GitHub repository.

            1. **Task 1**: Implement `random_edge_attack(graph)` - Function that returns a random edge to remove
            2. **Task 2**: Implement `degree_edge_attack(graph)` - Function that returns the edge connecting highest-degree nodes
            3. **Task 3**: Implement `custom_edge_attack(graph)` - Design your own edge attack strategy (betweenness, custom logic, etc.)
            4. Update this notebook by using `git add`, `git commit`, and then `git push`.
            5. The notebook will be automatically graded, and your score will be shown on GitHub.
            """
            ),
            "🔒 Protected Files": mo.md(
                r"""
            Protected files are test files and configuration files you cannot modify. They appear in your repository but don't make any changes to them.
            """
            ),
            "⚖️ Academic Integrity": mo.md(
                r"""
            There is a system that automatically checks code similarity across all submissions and online repositories. Sharing code or submitting copied work will result in zero credit and disciplinary action.

            While you can discuss concepts, each student must write their own code. Cite any external resources, including AI tools, in your comments.
            """
            ),
            "📚 Allowed Libraries": mo.md(
                r"""
            You **cannot** import any other libraries that result in the grading script failing or a zero score. Only use: `numpy`, `igraph`, `altair`, `pandas`.
            """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🚇 The London Transportation Network Dataset

    ### What is this network?

    The **London Multiplex Transportation Network** represents the real public transport system in London, England. This dataset captures the complex interconnections between different transportation modes in one of the world's most sophisticated urban transit systems.

    **Network Properties:**

    - **369 nodes**: Individual transport stations across London
    - **430 edges**: Direct connections between stations
    - **3 transportation layers**: Underground (Tube), Overground, and DLR (Docklands Light Railway)
    - **Geographic coordinates**: Real latitude/longitude for every station
    - **Multiplex structure**: Stations can be connected via multiple transportation modes

    ### Data Source & Research Context

    This dataset comes from **Manlio De Domenico's** research on navigability of interconnected networks under random failures (available at [manliodedomenico.com](https://manliodedomenico.com/data/)). It's been used in multiple scientific publications studying:

    - Network resilience in transportation systems
    - Cascading failures in multiplex networks
    - Urban mobility and accessibility
    - Infrastructure vulnerability assessment

    ---
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 1: Random Edge Attack (This function is implemented for the sake of demonstration; you do not need to change anything here)

    Implement a **plug-and-play** function that selects edges to remove randomly. This models random failures in infrastructure networks like cable cuts, router malfunctions, or accidental disconnections.

    Your function should:
    - Take a network as input
    - Return a tuple `(source_node, target_node)` representing an edge to remove
    - Handle edge cases (empty graph, no edges remaining)
    - Be **stateless** - each call should work independently

    **Edge format**: Return `(u, v)` where `u` and `v` are node IDs of the edge endpoints.
    """
    )
    return


@app.cell
def _(np):
    def random_edge_attack_sequence(graph):
        """
        EXAMPLE IMPLEMENTATION: Generate complete sequence of random edge removals.
        This function is provided as an example - students don't need to implement this.

        Args:
            graph (igraph.Graph): Input graph

        Returns:
            list: Complete sequence of (source_node, target_node) tuples in removal order
        """
        # Create list of all edges
        all_edges = [(edge.source, edge.target) for edge in graph.es]

        # Shuffle them randomly
        np.random.shuffle(all_edges)

        return all_edges
    return (random_edge_attack_sequence,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 2: Degree-Based Edge Attack

    Implement a function that selects edges connecting **high-degree nodes** for removal. This targets the most connected parts of the network, which are often critical for maintaining connectivity.

    ### Mathematical Definition

    For each edge $e = (u, v)$ in the network, calculate the **degree product score**:

    $$\text{Score}(e) = \text{degree}(u) \times \text{degree}(v)$$

    Where:
    - $\text{degree}(u)$ = number of edges connected to node $u$
    - $\text{degree}(v)$ = number of edges connected to node $v$

    **Edge Removal Order**: Remove edges in **descending order** of their degree product scores:
    $$\text{Score}(e_1) \geq \text{Score}(e_2) \geq \text{Score}(e_3) \geq \ldots$$

    ### Your function should:

    - Calculate degree product score for all edges using the formula above
    - Sort edges by score in descending order (highest scores first)
    - Return complete sequence as list of `(source_node, target_node)` tuples
    - Be stateless like Task 1

    **Implementation Hint**: Use `graph.degree()` to get node degrees, then compute $\text{degree}(u) \times \text{degree}(v)$ for each edge $(u,v)$.
    """
    )
    return


@app.function
# Task 2
def degree_edge_attack_sequence(graph):
    """
    TASK 1: Implement degree-based edge attack sequence.
    Generate complete sequence of edges to remove, prioritizing edges connecting high-degree nodes.

    Args:
        graph (igraph.Graph): Input graph

    Returns:
        list: Complete sequence of (source_node, target_node) tuples in removal order

    Hint: Sort edges by the product of their endpoint degrees (highest first)
    """
    # TODO: Implement your degree-based attack sequence here!
    #
    # Strategy: Remove edges connecting nodes with highest combined degrees first
    #
    # Steps:
    # 1. Get all edges and their endpoint degrees
    # 2. Calculate degree product for each edge (degree[source] * degree[target])
    # 3. Sort edges by degree product (highest first)
    # 4. Return the sorted list
    #
    # Your code here:

    # TODO: Implement your degree-based attack sequence here!
    #
    # Follow the mathematical definition from the task description:
    # 1. For each edge e = (u, v), calculate Score(e) = degree(u) × degree(v)
    # 2. Sort edges by score in descending order
    # 3. Return the sorted list of (source_node, target_node) tuples
    #
    # Placeholder implementation - replace with your implementation
    import random
    edges = [(edge.source, edge.target) for edge in graph.es]
    random.shuffle(edges)
    return edges


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3: Custom Edge Attack Strategy

    **This is the main challenge!** Design your own edge attack strategy that breaks the London Transport network faster than the degree-based edge attack.

    ### Your Mission:
    Develop a custom edge selection strategy that makes connectivity drop more rapidly than removing edges by degree alone.

    ### Success Criteria:
    Your attack should make the London Transport network's connectivity drop below 0.5 using **fewer edge removals** than the degree-based edge attack.

    ### Ideas:
    - Instead of calculating the order of edges all at once based on the original network in the begining, you can compute the likely vulnerable edges at each edge removal step.
    - High-degree nodes with few common neighbors are easy targets. You can think of a strategy based on two node characteristics, i.e., degree product and the number of common neighbors.
    """
    )
    return


@app.function
# Task 3 - Your custom attack strategy
def custom_edge_attack_sequence(graph):
    """
    TASK 2: Implement your custom edge attack sequence to break networks faster than degree-based attack.

    Args:
        graph (igraph.Graph): Input graph

    Returns:
        list: Complete sequence of (source_node, target_node) tuples in removal order

    TODO: Describe your strategy here!
    Strategy description: [Explain your approach - e.g., betweenness centrality, edge betweenness, closeness, etc.]
    """
    # TODO: Implement your custom attack sequence here!
    #
    # Challenge: Beat the degree-based attack in terms of making connectivity drop faster
    #
    # Your code here:

    # TODO: Implement your custom attack strategy here!
    #
    # Replace this placeholder with your own edge attack algorithm.
    # Your strategy should outperform the degree-based attack.
    #
    # Return: Complete sequence of (source_node, target_node) tuples

    # Placeholder implementation - replace with your strategy
    import random
    edges = [(edge.source, edge.target) for edge in graph.es]
    random.shuffle(edges)
    return edges


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## Interactive Analysis: London Transport Network Edge Attacks

    Now let's test your implementations on the London Transport network! This puts your code to work on a **real infrastructure network** where every node represents an actual train station and every edge represents a physical connection that millions of Londoners use daily.

    ### From Theory to Practice

    Your attack functions will generate **complete sequences** of edges to remove, and the visualization will show how London's transport connectivity degrades as you progress through these sequences. This approach mirrors real-world scenarios:

    - **Random sequence**: Simulates cascading failures from equipment breakdowns, weather events, or random disruptions
    - **Degree-based sequence**: Models targeted attacks on major interchanges like King's Cross, Oxford Circus, or Stratford
    - **Custom sequence**: Your strategic approach to maximally disrupt London's transport with minimal edge removals

    ### Real-Time Edge Removal Visualization
    Use the controls below to see how each attack strategy progressively fragments the network. The geographic visualization shows **actual London geography** with borough boundaries and station locations - you can watch connectivity patterns change across the real city!
    """
    )
    return


@app.cell(hide_code=True)
def _(mo, test_network):
    # Attack strategy selector and edge removal slider
    strategy_selector = mo.ui.dropdown(
        options=["random", "degree", "custom"],
        value="random",
        label="Attack Strategy",
    )

    # Set max edges based on network size (will be refined in next cell)
    max_edges_removable = min(445, test_network.ecount())

    # Slider for number of edges removed
    edges_removed_slider = mo.ui.slider(
        start=0,
        stop=max_edges_removable,
        step=1,
        value=0,
        label=f"Number of Edges Removed (Max: {max_edges_removable})",
    )

    mo.md(f"""
    **Select Attack Strategy:** {strategy_selector}

    **Progressive Edge Removal:** {edges_removed_slider}
    """)
    return edges_removed_slider, strategy_selector


@app.cell(hide_code=True)
def _(
    attack_comparison_chart,
    edges_removed_slider,
    mo,
    network_chart,
    strategy_selector,
):
    # Display current status
    status = mo.md(f"""
    ### Current Status:
    **Strategy**: {strategy_selector.value}
    **Edges Removed**: {edges_removed_slider.value}
    """)

    mo.vstack(
        [
            status,
            mo.hstack(
                [network_chart, attack_comparison_chart],
                justify="center",
                align="center",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Understanding the Results

    The visualizations show how your attack strategies fragment London's transport network. The left panel displays a geographic map of London stations, while the right panel compares attack effectiveness.

    **Geographic Visualization**: Stations in the largest connected component appear in light red, while isolated stations are gray. Hover over stations to see actual names like King's Cross or Oxford Circus. London borough boundaries provide geographic context.

    **Comparison Charts**: Each strategy appears as a colored line (blue=random, red=degree, orange=custom) plotting fraction of edges removed against network connectivity. The large dot shows your current slider position, and the gray dashed line marks 50% connectivity.

    **Network Fragmentation**: Early edge removal (10-20%) has minimal impact. The critical phase (20-60%) causes rapid connectivity loss as major corridors are severed. Beyond 60%, the network fragments into isolated components.

    **Your Goal**: Design a custom attack sequence that reaches 50% connectivity faster than degree-based attacks. Random attacks represent accidental failures, degree attacks target major interchanges, and your custom strategy should exploit London's specific vulnerabilities like river crossings or central bottlenecks.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Libraries""")
    return


@app.cell(hide_code=True)
def _():
    # All imports in one place to avoid conflicts
    import altair as alt

    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    import io
    import base64
    import os
    import urllib.request
    import zipfile
    from vega_datasets import data

    # Configure Altair for large datasets
    # Disable max_rows limit for handling large network data
    alt.data_transformers.disable_max_rows()
    return alt, base64, data, io, os, plt, zipfile


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Code""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Load Karate Club Network""")
    return


@app.cell(hide_code=True)
def _(igraph):
    # Load Zachary's Karate Club network
    def load_karate_network():
        """Load the famous Zachary's Karate Club network"""
        try:
            # Load the built-in Karate Club network from igraph
            g_karate = igraph.Graph.Famous("Zachary")
            return g_karate
        except Exception as e:
            print(f"Error loading Karate Club network: {e}")
            # Create a small test network if loading fails
            g = igraph.Graph.Erdos_Renyi(34, 0.1)
            return g.connected_components().giant()


    # Load the Karate Club network
    karate_network = load_karate_network()
    print(
        f"Karate Club network: {karate_network.vcount()} nodes, {karate_network.ecount()} edges"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Network Utility Functions""")
    return


@app.cell(hide_code=True)
def _(np):
    def network_connectivity(graph, original_size=None):
        """Calculate network connectivity as fraction of nodes in largest component"""
        if original_size is None:
            original_size = graph.vcount()

        if graph.vcount() == 0:
            return 0.0

        components = graph.connected_components()
        return (
            max(components.sizes()) / original_size if components.sizes() else 0.0
        )


    def calculate_network_stats(graph):
        """Calculate basic network statistics"""
        return {
            "nodes": graph.vcount(),
            "edges": graph.ecount(),
            "density": graph.density(),
            "avg_degree": np.mean(graph.degree()),
            "max_degree": max(graph.degree()) if graph.vcount() > 0 else 0,
        }
    return calculate_network_stats, network_connectivity


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Run Attack Simulations""")
    return


@app.cell(hide_code=True)
def _(
    calculate_network_stats,
    london_network,
    network_connectivity,
    pd,
    random_edge_attack_sequence,
):
    # Edge-based attack simulation functions
    def simulate_edge_attack_sequence(
        graph, attack_function, max_edges=None, return_deletions=False
    ):
        """
        Simulate edge removal sequence using the given attack function

        Args:
            graph: Input graph
            attack_function: Function that returns (u, v) edge to remove
            max_edges: Maximum number of edges to remove (None = all edges)
            return_deletions: If True, also return the deletion order

        Returns:
            DataFrame with frac_edges_removed and connectivity columns
            If return_deletions=True: (DataFrame, list of edges removed)
        """
        g = graph.copy()
        original_nodes = g.vcount()
        total_edges = g.ecount()

        if max_edges is None:
            max_edges = total_edges

        results = [{"frac_edges_removed": 0.0, "connectivity": 1.0}]
        deletion_order = []

        for i in range(min(max_edges, total_edges)):
            # Get edge to remove using attack function
            try:
                edge_to_remove = attack_function(g)
                if edge_to_remove is None:
                    break

                u, v = edge_to_remove

                # Remove the edge
                if g.are_adjacent(u, v):
                    g.delete_edges([(u, v)])
                    deletion_order.append(
                        (min(u, v), max(u, v))
                    )  # Normalize edge order

                # Calculate connectivity
                connectivity = network_connectivity(g, original_nodes)
                frac_removed = (i + 1) / total_edges

                results.append(
                    {
                        "frac_edges_removed": frac_removed,
                        "connectivity": connectivity,
                    }
                )

                # Stop if network is completely disconnected
                if connectivity < 0.01:
                    break

            except Exception as e:
                print(f"Error in attack simulation: {e}")
                break

        if return_deletions:
            return pd.DataFrame(results), deletion_order
        return pd.DataFrame(results)


    # Generate attack sequences for all strategies
    def simulate_attack_sequence_from_edges(graph, edge_sequence):
        """
        NEW APPROACH: Simulate network robustness from pre-computed edge sequence.
        This replaces the old approach with complete pre-computation.

        Args:
            graph: Original network
            edge_sequence: Complete list of (u,v) edge tuples in removal order

        Returns:
            dict: Contains connectivity profile, largest component membership over time
        """
        g = graph.copy()
        original_nodes = g.vcount()
        total_edges = len(edge_sequence)

        # Track results
        results = []
        component_history = []

        # Initial state (no edges removed)
        components = g.connected_components()
        largest_comp = max(components, key=len)
        connectivity = len(largest_comp) / original_nodes

        results.append(
            {
                "edges_removed": 0,
                "frac_edges_removed": 0.0,
                "connectivity": connectivity,
                "largest_component_size": len(largest_comp),
            }
        )
        component_history.append(set(largest_comp))

        # Remove edges sequentially and track connectivity
        for i, (u, v) in enumerate(edge_sequence):
            try:
                if g.are_adjacent(u, v):
                    g.delete_edges([(u, v)])

                # Calculate new connectivity and largest component
                components = g.connected_components()
                if components:
                    largest_comp = max(components, key=len)
                    connectivity = len(largest_comp) / original_nodes
                else:
                    largest_comp = []
                    connectivity = 0.0

                results.append(
                    {
                        "edges_removed": i + 1,
                        "frac_edges_removed": (i + 1) / total_edges,
                        "connectivity": connectivity,
                        "largest_component_size": len(largest_comp),
                    }
                )
                component_history.append(set(largest_comp))

            except:
                continue

        return {
            "profile": pd.DataFrame(results),
            "component_history": component_history,
            "edge_sequence": edge_sequence,
        }


    def generate_attack_analyses(graph):
        """Generate complete pre-computed analyses for all attack strategies"""
        analyses = {}

        # Random attack analysis
        try:
            edge_seq = random_edge_attack_sequence(graph)
            analyses["random"] = simulate_attack_sequence_from_edges(
                graph, edge_seq
            )
        except Exception as e:
            print(f"Random attack failed: {e}")
            analyses["random"] = {
                "profile": pd.DataFrame(
                    {
                        "edges_removed": [0],
                        "frac_edges_removed": [0],
                        "connectivity": [1],
                    }
                ),
                "component_history": [set()],
                "edge_sequence": [],
            }

        # Degree-based attack analysis
        try:
            edge_seq = degree_edge_attack_sequence(graph)
            if edge_seq:  # Only if implementation exists
                analyses["degree"] = simulate_attack_sequence_from_edges(
                    graph, edge_seq
                )
            else:
                raise Exception("Not implemented")
        except Exception as e:
            print(f"Degree attack not implemented or failed: {e}")
            analyses["degree"] = {
                "profile": pd.DataFrame(
                    {
                        "edges_removed": [0],
                        "frac_edges_removed": [0],
                        "connectivity": [1],
                    }
                ),
                "component_history": [set()],
                "edge_sequence": [],
            }

        # Custom attack analysis
        try:
            edge_seq = custom_edge_attack_sequence(graph)
            if edge_seq:  # Only if implementation exists
                analyses["custom"] = simulate_attack_sequence_from_edges(
                    graph, edge_seq
                )
            else:
                raise Exception("Not implemented")
        except Exception as e:
            print(f"Custom attack not implemented or failed: {e}")
            analyses["custom"] = {
                "profile": pd.DataFrame(
                    {
                        "edges_removed": [0],
                        "frac_edges_removed": [0],
                        "connectivity": [1],
                    }
                ),
                "component_history": [set()],
                "edge_sequence": [],
            }

        return analyses


    # Use the London Transport network (or karate club if London not available)
    test_network = london_network.connected_components().giant()


    # Generate complete pre-computed analyses for all attack strategies
    attack_analyses = generate_attack_analyses(test_network)
    network_stats = calculate_network_stats(test_network)

    # Extract data for backward compatibility
    attack_sequences = {}
    precomputed_deletions = {}
    for strategy, analysis in attack_analyses.items():
        attack_sequences[strategy] = analysis["profile"]
        precomputed_deletions[strategy] = analysis["edge_sequence"]

    print(
        f"Test network: {test_network.vcount()} nodes, {test_network.ecount()} edges"
    )
    return attack_sequences, network_stats, precomputed_deletions, test_network


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Robustness Chart""")
    return


@app.cell(hide_code=True)
def _(
    alt,
    attack_sequences,
    current_connectivity,
    edges_removed_slider,
    pd,
    strategy_selector,
):
    # Create robustness profile chart for selected strategy
    def create_robustness_chart(
        sequences, selected_strategy, current_edges_removed, current_conn
    ):
        if (
            selected_strategy not in sequences
            or len(sequences[selected_strategy]) == 0
        ):
            return (
                alt.Chart()
                .mark_text(
                    text="Please implement the required functions to see visualization",
                    fontSize=14,
                )
                .properties(width=400, height=300)
            )

        data = sequences[selected_strategy].copy()
        data["strategy"] = selected_strategy

        # Color mapping
        color_map = {"random": "blue", "degree": "red", "custom": "orange"}
        color = color_map.get(selected_strategy, "gray")

        # Main line chart
        chart = (
            alt.Chart(data)
            .mark_line(strokeWidth=3, color=color)
            .encode(
                x=alt.X(
                    "frac_edges_removed:Q",
                    title="Fraction of Edges Removed",
                    scale=alt.Scale(
                        domain=[0, max(data["frac_edges_removed"].max(), 0.3)]
                    ),
                ),
                y=alt.Y(
                    "connectivity:Q",
                    title="Network Connectivity",
                    scale=alt.Scale(domain=[0, 1]),
                ),
            )
        )

        # Add points for data
        points = (
            alt.Chart(data)
            .mark_circle(size=40, color=color, opacity=0.6)
            .encode(
                x=alt.X("frac_edges_removed:Q"),
                y=alt.Y("connectivity:Q"),
            )
        )

        # Add current position marker
        current_frac_removed = (
            current_edges_removed
            / max(1, data.iloc[0]["frac_edges_removed"] * len(data))
            if len(data) > 1
            else 0
        )
        current_point = (
            alt.Chart(
                pd.DataFrame(
                    [
                        {
                            "frac_edges_removed": current_frac_removed,
                            "connectivity": current_conn,
                        }
                    ]
                )
            )
            .mark_circle(
                size=200, color=color, stroke="black", strokeWidth=3, opacity=0.9
            )
            .encode(
                x=alt.X("frac_edges_removed:Q"),
                y=alt.Y("connectivity:Q"),
            )
        )

        # Add reference lines
        reference_lines = (
            alt.Chart(pd.DataFrame({"y": [0.5]}))
            .mark_rule(color="gray", strokeDash=[5, 5], opacity=0.7)
            .encode(y=alt.Y("y:Q"))
        )

        return (chart + points + current_point + reference_lines).properties(
            width=400,
            height=300,
            title=f"{selected_strategy.title()} Edge Attack - Connectivity: {current_conn:.3f}",
        )


    robustness_chart = create_robustness_chart(
        attack_sequences,
        strategy_selector.value,
        edges_removed_slider.value,
        current_connectivity,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Attack Comparison Chart""")
    return


@app.cell(hide_code=True)
def _(
    alt,
    attack_sequences,
    edges_removed_slider,
    london_network,
    pd,
    strategy_selector,
    test_network,
):
    # Create comparison chart of all attack strategies
    def create_comparison_chart(
        sequences, current_edges_removed, selected_strategy, total_edges
    ):
        # Combine all results
        combined_data = []
        color_map = {"random": "blue", "degree": "red", "custom": "orange"}

        for strategy, data in sequences.items():
            if len(data) > 0:
                temp_data = data.copy()
                temp_data["strategy"] = strategy
                combined_data.append(temp_data)

        if not combined_data:
            return (
                alt.Chart()
                .mark_text(
                    text="Please implement the required functions to see comparison",
                    fontSize=14,
                )
                .properties(width=600, height=400)
            )

        comparison_df = pd.concat(combined_data, ignore_index=True)

        # Main chart
        lines = (
            alt.Chart(comparison_df)
            .mark_line(strokeWidth=3)
            .encode(
                x=alt.X(
                    "frac_edges_removed:Q",
                    title="Fraction of Edges Removed",
                    scale=alt.Scale(
                        domain=[0, comparison_df["frac_edges_removed"].max()]
                    ),
                ),
                y=alt.Y(
                    "connectivity:Q",
                    title="Network Connectivity",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                color=alt.Color(
                    "strategy:N",
                    scale=alt.Scale(
                        domain=["random", "degree", "custom"],
                        range=["blue", "red", "orange"],
                    ),
                    legend=alt.Legend(
                        title="Attack Strategy",
                        orient="top-right",
                        fillColor="black",
                        padding=10,
                        cornerRadius=5,
                        strokeColor="lightgray",
                    ),
                ),
            )
        )

        # Add reference line at 50% connectivity
        reference_line = (
            alt.Chart(pd.DataFrame({"y": [0.5]}))
            .mark_rule(color="gray", strokeDash=[5, 5], opacity=0.7)
            .encode(y=alt.Y("y:Q"))
        )

        # Add text annotation
        annotation = (
            alt.Chart(
                pd.DataFrame({"x": [0.01], "y": [0.52], "text": ["50% threshold"]})
            )
            .mark_text(align="left", fontSize=10, color="gray")
            .encode(x="x:Q", y="y:Q", text="text:N")
        )

        # Add current position dots for each strategy
        current_frac_removed = (
            current_edges_removed / total_edges if total_edges > 0 else 0
        )
        current_positions = []

        for strategy, data in sequences.items():
            if len(data) > 0:
                # Find the closest data point to current slider position
                closest_idx = (
                    (data["frac_edges_removed"] - current_frac_removed)
                    .abs()
                    .idxmin()
                )
                current_connectivity = data.iloc[closest_idx]["connectivity"]

                current_positions.append(
                    {
                        "frac_edges_removed": current_frac_removed,
                        "connectivity": current_connectivity,
                        "strategy": strategy,
                    }
                )

        current_points = None
        if current_positions:
            current_points = (
                alt.Chart(pd.DataFrame(current_positions))
                .mark_circle(size=200, stroke="black", strokeWidth=2)
                .encode(
                    x="frac_edges_removed:Q",
                    y="connectivity:Q",
                    color=alt.Color(
                        "strategy:N",
                        scale=alt.Scale(
                            domain=["random", "degree", "custom"],
                            range=["blue", "red", "orange"],
                        ),
                        legend=None,
                    ),
                )
            )

        network_name = (
            "London Transport Network"
            if london_network is not None
            else "Karate Club Network"
        )

        chart_layers = [lines, reference_line, annotation]
        if current_points is not None:
            chart_layers.append(current_points)

        return alt.layer(*chart_layers).properties(
            width=600,
            height=400,
            title=f"Edge Attack Strategy Comparison: {network_name}",
        )


    attack_comparison_chart = create_comparison_chart(
        attack_sequences,
        edges_removed_slider.value,
        strategy_selector.value,
        test_network.ecount(),
    )
    return (attack_comparison_chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Real-Time Network Visualization""")
    return


@app.cell(hide_code=True)
def _(
    base64,
    edges_removed_slider,
    igraph,
    io,
    london_network,
    network_connectivity,
    plt,
    strategy_selector,
    test_network,
):
    # This cell is deprecated - we now use pre-computed sequences and geographic visualization
    # Kept for compatibility but returns simplified connectivity calculation


    def create_current_network_state(graph, attack_strategy, num_edges_removed):
        """Create network state after removing specified number of edges (simplified version)"""
        # Since we now use pre-computed sequences, just return basic connectivity
        # This is used only for the simple connectivity calculation
        return graph, []


    def create_network_visualization(graph, removed_edges, original_graph):
        """Create igraph network visualization with removed edges highlighted"""
        if graph.vcount() == 0:
            return "<p>Network is empty - all edges removed</p>"

        try:
            import matplotlib

            matplotlib.use("Agg")  # Use non-interactive backend

            # Create a copy of the original graph for visualization
            viz_graph = original_graph.copy()

            # Set edge colors and widths based on removal status
            removed_edge_set = set(
                (min(u, v), max(u, v)) for u, v in removed_edges
            )
            edge_colors = []
            edge_widths = []

            for edge in viz_graph.es:
                u, v = edge.source, edge.target
                edge_key = (min(u, v), max(u, v))
                if edge_key in removed_edge_set:
                    edge_colors.append("red")
                    edge_widths.append(1)  # Thinner for removed edges
                else:
                    edge_colors.append("steelblue")
                    edge_widths.append(2)  # Thicker for active edges

            # Set all nodes to the same color (no differentiation)
            node_colors = [
                "lightblue"
            ] * viz_graph.vcount()  # All nodes same color

            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_aspect("equal")

            # Configure igraph to use matplotlib backend
            try:
                # Generate layout with proper seeding
                import random

                random.seed(42)
                np.random.seed(42)
                layout = viz_graph.layout_fruchterman_reingold()

                # Plot using igraph with matplotlib target
                igraph.plot(
                    viz_graph,
                    target=ax,
                    layout=layout,
                    vertex_size=25,
                    vertex_color=node_colors,
                    vertex_label=list(range(viz_graph.vcount())),
                    vertex_label_size=9,
                    vertex_label_color="black",
                    edge_color=edge_colors,
                    edge_width=edge_widths,
                    margin=30,
                )

                # Customize the plot
                network_name = (
                    "London Transport Network"
                    if london_network is not None
                    else "Karate Club Network"
                )
                ax.set_title(
                    f"{network_name} - {len(removed_edges)} edges removed\n"
                    f"Connectivity: {network_connectivity(graph, original_graph.vcount()):.3f}",
                    fontsize=14,
                    pad=20,
                )

                # Create legend
                import matplotlib.patches as mpatches

                legend_elements = [
                    mpatches.Patch(color="steelblue", label="Active edges"),
                    mpatches.Patch(color="red", label="Removed edges"),
                    mpatches.Patch(color="lightblue", label="Network nodes"),
                ]
                ax.legend(
                    handles=legend_elements,
                    loc="upper left",
                    bbox_to_anchor=(0.02, 0.98),
                )

                # Remove axes
                ax.set_xticks([])
                ax.set_yticks([])
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_visible(False)
                ax.spines["left"].set_visible(False)

                plt.tight_layout()

                # Save to base64 for HTML embedding
                buffer = io.BytesIO()
                plt.savefig(
                    buffer,
                    format="png",
                    dpi=100,
                    bbox_inches="tight",
                    facecolor="white",
                    edgecolor="none",
                )
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.getvalue()).decode()
                plt.close(fig)

                return f'<img src="data:image/png;base64,{image_base64}" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px;" />'

            except Exception as plot_error:
                plt.close(fig)
                # Fallback to text summary if plotting fails
                connectivity = network_connectivity(graph, original_graph.vcount())
                components = graph.connected_components()
                largest_comp_size = (
                    max(components.sizes()) if components.sizes() else 0
                )

                return f"""
                <div style="border: 2px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
                    <h3>Network State (Plot unavailable: {plot_error})</h3>
                    <p><strong>Edges Removed:</strong> {len(removed_edges)}</p>
                    <p><strong>Edges Remaining:</strong> {graph.ecount()}</p>
                    <p><strong>Connectivity:</strong> {connectivity:.3f}</p>
                    <p><strong>Largest Component:</strong> {largest_comp_size}/{original_graph.vcount()} nodes</p>
                </div>
                """

        except Exception as e:
            return f"<p>Error creating visualization: {e}</p>"


    # Create current network state
    try:
        current_graph, removed_edges_list = create_current_network_state(
            test_network, strategy_selector.value, edges_removed_slider.value
        )

        current_network_viz = create_network_visualization(
            current_graph, removed_edges_list, test_network
        )

        # Calculate current connectivity
        current_connectivity = network_connectivity(
            current_graph, test_network.vcount()
        )

    except Exception as e:
        print(f"Error creating network visualization: {e}")
        current_network_viz = f"<p>Error: {e}</p>"
        current_connectivity = 1.0
    return (current_connectivity,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Network Statistics Chart""")
    return


@app.cell(hide_code=True)
def _(alt, london_network, network_stats, pd):
    # Create network statistics visualization
    def create_stats_chart(stats):
        network_name = (
            "London Transport Network"
            if london_network is not None
            else "Karate Club Network"
        )
        stats_data = pd.DataFrame(
            [
                {"metric": "Nodes", "value": stats["nodes"]},
                {"metric": "Edges", "value": stats["edges"]},
                {"metric": "Avg Degree", "value": round(stats["avg_degree"], 2)},
                {"metric": "Max Degree", "value": stats["max_degree"]},
                {"metric": "Density", "value": round(stats["density"], 4)},
            ]
        )

        chart = (
            alt.Chart(stats_data)
            .mark_bar(color="steelblue")
            .encode(
                x=alt.X("value:Q", title="Value"),
                y=alt.Y("metric:N", title="Network Metric", sort=None),
                tooltip=["metric:N", "value:Q"],
            )
            .properties(width=300, height=250, title=f"{network_name} Statistics")
        )

        return chart


    network_stats_chart = create_stats_chart(network_stats)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## London Multiplex Transportation Network Dataset

    This section downloads and processes the London Multiplex Transportation Network dataset from Manlio De Domenico's research on navigability of interconnected networks under random failures.

    The dataset contains:
    - 369 train stations (nodes)
    - Multiple transportation layers: Underground, Overground, and DLR
    - Geographical coordinates and disruption data

    **Reference**: "Navigability of interconnected networks under random failures", De Domenico et al., PNAS 2014
    """
    )
    return


@app.cell(hide_code=True)
def _(mo, os, zipfile):
    # Download and extract London Multiplex Transport dataset


    def download_london_transport_data():
        """Download and extract London Multiplex Transportation dataset"""

        # Dataset URL and local paths
        url = "https://manliodedomenico.com/data/London_Multiplex_Transport.zip"
        zip_filename = "London_Multiplex_Transport.zip"
        extract_dir = "London_Transport_Data"

        # Create data directory if it doesn't exist
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        # Download the zip file if it doesn't exist
        if not os.path.exists(zip_filename):
            print(f"Downloading {url}...")
            try:
                # Add user agent to avoid being blocked
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req) as response:
                    with open(zip_filename, "wb") as f:
                        f.write(response.read())
                print(f"Downloaded {zip_filename}")
            except Exception as e:
                print(f"Error downloading dataset: {e}")
                print("Please manually download the dataset from:")
                print(
                    "https://manliodedomenico.com/data/London_Multiplex_Transport.zip"
                )
                print(
                    "and place it in the current directory, then run this cell again."
                )
                return None
        else:
            print(f"{zip_filename} already exists")

        # Extract the zip file
        try:
            with zipfile.ZipFile(zip_filename, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"Extracted to {extract_dir}")

            # Look for Dataset folder in the extracted contents
            dataset_path = None

            # Check common locations for Dataset folder
            possible_paths = [
                os.path.join(extract_dir, "Dataset"),
                os.path.join(extract_dir, "London_Multiplex_Transport", "Dataset"),
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    dataset_path = path
                    break

            if dataset_path:
                print(f"\nFound Dataset folder at: {dataset_path}")
                print(f"Contents of Dataset folder:")
                for item in os.listdir(dataset_path):
                    item_path = os.path.join(dataset_path, item)
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        print(f"  📄 {item} ({size:,} bytes)")
                    else:
                        print(f"  📁 {item}/")
                return dataset_path
            else:
                print("Dataset folder not found in extracted files")
                print(f"Extracted contents structure:")
                for root, dirs, files in os.walk(extract_dir):
                    level = root.replace(extract_dir, "").count(os.sep)
                    indent = " " * 2 * level
                    print(f"{indent}{os.path.basename(root)}/")
                    subindent = " " * 2 * (level + 1)
                    for f in files[:5]:  # Show only first 5 files to avoid clutter
                        print(f"{subindent}{f}")
                    if len(files) > 5:
                        print(f"{subindent}... and {len(files) - 5} more files")
                return extract_dir

        except Exception as e:
            print(f"Error extracting dataset: {e}")
            return None


    # Download and extract the dataset
    dataset_path = download_london_transport_data()

    mo.md(f"""
    **Dataset Status**: {"✅ Successfully downloaded and extracted" if dataset_path else "❌ Download failed - Manual download required"}

    **Location**: `{dataset_path if dataset_path else "N/A"}`

    **Manual Download Instructions** (if automatic download failed):
    1. Download the dataset from: https://manliodedomenico.com/data/London_Multiplex_Transport.zip
    2. Place the ZIP file in the same directory as this notebook
    3. Re-run this cell to extract the data
    """)
    return (dataset_path,)


@app.cell(hide_code=True)
def _(dataset_path, igraph, mo, np, os, pd):
    # Read and process the London Transport dataset files
    def load_london_transport_network(dataset_path):
        """Load the London Transport multiplex network"""

        if not dataset_path or not os.path.exists(dataset_path):
            print("Dataset path not available")
            return None, None, None, None

        # File paths
        edges_file = os.path.join(dataset_path, "london_transport_multiplex.edges")
        nodes_file = os.path.join(dataset_path, "london_transport_nodes.txt")
        layers_file = os.path.join(dataset_path, "london_transport_layers.txt")

        # Load edges data (no header in edges file)
        if os.path.exists(edges_file):
            edges_df = pd.read_csv(
                edges_file,
                sep=" ",
                names=["layerID", "source", "target", "weight"],
                header=None,
            )
            print(f"Loaded {len(edges_df)} edges from multiplex network")
        else:
            print(f"Edges file not found: {edges_file}")
            return None, None, None, None

        # Load nodes data with coordinates
        if os.path.exists(nodes_file):
            # The nodes file has a header: nodeID nodeLabel nodeLat nodeLong
            nodes_df = pd.read_csv(nodes_file, sep=" ")
            # Keep the required columns including nodeLabel for tooltips and rename them
            nodes_df = nodes_df[
                ["nodeID", "nodeLabel", "nodeLat", "nodeLong"]
            ].rename(columns={"nodeLat": "latitude", "nodeLong": "longitude"})
            print(f"Loaded {len(nodes_df)} nodes with coordinates (expected 369)")
        else:
            print(f"Nodes file not found: {nodes_file}")
            nodes_df = None

        # Load layers information (has header: layerID layerLabel)
        if os.path.exists(layers_file):
            try:
                # Parse manually since layer labels contain spaces
                with open(layers_file, "r") as f:
                    lines = f.readlines()

                layers_data = []
                for line in lines[1:]:  # Skip header line
                    line = line.strip()
                    if line:
                        parts = line.split(" ", 1)  # Split only on first space
                        if len(parts) >= 2:
                            layers_data.append(
                                {"layerID": int(parts[0]), "layerLabel": parts[1]}
                            )

                layers_df = pd.DataFrame(layers_data)
                print(f"Loaded {len(layers_df)} layers with labels")
            except Exception as e:
                print(f"Error reading layers file: {e}")
                layers_df = None
        else:
            print(f"Layers file not found: {layers_file}")
            layers_df = None

        # Create aggregated network (all layers combined)
        print("\nCreating aggregated network...")

        # Get unique edges with proper normalization for undirected graph
        # Normalize edge directions to avoid (u,v) and (v,u) being treated as different
        normalized_edges = []
        for _, row in edges_df[["source", "target"]].iterrows():
            source, target = row["source"], row["target"]
            # Normalize: smaller node first for undirected graph
            edge = (min(source, target), max(source, target))
            normalized_edges.append(edge)

        # Remove duplicates using set
        unique_edges_set = set(normalized_edges)
        print(
            f"Removed {len(normalized_edges) - len(unique_edges_set)} duplicate edges"
        )

        # Create igraph network
        max_node = max(edges_df["source"].max(), edges_df["target"].max())
        g = igraph.Graph(n=max_node + 1, directed=False)

        # Add edges
        edge_list = list(unique_edges_set)
        g.add_edges(edge_list)

        # Remove isolated nodes and get the giant component
        g = g.connected_components().giant()

        print(f"Final network: {g.vcount()} nodes, {g.ecount()} edges")

        return g, edges_df, nodes_df, layers_df


    # Load the London Transport network
    if dataset_path:
        london_network, edges_df, nodes_df, layers_df = (
            load_london_transport_network(dataset_path)
        )

        # Display network statistics
        if london_network:
            london_stats = {
                "nodes": london_network.vcount(),
                "edges": london_network.ecount(),
                "density": london_network.density(),
                "avg_degree": np.mean(london_network.degree()),
                "max_degree": max(london_network.degree()),
                "components": len(london_network.connected_components()),
            }

            mo.md(f"""
            ## London Transport Network Statistics

            - **Nodes**: {london_stats["nodes"]:,}
            - **Edges**: {london_stats["edges"]:,}
            - **Average Degree**: {london_stats["avg_degree"]:.2f}
            - **Maximum Degree**: {london_stats["max_degree"]}
            - **Network Density**: {london_stats["density"]:.4f}
            - **Connected Components**: {london_stats["components"]}

            The network represents London's transportation system with Underground, Overground, and DLR connections.
            You can now apply your edge attack strategies to this real-world transportation network!
            """)
        else:
            mo.md("❌ Failed to load London Transport network")
    else:
        london_network = None
        mo.md("❌ Dataset not available for analysis")
    return edges_df, london_network, nodes_df


@app.cell(hide_code=True)
def _(precomputed_deletions):
    # Display precomputation results - edge deletion orders computed with attack sequences
    print(
        "🚀 Using optimized attack sequence generation with pre-computed edge deletions..."
    )

    if precomputed_deletions:
        for strategy_name, deletion_order in precomputed_deletions.items():
            print(
                f"    ✅ {strategy_name}: {len(deletion_order)} edges in deletion order"
            )
        print(f"🎯 Pre-computation complete! Slider will now be responsive.")
    else:
        print("❌ No deletion orders available")
    return


@app.cell(hide_code=True)
def _(
    alt,
    current_connectivity,
    data,
    edges_df,
    edges_removed_slider,
    london_network,
    mo,
    nodes_df,
    pd,
    precomputed_deletions,
    strategy_selector,
    test_network,
):
    # ====================================================================================
    # GEOGRAPHIC NETWORK VISUALIZATION CODE
    # ====================================================================================
    # This section contains the main visualization function that creates the interactive
    # London Transport Network map. Students can modify this code to customize the
    # visualization or experiment with different visual representations.

    # Pre-compute static geographic background (cached for performance)
    _cached_background = None
    _cached_borough_labels = None
    _cached_tube_lines = None


    def create_simple_background(
        lon_min, lon_max, lat_min, lat_max, chart_width, chart_height
    ):
        """Create a simple, fast geographic background without complex topology"""
        try:
            # Use topological features for proper geographic background
            boroughs = alt.topo_feature(data.londonBoroughs.url, "boroughs")

            # Create simple borough boundaries
            background = (
                alt.Chart(boroughs)
                .mark_geoshape(
                    stroke="darkgray", strokeWidth=1, fill="lightgray", opacity=0.2
                )
                .project(type="identity", reflectY=True)
                .properties(width=chart_width, height=chart_height)
            )

            print("✅ Simple geographic background created")
            return background

        except Exception as geo_error:
            print(f"Debug: Geographic data loading failed: {geo_error}")
            # Fallback to coordinate grid
            return (
                alt.Chart(
                    pd.DataFrame(
                        {
                            "x": [lon_min, lon_max, lon_max, lon_min, lon_min],
                            "y": [lat_min, lat_min, lat_max, lat_max, lat_min],
                        }
                    )
                )
                .mark_line(stroke="lightgray", strokeWidth=1, opacity=0.3)
                .encode(x="x:Q", y="y:Q")
                .properties(width=chart_width, height=chart_height)
            )


    def create_interactive_geographic_visualization(
        network, nodes_data, edges_data, attack_strategy, num_edges_removed
    ):
        """Create geographic visualization showing current network state with London background"""

        if london_network is None or nodes_data is None or edges_data is None:
            return mo.md(
                "❌ Geographic visualization requires London Transport network data"
            )

        try:
            import time

            start_time = time.time()
            print(
                f"Debug: Creating visualization with {num_edges_removed} edges to remove using {attack_strategy} strategy"
            )

            # Step 1: Use pre-computed deletion order (much faster!)
            if (
                attack_strategy in precomputed_deletions
                and precomputed_deletions[attack_strategy]
            ):
                deletion_order = precomputed_deletions[attack_strategy]
                # Take only the first num_edges_removed edges from the pre-computed order
                edges_to_remove = deletion_order[:num_edges_removed]
                edges_to_remove_set = set(edges_to_remove)
                print(
                    f"Debug: Using pre-computed order - removing {len(edges_to_remove)} edges"
                )

                # Assertion to ensure consistency between slider value and actual edges shown
                assert len(edges_to_remove) == min(
                    num_edges_removed, len(deletion_order)
                ), (
                    f"Inconsistency detected: Slider value ({num_edges_removed}) doesn't match edges to remove ({len(edges_to_remove)}). "
                    f"Available deletion order has {len(deletion_order)} edges."
                )
            else:
                print(
                    f"Debug: No pre-computed order available for {attack_strategy}, skipping removal"
                )
                edges_to_remove = []
                edges_to_remove_set = set()

                # Assertion to ensure when no deletion order is available, we show 0 edges removed
                assert len(edges_to_remove) == 0, (
                    f"Inconsistency detected: No deletion order available but {len(edges_to_remove)} edges marked for removal."
                )

            # Step 2: Vectorized edge filtering (much faster!)
            # Create normalized edge pairs for comparison
            edges_data_copy = edges_data.copy()
            edges_data_copy["edge_key"] = edges_data_copy.apply(
                lambda row: (
                    min(int(row["source"]), int(row["target"])),
                    max(int(row["source"]), int(row["target"])),
                ),
                axis=1,
            )

            # Calculate connected components after edge removal for coloring using igraph
            # Create network copy and remove edges
            current_network = network.copy()
            if edges_to_remove:
                # Remove edges from the network copy
                edges_to_remove_list = [(u, v) for u, v in edges_to_remove]
                try:
                    current_network.delete_edges(edges_to_remove_list)
                except:
                    pass  # Some edges might not exist

            # Use igraph's connected components (no scipy needed!)
            components = current_network.connected_components()
            n_components = len(components)

            # Find the largest component (main network) - must have more than 1 node
            largest_component_id = -1  # No main component by default
            largest_size = 0
            for comp_id, component in enumerate(components):
                if (
                    len(component) > largest_size and len(component) > 1
                ):  # Must be more than isolated node
                    largest_size = len(component)
                    largest_component_id = comp_id

            # Create component labels array - only label the largest component
            component_labels = [
                -1
            ] * current_network.vcount()  # -1 = not main component
            for comp_id, component in enumerate(components):
                label = (
                    0 if comp_id == largest_component_id else -1
                )  # 0=largest, -1=not main
                for node in component:
                    component_labels[node] = label

            # Define colors: light red for main component only
            component_colors = ["#ff6b6b"]  # Only main component gets color

            print(
                f"🔗 Found {n_components} connected components after removing {len(edges_to_remove)} edges"
            )
            if largest_component_id >= 0:
                print(
                    f"   Main component: {largest_size} nodes, Other fragments: {n_components - 1}"
                )
                print(f"   Debug: Main component ID: {largest_component_id}")
            else:
                print(
                    f"   No main component found - network fully fragmented into isolated nodes/small fragments"
                )
                print(
                    f"   Debug: All components are isolated nodes or very small fragments"
                )

            # Filter out edges to remove using vectorized operations
            survived_edges_df = edges_data_copy[
                ~edges_data_copy["edge_key"].isin(edges_to_remove_set)
            ]

            # Step 3: Optimized edge visualization data preparation with component coloring
            edge_viz_data = []
            if not survived_edges_df.empty:
                edges_to_show = survived_edges_df

                # Create node coordinate lookup dictionary for O(1) access
                node_coords = nodes_data.set_index("nodeID")[
                    ["longitude", "latitude"]
                ].to_dict("index")

                # Vectorized coordinate assignment with performance limit and component coloring
                for _, row in edges_to_show.iterrows():
                    source_id = int(row["source"])
                    target_id = int(row["target"])

                    if source_id in node_coords and target_id in node_coords:
                        # Assign edge to the same component as its source node (or target if source not in components)
                        edge_component = (
                            component_labels[source_id]
                            if source_id < len(component_labels)
                            else (
                                component_labels[target_id]
                                if target_id < len(component_labels)
                                else -1
                            )
                        )
                        # Safe edge color assignment
                        try:
                            edge_color = (
                                component_colors[0]
                                if (
                                    edge_component == 0
                                    and len(component_colors) > 0
                                )
                                else "#cccccc"
                            )
                        except Exception as e:
                            print(f"   Debug: Edge color assignment error: {e}")
                            edge_color = "#cccccc"

                        edge_viz_data.append(
                            {
                                "source_lon": float(
                                    node_coords[source_id]["longitude"]
                                ),
                                "source_lat": float(
                                    node_coords[source_id]["latitude"]
                                ),
                                "target_lon": float(
                                    node_coords[target_id]["longitude"]
                                ),
                                "target_lat": float(
                                    node_coords[target_id]["latitude"]
                                ),
                                "component": edge_component,
                                "color": edge_color,
                            }
                        )

                if len(survived_edges_df) > 200:
                    print(
                        f"⚡ Performance mode: Showing 200 of {len(survived_edges_df)} remaining edges"
                    )

            edges_viz_df = pd.DataFrame(edge_viz_data)

            # Prepare node data with component colors
            degrees = network.degree()  # Use original degrees for sizing
            nodes_data_copy = nodes_data.copy()
            nodes_data_copy["degree"] = nodes_data_copy["nodeID"].apply(
                lambda x: degrees[x] if x < len(degrees) else 0
            )
            nodes_data_copy["component"] = nodes_data_copy["nodeID"].apply(
                lambda x: component_labels[x] if x < len(component_labels) else -1
            )

            # Safe color assignment with error handling
            def assign_color(component_id):
                try:
                    if component_id == 0 and len(component_colors) > 0:
                        return component_colors[0]  # Red for main component
                    else:
                        return "#cccccc"  # Gray for others
                except Exception as e:
                    print(
                        f"   Debug: Color assignment error for component {component_id}: {e}"
                    )
                    return "#cccccc"

            nodes_data_copy["color"] = nodes_data_copy["component"].apply(
                assign_color
            )

            # Debug: Check component distribution
            component_counts = nodes_data_copy["component"].value_counts()
            print(f"   Debug: Component distribution: {dict(component_counts)}")
            print(
                f"   Debug: Sample color assignments: {list(nodes_data_copy[['component', 'color']].head(10).values)}"
            )

            # Add human-readable component type for tooltips
            nodes_data_copy["component_type"] = nodes_data_copy["component"].apply(
                lambda x: "Main Component" if x == 0 else "Disconnected"
            )

            nodes_viz_df = nodes_data_copy[
                nodes_data_copy["nodeID"] < len(degrees)
            ][
                [
                    "nodeID",
                    "nodeLabel",
                    "longitude",
                    "latitude",
                    "degree",
                    "component",
                    "color",
                    "component_type",
                ]
            ].rename(columns={"nodeLabel": "station_name"})

            # Debug: Check data content
            print(f"Debug: Edge viz data rows: {len(edge_viz_data)}")
            print(f"Debug: Node viz data rows: {len(nodes_viz_df)}")
            print(f"Debug: Edges viz df shape: {edges_viz_df.shape}")
            print(f"Debug: Nodes viz df shape: {nodes_viz_df.shape}")
            if not nodes_viz_df.empty:
                print(
                    f"Debug: Longitude range: {nodes_viz_df['longitude'].min()} to {nodes_viz_df['longitude'].max()}"
                )
                print(
                    f"Debug: Latitude range: {nodes_viz_df['latitude'].min()} to {nodes_viz_df['latitude'].max()}"
                )

            # Get data ranges for scaling
            if not nodes_viz_df.empty:
                lon_min, lon_max = (
                    nodes_viz_df["longitude"].min(),
                    nodes_viz_df["longitude"].max(),
                )
                lat_min, lat_max = (
                    nodes_viz_df["latitude"].min(),
                    nodes_viz_df["latitude"].max(),
                )
            else:
                # Fallback to London bounds if no data
                lon_min, lon_max = -0.5, 0.2
                lat_min, lat_max = 51.3, 51.7

            # Calculate chart dimensions
            lon_range = lon_max - lon_min
            lat_range = lat_max - lat_min
            aspect_ratio = (lon_range * 0.7) / lat_range
            chart_height = 600
            chart_width = int(chart_height * aspect_ratio)

            # Create simple, fast background with proper dimensions
            background = create_simple_background(
                lon_min, lon_max, lat_min, lat_max, chart_width, chart_height
            )

            # Step 4: Create network layers with geographic projection and component coloring
            # Plot survived edges colored by their connected component
            if not edges_viz_df.empty:
                edges_layer = (
                    alt.Chart(edges_viz_df)
                    .mark_rule(opacity=0.6, strokeWidth=2)
                    .encode(
                        longitude="source_lon:Q",
                        latitude="source_lat:Q",
                        longitude2="target_lon:Q",
                        latitude2="target_lat:Q",
                        color=alt.Color(
                            "color:N",
                            scale=None,  # Use the exact colors we specified
                            legend=None,  # Hide edge legend since nodes already show it
                        ),
                        tooltip=["component:O"],
                    )
                )
            else:
                # Empty layer if no edges
                edges_layer = alt.Chart(pd.DataFrame()).mark_point()

            # Create nodes layer - colored by connected component
            if not nodes_viz_df.empty:
                nodes_layer = (
                    alt.Chart(nodes_viz_df)
                    .mark_circle(
                        stroke="black",
                        strokeWidth=1,
                        opacity=0.9,
                        size=60,
                    )
                    .encode(
                        longitude="longitude:Q",
                        latitude="latitude:Q",
                        color=alt.Color(
                            "color:N",
                            scale=None,  # Use the exact colors we specified
                            legend=alt.Legend(
                                title="Network Status",
                                labelExpr="datum.label == '#ff6b6b' ? 'Main Component' : 'Disconnected'",
                                symbolType="circle",
                                symbolSize=100,
                            ),
                        ),
                        tooltip=[
                            "station_name:N",
                            "degree:Q",
                            "component_type:N",
                        ],  # Show station name, degree, and component type
                    )
                )
            else:
                # Empty layer if no nodes
                nodes_layer = alt.Chart(pd.DataFrame()).mark_point()

            # Simple layering without interactive zoom to avoid selection conflicts

            # Step 5: Combine layers - simplified for performance
            network_name = "London Transport Network"
            chart = (
                (background + edges_layer + nodes_layer)
                .resolve_scale(color="independent", size="independent")
                .properties(
                    title=f"{network_name} - {len(edges_to_remove)} edges removed (Connectivity: {current_connectivity:.3f})",
                    width=chart_width,
                    height=chart_height,
                )
            )
            chart = mo.ui.altair_chart(chart)

            # Final assertion to ensure the visualization title displays the expected number of edges
            expected_edges_removed = min(
                num_edges_removed,
                len(deletion_order)
                if attack_strategy in precomputed_deletions
                and precomputed_deletions[attack_strategy]
                else 0,
            )
            assert len(edges_to_remove) == expected_edges_removed, (
                f"Final consistency check failed: Title will show {len(edges_to_remove)} edges removed, but expected {expected_edges_removed} based on slider value {num_edges_removed}."
            )
            print(
                f"✅ Consistency check passed: Slider value ({num_edges_removed}) matches visualization ({len(edges_to_remove)} edges removed)"
            )

            # Performance timing
            end_time = time.time()
            print(
                f"🚀 Visualization rendered in {end_time - start_time:.3f} seconds"
            )

            return chart

        except Exception as e:
            print(f"Debug: Exception in geographic visualization: {e}")
            import traceback

            traceback.print_exc()

            # Fallback: Create a simple chart showing the error and basic info
            return mo.md(f"""
            ❌ Error creating geographic visualization: {e}

            **Debugging Info:**
            - Network nodes: {network.vcount() if network else "None"}
            - Network edges: {network.ecount() if network else "None"}
            - Nodes data: {len(nodes_data) if nodes_data is not None else "None"}
            - Edges data: {len(edges_data) if edges_data is not None else "None"}
            """)


    # ====================================================================================
    # VISUALIZATION FUNCTION CALL
    # ====================================================================================
    # This section calls the visualization function defined above and displays the result

    # Create and display the visualization using the geographic visualization function
    if (
        london_network is not None
        and nodes_df is not None
        and edges_df is not None
    ):
        # Use the slider values directly for visualization
        network_chart = create_interactive_geographic_visualization(
            test_network,
            nodes_df,
            edges_df,
            strategy_selector.value,  # Use selected attack strategy
            edges_removed_slider.value,  # Use slider value directly
        )
    else:
        mo.md(
            "❌ London Transport network data not available for geographic visualization"
        )
    return (network_chart,)


@app.cell(hide_code=True)
def _(alt, data, edges_df, london_network, mo, nodes_df, pd):
    # Create geographic visualization of London Transport network
    def create_geographic_network_visualization(network, nodes_data, edges_data):
        """Create a geographic visualization using station coordinates with London geography"""

        if network is None or nodes_data is None or edges_data is None:
            return mo.md(
                "❌ Network data not available for geographic visualization"
            )

        try:
            # Prepare node data for visualization
            node_viz_data = []
            degrees = network.degree()

            for i, row in nodes_data.iterrows():
                node_id = int(row["nodeID"])  # Ensure integer for list indexing
                if node_id < len(degrees):  # Make sure node exists in network
                    node_viz_data.append(
                        {
                            "nodeID": node_id,
                            "longitude": float(row["longitude"]),
                            "latitude": float(row["latitude"]),
                            "degree": degrees[node_id],
                            "node_size": min(
                                degrees[node_id] * 3 + 5, 50
                            ),  # Scale node size by degree
                        }
                    )

            nodes_viz_df = pd.DataFrame(node_viz_data)

            # Prepare edge data for visualization
            edge_viz_data = []
            for _, row in edges_data.iterrows():
                source_id = int(row["source"])
                target_id = int(row["target"])

                # Get coordinates for source and target nodes
                source_node = nodes_data[nodes_data["nodeID"] == source_id]
                target_node = nodes_data[nodes_data["nodeID"] == target_id]

                if len(source_node) > 0 and len(target_node) > 0:
                    edge_viz_data.append(
                        {
                            "source": source_id,
                            "target": target_id,
                            "source_lon": source_node.iloc[0]["longitude"],
                            "source_lat": source_node.iloc[0]["latitude"],
                            "target_lon": target_node.iloc[0]["longitude"],
                            "target_lat": target_node.iloc[0]["latitude"],
                        }
                    )

            edges_viz_df = pd.DataFrame(edge_viz_data)

            # Get data ranges for proper scaling - MOVE THIS UP
            lon_min, lon_max = (
                nodes_viz_df["longitude"].min(),
                nodes_viz_df["longitude"].max(),
            )
            lat_min, lat_max = (
                nodes_viz_df["latitude"].min(),
                nodes_viz_df["latitude"].max(),
            )

            # Calculate proper aspect ratio for London coordinates
            lon_range = lon_max - lon_min
            lat_range = lat_max - lat_min

            # For London's latitude (~51.5°), 1 degree longitude ≈ 0.7 * 1 degree latitude in distance
            aspect_ratio = (lon_range * 0.7) / lat_range
            chart_height = 500  # Reduced height to fit screen better
            chart_width = int(chart_height * aspect_ratio)

            # Create London geography background layers
            boroughs = alt.topo_feature(data.londonBoroughs.url, "boroughs")
            tubelines = alt.topo_feature(data.londonTubeLines.url, "line")
            centroids = data.londonCentroids.url

            # Borough boundaries background - make more visible
            background = (
                alt.Chart(boroughs)
                .mark_geoshape(
                    stroke="darkgray", strokeWidth=1, fill="lightgray", opacity=0.8
                )
                .project(type="identity", reflectY=True)
                .properties(width=chart_width, height=chart_height)
            )

            # Borough labels (optional, can be commented out if too cluttered)
            borough_labels = (
                alt.Chart(centroids)
                .mark_text(
                    fontSize=10, opacity=0.6, color="black", fontWeight="bold"
                )
                .encode(longitude="cx:Q", latitude="cy:Q", text="bLabel:N")
                .transform_calculate(
                    "bLabel",
                    "indexof(datum.name,' ') > 0 ? substring(datum.name,0,indexof(datum.name, ' ')) : datum.name",
                )
            )

            # Create edges layer - simplified approach
            edge_lines = []
            for _, row in edges_viz_df.iterrows():
                edge_lines.extend(
                    [
                        {
                            "x": row["source_lon"],
                            "y": row["source_lat"],
                            "group": row["source"],
                        },
                        {
                            "x": row["target_lon"],
                            "y": row["target_lat"],
                            "group": row["source"],
                        },
                        {
                            "x": None,
                            "y": None,
                            "group": row["source"],
                        },  # Break line
                    ]
                )

            edge_lines_df = pd.DataFrame(edge_lines)

            edges_layer = (
                alt.Chart(edge_lines_df)
                .mark_line(color="lightblue", opacity=0.4, strokeWidth=1)
                .encode(
                    x=alt.X("x:Q", title="Longitude"),
                    y=alt.Y("y:Q", title="Latitude"),
                    detail="group:N",
                )
            )

            # Create nodes layer
            nodes_layer = (
                alt.Chart(nodes_viz_df)
                .mark_circle(stroke="black", strokeWidth=2)
                .encode(
                    x=alt.X(
                        "longitude:Q",
                        title="Longitude",
                        axis=alt.Axis(grid=False, tickCount=5),
                        scale=alt.Scale(domain=[lon_min - 0.01, lon_max + 0.01]),
                    ),
                    y=alt.Y(
                        "latitude:Q",
                        title="Latitude",
                        axis=alt.Axis(grid=False, tickCount=5),
                        scale=alt.Scale(domain=[lat_min - 0.01, lat_max + 0.01]),
                    ),
                    size=alt.Size(
                        "degree:Q",
                        scale=alt.Scale(range=[50, 400]),
                        legend=alt.Legend(title="Station Degree"),
                    ),
                    color=alt.Color(
                        "degree:Q",
                        scale=alt.Scale(scheme="plasma"),
                        legend=alt.Legend(title="Connections"),
                    ),
                    tooltip=["nodeID:N", "degree:Q", "latitude:Q", "longitude:Q"],
                )
            )

            # Update edges layer with same scaling
            edges_layer = (
                alt.Chart(edge_lines_df)
                .mark_line(color="red", opacity=0.7, strokeWidth=2)
                .encode(
                    x=alt.X(
                        "x:Q",
                        title="Longitude",
                        axis=alt.Axis(grid=False, tickCount=5),
                        scale=alt.Scale(domain=[lon_min - 0.01, lon_max + 0.01]),
                    ),
                    y=alt.Y(
                        "y:Q",
                        title="Latitude",
                        axis=alt.Axis(grid=False, tickCount=5),
                        scale=alt.Scale(domain=[lat_min - 0.01, lat_max + 0.01]),
                    ),
                    detail="group:N",
                )
            )

            # Add official tube lines for context (more visible)
            official_lines = (
                alt.Chart(tubelines)
                .mark_geoshape(
                    filled=False, strokeWidth=1, opacity=0.6, stroke="#888888"
                )
                .project(type="identity", reflectY=True)
                .properties(width=chart_width, height=chart_height)
            )

            # Create interactive selection for zoom and pan
            zoom = alt.selection_interval(bind="scales")

            # Apply zoom to all layers
            background = background.add_params(zoom)
            official_lines = official_lines.add_params(zoom)
            edges_layer = edges_layer.add_params(zoom)
            nodes_layer = nodes_layer.add_params(zoom)
            borough_labels = borough_labels.add_params(zoom)

            # Combine all layers: background + official lines + our network + nodes
            chart = (
                (
                    background
                    + official_lines
                    + edges_layer
                    + nodes_layer
                    + borough_labels
                )
                .resolve_scale(color="independent", size="independent")
                .properties(
                    width=chart_width,
                    height=chart_height,
                    title="London Transport Network - Interactive Geographic Map (Use mouse to zoom and pan)",
                )
            )

            return chart

        except Exception as e:
            return mo.md(f"❌ Error creating geographic visualization: {e}")


    # Create the visualization
    geographic_viz = create_geographic_network_visualization(
        london_network, nodes_df, edges_df
    )
    geographic_viz
    return


if __name__ == "__main__":
    app.run()
