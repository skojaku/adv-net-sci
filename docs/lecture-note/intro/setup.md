
---
title: Setup
---

## Python

To follow the course materials, you'll need Python 3.8 or higher. We recommend using the latest stable version of Python.

### Installing Python

If you don't have Python installed:
- **Windows/Mac**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: Use your package manager (e.g., `sudo apt install python3`)

### Required Packages

Install the required packages using pip:

```bash
pip install numpy pandas matplotlib seaborn networkx igraph-python graph-tool scikit-learn
```

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

Marimo is a reactive Python notebook that we'll use for interactive coding exercises.

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

Visual Studio Code is our recommended code editor for this course.

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

We'll use Github for version control and collaboration.

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
