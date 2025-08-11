import marimo

__generated_with = "0.10.6"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import networkx as nx
    from scipy.ndimage import label
    return ListedColormap, label, mo, np, nx, plt


@app.cell
def __():
    # Create a slider to control the puddle probability
    p_slider = mo.ui.slider(
        start=0.0, 
        stop=1.0, 
        step=0.01, 
        value=0.5, 
        label="Puddle Probability (p)"
    )
    
    # Display the slider
    mo.md(f"""
    ## Interactive Percolation Visualization
    
    Use the slider to control the probability that each square becomes a "puddle". 
    Watch how connected components emerge and disappear as you change the probability!
    
    Current probability: **{p_slider.value:.2f}**
    
    {p_slider}
    """)
    return (p_slider,)


@app.cell
def __(ListedColormap, label, mo, np, p_slider, plt):
    # Grid parameters
    grid_size = 50
    
    # Generate the percolation grid based on slider value
    np.random.seed(42)  # For reproducible results during demo
    grid = np.random.random((grid_size, grid_size)) < p_slider.value
    
    # Find connected components (puddles that touch each other)
    labeled_array, num_features = label(grid)
    
    # Find the largest connected component
    if num_features > 0:
        component_sizes = [(labeled_array == i).sum() for i in range(1, num_features + 1)]
        largest_component_size = max(component_sizes)
        largest_component_fraction = largest_component_size / (grid_size * grid_size)
    else:
        largest_component_size = 0
        largest_component_fraction = 0.0
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Create custom colormap: white for empty, blue for puddles
    colors = ['white', '#4472C4']  # white for 0, blue for 1
    cmap = ListedColormap(colors)
    
    # Plot the grid
    im = ax.imshow(grid, cmap=cmap, interpolation='nearest')
    
    # Styling
    ax.set_title(f'Percolation Grid (p = {p_slider.value:.2f})\n'
                f'Largest Component: {largest_component_size} squares '
                f'({largest_component_fraction:.1%} of grid)', 
                fontsize=14, pad=20)
    ax.set_xlabel('Grid Position')
    ax.set_ylabel('Grid Position')
    
    # Add grid lines for clarity
    ax.set_xticks(np.arange(-0.5, grid_size, 10), minor=True)
    ax.set_yticks(np.arange(-0.5, grid_size, 10), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', alpha=0.3)
    ax.tick_params(which='minor', size=0)
    
    # Return the plot
    plt.gca()
    return ax, component_sizes, fig, grid, grid_size, im, labeled_array, largest_component_fraction, largest_component_size, num_features


@app.cell
def __(mo, np, p_slider, plt):
    # Generate data for the phase transition plot
    p_values = np.linspace(0, 1, 100)
    largest_component_fractions = []
    
    grid_size_small = 50  # Use smaller grid for faster computation
    
    # Calculate largest component size for different probabilities
    np.random.seed(42)  # Fixed seed for consistent results
    for p in p_values:
        # Generate random grid
        test_grid = np.random.random((grid_size_small, grid_size_small)) < p
        
        # Find connected components
        from scipy.ndimage import label
        labeled_test, num_test = label(test_grid)
        
        if num_test > 0:
            test_sizes = [(labeled_test == i).sum() for i in range(1, num_test + 1)]
            largest_test = max(test_sizes) / (grid_size_small * grid_size_small)
        else:
            largest_test = 0.0
        
        largest_component_fractions.append(largest_test)
    
    # Create the phase transition plot
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # Plot the phase transition curve
    ax2.plot(p_values, largest_component_fractions, 'b-', linewidth=2, 
             label='Largest Component Size')
    
    # Highlight current probability
    current_idx = int(p_slider.value * 99)  # Convert to index
    ax2.plot(p_slider.value, largest_component_fractions[current_idx], 
             'ro', markersize=10, label=f'Current p = {p_slider.value:.2f}')
    
    # Mark approximate critical point (for 2D lattice, pc ≈ 0.593)
    critical_p = 0.593
    ax2.axvline(x=critical_p, color='gray', linestyle='--', alpha=0.7, 
                label=f'Critical point (p_c ≈ {critical_p})')
    
    # Styling
    ax2.set_xlabel('Probability (p)', fontsize=12)
    ax2.set_ylabel('Fraction of Grid in Largest Component', fontsize=12)
    ax2.set_title('Percolation Phase Transition', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    
    # Add phase labels
    ax2.text(0.2, 0.8, 'Disconnected\nPhase', fontsize=11, ha='center', 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax2.text(0.8, 0.8, 'Connected\nPhase', fontsize=11, ha='center',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    plt.gca()
    return ax2, critical_p, current_idx, fig2, grid_size_small, largest_component_fractions, largest_test, num_test, p_values, test_grid, test_sizes


if __name__ == "__main__":
    app.run()