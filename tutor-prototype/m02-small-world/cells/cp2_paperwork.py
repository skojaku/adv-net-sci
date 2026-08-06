# Premade cells for checkpoint cp2_paperwork — the photo drop area.
# Three cells: the drop box, a LIVE preview of whatever is in it, and a send
# button. The preview is reactive, so a student who worked it out wrong just
# drops a new photo into the same box — it replaces the old one, and they
# press send again. Pressing send appends a line to
# session_artifacts/student_signal.txt, which the extension watches: the
# tutor learns the photo is up without the student typing in the terminal.
# describe: A drop area for a phone photo of the student's hand-worked distance table, a live preview of it, and a "Send to my tutor" button; dropping a new photo replaces the preview, so they can redo the table as many times as they like.
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
        "beats a tidy answer.</span>"
    ),
])
# --- cell: cp2_paperwork_photo_preview ---
from pathlib import Path as _P

_files = list(cp2_paperwork_photo.value or [])
# A photo already saved means this session is over and someone is reading
# the notebook. The drop box cannot remember the file across a restart, but
# the saved copy is two cells below — so "your photo appears here once you
# drop it in" was simply false to every later reader.
_done = not _files and _P("assets/uploads/cp2_paperwork_photo_view.jpg").exists()
cp2_paperwork_photo_send = mo.ui.run_button(label="📨 Send to my tutor", disabled=not _files)
if _done:
    _out = mo.md("")
elif not _files:
    _out = mo.vstack([
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
            "here once you drop it in above.*</span>"
        ),
        cp2_paperwork_photo_send,
    ])
else:
    _out = mo.vstack([
        mo.image(_files[0].contents, width=420),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
            "your tutor will see. Missed a pair, or want to redo the table? Drop "
            "another photo into the box above — it replaces this one, as many "
            "times as you like. When it looks right, press send.</span>"
        ),
        cp2_paperwork_photo_send,
    ])
_out
# --- cell: cp2_paperwork_photo_sent ---
from pathlib import Path as _P

# Recomputed, not borrowed: a name starting with "_" is private to its cell
# in marimo, so the preview cell's copy is not visible here.
_done = not (cp2_paperwork_photo.value or []) and _P("assets/uploads/cp2_paperwork_photo_view.jpg").exists()
if cp2_paperwork_photo_send.value and (cp2_paperwork_photo.value or []):

    _P("session_artifacts").mkdir(exist_ok=True)
    with open("session_artifacts/student_signal.txt", "a") as _f:
        _f.write("cp2_paperwork_photo\n")
    _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
else:
    _sent = (
        mo.md("")
        if _done
        else mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
            "when the photo looks right — that is what tells your tutor to look.*</span>"
        )
    )
_sent
