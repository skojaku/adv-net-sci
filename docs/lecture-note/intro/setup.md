
---
title: Setup
---

## Python

We'll use Python to work with data throughout this course. Python is an excellent choice for network science for its rich ecosystem of libraries, readable and intuitive syntax, and well-documented documentation.

We strongly recommend using virtual environments to manage your Python packages. Virtual environments create isolated Python installations for each project, avoiding dependency hell and providing several key benefits:

- **Reproducibility**: Your code will work consistently across different machines and over time
- **Flexibility**: You can use different versions of packages for different projects without conflicts  
- **Prevent project interference**: Changes to one project won't break another project's dependencies

::: {fig-python-ecosystem}

![Dependency hell](https://cdn-media-1.freecodecamp.org/images/1*i4QK4sSGX7Q4RRgOytkSuw.jpeg)

Without virtual environments, you risk dependency hell where package conflicts make your projects unusable.

:::
**Using UV (Recommended)**

We recommend using [UV](https://docs.astral.sh/uv/), a fast Python package and project manager. UV is significantly faster than traditional tools and makes managing Python environments effortless.

Install UV:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Create and activate a virtual environment for this course:
```bash
# Create a new project with virtual environment
uv init network-science-course
cd network-science-course

# Add required packages
uv add numpy pandas matplotlib seaborn networkx igraph-python scikit-learn marimo

# Activate the environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

**Alternative: Using venv**

If you prefer the standard approach:
```bash
# Create virtual environment
python -m venv network-science-env

# Activate it
source network-science-env/bin/activate  # On macOS/Linux
# or
network-science-env\Scripts\activate     # On Windows

# Install packages
pip install numpy pandas matplotlib seaborn networkx igraph-python graph-tool scikit-learn marimo
```



::: {.callout-note}

You'll need Python 3.8 or higher. We recommend using the latest stable version of Python.

:::

### Trouble shooting with Google Colab

Google Colab has many packages pre-installed. However, they do not include some packages for network analysis like `igraph` and `graph-tool`.

**Installing igraph**
Create a cell on top of the notebook and run the following code to install the igraph:
```python
!sudo apt install libcairo2-dev pkg-config python3-dev
!pip install pycairo cairocffi
!pip install igraph
```

**Installing graph-tool**
Create a cell on top of the notebook and run the following code to install the graph-tool:
```python
!wget https://downloads.skewed.de/skewed-keyring/skewed-keyring_1.0_all_$(lsb_release -s -c).deb
!dpkg -i skewed-keyring_1.0_all_$(lsb_release -s -c).deb
!echo "deb [signed-by=/usr/share/keyrings/skewed-keyring.gpg] https://downloads.skewed.de/apt $(lsb_release -s -c) main" > /etc/apt/sources.list.d/skewed.list
!apt-get update
!apt-get install python3-graph-tool python3-matplotlib python3-cairo

# Colab uses a Python install that deviates from the system's! Bad colab! We need some workarounds.
!apt purge python3-cairo
!apt install libcairo2-dev pkg-config python3-dev
!pip install --force-reinstall pycairo
!pip install zstandar
```

## Marimo Notebook

We'll use Marimo notebooks for assignments and interactive exercises throughout the course. Marimo is a reactive Python notebook that automatically updates when you change code, making it perfect for exploring network data and seeing results in real-time.

### Installation

Install marimo using pip:

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
