# /// script
# dependencies = [
#     "cairocffi==1.7.1",
#     "marimo",
#     "matplotlib==3.10.5",
#     "numpy==2.2.6",
#     "pycairo==1.28.0",
#     "python-igraph==0.11.9",
#     "scipy==1.15.3",
#     "seaborn==0.13.2",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App(width="full")

with app.setup(hide_code=True):
    # Initialization code that runs before all other cells
    import numpy as np
    import igraph


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Assignment: Respondent Sampling


    ## Preparation: Respondent Driven Sampling

    Imagine you want to learn about the social media habits of a big group of people, but you don't have a list of everyone—and even if you did, not everyone would answer your survey! This is where Respondent Driven Sampling (RDS) comes to the rescue. RDS is a popular way to reach hard-to-reach groups in social sciences.

    <div style="display: flex; justify-content: center;">
        <img src="https://tgmresearch.com/templates/yootheme/cache/27/snowball-sampling-method-27fdb322.webp" style="width:500px;">
    </div>

    Here's how it works: you start by picking a few people at random (these are your “seeds”). Each seed gets a handful of “coupons” to invite their friends to join the survey. When those friends participate, they get their own coupons to pass along, and so on. The survey spreads through the network.

    Now, we will simulate the survey process, and your goal is to estimate, as best as you can, the distribution of platform preferences in the population.
    **Note that the survey data is biased due to the friendship paradox**, and your task is to implement an estimator that is less biased by naive counts of the original survey data.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 📋 Assignment Instructions & Grading""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "📋 Assignment Tasks": mo.md(
                r"""
            Complete the following task and upload your notebook to your GitHub repository.

            1. **Task 1**: Implement `compute_ccdf`
            2. **Task 2**: Implement `estimate_platform_distribution`
            3. Update this notebook by using `git add`, `git commit`, and then `git push`.
            4. The notebook will be automatically graded, and your score will be shown on GitHub.
            """
            ),
            "🔒 Protected Files": mo.md(
                r"""
            Protected files are test files and configuration files you cannot modify. They appear in your repository but don't make any changes to them.
            """
            ),
            "⚖️ Academic Integrity": mo.md(
                r"""
            There is a system that automatically checks code similarity across all submissions and online repositories. Sharing code or submitting copied work will result in zero credit and disciplinary action.

            While you can discuss concepts, each student must write their own code. Cite any external resources, including AI tools, in your comments.
            """
            ),
            "📚 Allowed Libraries": mo.md(
                r"""
            You **cannot** import any other libraries that result in the grading script failing or a zero score. Only use: `numpy`, `pandas`, `scipy`
            """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Survey data

    We ask each survey participant to provide the primary social media platform they use, along with the number of coupons they sent out to their friends ("degree").
    There is no limit on the number of coupons a participant can send out. The individual recipients of the coupons participate in the survey with a probability of 0.15 independently of each other.
    The survey data is stored as a pandas dataframe as follows:
    """
    )
    return


@app.cell(hide_code=True)
def _(simulation_results):
    survey_data = simulation_results[0]["survey_data"]
    survey_data
    return (survey_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Observe that there is a **correlation** between the platform preference and the degree of the node. What correlation do you see here? You can get an idea by sorting the table by the ascending/descending order of degree. Click the column "degree" and see the table in different sorting order."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Implementation example

    Here is an example implementation of your estimator. This function computes the percentage of the platform preferences of the participants in the survey data.
    """
    )
    return


@app.function
def estimate_naive_platform_distribution(survey_data):
    """
    Estimate the unbiased distribution of social media platform preferences using degree-based correction.

    Args:
        survey_data (pandas.DataFrame): pandas.DataFrame for survey responses consisting of platform names, degree, and participant IDs.

    Returns:
        list of tuples: Unbiased estimate as [(platform, percentage), ...] e.g., [("Facebook", 0.3), ("Instagram", 0.2), ("LinkedIn", 0.1), ...]

    """

    counts = survey_data.groupby("platform").size().to_dict()

    total = survey_data["platform"].shape[0]

    result = [
        (platform, counts[platform] / total) for platform in counts.keys()
    ]
    return result


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""This estimator won't be accurate because the participants are a biased subset of the whole population. To see this point clearly, let us see which nodes in the network participate in the survey. Below is the social network of the individuals including both participants and non-participants. Edges are not drawn to save computational cost. High-degree nodes are placed near the center and low-degree nodes are on the periphery of the plot."""
    )
    return


