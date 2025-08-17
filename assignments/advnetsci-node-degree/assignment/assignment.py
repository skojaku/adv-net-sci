import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full", theme="dark")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Node Degree and the Friendship Paradox Assignment

    Welcome to the Node Degree assignment! In this assignment, you'll implement key functions for analyzing degree distributions and demonstrating the friendship paradox in networks.

    You'll learn to:
    - Compute degree distributions and their statistical properties
    - Implement the friendship paradox sampling mechanism
    - Visualize heavy-tailed distributions using proper techniques
    - Calculate key network statistics related to degree heterogeneity
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
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

            1. **Task 1**: Implement degree distribution calculation
            2. **Task 2**: Compute friendship paradox statistics  
            3. **Task 3**: Calculate CCDF for visualization
            4. **Task 4**: Implement degree-biased sampling
            5. Update this notebook by using `git add`, `git commit`, and then `git push`.
            6. The notebook will be automatically graded, and your score will be shown on GitHub.
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
            You **cannot** import any other libraries that result in the grading script failing or a zero score. Only use: `numpy`, `igraph`, `pandas`, `matplotlib`, `seaborn`, `scipy`
            """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 1: Degree Distribution

    Implement a function to compute the degree distribution of a network. The degree distribution p(k) represents the fraction of nodes with degree k.
    
    **Key concepts:**
    - Degree sequence: list of all node degrees
    - Probability mass function: P(k) = (number of nodes with degree k) / (total number of nodes)
    - Handle networks with isolated nodes (degree 0)
    """
    )
    return


@app.function
def compute_degree_distribution(g):
    """
    Compute the degree distribution of a graph.
    
    Args:
        g (igraph.Graph): Input graph
        
    Returns:
        numpy.ndarray: Degree distribution where index k represents degree k
                      and value represents P(k) = fraction of nodes with degree k
                      
    Example:
        For a graph with degrees [1, 1, 2, 2, 3]:
        Returns array [0.0, 0.4, 0.4, 0.2] representing:
        - P(0) = 0.0 (no nodes with degree 0)
        - P(1) = 0.4 (2 out of 5 nodes have degree 1)  
        - P(2) = 0.4 (2 out of 5 nodes have degree 2)
        - P(3) = 0.2 (1 out of 5 nodes have degree 3)
    """
    # TODO: Implement this function
    # Hint: Use g.degree() to get degree sequence, np.bincount() to count occurrences
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 2: Friendship Paradox Statistics

    Implement a function to compute key statistics that demonstrate the friendship paradox. Your function should return the average degree of nodes and the average degree of their friends.
    
    **Key concepts:**
    - Average node degree: mean of all node degrees
    - Average friend degree: average degree when sampling through edges (degree-biased)
    - Friendship paradox: friends have higher average degree than nodes
    """
    )
    return


@app.function
def compute_friendship_paradox_stats(g):
    """
    Compute statistics demonstrating the friendship paradox.
    
    Args:
        g (igraph.Graph): Input graph
        
    Returns:
        tuple: (avg_node_degree, avg_friend_degree)
            - avg_node_degree (float): Average degree across all nodes
            - avg_friend_degree (float): Average degree when sampling friends through edges
            
    Example:
        For a star graph with 1 central node (degree 4) and 4 leaf nodes (degree 1):
        - avg_node_degree = (4 + 1 + 1 + 1 + 1) / 5 = 1.6
        - avg_friend_degree = (4 + 4 + 4 + 4) / 4 = 4.0 (all edges point to center)
    """
    # TODO: Implement this function
    # Hint: For friend degrees, extract edges and sample source node degrees
    # Use g.get_edgelist() or adjacency matrix to get edges
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3: CCDF Calculation

    Implement a function to compute the Complementary Cumulative Distribution Function (CCDF) of a degree distribution. CCDF(k) represents the fraction of nodes with degree greater than k.
    
    **Key concepts:**
    - CCDF(k) = P(degree > k) = sum of P(k') for all k' > k
    - CCDF is monotonically decreasing
    - Better for visualizing heavy-tailed distributions than PDF
    """
    )
    return


