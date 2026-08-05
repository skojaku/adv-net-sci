# Premade cell for checkpoint cp2_paperwork — photo upload area for the
# by-hand distance table (5-person ring, done entirely on paper).
# The student tells the tutor in the terminal once the photo is up; the
# tutor then calls nb_view_image(widget="cp2_paperwork_photo", ...) to see it
# (that call also creates the in-notebook photo-view cell automatically).
# describe: A photo upload area for the student's hand-worked distance table.
# --- cell: cp2_paperwork_photo ---
cp2_paperwork_photo = mo.ui.file(
    kind="area",
    filetypes=[".jpg", ".jpeg", ".png", ".webp"],
    label="Photo of your paper work",
)
mo.vstack([
    cp2_paperwork_photo,
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
        "your paper here — the 5-dot ring, your list of all 10 pairs with a "
        "distance beside each, and the average at the bottom. Working shown "
        "beats a tidy answer. Once it is up, say so in the terminal.</span>"
    ),
])
