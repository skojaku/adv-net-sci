# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "altair==5.5.0",
#     "gensim==4.4.0",
#     "networkx==3.4.2",
#     "numpy==2.2.6",
#     "scipy==1.15.3",
# ]
# ///
#
# The Module 8 lab: character embeddings (slides 14 and 15 of
# slides/m08/m08-embedding.md).
#
# Random walks on the Les Miserables co-appearance network, word2vec on the
# walks, the closest characters, and a walk that restarts at its start node
# (personalized PageRank). Three cells are the student's:
#
#   * cosine(x, y)               -- one line
#   * closest(vectors, name, k)  -- score every other character, sort
#   * ppr_walk(G, start, length, alpha, rng) -- the task of slide 15
#
# The walk simulator and the word2vec call are given and shown. Everything
# else is the hidden kit.
#
# Rules this file obeys (lecture-note/LAB_NOTEBOOK_GUIDE.md):
#
#   * The stylesheet travels inside the file (molab ignores css_file). Refresh
#     it with `python tools/build_lab_notebooks.py m08-embedding`, which also
#     writes lab-solutions.py.
#   * Nothing is fetched at run time: the network ships with networkx
#     (nx.les_miserables_graph(), Knuth 1993).
#   * A waiting card, not an exception, for anything downstream of a blank.
#   * Student code runs under a step limit (run_limited), so a walk loop that
#     never ends gives a sentence, not a hung kernel.
#   * The closest characters depend on the platform's floating point, so no
#     sentence names a character. Every number under a figure is computed.
#   * gensim's compiled code now and then prints "Exception ignored in:
#     'gensim.models.word2vec_inner.our_dot_float'" with no exception set
#     (seen with numpy 1.26 and 2.x alike). It is harmless; quiet() keeps it
#     off the page.

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import base64
    import contextlib
    import html
    import io
    import random
    import sys

    import altair as alt
    import marimo as mo
    import networkx as nx
    import numpy as np

    # The look travels inside the notebook rather than beside it. molab ignores
    # a notebook's css_file setting (marimo-team/marimo#8467), so
    # lecture-hall.css is carried here as base64 and injected by the first
    # cell. Refresh it with tools/build_lab_notebooks.py.
    LECTURE_HALL_CSS_B64 = "LyogTGVjdHVyZSBIYWxsIOKAlCBtYXJpbW8gY3VzdG9tIENTUywgZHJhd24gYnkgaGFuZAogICBVc2FnZTogcHV0IHRoaXMgbmV4dCB0byB5b3VyIG5vdGVib29rIGFuZCBhZGQgdG8gdGhlIG5vdGVib29rJ3MgY29uZmlnOgogICAgIFtkaXNwbGF5XSBjc3NfZmlsZSA9ICJsZWN0dXJlLWhhbGwuY3NzIgogICBvciBpbiBtYXJpbW8udG9tbCB1bmRlciBbZGlzcGxheV0uCgogICBUaGUgbm90ZWJvb2sgaXMgYSBsZWN0dXJlIG5vdGUgdGhlIHN0dWRlbnQgYW5kIHRoZSB0dXRvciBmaWxsIGluIHRvZ2V0aGVyLAogICBzbyBpdCBpcyBkcmVzc2VkIGFzIG9uZTogZG90LWdyaWQgcGFwZXIsIHdvYmJseSBpbmsgYm9yZGVycywgYW5kIHNlY3Rpb24KICAgcnVsZXMgZHJhd24gd2l0aCBhIHBlbi4KCiAgIFRIRSBIQU5EIElTIElOIFRIRSBMSU5FUywgTk9UIElOIFRIRSBMRVRURVJTLiBBIGhhbmR3cml0aW5nIGZhY2UgZm9yIHRoZQogICBwcm9zZSB3YXMgdGlyaW5nIHRvIHJlYWQgb3ZlciBuaW5ldHkgbWludXRlcyBhbmQgbWFkZSB0aGUgcGFnZSBsb29rIGxpa2UgYQogICBncmVldGluZyBjYXJkIHJhdGhlciB0aGFuIGEgbGVjdHVyZSBub3RlLiBTbyB0aGUgdHlwZSBpcyBleGFjdGx5IHRoZSBjb3Vyc2UKICAgbGVjdHVyZSBub3RlJ3MgKGFkdi1uZXQtc2NpL2xlY3R1cmUtbm90ZS9zY3NzL21pbmltYWwuc2Nzcyk6IGEgc3lzdGVtIHNhbnMKICAgZm9yIHRoZSBib2R5LCBhIHN5c3RlbSBzZXJpZiBmb3IgdGhlIGhlYWRpbmdzLCAxOHB4LzEuNjUg4oCUIHRoZSBzYW1lCiAgIHJlYWRpbmcgZXhwZXJpZW5jZSBvbiBib3RoIGhhbHZlcyBvZiB0aGUgY291cnNlLiBXaGF0IHN0YXlzIGhhbmQtZHJhd24gaXMKICAgZXZlcnl0aGluZyB0aGF0IGlzIG5vdCByZWFkIGFzIGEgd29yZDogdGhlIHdhdnkgc2VjdGlvbiBydWxlcywgdGhlIHdvYmJseQogICBib3JkZXJzIGFuZCBwZW4gc2hhZG93cywgdGhlIHNrZXRjaGVkIG1hdHBsb3RsaWIgc3Ryb2tlcywgYW5kIG5ldHZpeidzCiAgIHR1cmJ1bGVudCBlZGdlcy4KCiAgIE5vIHdlYmZvbnQsIG5vIG5ldHdvcmsgcmVxdWVzdDogYSBzdHVkZW50IG9uIGEgcGxhbmUgZ2V0cyB0aGUgc2FtZSBwYWdlLAogICBhbmQgdGhlcmUgaXMgbm8gZmlyc3QtcGFpbnQgZmxhc2ggb2YgYSBmYWxsYmFjayBmYWNlLgoKICAgVGhlIGFjY2VudHMgYXJlIHRoZSBMRUNUVVJFIFNMSURFUycgYWNjZW50cywgdmVyYmF0aW0g4oCUIHRoZSBtb2R1bGUgaXMgb25lCiAgIGNvdXJzZSwgc28gdGhlIGNvbG91ciB0aGF0IG1lYW5zICJ0aGUgdGhpbmcgd2UgYXJlIGxvb2tpbmcgYXQiIGhhcyB0byBtZWFuCiAgIGl0IGluIGJvdGggaGFsdmVzLiBDaGFuZ2Ugb25lIG9mIHRoZW0gaGVyZSBhbmQgeW91IG11c3QgY2hhbmdlIGl0IGluCiAgIGFkdi1uZXQtc2NpL3NsaWRlcy9tMDIvZmlndXJlcy9tYWtlX2ZpZ3VyZXMucHkgdG9vLCBhbmQgaW4gZXZlcnkgY2VsbHMvKi5weQogICB0aGF0IGhhcmRjb2RlcyBpdCAodGhleSBhbGwgZG8sIGZvciB0aGVpciBub2RlcyBhbmQgZWRnZXMpLiAqLwoKOnJvb3QgewogIC8qIHBhbGV0dGUg4oCUIHRoZSB0aHJlZSBhY2NlbnRzIGNvbWUgZnJvbSB0aGUgc2xpZGUgZGVjawogICAgIChtYWtlX2ZpZ3VyZXMucHk6IEFDQ0VOVCAvIEFDQ0VOVDIgLyBBQ0NFTlQzKSwgYW5kIHRoZSBwcmVtYWRlIGNlbGxzCiAgICAgaGFyZGNvZGUgdGhlIHNhbWUgaGV4ZXMgZm9yIHRoZWlyIG5vZGVzIGFuZCBlZGdlcywgc28gYSByZXBhaW50IGhlcmUKICAgICBkZXN5bmNzIGJvdGguIFdoYXQgaXMgTk9UIHRoZSBzbGlkZXMnIGlzIHRoZSBwYXBlcjogd2hpdGUgYmVjYW1lIHdhcm0sCiAgICAgYW5kIHRoZSBwZW5jaWwgcnVsZSAoLS1saC1ydWxlKSBpcyBhIG5ldyB0b2tlbiByYXRoZXIgdGhhbiBhIHJlcGFpbnQgb2YKICAgICAtLWxoLWxpbmUsIHdoaWNoIGlzIGEgbm9kZSBmaWxsIGluIGNwMiBhbmQgY3A1LiAqLwogIC0tbGgtcGFwZXI6ICAgI0ZGRkRGNzsKICAtLWxoLWNhcmQ6ICAgICNGRkZGRkY7CiAgLS1saC1zdXJmYWNlOiAjRjZGMkU5OwogIC0tbGgtbGluZTogICAgI0U0RTZFQTsKICAtLWxoLXJ1bGU6ICAgICNEOUQyQzI7CiAgLS1saC1pbms6ICAgICAjMUQxRTIxOwogIC0tbGgtaW5rLTI6ICAgIzM1MzczQzsKICAtLWxoLW11dGVkOiAgICM2QTZENzU7CiAgLS1saC1ibHVlOiAgICAjMjIzMzZCOwogIC0tbGgtYmx1ZS0yOiAgIzM5NTlBNjsKICAtLWxoLXJ1c3Q6ICAgICNCMTQ0MzQ7CgogIC8qIHR5cGUg4oCUIHRoZSBsZWN0dXJlIG5vdGUncyB0aHJlZSBzdGFja3MsIHZlcmJhdGltLiBBbGwgZnJvbSB0aGUgc3lzdGVtOgogICAgIG5vdGhpbmcgaGVyZSBpcyBmZXRjaGVkLiAqLwogIC0tbGgtc2VyaWY6ICAgIklvd2FuIE9sZCBTdHlsZSIsICJQYWxhdGlubyBMaW5vdHlwZSIsIFBhbGF0aW5vLAogICAgICAgICAgICAgICAgIkJvb2sgQW50aXF1YSIsICJIb2VmbGVyIFRleHQiLCBHZW9yZ2lhLAogICAgICAgICAgICAgICAgIlRpbWVzIE5ldyBSb21hbiIsIHNlcmlmOwogIC0tbGgtc2FuczogICAgc3lzdGVtLXVpLCAtYXBwbGUtc3lzdGVtLCAiU2Vnb2UgVUkiLCBSb2JvdG8sCiAgICAgICAgICAgICAgICAiSGVsdmV0aWNhIE5ldWUiLCAiTm90byBTYW5zIiwgIkxpYmVyYXRpb24gU2FucyIsIEFyaWFsLAogICAgICAgICAgICAgICAgc2Fucy1zZXJpZjsKICAtLWxoLW1vbm86ICAgIHVpLW1vbm9zcGFjZSwgU0ZNb25vLVJlZ3VsYXIsICJTRiBNb25vIiwgTWVubG8sIENvbnNvbGFzLAogICAgICAgICAgICAgICAgIkxpYmVyYXRpb24gTW9ubyIsIG1vbm9zcGFjZTsKICAvKiBUaGUgb25lIGhhbmQtd3JpdHRlbiBmYWNlIG9uIHRoZSBwYWdlLCBhbmQgaXQgd3JpdGVzIGV4YWN0bHkgb25lIHRoaW5nOgogICAgIHRoZSBzdHVkZW50J3Mgb3duIGFuc3dlcnMsIGluc2lkZSB0aGUgZm9sZC4gUHJpbnRlZCBub3RlLCBoYW5kd3JpdHRlbgogICAgIG1hcmdpbiDigJQgdGhlIGRpZmZlcmVuY2UgYmV0d2VlbiB0aGUgdHdvIGlzIHRoZSBwb2ludC4gU3lzdGVtIGZhY2VzIG9ubHksCiAgICAgbGlrZSBldmVyeXRoaW5nIGVsc2UgaGVyZTogbWFjT1Mgc2hpcHMgdGhlIGZpcnN0IHR3bywgV2luZG93cyB0aGUgbmV4dAogICAgIHR3bywgYGN1cnNpdmVgIGNhdGNoZXMgdGhlIHJlc3QuICovCiAgLS1saC1oYW5kOiAgICAiQ2hhbGtib2FyZCBTRSIsICJCcmFkbGV5IEhhbmQiLCAiU2Vnb2UgUHJpbnQiLAogICAgICAgICAgICAgICAgIkNvbWljIFNhbnMgTVMiLCBjdXJzaXZlOwoKICAvKiB0aGUgaGFuZC1kcmF3biBraXQ6IHR3byByb3VuZGluZyBzZXRzLCBhbHRlcm5hdGVkIHNvIG5vIHR3byBib3hlcyBvbiB0aGUKICAgICBwYWdlIGhhdmUgdGhlIHNhbWUgY29ybmVycywgYW5kIG9uZSBpbmsgc2hhZG93IHRoYXQgZmFrZXMgYSBzZWNvbmQgcGFzcwogICAgIG9mIHRoZSBwZW4uICovCiAgLS1saC13b2JibGU6ICAgMTRweCA2cHggMTZweCA4cHggLyA4cHggMTZweCA2cHggMTRweDsKICAtLWxoLXdvYmJsZS0yOiA2cHggMTZweCA4cHggMTRweCAvIDE2cHggNnB4IDE0cHggOHB4OwogIC0tbGgtcGVuOiAgICAgIDNweCA0cHggMCAtMXB4IHJnYmEoMzUsIDM0LCA0MywgMC4xNik7CiAgLS1saC1wZW4tc29mdDogMnB4IDNweCAwIC0xcHggcmdiYSgzNSwgMzQsIDQzLCAwLjEyKTsKCiAgLyogYSB3YXZ5IHN0cm9rZSwgdXNlZCBmb3IgdW5kZXJsaW5lcyBhbmQgdGFibGUgcnVsZXMgKi8KICAtLWxoLXN0cm9rZTogdXJsKCJkYXRhOmltYWdlL3N2Zyt4bWwsJTNDc3ZnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Zycgd2lkdGg9JzEyMCcgaGVpZ2h0PSc3JyB2aWV3Qm94PScwIDAgMTIwIDcnJTNFJTNDcGF0aCBkPSdNMSA0LjRDMjAgMS45IDQwIDYuMiA2MCAzLjcgODAgMS40IDEwMCA1LjYgMTE5IDMuMicgZmlsbD0nbm9uZScgc3Ryb2tlPSclMjNCMTQ0MzQnIHN0cm9rZS13aWR0aD0nMicgc3Ryb2tlLWxpbmVjYXA9J3JvdW5kJy8lM0UlM0Mvc3ZnJTNFIik7CiAgLS1saC1zdHJva2UtZmFpbnQ6IHVybCgiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMjAnIGhlaWdodD0nNycgdmlld0JveD0nMCAwIDEyMCA3JyUzRSUzQ3BhdGggZD0nTTEgNC40QzIwIDEuOSA0MCA2LjIgNjAgMy43IDgwIDEuNCAxMDAgNS42IDExOSAzLjInIGZpbGw9J25vbmUnIHN0cm9rZT0nJTIzRDlEMkMyJyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcvJTNFJTNDL3N2ZyUzRSIpOwoKICAvKiBtYXJpbW8gdG9rZW5zICovCiAgLS1iYWNrZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1pbmspOwogIC0tY2FyZDogdmFyKC0tbGgtY2FyZCk7CiAgLS1jYXJkLWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1wb3BvdmVyOiB2YXIoLS1saC1jYXJkKTsKICAtLXBvcG92ZXItZm9yZWdyb3VuZDogdmFyKC0tbGgtaW5rKTsKICAtLW11dGVkOiB2YXIoLS1saC1zdXJmYWNlKTsKICAtLW11dGVkLWZvcmVncm91bmQ6IHZhcigtLWxoLW11dGVkKTsKICAtLWJvcmRlcjogdmFyKC0tbGgtbGluZSk7CiAgLS1pbnB1dDogdmFyKC0tbGgtbGluZSk7CiAgLS1yaW5nOiB2YXIoLS1saC1ibHVlKTsKICAtLXByaW1hcnk6IHZhcigtLWxoLWJsdWUpOwogIC0tcHJpbWFyeS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1zZWNvbmRhcnk6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tc2Vjb25kYXJ5LWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1hY2NlbnQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tYWNjZW50LWZvcmVncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIC0tZGVzdHJ1Y3RpdmU6IHZhcigtLWxoLXJ1c3QpOwogIC0tZGVzdHJ1Y3RpdmUtZm9yZWdyb3VuZDogdmFyKC0tbGgtcGFwZXIpOwogIC0tcmFkaXVzOiAzcHg7CgogIC0tdGV4dC1mb250OiB2YXIoLS1saC1zYW5zKTsKICAtLWhlYWRpbmctZm9udDogdmFyKC0tbGgtc2VyaWYpOwogIC0tY29kZS1mb250OiB2YXIoLS1saC1tb25vKTsKfQoKLyogLS0tLS0tLS0tLSBwYWdlIC0tLS0tLS0tLS0gKi8KCi8qIERvdC1ncmlkLCBub3QgcnVsZWQgbGluZXM6IHRoZSBzYW1lICJ0aGlzIGlzIGEgc2tldGNoYm9vayIgc2lnbmFsLCBidXQgaXQKICAgZG9lcyBub3QgZmlnaHQgYSBsaW5lIG9mIHByb3NlIGZvciB0aGUgc2FtZSBob3Jpem9udGFsIGJhbmQuICovCmJvZHksCiNBcHAgewogIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWxoLXBhcGVyKTsKICBiYWNrZ3JvdW5kLWltYWdlOiByYWRpYWwtZ3JhZGllbnQocmdiYSgzMSwgNTgsIDk1LCAwLjA4NSkgMXB4LCB0cmFuc3BhcmVudCAxcHgpOwogIGJhY2tncm91bmQtc2l6ZTogMjRweCAyNHB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIC13ZWJraXQtZm9udC1zbW9vdGhpbmc6IGFudGlhbGlhc2VkOwp9CgovKiAtLS0tLS0tLS0tIHByb3NlIC0tLS0tLS0tLS0gKi8KCi5tYXJrZG93biwKLnByb3NlIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgZm9udC1zaXplOiAxOHB4OwogIGxpbmUtaGVpZ2h0OiAxLjY1OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgdGV4dC13cmFwOiBwcmV0dHk7CiAgbWF4LXdpZHRoOiA2OGNoOwp9CgovKiBUaGUgbGVjdHVyZSBub3RlJ3Mgc2VyaWYgYW5kIGl0cyBzY2FsZSDigJQgaDEgMi4wNSAvIGgyIDEuNTUgLyBoMyAxLjIyIC8KICAgaDQgMS4wMiBhZ2FpbnN0IGl0cyAxOHB4IHJvb3QuIFdyaXR0ZW4gb3V0IGluIHB4IGJlY2F1c2UgbWFyaW1vJ3Mgcm9vdAogICBzdGF5cyB0aGUgYnJvd3NlcidzIDE2cHgsIHNvIGEgcmVtIGhlcmUgd291bGQgYmUgYSBkaWZmZXJlbnQgc2l6ZSB0aGFuCiAgIHRoZSBzYW1lIHJlbSBvbiB0aGUgbm90ZS4gKi8KLm1hcmtkb3duIGgxLCAubWFya2Rvd24gaDIsIC5tYXJrZG93biBoMywgLm1hcmtkb3duIGg0LAoucHJvc2UgaDEsIC5wcm9zZSBoMiwgLnByb3NlIGgzLCAucHJvc2UgaDQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zZXJpZik7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtaW5rKTsKICBsaW5lLWhlaWdodDogMS4yNTsKICBsZXR0ZXItc3BhY2luZzogMDsKfQoKLm1hcmtkb3duIGgxLCAucHJvc2UgaDEgewogIGZvbnQtc2l6ZTogMzdweDsKICBtYXJnaW46IDAgMCAyMnB4OwogIGxldHRlci1zcGFjaW5nOiAtMC4wMWVtOwp9CgovKiBBIGNoYXB0ZXIgYnJlYWsg4oCUIG9uZSBvZiB0aGUgdHdvIHBsYWNlcyB0aGUgcGVuIHN0aWxsIHdyaXRlcy4gKi8KLm1hcmtkb3duIGgyLCAucHJvc2UgaDIgewogIGZvbnQtc2l6ZTogMjhweDsKICBtYXJnaW46IDUwcHggMCAxNnB4OwogIHBhZGRpbmctYm90dG9tOiAwLjE4ZW07CiAgYmFja2dyb3VuZC1pbWFnZTogdmFyKC0tbGgtc3Ryb2tlKTsKICBiYWNrZ3JvdW5kLXJlcGVhdDogcmVwZWF0LXg7CiAgYmFja2dyb3VuZC1wb3NpdGlvbjogbGVmdCBib3R0b207CiAgYmFja2dyb3VuZC1zaXplOiAxMjBweCA3cHg7Cn0KCi8qIEEgbm90ZSBjZWxsJ3Mgb3duIHRpdGxlIChgIyMjIPCfk48gRGlzdGFuY2UgYW5kIGF2ZXJhZ2UgcGF0aCBsZW5ndGhgKS4gSXQgaXMKICAgc2V0IGxhcmdlciB0aGFuIHRoZSBwcm9zZSBiZW5lYXRoIGl0IHNvIHRoZSBmaW5pc2hlZCBub3RlYm9vayByZWFkcyBhcyBhCiAgIHJ1biBvZiBzZWN0aW9ucywgbm90IG9uZSBsb25nIGNvbHVtbi4gKi8KLm1hcmtkb3duIGgzLCAucHJvc2UgaDMgeyBmb250LXNpemU6IDIycHg7IG1hcmdpbjogMzZweCAwIDEzcHg7IH0KCi8qIFF1aWV0ZXIgdGhhbiBoMzogc2l6ZSBhbmQgd2VpZ2h0IG9ubHksIG5ldmVyIGEgcnVsZS4gKi8KLm1hcmtkb3duIGg0LCAucHJvc2UgaDQgeyBmb250LXNpemU6IDE4cHg7IG1hcmdpbjogMjdweCAwIDlweDsgfQoKLm1hcmtkb3duIGEsIC5wcm9zZSBhIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyB0ZXh0LWRlY29yYXRpb24tY29sb3I6IHZhcigtLWxoLWxpbmUpOyB9Ci5tYXJrZG93biBhOmhvdmVyLCAucHJvc2UgYTpob3ZlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBjdXJyZW50Q29sb3I7IH0KCi5tYXJrZG93biBzdHJvbmcsIC5wcm9zZSBzdHJvbmcgeyBjb2xvcjogdmFyKC0tbGgtaW5rKTsgZm9udC13ZWlnaHQ6IDcwMDsgfQoKLyogQSBxdW90ZSBjYXJyaWVzIE5PIGNocm9tZSBhdCBhbGw6IG5vIGZpbGwsIG5vIGJvcmRlciwgbm90IGV2ZW4gYSBydWxlIGluCiAgIHRoZSBtYXJnaW4g4oCUIGdyZXkgaW5rIGlzIHRoZSB3aG9sZSB0cmVhdG1lbnQuCgogICBJdCBoYXMgYmVlbiB3YWxrZWQgZG93biBvbmUgc3RlcCBhdCBhIHRpbWUgYW5kIGVhY2ggc3RlcCB3YXMgcmlnaHQuIEl0CiAgIHN0YXJ0ZWQgYXMgYSBzY3JhcCBvZiBwYXBlciBwaW5uZWQgdG8gdGhlIHBhZ2UgKGZpbGxlZCwgbmF2eS1ib3JkZXJlZCwKICAgc2hhZG93ZWQsIHRpbHRlZCBhIHF1YXJ0ZXIgZGVncmVlKSwgd2hpY2ggc2FpZCBMT09LIEFUIFRISVMgYWJvdXQgYSBsaW5lCiAgIHRoZSByZWFkZXIgaGFkIGFscmVhZHkgY2xpY2tlZCB0byBvcGVuLiBUaGVuIGEgbWFyZ2luIHJ1bGUsIHdoaWNoIHN0aWxsCiAgIGRyZXcgYSB2ZXJ0aWNhbCBsaW5lIGRvd24gYSBwYWdlIHRoYXQgaGFzIHBsZW50eS4gV2hhdCBpcyBsZWZ0IGlzIHdoYXQKICAgdGhlIHF1b3RlIGFjdHVhbGx5IGlzOiB0aGUgc3R1ZGVudCdzIG93biB3b3JkcywgaW4gdGhlIHBhZ2UncyBxdWlldCBncmV5LAogICB1bmRlciBhIGhlYWRpbmcgdGhhdCBhbHJlYWR5IG5hbWVzIHRoZW0uICM2QTZENzUgb24gd2hpdGUgaXMgNS4yOjEg4oCUCiAgIHF1aWV0IGlzIG5vdCB0aGUgc2FtZSBhcyB1bnJlYWRhYmxlLCBhbmQgdGhpcyBsaW5lIGlzIHRoZSBncmFkZWQgb25lLiAqLwoubWFya2Rvd24gYmxvY2txdW90ZSwKLnByb3NlIGJsb2NrcXVvdGUgewogIG1hcmdpbjogMS40ZW0gMDsKICBwYWRkaW5nOiAwOwogIGJhY2tncm91bmQ6IG5vbmU7CiAgYm9yZGVyOiAwOwogIGJvcmRlci1yYWRpdXM6IDA7CiAgYm94LXNoYWRvdzogbm9uZTsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGZvbnQtc3R5bGU6IG5vcm1hbDsKfQoKLyogLS0tLS0tLS0tLSB0aGUgc3R1ZGVudCdzIG93biBhbnN3ZXIsIGZvbGRlZCAtLS0tLS0tLS0tICovCgovKiBFdmVyeSBub3RlIGNlbGwgZW5kcyB3aXRoIHdoYXQgdGhlIHN0dWRlbnQgc2FpZCwgcXVvdGVkIHZlcmJhdGltLiBMZWZ0CiAgIG9wZW4gaXQgd2FzIHRoZSBsb3VkZXN0IHRoaW5nIG9uIHRoZSBwYWdlIOKAlCBhIGJvcmRlcmVkLCBzaGFkb3dlZCBzbGFiCiAgIHVuZGVyIGV2ZXJ5IHNpbmdsZSBub3RlLCBjb21wZXRpbmcgd2l0aCB0aGUgZmlndXJlIGFib3ZlIGl0IGFuZCB3aXRoIHRoZQogICBleHBsYW5hdGlvbiB0aGUgbm90ZSBleGlzdHMgdG8gZ2l2ZS4gU28gaXQgaXMgZm9sZGVkOiB0aGUgbm90ZSByZWFkcyBhcwogICB0aGUgbGVjdHVyZSBub3RlIGl0IGlzLCBhbmQgdGhlIGFuc3dlciBpcyBvbmUgY2xpY2sgYXdheS4KICAgYG1vLm1kYCByZW5kZXJzIGAvLy8gZGV0YWlscyB8IE15IGFuc3dlcmAgKyBgdHlwZTogbGgtYW5zd2VyYCBpbnRvIHRoaXMuCgogICBDbG9zZWQsIGl0IGlzIGEgZGFzaGVkIHRhYiBpbiB0aGUgbWFyZ2luIGNvbG91ciDigJQgcHJlc2VudCwgcXVpZXQsIGNsZWFybHkKICAgcHJlc3NhYmxlLiBPcGVuLCBpdCBpcyB0aGVpciB3b3JkcyBiZWhpbmQgYSBtYXJnaW4gcnVsZSwgYW5kIG5vdGhpbmcgZWxzZToKICAgYSByZWFkZXIgd2hvIGNsaWNrZWQgdG8gc2VlIHRoZSBhbnN3ZXIgZG9lcyBub3QgYWxzbyBuZWVkIGl0IGJveGVkLiAqLwovKiBtYXJpbW8gZHJlc3NlcyBFVkVSWSBgLm1hcmtkb3duIGRldGFpbHNgIGFzIGFuIGFkbW9uaXRpb24sIGFuZCB0aGVyZSBpcyBubwogICBvcHRpbmcgb3V0IGJ5IG5hbWluZyBhbiB1bmtub3duIHR5cGU6IGEgY2FyZC1jb2xvdXJlZCBiYWNrZ3JvdW5kLCBhIDZweAogICBsZWZ0IHJ1bGUsIGEgY2hldnJvbiBidWlsdCBvdXQgb2YgdHdvIHJvdGF0ZWQgYm9yZGVycyBvbiBgc3VtbWFyeTo6YmVmb3JlYCwKICAgYW5kIGEgMXJlbSBwYWQgb24gZXZlcnkgY2hpbGQgdGhhdCBpcyBub3QgdGhlIHN1bW1hcnkuIE9uIHBhcGVyLWNvbG91cmVkCiAgIHBhZ2VzIHRoYXQgY2FyZCByZWFkcyBhcyBhIGdyZXkgc2xhYiBwYXJrZWQgYmVoaW5kIHRoZSBhbnN3ZXIuIEFsbCBmb3VyIGFyZQogICB1bmRvbmUgaGVyZSDigJQgdGhpcyBmb2xkIGlzIGRyYXduIGZyb20gc2NyYXRjaCwgbm90IHRoZW1lZC4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgewogIG1hcmdpbjogMS4yZW0gMDsKICBiYWNrZ3JvdW5kOiBub25lOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwp9Ci8qIFRoZSAxcmVtIHBhZCBtYXJpbW8gcHV0cyBvbiB0aGUgcXVvdGUuIFRoZSBxdW90ZSBoYXMgaXRzIG93bi4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gKjpub3Qoc3VtbWFyeSksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+ICo6bm90KHN1bW1hcnkpIHsgcGFkZGluZzogMDsgfQoKLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSB7CiAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgYWxpZ24taXRlbXM6IGJhc2VsaW5lOwogIGdhcDogMC40NWVtOwogIHdpZHRoOiBmaXQtY29udGVudDsKICBjdXJzb3I6IHBvaW50ZXI7CiAgcGFkZGluZzogMnB4IDEycHggNHB4OwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXNpemU6IDE0cHg7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGJhY2tncm91bmQ6IHRyYW5zcGFyZW50OwogIGJvcmRlcjogMS41cHggZGFzaGVkIHZhcigtLWxoLXJ1bGUpOwogIGJvcmRlci1yYWRpdXM6IHZhcigtLWxoLXdvYmJsZS0yKTsKICAvKiBCb3RoIHNwZWxsaW5nczogU2FmYXJpIHN0aWxsIHNoaXBzIHRoZSBwc2V1ZG8tZWxlbWVudCwgZXZlcnlvbmUgZWxzZQogICAgIGhvbm91cnMgbGlzdC1zdHlsZS4gTGVmdCBpbiwgdGhlIGRlZmF1bHQgdHJpYW5nbGUgc2l0cyBvdXRzaWRlIHRoZSB0YWIuICovCiAgbGlzdC1zdHlsZTogbm9uZTsKICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lOwogIHVzZXItc2VsZWN0OiBub25lOwogIHRyYW5zaXRpb246IGNvbG9yIDAuMTJzIGVhc2UsIGJvcmRlci1jb2xvciAwLjEycyBlYXNlOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIgeyBkaXNwbGF5OiBub25lOyB9CgovKiBPdXJzLiBtYXJpbW8ncyBjaGV2cm9uIGlzIHR3byByb3RhdGVkIGJvcmRlcnMgd2l0aCBwYWRkaW5nIGFuZCBhIG1hcmdpbiwKICAgc28gZXZlcnkgb25lIG9mIHRob3NlIHByb3BlcnRpZXMgaGFzIHRvIGJlIG5hbWVkIHRvIGJlIHN3aXRjaGVkIG9mZiDigJQKICAgbGVmdCBpbiwgaXRzIDQ1ZGVnIGJveCBsYW5kcyBvbiB0b3Agb2YgdGhpcyBhcnJvdy4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeTo6YmVmb3JlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OjpiZWZvcmUgewogIGNvbnRlbnQ6ICLilrgiOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwogIG1hcmdpbjogMDsKICB0cmFuc2Zvcm06IG5vbmU7CiAgdHJhbnNpdGlvbjogbm9uZTsKICB2ZXJ0aWNhbC1hbGlnbjogYmFzZWxpbmU7CiAgZm9udC1zaXplOiAxMXB4OwogIGxpbmUtaGVpZ2h0OiAxOwogIGNvbG9yOiB2YXIoLS1saC1ibHVlLTIpOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnk6OmJlZm9yZSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyW29wZW5dID4gc3VtbWFyeTo6YmVmb3JlIHsKICBjb250ZW50OiAi4pa+IjsKICB0cmFuc2Zvcm06IG5vbmU7Cn0KCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIgewogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtYmx1ZS0yKTsKfQoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OmZvY3VzLXZpc2libGUsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Zm9jdXMtdmlzaWJsZSB7CiAgb3V0bGluZTogMnB4IHNvbGlkIHZhcigtLWxoLWJsdWUpOwogIG91dGxpbmUtb2Zmc2V0OiAycHg7Cn0KCi8qIE9wZW46IHRoZSB0YWIgaGFuZHMgb3ZlciB0byB0aGUgcXVvdGUsIHNvIGl0IHN0b3BzIGRyYXdpbmcgYSBib3JkZXIuICovCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnkgewogIGJvcmRlci1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgcGFkZGluZy1sZWZ0OiAwOwogIHBhZGRpbmctcmlnaHQ6IDA7Cn0KCi8qIEluc2lkZSB0aGUgZm9sZCwgYW5kIE9OTFkgaW5zaWRlIGl0LCB0aGUgcXVvdGUgaXMgaGFuZHdyaXRpbmcuIFRoYXQgaXMKICAgd2hhdCB0ZWxscyBhIHJlYWRlciBhdCBhIGdsYW5jZSB3aGljaCB3b3JkcyBhcmUgdGhlIG5vdGUncyBhbmQgd2hpY2ggYXJlCiAgIHRoZWlycyDigJQgdGhlIGdyZXkgYWxvbmUgbGVmdCB0aGUgdHdvIGxvb2tpbmcgbGlrZSBvbmUgdm9pY2UuCiAgIFNjb3BlZCB0byB0aGUgZm9sZCBvbiBwdXJwb3NlOiBjcDcgcXVvdGVzIGFuIEFJJ3MgYW5hbHlzaXMgaW4gYQogICBibG9ja3F1b3RlIHRvbywgYW5kIHRoYXQgb25lIGlzIGVtcGhhdGljYWxseSBub3Qgd3JpdHRlbiBieSBoYW5kLiAqLwoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlIHsKICBtYXJnaW4tdG9wOiAwLjNlbTsKICBmb250LWZhbWlseTogdmFyKC0tbGgtaGFuZCk7CiAgLyogVGhlc2UgZmFjZXMgcnVuIHNtYWxsIGZvciB0aGVpciBwb2ludCBzaXplIOKAlCBTZWdvZSBQcmludCBlc3BlY2lhbGx5LiAqLwogIGZvbnQtc2l6ZTogMS4wNmVtOwogIGxpbmUtaGVpZ2h0OiAxLjU7Cn0KCi5tYXJrZG93biBociwgLnByb3NlIGhyIHsKICBib3JkZXI6IDA7CiAgaGVpZ2h0OiA3cHg7CiAgbWFyZ2luOiAyZW0gMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UtZmFpbnQpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGNlbnRlcjsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoKLm1hcmtkb3duIGNvZGU6bm90KHByZSBjb2RlKSwKLnByb3NlIGNvZGU6bm90KHByZSBjb2RlKSB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMC44NmVtOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHBhZGRpbmc6IDAuMWVtIDAuNGVtOwogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB0YWJsZXMgLS0tLS0tLS0tLSAqLwoKLm1hcmtkb3duIHRhYmxlLCAucHJvc2UgdGFibGUgeyBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOyBmb250LXNpemU6IDE2cHg7IH0KLm1hcmtkb3duIHRoLCAucHJvc2UgdGggewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXdlaWdodDogNzAwOwogIGZvbnQtc2l6ZTogMTRweDsKICBsZXR0ZXItc3BhY2luZzogMC4wMmVtOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHRleHQtYWxpZ246IGxlZnQ7CiAgYm9yZGVyLWJvdHRvbTogMDsKICBwYWRkaW5nOiA2cHggMTRweCA4cHggMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGJvdHRvbTsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoubWFya2Rvd24gdGQsIC5wcm9zZSB0ZCB7CiAgcGFkZGluZzogOHB4IDE0cHggOHB4IDA7CiAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkIHZhcigtLWxoLXJ1bGUpOwogIC8qIE51bWJlcnMgc3RheSBtZWNoYW5pY2FsOiBhIGNvbHVtbiB0aGF0IGRvZXMgbm90IGxpbmUgdXAgaXMgYSBjb2x1bW4gdGhhdAogICAgIGNhbm5vdCBiZSBjb21wYXJlZCwgd2hpY2ggaXMgdGhlIHdob2xlIHJlYXNvbiB0aGUgdGFibGUgaXMgdGhlcmUuICovCiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMTVweDsKICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zOwp9CgovKiAtLS0tLS0tLS0tIGNlbGxzIC0tLS0tLS0tLS0gKi8KCi5jZWxsLApbZGF0YS10ZXN0aWQ9ImNlbGwiXSB7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQouY2VsbDpudGgtb2YtdHlwZShldmVuKSwKW2RhdGEtdGVzdGlkPSJjZWxsIl06bnRoLW9mLXR5cGUoZXZlbikgeyBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7IH0KCi5jZWxsOmZvY3VzLXdpdGhpbiwKW2RhdGEtdGVzdGlkPSJjZWxsIl06Zm9jdXMtd2l0aGluIHsKICBib3gtc2hhZG93OiAwIDAgMCAycHggdmFyKC0tbGgtcnVsZSksIHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLmNlbGwtZWRpdG9yLAouY20tZWRpdG9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxMy41cHg7CiAgbGluZS1oZWlnaHQ6IDEuNTU7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7Cn0KCi5jbS1lZGl0b3IgLmNtLWd1dHRlcnMgewogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7CiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tbGgtcnVsZSk7Cn0KCi5jbS1lZGl0b3IuY20tZm9jdXNlZCB7IG91dGxpbmU6IDJweCBzb2xpZCB2YXIoLS1saC1ibHVlKTsgfQouY20tZWRpdG9yIC5jbS1jdXJzb3IgeyBib3JkZXItbGVmdC1jb2xvcjogdmFyKC0tbGgtcnVzdCk7IH0KLmNtLWVkaXRvciAuY20tc2VsZWN0aW9uQmFja2dyb3VuZCwKLmNtLWVkaXRvci5jbS1mb2N1c2VkIC5jbS1zZWxlY3Rpb25CYWNrZ3JvdW5kIHsgYmFja2dyb3VuZDogI0RDRTNFRCAhaW1wb3J0YW50OyB9Ci5jbS1lZGl0b3IgLmNtLWFjdGl2ZUxpbmUgeyBiYWNrZ3JvdW5kOiByZ2JhKDMxLCA1OCwgOTUsIDAuMDQ1KTsgfQoKLyogc3ludGF4ICovCi5jbS1lZGl0b3IgLnRvay1rZXl3b3JkLAouY20tZWRpdG9yIC5jbS1rZXl3b3JkIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyBmb250LXdlaWdodDogNTAwOyB9Ci5jbS1lZGl0b3IgLnRvay1udW1iZXIsCi5jbS1lZGl0b3IgLmNtLW51bWJlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgfQouY20tZWRpdG9yIC50b2stc3RyaW5nLAouY20tZWRpdG9yIC5jbS1zdHJpbmcgeyBjb2xvcjogIzRCNkEzQTsgfQouY20tZWRpdG9yIC50b2stY29tbWVudCwKLmNtLWVkaXRvciAuY20tY29tbWVudCB7IGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7IGZvbnQtc3R5bGU6IGl0YWxpYzsgfQouY20tZWRpdG9yIC50b2stdmFyaWFibGVOYW1lLAouY20tZWRpdG9yIC50b2stcHJvcGVydHlOYW1lIHsgY29sb3I6IHZhcigtLWxoLWluayk7IH0KLmNtLWVkaXRvciAudG9rLW9wZXJhdG9yIHsgY29sb3I6IHZhcigtLWxoLWluay0yKTsgfQoKLyogLS0tLS0tLS0tLSBvdXRwdXQgLS0tLS0tLS0tLSAqLwoKLm91dHB1dC1hcmVhLAoubWFyaW1vLW91dHB1dCB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7Cn0KCi5vdXRwdXQtYXJlYSBwcmUsCnByZS5vdXRwdXQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1tb25vKTsKICBmb250LXNpemU6IDEzcHg7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7CiAgcGFkZGluZzogMTBweCAxMnB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwp9CgovKiBBIGZpZ3VyZSBpcyBhIGRyYXdpbmcgdGFwZWQgb250byB0aGUgcGFnZS4gKi8KLm91dHB1dC1hcmVhIGltZywKLm1hcmltby1vdXRwdXQgaW1nLAoub3V0cHV0LWFyZWEgc3ZnLAoubWFyaW1vLW91dHB1dCBzdmcgewogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB1aSBjaHJvbWUgLS0tLS0tLS0tLSAqLwoKYnV0dG9uLAoubWFyaW1vLWJ1dHRvbiB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQoKLyogQW55dGhpbmcgdGhlIHN0dWRlbnQgYWN0dWFsbHkgcHJlc3NlcyDigJQg4pa2IFJ1biwg8J+TqCBTZW5kIHRvIG15IHR1dG9yLCB0aGUKICAgcmVmZXJlZSdzIGFwcGVhbCDigJQgaXMgZHJhd24sIGFuZCBtb3ZlcyB1bmRlciB0aGUgcHJlc3MuICovCi5tYXJpbW8tcnVuLWJ1dHRvbiwKLm1hcmltby1idXR0b24sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXSwKYnV0dG9uW2RhdGEtdmFyaWFudD0ic2Vjb25kYXJ5Il0sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4pOwogIHRyYW5zaXRpb246IHRyYW5zZm9ybSAwLjA2cyBlYXNlLCBib3gtc2hhZG93IDAuMDZzIGVhc2U7Cn0KLm1hcmltby1ydW4tYnV0dG9uOmFjdGl2ZSwKLm1hcmltby1idXR0b246YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJwcmltYXJ5Il06YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJzZWNvbmRhcnkiXTphY3RpdmUsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXTphY3RpdmUgewogIHRyYW5zZm9ybTogdHJhbnNsYXRlKDJweCwgMi41cHgpOwogIGJveC1zaGFkb3c6IG5vbmU7Cn0KCi5tYXJpbW8tcnVuLWJ1dHRvbiwKYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdIHsKICBiYWNrZ3JvdW5kOiB2YXIoLS1saC1ibHVlKTsKICBjb2xvcjogdmFyKC0tbGgtcGFwZXIpOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtaW5rKTsKfQoubWFyaW1vLXJ1bi1idXR0b246aG92ZXIsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXTpob3ZlciB7IGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUtMik7IH0KCi8qIFNsaWRlcnM6IGEgcGVuY2lsIGxpbmUgd2l0aCBhIGJlYWQgb24gaXQuIFNlbGVjdG9ycyBjb3ZlciBtYXJpbW8ncyBvd24KICAgd2lkZ2V0IGFuZCBhIHBsYWluIHJhbmdlIGlucHV0LCB3aGljaGV2ZXIgdGhlIGJ1aWxkIHJlbmRlcnMuICovCmlucHV0W3R5cGU9InJhbmdlIl0gewogIGFjY2VudC1jb2xvcjogdmFyKC0tbGgtYmx1ZSk7CiAgaGVpZ2h0OiAyMnB4Owp9Cltyb2xlPSJzbGlkZXIiXSwKW2RhdGEtb3JpZW50YXRpb249Imhvcml6b250YWwiXSBbcm9sZT0ic2xpZGVyIl0gewogIGJvcmRlcjogMnB4IHNvbGlkIHZhcigtLWxoLWluayk7CiAgYm9yZGVyLXJhZGl1czogNTglIDQyJSA1MCUgNTAlIC8gNTAlIDUwJSA0MiUgNTglOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIGJveC1zaGFkb3c6IHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLyogVGV4dCB0aGUgc3R1ZGVudCB0eXBlcyBpbnRvOiBhIHJ1bGVkIGJveCwgbm90IGEgY2hyb21lIGZpZWxkLiAqLwppbnB1dFt0eXBlPSJ0ZXh0Il0sCmlucHV0W3R5cGU9Im51bWJlciJdLAp0ZXh0YXJlYSwKLm1hcmltby10ZXh0LWlucHV0IHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtY2FyZCk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7CiAgYm94LXNoYWRvdzogdmFyKC0tbGgtcGVuLXNvZnQpOwp9CgovKiBUaGUgcGhvdG8gZHJvcCBib3gg4oCUIHRoZSBvbmUgcGxhY2Ugb24gdGhlIHBhZ2UgdGhhdCBhc2tzIGZvciBwYXBlci4gKi8KW2RhdGEtdGVzdGlkPSJmaWxlLXVwbG9hZCJdLAoubWFyaW1vLWZpbGUtdXBsb2FkLAouZHJvcHpvbmUgewogIGJvcmRlcjogMi41cHggZGFzaGVkIHZhcigtLWxoLWluaykgIWltcG9ydGFudDsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUpOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWNhcmQpOwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKfQoKLyogc3RhbGUgLyBlcnJvciBzdGF0ZXMgKi8KLmNlbGwuc3RhbGUsCltkYXRhLXN0YWxlPSJ0cnVlIl0geyBib3gtc2hhZG93OiBpbnNldCAzcHggMCAwIHZhcigtLWxoLXJ1c3QpOyB9CgoubWFyaW1vLWVycm9yLAoub3V0cHV0LWFyZWEgLmVycm9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxM3B4OwogIGJhY2tncm91bmQ6ICNGQkVERTc7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVzdCk7CiAgY29sb3I6ICM2RTJGMTQ7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBwYWRkaW5nOiAxMHB4IDEycHg7Cn0KCi8qIHNsaWRlcyAvIGFwcCB2aWV3ICovCi5zbGlkZXMsCltkYXRhLW1vZGU9InByZXNlbnQiXSAubWFya2Rvd24geyBmb250LXNpemU6IDE4cHg7IH0KCi8qIEEgc3R1ZGVudCB3aG8gaGFzIGFza2VkIGZvciBsZXNzIG1vdGlvbiBnZXRzIHRoZSBkcmF3aW5nIHdpdGhvdXQgdGhlCiAgIGJ1dHRvbiB0aGF0IG1vdmVzIHVuZGVyIHRoZSBwcmVzcy4gKi8KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOiByZWR1Y2UpIHsKICAubWFyaW1vLXJ1bi1idXR0b24sCiAgLm1hcmltby1idXR0b24sCiAgYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9InNlY29uZGFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7IHRyYW5zaXRpb246IG5vbmU7IH0KfQo="  # BUILT
    LECTURE_HALL_CSS = base64.b64decode(LECTURE_HALL_CSS_B64).decode("utf-8")

    INK = "#1D1E21"
    RULE = "#D9D2C2"
    BLUE = "#3959A6"
    RUST = "#B14434"
    PAPER = "#FFFDF7"
    DOT = "#CFC9BB"
    MUTED = "#6A6D75"
    MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
    WOBBLE = "7px 4px 8px 5px / 5px 8px 4px 7px"

    # ---- the network, for the kit's own figures and checks ------------------
    LES = nx.les_miserables_graph()
    POS = {n: (float(x), float(y)) for n, (x, y) in nx.spring_layout(LES, k=0.32, iterations=300, seed=3).items()}
    HOPS = dict(nx.all_pairs_shortest_path_length(LES))
    PATH = nx.path_graph(10)  # 0 - 1 - 2 - ... - 9, for checking ppr_walk

    # ---- words and boxes -----------------------------------------------------

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">{text}</div>'
        )

    def verdict(ok, msg):
        return note(msg, BLUE if ok else RUST)

    WAITING = mo.Html(
        f'<div style="font-family:{SANS};font-size:15px;color:{MUTED};'
        f'border:1.5px dashed {RULE};border-radius:{WOBBLE};padding:10px 14px;'
        'display:inline-block">Waiting on the cell above.</div>'
    )

    def sentence(walk, mark=None, upto=24):
        """A walk printed as a sentence. `mark` is drawn in rust."""
        words = []
        for n in walk[:upto]:
            w = html.escape(str(n))
            words.append(f'<b style="color:{RUST}">{w}</b>' if n == mark else w)
        tail = " …" if len(walk) > upto else ""
        return mo.Html(
            f'<div style="font-family:{MONO};font-size:14px;line-height:1.7;'
            f"color:{INK};background:{PAPER};border:1.5px solid {RULE};"
            f'border-radius:{WOBBLE};padding:10px 14px;margin:8px 0">'
            + " ".join(words) + tail + "</div>"
        )

    @contextlib.contextmanager
    def quiet():
        """Keep stderr off the page: see the note at the top of the file."""
        with contextlib.redirect_stderr(io.StringIO()):
            yield

    # ---- running student code with a step limit ------------------------------

    class TooLong(Exception):
        pass

    def run_limited(fn, *args, limit=3_000_000):
        """fn(*args), stopped with TooLong after `limit` traced events."""
        count = 0

        def tracer(frame, event, arg):
            nonlocal count
            count += 1
            if count > limit:
                raise TooLong
            return tracer

        old = sys.gettrace()
        sys.settrace(tracer)
        try:
            return fn(*args)
        finally:
            sys.settrace(old)

    def failed(e):
        return f"stops with <code>{html.escape(type(e).__name__)}: {html.escape(str(e))}</code>"

    # ---- vectors -------------------------------------------------------------

    def cos_all(vectors, name):
        """Cosine similarity of `name` with every other character."""
        others = [n for n in vectors if n != name]
        V = np.array([vectors[n] for n in others], dtype=float)
        v = np.asarray(vectors[name], dtype=float)
        # Sums, not @: numpy 2 on macOS (Accelerate) warns about matmul on
        # finite input, and the warning would land on the page.
        sims = (V * v).sum(axis=1) / (np.sqrt((V * V).sum(axis=1)) * np.sqrt((v * v).sum()))
        return dict(zip(others, sims.tolist()))

    def kit_closest(vectors, name, k=10):
        sims = cos_all(vectors, name)
        return sorted(sims, key=lambda n: -sims[n])[:k]

    def pca_2d(vectors):
        """The two directions along which the vectors spread the most."""
        names = list(vectors)
        X = np.array([vectors[n] for n in names], dtype=float)
        X = X - X.mean(axis=0)
        _, _, Vt = np.linalg.svd(X, full_matrices=False)
        Y = (X[:, None, :] * Vt[None, :2, :]).sum(axis=2)  # X @ Vt[:2].T, see cos_all
        return {n: (float(a), float(b)) for n, (a, b) in zip(names, Y)}

    def neighbours_and_hops(s, near):
        """How many of `near` are linked to s, and their mean distance from s."""
        linked = sum(LES.has_edge(s, n) for n in near)
        return linked, float(np.mean([HOPS[s][n] for n in near]))

    # ---- figures -------------------------------------------------------------

    ROLES = ["other", "closest", "chosen"]

    def panel(xy, me=None, near=(), title="", width=300, height=260, edges=False):
        """Dots at `xy`: `me` in rust, `near` in blue, the rest grey.
        edges=True also draws the links of the network."""
        near = set(near)
        rows = [
            dict(name=n, x=x, y=y, role="chosen" if n == me else "closest" if n in near else "other")
            for n, (x, y) in xy.items()
        ]
        rows.sort(key=lambda r: ROLES.index(r["role"]))  # chosen drawn last, on top
        X = alt.X("x:Q", axis=None, scale=alt.Scale(zero=False, nice=False))
        Y = alt.Y("y:Q", axis=None, scale=alt.Scale(zero=False, nice=False))
        layers = []
        if edges:
            erows = [
                dict(x=xy[a][0], y=xy[a][1], x2=xy[b][0], y2=xy[b][1])
                for a, b in LES.edges() if a in xy and b in xy
            ]
            layers.append(
                alt.Chart(alt.Data(values=erows))
                .mark_rule(color=RULE, strokeWidth=0.9)
                .encode(x=X, y=Y, x2="x2:Q", y2="y2:Q")
            )
        dots = alt.Chart(alt.Data(values=rows))
        layers.append(
            dots.mark_circle(stroke=INK, strokeWidth=0.6, opacity=1).encode(
                x=X, y=Y, tooltip=alt.Tooltip("name:N", title="character"),
                color=alt.Color("role:N", legend=None,
                                scale=alt.Scale(domain=ROLES, range=[DOT, BLUE, RUST])),
                size=alt.Size("role:N", legend=None,
                              scale=alt.Scale(domain=ROLES, range=[34, 80, 190])),
            )
        )
        if me is not None:
            layers.append(
                dots.transform_filter(alt.datum.role == "chosen")
                .mark_text(dy=-14, fontWeight="bold", fontSize=13, color=INK)
                .encode(x=X, y=Y, text="name:N")
            )
        return alt.layer(*layers).properties(width=width, height=height, title=title)

    def show(*panels):
        return (
            alt.hconcat(*panels, spacing=24)
            .configure(background=PAPER)
            .configure_view(stroke=None)
            .configure_title(fontSize=13, anchor="start", color=INK, font=SANS)
        )

    # ---- is the cell above filled in yet -------------------------------------

    COSINE_CASES = [
        (([1.0, 2.0], [2.0, 4.0]), 1.0, "same direction"),
        (([1.0, 0.0], [0.0, 1.0]), 0.0, "at right angles"),
        (([3.0, 4.0], [4.0, 3.0]), 0.96, ""),
        (([1.0, 0.0], [-1.0, 0.0]), -1.0, "opposite directions"),
    ]

    def cosine_problem(fn):
        """None when fn is the cosine similarity; else what is wrong."""
        for (x, y), want, why in COSINE_CASES:
            args = (np.array(x), np.array(y))
            try:
                got = run_limited(fn, *args)
            except Exception as e:
                return f"<code>cosine</code> {failed(e)}."
            if got is None or got is ...:
                return "Not yet — <code>cosine</code> returns nothing; it should return a number."
            try:
                got = float(got)
            except (TypeError, ValueError):
                return f"Not yet — <code>cosine</code> returns <code>{html.escape(repr(got))}</code>, not a number."
            if abs(got - want) > 1e-9:
                dot = float(np.dot(x, y))
                hint = (
                    " That is the dot product: divide it by the two lengths."
                    if abs(got - dot) < 1e-9 else ""
                )
                why = f" ({why})" if why else ""
                return (
                    f"Not yet — <code>cosine({x}, {y})</code> should be "
                    f"<b>{want:g}</b>{why}; yours gives <b>{got:.4g}</b>.{hint}"
                )
        return None

    TOY = {
        "a": np.array([1.0, 0.0]),
        "b": np.array([0.9, 0.1]),
        "c": np.array([0.0, 1.0]),
        "d": np.array([-1.0, 0.0]),
        "e": np.array([10.0, 5.0]),
    }

    def as_names(got):
        """Accept a list of names, or of (name, score) pairs."""
        if isinstance(got, (list, tuple)) and all(isinstance(g, (list, tuple)) and len(g) == 2 for g in got):
            return [g[0] for g in got]
        return got

    def closest_problem(fn, vectors, name):
        """None when fn lists the k closest characters; else what is wrong."""
        try:
            toy = as_names(run_limited(fn, TOY, "a", 2))
        except Exception as e:
            return f"<code>closest</code> {failed(e)}."
        if toy is None or toy is ...:
            return "Not yet — <code>closest</code> returns nothing; it should return a list of names."
        if not isinstance(toy, (list, tuple)):
            return f"Not yet — <code>closest</code> returns a <code>{type(toy).__name__}</code>; return a list of names."
        toy = list(toy)
        if toy != ["b", "e"]:
            if toy[:1] == ["a"]:
                why = "The list starts with the character itself (its cosine with itself is 1). Leave it out."
            elif toy == ["e", "b"]:
                why = "This is the order of the dot product. Score with <code>cosine</code>."
            elif toy == ["d", "c"]:
                why = "These are the least similar. Sort from the largest cosine down."
            elif len(toy) != 2:
                why = f"That is {len(toy)} names; return <code>k</code> of them."
            else:
                why = ""
            return (
                "Not yet — on the vectors a = (1, 0), b = (0.9, 0.1), c = (0, 1), "
                "d = (−1, 0), e = (10, 5), <code>closest(vectors, 'a', 2)</code> "
                f"should be <code>['b', 'e']</code>; yours gives <code>{html.escape(repr(toy))}</code>. {why}"
            )
        try:
            got = list(as_names(run_limited(fn, vectors, name, 10)))
        except Exception as e:
            return f"<code>closest</code> on the characters {failed(e)}."
        sims = cos_all(vectors, name)
        want = kit_closest(vectors, name, 10)
        if len(got) != 10 or any(n not in sims for n in got):
            return f"Not yet — expected 10 names of other characters, got <code>{html.escape(repr(got))}</code>."
        s = [sims[n] for n in got]
        if any(a < b - 1e-6 for a, b in zip(s, s[1:])) or min(s) < sims[want[-1]] - 1e-6:
            return f"Not yet — for {html.escape(name)} the 10 closest are {', '.join(want)}; yours are {', '.join(map(str, got))}."
        return None

    WALK_CHECKS = {}  # id(fn) -> (fn, result): three cells ask about the same fn

    def check_walk(fn):
        """(problem, restart rate): problem is None when fn is a walk with
        restart, and otherwise one sentence saying what is wrong."""
        hit = WALK_CHECKS.get(id(fn))
        if hit is None or hit[0] is not fn:
            r = walk_problem_uncached(fn)
            hit = WALK_CHECKS[id(fn)] = (fn, (r, None) if isinstance(r, str) else r)
        return hit[1]

    def walk_ready(fn):
        """True once the check under ppr_walk is green."""
        return check_walk(fn)[0] is None

    def pair_distances(walks, window=5):
        """Share of the pairs word2vec trains on (two nodes up to `window`
        steps apart in a walk, window=5 as in embed) at each distance in links:
        0, 1, 2, 3, and 4 or more."""
        counts = np.zeros(5)
        for w in walks:
            for i, a in enumerate(w):
                for b in w[i + 1 : i + 1 + window]:
                    counts[min(HOPS[a][b], 4)] += 1
        return counts / counts.sum()

    def walk_problem_uncached(fn):
        """Checked on a path 0 - 1 - ... - 9 with start 0: from nodes 2 to 9,
        a step to 0 can only be a restart."""

        def run(length, alpha, seed):
            return run_limited(fn, PATH, 0, length, alpha, random.Random(seed))

        try:
            w = run(50, 0.3, 1)
        except TooLong:
            return (
                "Not yet — <code>ppr_walk</code> did not finish. Check that every pass of "
                "the loop appends one node, and that a restart appends <code>start</code> "
                "instead of emptying the walk."
            )
        except Exception as e:
            return f"<code>ppr_walk</code> {failed(e)}."
        if not isinstance(w, list):
            return f"Not yet — <code>ppr_walk</code> returns a <code>{type(w).__name__}</code>; return the list <code>walk</code>."
        if len(w) == 1:
            return "Not yet — the walk is still <code>[start]</code>: nothing is appended."
        if len(w) != 50:
            return f"Not yet — <code>ppr_walk(G, 0, 50, ...)</code> gives {len(w)} nodes; it should give 50. <code>start</code> is the first of them."
        if w[0] != 0:
            return f"Not yet — the walk should begin at <code>start</code>; it begins at {w[0]!r}."
        for a, b in zip(w, w[1:]):
            if b != 0 and not PATH.has_edge(a, b):
                return (
                    f"Not yet — the step {a} → {b} is neither a move to a neighbour "
                    "nor a return to the start (0)."
                )
        try:
            w0 = run(2000, 0.0, 3)
            long = run(20000, 0.3, 4)
            w1 = run(20, 1.0, 2)
            same = run(30, 0.3, 5) == run(30, 0.3, 5)
        except TooLong:
            return "Not yet — <code>ppr_walk</code> did not finish on a longer walk."
        except Exception as e:
            return f"<code>ppr_walk</code> {failed(e)}."
        jumps = sum(1 for a, b in zip(w0, w0[1:]) if a >= 2 and b == 0)
        if jumps:
            return f"Not yet — with <code>alpha = 0</code> the walk should never restart, but it jumped back to the start {jumps} times."
        steps = [(a, b) for a, b in zip(long, long[1:]) if a >= 2]
        rate = sum(b == 0 for _, b in steps) / max(len(steps), 1)
        if abs(rate - 0.3) > 0.04:
            hint = " Restart when <code>rng.random() &lt; alpha</code>." if abs(rate - 0.7) < 0.04 else ""
            return (
                f"Not yet — with <code>alpha = 0.3</code> the walk restarted in {rate:.0%} of its "
                f"steps from nodes 2 to 9; it should be about 30%.{hint}"
            )
        if w1 != [0] * 20:
            return "Not yet — with <code>alpha = 1</code> every step should return to the start: <code>[0, 0, 0, ...]</code>."
        if not same:
            return (
                "Not yet — two calls with the same seed gave different walks. Draw every "
                "random number from <code>rng</code>, not from the <code>random</code> module."
            )
        return None, rate


