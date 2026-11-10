# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "altair==5.5.0",
#     "anywidget",
#     "gensim==4.4.0",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "python-igraph==0.11.9",
#     "scipy==1.15.3",
#     "traitlets",
# ]
# ///
#
# The Module 8 lab: character embeddings (the two lab slides of
# slides/m08/m08-embedding.md). Les Miserables from CSV, random walks in NumPy,
# word2vec, a picture of the embedding and the network in the same colours,
# then the walk with restart into the same word2vec. Two blanks, coded in class
# with the lecturer: random_walk and random_walk_with_restart.
#
#   * The stylesheet travels inside the file (molab ignores css_file). Refresh
#     it with `python tools/build_lab_notebooks.py m08-embedding`, which also
#     writes lab-solutions.py.
#   * The data is read from the course repository on GitHub (main branch).
#   * Sections start folded: marimo keeps the folded state in the browser, not
#     in the file, so FoldSections (last cell) clicks marimo's fold toggles once
#     after the page has drawn. FOLD_CSS makes the toggles visible.
#   * gensim's compiled code now and then prints "Exception ignored in:
#     'gensim.models.word2vec_inner.our_dot_float'" with no exception set. It
#     is harmless; quiet() keeps it off the page.

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import base64
    import contextlib
    import io
    import random
    import warnings

    import altair as alt
    import anywidget
    import igraph
    import marimo as mo
    import numpy as np
    import pandas as pd
    import traitlets

    # molab ignores css_file (marimo-team/marimo#8467), so lecture-hall.css is
    # carried here as base64 and injected by the first cell.
    LECTURE_HALL_CSS_B64 = "LyogTGVjdHVyZSBIYWxsIOKAlCBtYXJpbW8gY3VzdG9tIENTUywgZHJhd24gYnkgaGFuZAogICBVc2FnZTogcHV0IHRoaXMgbmV4dCB0byB5b3VyIG5vdGVib29rIGFuZCBhZGQgdG8gdGhlIG5vdGVib29rJ3MgY29uZmlnOgogICAgIFtkaXNwbGF5XSBjc3NfZmlsZSA9ICJsZWN0dXJlLWhhbGwuY3NzIgogICBvciBpbiBtYXJpbW8udG9tbCB1bmRlciBbZGlzcGxheV0uCgogICBUaGUgbm90ZWJvb2sgaXMgYSBsZWN0dXJlIG5vdGUgdGhlIHN0dWRlbnQgYW5kIHRoZSB0dXRvciBmaWxsIGluIHRvZ2V0aGVyLAogICBzbyBpdCBpcyBkcmVzc2VkIGFzIG9uZTogZG90LWdyaWQgcGFwZXIsIHdvYmJseSBpbmsgYm9yZGVycywgYW5kIHNlY3Rpb24KICAgcnVsZXMgZHJhd24gd2l0aCBhIHBlbi4KCiAgIFRIRSBIQU5EIElTIElOIFRIRSBMSU5FUywgTk9UIElOIFRIRSBMRVRURVJTLiBBIGhhbmR3cml0aW5nIGZhY2UgZm9yIHRoZQogICBwcm9zZSB3YXMgdGlyaW5nIHRvIHJlYWQgb3ZlciBuaW5ldHkgbWludXRlcyBhbmQgbWFkZSB0aGUgcGFnZSBsb29rIGxpa2UgYQogICBncmVldGluZyBjYXJkIHJhdGhlciB0aGFuIGEgbGVjdHVyZSBub3RlLiBTbyB0aGUgdHlwZSBpcyBleGFjdGx5IHRoZSBjb3Vyc2UKICAgbGVjdHVyZSBub3RlJ3MgKGFkdi1uZXQtc2NpL2xlY3R1cmUtbm90ZS9zY3NzL21pbmltYWwuc2Nzcyk6IGEgc3lzdGVtIHNhbnMKICAgZm9yIHRoZSBib2R5LCBhIHN5c3RlbSBzZXJpZiBmb3IgdGhlIGhlYWRpbmdzLCAxOHB4LzEuNjUg4oCUIHRoZSBzYW1lCiAgIHJlYWRpbmcgZXhwZXJpZW5jZSBvbiBib3RoIGhhbHZlcyBvZiB0aGUgY291cnNlLiBXaGF0IHN0YXlzIGhhbmQtZHJhd24gaXMKICAgZXZlcnl0aGluZyB0aGF0IGlzIG5vdCByZWFkIGFzIGEgd29yZDogdGhlIHdhdnkgc2VjdGlvbiBydWxlcywgdGhlIHdvYmJseQogICBib3JkZXJzIGFuZCBwZW4gc2hhZG93cywgdGhlIHNrZXRjaGVkIG1hdHBsb3RsaWIgc3Ryb2tlcywgYW5kIG5ldHZpeidzCiAgIHR1cmJ1bGVudCBlZGdlcy4KCiAgIE5vIHdlYmZvbnQsIG5vIG5ldHdvcmsgcmVxdWVzdDogYSBzdHVkZW50IG9uIGEgcGxhbmUgZ2V0cyB0aGUgc2FtZSBwYWdlLAogICBhbmQgdGhlcmUgaXMgbm8gZmlyc3QtcGFpbnQgZmxhc2ggb2YgYSBmYWxsYmFjayBmYWNlLgoKICAgVGhlIGFjY2VudHMgYXJlIHRoZSBMRUNUVVJFIFNMSURFUycgYWNjZW50cywgdmVyYmF0aW0g4oCUIHRoZSBtb2R1bGUgaXMgb25lCiAgIGNvdXJzZSwgc28gdGhlIGNvbG91ciB0aGF0IG1lYW5zICJ0aGUgdGhpbmcgd2UgYXJlIGxvb2tpbmcgYXQiIGhhcyB0byBtZWFuCiAgIGl0IGluIGJvdGggaGFsdmVzLiBDaGFuZ2Ugb25lIG9mIHRoZW0gaGVyZSBhbmQgeW91IG11c3QgY2hhbmdlIGl0IGluCiAgIGFkdi1uZXQtc2NpL3NsaWRlcy9tMDIvZmlndXJlcy9tYWtlX2ZpZ3VyZXMucHkgdG9vLCBhbmQgaW4gZXZlcnkgY2VsbHMvKi5weQogICB0aGF0IGhhcmRjb2RlcyBpdCAodGhleSBhbGwgZG8sIGZvciB0aGVpciBub2RlcyBhbmQgZWRnZXMpLiAqLwoKOnJvb3QgewogIC8qIHBhbGV0dGUg4oCUIHRoZSB0aHJlZSBhY2NlbnRzIGNvbWUgZnJvbSB0aGUgc2xpZGUgZGVjawogICAgIChtYWtlX2ZpZ3VyZXMucHk6IEFDQ0VOVCAvIEFDQ0VOVDIgLyBBQ0NFTlQzKSwgYW5kIHRoZSBwcmVtYWRlIGNlbGxzCiAgICAgaGFyZGNvZGUgdGhlIHNhbWUgaGV4ZXMgZm9yIHRoZWlyIG5vZGVzIGFuZCBlZGdlcywgc28gYSByZXBhaW50IGhlcmUKICAgICBkZXN5bmNzIGJvdGguIFdoYXQgaXMgTk9UIHRoZSBzbGlkZXMnIGlzIHRoZSBwYXBlcjogd2hpdGUgYmVjYW1lIHdhcm0sCiAgICAgYW5kIHRoZSBwZW5jaWwgcnVsZSAoLS1saC1ydWxlKSBpcyBhIG5ldyB0b2tlbiByYXRoZXIgdGhhbiBhIHJlcGFpbnQgb2YKICAgICAtLWxoLWxpbmUsIHdoaWNoIGlzIGEgbm9kZSBmaWxsIGluIGNwMiBhbmQgY3A1LiAqLwogIC0tbGgtcGFwZXI6ICAgI0ZGRkRGNzsKICAtLWxoLWNhcmQ6ICAgICNGRkZGRkY7CiAgLS1saC1zdXJmYWNlOiAjRjZGMkU5OwogIC0tbGgtbGluZTogICAgI0U0RTZFQTsKICAtLWxoLXJ1bGU6ICAgICNEOUQyQzI7CiAgLS1saC1pbms6ICAgICAjMUQxRTIxOwogIC0tbGgtaW5rLTI6ICAgIzM1MzczQzsKICAtLWxoLW11dGVkOiAgICM2QTZENzU7CiAgLS1saC1ibHVlOiAgICAjMjIzMzZCOwogIC0tbGgtYmx1ZS0yOiAgIzM5NTlBNjsKICAtLWxoLXJ1c3Q6ICAgICNCMTQ0MzQ7CgogIC8qIHR5cGUg4oCUIHRoZSBsZWN0dXJlIG5vdGUncyB0aHJlZSBzdGFja3MsIHZlcmJhdGltLiBBbGwgZnJvbSB0aGUgc3lzdGVtOgogICAgIG5vdGhpbmcgaGVyZSBpcyBmZXRjaGVkLiAqLwogIC0tbGgtc2VyaWY6ICAgIklvd2FuIE9sZCBTdHlsZSIsICJQYWxhdGlubyBMaW5vdHlwZSIsIFBhbGF0aW5vLAogICAgICAgICAgICAgICAgIkJvb2sgQW50aXF1YSIsICJIb2VmbGVyIFRleHQiLCBHZW9yZ2lhLAogICAgICAgICAgICAgICAgIlRpbWVzIE5ldyBSb21hbiIsIHNlcmlmOwogIC0tbGgtc2FuczogICAgc3lzdGVtLXVpLCAtYXBwbGUtc3lzdGVtLCAiU2Vnb2UgVUkiLCBSb2JvdG8sCiAgICAgICAgICAgICAgICAiSGVsdmV0aWNhIE5ldWUiLCAiTm90byBTYW5zIiwgIkxpYmVyYXRpb24gU2FucyIsIEFyaWFsLAogICAgICAgICAgICAgICAgc2Fucy1zZXJpZjsKICAtLWxoLW1vbm86ICAgIHVpLW1vbm9zcGFjZSwgU0ZNb25vLVJlZ3VsYXIsICJTRiBNb25vIiwgTWVubG8sIENvbnNvbGFzLAogICAgICAgICAgICAgICAgIkxpYmVyYXRpb24gTW9ubyIsIG1vbm9zcGFjZTsKICAvKiBUaGUgb25lIGhhbmQtd3JpdHRlbiBmYWNlIG9uIHRoZSBwYWdlLCBhbmQgaXQgd3JpdGVzIGV4YWN0bHkgb25lIHRoaW5nOgogICAgIHRoZSBzdHVkZW50J3Mgb3duIGFuc3dlcnMsIGluc2lkZSB0aGUgZm9sZC4gUHJpbnRlZCBub3RlLCBoYW5kd3JpdHRlbgogICAgIG1hcmdpbiDigJQgdGhlIGRpZmZlcmVuY2UgYmV0d2VlbiB0aGUgdHdvIGlzIHRoZSBwb2ludC4gU3lzdGVtIGZhY2VzIG9ubHksCiAgICAgbGlrZSBldmVyeXRoaW5nIGVsc2UgaGVyZTogbWFjT1Mgc2hpcHMgdGhlIGZpcnN0IHR3bywgV2luZG93cyB0aGUgbmV4dAogICAgIHR3bywgYGN1cnNpdmVgIGNhdGNoZXMgdGhlIHJlc3QuICovCiAgLS1saC1oYW5kOiAgICAiQ2hhbGtib2FyZCBTRSIsICJCcmFkbGV5IEhhbmQiLCAiU2Vnb2UgUHJpbnQiLAogICAgICAgICAgICAgICAgIkNvbWljIFNhbnMgTVMiLCBjdXJzaXZlOwoKICAvKiB0aGUgaGFuZC1kcmF3biBraXQ6IHR3byByb3VuZGluZyBzZXRzLCBhbHRlcm5hdGVkIHNvIG5vIHR3byBib3hlcyBvbiB0aGUKICAgICBwYWdlIGhhdmUgdGhlIHNhbWUgY29ybmVycywgYW5kIG9uZSBpbmsgc2hhZG93IHRoYXQgZmFrZXMgYSBzZWNvbmQgcGFzcwogICAgIG9mIHRoZSBwZW4uICovCiAgLS1saC13b2JibGU6ICAgMTRweCA2cHggMTZweCA4cHggLyA4cHggMTZweCA2cHggMTRweDsKICAtLWxoLXdvYmJsZS0yOiA2cHggMTZweCA4cHggMTRweCAvIDE2cHggNnB4IDE0cHggOHB4OwogIC0tbGgtcGVuOiAgICAgIDNweCA0cHggMCAtMXB4IHJnYmEoMzUsIDM0LCA0MywgMC4xNik7CiAgLS1saC1wZW4tc29mdDogMnB4IDNweCAwIC0xcHggcmdiYSgzNSwgMzQsIDQzLCAwLjEyKTsKCiAgLyogYSB3YXZ5IHN0cm9rZSwgdXNlZCBmb3IgdW5kZXJsaW5lcyBhbmQgdGFibGUgcnVsZXMgKi8KICAtLWxoLXN0cm9rZTogdXJsKCJkYXRhOmltYWdlL3N2Zyt4bWwsJTNDc3ZnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Zycgd2lkdGg9JzEyMCcgaGVpZ2h0PSc3JyB2aWV3Qm94PScwIDAgMTIwIDcnJTNFJTNDcGF0aCBkPSdNMSA0LjRDMjAgMS45IDQwIDYuMiA2MCAzLjcgODAgMS40IDEwMCA1LjYgMTE5IDMuMicgZmlsbD0nbm9uZScgc3Ryb2tlPSclMjNCMTQ0MzQnIHN0cm9rZS13aWR0aD0nMicgc3Ryb2tlLWxpbmVjYXA9J3JvdW5kJy8lM0UlM0Mvc3ZnJTNFIik7CiAgLS1saC1zdHJva2UtZmFpbnQ6IHVybCgiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMjAnIGhlaWdodD0nNycgdmlld0JveD0nMCAwIDEyMCA3JyUzRSUzQ3BhdGggZD0nTTEgNC40QzIwIDEuOSA0MCA2LjIgNjAgMy43IDgwIDEuNCAxMDAgNS42IDExOSAzLjInIGZpbGw9J25vbmUnIHN0cm9rZT0nJTIzRDlEMkMyJyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcvJTNFJTNDL3N2ZyUzRSIpOwoKICAvKiBtYXJpbW8gdG9rZW5zICovCiAgLS1iYWNrZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1pbmspOwogIC0tY2FyZDogdmFyKC0tbGgtY2FyZCk7CiAgLS1jYXJkLWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1wb3BvdmVyOiB2YXIoLS1saC1jYXJkKTsKICAtLXBvcG92ZXItZm9yZWdyb3VuZDogdmFyKC0tbGgtaW5rKTsKICAtLW11dGVkOiB2YXIoLS1saC1zdXJmYWNlKTsKICAtLW11dGVkLWZvcmVncm91bmQ6IHZhcigtLWxoLW11dGVkKTsKICAtLWJvcmRlcjogdmFyKC0tbGgtbGluZSk7CiAgLS1pbnB1dDogdmFyKC0tbGgtbGluZSk7CiAgLS1yaW5nOiB2YXIoLS1saC1ibHVlKTsKICAtLXByaW1hcnk6IHZhcigtLWxoLWJsdWUpOwogIC0tcHJpbWFyeS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1zZWNvbmRhcnk6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tc2Vjb25kYXJ5LWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1hY2NlbnQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tYWNjZW50LWZvcmVncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIC0tZGVzdHJ1Y3RpdmU6IHZhcigtLWxoLXJ1c3QpOwogIC0tZGVzdHJ1Y3RpdmUtZm9yZWdyb3VuZDogdmFyKC0tbGgtcGFwZXIpOwogIC0tcmFkaXVzOiAzcHg7CgogIC0tdGV4dC1mb250OiB2YXIoLS1saC1zYW5zKTsKICAtLWhlYWRpbmctZm9udDogdmFyKC0tbGgtc2VyaWYpOwogIC0tY29kZS1mb250OiB2YXIoLS1saC1tb25vKTsKfQoKLyogLS0tLS0tLS0tLSBwYWdlIC0tLS0tLS0tLS0gKi8KCi8qIERvdC1ncmlkLCBub3QgcnVsZWQgbGluZXM6IHRoZSBzYW1lICJ0aGlzIGlzIGEgc2tldGNoYm9vayIgc2lnbmFsLCBidXQgaXQKICAgZG9lcyBub3QgZmlnaHQgYSBsaW5lIG9mIHByb3NlIGZvciB0aGUgc2FtZSBob3Jpem9udGFsIGJhbmQuICovCmJvZHksCiNBcHAgewogIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWxoLXBhcGVyKTsKICBiYWNrZ3JvdW5kLWltYWdlOiByYWRpYWwtZ3JhZGllbnQocmdiYSgzMSwgNTgsIDk1LCAwLjA4NSkgMXB4LCB0cmFuc3BhcmVudCAxcHgpOwogIGJhY2tncm91bmQtc2l6ZTogMjRweCAyNHB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIC13ZWJraXQtZm9udC1zbW9vdGhpbmc6IGFudGlhbGlhc2VkOwp9CgovKiAtLS0tLS0tLS0tIHByb3NlIC0tLS0tLS0tLS0gKi8KCi5tYXJrZG93biwKLnByb3NlIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgZm9udC1zaXplOiAxOHB4OwogIGxpbmUtaGVpZ2h0OiAxLjY1OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgdGV4dC13cmFwOiBwcmV0dHk7CiAgbWF4LXdpZHRoOiA2OGNoOwp9CgovKiBUaGUgbGVjdHVyZSBub3RlJ3Mgc2VyaWYgYW5kIGl0cyBzY2FsZSDigJQgaDEgMi4wNSAvIGgyIDEuNTUgLyBoMyAxLjIyIC8KICAgaDQgMS4wMiBhZ2FpbnN0IGl0cyAxOHB4IHJvb3QuIFdyaXR0ZW4gb3V0IGluIHB4IGJlY2F1c2UgbWFyaW1vJ3Mgcm9vdAogICBzdGF5cyB0aGUgYnJvd3NlcidzIDE2cHgsIHNvIGEgcmVtIGhlcmUgd291bGQgYmUgYSBkaWZmZXJlbnQgc2l6ZSB0aGFuCiAgIHRoZSBzYW1lIHJlbSBvbiB0aGUgbm90ZS4gKi8KLm1hcmtkb3duIGgxLCAubWFya2Rvd24gaDIsIC5tYXJrZG93biBoMywgLm1hcmtkb3duIGg0LAoucHJvc2UgaDEsIC5wcm9zZSBoMiwgLnByb3NlIGgzLCAucHJvc2UgaDQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zZXJpZik7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtaW5rKTsKICBsaW5lLWhlaWdodDogMS4yNTsKICBsZXR0ZXItc3BhY2luZzogMDsKfQoKLm1hcmtkb3duIGgxLCAucHJvc2UgaDEgewogIGZvbnQtc2l6ZTogMzdweDsKICBtYXJnaW46IDAgMCAyMnB4OwogIGxldHRlci1zcGFjaW5nOiAtMC4wMWVtOwp9CgovKiBBIGNoYXB0ZXIgYnJlYWsg4oCUIG9uZSBvZiB0aGUgdHdvIHBsYWNlcyB0aGUgcGVuIHN0aWxsIHdyaXRlcy4gKi8KLm1hcmtkb3duIGgyLCAucHJvc2UgaDIgewogIGZvbnQtc2l6ZTogMjhweDsKICBtYXJnaW46IDUwcHggMCAxNnB4OwogIHBhZGRpbmctYm90dG9tOiAwLjE4ZW07CiAgYmFja2dyb3VuZC1pbWFnZTogdmFyKC0tbGgtc3Ryb2tlKTsKICBiYWNrZ3JvdW5kLXJlcGVhdDogcmVwZWF0LXg7CiAgYmFja2dyb3VuZC1wb3NpdGlvbjogbGVmdCBib3R0b207CiAgYmFja2dyb3VuZC1zaXplOiAxMjBweCA3cHg7Cn0KCi8qIEEgbm90ZSBjZWxsJ3Mgb3duIHRpdGxlIChgIyMjIPCfk48gRGlzdGFuY2UgYW5kIGF2ZXJhZ2UgcGF0aCBsZW5ndGhgKS4gSXQgaXMKICAgc2V0IGxhcmdlciB0aGFuIHRoZSBwcm9zZSBiZW5lYXRoIGl0IHNvIHRoZSBmaW5pc2hlZCBub3RlYm9vayByZWFkcyBhcyBhCiAgIHJ1biBvZiBzZWN0aW9ucywgbm90IG9uZSBsb25nIGNvbHVtbi4gKi8KLm1hcmtkb3duIGgzLCAucHJvc2UgaDMgeyBmb250LXNpemU6IDIycHg7IG1hcmdpbjogMzZweCAwIDEzcHg7IH0KCi8qIFF1aWV0ZXIgdGhhbiBoMzogc2l6ZSBhbmQgd2VpZ2h0IG9ubHksIG5ldmVyIGEgcnVsZS4gKi8KLm1hcmtkb3duIGg0LCAucHJvc2UgaDQgeyBmb250LXNpemU6IDE4cHg7IG1hcmdpbjogMjdweCAwIDlweDsgfQoKLm1hcmtkb3duIGEsIC5wcm9zZSBhIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyB0ZXh0LWRlY29yYXRpb24tY29sb3I6IHZhcigtLWxoLWxpbmUpOyB9Ci5tYXJrZG93biBhOmhvdmVyLCAucHJvc2UgYTpob3ZlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBjdXJyZW50Q29sb3I7IH0KCi5tYXJrZG93biBzdHJvbmcsIC5wcm9zZSBzdHJvbmcgeyBjb2xvcjogdmFyKC0tbGgtaW5rKTsgZm9udC13ZWlnaHQ6IDcwMDsgfQoKLyogQSBxdW90ZSBjYXJyaWVzIE5PIGNocm9tZSBhdCBhbGw6IG5vIGZpbGwsIG5vIGJvcmRlciwgbm90IGV2ZW4gYSBydWxlIGluCiAgIHRoZSBtYXJnaW4g4oCUIGdyZXkgaW5rIGlzIHRoZSB3aG9sZSB0cmVhdG1lbnQuCgogICBJdCBoYXMgYmVlbiB3YWxrZWQgZG93biBvbmUgc3RlcCBhdCBhIHRpbWUgYW5kIGVhY2ggc3RlcCB3YXMgcmlnaHQuIEl0CiAgIHN0YXJ0ZWQgYXMgYSBzY3JhcCBvZiBwYXBlciBwaW5uZWQgdG8gdGhlIHBhZ2UgKGZpbGxlZCwgbmF2eS1ib3JkZXJlZCwKICAgc2hhZG93ZWQsIHRpbHRlZCBhIHF1YXJ0ZXIgZGVncmVlKSwgd2hpY2ggc2FpZCBMT09LIEFUIFRISVMgYWJvdXQgYSBsaW5lCiAgIHRoZSByZWFkZXIgaGFkIGFscmVhZHkgY2xpY2tlZCB0byBvcGVuLiBUaGVuIGEgbWFyZ2luIHJ1bGUsIHdoaWNoIHN0aWxsCiAgIGRyZXcgYSB2ZXJ0aWNhbCBsaW5lIGRvd24gYSBwYWdlIHRoYXQgaGFzIHBsZW50eS4gV2hhdCBpcyBsZWZ0IGlzIHdoYXQKICAgdGhlIHF1b3RlIGFjdHVhbGx5IGlzOiB0aGUgc3R1ZGVudCdzIG93biB3b3JkcywgaW4gdGhlIHBhZ2UncyBxdWlldCBncmV5LAogICB1bmRlciBhIGhlYWRpbmcgdGhhdCBhbHJlYWR5IG5hbWVzIHRoZW0uICM2QTZENzUgb24gd2hpdGUgaXMgNS4yOjEg4oCUCiAgIHF1aWV0IGlzIG5vdCB0aGUgc2FtZSBhcyB1bnJlYWRhYmxlLCBhbmQgdGhpcyBsaW5lIGlzIHRoZSBncmFkZWQgb25lLiAqLwoubWFya2Rvd24gYmxvY2txdW90ZSwKLnByb3NlIGJsb2NrcXVvdGUgewogIG1hcmdpbjogMS40ZW0gMDsKICBwYWRkaW5nOiAwOwogIGJhY2tncm91bmQ6IG5vbmU7CiAgYm9yZGVyOiAwOwogIGJvcmRlci1yYWRpdXM6IDA7CiAgYm94LXNoYWRvdzogbm9uZTsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGZvbnQtc3R5bGU6IG5vcm1hbDsKfQoKLyogLS0tLS0tLS0tLSB0aGUgc3R1ZGVudCdzIG93biBhbnN3ZXIsIGZvbGRlZCAtLS0tLS0tLS0tICovCgovKiBFdmVyeSBub3RlIGNlbGwgZW5kcyB3aXRoIHdoYXQgdGhlIHN0dWRlbnQgc2FpZCwgcXVvdGVkIHZlcmJhdGltLiBMZWZ0CiAgIG9wZW4gaXQgd2FzIHRoZSBsb3VkZXN0IHRoaW5nIG9uIHRoZSBwYWdlIOKAlCBhIGJvcmRlcmVkLCBzaGFkb3dlZCBzbGFiCiAgIHVuZGVyIGV2ZXJ5IHNpbmdsZSBub3RlLCBjb21wZXRpbmcgd2l0aCB0aGUgZmlndXJlIGFib3ZlIGl0IGFuZCB3aXRoIHRoZQogICBleHBsYW5hdGlvbiB0aGUgbm90ZSBleGlzdHMgdG8gZ2l2ZS4gU28gaXQgaXMgZm9sZGVkOiB0aGUgbm90ZSByZWFkcyBhcwogICB0aGUgbGVjdHVyZSBub3RlIGl0IGlzLCBhbmQgdGhlIGFuc3dlciBpcyBvbmUgY2xpY2sgYXdheS4KICAgYG1vLm1kYCByZW5kZXJzIGAvLy8gZGV0YWlscyB8IE15IGFuc3dlcmAgKyBgdHlwZTogbGgtYW5zd2VyYCBpbnRvIHRoaXMuCgogICBDbG9zZWQsIGl0IGlzIGEgZGFzaGVkIHRhYiBpbiB0aGUgbWFyZ2luIGNvbG91ciDigJQgcHJlc2VudCwgcXVpZXQsIGNsZWFybHkKICAgcHJlc3NhYmxlLiBPcGVuLCBpdCBpcyB0aGVpciB3b3JkcyBiZWhpbmQgYSBtYXJnaW4gcnVsZSwgYW5kIG5vdGhpbmcgZWxzZToKICAgYSByZWFkZXIgd2hvIGNsaWNrZWQgdG8gc2VlIHRoZSBhbnN3ZXIgZG9lcyBub3QgYWxzbyBuZWVkIGl0IGJveGVkLiAqLwovKiBtYXJpbW8gZHJlc3NlcyBFVkVSWSBgLm1hcmtkb3duIGRldGFpbHNgIGFzIGFuIGFkbW9uaXRpb24sIGFuZCB0aGVyZSBpcyBubwogICBvcHRpbmcgb3V0IGJ5IG5hbWluZyBhbiB1bmtub3duIHR5cGU6IGEgY2FyZC1jb2xvdXJlZCBiYWNrZ3JvdW5kLCBhIDZweAogICBsZWZ0IHJ1bGUsIGEgY2hldnJvbiBidWlsdCBvdXQgb2YgdHdvIHJvdGF0ZWQgYm9yZGVycyBvbiBgc3VtbWFyeTo6YmVmb3JlYCwKICAgYW5kIGEgMXJlbSBwYWQgb24gZXZlcnkgY2hpbGQgdGhhdCBpcyBub3QgdGhlIHN1bW1hcnkuIE9uIHBhcGVyLWNvbG91cmVkCiAgIHBhZ2VzIHRoYXQgY2FyZCByZWFkcyBhcyBhIGdyZXkgc2xhYiBwYXJrZWQgYmVoaW5kIHRoZSBhbnN3ZXIuIEFsbCBmb3VyIGFyZQogICB1bmRvbmUgaGVyZSDigJQgdGhpcyBmb2xkIGlzIGRyYXduIGZyb20gc2NyYXRjaCwgbm90IHRoZW1lZC4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgewogIG1hcmdpbjogMS4yZW0gMDsKICBiYWNrZ3JvdW5kOiBub25lOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwp9Ci8qIFRoZSAxcmVtIHBhZCBtYXJpbW8gcHV0cyBvbiB0aGUgcXVvdGUuIFRoZSBxdW90ZSBoYXMgaXRzIG93bi4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gKjpub3Qoc3VtbWFyeSksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+ICo6bm90KHN1bW1hcnkpIHsgcGFkZGluZzogMDsgfQoKLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSB7CiAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgYWxpZ24taXRlbXM6IGJhc2VsaW5lOwogIGdhcDogMC40NWVtOwogIHdpZHRoOiBmaXQtY29udGVudDsKICBjdXJzb3I6IHBvaW50ZXI7CiAgcGFkZGluZzogMnB4IDEycHggNHB4OwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXNpemU6IDE0cHg7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGJhY2tncm91bmQ6IHRyYW5zcGFyZW50OwogIGJvcmRlcjogMS41cHggZGFzaGVkIHZhcigtLWxoLXJ1bGUpOwogIGJvcmRlci1yYWRpdXM6IHZhcigtLWxoLXdvYmJsZS0yKTsKICAvKiBCb3RoIHNwZWxsaW5nczogU2FmYXJpIHN0aWxsIHNoaXBzIHRoZSBwc2V1ZG8tZWxlbWVudCwgZXZlcnlvbmUgZWxzZQogICAgIGhvbm91cnMgbGlzdC1zdHlsZS4gTGVmdCBpbiwgdGhlIGRlZmF1bHQgdHJpYW5nbGUgc2l0cyBvdXRzaWRlIHRoZSB0YWIuICovCiAgbGlzdC1zdHlsZTogbm9uZTsKICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lOwogIHVzZXItc2VsZWN0OiBub25lOwogIHRyYW5zaXRpb246IGNvbG9yIDAuMTJzIGVhc2UsIGJvcmRlci1jb2xvciAwLjEycyBlYXNlOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIgeyBkaXNwbGF5OiBub25lOyB9CgovKiBPdXJzLiBtYXJpbW8ncyBjaGV2cm9uIGlzIHR3byByb3RhdGVkIGJvcmRlcnMgd2l0aCBwYWRkaW5nIGFuZCBhIG1hcmdpbiwKICAgc28gZXZlcnkgb25lIG9mIHRob3NlIHByb3BlcnRpZXMgaGFzIHRvIGJlIG5hbWVkIHRvIGJlIHN3aXRjaGVkIG9mZiDigJQKICAgbGVmdCBpbiwgaXRzIDQ1ZGVnIGJveCBsYW5kcyBvbiB0b3Agb2YgdGhpcyBhcnJvdy4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeTo6YmVmb3JlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OjpiZWZvcmUgewogIGNvbnRlbnQ6ICLilrgiOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwogIG1hcmdpbjogMDsKICB0cmFuc2Zvcm06IG5vbmU7CiAgdHJhbnNpdGlvbjogbm9uZTsKICB2ZXJ0aWNhbC1hbGlnbjogYmFzZWxpbmU7CiAgZm9udC1zaXplOiAxMXB4OwogIGxpbmUtaGVpZ2h0OiAxOwogIGNvbG9yOiB2YXIoLS1saC1ibHVlLTIpOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnk6OmJlZm9yZSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyW29wZW5dID4gc3VtbWFyeTo6YmVmb3JlIHsKICBjb250ZW50OiAi4pa+IjsKICB0cmFuc2Zvcm06IG5vbmU7Cn0KCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIgewogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtYmx1ZS0yKTsKfQoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OmZvY3VzLXZpc2libGUsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Zm9jdXMtdmlzaWJsZSB7CiAgb3V0bGluZTogMnB4IHNvbGlkIHZhcigtLWxoLWJsdWUpOwogIG91dGxpbmUtb2Zmc2V0OiAycHg7Cn0KCi8qIE9wZW46IHRoZSB0YWIgaGFuZHMgb3ZlciB0byB0aGUgcXVvdGUsIHNvIGl0IHN0b3BzIGRyYXdpbmcgYSBib3JkZXIuICovCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnkgewogIGJvcmRlci1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgcGFkZGluZy1sZWZ0OiAwOwogIHBhZGRpbmctcmlnaHQ6IDA7Cn0KCi8qIEluc2lkZSB0aGUgZm9sZCwgYW5kIE9OTFkgaW5zaWRlIGl0LCB0aGUgcXVvdGUgaXMgaGFuZHdyaXRpbmcuIFRoYXQgaXMKICAgd2hhdCB0ZWxscyBhIHJlYWRlciBhdCBhIGdsYW5jZSB3aGljaCB3b3JkcyBhcmUgdGhlIG5vdGUncyBhbmQgd2hpY2ggYXJlCiAgIHRoZWlycyDigJQgdGhlIGdyZXkgYWxvbmUgbGVmdCB0aGUgdHdvIGxvb2tpbmcgbGlrZSBvbmUgdm9pY2UuCiAgIFNjb3BlZCB0byB0aGUgZm9sZCBvbiBwdXJwb3NlOiBjcDcgcXVvdGVzIGFuIEFJJ3MgYW5hbHlzaXMgaW4gYQogICBibG9ja3F1b3RlIHRvbywgYW5kIHRoYXQgb25lIGlzIGVtcGhhdGljYWxseSBub3Qgd3JpdHRlbiBieSBoYW5kLiAqLwoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlIHsKICBtYXJnaW4tdG9wOiAwLjNlbTsKICBmb250LWZhbWlseTogdmFyKC0tbGgtaGFuZCk7CiAgLyogVGhlc2UgZmFjZXMgcnVuIHNtYWxsIGZvciB0aGVpciBwb2ludCBzaXplIOKAlCBTZWdvZSBQcmludCBlc3BlY2lhbGx5LiAqLwogIGZvbnQtc2l6ZTogMS4wNmVtOwogIGxpbmUtaGVpZ2h0OiAxLjU7Cn0KCi5tYXJrZG93biBociwgLnByb3NlIGhyIHsKICBib3JkZXI6IDA7CiAgaGVpZ2h0OiA3cHg7CiAgbWFyZ2luOiAyZW0gMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UtZmFpbnQpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGNlbnRlcjsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoKLm1hcmtkb3duIGNvZGU6bm90KHByZSBjb2RlKSwKLnByb3NlIGNvZGU6bm90KHByZSBjb2RlKSB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMC44NmVtOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHBhZGRpbmc6IDAuMWVtIDAuNGVtOwogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB0YWJsZXMgLS0tLS0tLS0tLSAqLwoKLm1hcmtkb3duIHRhYmxlLCAucHJvc2UgdGFibGUgeyBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOyBmb250LXNpemU6IDE2cHg7IH0KLm1hcmtkb3duIHRoLCAucHJvc2UgdGggewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXdlaWdodDogNzAwOwogIGZvbnQtc2l6ZTogMTRweDsKICBsZXR0ZXItc3BhY2luZzogMC4wMmVtOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHRleHQtYWxpZ246IGxlZnQ7CiAgYm9yZGVyLWJvdHRvbTogMDsKICBwYWRkaW5nOiA2cHggMTRweCA4cHggMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGJvdHRvbTsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoubWFya2Rvd24gdGQsIC5wcm9zZSB0ZCB7CiAgcGFkZGluZzogOHB4IDE0cHggOHB4IDA7CiAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkIHZhcigtLWxoLXJ1bGUpOwogIC8qIE51bWJlcnMgc3RheSBtZWNoYW5pY2FsOiBhIGNvbHVtbiB0aGF0IGRvZXMgbm90IGxpbmUgdXAgaXMgYSBjb2x1bW4gdGhhdAogICAgIGNhbm5vdCBiZSBjb21wYXJlZCwgd2hpY2ggaXMgdGhlIHdob2xlIHJlYXNvbiB0aGUgdGFibGUgaXMgdGhlcmUuICovCiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMTVweDsKICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zOwp9CgovKiAtLS0tLS0tLS0tIGNlbGxzIC0tLS0tLS0tLS0gKi8KCi5jZWxsLApbZGF0YS10ZXN0aWQ9ImNlbGwiXSB7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQouY2VsbDpudGgtb2YtdHlwZShldmVuKSwKW2RhdGEtdGVzdGlkPSJjZWxsIl06bnRoLW9mLXR5cGUoZXZlbikgeyBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7IH0KCi5jZWxsOmZvY3VzLXdpdGhpbiwKW2RhdGEtdGVzdGlkPSJjZWxsIl06Zm9jdXMtd2l0aGluIHsKICBib3gtc2hhZG93OiAwIDAgMCAycHggdmFyKC0tbGgtcnVsZSksIHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLmNlbGwtZWRpdG9yLAouY20tZWRpdG9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxMy41cHg7CiAgbGluZS1oZWlnaHQ6IDEuNTU7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7Cn0KCi5jbS1lZGl0b3IgLmNtLWd1dHRlcnMgewogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7CiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tbGgtcnVsZSk7Cn0KCi5jbS1lZGl0b3IuY20tZm9jdXNlZCB7IG91dGxpbmU6IDJweCBzb2xpZCB2YXIoLS1saC1ibHVlKTsgfQouY20tZWRpdG9yIC5jbS1jdXJzb3IgeyBib3JkZXItbGVmdC1jb2xvcjogdmFyKC0tbGgtcnVzdCk7IH0KLmNtLWVkaXRvciAuY20tc2VsZWN0aW9uQmFja2dyb3VuZCwKLmNtLWVkaXRvci5jbS1mb2N1c2VkIC5jbS1zZWxlY3Rpb25CYWNrZ3JvdW5kIHsgYmFja2dyb3VuZDogI0RDRTNFRCAhaW1wb3J0YW50OyB9Ci5jbS1lZGl0b3IgLmNtLWFjdGl2ZUxpbmUgeyBiYWNrZ3JvdW5kOiByZ2JhKDMxLCA1OCwgOTUsIDAuMDQ1KTsgfQoKLyogc3ludGF4ICovCi5jbS1lZGl0b3IgLnRvay1rZXl3b3JkLAouY20tZWRpdG9yIC5jbS1rZXl3b3JkIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyBmb250LXdlaWdodDogNTAwOyB9Ci5jbS1lZGl0b3IgLnRvay1udW1iZXIsCi5jbS1lZGl0b3IgLmNtLW51bWJlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgfQouY20tZWRpdG9yIC50b2stc3RyaW5nLAouY20tZWRpdG9yIC5jbS1zdHJpbmcgeyBjb2xvcjogIzRCNkEzQTsgfQouY20tZWRpdG9yIC50b2stY29tbWVudCwKLmNtLWVkaXRvciAuY20tY29tbWVudCB7IGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7IGZvbnQtc3R5bGU6IGl0YWxpYzsgfQouY20tZWRpdG9yIC50b2stdmFyaWFibGVOYW1lLAouY20tZWRpdG9yIC50b2stcHJvcGVydHlOYW1lIHsgY29sb3I6IHZhcigtLWxoLWluayk7IH0KLmNtLWVkaXRvciAudG9rLW9wZXJhdG9yIHsgY29sb3I6IHZhcigtLWxoLWluay0yKTsgfQoKLyogLS0tLS0tLS0tLSBvdXRwdXQgLS0tLS0tLS0tLSAqLwoKLm91dHB1dC1hcmVhLAoubWFyaW1vLW91dHB1dCB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7Cn0KCi5vdXRwdXQtYXJlYSBwcmUsCnByZS5vdXRwdXQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1tb25vKTsKICBmb250LXNpemU6IDEzcHg7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7CiAgcGFkZGluZzogMTBweCAxMnB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwp9CgovKiBBIGZpZ3VyZSBpcyBhIGRyYXdpbmcgdGFwZWQgb250byB0aGUgcGFnZS4gKi8KLm91dHB1dC1hcmVhIGltZywKLm1hcmltby1vdXRwdXQgaW1nLAoub3V0cHV0LWFyZWEgc3ZnLAoubWFyaW1vLW91dHB1dCBzdmcgewogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB1aSBjaHJvbWUgLS0tLS0tLS0tLSAqLwoKYnV0dG9uLAoubWFyaW1vLWJ1dHRvbiB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQoKLyogQW55dGhpbmcgdGhlIHN0dWRlbnQgYWN0dWFsbHkgcHJlc3NlcyDigJQg4pa2IFJ1biwg8J+TqCBTZW5kIHRvIG15IHR1dG9yLCB0aGUKICAgcmVmZXJlZSdzIGFwcGVhbCDigJQgaXMgZHJhd24sIGFuZCBtb3ZlcyB1bmRlciB0aGUgcHJlc3MuICovCi5tYXJpbW8tcnVuLWJ1dHRvbiwKLm1hcmltby1idXR0b24sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXSwKYnV0dG9uW2RhdGEtdmFyaWFudD0ic2Vjb25kYXJ5Il0sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4pOwogIHRyYW5zaXRpb246IHRyYW5zZm9ybSAwLjA2cyBlYXNlLCBib3gtc2hhZG93IDAuMDZzIGVhc2U7Cn0KLm1hcmltby1ydW4tYnV0dG9uOmFjdGl2ZSwKLm1hcmltby1idXR0b246YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJwcmltYXJ5Il06YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJzZWNvbmRhcnkiXTphY3RpdmUsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXTphY3RpdmUgewogIHRyYW5zZm9ybTogdHJhbnNsYXRlKDJweCwgMi41cHgpOwogIGJveC1zaGFkb3c6IG5vbmU7Cn0KCi5tYXJpbW8tcnVuLWJ1dHRvbiwKYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdIHsKICBiYWNrZ3JvdW5kOiB2YXIoLS1saC1ibHVlKTsKICBjb2xvcjogdmFyKC0tbGgtcGFwZXIpOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtaW5rKTsKfQoubWFyaW1vLXJ1bi1idXR0b246aG92ZXIsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXTpob3ZlciB7IGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUtMik7IH0KCi8qIFNsaWRlcnM6IGEgcGVuY2lsIGxpbmUgd2l0aCBhIGJlYWQgb24gaXQuIFNlbGVjdG9ycyBjb3ZlciBtYXJpbW8ncyBvd24KICAgd2lkZ2V0IGFuZCBhIHBsYWluIHJhbmdlIGlucHV0LCB3aGljaGV2ZXIgdGhlIGJ1aWxkIHJlbmRlcnMuICovCmlucHV0W3R5cGU9InJhbmdlIl0gewogIGFjY2VudC1jb2xvcjogdmFyKC0tbGgtYmx1ZSk7CiAgaGVpZ2h0OiAyMnB4Owp9Cltyb2xlPSJzbGlkZXIiXSwKW2RhdGEtb3JpZW50YXRpb249Imhvcml6b250YWwiXSBbcm9sZT0ic2xpZGVyIl0gewogIGJvcmRlcjogMnB4IHNvbGlkIHZhcigtLWxoLWluayk7CiAgYm9yZGVyLXJhZGl1czogNTglIDQyJSA1MCUgNTAlIC8gNTAlIDUwJSA0MiUgNTglOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIGJveC1zaGFkb3c6IHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLyogVGV4dCB0aGUgc3R1ZGVudCB0eXBlcyBpbnRvOiBhIHJ1bGVkIGJveCwgbm90IGEgY2hyb21lIGZpZWxkLiAqLwppbnB1dFt0eXBlPSJ0ZXh0Il0sCmlucHV0W3R5cGU9Im51bWJlciJdLAp0ZXh0YXJlYSwKLm1hcmltby10ZXh0LWlucHV0IHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtY2FyZCk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7CiAgYm94LXNoYWRvdzogdmFyKC0tbGgtcGVuLXNvZnQpOwp9CgovKiBUaGUgcGhvdG8gZHJvcCBib3gg4oCUIHRoZSBvbmUgcGxhY2Ugb24gdGhlIHBhZ2UgdGhhdCBhc2tzIGZvciBwYXBlci4gKi8KW2RhdGEtdGVzdGlkPSJmaWxlLXVwbG9hZCJdLAoubWFyaW1vLWZpbGUtdXBsb2FkLAouZHJvcHpvbmUgewogIGJvcmRlcjogMi41cHggZGFzaGVkIHZhcigtLWxoLWluaykgIWltcG9ydGFudDsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUpOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWNhcmQpOwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKfQoKLyogc3RhbGUgLyBlcnJvciBzdGF0ZXMgKi8KLmNlbGwuc3RhbGUsCltkYXRhLXN0YWxlPSJ0cnVlIl0geyBib3gtc2hhZG93OiBpbnNldCAzcHggMCAwIHZhcigtLWxoLXJ1c3QpOyB9CgoubWFyaW1vLWVycm9yLAoub3V0cHV0LWFyZWEgLmVycm9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxM3B4OwogIGJhY2tncm91bmQ6ICNGQkVERTc7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVzdCk7CiAgY29sb3I6ICM2RTJGMTQ7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBwYWRkaW5nOiAxMHB4IDEycHg7Cn0KCi8qIHNsaWRlcyAvIGFwcCB2aWV3ICovCi5zbGlkZXMsCltkYXRhLW1vZGU9InByZXNlbnQiXSAubWFya2Rvd24geyBmb250LXNpemU6IDE4cHg7IH0KCi8qIEEgc3R1ZGVudCB3aG8gaGFzIGFza2VkIGZvciBsZXNzIG1vdGlvbiBnZXRzIHRoZSBkcmF3aW5nIHdpdGhvdXQgdGhlCiAgIGJ1dHRvbiB0aGF0IG1vdmVzIHVuZGVyIHRoZSBwcmVzcy4gKi8KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOiByZWR1Y2UpIHsKICAubWFyaW1vLXJ1bi1idXR0b24sCiAgLm1hcmltby1idXR0b24sCiAgYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9InNlY29uZGFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7IHRyYW5zaXRpb246IG5vbmU7IH0KfQo="  # BUILT
    LECTURE_HALL_CSS = base64.b64decode(LECTURE_HALL_CSS_B64).decode("utf-8")

    # pd.DataFrame(sentences) has columns 0, 1, 2, ...; marimo warns about that.
    warnings.filterwarnings("ignore", message="DataFrame has integer column names")

    # marimo's fold toggle sits left of a heading cell and shows only on hover.
    # Show it always, larger, and mark a folded section clearly.
    FOLD_CSS = r"""
    div.absolute.top-5.\-left-7 { left: -2.7rem !important; top: 1.1rem !important; }
    div.absolute.top-5.\-left-7 > button {
      width: 32px !important; height: 32px !important; border-radius: 50% !important;
      opacity: 1 !important; color: #B14434 !important; background: #FFFDF7 !important;
      border: 1.5px solid #B14434 !important;
    }
    .marimo-cell:has(.output-area h2) div.absolute.top-5.\-left-7 { top: 4.2rem !important; }
    div.absolute.top-5.\-left-7 > button:hover { color: #FFFDF7 !important; background: #B14434 !important; }
    div.absolute.top-5.\-left-7 > button svg { width: 20px; height: 20px; opacity: 1 !important; stroke-width: 2.4; }
    div.h-9.bg-muted.rounded-b.cursor-pointer {
      height: 48px !important; opacity: 1 !important; margin-top: 4px;
      background: #F6F2E9 !important; border: 1.5px dashed #B14434; border-radius: 10px !important;
    }
    div.h-9.bg-muted.rounded-b.cursor-pointer:hover { background: #F3E4DC !important; }
    div.h-9.bg-muted.rounded-b.cursor-pointer span, div.h-9.bg-muted.rounded-b.cursor-pointer svg {
      color: #B14434 !important; font-size: 16px !important; font-weight: 600;
    }
    div.h-9.bg-muted.rounded-b.cursor-pointer span::before { content: "Click to open · "; }
    """

    INK = "#1D1E21"
    RULE = "#D9D2C2"
    PAPER = "#FFFDF7"
    SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"

    @contextlib.contextmanager
    def quiet():
        """Keep stderr off the page: see the note at the top of the file."""
        with contextlib.redirect_stderr(io.StringIO()):
            yield

    # ---- the picture ---------------------------------------------------------

    def pca_2d(X):
        """The two directions along which the rows of X spread the most."""
        X = np.asarray(X, dtype=float)
        X = X - X.mean(axis=0)
        _, _, Vt = np.linalg.svd(X, full_matrices=False)
        # Sums, not @: numpy 2 on macOS warns about matmul on finite input.
        return (X[:, None, :] * Vt[None, :2, :]).sum(axis=2)

    def _rgb(h):
        return np.array([int(h[i : i + 2], 16) for i in (1, 3, 5)]) / 255

    MID, LEFT, RIGHT = _rgb("#D6D1C7"), _rgb("#3959A6"), _rgb("#B14434")
    TOP, BOTTOM = _rgb(INK), _rgb("#FFFFFF")

    def colours(xy):
        """Left to right: blue, grey, red. Top to bottom: dark, grey, light."""
        out = []
        q = np.quantile(np.abs(xy), 0.9, axis=0)
        for x, y in np.clip(xy / q, -1, 1):
            c = MID + abs(x) * ((LEFT if x < 0 else RIGHT) - MID)
            c = c + 0.55 * abs(y) * ((TOP if y > 0 else BOTTOM) - c)
            out.append("#" + "".join(f"{round(255 * v):02x}" for v in c))
        return out

    def network_layout(edges, n):
        random.seed(3)  # igraph draws its random numbers from Python's random
        g = igraph.Graph(n=n, edges=edges[["src", "trg"]].to_numpy().tolist())
        return np.array(g.layout_fruchterman_reingold(niter=1000).coords)

    def draw(vectors, edges):
        """The embedding (left) and the network (right), coloured by the
        position of each node in the embedding."""
        names = list(vectors.index)
        emb = pca_2d(vectors.to_numpy())
        net = network_layout(edges, len(names))
        col = colours(emb)
        X = alt.X("x:Q", axis=None, scale=alt.Scale(zero=False, nice=False))
        Y = alt.Y("y:Q", axis=None, scale=alt.Scale(zero=False, nice=False))

        def dots(xy, title, links=False):
            rows = [dict(name=a, x=float(p[0]), y=float(p[1]), c=c) for a, p, c in zip(names, xy, col)]
            layers = []
            if links:
                lines = [
                    dict(x=float(xy[s][0]), y=float(xy[s][1]), x2=float(xy[t][0]), y2=float(xy[t][1]))
                    for s, t in zip(edges["src"], edges["trg"])
                ]
                layers.append(alt.Chart(alt.Data(values=lines)).mark_rule(color=RULE, strokeWidth=1).encode(x=X, y=Y, x2="x2:Q", y2="y2:Q"))
            layers.append(
                alt.Chart(alt.Data(values=rows))
                .mark_circle(size=110, stroke=INK, strokeWidth=0.7, opacity=1)
                .encode(x=X, y=Y, color=alt.Color("c:N", scale=None), tooltip=alt.Tooltip("name:N", title="character"))
            )
            return alt.layer(*layers).properties(width=400, height=360, title=title)

        return (
            alt.hconcat(dots(emb, "embedding (PCA)"), dots(net, "network", links=True), spacing=30)
            .configure(background=PAPER)
            .configure_view(stroke=None)
            .configure_title(fontSize=14, anchor="start", color=INK, font=SANS)
        )

    # ---- start with every section folded -------------------------------------

    class FoldSections(anywidget.AnyWidget):
        """Clicks marimo's fold toggle of every section heading (h2), once per
        page load, after all the headings have drawn."""

        _esm = r"""
        function render({ model, el }) {
          if (window.__labFolded) return;
          window.__labFolded = true;
          const want = model.get("sections");
          const heads = () => [...document.querySelectorAll(".marimo-cell")]
            .filter((c) => c.querySelector(".output-area h2"));
          let tries = 0;
          const timer = setInterval(() => {
            tries += 1;
            if (heads().length < want && tries < 100) return;
            clearInterval(timer);
            let i = 0;
            const next = () => {
              const cell = heads()[i++];
              if (!cell) {
                document.querySelectorAll("#App, main, html").forEach((e) => e.scrollTo(0, 0));
                return;
              }
              const toggle = cell.querySelector("div.absolute.top-5 button");
              if (toggle) toggle.click();
              setTimeout(next, 80);
            };
            next();
          }, 300);
        }
        export default { render };
        """
        sections = traitlets.Int(0).tag(sync=True)


