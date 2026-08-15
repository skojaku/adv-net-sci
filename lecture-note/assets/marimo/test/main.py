import marimo

__generated_with = "0.14.13"
app = marimo.App(width="full")


@app.cell
def _():
    import numpy as np
    import marimo as mo
    return mo, np


@app.cell
def _():
    return


@app.cell
def _(np):
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Generate random data
    np.random.seed(0)
    x = np.random.normal(loc=0, scale=1, size=100)
    y = np.random.normal(loc=0, scale=1, size=100)

    # Create a seaborn scatter plot
    sns.scatterplot(x=x, y=y, color="blue", alpha=0.6)

    # Adding titles and labels
    plt.title("Scatter Plot of Randomly Generated Gaussian Variables")
    plt.xlabel("X-axis: Gaussian Variable 1")
    plt.ylabel("Y-axis: Gaussian Variable 2")

    plt.gca()
    return (plt,)


@app.cell
def _(mo):
    mo.ui.chat(
        mo.ai.llm.google(
            "gemini-2.5-flash-lite",
            system_message="You are a helpful chemist. Output your answer in markdown or latex.",
            api_key="AIzaSyCEFfNiTQMmixAXreE88zfGRQ1AP-xsv1Q",
        ),
        # Provide some sample prompts
        prompts=[
            "What is the chemical formula for water?",
            "What is the chemical formula for carbon dioxide?",
            "What is the chemical formula for {{compound}}?",
        ],
        # Show some configuration controls to change temperature, token limit, etc.
        show_configuration_controls=True,
    )
    return


@app.cell
def _(np, plt):
    # Parameters for the Poisson distribution
    lambda_param = 5  # Mean number of events
    num_points = 100  # Number of random points

    # Generate Poisson random scatter data
    _x = np.random.poisson(lambda_param, num_points)
    _y = np.random.poisson(lambda_param, num_points)

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(_x, _y, color="blue", alpha=0.6, edgecolor="black")
    plt.title("Poisson Random Scatter Plot", fontsize=16)
    plt.xlabel("X-axis (Poisson samples)", fontsize=14)
    plt.ylabel("Y-axis (Poisson samples)", fontsize=14)
    plt.grid(True)
    plt.gca()
    return


