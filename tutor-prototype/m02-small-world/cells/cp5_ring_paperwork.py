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
cp5_ring_paperwork_photo