@app.cell(hide_code=True)
def _(
    alpha,
    bias_expo,
    g_backborn,
    platform_list,
    run_simulation,
    vis_single_network,
):
    np.random.seed(32)
    (
        _g_perc,
        _node_platform_preferences,
        _survey_data,
        _initial_participants,
    ) = run_simulation(
        g=g_backborn,
        initial_sample_size=10,
        participation_prob=0.2,
        alpha=alpha,
        bias_expo=bias_expo,
        platform_list=platform_list,
    )
    _deg_perc = np.array(_g_perc.degree())
    is_participant = [
        "Participant" if s > 0 else "Non-participant" for s in _deg_perc
    ]
    _fig = vis_single_network(g_backborn, node_labels=is_participant)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The node size represents the degree of the node. We see that the participants tend to have a larger degree.
    Let us go deeper into this by focusing on the degree distributions. Your first task is to implement the *complementary cumulative distribution function* (CCDF) of a given degree sequence. Implement the CCDF function.
    """
    )
    return


@app.function
# Task 1
def compute_ccdf(degree_sequence):
    """
    Compute the complementary cumulative distribution function of a given degree sequence.

    The CCDF at a given point x (denoted by F(x)) is given by the fraction of data points y that is **greater than** x.

    F(x) = P(y>x)

    Args:
        degree_sequence (numpy.ndarray): An array of integers representing the degree sequence.

    Returns:
        ccdf (list of tuples): Complementary cumulative distribution function as [(degree, percentage), ...] e.g., [(1, 0.3), (2, 0.2), (3, 0.1), ...].
    """
    pass


@app.cell(hide_code=True)
def _(create_ccdf_chart, g_backborn, simulation_results):
    _sample_id = 0
    _sample_data = simulation_results[_sample_id]
    _fig = create_ccdf_chart(g_backborn, _sample_data["g_perc"], compute_ccdf)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Observe that the degree distribution of the participants in the survey is much more concentrated in the higher degrees, a hallmark of the friendship paradox.
    This is why the naive estimator is not accurate.


    Now, let's implement a better estimator. Your goal is to provide an estimate better than the naive approach. Any idea can be implemented. A way to improve the estimate is to take into account the friendship paradox 😉. Think about which nodes are likely to be sampled, to what extent, and way to correct for the bias. If a node has 10 edges in the network, how likely is the node sampled compared to a node with one edge?
    """
    )
    return


@app.function
# Task 2
def estimate_platform_distribution(survey_data):
    """
    Estimate the unbiased distribution of social media platform preferences using degree-based correction.

    Args:
        survey_data (pandas.DataFrame): pandas.DataFrame for survey responses consisting of platform names, degree, and participant IDs.

    Returns:
        list of tuples: Unbiased estimate as [(platform, percentage), ...] e.g., [("Facebook", 0.3), ("Instagram", 0.2), ("LinkedIn", 0.1), ...]

    """
    pass


@app.cell(hide_code=True)
def _(mo):
    # Create interactive controls
    button = mo.ui.run_button(label="(Re-)Run simulation", kind="success")

    mo.md(f"""
    ### Simulations

    Let's run the simulation and measure the estimation errors by the Mean Squared Error (MSE). We will run 10 simulations and evaluate the error averaged over the simulations. Below, we show one of the ten simulation result on the left, and the error distribution across the 10 simulations on the right. Aim for 2 times smaller error than the naive estimate.

    {button}

    """)
    return (button,)


