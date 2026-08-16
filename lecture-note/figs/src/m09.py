"""Regenerate the static figures for this module.

Extracted from lecture-note/m09-graph-neural-networks/01-concepts.qmd.
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
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("talk")

alpha = 1
lambdas = np.linspace(0, 10, 100)
h_low = 1 / (1 + alpha * lambdas)
h_high = (alpha * lambdas) / (1 + alpha * lambdas)

ACCENT = "#593196"
CONTRAST = "#c2410c"

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
sns.lineplot(x=lambdas, y=h_low, ax=axes[0], color=ACCENT, linewidth=2.5)
sns.lineplot(x=lambdas, y=h_high, ax=axes[1], color=CONTRAST, linewidth=2.5)
axes[0].set_title("Low-pass filter")
axes[1].set_title("High-pass filter")
fig.text(0.5, 0.01, r"Eigenvalue $\lambda$", ha="center")
axes[0].set_ylabel(r"Filter response $h(\lambda)$")
sns.despine()
plt.tight_layout()
_save('m09-fig-00')
