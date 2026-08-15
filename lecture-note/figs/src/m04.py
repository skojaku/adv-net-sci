"""Regenerate the static figures for this module.

Extracted from lecture-note/m04-node-degree/01-concepts.qmd.
Run from the repository root; writes SVGs into lecture-note/figs/.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
OUT.mkdir(parents=True, exist_ok=True)


def _save(name):
    plt.savefig(OUT / f'{name}.svg', bbox_inches='tight', transparent=True)
    plt.close('all')
    print('wrote', name + '.svg')


# --- cell 0 --------------------------------------------------
# caption: A histogram of a scale-free degree distribution on a linear scale. It's nearly impossible to see the structure of the tail.
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import powerlaw

# Generate synthetic data from a power-law distribution
np.random.seed(42)
fit = powerlaw.Fit(np.random.zipf(2.5, 1000), discrete=True)
degrees = fit.power_law.generate_random(1000)
degrees = [int(d) for d in degrees if d > 0]

# Plotting with seaborn
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(degrees, bins=int(np.max(degrees)), stat="probability", edgecolor='black', ax=ax)
ax.set_xlabel("Degree (k)")
ax.set_ylabel("Fraction of Nodes, P(k)")
plt.tight_layout()
sns.despine()
plt.show()
_save('linear-hist')

# --- cell 1 --------------------------------------------------
# caption: The same degree histogram on a log-log scale. The structure becomes much clearer, revealing a roughly linear relationship.
# Prepare the data for plotting: get histogram bins and densities
counts, bins = np.histogram(degrees, bins=int(np.max(degrees)))
bins = bins[:-1]
non_zero_indices = counts > 0
counts = counts[non_zero_indices]
bins = bins[non_zero_indices]
density = counts / len(degrees)

# Plotting with seaborn
fig, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(x=bins, y=density, color='dodgerblue', ax=ax, s = 30)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Degree (k)")
ax.set_ylabel("Fraction of Nodes, P(k)")
sns.despine()
plt.tight_layout()
plt.show()
_save('loglog-hist')

# --- cell 2 --------------------------------------------------
# caption: The CCDF of the degree distribution on a log-log scale. 
# Plotting the CCDF using seaborn's ecdfplot (complementary CDF)
fig, ax = plt.subplots(figsize=(6, 4))
sns.ecdfplot(degrees, ax=ax, complementary=True, color=sns.color_palette()[1], linewidth=2, log_scale=(True, True))
ax.set_xlabel("Degree (k)")
ax.set_ylabel("CCDF (P(k' > k))")
sns.despine()
plt.tight_layout()
plt.show()
_save('ccdf-hist')

# --- cell 3 --------------------------------------------------
# caption: The CDF of the degree distribution on a log-log scale. 
# Plotting the CCDF using seaborn's ecdfplot (complementary CDF)
fig, ax = plt.subplots(figsize=(6, 4))
sns.ecdfplot(degrees, ax=ax, color=sns.color_palette()[3], linewidth=2, log_scale=(True, True))
ax.set_xlabel("Degree (k)")
ax.set_ylabel("CDF (P(k' ≤ k))")
sns.despine()
plt.tight_layout()
plt.show()
_save('cdf-hist')
