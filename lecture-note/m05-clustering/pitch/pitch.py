# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# The Module 5 pitch: one result on Zachary's karate club, to be sold in three
# minutes.
#
# Four groups in the room each get a different definition of "community" and
# the result it gives on the same 34 people. The notebook shows that result,
# the numbers behind it, and one knob to turn. Nothing here is a question to be
# answered in the notebook; the pitch is spoken. Handout: pitch-sheet.tex.
#
# Rules this file obeys (see lecture-note/LAB_NOTEBOOK_GUIDE.md):
#
#   * One file, nothing fetched at run time. The data is 34 faction labels and
#     34 positions, pasted below; the 78 edges come with igraph.
#   * The stylesheet travels inside the file, because molab ignores css_file
#     (marimo-team/marimo#8467). Refresh it with
#     `python tools/build_lab_notebooks.py m05-pitch` after editing
#     lecture-hall.css.
#   * No number about a result is written in a sentence. Every figure the
#     student reads is computed by the cell that shows it.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import base64
    import html
    import random

    import igraph
    import marimo as mo
    import numpy as np

    LECTURE_HALL_CSS_B64 = "LyogTGVjdHVyZSBIYWxsIOKAlCBtYXJpbW8gY3VzdG9tIENTUywgZHJhd24gYnkgaGFuZAogICBVc2FnZTogcHV0IHRoaXMgbmV4dCB0byB5b3VyIG5vdGVib29rIGFuZCBhZGQgdG8gdGhlIG5vdGVib29rJ3MgY29uZmlnOgogICAgIFtkaXNwbGF5XSBjc3NfZmlsZSA9ICJsZWN0dXJlLWhhbGwuY3NzIgogICBvciBpbiBtYXJpbW8udG9tbCB1bmRlciBbZGlzcGxheV0uCgogICBUaGUgbm90ZWJvb2sgaXMgYSBsZWN0dXJlIG5vdGUgdGhlIHN0dWRlbnQgYW5kIHRoZSB0dXRvciBmaWxsIGluIHRvZ2V0aGVyLAogICBzbyBpdCBpcyBkcmVzc2VkIGFzIG9uZTogZG90LWdyaWQgcGFwZXIsIHdvYmJseSBpbmsgYm9yZGVycywgYW5kIHNlY3Rpb24KICAgcnVsZXMgZHJhd24gd2l0aCBhIHBlbi4KCiAgIFRIRSBIQU5EIElTIElOIFRIRSBMSU5FUywgTk9UIElOIFRIRSBMRVRURVJTLiBBIGhhbmR3cml0aW5nIGZhY2UgZm9yIHRoZQogICBwcm9zZSB3YXMgdGlyaW5nIHRvIHJlYWQgb3ZlciBuaW5ldHkgbWludXRlcyBhbmQgbWFkZSB0aGUgcGFnZSBsb29rIGxpa2UgYQogICBncmVldGluZyBjYXJkIHJhdGhlciB0aGFuIGEgbGVjdHVyZSBub3RlLiBTbyB0aGUgdHlwZSBpcyBleGFjdGx5IHRoZSBjb3Vyc2UKICAgbGVjdHVyZSBub3RlJ3MgKGFkdi1uZXQtc2NpL2xlY3R1cmUtbm90ZS9zY3NzL21pbmltYWwuc2Nzcyk6IGEgc3lzdGVtIHNhbnMKICAgZm9yIHRoZSBib2R5LCBhIHN5c3RlbSBzZXJpZiBmb3IgdGhlIGhlYWRpbmdzLCAxOHB4LzEuNjUg4oCUIHRoZSBzYW1lCiAgIHJlYWRpbmcgZXhwZXJpZW5jZSBvbiBib3RoIGhhbHZlcyBvZiB0aGUgY291cnNlLiBXaGF0IHN0YXlzIGhhbmQtZHJhd24gaXMKICAgZXZlcnl0aGluZyB0aGF0IGlzIG5vdCByZWFkIGFzIGEgd29yZDogdGhlIHdhdnkgc2VjdGlvbiBydWxlcywgdGhlIHdvYmJseQogICBib3JkZXJzIGFuZCBwZW4gc2hhZG93cywgdGhlIHNrZXRjaGVkIG1hdHBsb3RsaWIgc3Ryb2tlcywgYW5kIG5ldHZpeidzCiAgIHR1cmJ1bGVudCBlZGdlcy4KCiAgIE5vIHdlYmZvbnQsIG5vIG5ldHdvcmsgcmVxdWVzdDogYSBzdHVkZW50IG9uIGEgcGxhbmUgZ2V0cyB0aGUgc2FtZSBwYWdlLAogICBhbmQgdGhlcmUgaXMgbm8gZmlyc3QtcGFpbnQgZmxhc2ggb2YgYSBmYWxsYmFjayBmYWNlLgoKICAgVGhlIGFjY2VudHMgYXJlIHRoZSBMRUNUVVJFIFNMSURFUycgYWNjZW50cywgdmVyYmF0aW0g4oCUIHRoZSBtb2R1bGUgaXMgb25lCiAgIGNvdXJzZSwgc28gdGhlIGNvbG91ciB0aGF0IG1lYW5zICJ0aGUgdGhpbmcgd2UgYXJlIGxvb2tpbmcgYXQiIGhhcyB0byBtZWFuCiAgIGl0IGluIGJvdGggaGFsdmVzLiBDaGFuZ2Ugb25lIG9mIHRoZW0gaGVyZSBhbmQgeW91IG11c3QgY2hhbmdlIGl0IGluCiAgIGFkdi1uZXQtc2NpL3NsaWRlcy9tMDIvZmlndXJlcy9tYWtlX2ZpZ3VyZXMucHkgdG9vLCBhbmQgaW4gZXZlcnkgY2VsbHMvKi5weQogICB0aGF0IGhhcmRjb2RlcyBpdCAodGhleSBhbGwgZG8sIGZvciB0aGVpciBub2RlcyBhbmQgZWRnZXMpLiAqLwoKOnJvb3QgewogIC8qIHBhbGV0dGUg4oCUIHRoZSB0aHJlZSBhY2NlbnRzIGNvbWUgZnJvbSB0aGUgc2xpZGUgZGVjawogICAgIChtYWtlX2ZpZ3VyZXMucHk6IEFDQ0VOVCAvIEFDQ0VOVDIgLyBBQ0NFTlQzKSwgYW5kIHRoZSBwcmVtYWRlIGNlbGxzCiAgICAgaGFyZGNvZGUgdGhlIHNhbWUgaGV4ZXMgZm9yIHRoZWlyIG5vZGVzIGFuZCBlZGdlcywgc28gYSByZXBhaW50IGhlcmUKICAgICBkZXN5bmNzIGJvdGguIFdoYXQgaXMgTk9UIHRoZSBzbGlkZXMnIGlzIHRoZSBwYXBlcjogd2hpdGUgYmVjYW1lIHdhcm0sCiAgICAgYW5kIHRoZSBwZW5jaWwgcnVsZSAoLS1saC1ydWxlKSBpcyBhIG5ldyB0b2tlbiByYXRoZXIgdGhhbiBhIHJlcGFpbnQgb2YKICAgICAtLWxoLWxpbmUsIHdoaWNoIGlzIGEgbm9kZSBmaWxsIGluIGNwMiBhbmQgY3A1LiAqLwogIC0tbGgtcGFwZXI6ICAgI0ZGRkRGNzsKICAtLWxoLWNhcmQ6ICAgICNGRkZGRkY7CiAgLS1saC1zdXJmYWNlOiAjRjZGMkU5OwogIC0tbGgtbGluZTogICAgI0U0RTZFQTsKICAtLWxoLXJ1bGU6ICAgICNEOUQyQzI7CiAgLS1saC1pbms6ICAgICAjMUQxRTIxOwogIC0tbGgtaW5rLTI6ICAgIzM1MzczQzsKICAtLWxoLW11dGVkOiAgICM2QTZENzU7CiAgLS1saC1ibHVlOiAgICAjMjIzMzZCOwogIC0tbGgtYmx1ZS0yOiAgIzM5NTlBNjsKICAtLWxoLXJ1c3Q6ICAgICNCMTQ0MzQ7CgogIC8qIHR5cGUg4oCUIHRoZSBsZWN0dXJlIG5vdGUncyB0aHJlZSBzdGFja3MsIHZlcmJhdGltLiBBbGwgZnJvbSB0aGUgc3lzdGVtOgogICAgIG5vdGhpbmcgaGVyZSBpcyBmZXRjaGVkLiAqLwogIC0tbGgtc2VyaWY6ICAgIklvd2FuIE9sZCBTdHlsZSIsICJQYWxhdGlubyBMaW5vdHlwZSIsIFBhbGF0aW5vLAogICAgICAgICAgICAgICAgIkJvb2sgQW50aXF1YSIsICJIb2VmbGVyIFRleHQiLCBHZW9yZ2lhLAogICAgICAgICAgICAgICAgIlRpbWVzIE5ldyBSb21hbiIsIHNlcmlmOwogIC0tbGgtc2FuczogICAgc3lzdGVtLXVpLCAtYXBwbGUtc3lzdGVtLCAiU2Vnb2UgVUkiLCBSb2JvdG8sCiAgICAgICAgICAgICAgICAiSGVsdmV0aWNhIE5ldWUiLCAiTm90byBTYW5zIiwgIkxpYmVyYXRpb24gU2FucyIsIEFyaWFsLAogICAgICAgICAgICAgICAgc2Fucy1zZXJpZjsKICAtLWxoLW1vbm86ICAgIHVpLW1vbm9zcGFjZSwgU0ZNb25vLVJlZ3VsYXIsICJTRiBNb25vIiwgTWVubG8sIENvbnNvbGFzLAogICAgICAgICAgICAgICAgIkxpYmVyYXRpb24gTW9ubyIsIG1vbm9zcGFjZTsKICAvKiBUaGUgb25lIGhhbmQtd3JpdHRlbiBmYWNlIG9uIHRoZSBwYWdlLCBhbmQgaXQgd3JpdGVzIGV4YWN0bHkgb25lIHRoaW5nOgogICAgIHRoZSBzdHVkZW50J3Mgb3duIGFuc3dlcnMsIGluc2lkZSB0aGUgZm9sZC4gUHJpbnRlZCBub3RlLCBoYW5kd3JpdHRlbgogICAgIG1hcmdpbiDigJQgdGhlIGRpZmZlcmVuY2UgYmV0d2VlbiB0aGUgdHdvIGlzIHRoZSBwb2ludC4gU3lzdGVtIGZhY2VzIG9ubHksCiAgICAgbGlrZSBldmVyeXRoaW5nIGVsc2UgaGVyZTogbWFjT1Mgc2hpcHMgdGhlIGZpcnN0IHR3bywgV2luZG93cyB0aGUgbmV4dAogICAgIHR3bywgYGN1cnNpdmVgIGNhdGNoZXMgdGhlIHJlc3QuICovCiAgLS1saC1oYW5kOiAgICAiQ2hhbGtib2FyZCBTRSIsICJCcmFkbGV5IEhhbmQiLCAiU2Vnb2UgUHJpbnQiLAogICAgICAgICAgICAgICAgIkNvbWljIFNhbnMgTVMiLCBjdXJzaXZlOwoKICAvKiB0aGUgaGFuZC1kcmF3biBraXQ6IHR3byByb3VuZGluZyBzZXRzLCBhbHRlcm5hdGVkIHNvIG5vIHR3byBib3hlcyBvbiB0aGUKICAgICBwYWdlIGhhdmUgdGhlIHNhbWUgY29ybmVycywgYW5kIG9uZSBpbmsgc2hhZG93IHRoYXQgZmFrZXMgYSBzZWNvbmQgcGFzcwogICAgIG9mIHRoZSBwZW4uICovCiAgLS1saC13b2JibGU6ICAgMTRweCA2cHggMTZweCA4cHggLyA4cHggMTZweCA2cHggMTRweDsKICAtLWxoLXdvYmJsZS0yOiA2cHggMTZweCA4cHggMTRweCAvIDE2cHggNnB4IDE0cHggOHB4OwogIC0tbGgtcGVuOiAgICAgIDNweCA0cHggMCAtMXB4IHJnYmEoMzUsIDM0LCA0MywgMC4xNik7CiAgLS1saC1wZW4tc29mdDogMnB4IDNweCAwIC0xcHggcmdiYSgzNSwgMzQsIDQzLCAwLjEyKTsKCiAgLyogYSB3YXZ5IHN0cm9rZSwgdXNlZCBmb3IgdW5kZXJsaW5lcyBhbmQgdGFibGUgcnVsZXMgKi8KICAtLWxoLXN0cm9rZTogdXJsKCJkYXRhOmltYWdlL3N2Zyt4bWwsJTNDc3ZnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Zycgd2lkdGg9JzEyMCcgaGVpZ2h0PSc3JyB2aWV3Qm94PScwIDAgMTIwIDcnJTNFJTNDcGF0aCBkPSdNMSA0LjRDMjAgMS45IDQwIDYuMiA2MCAzLjcgODAgMS40IDEwMCA1LjYgMTE5IDMuMicgZmlsbD0nbm9uZScgc3Ryb2tlPSclMjNCMTQ0MzQnIHN0cm9rZS13aWR0aD0nMicgc3Ryb2tlLWxpbmVjYXA9J3JvdW5kJy8lM0UlM0Mvc3ZnJTNFIik7CiAgLS1saC1zdHJva2UtZmFpbnQ6IHVybCgiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMjAnIGhlaWdodD0nNycgdmlld0JveD0nMCAwIDEyMCA3JyUzRSUzQ3BhdGggZD0nTTEgNC40QzIwIDEuOSA0MCA2LjIgNjAgMy43IDgwIDEuNCAxMDAgNS42IDExOSAzLjInIGZpbGw9J25vbmUnIHN0cm9rZT0nJTIzRDlEMkMyJyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcvJTNFJTNDL3N2ZyUzRSIpOwoKICAvKiBtYXJpbW8gdG9rZW5zICovCiAgLS1iYWNrZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1pbmspOwogIC0tY2FyZDogdmFyKC0tbGgtY2FyZCk7CiAgLS1jYXJkLWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1wb3BvdmVyOiB2YXIoLS1saC1jYXJkKTsKICAtLXBvcG92ZXItZm9yZWdyb3VuZDogdmFyKC0tbGgtaW5rKTsKICAtLW11dGVkOiB2YXIoLS1saC1zdXJmYWNlKTsKICAtLW11dGVkLWZvcmVncm91bmQ6IHZhcigtLWxoLW11dGVkKTsKICAtLWJvcmRlcjogdmFyKC0tbGgtbGluZSk7CiAgLS1pbnB1dDogdmFyKC0tbGgtbGluZSk7CiAgLS1yaW5nOiB2YXIoLS1saC1ibHVlKTsKICAtLXByaW1hcnk6IHZhcigtLWxoLWJsdWUpOwogIC0tcHJpbWFyeS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1zZWNvbmRhcnk6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tc2Vjb25kYXJ5LWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1hY2NlbnQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tYWNjZW50LWZvcmVncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIC0tZGVzdHJ1Y3RpdmU6IHZhcigtLWxoLXJ1c3QpOwogIC0tZGVzdHJ1Y3RpdmUtZm9yZWdyb3VuZDogdmFyKC0tbGgtcGFwZXIpOwogIC0tcmFkaXVzOiAzcHg7CgogIC0tdGV4dC1mb250OiB2YXIoLS1saC1zYW5zKTsKICAtLWhlYWRpbmctZm9udDogdmFyKC0tbGgtc2VyaWYpOwogIC0tY29kZS1mb250OiB2YXIoLS1saC1tb25vKTsKfQoKLyogLS0tLS0tLS0tLSBwYWdlIC0tLS0tLS0tLS0gKi8KCi8qIERvdC1ncmlkLCBub3QgcnVsZWQgbGluZXM6IHRoZSBzYW1lICJ0aGlzIGlzIGEgc2tldGNoYm9vayIgc2lnbmFsLCBidXQgaXQKICAgZG9lcyBub3QgZmlnaHQgYSBsaW5lIG9mIHByb3NlIGZvciB0aGUgc2FtZSBob3Jpem9udGFsIGJhbmQuICovCmJvZHksCiNBcHAgewogIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWxoLXBhcGVyKTsKICBiYWNrZ3JvdW5kLWltYWdlOiByYWRpYWwtZ3JhZGllbnQocmdiYSgzMSwgNTgsIDk1LCAwLjA4NSkgMXB4LCB0cmFuc3BhcmVudCAxcHgpOwogIGJhY2tncm91bmQtc2l6ZTogMjRweCAyNHB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIC13ZWJraXQtZm9udC1zbW9vdGhpbmc6IGFudGlhbGlhc2VkOwp9CgovKiAtLS0tLS0tLS0tIHByb3NlIC0tLS0tLS0tLS0gKi8KCi5tYXJrZG93biwKLnByb3NlIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgZm9udC1zaXplOiAxOHB4OwogIGxpbmUtaGVpZ2h0OiAxLjY1OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgdGV4dC13cmFwOiBwcmV0dHk7CiAgbWF4LXdpZHRoOiA2OGNoOwp9CgovKiBUaGUgbGVjdHVyZSBub3RlJ3Mgc2VyaWYgYW5kIGl0cyBzY2FsZSDigJQgaDEgMi4wNSAvIGgyIDEuNTUgLyBoMyAxLjIyIC8KICAgaDQgMS4wMiBhZ2FpbnN0IGl0cyAxOHB4IHJvb3QuIFdyaXR0ZW4gb3V0IGluIHB4IGJlY2F1c2UgbWFyaW1vJ3Mgcm9vdAogICBzdGF5cyB0aGUgYnJvd3NlcidzIDE2cHgsIHNvIGEgcmVtIGhlcmUgd291bGQgYmUgYSBkaWZmZXJlbnQgc2l6ZSB0aGFuCiAgIHRoZSBzYW1lIHJlbSBvbiB0aGUgbm90ZS4gKi8KLm1hcmtkb3duIGgxLCAubWFya2Rvd24gaDIsIC5tYXJrZG93biBoMywgLm1hcmtkb3duIGg0LAoucHJvc2UgaDEsIC5wcm9zZSBoMiwgLnByb3NlIGgzLCAucHJvc2UgaDQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zZXJpZik7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtaW5rKTsKICBsaW5lLWhlaWdodDogMS4yNTsKICBsZXR0ZXItc3BhY2luZzogMDsKfQoKLm1hcmtkb3duIGgxLCAucHJvc2UgaDEgewogIGZvbnQtc2l6ZTogMzdweDsKICBtYXJnaW46IDAgMCAyMnB4OwogIGxldHRlci1zcGFjaW5nOiAtMC4wMWVtOwp9CgovKiBBIGNoYXB0ZXIgYnJlYWsg4oCUIG9uZSBvZiB0aGUgdHdvIHBsYWNlcyB0aGUgcGVuIHN0aWxsIHdyaXRlcy4gKi8KLm1hcmtkb3duIGgyLCAucHJvc2UgaDIgewogIGZvbnQtc2l6ZTogMjhweDsKICBtYXJnaW46IDUwcHggMCAxNnB4OwogIHBhZGRpbmctYm90dG9tOiAwLjE4ZW07CiAgYmFja2dyb3VuZC1pbWFnZTogdmFyKC0tbGgtc3Ryb2tlKTsKICBiYWNrZ3JvdW5kLXJlcGVhdDogcmVwZWF0LXg7CiAgYmFja2dyb3VuZC1wb3NpdGlvbjogbGVmdCBib3R0b207CiAgYmFja2dyb3VuZC1zaXplOiAxMjBweCA3cHg7Cn0KCi8qIEEgbm90ZSBjZWxsJ3Mgb3duIHRpdGxlIChgIyMjIPCfk48gRGlzdGFuY2UgYW5kIGF2ZXJhZ2UgcGF0aCBsZW5ndGhgKS4gSXQgaXMKICAgc2V0IGxhcmdlciB0aGFuIHRoZSBwcm9zZSBiZW5lYXRoIGl0IHNvIHRoZSBmaW5pc2hlZCBub3RlYm9vayByZWFkcyBhcyBhCiAgIHJ1biBvZiBzZWN0aW9ucywgbm90IG9uZSBsb25nIGNvbHVtbi4gKi8KLm1hcmtkb3duIGgzLCAucHJvc2UgaDMgeyBmb250LXNpemU6IDIycHg7IG1hcmdpbjogMzZweCAwIDEzcHg7IH0KCi8qIFF1aWV0ZXIgdGhhbiBoMzogc2l6ZSBhbmQgd2VpZ2h0IG9ubHksIG5ldmVyIGEgcnVsZS4gKi8KLm1hcmtkb3duIGg0LCAucHJvc2UgaDQgeyBmb250LXNpemU6IDE4cHg7IG1hcmdpbjogMjdweCAwIDlweDsgfQoKLm1hcmtkb3duIGEsIC5wcm9zZSBhIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyB0ZXh0LWRlY29yYXRpb24tY29sb3I6IHZhcigtLWxoLWxpbmUpOyB9Ci5tYXJrZG93biBhOmhvdmVyLCAucHJvc2UgYTpob3ZlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBjdXJyZW50Q29sb3I7IH0KCi5tYXJrZG93biBzdHJvbmcsIC5wcm9zZSBzdHJvbmcgeyBjb2xvcjogdmFyKC0tbGgtaW5rKTsgZm9udC13ZWlnaHQ6IDcwMDsgfQoKLyogQSBxdW90ZSBjYXJyaWVzIE5PIGNocm9tZSBhdCBhbGw6IG5vIGZpbGwsIG5vIGJvcmRlciwgbm90IGV2ZW4gYSBydWxlIGluCiAgIHRoZSBtYXJnaW4g4oCUIGdyZXkgaW5rIGlzIHRoZSB3aG9sZSB0cmVhdG1lbnQuCgogICBJdCBoYXMgYmVlbiB3YWxrZWQgZG93biBvbmUgc3RlcCBhdCBhIHRpbWUgYW5kIGVhY2ggc3RlcCB3YXMgcmlnaHQuIEl0CiAgIHN0YXJ0ZWQgYXMgYSBzY3JhcCBvZiBwYXBlciBwaW5uZWQgdG8gdGhlIHBhZ2UgKGZpbGxlZCwgbmF2eS1ib3JkZXJlZCwKICAgc2hhZG93ZWQsIHRpbHRlZCBhIHF1YXJ0ZXIgZGVncmVlKSwgd2hpY2ggc2FpZCBMT09LIEFUIFRISVMgYWJvdXQgYSBsaW5lCiAgIHRoZSByZWFkZXIgaGFkIGFscmVhZHkgY2xpY2tlZCB0byBvcGVuLiBUaGVuIGEgbWFyZ2luIHJ1bGUsIHdoaWNoIHN0aWxsCiAgIGRyZXcgYSB2ZXJ0aWNhbCBsaW5lIGRvd24gYSBwYWdlIHRoYXQgaGFzIHBsZW50eS4gV2hhdCBpcyBsZWZ0IGlzIHdoYXQKICAgdGhlIHF1b3RlIGFjdHVhbGx5IGlzOiB0aGUgc3R1ZGVudCdzIG93biB3b3JkcywgaW4gdGhlIHBhZ2UncyBxdWlldCBncmV5LAogICB1bmRlciBhIGhlYWRpbmcgdGhhdCBhbHJlYWR5IG5hbWVzIHRoZW0uICM2QTZENzUgb24gd2hpdGUgaXMgNS4yOjEg4oCUCiAgIHF1aWV0IGlzIG5vdCB0aGUgc2FtZSBhcyB1bnJlYWRhYmxlLCBhbmQgdGhpcyBsaW5lIGlzIHRoZSBncmFkZWQgb25lLiAqLwoubWFya2Rvd24gYmxvY2txdW90ZSwKLnByb3NlIGJsb2NrcXVvdGUgewogIG1hcmdpbjogMS40ZW0gMDsKICBwYWRkaW5nOiAwOwogIGJhY2tncm91bmQ6IG5vbmU7CiAgYm9yZGVyOiAwOwogIGJvcmRlci1yYWRpdXM6IDA7CiAgYm94LXNoYWRvdzogbm9uZTsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGZvbnQtc3R5bGU6IG5vcm1hbDsKfQoKLyogLS0tLS0tLS0tLSB0aGUgc3R1ZGVudCdzIG93biBhbnN3ZXIsIGZvbGRlZCAtLS0tLS0tLS0tICovCgovKiBFdmVyeSBub3RlIGNlbGwgZW5kcyB3aXRoIHdoYXQgdGhlIHN0dWRlbnQgc2FpZCwgcXVvdGVkIHZlcmJhdGltLiBMZWZ0CiAgIG9wZW4gaXQgd2FzIHRoZSBsb3VkZXN0IHRoaW5nIG9uIHRoZSBwYWdlIOKAlCBhIGJvcmRlcmVkLCBzaGFkb3dlZCBzbGFiCiAgIHVuZGVyIGV2ZXJ5IHNpbmdsZSBub3RlLCBjb21wZXRpbmcgd2l0aCB0aGUgZmlndXJlIGFib3ZlIGl0IGFuZCB3aXRoIHRoZQogICBleHBsYW5hdGlvbiB0aGUgbm90ZSBleGlzdHMgdG8gZ2l2ZS4gU28gaXQgaXMgZm9sZGVkOiB0aGUgbm90ZSByZWFkcyBhcwogICB0aGUgbGVjdHVyZSBub3RlIGl0IGlzLCBhbmQgdGhlIGFuc3dlciBpcyBvbmUgY2xpY2sgYXdheS4KICAgYG1vLm1kYCByZW5kZXJzIGAvLy8gZGV0YWlscyB8IE15IGFuc3dlcmAgKyBgdHlwZTogbGgtYW5zd2VyYCBpbnRvIHRoaXMuCgogICBDbG9zZWQsIGl0IGlzIGEgZGFzaGVkIHRhYiBpbiB0aGUgbWFyZ2luIGNvbG91ciDigJQgcHJlc2VudCwgcXVpZXQsIGNsZWFybHkKICAgcHJlc3NhYmxlLiBPcGVuLCBpdCBpcyB0aGVpciB3b3JkcyBiZWhpbmQgYSBtYXJnaW4gcnVsZSwgYW5kIG5vdGhpbmcgZWxzZToKICAgYSByZWFkZXIgd2hvIGNsaWNrZWQgdG8gc2VlIHRoZSBhbnN3ZXIgZG9lcyBub3QgYWxzbyBuZWVkIGl0IGJveGVkLiAqLwovKiBtYXJpbW8gZHJlc3NlcyBFVkVSWSBgLm1hcmtkb3duIGRldGFpbHNgIGFzIGFuIGFkbW9uaXRpb24sIGFuZCB0aGVyZSBpcyBubwogICBvcHRpbmcgb3V0IGJ5IG5hbWluZyBhbiB1bmtub3duIHR5cGU6IGEgY2FyZC1jb2xvdXJlZCBiYWNrZ3JvdW5kLCBhIDZweAogICBsZWZ0IHJ1bGUsIGEgY2hldnJvbiBidWlsdCBvdXQgb2YgdHdvIHJvdGF0ZWQgYm9yZGVycyBvbiBgc3VtbWFyeTo6YmVmb3JlYCwKICAgYW5kIGEgMXJlbSBwYWQgb24gZXZlcnkgY2hpbGQgdGhhdCBpcyBub3QgdGhlIHN1bW1hcnkuIE9uIHBhcGVyLWNvbG91cmVkCiAgIHBhZ2VzIHRoYXQgY2FyZCByZWFkcyBhcyBhIGdyZXkgc2xhYiBwYXJrZWQgYmVoaW5kIHRoZSBhbnN3ZXIuIEFsbCBmb3VyIGFyZQogICB1bmRvbmUgaGVyZSDigJQgdGhpcyBmb2xkIGlzIGRyYXduIGZyb20gc2NyYXRjaCwgbm90IHRoZW1lZC4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgewogIG1hcmdpbjogMS4yZW0gMDsKICBiYWNrZ3JvdW5kOiBub25lOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwp9Ci8qIFRoZSAxcmVtIHBhZCBtYXJpbW8gcHV0cyBvbiB0aGUgcXVvdGUuIFRoZSBxdW90ZSBoYXMgaXRzIG93bi4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gKjpub3Qoc3VtbWFyeSksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+ICo6bm90KHN1bW1hcnkpIHsgcGFkZGluZzogMDsgfQoKLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSB7CiAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgYWxpZ24taXRlbXM6IGJhc2VsaW5lOwogIGdhcDogMC40NWVtOwogIHdpZHRoOiBmaXQtY29udGVudDsKICBjdXJzb3I6IHBvaW50ZXI7CiAgcGFkZGluZzogMnB4IDEycHggNHB4OwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXNpemU6IDE0cHg7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGJhY2tncm91bmQ6IHRyYW5zcGFyZW50OwogIGJvcmRlcjogMS41cHggZGFzaGVkIHZhcigtLWxoLXJ1bGUpOwogIGJvcmRlci1yYWRpdXM6IHZhcigtLWxoLXdvYmJsZS0yKTsKICAvKiBCb3RoIHNwZWxsaW5nczogU2FmYXJpIHN0aWxsIHNoaXBzIHRoZSBwc2V1ZG8tZWxlbWVudCwgZXZlcnlvbmUgZWxzZQogICAgIGhvbm91cnMgbGlzdC1zdHlsZS4gTGVmdCBpbiwgdGhlIGRlZmF1bHQgdHJpYW5nbGUgc2l0cyBvdXRzaWRlIHRoZSB0YWIuICovCiAgbGlzdC1zdHlsZTogbm9uZTsKICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lOwogIHVzZXItc2VsZWN0OiBub25lOwogIHRyYW5zaXRpb246IGNvbG9yIDAuMTJzIGVhc2UsIGJvcmRlci1jb2xvciAwLjEycyBlYXNlOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIgeyBkaXNwbGF5OiBub25lOyB9CgovKiBPdXJzLiBtYXJpbW8ncyBjaGV2cm9uIGlzIHR3byByb3RhdGVkIGJvcmRlcnMgd2l0aCBwYWRkaW5nIGFuZCBhIG1hcmdpbiwKICAgc28gZXZlcnkgb25lIG9mIHRob3NlIHByb3BlcnRpZXMgaGFzIHRvIGJlIG5hbWVkIHRvIGJlIHN3aXRjaGVkIG9mZiDigJQKICAgbGVmdCBpbiwgaXRzIDQ1ZGVnIGJveCBsYW5kcyBvbiB0b3Agb2YgdGhpcyBhcnJvdy4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeTo6YmVmb3JlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OjpiZWZvcmUgewogIGNvbnRlbnQ6ICLilrgiOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwogIG1hcmdpbjogMDsKICB0cmFuc2Zvcm06IG5vbmU7CiAgdHJhbnNpdGlvbjogbm9uZTsKICB2ZXJ0aWNhbC1hbGlnbjogYmFzZWxpbmU7CiAgZm9udC1zaXplOiAxMXB4OwogIGxpbmUtaGVpZ2h0OiAxOwogIGNvbG9yOiB2YXIoLS1saC1ibHVlLTIpOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnk6OmJlZm9yZSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyW29wZW5dID4gc3VtbWFyeTo6YmVmb3JlIHsKICBjb250ZW50OiAi4pa+IjsKICB0cmFuc2Zvcm06IG5vbmU7Cn0KCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIgewogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtYmx1ZS0yKTsKfQoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OmZvY3VzLXZpc2libGUsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Zm9jdXMtdmlzaWJsZSB7CiAgb3V0bGluZTogMnB4IHNvbGlkIHZhcigtLWxoLWJsdWUpOwogIG91dGxpbmUtb2Zmc2V0OiAycHg7Cn0KCi8qIE9wZW46IHRoZSB0YWIgaGFuZHMgb3ZlciB0byB0aGUgcXVvdGUsIHNvIGl0IHN0b3BzIGRyYXdpbmcgYSBib3JkZXIuICovCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnkgewogIGJvcmRlci1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgcGFkZGluZy1sZWZ0OiAwOwogIHBhZGRpbmctcmlnaHQ6IDA7Cn0KCi8qIEluc2lkZSB0aGUgZm9sZCwgYW5kIE9OTFkgaW5zaWRlIGl0LCB0aGUgcXVvdGUgaXMgaGFuZHdyaXRpbmcuIFRoYXQgaXMKICAgd2hhdCB0ZWxscyBhIHJlYWRlciBhdCBhIGdsYW5jZSB3aGljaCB3b3JkcyBhcmUgdGhlIG5vdGUncyBhbmQgd2hpY2ggYXJlCiAgIHRoZWlycyDigJQgdGhlIGdyZXkgYWxvbmUgbGVmdCB0aGUgdHdvIGxvb2tpbmcgbGlrZSBvbmUgdm9pY2UuCiAgIFNjb3BlZCB0byB0aGUgZm9sZCBvbiBwdXJwb3NlOiBjcDcgcXVvdGVzIGFuIEFJJ3MgYW5hbHlzaXMgaW4gYQogICBibG9ja3F1b3RlIHRvbywgYW5kIHRoYXQgb25lIGlzIGVtcGhhdGljYWxseSBub3Qgd3JpdHRlbiBieSBoYW5kLiAqLwoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlIHsKICBtYXJnaW4tdG9wOiAwLjNlbTsKICBmb250LWZhbWlseTogdmFyKC0tbGgtaGFuZCk7CiAgLyogVGhlc2UgZmFjZXMgcnVuIHNtYWxsIGZvciB0aGVpciBwb2ludCBzaXplIOKAlCBTZWdvZSBQcmludCBlc3BlY2lhbGx5LiAqLwogIGZvbnQtc2l6ZTogMS4wNmVtOwogIGxpbmUtaGVpZ2h0OiAxLjU7Cn0KCi5tYXJrZG93biBociwgLnByb3NlIGhyIHsKICBib3JkZXI6IDA7CiAgaGVpZ2h0OiA3cHg7CiAgbWFyZ2luOiAyZW0gMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UtZmFpbnQpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGNlbnRlcjsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoKLm1hcmtkb3duIGNvZGU6bm90KHByZSBjb2RlKSwKLnByb3NlIGNvZGU6bm90KHByZSBjb2RlKSB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMC44NmVtOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHBhZGRpbmc6IDAuMWVtIDAuNGVtOwogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB0YWJsZXMgLS0tLS0tLS0tLSAqLwoKLm1hcmtkb3duIHRhYmxlLCAucHJvc2UgdGFibGUgeyBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOyBmb250LXNpemU6IDE2cHg7IH0KLm1hcmtkb3duIHRoLCAucHJvc2UgdGggewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXdlaWdodDogNzAwOwogIGZvbnQtc2l6ZTogMTRweDsKICBsZXR0ZXItc3BhY2luZzogMC4wMmVtOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHRleHQtYWxpZ246IGxlZnQ7CiAgYm9yZGVyLWJvdHRvbTogMDsKICBwYWRkaW5nOiA2cHggMTRweCA4cHggMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGJvdHRvbTsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoubWFya2Rvd24gdGQsIC5wcm9zZSB0ZCB7CiAgcGFkZGluZzogOHB4IDE0cHggOHB4IDA7CiAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkIHZhcigtLWxoLXJ1bGUpOwogIC8qIE51bWJlcnMgc3RheSBtZWNoYW5pY2FsOiBhIGNvbHVtbiB0aGF0IGRvZXMgbm90IGxpbmUgdXAgaXMgYSBjb2x1bW4gdGhhdAogICAgIGNhbm5vdCBiZSBjb21wYXJlZCwgd2hpY2ggaXMgdGhlIHdob2xlIHJlYXNvbiB0aGUgdGFibGUgaXMgdGhlcmUuICovCiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMTVweDsKICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zOwp9CgovKiAtLS0tLS0tLS0tIGNlbGxzIC0tLS0tLS0tLS0gKi8KCi5jZWxsLApbZGF0YS10ZXN0aWQ9ImNlbGwiXSB7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQouY2VsbDpudGgtb2YtdHlwZShldmVuKSwKW2RhdGEtdGVzdGlkPSJjZWxsIl06bnRoLW9mLXR5cGUoZXZlbikgeyBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7IH0KCi5jZWxsOmZvY3VzLXdpdGhpbiwKW2RhdGEtdGVzdGlkPSJjZWxsIl06Zm9jdXMtd2l0aGluIHsKICBib3gtc2hhZG93OiAwIDAgMCAycHggdmFyKC0tbGgtcnVsZSksIHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLmNlbGwtZWRpdG9yLAouY20tZWRpdG9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxMy41cHg7CiAgbGluZS1oZWlnaHQ6IDEuNTU7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7Cn0KCi5jbS1lZGl0b3IgLmNtLWd1dHRlcnMgewogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7CiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tbGgtcnVsZSk7Cn0KCi5jbS1lZGl0b3IuY20tZm9jdXNlZCB7IG91dGxpbmU6IDJweCBzb2xpZCB2YXIoLS1saC1ibHVlKTsgfQouY20tZWRpdG9yIC5jbS1jdXJzb3IgeyBib3JkZXItbGVmdC1jb2xvcjogdmFyKC0tbGgtcnVzdCk7IH0KLmNtLWVkaXRvciAuY20tc2VsZWN0aW9uQmFja2dyb3VuZCwKLmNtLWVkaXRvci5jbS1mb2N1c2VkIC5jbS1zZWxlY3Rpb25CYWNrZ3JvdW5kIHsgYmFja2dyb3VuZDogI0RDRTNFRCAhaW1wb3J0YW50OyB9Ci5jbS1lZGl0b3IgLmNtLWFjdGl2ZUxpbmUgeyBiYWNrZ3JvdW5kOiByZ2JhKDMxLCA1OCwgOTUsIDAuMDQ1KTsgfQoKLyogc3ludGF4ICovCi5jbS1lZGl0b3IgLnRvay1rZXl3b3JkLAouY20tZWRpdG9yIC5jbS1rZXl3b3JkIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyBmb250LXdlaWdodDogNTAwOyB9Ci5jbS1lZGl0b3IgLnRvay1udW1iZXIsCi5jbS1lZGl0b3IgLmNtLW51bWJlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgfQouY20tZWRpdG9yIC50b2stc3RyaW5nLAouY20tZWRpdG9yIC5jbS1zdHJpbmcgeyBjb2xvcjogIzRCNkEzQTsgfQouY20tZWRpdG9yIC50b2stY29tbWVudCwKLmNtLWVkaXRvciAuY20tY29tbWVudCB7IGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7IGZvbnQtc3R5bGU6IGl0YWxpYzsgfQouY20tZWRpdG9yIC50b2stdmFyaWFibGVOYW1lLAouY20tZWRpdG9yIC50b2stcHJvcGVydHlOYW1lIHsgY29sb3I6IHZhcigtLWxoLWluayk7IH0KLmNtLWVkaXRvciAudG9rLW9wZXJhdG9yIHsgY29sb3I6IHZhcigtLWxoLWluay0yKTsgfQoKLyogLS0tLS0tLS0tLSBvdXRwdXQgLS0tLS0tLS0tLSAqLwoKLm91dHB1dC1hcmVhLAoubWFyaW1vLW91dHB1dCB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7Cn0KCi5vdXRwdXQtYXJlYSBwcmUsCnByZS5vdXRwdXQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1tb25vKTsKICBmb250LXNpemU6IDEzcHg7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7CiAgcGFkZGluZzogMTBweCAxMnB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwp9CgovKiBBIGZpZ3VyZSBpcyBhIGRyYXdpbmcgdGFwZWQgb250byB0aGUgcGFnZS4gKi8KLm91dHB1dC1hcmVhIGltZywKLm1hcmltby1vdXRwdXQgaW1nLAoub3V0cHV0LWFyZWEgc3ZnLAoubWFyaW1vLW91dHB1dCBzdmcgewogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB1aSBjaHJvbWUgLS0tLS0tLS0tLSAqLwoKYnV0dG9uLAoubWFyaW1vLWJ1dHRvbiB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQoKLyogQW55dGhpbmcgdGhlIHN0dWRlbnQgYWN0dWFsbHkgcHJlc3NlcyDigJQg4pa2IFJ1biwg8J+TqCBTZW5kIHRvIG15IHR1dG9yLCB0aGUKICAgcmVmZXJlZSdzIGFwcGVhbCDigJQgaXMgZHJhd24sIGFuZCBtb3ZlcyB1bmRlciB0aGUgcHJlc3MuICovCi5tYXJpbW8tcnVuLWJ1dHRvbiwKLm1hcmltby1idXR0b24sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXSwKYnV0dG9uW2RhdGEtdmFyaWFudD0ic2Vjb25kYXJ5Il0sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4pOwogIHRyYW5zaXRpb246IHRyYW5zZm9ybSAwLjA2cyBlYXNlLCBib3gtc2hhZG93IDAuMDZzIGVhc2U7Cn0KLm1hcmltby1ydW4tYnV0dG9uOmFjdGl2ZSwKLm1hcmltby1idXR0b246YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJwcmltYXJ5Il06YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJzZWNvbmRhcnkiXTphY3RpdmUsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXTphY3RpdmUgewogIHRyYW5zZm9ybTogdHJhbnNsYXRlKDJweCwgMi41cHgpOwogIGJveC1zaGFkb3c6IG5vbmU7Cn0KCi5tYXJpbW8tcnVuLWJ1dHRvbiwKYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdIHsKICBiYWNrZ3JvdW5kOiB2YXIoLS1saC1ibHVlKTsKICBjb2xvcjogdmFyKC0tbGgtcGFwZXIpOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtaW5rKTsKfQoubWFyaW1vLXJ1bi1idXR0b246aG92ZXIsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXTpob3ZlciB7IGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUtMik7IH0KCi8qIFNsaWRlcnM6IGEgcGVuY2lsIGxpbmUgd2l0aCBhIGJlYWQgb24gaXQuIFNlbGVjdG9ycyBjb3ZlciBtYXJpbW8ncyBvd24KICAgd2lkZ2V0IGFuZCBhIHBsYWluIHJhbmdlIGlucHV0LCB3aGljaGV2ZXIgdGhlIGJ1aWxkIHJlbmRlcnMuICovCmlucHV0W3R5cGU9InJhbmdlIl0gewogIGFjY2VudC1jb2xvcjogdmFyKC0tbGgtYmx1ZSk7CiAgaGVpZ2h0OiAyMnB4Owp9Cltyb2xlPSJzbGlkZXIiXSwKW2RhdGEtb3JpZW50YXRpb249Imhvcml6b250YWwiXSBbcm9sZT0ic2xpZGVyIl0gewogIGJvcmRlcjogMnB4IHNvbGlkIHZhcigtLWxoLWluayk7CiAgYm9yZGVyLXJhZGl1czogNTglIDQyJSA1MCUgNTAlIC8gNTAlIDUwJSA0MiUgNTglOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIGJveC1zaGFkb3c6IHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLyogVGV4dCB0aGUgc3R1ZGVudCB0eXBlcyBpbnRvOiBhIHJ1bGVkIGJveCwgbm90IGEgY2hyb21lIGZpZWxkLiAqLwppbnB1dFt0eXBlPSJ0ZXh0Il0sCmlucHV0W3R5cGU9Im51bWJlciJdLAp0ZXh0YXJlYSwKLm1hcmltby10ZXh0LWlucHV0IHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtY2FyZCk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7CiAgYm94LXNoYWRvdzogdmFyKC0tbGgtcGVuLXNvZnQpOwp9CgovKiBUaGUgcGhvdG8gZHJvcCBib3gg4oCUIHRoZSBvbmUgcGxhY2Ugb24gdGhlIHBhZ2UgdGhhdCBhc2tzIGZvciBwYXBlci4gKi8KW2RhdGEtdGVzdGlkPSJmaWxlLXVwbG9hZCJdLAoubWFyaW1vLWZpbGUtdXBsb2FkLAouZHJvcHpvbmUgewogIGJvcmRlcjogMi41cHggZGFzaGVkIHZhcigtLWxoLWluaykgIWltcG9ydGFudDsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUpOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWNhcmQpOwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKfQoKLyogc3RhbGUgLyBlcnJvciBzdGF0ZXMgKi8KLmNlbGwuc3RhbGUsCltkYXRhLXN0YWxlPSJ0cnVlIl0geyBib3gtc2hhZG93OiBpbnNldCAzcHggMCAwIHZhcigtLWxoLXJ1c3QpOyB9CgoubWFyaW1vLWVycm9yLAoub3V0cHV0LWFyZWEgLmVycm9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxM3B4OwogIGJhY2tncm91bmQ6ICNGQkVERTc7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVzdCk7CiAgY29sb3I6ICM2RTJGMTQ7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBwYWRkaW5nOiAxMHB4IDEycHg7Cn0KCi8qIHNsaWRlcyAvIGFwcCB2aWV3ICovCi5zbGlkZXMsCltkYXRhLW1vZGU9InByZXNlbnQiXSAubWFya2Rvd24geyBmb250LXNpemU6IDE4cHg7IH0KCi8qIEEgc3R1ZGVudCB3aG8gaGFzIGFza2VkIGZvciBsZXNzIG1vdGlvbiBnZXRzIHRoZSBkcmF3aW5nIHdpdGhvdXQgdGhlCiAgIGJ1dHRvbiB0aGF0IG1vdmVzIHVuZGVyIHRoZSBwcmVzcy4gKi8KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOiByZWR1Y2UpIHsKICAubWFyaW1vLXJ1bi1idXR0b24sCiAgLm1hcmltby1idXR0b24sCiAgYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9InNlY29uZGFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7IHRyYW5zaXRpb246IG5vbmU7IH0KfQo="  # BUILT
    LECTURE_HALL_CSS = base64.b64decode(LECTURE_HALL_CSS_B64).decode("utf-8")

    INK = "#1D1E21"
    SOFT = "#6b6b6b"
    RULE = "#D9D2C2"
    PAPER = "#FFFDF7"
    BLUE = "#3959A6"
    RUST = "#B14434"
    OCHRE = "#DAB167"
    GREY = "#9A978E"
    GROUP_COLOURS = [BLUE, RUST, OCHRE, GREY]
    TEXT_ON = [PAPER, PAPER, INK, INK]
    SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"

    # Zachary (1977). Node numbers are the ones printed in his paper, 1 to 34;
    # the code counts from 0. FACTION[i] is the club person i+1 joined when the
    # club split in 1972: 0 = Mr. Hi's club, 1 = the officers' club.
    FACTION = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    POS = [[249, 127], [442, 202], [495, 195], [385, 266], [322, 22], [29, 173], [148, 69], [388, 314], [568, 187], [646, 291], [128, 22], [81, 188], [271, 302], [449, 121], [967, 207], [1022, 287], [22, 22], [402, 51], [953, 296], [524, 268], [1006, 242], [238, 261], [901, 314], [925, 84], [644, 22], [815, 22], [985, 80], [748, 89], [642, 107], [921, 178], [698, 285], [673, 67], [785, 247], [776, 185]]
    N = 34
    G = igraph.Graph.Famous("Zachary")
    EDGES = G.get_edgelist()
    A = np.array(G.get_adjacency().data, dtype=float)
    DEG = A.sum(axis=1)
    MR_HI, JOHN_A, NODE_9 = 0, 33, 8   # 0-indexed

    GROUPS = {
        1: "Shape: k-core",
        2: "Cut: cheapest split, divided by size",
        3: "Chance: modularity",
        4: "Pattern: stochastic block model",
    }

    # ---- the four methods -----------------------------------------------------

    def kcore_labels():
        """Shell number of each node: the largest k whose k-core holds the node.
        Shells are numbered from 0 here so that a label is a colour index."""
        return [c - 1 for c in G.coreness()]

    def cut_value(S, kind):
        """The three objectives of the lecture note, for the side S (boolean)."""
        k = int(S.sum())
        if k in (0, N):
            return np.inf
        cut = A[S][:, ~S].sum()
        if kind == "cut":
            return cut
        if kind == "ratio":
            return cut / (k * (N - k))
        return cut / (DEG[S].sum() * DEG[~S].sum())

    def cut_labels(kind):
        """Best two-way split under `kind`. "cut" is exact (igraph); the other two
        are searched: sweep along the second eigenvector of the Laplacian, then
        move one person at a time while the objective improves."""
        if kind == "cut":
            part = G.mincut().partition
            lab = [0] * N
            for i in part[1]:
                lab[i] = 1
            return lab
        if kind == "ratio":
            L = np.diag(DEG) - A
            f = np.linalg.eigh(L)[1][:, 1]
        else:
            L = np.eye(N) - A / np.sqrt(np.outer(DEG, DEG))
            f = np.linalg.eigh(L)[1][:, 1] / np.sqrt(DEG)
        order = np.argsort(f)
        best_val, best_S = np.inf, None
        for i in range(1, N):
            S = np.zeros(N, dtype=bool)
            S[order[:i]] = True
            v = cut_value(S, kind)
            if v < best_val:
                best_val, best_S = v, S.copy()
        improved = True
        while improved:
            improved = False
            for i in range(N):
                T = best_S.copy()
                T[i] = ~T[i]
                v = cut_value(T, kind)
                if v < best_val - 1e-15:
                    best_val, best_S, improved = v, T, True
        return best_S.astype(int).tolist()

    def modularity_labels(algorithm, seed):
        random.seed(seed)
        if algorithm == "Leiden":
            part = G.community_leiden(objective_function="modularity", n_iterations=-1)
        else:
            part = G.community_multilevel()
        return list(part.membership)

    def sbm_loglik(labels, B, degree_corrected):
        """Log-likelihood of the stochastic block model at its best edge
        probabilities. Plain: each pair of groups has one edge probability,
        p_rs = m_rs / (pairs between r and s). Degree-corrected: Karrer and
        Newman (2011), which lets every person have their own degree."""
        Z = np.zeros((N, B))
        Z[np.arange(N), labels] = 1.0
        m_rs = Z.T @ A @ Z
        if degree_corrected:
            kappa = Z.T @ DEG
            with np.errstate(divide="ignore", invalid="ignore"):
                t = m_rs * np.log(m_rs / np.outer(kappa, kappa))
            return float(np.nansum(np.where(m_rs > 0, t, 0.0)))
        n_r = Z.sum(axis=0)
        m = m_rs / 2.0
        pairs = np.outer(n_r, n_r)
        np.fill_diagonal(pairs, n_r * (n_r - 1) / 2.0)
        iu = np.triu_indices(B)
        m_e, n_e = m[iu], pairs[iu]
        keep = n_e > 0
        m_e, n_e = m_e[keep], n_e[keep]
        p = np.clip(m_e / n_e, 1e-12, 1 - 1e-12)
        return float(np.sum(m_e * np.log(p) + (n_e - m_e) * np.log(1 - p)))

    def sbm_labels(B, degree_corrected, n_init=30, seed=0):
        """Greedy search: start from a random assignment, move one person at a
        time to the group that raises the likelihood, repeat until nobody moves;
        keep the best of `n_init` starts. Exact search is out of reach."""
        rng = np.random.default_rng(seed)
        best_ll, best = -np.inf, None
        for _ in range(n_init):
            lab = rng.integers(0, B, size=N)
            lab[rng.permutation(N)[:B]] = np.arange(B)   # every group is used
            cur = sbm_loglik(lab, B, degree_corrected)
            for _sweep in range(50):
                moved = False
                for i in rng.permutation(N):
                    home = lab[i]
                    for b in range(B):
                        if b == home:
                            continue
                        lab[i] = b
                        v = sbm_loglik(lab, B, degree_corrected)
                        if v > cur + 1e-9:
                            cur, home, moved = v, b, True
                        else:
                            lab[i] = home
                if not moved:
                    break
            if cur > best_ll:
                best_ll, best = cur, lab.copy()
        return best.tolist()

    # ---- what a result looks like ---------------------------------------------

    def relabel(labels):
        """Colour index by order of first appearance, so a colour is not an
        accident of which label a method happened to use."""
        seen = {}
        return [seen.setdefault(x, len(seen)) for x in labels]

    def mismatches(labels):
        """For a two-group result: who sits on the other side from the real
        split, under the better of the two ways to name the sides."""
        lab = np.array(labels)
        fac = np.array(FACTION)
        same = int((lab == fac).sum())
        agree = max(same, N - same)
        wrong = np.where((lab == fac) != (same >= N - same))[0]
        return agree, wrong.tolist()

    def rings(labels, limit=8):
        """The people to ring as 'other side from the real split': only when the
        result is a two-way split and at most `limit` people differ. A result that
        disagrees about half the club has no few people worth pointing at."""
        if len(set(labels)) != 2:
            return set()
        wrong = mismatches(labels)[1]
        return set(wrong) if len(wrong) <= limit else set()

    def karate_svg(labels, wrong=(), width=760, ring=None, title="", keep=False, between=True):
        """The 34 people. Colour = the group this method puts them in. Circle =
        Mr. Hi's club, square = the officers' club (what actually happened).
        Dashed edges join people the method puts in different groups. A heavy
        ring marks the people in `wrong`; a thin ring marks the people in `ring`."""
        labels = labels if keep else relabel(labels)
        W, H = 1044, 336 + (22 if title else 0)
        top = 22 if title else 0
        out = [f'<svg viewBox="0 0 {W} {H}" width="{width}" xmlns="http://www.w3.org/2000/svg" '
               f'style="max-width:100%;height:auto;font-family:{SANS}">']
        if title:
            out.append(f'<text x="4" y="15" font-size="15" font-weight="600" fill="{INK}">{html.escape(title)}</text>')
        for u, v in EDGES:
            cross = between and labels[u] != labels[v]
            (x1, y1), (x2, y2) = POS[u], POS[v]
            dash = ' stroke-dasharray="5 4"' if cross else ""
            col = INK if cross else "#BDB8AA"
            out.append(f'<line x1="{x1}" y1="{y1 + top}" x2="{x2}" y2="{y2 + top}" '
                       f'stroke="{col}" stroke-width="{1.3 if cross else 1.6}"{dash}/>')
        for i in range(N):
            x, y = POS[i]
            y += top
            c = labels[i] % len(GROUP_COLOURS)
            fill, txt = GROUP_COLOURS[c], TEXT_ON[c]
            if FACTION[i] == 0:
                out.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>')
            else:
                out.append(f'<rect x="{x - 13}" y="{y - 13}" width="26" height="26" rx="3" fill="{fill}" '
                           f'stroke="{INK}" stroke-width="1.2"/>')
            if i in wrong:
                out.append(f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="{INK}" stroke-width="3"/>')
            elif ring and i in ring:
                out.append(f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="{INK}" stroke-width="1.5"/>')
            out.append(f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" font-size="12.5" font-weight="600" '
                       f'fill="{txt}">{i + 1}</text>')
        out.append("</svg>")
        return "".join(out)

    def legend(wrong=False, between=True):
        s = ("<div style='font-size:0.82rem;color:#6b6b6b;margin:0.2rem 0 0.6rem'>"
             "Colour: the group this method puts a person in. "
             "<b>Circle</b>: joined Mr. Hi's club in 1972. <b>Square</b>: joined the officers' club."
             + (" Dashed line: an edge between two groups." if between else ""))
        if wrong:
            s += " Heavy ring: sits on the other side from the real split."
        return mo.Html(s + "</div>")

    def summary(labels, keep=False):
        """The numbers any result can be asked for, as a table. With keep=True
        the labels are used as given (k-core shells are numbered by k)."""
        lab = list(labels) if keep else relabel(labels)
        k = max(lab) + 1
        Q = G.modularity(lab)
        between = sum(lab[u] != lab[v] for u, v in EDGES)
        rows = []
        for c in range(k):
            members = [i for i in range(N) if lab[i] == c]
            hi = sum(FACTION[i] == 0 for i in members)
            sw = GROUP_COLOURS[c % len(GROUP_COLOURS)]
            rows.append(
                f"<tr><td><span style='color:{sw};font-size:1.2rem'>&#9679;</span> {c + 1}</td>"
                f"<td>{len(members)}</td><td>{hi}</td><td>{len(members) - hi}</td>"
                f"<td style='font-size:0.82rem'>{', '.join(str(i + 1) for i in members)}</td></tr>"
            )
        head = ("<tr><th>Group</th><th>People</th><th>Mr. Hi's club</th><th>Officers' club</th>"
                "<th>Members (node numbers)</th></tr>")
        facts = (f"<b>{k}</b> groups &nbsp;·&nbsp; modularity <b>Q = {Q:.4f}</b> &nbsp;·&nbsp; "
                 f"<b>{between}</b> of {len(EDGES)} edges run between groups")
        if k == 2:
            agree, wrong = mismatches(lab)
            who = ", ".join(str(i + 1) for i in wrong) or "nobody"
            facts += (f" &nbsp;·&nbsp; same side as the real split for <b>{agree}</b> of {N} people "
                      f"(other side: {who})")
        return mo.Html(f"<p>{facts}</p><table style='width:100%'>{head}{''.join(rows)}</table>")


@app.cell(hide_code=True)
def _():
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # The pitch: one result on the karate club

    In 1970–72 Wayne Zachary recorded who met whom outside the karate club's classes. In 1972 the club split in two over a fee dispute: 17 people left with the instructor, Mr. Hi, and 17 stayed with the administrator, John A. That split is the only data point here that actually happened.

    Your group has one definition of "community" and the result it gives on this network. **Pick your group number.** The sheet says which method it is.
    """)
    return


@app.cell(hide_code=True)
def _():
    who = mo.ui.dropdown(
        options={f"Group {k}": k for k in GROUPS},
        label="Your group",
    )
    who
    return (who,)


@app.cell(hide_code=True)
def _():
    # The knobs, all created here so that turning one does not reset the others.
    k_slider = mo.ui.slider(1, 4, value=4, step=1, label="k", show_value=True)
    cut_kind = mo.ui.dropdown(
        options={
            "Cut (fewest edges between the two sides)": "cut",
            "Ratio cut: cut / (n1 × n2)": "ratio",
            "Normalized cut: cut / (vol1 × vol2)": "ncut",
        },
        value="Normalized cut: cut / (vol1 × vol2)",
        label="Objective",
    )
    algo = mo.ui.dropdown(options=["Leiden", "Louvain"], value="Leiden", label="Algorithm")
    seed = mo.ui.slider(0, 9, value=7, step=1, label="Random seed", show_value=True)
    blocks = mo.ui.slider(2, 4, value=2, step=1, label="Number of groups", show_value=True)
    dc = mo.ui.switch(label="Degree-corrected")
    return algo, blocks, cut_kind, dc, k_slider, seed


@app.cell(hide_code=True)
def _(algo, blocks, cut_kind, dc, k_slider, seed, who):
    if who.value is None:
        _out = mo.callout(mo.md("Choose your group above."), kind="neutral")
    elif who.value == 1:
        _shell = kcore_labels()
        _k = k_slider.value
        _core = [i for i in range(N) if _shell[i] + 1 >= _k]
        _hi = sum(FACTION[i] == 0 for i in _core)
        _cliques = G.maximal_cliques()
        _out = mo.vstack([
            mo.md(r"""
    ## Group 1 — Shape: k-core

    **Definition.** The *k-core* is the largest set of people in which everyone has at least $k$ neighbours inside the set. A person's *shell* is the largest $k$ for which they are in the $k$-core. Colour = shell.
    """),
            mo.Html(karate_svg(_shell, ring=set(_core), keep=True, between=False)),
            legend(between=False),
            summary(_shell, keep=True),
            mo.md("**Turn the knob.** The ringed people are the $k$-core for the $k$ below."),
            k_slider,
            mo.md(
                f"The {_k}-core has **{len(_core)}** people: **{_hi}** from Mr. Hi's club and "
                f"**{len(_core) - _hi}** from the officers' club. "
                f"The largest clique (everyone knows everyone) has **{max(len(c) for c in _cliques)}** people."
            ),
        ])
    elif who.value == 2:
        _lab = cut_labels(cut_kind.value)
        _wrong = rings(_lab)
        _S = np.array(_lab, dtype=bool)
        _out = mo.vstack([
            mo.md(r"""
    ## Group 2 — Cut: the cheapest split, divided by size

    **Definition.** A community is one side of a split into two. A split is scored by its *cut*, the number of edges between the sides $\text{Cut}(V_1,V_2)=\sum_{i\in V_1}\sum_{j\in V_2}A_{ij}$, divided by a term for the size of the sides. The ratio and normalized objectives are searched (start from the second eigenvector of the Laplacian, then move one person at a time while the score improves), so the result is the best found, not a proof of the best.
    """),
            mo.Html(karate_svg(_lab, wrong=_wrong)),
            legend(wrong=bool(_wrong)),
            summary(_lab),
            mo.md("**Turn the knob.** Change what is being minimized."),
            cut_kind,
            mo.md(
                f"Objective value of this split: **{cut_value(_S, cut_kind.value):.5g}**."
            ),
        ])
    elif who.value == 3:
        _lab = modularity_labels(algo.value, seed.value)
        _qs = [G.modularity(modularity_labels(algo.value, s)) for s in range(10)]
        _out = mo.vstack([
            mo.md(r"""
    ## Group 3 — Chance: modularity

    **Definition.** A community is a set of people with more edges inside it than a random network with the same degrees would put there. Modularity is $Q=\frac{1}{2m}\sum_{ij}\left[A_{ij}-\frac{k_ik_j}{2m}\right]\delta(c_i,c_j)$, and the algorithm searches for the grouping with the highest $Q$. The number of groups is not given; the score chooses it.
    """),
            mo.Html(karate_svg(_lab)),
            legend(),
            summary(_lab),
            mo.md("**Turn the knob.** Louvain starts from a random order of nodes, so the seed changes the answer. Leiden is the variant that keeps every group connected."),
            mo.hstack([algo, seed], justify="start"),
            mo.md(f"Q over the ten seeds 0–9: lowest **{min(_qs):.4f}**, highest **{max(_qs):.4f}**."),
        ])
    else:
        _lab = sbm_labels(blocks.value, dc.value)
        _wrong = rings(_lab)
        _deg = [float(np.mean([DEG[i] for i in range(N) if relabel(_lab)[i] == c])) for c in range(max(relabel(_lab)) + 1)]
        _out = mo.vstack([
            mo.md(r"""
    ## Group 4 — Pattern: the stochastic block model

    **Definition.** A community is a set of people who connect to every group in the same way. Each pair of people is joined with a probability that depends only on the two people's groups. The fit chooses the grouping under which the observed network is most likely. The *degree-corrected* version also lets every person have their own degree.
    """),
            mo.Html(karate_svg(_lab, wrong=_wrong)),
            legend(wrong=bool(_wrong)),
            summary(_lab),
            mo.md("**Turn the knobs.** Number of groups, and whether people are allowed to differ in degree."),
            mo.hstack([blocks, dc], justify="start"),
            mo.md("Mean degree per group: " + ", ".join(f"**{d:.1f}**" for d in _deg) + "."),
        ])
    _out
    return


@app.cell(hide_code=True)
def _():
    show_all = mo.ui.switch(label="Show all four results (after the pitches)")
    mo.vstack([mo.md("---\n\n## After the pitches"), show_all])
    return (show_all,)


@app.cell(hide_code=True)
def _(show_all):
    if not show_all.value:
        _out = mo.md("")
    else:
        _runs = [
            ("1 · k-core shells", kcore_labels(), ()),
            ("2 · normalized cut", cut_labels("ncut"), None),
            ("3 · modularity (Leiden)", modularity_labels("Leiden", 0), ()),
            ("4 · stochastic block model, 2 groups", sbm_labels(2, False), None),
        ]
        _blocks = []
        for _title, _lab, _w in _runs:
            _wrong = rings(_lab) if _w is None else set()
            _keep = _title.startswith("1")
            _blocks.append(mo.vstack([
                mo.Html(karate_svg(_lab, wrong=_wrong, width=520, title=_title, keep=_keep)),
                summary(_lab, keep=_keep),
            ]))
        _out = mo.vstack([
            legend(wrong=True),
            mo.hstack(_blocks[0:2], widths="equal", align="start"),
            mo.hstack(_blocks[2:4], widths="equal", align="start"),
        ])
    _out
    return


if __name__ == "__main__":
    app.run()