@app.function  
def compute_degree_ccdf(degree_dist):
    """
    Compute the Complementary Cumulative Distribution Function (CCDF) of a degree distribution.
    
    Args:
        degree_dist (numpy.ndarray): Degree distribution P(k) where index k is degree
                                   and value is probability
        
    Returns:
        numpy.ndarray: CCDF where index k represents degree k and value represents
                      P(degree > k) = fraction of nodes with degree greater than k
                      
    Example:
        For degree_dist = [0.0, 0.4, 0.4, 0.2] (degrees 0,1,2,3 with probs 0,0.4,0.4,0.2):
        Returns [1.0, 0.6, 0.2, 0.0] representing:
        - CCDF(0) = 1.0 (all nodes have degree > 0, actually 100% have degree >= 1)  
        - CCDF(1) = 0.6 (60% of nodes have degree > 1)
        - CCDF(2) = 0.2 (20% of nodes have degree > 2)
        - CCDF(3) = 0.0 (0% of nodes have degree > 3)
    """
    # TODO: Implement this function
    # Hint: CCDF(k) = 1 - CDF(k), where CDF is cumulative sum
    # Be careful about the indexing and exclusion of the last element
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 4: Degree-Biased Sampling

    Implement a function that performs degree-biased sampling to demonstrate how high-degree nodes are overrepresented when sampling through network connections.
    
    **Key concepts:**
    - Edge-based sampling: sample edges uniformly, then take one endpoint
    - Degree bias: probability of sampling a node ∝ its degree
    - This sampling mechanism underlies the friendship paradox
    """
    )
    return


@app.function
def sample_degree_biased_nodes(g, num_samples):
    """
    Sample nodes with probability proportional to their degree (degree-biased sampling).
    
    Args:
        g (igraph.Graph): Input graph
        num_samples (int): Number of nodes to sample
        
    Returns:
        numpy.ndarray: Array of sampled node indices (may contain duplicates)
        
    Note:
        This function simulates the process of:
        1. Sampling edges uniformly at random
        2. Selecting one endpoint of each sampled edge
        
        High-degree nodes appear as endpoints more frequently, so they're more likely
        to be sampled. This creates the degree bias underlying the friendship paradox.
    """
    # TODO: Implement this function
    # Hint: Get all edges, sample num_samples edges uniformly, return one endpoint from each
    # Use np.random.choice() for sampling
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## Interactive Visualization

    Test your implementations with different network types and see how degree distributions and the friendship paradox vary across network structures.
    """
    )
    return


@app.cell
def _(mo, np, igraph):
    # Create different network types for testing
    def create_test_networks():
        networks = {}
        
        # Barabási-Albert (scale-free)
        networks['Scale-free'] = igraph.Graph.Barabasi(n=1000, m=2)
        
        # Erdős-Rényi (random)
        networks['Random'] = igraph.Graph.Erdos_Renyi(n=1000, p=0.004)
        
        # Watts-Strogatz (small-world)  
        networks['Small-world'] = igraph.Graph.Watts_Strogatz(1, 1000, 4, 0.1)
        
        # Regular lattice
        networks['Regular'] = igraph.Graph.Lattice([50, 20], circular=True)
        
        return networks
    
    test_networks = create_test_networks()
    
    # Network selector
    network_selector = mo.ui.dropdown(
        options=list(test_networks.keys()),
        value='Scale-free',
        label='Select network type:'
    )
    
    mo.vstack([
        mo.md("### Network Analysis Dashboard"),
        network_selector
    ])
    return create_test_networks, network_selector, test_networks


