"""
Interactive Watts-Strogatz Small-World Network Explorer

This Marimo notebook provides an interactive exploration of the Watts-Strogatz model,
allowing users to adjust the rewiring probability and observe how network properties change.

Author: Network Science Course
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")

@app.cell
def __(mo):
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

@app.cell
def __():
    import marimo as mo
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.collections import LineCollection
    import warnings
    warnings.filterwarnings('ignore')
    return LineCollection, mo, np, nx, patches, plt, warnings

@app.cell
def __(mo):
    # Create the main control panel
    mo.md("## Controls")
    return

@app.cell
def __(mo):
    # Rewiring probability slider
    p_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.01,
        value=0.1,
        show_value=True,
        label="Rewiring Probability (p)",
        full_width=True
    )
    
    # Network size slider
    N_slider = mo.ui.slider(
        start=10,
        stop=50,
        step=5,
        value=20,
        show_value=True,
        label="Number of Nodes (N)",
        full_width=True
    )
    
    # Degree slider
    k_slider = mo.ui.slider(
        start=2,
        stop=8,
        step=2,
        value=4,
        show_value=True,
        label="Node Degree (k)",
        full_width=True
    )
    
    # Display controls in a nice layout
    mo.vstack([
        mo.md("**Adjust the parameters to explore different network configurations:**"),
        p_slider,
        N_slider, 
        k_slider
    ])
    return N_slider, k_slider, p_slider

@app.cell
def __(N_slider, k_slider, nx, p_slider):
    def generate_networks(N, k, p, seed=42):
        """Generate Watts-Strogatz network and equivalent random graph"""
        # Generate Watts-Strogatz network
        G_ws = nx.watts_strogatz_graph(N, k, p, seed=seed)
        
        # Generate random network with same number of edges
        num_edges = G_ws.number_of_edges()
        prob_random = num_edges / (N * (N-1) / 2)  # Probability for same edge density
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
            L = float('inf')
        return C, L
    
    def compute_small_world_coefficient(C, L, C_random, L_random):
        """Compute the Watts-Strogatz small-world coefficient σ"""
        if C_random > 0 and L_random > 0 and L != float('inf'):
            sigma = (C / C_random) / (L / L_random)
        else:
            sigma = 0
        return sigma
    
    # Generate networks with current parameters
    G_ws, G_random = generate_networks(N_slider.value, k_slider.value, p_slider.value)
    return (
        G_random,
        G_ws,
        compute_metrics,
        compute_small_world_coefficient,
        generate_networks,
    )

@app.cell
def __(G_random, G_ws, compute_metrics, compute_small_world_coefficient):
    # Compute metrics for both networks
    C_ws, L_ws = compute_metrics(G_ws)
    C_random, L_random = compute_metrics(G_random)
    sigma = compute_small_world_coefficient(C_ws, L_ws, C_random, L_random)
    
    # Store metrics for display
    metrics = {
        'C_ws': C_ws,
        'L_ws': L_ws,
        'C_random': C_random,
        'L_random': L_random,
        'sigma': sigma
    }
    return C_random, C_ws, L_random, L_ws, metrics, sigma

@app.cell
def __(mo, metrics):
    # Display current metrics
    mo.md(f"""
    ## Current Network Metrics
    
    | Metric | Watts-Strogatz | Random | Ratio |
    |--------|----------------|---------|-------|
    | **Clustering (C)** | {metrics['C_ws']:.4f} | {metrics['C_random']:.4f} | {metrics['C_ws']/max(metrics['C_random'], 0.001):.2f} |
    | **Path Length (L)** | {metrics['L_ws']:.4f} | {metrics['L_random']:.4f} | {metrics['L_ws']/max(metrics['L_random'], 0.001):.2f} |
    | **Small-world σ** | {metrics['sigma']:.4f} | - | {'Strong' if metrics['sigma'] > 1 else 'Weak'} |
    """)
    return

@app.cell
def __(mo):
    mo.md("## Network Visualization")
    return

@app.cell
def __(
    G_random,
    G_ws,
    N_slider,
    k_slider,
    metrics,
    np,
    p_slider,
    patches,
    plt,
):
    def create_visualization():
        """Create the main network visualization and metrics plots"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
        
        # Plot 1: Watts-Strogatz Network
        N = N_slider.value
        k = k_slider.value
        
        # Create circular layout
        pos = {}
        angles = np.linspace(0, 2*np.pi, N, endpoint=False)
        for i, node in enumerate(G_ws.nodes()):
            pos[node] = (np.cos(angles[i]), np.sin(angles[i]))
        
        # Draw edges with different colors for original vs rewired
        edge_colors = []
        for edge in G_ws.edges():
            i, j = edge
            # Calculate ring distance (minimum distance around the circle)
            ring_distance = min(abs(i-j), N-abs(i-j))
            # Original edges connect to k/2 nearest neighbors on each side
            if ring_distance <= k//2:
                edge_colors.append('blue')  # Original edge
            else:
                edge_colors.append('red')   # Rewired edge
        
        # Draw the network
        nx.draw_networkx_edges(G_ws, pos, ax=ax1, edge_color=edge_colors, 
                              alpha=0.7, width=1.5)
        nx.draw_networkx_nodes(G_ws, pos, ax=ax1, node_color='lightblue', 
                              node_size=200, edgecolors='black')
        
        if N <= 30:  # Only show labels for smaller networks
            nx.draw_networkx_labels(G_ws, pos, ax=ax1, font_size=8)
        
        ax1.set_title(f'Watts-Strogatz Network\n(N={N}, k={k}, p={p_slider.value:.3f})', 
                     fontsize=12, fontweight='bold')
        ax1.set_aspect('equal')
        ax1.axis('off')
        
        # Add legend
        blue_patch = patches.Patch(color='blue', label='Original edges', alpha=0.7)
        red_patch = patches.Patch(color='red', label='Rewired edges', alpha=0.7)
        ax1.legend(handles=[blue_patch, red_patch], loc='upper right')
        
        # Plot 2: Random Network (for comparison)
        pos_random = {}
        for i, node in enumerate(G_random.nodes()):
            pos_random[node] = (np.cos(angles[i]), np.sin(angles[i]))
        
        nx.draw_networkx_edges(G_random, pos_random, ax=ax2, edge_color='gray', 
                              alpha=0.5, width=1)
        nx.draw_networkx_nodes(G_random, pos_random, ax=ax2, node_color='lightcoral', 
                              node_size=200, edgecolors='black')
        
        if N <= 30:
            nx.draw_networkx_labels(G_random, pos_random, ax=ax2, font_size=8)
            
        ax2.set_title(f'Random Network\n(Same N, similar edge density)', 
                     fontsize=12, fontweight='bold')
        ax2.set_aspect('equal')
        ax2.axis('off')
        
        # Plot 3: Clustering Coefficient Comparison
        C_ws = metrics['C_ws']
        C_random = metrics['C_random']
        
        bars = ax3.bar(['Watts-Strogatz', 'Random'], [C_ws, C_random],
                      color=['skyblue', 'lightcoral'], alpha=0.8, width=0.6)
        ax3.set_ylabel('Clustering Coefficient (C)', fontweight='bold')
        ax3.set_title('Clustering Comparison', fontweight='bold')
        ax3.set_ylim(0, max(C_ws, C_random, 0.1) * 1.2)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, [C_ws, C_random])):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
        
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Small-World Coefficient and Path Length
        L_ws = metrics['L_ws']
        L_random = metrics['L_random']
        sigma = metrics['sigma']
        
        # Create dual y-axis plot
        ax4_twin = ax4.twinx()
        
        # Path length comparison (left y-axis)
        if L_ws != float('inf'):
            bars_L = ax4.bar(['WS', 'Random'], [L_ws, L_random], 
                           color=['lightgreen', 'lightcoral'], alpha=0.8, width=0.4)
            ax4.set_ylabel('Average Path Length (L)', color='darkgreen', fontweight='bold')
            ax4.tick_params(axis='y', labelcolor='darkgreen')
            
            # Add path length labels
            for bar, val in zip(bars_L, [L_ws, L_random]):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                        f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Small-world coefficient (right y-axis) 
        sigma_bar = ax4_twin.bar(['Small-World σ'], [sigma], color='gold', 
                                alpha=0.8, width=0.3, x=1.5)
        ax4_twin.axhline(y=1, color='red', linestyle='--', alpha=0.7, 
                        label='σ = 1 (Random baseline)')
        ax4_twin.set_ylabel('Small-World Coefficient (σ)', color='darkorange', 
                           fontweight='bold')
        ax4_twin.tick_params(axis='y', labelcolor='darkorange')
        ax4_twin.set_ylim(0, max(sigma * 1.3, 2))
        
        # Add sigma label and interpretation
        ax4_twin.text(1.5, sigma + max(sigma * 0.1, 0.1), f'{sigma:.2f}', 
                     ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Interpretation
        if sigma > 1.5:
            interpretation = "Strong Small-World"
            interp_color = 'darkgreen'
        elif sigma > 1:
            interpretation = "Small-World"  
            interp_color = 'green'
        elif sigma > 0.5:
            interpretation = "Moderate"
            interp_color = 'orange'
        else:
            interpretation = "Random-like"
            interp_color = 'red'
        
        ax4_twin.text(1.5, max(sigma * 0.7, 0.3), interpretation, ha='center', va='center',
                     bbox=dict(boxstyle='round', facecolor=interp_color, alpha=0.3),
                     fontweight='bold')
        
        ax4.set_title('Path Length & Small-World Property', fontweight='bold')
        ax4_twin.legend(loc='upper left')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    # Create and display the visualization
    visualization_fig = create_visualization()
    mo.mpl.interactive(visualization_fig)
    return create_visualization, visualization_fig

@app.cell
def __(mo, p_slider):
    mo.md(f"""
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
    """)
    return

@app.cell
def __(mo):
    mo.md("""
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
    """)
    return

if __name__ == "__main__":
    app.run()