@app.cell(hide_code=True)
def _():
    # Stylesheets are global, so one <style> tag in the first cell dresses the
    # whole notebook -- in the editor, in `marimo run`, and in molab.
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Lab · Character embeddings

    Random walks on a network, word2vec on the walks, and a walk that restarts. Cells marked ✍️ are yours. Everything else runs itself.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1 · The network

    The 77 characters of *Les Misérables*. Two characters are linked when they appear in the same chapter (Knuth 1993). Point at a dot to see its name.
    """)
    return


@app.cell
def _():
    G = nx.les_miserables_graph()  # ships with networkx; edge weights are not used here
    return (G,)


@app.cell(hide_code=True)
def _(G):
    show(panel(POS, title=f"{G.number_of_nodes()} characters, {G.number_of_edges()} links",
               width=620, height=420, edges=True))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2 · Walks as sentences

    At every step the walker moves to a random neighbour: $\Pr(i \to j) = A_{ij} / k_i$. We start `WALKS_PER_NODE` walks from every character.
    """)
    return


@app.function
def random_walk(G, start, length, rng):
    """A plain random walk of `length` nodes from `start`. `rng` is a random.Random."""
    walk = [start]
    while len(walk) < length:
        walk.append(rng.choice(list(G[walk[-1]])))  # a random neighbour of the last node
    return walk


