# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "networkx",
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🌍 The Small-World Puzzle

    *Advanced Network Science — Module 02*

    This notebook starts almost empty — **that's on purpose.**
    Your AI tutor will build it with you, step by step, in the terminal
    window next to this one.

    **How this works:**

    - 💬 The **terminal** is where you and your tutor talk.
    - 📓 This **notebook** is your shared whiteboard. Questions and
      experiments will appear here as you go.
    - ✏️ You can answer in the notebook *or* just type your answer in the
      terminal — whichever feels easier. Both always work.
    - 🧭 Ask anything, anytime. Detours are encouraged.

    No programming experience needed. Say hello in the terminal to begin!
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):

    cp0_name = mo.ui.text(label="What should I call you?")
    cp0_python = mo.ui.radio(
        options=["I don't code", "I've tried a little Python", "I'm comfortable with Python"],
        label="How do you feel about Python?")

    mo.md(
        f"""
        ## 👋 Welcome!

        Let's get started. Tell me a bit about yourself:

        {cp0_name}
        {cp0_python}

        Answer here, or type in the terminal — both work!
        """
    )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### ✉️ Milgram's letter experiment (1960s)

    1960s, **Omaha, Nebraska**. Stanley Milgram hands 160 researchers a packet.
    Goal: get it to a specific **stockbroker in Boston** — but you may only
    forward it to someone you know on a first-name basis.

    No maps. No internet. Just passing it friend-to-friend.
    """)
    return


@app.cell(hide_code=True)
def _(mo):

    cp1_answer = mo.ui.radio(
        options=["about 6", "about 20", "about 60", "over 200"],
        label="For the letters that made it, how many hands did they pass through on average?",
    )

    mo.md(
        f"""
        ### 🎲 Your prediction

        {cp1_answer}
        """
    )

    return


@app.cell(hide_code=True)
def _(mo):

    cp2_dist = mo.ui.text(label="Distance (shortest path length) from A to D?")
    cp2_avg = mo.ui.text(label="Average path length over all 6 pairs? (fraction or decimal ok)")

    mo.md(
        f"""
        ### 🧮 Distance warm-up

        Look at the gold node **A**. To get to **D**, count **edges** (lines), not nodes.

        {cp2_dist}
        {cp2_avg}
        """
    )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 🧪 Another example

    **3 nodes in a line:** A — B — C

    Pairs:
    - A-B: distance = 1 (direct link)
    - B-C: distance = 1 (direct link)
    - A-C: distance = 2 (A → B → C)

    Sum = 1 + 1 + 2 = 4. Over 3 pairs: average = 4/3 ≈ 1.33

    **Distance = shortest number of edges between two nodes.**
    Count edges, not nodes!
    """)
    return


@app.cell
def _(mo):

    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")])

    pos = nx.circular_layout(G)
    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightblue",
                           edgecolors="black", linewidths=2, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=["A"], node_size=1500,
                           node_color="gold", edgecolors="black", linewidths=2, ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=18, font_weight="bold", ax=ax)
    ax.set_title("Distance puzzle — A is gold", fontsize=14)
    ax.axis("off")
    mo.mpl.interactive(fig)

    return


if __name__ == "__main__":
    app.run()
