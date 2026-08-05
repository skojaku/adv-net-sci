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
cp2_paperwork_photo