@app.cell
def _(G):
    WALKS_PER_NODE = 20
    LENGTH = 40

    _rng = random.Random(0)
    plain_walks = [random_walk(G, s, LENGTH, _rng) for s in G for _ in range(WALKS_PER_NODE)]
    return LENGTH, WALKS_PER_NODE, plain_walks


@app.cell(hide_code=True)
def _(plain_walks):
    _w = next(w for w in plain_walks if w[0] == "Valjean")
    mo.vstack([
        mo.md(f"{len(plain_walks):,} walks. The first one from Valjean, read as a sentence:"),
        sentence(_w, mark="Valjean"),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3 · word2vec on the walks

    Skip-gram with negative sampling, as on the slides: a pair of characters up to `window` steps apart in a walk is a real pair (label 1), and `negative` random pairs get label 0.
    """)
    return


@app.cell
def _():
    from gensim.models import Word2Vec

    def embed(walks):
        """word2vec on the walks. Returns {character: vector of length 32}."""
        with quiet():  # hides a harmless message from gensim's compiled code
            model = Word2Vec(
                walks,
                vector_size=32,  # d, the length of each vector
                window=5,  # real pairs: up to 5 steps apart in a walk
                negative=5,  # random pairs per real pair
                sg=1,  # skip-gram
                min_count=1,  # keep every character
                sample=0,  # keep every visit
                epochs=20,
                workers=1,
                seed=0,
            )
        return {name: model.wv[name] for name in model.wv.index_to_key}

    return (embed,)


@app.cell
def _(embed, plain_walks):
    vectors = embed(plain_walks)
    return (vectors,)


@app.cell(hide_code=True)
def _(vectors):
    _v = vectors["Valjean"]
    mo.md(
        f"{len(vectors)} vectors of length {len(_v)}. Valjean's starts "
        f"`[{', '.join(f'{x:.2f}' for x in _v[:5])}, ...]`."
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4 · ✍️ The closest characters

    Two vectors are close when their cosine similarity is large:

    $$\cos(\mathbf x, \mathbf y) = \frac{\mathbf x^\top \mathbf y}{\|\mathbf x\|\,\|\mathbf y\|}$$

    `x @ y` is the dot product, and `np.linalg.norm(x)` is the length of `x`.
    """)
    return


@app.function
def cosine(x, y):
    """Cosine similarity of two vectors x and y (numpy arrays of the same length)."""
    return ...  # ✍️ one line


@app.cell(hide_code=True)
def _():
    _p = cosine_problem(cosine)
    verdict(_p is None, _p or "<b>Correct</b> — 1 for the same direction, 0 at right angles, −1 for opposite directions.")
    return


@app.function
def closest(vectors, name, k=10):
    """The k characters whose vectors have the largest cosine similarity with
    the vector of `name`, most similar first, without `name` itself.

    vectors  a dict {character: numpy vector}; vectors[name] is one vector
    """
    # ✍️ your code here: score every other character with cosine(), then sort
    return ...


@app.cell(hide_code=True)
def _(vectors):
    if cosine_problem(cosine) is not None:
        _out = note("Waiting on <code>cosine</code>.", RULE)
    else:
        _p = closest_problem(closest, vectors, "Valjean")
        _out = verdict(_p is None, _p or "<b>Correct</b> — the 10 largest cosine similarities, largest first.")
    _out
    return


@app.cell(hide_code=True)
def _(G):
    who = mo.ui.dropdown(sorted(G.nodes), value="Valjean", label="Character")
    return (who,)


@app.cell(hide_code=True)
def _(vectors, who):
    _me = who.value
    _ready = cosine_problem(cosine) is None and closest_problem(closest, vectors, "Valjean") is None
    _near = list(as_names(closest(vectors, _me, 10))) if _ready else []
    _charts = show(
        panel(POS, _me, _near, title="in the network", width=330, height=290, edges=True),
        panel(pca_2d(vectors), _me, _near, title="the 77 vectors, in two dimensions (PCA)", width=330, height=290),
    )
    if _ready:
        _k, _h = neighbours_and_hops(_me, _near)
        _list = mo.md(
            f"**The 10 closest to {_me}:** " + ", ".join(_near) + ".  \n"
            f"{_k} of them are linked to {_me}; on average they are {_h:.1f} links away."
        )
    else:
        _list = note("The closest characters appear here once <code>closest</code> is correct.", RULE)
    mo.vstack([who, _charts, _list])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    PCA keeps the two directions along which the 77 vectors spread the most. Rust: the character you chose. Blue: its 10 closest.

    ---

    ## 5 · ✍️ A walk with restart

    At every step, the walker goes back to the start node $s$ with probability $\alpha$; otherwise it moves to a random neighbour:

    $$\Pr(i \to j) = \alpha\,[\,j = s\,] + (1-\alpha)\,A_{ij} / k_i$$

    `rng.random()` is a number in $[0, 1)$, so it is below `alpha` with probability `alpha`. A restart is a step: append `start` to the walk.
    """)
    return


@app.function
def ppr_walk(G, start, length, alpha, rng):
    """A walk of `length` nodes from `start` that restarts at `start` with
    probability `alpha` at every step. `rng` is a random.Random."""
    walk = [start]
    # ✍️ your code here: with probability alpha, go back to `start`;
    #    otherwise move to a random neighbour of the last node
    ...
    return walk


@app.cell(hide_code=True)
def _():
    _p, _rate = check_walk(ppr_walk)
    verdict(
        _p is None,
        _p or f"<b>Correct</b> — on a path of 10 nodes with α = 0.3, the walk went back "
        f"to the start in {_rate:.1%} of its steps from nodes two or more links away.",
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6 · Plain walk and walk with restart

    Every character starts `WALKS_PER_NODE` walks with restart, each one going back to its own start node. word2vec then embeds the walks as before.
    """)
    return


