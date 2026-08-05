# Premade cells for checkpoint cp5_ring_formula — the photo drop area.
# Three cells: the drop box, a LIVE preview of whatever is in it, and a send
# button. The preview is reactive, so a student who worked it out wrong just
# drops a new photo into the same box — it replaces the old one, and they
# press send again. Pressing send appends a line to
# session_artifacts/student_signal.txt, which the extension watches: the
# tutor learns the photo is up without the student typing in the terminal.
# describe: A drop area for a phone photo of the student's hand-worked triangle count and formula derivation, a live preview of it, and a "Send to my tutor" button; dropping a new photo replaces the preview, so they can redo the derivation as many times as they like.
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
        "Crossings-out are fine and welcome.</span>"
    ),
])
# --- cell: cp5_ring_paperwork_photo_preview ---
_files = list(cp5_ring_paperwork_photo.value or [])
cp5_ring_paperwork_photo_send = mo.ui.run_button(label="📨 Send to my tutor", disabled=not _files)
if not _files:
    _out = mo.vstack([
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
            "here once you drop it in above.*</span>"
        ),
        cp5_ring_paperwork_photo_send,
    ])
else:
    _out = mo.vstack([
        mo.image(_files[0].contents, width=420),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
            "your tutor will see. Want to fix a step and try again? Drop another "
            "photo into the box above — it replaces this one, as many times as "
            "you like. When it looks right, press send.</span>"
        ),
        cp5_ring_paperwork_photo_send,
    ])
_out
# --- cell: cp5_ring_paperwork_photo_sent ---
if cp5_ring_paperwork_photo_send.value and (cp5_ring_paperwork_photo.value or []):
    from pathlib import Path as _P

    _P("session_artifacts").mkdir(exist_ok=True)
    with open("session_artifacts/student_signal.txt", "a") as _f:
        _f.write("cp5_ring_paperwork_photo\n")
    _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
else:
    _sent = mo.md("")
_sent
