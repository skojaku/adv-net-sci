# Premade cells for checkpoint cp1_milgram — the experiment picture.
# Format: cells split by "# --- cell: <name> ---" markers, inserted in order.
# describe: The Milgram experiment photo (letters passed hand to hand from Nebraska to Boston).
# --- cell: cp1_milgram_img ---
mo.vstack([
    mo.image(
        src="assets/milgram-small-world-experiment.png",
        width=520,
        caption="Milgram's letter experiment (1960s)",
    ),
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>Read the picture as a "
        "relay. A packet starts with a randomly chosen person in Omaha, "
        "Nebraska, and has to reach one named stockbroker near Boston. Nobody "
        "may post it directly: each holder passes it to a single person they "
        "know on a first-name basis and who they think sits closer to the "
        "target. Each arrow is one such hand-off. The drawing shows the idea, "
        "not the result.</span>"
    ),
])