@app.cell
def _(G, LENGTH, WALKS_PER_NODE, embed):
    ALPHAS = (0.05, 0.5)  # try other values

    ppr_walks, ppr_vectors = {}, {}
    if walk_ready(ppr_walk):  # once the check above is green
        for _alpha in ALPHAS:
            _rng = random.Random(0)
            ppr_walks[_alpha] = [ppr_walk(G, s, LENGTH, _alpha, _rng) for s in G for _ in range(WALKS_PER_NODE)]
            ppr_vectors[_alpha] = embed(ppr_walks[_alpha])
    return ALPHAS, ppr_vectors, ppr_walks


@app.cell(hide_code=True)
def _(ppr_walks):
    if not ppr_walks:
        _out = WAITING
    else:
        _alpha = max(ppr_walks)
        _w = next(w for w in ppr_walks[_alpha] if w[0] == "Valjean")
        _out = mo.vstack([
            mo.md(f"The first walk from Valjean with α = {_alpha}:"),
            sentence(_w, mark="Valjean"),
        ])
    _out
    return


@app.cell(hide_code=True)
def _(ALPHAS, plain_walks, ppr_walks):
    if not ppr_walks:
        _out = mo.md("")
    else:
        _labels = ["plain walk"] + [f"α = {a}" for a in ALPHAS]
        _shares = [pair_distances(plain_walks)] + [pair_distances(ppr_walks[a]) for a in ALPHAS]
        _rows = [
            dict(rule=label, distance=d, share=float(s[k]))
            for label, s in zip(_labels, _shares)
            for k, d in enumerate(["0", "1", "2", "3", "4+"])
        ]
        _colors = [INK, "#DAB167", BLUE, MUTED, RUST][: len(_labels)]
        _chart = (
            alt.Chart(alt.Data(values=_rows))
            .mark_circle(size=110, stroke=INK, strokeWidth=0.6, opacity=1)
            .encode(
                x=alt.X("distance:O", sort=None, title="distance in links between the two characters",
                        axis=alt.Axis(labelAngle=0)),
                xOffset=alt.XOffset("rule:N", sort=_labels),
                y=alt.Y("share:Q", title="share of pairs", axis=alt.Axis(format="%")),
                color=alt.Color("rule:N", sort=_labels, title=None,
                                scale=alt.Scale(domain=_labels, range=_colors)),
                tooltip=["rule:N", "distance:O", alt.Tooltip("share:Q", format=".1%")],
            )
            .properties(width=440, height=220, title="the pairs word2vec trains on: two characters up to 5 steps apart in a walk")
            .configure(background=PAPER)
            .configure_view(stroke=None)
            .configure_title(fontSize=13, anchor="start", color=INK, font=SANS)
        )
        _out = mo.vstack([
            _chart,
            mo.md("Distance 0: the same character twice in one window."),
        ])
    _out
    return


