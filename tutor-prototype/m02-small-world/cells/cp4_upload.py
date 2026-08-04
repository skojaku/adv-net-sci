# Premade cell for checkpoint cp4_shortcut_drawing — photo upload area.
# Insert with done_signal="cp4_shortcut_drawing" to get the Done button.
# describe: A photo upload area for the student's hand drawing.
# --- cell: cp4_photo ---
cp4_photo = mo.ui.file(
    kind="area",
    filetypes=[".jpg", ".jpeg", ".png", ".webp"],
    label="Photo of your drawing",
)
cp4_photo
