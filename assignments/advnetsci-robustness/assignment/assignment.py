# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "python-igraph==0.11.9",
#     "pyarrow",
#     "openai==1.99.5",
# ]
# ///

import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Network Robustness Assignment

    Welcome to the Network Robustness assignment! You'll learn about network resilience through hands-on implementation and develop strategies to attack real-world networks.

    Network robustness focuses on two key aspects:

    - **Random failures**: How networks behave when nodes fail randomly (equipment failures, random errors)
    - **Targeted attacks**: How networks respond to deliberate attacks on critical nodes (cyber attacks, strategic disruptions)

    This assignment will guide you through implementing robustness metrics and developing your own attack strategy to break networks more effectively than standard degree-based attacks.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Understanding Network Robustness

    Network robustness measures how well a network maintains connectivity when nodes or edges are removed. Key concepts include:

    1. **Connectivity**: Fraction of nodes in the largest connected component
    2. **Random attacks**: Simulating random failures in infrastructure
    3. **Targeted attacks**: Strategic removal of important nodes
    4. **Critical threshold**: Point at which network fragments

    Real-world applications span transportation networks, power grids, social networks, and the internet.

    ---

    # 📋 Assignment Instructions & Grading
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "📋 Assignment Tasks": mo.md(
                r"""
            Complete the following tasks and upload your notebook to your GitHub repository.

            1. **Task 1**: Implement `simulate_random_attack(graph)` - Simulate random node removal and measure connectivity decline
            2. **Task 2**: Implement `simulate_targeted_attack(graph, criterion)` - Implement degree-based targeted attack
            3. **Task 3**: Implement `simulate_custom_attack(graph)` - Design your own attack strategy that breaks the airport network faster than degree-based attack
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
    ## Task 1: Random Attack Simulation

    Implement a function that simulates **random node removal** from a network. This models random failures in infrastructure networks.

    Your function should:
    - Remove nodes randomly one by one
    - Calculate connectivity after each removal (fraction of nodes in largest component)
    - Return a DataFrame with columns: `frac_nodes_removed`, `connectivity`

    **Connectivity** = (Size of largest connected component) / (Original network size)
    """
    )
    return


@app.function
# Task 1
def simulate_random_attack(graph):
    """
    Simulate random node removal and measure connectivity decline.
    
    Args:
        graph (igraph.Graph): Input graph
        
    Returns:
        pd.DataFrame: DataFrame with columns 'frac_nodes_removed' and 'connectivity'
    """
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 2: Targeted Attack Simulation

    Implement a function that simulates **targeted attacks** based on node properties. The degree-based attack removes nodes with the highest degree first.

    Your function should:
    - Support different attack criteria (focus on "degree" for this task)
    - Remove the node with highest degree, then second highest, etc.
    - Calculate connectivity after each removal
    - Return a DataFrame with the same format as Task 1

    **Hint**: Use `graph.degree()` to get node degrees, and `np.argmax()` to find the node with maximum degree.
    """
    )
    return


@app.function
# Task 2
def simulate_targeted_attack(graph, criterion="degree"):
    """
    Simulate targeted node removal based on specified criterion.
    
    Args:
        graph (igraph.Graph): Input graph
        criterion (str): Attack criterion ("degree", "betweenness", etc.)
        
    Returns:
        pd.DataFrame: DataFrame with columns 'frac_nodes_removed' and 'connectivity'
    """
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3: Custom Attack Strategy

    **This is the main challenge!** Design your own attack strategy that breaks the airport network faster than the standard degree-based attack.

    ### Your Mission:
    Develop a custom attack that makes connectivity drop more rapidly than removing nodes by degree alone.

    ### Ideas to Consider:
    - **Betweenness centrality**: Nodes that lie on many shortest paths
    - **Closeness centrality**: Nodes with short distances to all other nodes  
    - **PageRank**: Nodes with high influence (like Google's algorithm)
    - **Hybrid strategies**: Combine multiple metrics
    - **Community-based**: Target nodes that connect different parts of the network
    - **Your own creative approach**: Think outside the box!

    ### Success Criteria:
    Your attack should make the airport network's connectivity drop below 0.5 using **fewer node removals** than the degree-based attack.

    ### Research Tips:
    Look up different centrality measures in igraph documentation:
    - `graph.betweenness()` 
    - `graph.closeness()`
    - `graph.pagerank()`
    - `graph.eigenvector_centrality()`
    """
    )
    return


@app.function
# Task 3 - Your custom attack strategy
def simulate_custom_attack(graph):
    """
    Implement your custom attack strategy to break networks faster than degree-based attack.
    
    Args:
        graph (igraph.Graph): Input graph
        
    Returns:
        pd.DataFrame: DataFrame with columns 'frac_nodes_removed' and 'connectivity'
        
    Note: Describe your strategy in the docstring!
    Strategy description: [TODO: Describe your approach here]
    """
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## Interactive Analysis: Airport Network Robustness

    Now let's test your implementations on the real-world airport network! This network represents global air transportation where nodes are airports and edges are flight routes.

    The visualization below shows how different attack strategies affect network connectivity. Your custom attack should outperform the degree-based attack!
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Attack strategy selector
    strategy_selector = mo.ui.dropdown(
        options=["random", "degree", "custom"], 
        value="degree",
        label="Attack Strategy"
    )
    strategy_selector
    return (strategy_selector,)