@app.cell(hide_code=True)
def _(G):
    s_pick = mo.ui.dropdown(sorted(G.nodes), value="Valjean", label="Start node s")
    return (s_pick,)


@app.cell(hide_code=True)
def _(ALPHAS, G, ppr_vectors, s_pick, vectors):
    if not ppr_vectors:
        _out = mo.md("")
    else:
        _s = s_pick.value
        _rules = [("plain walk", vectors)] + [(f"α = {a}", ppr_vectors[a]) for a in ALPHAS]
        _near = {label: kit_closest(vecs, _s) for label, vecs in _rules}

        def _name(n):
            h = HOPS[_s][n]
            return html.escape(n) if h == 1 else f'{html.escape(n)} <span style="color:{MUTED}">· {h}</span>'

        _head = "".join(f"<th>{html.escape(label)}</th>" for label, _ in _rules)
        _body = "".join(
            f"<tr><td>{i + 1}</td>" + "".join(f"<td>{_name(_near[label][i])}</td>" for label, _ in _rules) + "</tr>"
            for i in range(10)
        )
        _stats = [neighbours_and_hops(_s, _near[label]) for label, _ in _rules]
        _foot = (
            "<tr><td></td>" + "".join(f"<td><b>{k} of 10</b> linked to s</td>" for k, _ in _stats) + "</tr>"
            "<tr><td></td>" + "".join(f"<td>mean distance <b>{h:.1f}</b></td>" for _, h in _stats) + "</tr>"
        )
        _table = mo.Html(
            f'<table style="font-family:{SANS};font-size:15px;border-collapse:collapse">'
            f"<thead><tr><th></th>{_head}</tr></thead><tbody>{_body}{_foot}</tbody></table>"
        )
        _charts = show(*[
            panel(POS, _s, _near[label], title=label, width=300, height=260, edges=True)
            for label, _ in _rules
        ])
        _out = mo.vstack([
            s_pick,
            mo.md(
                f"{html.escape(_s)} has {G.degree(_s)} links. Below: the 10 characters closest to "
                f"{html.escape(_s)} under each walk rule. A grey number is the distance in links "
                "from s; no number means a direct link."
            ),
            _table,
            _charts,
        ])
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    **Questions.** Which characters are closest to $s$ for $\alpha = 0.05$ and $\alpha = 0.5$? How do they differ from the plain walk? Start with Valjean, then try a character with one or two links.
    """)
    return


if __name__ == "__main__":
    app.run()