@app.cell(hide_code=True)
def _():
    mo.Html(f"<style>{LECTURE_HALL_CSS}{FOLD_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Lab · Character embeddings
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1 · Data
    """)
    return


@app.cell
def _():
    URL = "https://raw.githubusercontent.com/skojaku/adv-net-sci/main/lecture-note/assets/data/lesmis/"
    edges = pd.read_csv(URL + "edge_table.csv")
    names = pd.read_csv(URL + "node_table.csv")["name"].to_numpy()
    edges
    return edges, names


@app.cell
def _(names):
    names
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2 · Random walks

    At every step, move to a random neighbour.
    """)
    return


@app.cell
def _(edges, names):
    n = len(names)
    A = np.zeros((n, n))
    A[edges["src"], edges["trg"]] = 1
    A[edges["trg"], edges["src"]] = 1
    return A, n


@app.function
def random_walk(A, start, length, rng):
    walk = [start]
    # ✍️ your code here
    return walk


@app.cell
def _(A, n, names):
    rng = np.random.default_rng(0)
    walks = [random_walk(A, i, 40, rng) for i in range(n) for _ in range(20)]
    sentences = [names[w].tolist() for w in walks]
    pd.DataFrame(sentences)
    return (sentences,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3 · word2vec
    """)
    return


@app.cell
def _(names):
    from gensim.models import Word2Vec

    def embed(sentences):
        with quiet():  # hides a harmless message from gensim
            model = Word2Vec(
                sentences, vector_size=32, window=5, negative=5, sg=1,
                min_count=1, sample=0, epochs=20, workers=1, seed=0,
            )
        return pd.DataFrame(model.wv[names], index=names)

    return (embed,)


@app.cell
def _(embed, sentences):
    vectors = embed(sentences)
    vectors
    return (vectors,)


@app.cell(hide_code=True)
def _(edges, vectors):
    draw(vectors, edges)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4 · Random walk with restart

    With probability $\alpha$, go back to the start node; otherwise move to a random neighbour.
    """)
    return


@app.function
def random_walk_with_restart(A, start, length, alpha, rng):
    walk = [start]
    # ✍️ your code here
    return walk


@app.cell
def _(A, n, names):
    alpha = 0.5  # also try 0.05
    rng_restart = np.random.default_rng(0)
    walks_restart = [random_walk_with_restart(A, i, 40, alpha, rng_restart) for i in range(n) for _ in range(20)]
    sentences_restart = [names[w].tolist() for w in walks_restart]
    pd.DataFrame(sentences_restart)
    return (sentences_restart,)


@app.cell
def _(embed, sentences_restart):
    vectors_restart = embed(sentences_restart)
    vectors_restart
    return (vectors_restart,)


@app.cell(hide_code=True)
def _(edges, vectors_restart):
    draw(vectors_restart, edges)
    return


@app.cell(hide_code=True)
def _():
    mo.ui.anywidget(FoldSections(sections=4))
    return


if __name__ == "__main__":
    app.run()