@app.cell(hide_code=True)
def _(attack_comparison_chart):
    attack_comparison_chart
    return


@app.cell(hide_code=True)
def _(mo, network_stats_chart, robustness_chart):
    mo.hstack(
        [robustness_chart, network_stats_chart],
        justify="center",
        align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Understanding the Results

    The interactive plots above show:

    1. **Attack Comparison**: Head-to-head comparison of all three strategies
    2. **Robustness Profile**: Detailed view of connectivity decline for selected strategy  
    3. **Network Statistics**: Key metrics of the airport network

    ### Success Metrics:
    - **Speed**: How quickly does connectivity drop to 50%?
    - **Effectiveness**: What's the steepest decline in connectivity?
    - **Critical threshold**: At what removal fraction does the network fragment?

    ### Analyzing Your Strategy:
    - Does your custom attack outperform degree-based attack?
    - What makes your strategy effective?
    - How does it compare to random failures?

    **Goal**: Your custom attack should reach 50% connectivity with fewer node removals than the degree-based attack!
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Libraries""")
    return


@app.cell
def _():
    # All imports in one place to avoid conflicts
    import numpy as np
    import igraph
    import altair as alt
    import pandas as pd
    return alt, igraph, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Code""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Load Airport Network""")
    return


@app.cell(hide_code=True)
def _(igraph, np, pd):
    # Load and process airport network data
    def load_airport_network():
        """Load the airport network from online data"""
        try:
            # Load airport network data
            df_airports = pd.read_csv(
                "https://raw.githubusercontent.com/skojaku/core-periphery-detection/master/data/edge-table-airport.csv"
            )
            
            # Process edge data to create consecutive node IDs
            edges = df_airports[["source", "target"]].to_numpy()
            edges = np.unique(edges.reshape(-1), return_inverse=True)[1]
            edges = edges.reshape(-1, 2)
            
            # Create network
            g_airports = igraph.Graph()
            g_airports.add_vertices(np.max(edges) + 1)
            g_airports.add_edges([tuple(edge) for edge in edges])
            
            return g_airports
            
        except Exception as e:
            print(f"Error loading airport network: {e}")
            # Create a small test network if loading fails
            g = igraph.Graph.Erdos_Renyi(100, 0.05)
            return g.connected_components().giant()

    # Load the airport network
    airport_network = load_airport_network()
    print(f"Airport network: {airport_network.vcount()} nodes, {airport_network.ecount()} edges")
    return (airport_network,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Network Utility Functions""")
    return


@app.cell(hide_code=True)
def _():
    def network_connectivity(graph, original_size=None):
        """Calculate network connectivity as fraction of nodes in largest component"""
        if original_size is None:
            original_size = graph.vcount()
        
        if graph.vcount() == 0:
            return 0.0
        
        components = graph.connected_components()
        return max(components.sizes()) / original_size if components.sizes() else 0.0
    
    
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
def _(airport_network, pd):
    # Run all attack simulations
    def run_all_attacks(graph):
        """Run all attack simulations and return results"""
        results = {}
        
        try:
            # Random attack
            results["random"] = simulate_random_attack(graph.copy())
            if results["random"] is None:
                results["random"] = pd.DataFrame({"frac_nodes_removed": [0], "connectivity": [1]})
        except:
            results["random"] = pd.DataFrame({"frac_nodes_removed": [0], "connectivity": [1]})
            
        try:
            # Degree-based targeted attack
            results["degree"] = simulate_targeted_attack(graph.copy(), "degree")
            if results["degree"] is None:
                results["degree"] = pd.DataFrame({"frac_nodes_removed": [0], "connectivity": [1]})
        except:
            results["degree"] = pd.DataFrame({"frac_nodes_removed": [0], "connectivity": [1]})
            
        try:
            # Custom attack
            results["custom"] = simulate_custom_attack(graph.copy())
            if results["custom"] is None:
                results["custom"] = pd.DataFrame({"frac_nodes_removed": [0], "connectivity": [1]})
        except:
            results["custom"] = pd.DataFrame({"frac_nodes_removed": [0], "connectivity": [1]})
        
        return results
    
    # Run simulations on a subset for performance (use first 500 nodes if network is large)
    if airport_network.vcount() > 500:
        # Get the largest connected component of first 500 nodes
        subgraph_nodes = list(range(min(500, airport_network.vcount())))
        test_network = airport_network.subgraph(subgraph_nodes).connected_components().giant()
    else:
        test_network = airport_network
    
    attack_results = run_all_attacks(test_network)
    network_stats = calculate_network_stats(test_network)
    
    print(f"Test network: {test_network.vcount()} nodes, {test_network.ecount()} edges")
    return attack_results, network_stats, test_network


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Robustness Chart""")
    return


