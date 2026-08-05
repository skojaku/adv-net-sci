# Premade cell for checkpoint cp4_shortcut_drawing — photo upload area.
# The student tells the tutor in the terminal once the photo is up.
# describe: A photo upload area for the student's hand drawing.
# --- cell: cp4_photo ---
cp4_photo = mo.ui.file(
    kind="area",
    filetypes=[".jpg", ".jpeg", ".png", ".webp"],
    label="Photo of your drawing",
)
mo.vstack([
    cp4_photo,
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
        "your 8-dot ring here — the drawing with your one extra cable on it. "
        "It does not need to be neat; it needs to show which two dots you "
        "joined. Once it is up, say so in the terminal.</span>"
    ),
])
