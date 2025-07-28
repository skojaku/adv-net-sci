
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

::: {#fig-python-ecosystem}

![](https://cdn-media-1.freecodecamp.org/images/1*i4QK4sSGX7Q4RRgOytkSuw.jpeg)

Without virtual environments, you risk dependency hell where package conflicts make your projects unusable.

:::


**Using uv (Recommended)**

We recommend using [uv](https://docs.astral.sh/uv/), a fast Python package and project manager. While we won't be running uv commands directly in this course, you'll need uv to properly run Marimo notebooks, which provides a much better development experience. [See here for installation instructions](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

::: {.column-margin}

<iframe width="250" height="125" src="https://www.youtube.com/embed/bwRgYxmCqLI?si=-PMkEhKuFW4IyMXW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

:::



**Other Options**

If you prefer tools other than uv, here are some alternatives:

- [venv](https://docs.python.org/3/library/venv.html): The standard library for creating virtual environments;
- [pyenv](https://github.com/pyenv/pyenv): Great for managing multiple Python versions;
- [Conda](https://docs.conda.io/): Popular in data science, includes non-Python packages;
- [Mamba](https://mamba.readthedocs.io/): Faster drop-in replacement for conda;
- [Miniforge](https://github.com/conda-forge/miniforge): Community-driven conda distribution with mamba included;



## Marimo Notebook

We'll use [Marimo](https://marimo.io/) ([GitHub](https://github.com/marimo-team/marimo)) notebooks for assignments and interactive exercises throughout the course. Marimo is a reactive Python notebook that automatically updates when you change code, making it perfect for exploring network data and seeing results in real-time.

::: {.column-margin}

<iframe width="250" height="150" src="https://www.youtube.com/embed/3N6lInzq5MI?si=8WXcexm56zn86WkW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

:::

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

**Running Marimo**

To start a new marimo notebook:

```bash
marimo edit
```

To open an existing marimo notebook:

```bash
marimo edit notebook.py
```


## Github

We'll use GitHub for assignment collection and auto-grading in this course. 

**Minimum Requirements**

At the minimum level, you only need to:
1. Create a GitHub account at [github.com](https://github.com)
2. Know how to upload files to GitHub

Detailed instructions on how to upload your assignments to GitHub will be provided separately - advanced Git features are not required for the course. See this [assignment example](https://github.com/sk-classroom/starter) to get familiar with the format.

**For Students Interested in Learning More**

Understanding Git and GitHub is useful for seamlessly working with assignments and will benefit your programming workflow. Additionally, Git and GitHub integrate nicely with AI tools for productivity improvement, making your development process more efficient.

**GitHub Desktop (Recommended for Beginners)**

If you want to learn more about version control, start with [GitHub Desktop](https://desktop.github.com/), a user-friendly graphical interface:

1. Go to [desktop.github.com](https://desktop.github.com/)
2. Download for your operating system  
3. Install and sign in with your GitHub account

**Understanding Git and Version Control**

Git is a version control system that tracks changes in your code over time. Think of it as a sophisticated "save" system that:
- Keeps a complete history of all changes to your files
- Lets you go back to any previous version
- Allows multiple people to work on the same project simultaneously
- Helps you manage different versions or "branches" of your work

GitHub is a cloud-based platform that hosts Git repositories and adds collaboration features.

**Learning Resources**

Essential resources to understand Git concepts:
- [Interactive Git Tutorial](https://learngitbranching.js.org/) - Visual, hands-on learning
- [GitHub Desktop Documentation](https://docs.github.com/en/desktop) - Official desktop app guide
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) - Detailed tutorials with examples