@app.cell(hide_code=True)
def _(
    alpha,
    bias_expo,
    button,
    g_backborn,
    initial_sample_size,
    mo,
    n_simulations,
    participation_prob,
    platform_list,
    run_simulation,
):
    # Run simulation when button clicked or sliders change
    if button.value:
        _a = 1  # dummy
    else:
        _a = 3  # dummy

    simulation_results = []
    with mo.status.progress_bar(total=n_simulations) as bar:
        for _ in range(n_simulations):
            while True:
                (
                    _g_perc,
                    _node_platform_preferences,
                    _survey_data,
                    _initial_participants,
                ) = run_simulation(
                    g=g_backborn,
                    initial_sample_size=initial_sample_size,
                    participation_prob=participation_prob,
                    alpha=alpha,
                    bias_expo=bias_expo,
                    platform_list=platform_list,
                )
                if len(_survey_data) > 200:
                    break

            simulation_results.append(
                {
                    "node_platform_preferences": _node_platform_preferences,
                    "survey_data": _survey_data,
                    "initial_participants": _initial_participants,
                    "g_perc": _g_perc,
                }
            )
            bar.update()
    return (simulation_results,)


@app.cell(hide_code=True)
def _(
    create_comparison_chart,
    create_error_chart,
    error_table,
    mo,
    platform_list,
    simulation_results,
    survey_data,
):
    _fig1 = create_comparison_chart(
        survey_data,
        simulation_results[0]["node_platform_preferences"],
        platform_list,
    )
    _fig2 = create_error_chart(error_table)

    mo.hstack([_fig1, _fig2], justify="center", align="center")
    return


