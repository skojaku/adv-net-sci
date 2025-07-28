
---
title: Setup
---

## Python and Virtual Environments

We'll use Python to work with data throughout this course. Python is an excellent choice for network science for its rich ecosystem of libraries, readable and intuitive syntax, and well-documented documentation.

We strongly recommend using **virtual environments** to manage your Python packages. Virtual environments create isolated Python installations for each project, avoiding dependency hell and providing several key benefits:


::: {.column-margin}

Don't confuse Python virtual environments with virtual machines (VMs). Python virtual environments are lightweight isolation tools that only separate Python packages and dependencies within the same operating system. Virtual machines, on the other hand, create complete isolated operating systems.

:::

- **Reproducibility**: Your code will work consistently across different machines and over time
- **Flexibility**: You can use different versions of packages for different projects without conflicts
- **Prevent project interference**: Changes to one project won't break another project's dependencies

::: {#fig-python-ecosystem .column-margin}

![](https://cdn-media-1.freecodecamp.org/images/1*i4QK4sSGX7Q4RRgOytkSuw.jpeg)

Without virtual environments, you risk dependency hell where package conflicts make your projects unusable.

:::


**Using uv (Recommended)**

We recommend using [uv](https://docs.astral.sh/uv/), a fast Python package and project manager. While we won't be running uv commands directly in this course, you'll need uv to properly run Marimo notebooks, which provides a much better development experience. [See here for installation instructions](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).



::: {.column-margin}

**Other Options**

If you prefer tools other than uv, here are some alternatives:

*[venv](https://docs.python.org/3/library/venv.html):* The standard library for creating virtual environments

*[pyenv](https://github.com/pyenv/pyenv):* Great for managing multiple Python versions

*[Conda](https://docs.conda.io/):* Popular in data science, includes non-Python packages

*[Mamba](https://mamba.readthedocs.io/):* Faster drop-in replacement for conda

*[Miniforge](https://github.com/conda-forge/miniforge):* Community-driven conda distribution with mamba included

:::

<iframe width="560" height="315" src="https://www.youtube.com/embed/bwRgYxmCqLI?si=-PMkEhKuFW4IyMXW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Marimo Notebook

We'll use Marimo notebooks for assignments and interactive exercises throughout the course. Marimo is a reactive Python notebook that automatically updates when you change code, making it perfect for exploring network data and seeing results in real-time.

**Using Marimo's Sandbox Feature with uv (Recommended)**

Marimo integrates especially tightly with uv and provides a package sandbox feature that lets you inline dependencies directly in notebook files. This is the easiest way to get started - no prior uv knowledge required.

Creating a sandboxed notebook:
```bash
uvx marimo edit --sandbox my_notebook.py
```

This command installs marimo in a temporary environment, tracks your dependencies and stores them in the notebook file, and automatically downloads any existing dependencies.

Running sandboxed notebooks:
```bash
uv run my_notebook.py
```

Benefits: Dependencies are embedded in the notebook file itself, perfect reproducibility, and no need to manage separate dependency files.

**Alternative Installation**

If you're not using uv, you can install marimo with pip:
```bash
pip install marimo
```

### Running Marimo

To start a new marimo notebook:

```bash
marimo edit
```

To open an existing marimo notebook:

```bash
marimo edit notebook.py
```

### Key Features

- **Reactive**: Cells automatically re-run when their dependencies change
- **Version control friendly**: Notebooks are stored as Python files
- **Interactive widgets**: Built-in support for sliders, dropdowns, and other UI elements

## VS Code

Visual Studio Code is our recommended code editor for this course. It provides excellent Python support, integrated debugging, and extensions that make working with network data and Marimo notebooks more efficient.

### Installation

Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)

### Recommended Extensions

Install these extensions for the best Python development experience:

- **Python** (Microsoft): Python language support
- **Jupyter** (Microsoft): Jupyter notebook support
- **Python Docstring Generator**: Auto-generate docstrings
- **GitLens**: Enhanced Git capabilities
- **Marimo** (marimo-team): Marimo notebook support

### Configuration

Create a `.vscode/settings.json` file in your project root with:

```json
{
    "python.defaultInterpreterPath": "python3",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

## Github

We'll use GitHub for assignments in this course. GitHub provides version control for your code and a platform for submitting and reviewing your work. You'll create repositories, commit your solutions, and share them for evaluation.

### Creating a Github Account

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Follow the registration process

### Setting up Git

Configure your Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### SSH Key Setup (Recommended)

1. Generate an SSH key:
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

2. Add the key to your SSH agent:
```bash
ssh-add ~/.ssh/id_ed25519
```

3. Copy the public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

4. Add the key to your Github account under Settings > SSH and GPG keys

### Basic Git Workflow

```bash
# Clone a repository
git clone git@github.com:username/repository.git

# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push changes
git push origin main
````