@app.cell
def _():
    import ell
    from openai import OpenAI

    # Set up Google Gemini via OpenAI-compatible endpoint
    client = OpenAI(
        api_key="AIzaSyCEFfNiTQMmixAXreE88zfGRQ1AP-xsv1Q",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    ## Configure ell to use Ollama
    # client = OpenAI(
    #    base_url="https://chat.binghamton.edu/api",  # Ollama's OpenAI-compatible endpoint
    #    api_key="sk-7b747530179c4cc992159b7aaec18155",  # Dummy key, required but not used
    # )
    return (ell,)


@app.cell
def _():
    import polars as pl

    df = pl.read_csv("hf://datasets/scikit-learn/Fish/Fish.csv")
    return (df,)


@app.cell
def _(df, ell, mo):
    @ell.tool()
    def chart_data(x_encoding: str, y_encoding: str, color: str):
        """Generate an altair chart"""
        import altair as alt

        return (
            alt.Chart(df)
            .mark_circle()
            .encode(x=x_encoding, y=y_encoding, color=color)
            .properties(width=500)
        )


    @ell.tool()
    def filter_dataset(sql_query: str):
        """
        Filter a polars dataframe using SQL. Please only use fields from the schema.
        When referring to the table in SQL, call it 'data'.
        """
        filtered = df.sql(sql_query, table_name="data")
        return mo.ui.table(
            filtered,
            label=f"```sql\n{sql_query}\n```",
            selection=None,
        )


    from typing import List


    @ell.tool()
    def visualize_quiz_questions(quiz_question: str, answers: List[str]) -> str:
        """Generate quiz questions based on a given prompt."""
        return mo.ui.radio(
            label=quiz_question,
            options=answers,
            value=None,
        )


    lecture_content = """

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


    We recommend using [mamba](https://mamba.readthedocs.io/) and [uv](https://docs.astral.sh/uv/).
    Mamba is a tool for quickly installing Python and other packages, and for creating isolated environments for your projects.
    uv is a fast Python package and project manager. While we won't be running uv commands directly in this course, you'll need uv to properly run Marimo notebooks, which provides a much better development experience. [See here for installation instructions](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

    Follow the following steps to install mamba, uv, along with the minimum Python packages required for this course.

    1. [Install mamba] (https://github.com/conda-forge/miniforge)
    2. Run the following command to create a new environment with the minimum Python packages required for this course.

    ```bash
    mamba create -n advnetsci python==3.11 matplotlib scipy numpy pandas seaborn uv
    ```

    3. Activate the environment.

    ```bash
    mamba activate advnetsci
    ```

    4. Pip install marimo.

    ```bash
    pip install marimo
    ```

    ::: {.column-margin}

    <iframe width="250" height="125" src="https://www.youtube.com/embed/bwRgYxmCqLI?si=-PMkEhKuFW4IyMXW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

    :::



    #### Other Options

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

    #### Alternative Installation

    If you're not using uv, you can install marimo with pip:
    ```bash
    pip install marimo
    ```

    #### Running Marimo

    To start a new marimo notebook:

    ```bash
    marimo edit
    ```

    To open an existing marimo notebook:

    ```bash
    marimo edit notebook.py
    ```


    ## Github and GitHub Copilot

    We'll use GitHub for assignment collection and auto-grading in this course.

    ::: {.column-margin}

    <iframe width="250" height="150" src="https://www.youtube.com/embed/tRZGeaHPoaw?si=1zN_yNTx7O8bQYJJ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

    :::

    ### Minimum Requirements

    At the minimum level, you only need to:

    1. Create a GitHub account at [github.com](https://github.com)
    2. Know how to upload files to GitHub

    Detailed instructions on how to upload your assignments to GitHub will be provided separately - advanced Git features are not required for the course. See this [assignment example](https://github.com/sk-classroom/starter) to get familiar with the format.

    ### Subscribing to GitHub Copilot

    We strongly encourage you to use [GitHub Copilot](https://github.com/features/copilot), an AI-powered coding assistant that helps you write code faster and more efficiently.
    GitHub Copilot is an AI pair programmer that provides intelligent code suggestions, completions, and explanations directly in code editor, including VS Code and Marimo.

    Students can get free access to GitHub Copilot Pro, which includes enhanced features and priority access. Visit the [GitHub Copilot Pro free access page](https://docs.github.com/en/copilot/how-tos/manage-your-account/get-free-access-to-copilot-pro) to get started.

    Marimo notebook supports GitHub Copilot out of the box. [See the instruction](https://docs.marimo.io/guides/editor_features/ai_completion/#github-copilot) to enable it. If you are using VS Code, you can also install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) to get the same experience.



    ### For Students Interested in Learning More {.unnumbered}

    Understanding Git and GitHub is useful for seamlessly working with assignments and will benefit your programming workflow. Additionally, Git and GitHub integrate nicely with AI tools for productivity improvement, making your development process more efficient.


    ::: {.column-margin}

    Git(Hub) and AI tools are like a pair of best friends. Git ensures that all edits are tracked and can be reverted. GitHub makes it easy for you to collaborate with (multiple) AI agents with you.


    <iframe width="250" height="150" src="https://www.youtube.com/embed/vygKnE5M6as?si=UB54u4asmVzmv9M6" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


    <iframe width="250" height="150" src="https://www.youtube.com/embed/NKkO8JL6IJg?si=Yv57-uVHLRQrtT5w" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    :::


    #### GitHub Desktop (Recommended for Beginners)

    If you want to learn more about version control, start with [GitHub Desktop](https://desktop.github.com/), a user-friendly graphical interface:

    1. Go to [desktop.github.com](https://desktop.github.com/)
    2. Download for your operating system
    3. Install and sign in with your GitHub account

    #### Understanding Git and Version Control

    Git is a version control system that tracks changes in your code over time. Think of it as a sophisticated "save" system that:

    - Keeps a complete history of all changes to your files
    - Lets you go back to any previous version
    - Allows multiple people to work on the same project simultaneously
    - Helps you manage different versions or "branches" of your work

    GitHub is a cloud-based platform that hosts Git repositories and adds collaboration features.

    #### Learning Resources

    Essential resources to understand Git concepts:

    - [Interactive Git Tutorial](https://learngitbranching.js.org/) - Visual, hands-on learning
    - [GitHub Desktop Documentation](https://docs.github.com/en/desktop) - Official desktop app guide
    - [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) - Detailed tutorials with examples

    """
    return (lecture_content,)


@app.cell
def _(lecture_content):
    import marimo as mo

    config = mo.ai.ChatModelConfig(
        max_tokens=2000,
        temperature=0.5,
        top_p=0.9,
        top_k=10,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    mo.ui.chat(
        mo.ai.llm.google(
            "gemini-2.5-flash-lite",
            system_message=f"You are a helpful tutor for students. Output your answer in markdown. Lecture Content: {lecture_content}",
            api_key="AIzaSyCEFfNiTQMmixAXreE88zfGRQ1AP-xsv1Q",
        ),
        # Provide some sample prompts
        prompts=[
            "What is the chemical formula for water?",
            "What is the chemical formula for carbon dioxide?",
            "What is the chemical formula for {{compound}}?",
        ],
        # Show some configuration controls to change temperature, token limit, etc.
        show_configuration_controls=True,
        config=config,
    )
    return (mo,)


app._unparsable_cell(
    r"""
        \"\"\"You are a data scientist that can analyze a dataset\"\"\"
        return f\"I have a dataset with schema: {df.schema}. \n{prompt}\"
    """,
    name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