@app.cell(hide_code=True)
def _(error_table, mo):
    error_naive = (
        error_table.query("estimator == 'naive'")
        .sort_values("sample_id")["MSE"]
        .values
    )
    error_corrected = (
        error_table.query("estimator == 'corrected'")
        .sort_values("sample_id")["MSE"]
        .values
    )

    success_rate = np.mean(error_naive > error_corrected)

    ret = ""
    if success_rate > 0.7:
        ret = mo.callout(
            mo.md(f"""Your corrected estimator outperformed the naive estimator in {success_rate * 100:.1f}% of simulations.
            <br>
            Mean Squared Error (MSE) for your estimator: {np.mean(error_corrected):.6f}
            <br>
            Mean Squared Error (MSE) for naive estimator: {np.mean(error_naive):.6f}

            Note that, even if successful, the test may fail especially when the success rate is close to the grading threshold (70%) due to the stochastic nature of the simulations.
            """),
            kind="success",
        )
    else:
        ret = mo.callout(
            mo.md(f"""Your corrected estimator outperformed the naive estimator in only {success_rate * 100:.1f}% of simulations.
            <br>
            Mean Squared Error (MSE) for your estimator: {np.mean(error_corrected):.6f}
            <br>
            Mean Squared Error (MSE) for naive estimator: {np.mean(error_naive):.6f}
            <br>
            Aim for >70% success rate. If you are below this, consider revisiting your weighting logic.
            """),
            kind="danger",
        )

    ret
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Let us remind that there is a correlation betweeen the platform preference and the degree, i.e., hubs tend to prefer the popular platforms. Combined with the friendship paradox, the naive estimate tends to overestimate the percentage for the popular platforms substantially."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Code

    The following cells are for the codes for running simulations and creating the visualizations. Welcome to review and change the code. Try out different parameters if you like to see how underlying network topology affects the friendship paradox, along with the hubs' preferen bias towards popular platforms
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Simulation""")
    return


@app.cell
def _():
    # Number of edges to attach from a new node to existing nodes in the Barabási–Albert model
    m = 2

    # Total number of nodes in the generated network
    n_nodes = 3000

    # Number of initial "seed" participants in the RDS simulation
    initial_sample_size = 5

    # Probability that a recruited friend will participate in the survey
    participation_prob = 0.15

    # Alpha parameter controls the strength of hubs' preference towards popular platforms. Lower value leads to a stronger preference bias.
    alpha = 1e-2

    # Exponent for biasing the platform preference distribution (higher = more skewed)
    bias_expo = 2.0

    # Generate the underlying social network using the Barabási–Albert preferential attachment model
    g_backborn = igraph.Graph.Barabasi(n=n_nodes, m=m)

    # Number of simulations
    n_simulations = 10

    platform_list = [
        "Facebook",
        "Instagram",
        "LinkedIn",
        "TikTok",
        "X",
        "YouTube",
    ]
    return (
        alpha,
        bias_expo,
        g_backborn,
        initial_sample_size,
        n_simulations,
        participation_prob,
        platform_list,
    )


@app.cell(hide_code=True)
def _(pd, run_percolation, sparse):
    # Generate network based on slider values (reactive to changes)
    def run_simulation(
        g,
        initial_sample_size,
        participation_prob,
        alpha,
        bias_expo,
        platform_list,
    ):
        np.random.shuffle(platform_list)
        # g = igraph.Graph.Barabasi(n=n_nodes, m=m)
        A = g.get_adjacency_sparse()
        citing, cited, _ = sparse.find(A)
        n_nodes = g.vcount()

        _deg = np.array(g.degree())
        _deg_norm = _deg / np.max(_deg)

        platform_bias = np.random.rand(len(platform_list)) ** bias_expo
        platform_bias /= np.max(platform_bias)

        # P is the probability of a node choosing a platform
        P = np.exp(np.outer(_deg_norm, platform_bias) / alpha)
        P /= np.sum(P, axis=1, keepdims=True)
        gumbel = np.random.gumbel(size=P.shape)
        preference_platform_ids = np.argmax(np.log(P) + gumbel, axis=1)
        preferences = np.array(platform_list)[preference_platform_ids]

        # Simulate network survey sampling (friend recruitment)
        survey_participants = []
        survey_data = []

        # Step 1: Start with random initial sample
        total_nodes = g.vcount()
        initial_participants = np.random.choice(
            total_nodes, size=initial_sample_size, replace=False
        ).tolist()

        # Step 2: Percolate the network by removing each edge with probability 1-p
        g_perc = run_percolation(g, initial_participants, participation_prob)

        # Step 3: For each initial participant, get their connected component in the percolated graph
        membership = np.array(g_perc.connected_components(mode="weak").membership)
        # Find all unique component ids for the initial participants
        component_ids = np.unique(membership[initial_participants])
        # All nodes in any of these components are participants
        participants = np.where(np.isin(membership, component_ids))[0]

        # Step 4: Collect survey responses
        degree = np.array(g.degree())

        survey_data = pd.DataFrame(
            {
                "participants": participants,
                "platform": preferences[participants],
                "degree": degree[participants],
            }
        )
        return g_perc, preferences, survey_data, initial_participants
    return (run_simulation,)


@app.cell(hide_code=True)
def _(pd, platform_list, simulation_results):
    def run_estimators(simulation_results, platform_list):
        result_tables = []
        errors = []
        for _i, result in enumerate(simulation_results):
            # True population distribution (ground truth from all nodes)
            # node_platform_preferences is a numpy array of all node preferences
            _true_counts = (
                pd.Series(result["node_platform_preferences"])
                .value_counts()
                .reindex(platform_list, fill_value=0)
            )
            _true_total = _true_counts.sum()
            _true_prop = _true_counts / _true_total

            # Naive estimate: just raw survey proportions (from survey_data)
            _naive_result = estimate_naive_platform_distribution(
                result["survey_data"]
            )
            _naive_df = (
                pd.DataFrame(_naive_result, columns=["platform", "proportion"])
                .set_index("platform")
                .reindex(platform_list, fill_value=0)
            )
            _naive_prop = _naive_df["proportion"].values

            # Corrected estimate using the student's function
            _corrected_result = estimate_platform_distribution(
                result["survey_data"]
            )
            _corrected_df = (
                pd.DataFrame(_corrected_result, columns=["platform", "proportion"])
                .set_index("platform")
                .reindex(platform_list, fill_value=0)
            )
            _corrected_dist = _corrected_df["proportion"].values

            # Create master table
            _result_table = pd.DataFrame(
                {
                    "True Proportion": _true_prop,
                    "Naive Proportion": _naive_prop,
                    "Estimated Proportion": _corrected_dist,
                },
                index=platform_list,
            )
            result_tables.append(_result_table)
            # Compute errors
            _naive_error = np.mean((_naive_prop - _true_prop) ** 2)
            _corrected_error = np.mean((_corrected_dist - _true_prop) ** 2)
            errors.append(
                {"estimator": "naive", "MSE": _naive_error, "sample_id": _i}
            )
            errors.append(
                {
                    "estimator": "corrected",
                    "MSE": _corrected_error,
                    "sample_id": _i,
                }
            )
        error_table = pd.DataFrame(errors)
        return result_tables, error_table


    estimation_result_tables, error_table = run_estimators(
        simulation_results, platform_list
    )
    return (error_table,)


@app.cell(hide_code=True)
def _(heapq):
    def run_percolation(graph, seed, edge_prob):
        """
        Find the minimum spanning tree (MST) of a graph using Prim's algorithm,
        starting from the specified seed node.

        Parameters:
            graph: igraph.Graph
                The input undirected, weighted graph.
            seed: int
                The index of the starting node.

        Returns:
            mst_graph: igraph.Graph
                The MST as an igraph.Graph object, with the same node ids as the input.
        """

        n = graph.vcount()
        if isinstance(seed, int):
            seed = [seed]
        visited = set(seed)
        mst_edges = []
        edge_heap = []

        # Add all edges from the seed node to the heap
        for s in seed:
            for neighbor in graph.neighbors(s):
                eid = graph.get_eid(s, neighbor)
                weight = (
                    graph.es[eid]["weight"]
                    if "weight" in graph.es.attributes()
                    else 1.0
                )
                heapq.heappush(edge_heap, (weight, s, neighbor))

        while len(visited) < n and edge_heap:
            weight, u, v = heapq.heappop(edge_heap)
            if np.random.rand() > edge_prob:
                continue
            if v in visited:
                continue
            # Add edge to MST
            mst_edges.append((u, v, weight))
            visited.add(v)
            # Add all edges from the new node to the heap
            for neighbor in graph.neighbors(v):
                if neighbor not in visited:
                    eid = graph.get_eid(v, neighbor)
                    w = (
                        graph.es[eid]["weight"]
                        if "weight" in graph.es.attributes()
                        else 1.0
                    )
                    heapq.heappush(edge_heap, (w, v, neighbor))

        # Create MST igraph object with the same node ids and attributes
        mst_graph = igraph.Graph()
        mst_graph.add_vertices(graph.vcount())
        # Copy vertex attributes
        for attr in graph.vs.attributes():
            mst_graph.vs[attr] = graph.vs[attr]
        # Add edges and weights
        mst_graph.add_edges([(u, v) for u, v, w in mst_edges])
        if "weight" in graph.es.attributes():
            mst_graph.es["weight"] = [w for u, v, w in mst_edges]
        return mst_graph
    return (run_percolation,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization""")
    return


