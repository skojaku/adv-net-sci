# Premade cell for checkpoint cp5_ring_formula — photo upload area for the
# C(k) / L(N,k) derivation work (triangle count + formula reasoning, on paper).
# The student tells the tutor in the terminal once the photo is up; the
# tutor then calls nb_view_image(widget="cp5_ring_paperwork_photo", ...) to
# see it (that call also creates the in-notebook photo-view cell).
# describe: A photo upload area for the student's hand-worked triangle count and formula reasoning.
# --- cell: cp5_ring_paperwork_photo ---
cp5_ring_paperwork_photo = mo.ui.file(
    kind="area",
    filetypes=[".jpg", ".jpeg", ".png", ".webp"],
    label="Photo of your ring working (triangles + formulas)",
)
mo.vstack([
    cp5_ring_paperwork_photo,
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
        "your derivation here — node 0's friends, which pairs among them "
        "already know each other, and the two formulas you ended up with. "
        "Crossings-out are fine and welcome. Once it is up, say so in the "
        "terminal.</span>"
    ),
])