@app.cell
def _(
    compute_degree_ccdf,
    compute_degree_distribution, 
    compute_friendship_paradox_stats,
    mo,
    network_selector,
    np,
    plt,
    sample_degree_biased_nodes,
    test_networks
):
    if network_selector.value:
        # Get selected network
        g = test_networks[network_selector.value]
        
        # Test your implementations
        try:
            # Task 1: Degree distribution
            deg_dist = compute_degree_distribution(g)
            
            # Task 2: Friendship paradox stats
            avg_node_deg, avg_friend_deg = compute_friendship_paradox_stats(g)
            
            # Task 3: CCDF
            ccdf = compute_degree_ccdf(deg_dist)
            
            # Task 4: Degree-biased sampling
            biased_samples = sample_degree_biased_nodes(g, 1000)
            
            # Create visualization
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
            
            # Plot 1: Degree distribution (linear scale)
            degrees = np.arange(len(deg_dist))
            ax1.bar(degrees, deg_dist, alpha=0.7, color='skyblue')
            ax1.set_xlabel('Degree')
            ax1.set_ylabel('Probability P(k)')
            ax1.set_title(f'{network_selector.value} Network: Degree Distribution')
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: CCDF (log-log scale)
            valid_idx = ccdf > 0
            ax2.loglog(degrees[valid_idx], ccdf[valid_idx], 'o-', color='red', markersize=4)
            ax2.set_xlabel('Degree')
            ax2.set_ylabel('CCDF P(k\' > k)')
            ax2.set_title('Degree CCDF (Log-Log Scale)')
            ax2.grid(True, alpha=0.3)
            
            # Plot 3: Friendship paradox comparison
            labels = ['Nodes', 'Friends']
            values = [avg_node_deg, avg_friend_deg]
            colors = ['blue', 'red']
            bars = ax3.bar(labels, values, color=colors, alpha=0.7)
            ax3.set_ylabel('Average Degree')
            ax3.set_title('Friendship Paradox')
            ax3.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(values),
                        f'{value:.2f}', ha='center', va='bottom')
            
            # Plot 4: Degree bias demonstration
            actual_degrees = g.degree()
            biased_degrees = [actual_degrees[i] for i in biased_samples]
            
            ax4.hist(actual_degrees, bins=30, alpha=0.5, label='Uniform sampling', 
                    density=True, color='blue')
            ax4.hist(biased_degrees, bins=30, alpha=0.5, label='Degree-biased sampling',
                    density=True, color='red')
            ax4.set_xlabel('Degree')
            ax4.set_ylabel('Density')
            ax4.set_title('Sampling Bias Comparison')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Display results
            mo.vstack([
                mo.md(f"""
                ### Results for {network_selector.value} Network
                
                **Network Statistics:**
                - Nodes: {g.vcount()}
                - Edges: {g.ecount()}  
                - Average degree: {avg_node_deg:.3f}
                - Average friend degree: {avg_friend_deg:.3f}
                - Friendship paradox ratio: {avg_friend_deg/avg_node_deg:.3f}
                """),
                mo.as_html(fig)
            ])
            
        except Exception as e:
            mo.md(f"**Error**: {str(e)}\n\nMake sure to implement all required functions!")
    else:
        mo.md("Select a network to analyze")
    return (
        avg_friend_deg,
        avg_node_deg,
        ax1,
        ax2,
        ax3,
        ax4,
        bars,
        biased_degrees,
        biased_samples,
        ccdf,
        colors,
        deg_dist,
        degrees,
        fig,
        g,
        labels,
        valid_idx,
        values,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Understanding the Results

    Reflect on the visualizations and answer these questions:

    1. **Degree Distribution Shape**: How does the degree distribution shape differ between network types? Which networks show heavy tails?

    2. **CCDF Slopes**: In the log-log CCDF plot, what does a straight line indicate? How do the slopes compare across network types?

    3. **Friendship Paradox**: Which network type shows the strongest friendship paradox effect? Why might this be?

    4. **Sampling Bias**: How does degree-biased sampling change the distribution of sampled degrees compared to uniform sampling?

    These patterns reveal fundamental differences in network structure and have implications for processes like disease spreading, information diffusion, and targeted interventions.
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
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import sparse
    return igraph, np, plt, seaborn, sns, sparse


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()