@app.cell(hide_code=True)
def _(pd, plt, sns):
    def vis_single_network(g, node_labels=None):
        # Visualize the network g using igraph's plotting functionality

        sns.set_style("white")
        sns.set(font_scale=1.2)
        sns.set_style("ticks")

        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        degree = np.array(g.degree())

        # Max scaling
        degree_norm = degree / np.max(degree)

        angles = np.random.randn(len(degree), 2)
        angles = np.einsum(
            "ij,i->ij", angles, 1.0 / np.linalg.norm(angles, axis=1).reshape(-1)
        )

        xy = np.einsum(
            "ij,i->ij",
            angles,
            np.min(degree_norm) / (degree_norm + np.median(degree_norm)),
        )

        _data_table = pd.DataFrame(
            {"x": xy[:, 0], "y": xy[:, 1], "degree": degree}
        )

        cmap = sns.color_palette("bright")

        if node_labels is not None:
            # Plot only the nodes, not the edges
            _data_table["label"] = node_labels
            sns.scatterplot(
                _data_table,
                x="x",
                y="y",
                size="degree",
                hue="label",
                sizes=(5, 150),
                ax=ax,
                palette={
                    "Participant": cmap[1],
                    "Non-participant": cmap[0],
                },
                edgecolors="white",
                linewidth=1,
            )
        else:
            sns.scatterplot(
                _data_table, x="x", y="y", size="degree", sizes=(5, 350), ax=ax
            )

        if node_labels is not None:
            ax.legend(
                loc="lower left",
                bbox_to_anchor=(1, 0),
                facecolor="none",
                edgecolor="none",
                labelcolor="white",
            )
        ax.axis("off")

        # Set spine colors (figure boundaries) to white
        for spine in ax.spines.values():
            spine.set_color("white")

        return fig
    return (vis_single_network,)