@app.cell(hide_code=True)
def _(alt, attack_results, strategy_selector):
    # Create robustness profile chart for selected strategy
    def create_robustness_chart(results, selected_strategy):
        if selected_strategy not in results or len(results[selected_strategy]) == 0:
            return alt.Chart().mark_text(
                text="Please implement the required functions to see visualization",
                fontSize=14
            ).properties(width=400, height=300)
        
        data = results[selected_strategy].copy()
        data["strategy"] = selected_strategy
        
        # Color mapping
        color_map = {"random": "blue", "degree": "red", "custom": "orange"}
        color = color_map.get(selected_strategy, "gray")
        
        chart = (
            alt.Chart(data)
            .mark_line(strokeWidth=3, color=color)
            .encode(
                x=alt.X("frac_nodes_removed:Q", 
                       title="Fraction of Nodes Removed",
                       scale=alt.Scale(domain=[0, 1])),
                y=alt.Y("connectivity:Q", 
                       title="Network Connectivity",
                       scale=alt.Scale(domain=[0, 1])),
            )
        )
        
        # Add points
        points = (
            alt.Chart(data)
            .mark_circle(size=60, color=color, opacity=0.7)
            .encode(
                x=alt.X("frac_nodes_removed:Q"),
                y=alt.Y("connectivity:Q"),
            )
        )
        
        # Add reference lines
        reference_lines = alt.Chart(pd.DataFrame({"y": [0.5]})).mark_rule(
            color="gray", strokeDash=[5, 5], opacity=0.7
        ).encode(y=alt.Y("y:Q"))
        
        return (
            (chart + points + reference_lines)
            .properties(
                width=400,
                height=300,
                title=f"{selected_strategy.title()} Attack Strategy"
            )
        )
    
    robustness_chart = create_robustness_chart(attack_results, strategy_selector.value)
    return (robustness_chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Attack Comparison Chart""")
    return


@app.cell(hide_code=True)
def _(alt, attack_results, pd):
    # Create comparison chart of all attack strategies
    def create_comparison_chart(results):
        # Combine all results
        combined_data = []
        color_map = {"random": "blue", "degree": "red", "custom": "orange"}
        
        for strategy, data in results.items():
            if len(data) > 0:
                temp_data = data.copy()
                temp_data["strategy"] = strategy
                combined_data.append(temp_data)
        
        if not combined_data:
            return alt.Chart().mark_text(
                text="Please implement the required functions to see comparison",
                fontSize=14
            ).properties(width=600, height=400)
        
        comparison_df = pd.concat(combined_data, ignore_index=True)
        
        # Main chart
        lines = (
            alt.Chart(comparison_df)
            .mark_line(strokeWidth=3)
            .encode(
                x=alt.X("frac_nodes_removed:Q", 
                       title="Fraction of Nodes Removed",
                       scale=alt.Scale(domain=[0, 1])),
                y=alt.Y("connectivity:Q", 
                       title="Network Connectivity",
                       scale=alt.Scale(domain=[0, 1])),
                color=alt.Color("strategy:N", 
                               scale=alt.Scale(
                                   domain=["random", "degree", "custom"],
                                   range=["blue", "red", "orange"]
                               ),
                               legend=alt.Legend(title="Attack Strategy")),
            )
        )
        
        # Add reference line at 50% connectivity
        reference_line = alt.Chart(pd.DataFrame({"y": [0.5]})).mark_rule(
            color="gray", strokeDash=[5, 5], opacity=0.7
        ).encode(y=alt.Y("y:Q"))
        
        # Add text annotation
        annotation = alt.Chart(pd.DataFrame({"x": [0.02], "y": [0.52], "text": ["50% threshold"]})).mark_text(
            align="left", fontSize=10, color="gray"
        ).encode(x="x:Q", y="y:Q", text="text:N")
        
        return (
            (lines + reference_line + annotation)
            .properties(
                width=600,
                height=400,
                title="Attack Strategy Comparison: Airport Network"
            )
        )
    
    attack_comparison_chart = create_comparison_chart(attack_results)
    return (attack_comparison_chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Create Network Statistics Chart""")
    return


@app.cell(hide_code=True)
def _(alt, network_stats, pd):
    # Create network statistics visualization
    def create_stats_chart(stats):
        stats_data = pd.DataFrame([
            {"metric": "Nodes", "value": stats["nodes"]},
            {"metric": "Edges", "value": stats["edges"]}, 
            {"metric": "Avg Degree", "value": round(stats["avg_degree"], 2)},
            {"metric": "Max Degree", "value": stats["max_degree"]},
            {"metric": "Density", "value": round(stats["density"], 4)}
        ])
        
        chart = (
            alt.Chart(stats_data)
            .mark_bar(color="steelblue")
            .encode(
                x=alt.X("value:Q", title="Value"),
                y=alt.Y("metric:N", title="Network Metric", sort=None),
                tooltip=["metric:N", "value:Q"]
            )
            .properties(
                width=300,
                height=250,
                title="Airport Network Statistics"
            )
        )
        
        return chart
    
    network_stats_chart = create_stats_chart(network_stats)
    return (network_stats_chart,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()