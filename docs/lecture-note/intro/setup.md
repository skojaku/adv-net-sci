# Set up the environment

A main component of this course is to learn how to code in Python. And this needs some setup to be done before we start.
The lecture note is *executable*. So in principle, you can run the code on browser.
However, it takes some time to prepare MyBinder, a service that offers free cloud computing resources, and may not work when the server is busy.
So, let's consider the following alternatives.

# Most recommended: Use VS Code or JupyterLab

This is the most recommended way to maximize your learning experience.

1. Git clone the repository via [the course repository](https://github.com/skojaku/adv-net-ci).
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


# Alternative: Use Google Colab

Google Colab is another alternative. But you might need to install some extra packages every time you start a new session.

1. Download the notebook you want to run from the lecture note.
2. Upload the notebook to Google Colab.


# Github Codespaces

Github Codespaces is probably another alternative. But I have not tried it yet.