@app.cell(hide_code=True)
def _(pd, plt, sns):
    def create_comparison_chart(
        survey_data, node_platform_preferences, platform_list
    ):
        # Only create a single bar chart (no network plot)
        fig, ax2 = plt.subplots(1, 1, figsize=(8, 6))
        # Set transparent background
        fig.patch.set_alpha(0.0)
        ax2.patch.set_alpha(0.0)

        # True population distribution (ground truth from all nodes)
        # node_platform_preferences is a numpy array of all node preferences
        true_counts = (
            pd.Series(node_platform_preferences)
            .value_counts()
            .reindex(platform_list, fill_value=0)
        )
        true_total = true_counts.sum()
        true_prop = true_counts / true_total

        # Naive estimate: just raw survey proportions (from survey_data)
        naive_result = estimate_naive_platform_distribution(survey_data)
        naive_df = (
            pd.DataFrame(naive_result, columns=["platform", "proportion"])
            .set_index("platform")
            .reindex(platform_list, fill_value=0)
        )
        naive_prop = naive_df["proportion"].values

        # Corrected estimate using the student's function
        corrected_result = estimate_platform_distribution(survey_data)
        corrected_df = (
            pd.DataFrame(corrected_result, columns=["platform", "proportion"])
            .set_index("platform")
            .reindex(platform_list, fill_value=0)
        )
        corrected_dist = corrected_df["proportion"].values

        # Create master table
        master_table = pd.DataFrame(
            {
                "True Proportion": true_prop,
                "Naive Proportion": naive_prop,
                "Estimated Proportion": corrected_dist,
            },
            index=platform_list,
        )

        # Create grouped bar chart using seaborn
        plot_df = master_table.reset_index().melt(
            id_vars="index",
            value_vars=[
                "True Proportion",
                "Naive Proportion",
                "Estimated Proportion",
            ],
            var_name="Estimate",
            value_name="Proportion",
        )
        plot_df.rename(columns={"index": "Platform"}, inplace=True)
        estimate_palette = {
            "True Proportion": "#fff3cc",
            "Naive Proportion": "#fafafa",
            "Estimated Proportion": "yellow",
        }

        sns.barplot(
            data=plot_df,
            x="Platform",
            y="Proportion",
            hue="Estimate",
            ax=ax2,
            palette=estimate_palette,
        )

        ax2.set_xlabel("Social Media Platform", color="white")
        ax2.set_ylabel("Proportion", color="white")
        ax2.set_title("Distribution Comparison", color="white")
        ax2.set_xticks(range(len(master_table.index)))
        ax2.set_xticklabels(master_table.index)

        # Set tick colors to white
        ax2.tick_params(axis="x", colors="white")
        ax2.tick_params(axis="y", colors="white")

        # Set spine colors (figure boundaries) to white
        for spine in ax2.spines.values():
            spine.set_color("white")

        ax2.legend(facecolor="none", edgecolor="none", labelcolor="white")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig
    return (create_comparison_chart,)


