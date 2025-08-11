# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib==3.10.5",
#     "numpy==2.3.2",
#     "scipy==1.16.1",
# ]
# ///
import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from scipy.ndimage import label
    return ListedColormap, label, mo, np, plt


@app.cell
def _(mo):
    # Create a slider to control the puddle probability
    p_slider = mo.ui.slider(
        start=0.0, 
        stop=1.0, 
        step=0.01, 
        value=0.5, 
        label="Puddle Probability (p)"
    )
    return (p_slider,)


@app.cell
def _(mo, p_slider):
    # Display the slider with current value
    mo.md(f"""
    ## Interactive Percolation Visualization

    Use the slider to control the probability that each square becomes a "puddle". 
    Watch how connected components emerge and disappear as you change the probability!

    Current probability: **{p_slider.value:.2f}**

    {p_slider}
    """)
    return


@app.cell
def _(ListedColormap, label, np, p_slider, plt):
    # Grid parameters
    grid_size = 50

    # Generate the percolation grid based on slider value
    np.random.seed(42)  # For reproducible results during demo
    grid = np.random.random((grid_size, grid_size)) < p_slider.value

    # Find connected components (puddles that touch each other)
    labeled_array, num_features = label(grid)

    # Find the largest connected component
    if num_features > 0:
        sizes = [(labeled_array == i).sum() for i in range(1, num_features + 1)]
        largest_size = max(sizes)
        largest_fraction = largest_size / (grid_size * grid_size)
    else:
        largest_size = 0
        largest_fraction = 0.0

    # Create visualization
    plt.figure(figsize=(8, 8))

    # Create a display grid that shows largest component in red
    display_grid = np.zeros_like(grid, dtype=int)
    
    # Find the largest component
    if num_features > 0:
        # Find which label corresponds to the largest component
        largest_label = np.argmax(sizes) + 1  # +1 because labels start from 1
        
        # Set display values: 0=white, 1=blue (small components), 2=red (largest component)
        display_grid[grid] = 1  # All puddles start as blue
        display_grid[labeled_array == largest_label] = 2  # Largest component in red

    # Create custom colormap: white for empty, blue for small components, red for largest
    colors = ['white', '#4472C4', '#E74C3C']  # white, blue, red
    cmap = ListedColormap(colors)

    # Plot the grid
    plt.imshow(display_grid, cmap=cmap, interpolation='nearest')

    # Styling
    plt.title(f'Percolation Grid (p = {p_slider.value:.2f})\n'
             f'Largest Component (Red): {largest_size} squares '
             f'({largest_fraction:.1%} of grid)', 
             fontsize=14, pad=20)
    plt.xlabel('Grid Position')
    plt.ylabel('Grid Position')

    # Add grid lines for clarity
    plt.xticks(np.arange(-0.5, grid_size, 10), minor=True)
    plt.yticks(np.arange(-0.5, grid_size, 10), minor=True)
    plt.grid(which='minor', color='gray', linestyle='-', alpha=0.3)
    plt.tick_params(which='minor', size=0)
    
    # Add a legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='white', edgecolor='black', label='Empty'),
        Patch(facecolor='#4472C4', label='Small Components'), 
        Patch(facecolor='#E74C3C', label='Largest Component')
    ]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))

    # Return the plot
    plt.gca()
    return


@app.cell
def _(label, np, p_slider, plt):
    # Generate data for the phase transition plot
    prob_values = np.linspace(0, 1, 100)
    component_fractions = []

    grid_size_phase = 50  # Use smaller grid for faster computation

    # Calculate largest component size for different probabilities
    np.random.seed(42)  # Fixed seed for consistent results
    for prob in prob_values:
        # Generate random grid
        phase_grid = np.random.random((grid_size_phase, grid_size_phase)) < prob

        # Find connected components
        labeled_phase, num_phase = label(phase_grid)

        if num_phase > 0:
            phase_sizes = [(labeled_phase == i).sum() for i in range(1, num_phase + 1)]
            largest_phase = max(phase_sizes) / (grid_size_phase * grid_size_phase)
        else:
            largest_phase = 0.0

        component_fractions.append(largest_phase)

    # Create the phase transition plot
    plt.figure(figsize=(8, 6))

    # Plot the phase transition curve
    plt.plot(prob_values, component_fractions, 'b-', linewidth=2, 
             label='Largest Component Size')

    # Highlight current probability
    current_idx = int(p_slider.value * 99)  # Convert to index
    plt.plot(p_slider.value, component_fractions[current_idx], 
             'ro', markersize=10, label=f'Current p = {p_slider.value:.2f}')

    # Mark approximate critical point (for 2D lattice, pc ≈ 0.593)
    critical_p = 0.593
    plt.axvline(x=critical_p, color='gray', linestyle='--', alpha=0.7, 
                label=f'Critical point (p_c ≈ {critical_p})')

    # Styling
    plt.xlabel('Probability (p)', fontsize=12)
    plt.ylabel('Fraction of Grid in Largest Component', fontsize=12)
    plt.title('Percolation Phase Transition', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    # Add phase labels
    plt.text(0.2, 0.8, 'Disconnected\nPhase', fontsize=11, ha='center', 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    plt.text(0.8, 0.8, 'Connected\nPhase', fontsize=11, ha='center',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    plt.gca()
    return


if __name__ == "__main__":
    app.run()