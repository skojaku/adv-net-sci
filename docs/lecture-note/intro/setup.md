# Set up the environment

This course involves coding in Python, which requires some setup. While the lecture notes are executable in-browser, this can be slow and unreliable. Here are some recommended alternatives for a better learning experience:

## Local (recommended)

### Option 1: Git + VS Code or JupyterLab

This is the most recommended way to maximize your learning experience.

1. Git clone the repository via [the course repository](https://github.com/skojaku/adv-net-ci) by `git clone https://github.com/skojaku/adv-net-ci`.
  - Anyone who has experience with GitHub Desktop, please help me write the instruction on how to clone the repository.
2. Open the repository in VS Code or JupyterLab.
3. Create an environemtn using conda or mamba through the `environment.yml` file.
4. Download the notebook you want to run from the lecture note, and run it locally.

If the installation is successful, you can run the following code

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx
import igraph
import pandas
import scipy
```

### Option 2: Without Git

You can download the notebook by clicking the `Download` button on top of the lecture note. You can then import the notebook to your dev tool and run it.

## Cloud

### Google Colab
Google Colab is another alternative. But you might need to install some extra packages every time you start a new session.

1. Download the notebook you want to run from the lecture note.
2. Upload the notebook to Google Colab.

Sometimes you might see and error like `ModuleNotFoundError: No module named 'python-igraph'`. In that case, you can install the missing package by `!pip install python-igraph` in the cell.

### Github Codespaces

Github Codespaces is probably another alternative. But I have not tried it yet.