@app.cell(hide_code=True)
def _(plt, sns):
    def create_error_chart(error_table):
        # Use seaborn to create a scatter plot: x = sample id, y = error, hue = estimator

        # Assign sample ids: every two rows (naive/corrected) correspond to one simulation
        error_table = error_table.copy()
        error_table["sample_id"] = error_table.groupby("estimator").cumcount()

        sns.set_style("white")
        sns.set(font_scale=1.2)
        sns.set_style("ticks")

        fig, ax = plt.subplots(figsize=(6, 6))
        # Set transparent background
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        cmap = sns.color_palette()

        # Create a color map for the estimators
        estimator_colors = {"naive": cmap[0], "corrected": cmap[1]}

        # Use seaborn scatterplot
        sns.scatterplot(
            data=error_table,
            x="sample_id",
            y="MSE",
            hue="estimator",
            style="estimator",
            ax=ax,
            palette=estimator_colors,
            s=80,
        )

        # Add horizontal lines for average MSE of each estimator
        for estimator, color in zip(
            ["naive", "corrected"],
            [estimator_colors["naive"], estimator_colors["corrected"]],
        ):
            mean_mse = error_table.loc[
                error_table["estimator"] == estimator, "MSE"
            ].mean()
            ax.axhline(
                mean_mse,
                color=color,
                linestyle="--",
                linewidth=2,
                alpha=0.7,
                label=f"{estimator} mean",
            )

        ax.set_xlabel("Simulation Sample ID", color="white")
        ax.set_ylabel("Mean Squared Error (MSE)", color="white")
        ax.set_title("Estimator Error per Simulation", color="white")
        ax.grid(True, alpha=0.3)

        # Set tick colors to white
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")

        # Set spine colors (figure boundaries) to white
        for spine in ax.spines.values():
            spine.set_color("white")

        # To avoid duplicate legend entries for mean lines, use legend only for scatter
        handles, labels = ax.get_legend_handles_labels()
        # Remove duplicate mean lines
        seen = set()
        new_handles = []
        new_labels = []
        for h, l in zip(handles, labels):
            if l not in seen:
                new_handles.append(h)
                new_labels.append(l)
                seen.add(l)
        ax.legend(
            new_handles,
            new_labels,
            facecolor="none",
            edgecolor="none",
            labelcolor="white",
        )
        return fig
    return (create_error_chart,)


@app.cell(hide_code=True)
def _(plt, sns):
    def create_ccdf_chart(g_backborn, g_perc, compute_ccdf):
        # Compute degree sequences
        degrees_backbone = np.array(g_backborn.degree())
        degrees_perc = np.array(g_perc.degree())

        is_nonzero_degree = degrees_perc > 0
        degrees_perc = degrees_backbone[is_nonzero_degree]  # Remove zero degrees

        # Compute CCDFs
        ccdf_backbone = compute_ccdf(degrees_backbone)
        ccdf_perc = compute_ccdf(degrees_perc)

        # Unpack for plotting
        deg_b, ccdf_b = zip(*ccdf_backbone)
        deg_p, ccdf_p = zip(*ccdf_perc)

        sns.set_style("white")
        sns.set(font_scale=1.2)
        sns.set_style("ticks")
        _fig, _ax = plt.subplots(figsize=(7, 5))
        # Set transparent background
        _fig.patch.set_alpha(0.0)
        _ax.patch.set_alpha(0.0)

        sns.lineplot(x=deg_b, y=ccdf_b, marker="o", label="Population", ax=_ax)
        sns.lineplot(x=deg_p, y=ccdf_p, marker="s", label="Participants", ax=_ax)
        _ax.set_xlabel("Degree", color="white")
        _ax.set_ylabel("CCDF", color="white")
        _ax.set_title(
            "Degree CCDF of Backbone and Percolated Networks", color="white"
        )

        # Set tick colors to white
        _ax.tick_params(axis="x", colors="white")
        _ax.tick_params(axis="y", colors="white")

        # Set spine colors (figure boundaries) to white
        for spine in _ax.spines.values():
            spine.set_color("white")

        _ax.legend(facecolor="none", edgecolor="none", labelcolor="white")
        _ax.set_xscale("log")
        _ax.set_yscale("log")
        return _fig
    return (create_ccdf_chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Libraries""")
    return


@app.cell
def _():
    # All imports in one place to avoid conflicts
    import marimo as mo
    import matplotlib.pyplot as plt
    from scipy import sparse
    import seaborn as sns
    from matplotlib.lines import Line2D
    import heapq
    import pandas as pd
    return heapq, mo, pd, plt, sns, sparse


if __name__ == "__main__":
    app.run()
