# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "python-igraph==0.11.9",
#     "tabulate",
#     "matplotlib==3.10.3",
# ]
# ///
#
# Part 5 of the Module 2 pen-and-paper sheet, done alone at a laptop.
#
# The sheet builds Ringville by hand -- sixteen people in a circle, four
# friends each -- counts the handshakes from person 1, adds two shortcuts and
# counts again, then counts how many of one person's friend-pairs are friends.
# This notebook does the same three things by machine and then does the one
# thing pencil and paper cannot: turns the rewiring dial and draws the curve.
#
# The programming is deliberately thin. The class is not a programming class,
# and a student stuck on a nested comprehension is not learning what a
# handshake count is. So every blank sits inside a loop or a call that is
# already written, and the longest answer is one short line:
#
#   * ring_edges     -- both loops given, the student writes one line for j.
#     The page does NOT say to use `%`. It says j runs off the end of the
#     circle and has to come back to the beginning, and that there is more than
#     one way to do that; the modulo is one answer, not the answer.
#   * distances_from -- no breadth-first search. igraph is taught in two steps
#     on the small town first (edge list -> Graph, then .distances(source=s)),
#     with a live cell whose `source` the student changes and checks against
#     the drawing, and the blank is those two lines on a town it is handed.
#   * local_clustering -- the loop over pairs is given, and it uses
#     itertools.combinations rather than a numpy fancy-index square, so there
#     is no double-counting trap to fall into and climb out of.
#
# Three rules the file obeys, the first two learned the hard way on m01:
#
#   * No animation walks Ringville. The wave that shows what a handshake count
#     IS runs on a different, smaller town, because a coloured-in Ringville is
#     Question 1(b)'s answer sitting on the screen. Ringville appears as a
#     picture with nothing printed off it, and the checks on the student's
#     functions are run on the small town for the same reason.
#
#   * The stylesheet travels inside the file. molab ignores css_file
#     (marimo-team/marimo#8467), so lecture-hall.css is carried here as base64
#     and injected by the first cell. Refresh it with
#     `python tools/build_lab_notebooks.py m02-small-world` after editing it.
#
#   * igraph is pinned to the version the coding notebooks already use
#     (python-igraph==0.11.9, see notebooks/m02-small-world/starter.py), so the
#     idiom a student meets here is the one they meet there.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The drawing kit. Nothing here is yours to edit.
    import base64
    import itertools
    import math

    import igraph
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # The look travels inside the notebook rather than beside it. molab ignores
    # a notebook's css_file setting (marimo-team/marimo#8467) and this file is
    # uploaded there on its own, so lecture-hall.css is carried here, base64 so
    # that no quote or backslash in it can break the Python, and injected as a
    # <style> tag by the first cell -- the workaround marimo recommends.
    # Refresh it with tools/build_lab_notebooks.py after editing the CSS.
    LECTURE_HALL_CSS_B64 = "LyogTGVjdHVyZSBIYWxsIOKAlCBtYXJpbW8gY3VzdG9tIENTUywgZHJhd24gYnkgaGFuZAogICBVc2FnZTogcHV0IHRoaXMgbmV4dCB0byB5b3VyIG5vdGVib29rIGFuZCBhZGQgdG8gdGhlIG5vdGVib29rJ3MgY29uZmlnOgogICAgIFtkaXNwbGF5XSBjc3NfZmlsZSA9ICJsZWN0dXJlLWhhbGwuY3NzIgogICBvciBpbiBtYXJpbW8udG9tbCB1bmRlciBbZGlzcGxheV0uCgogICBUaGUgbm90ZWJvb2sgaXMgYSBsZWN0dXJlIG5vdGUgdGhlIHN0dWRlbnQgYW5kIHRoZSB0dXRvciBmaWxsIGluIHRvZ2V0aGVyLAogICBzbyBpdCBpcyBkcmVzc2VkIGFzIG9uZTogZG90LWdyaWQgcGFwZXIsIHdvYmJseSBpbmsgYm9yZGVycywgYW5kIHNlY3Rpb24KICAgcnVsZXMgZHJhd24gd2l0aCBhIHBlbi4KCiAgIFRIRSBIQU5EIElTIElOIFRIRSBMSU5FUywgTk9UIElOIFRIRSBMRVRURVJTLiBBIGhhbmR3cml0aW5nIGZhY2UgZm9yIHRoZQogICBwcm9zZSB3YXMgdGlyaW5nIHRvIHJlYWQgb3ZlciBuaW5ldHkgbWludXRlcyBhbmQgbWFkZSB0aGUgcGFnZSBsb29rIGxpa2UgYQogICBncmVldGluZyBjYXJkIHJhdGhlciB0aGFuIGEgbGVjdHVyZSBub3RlLiBTbyB0aGUgdHlwZSBpcyBleGFjdGx5IHRoZSBjb3Vyc2UKICAgbGVjdHVyZSBub3RlJ3MgKGFkdi1uZXQtc2NpL2xlY3R1cmUtbm90ZS9zY3NzL21pbmltYWwuc2Nzcyk6IGEgc3lzdGVtIHNhbnMKICAgZm9yIHRoZSBib2R5LCBhIHN5c3RlbSBzZXJpZiBmb3IgdGhlIGhlYWRpbmdzLCAxOHB4LzEuNjUg4oCUIHRoZSBzYW1lCiAgIHJlYWRpbmcgZXhwZXJpZW5jZSBvbiBib3RoIGhhbHZlcyBvZiB0aGUgY291cnNlLiBXaGF0IHN0YXlzIGhhbmQtZHJhd24gaXMKICAgZXZlcnl0aGluZyB0aGF0IGlzIG5vdCByZWFkIGFzIGEgd29yZDogdGhlIHdhdnkgc2VjdGlvbiBydWxlcywgdGhlIHdvYmJseQogICBib3JkZXJzIGFuZCBwZW4gc2hhZG93cywgdGhlIHNrZXRjaGVkIG1hdHBsb3RsaWIgc3Ryb2tlcywgYW5kIG5ldHZpeidzCiAgIHR1cmJ1bGVudCBlZGdlcy4KCiAgIE5vIHdlYmZvbnQsIG5vIG5ldHdvcmsgcmVxdWVzdDogYSBzdHVkZW50IG9uIGEgcGxhbmUgZ2V0cyB0aGUgc2FtZSBwYWdlLAogICBhbmQgdGhlcmUgaXMgbm8gZmlyc3QtcGFpbnQgZmxhc2ggb2YgYSBmYWxsYmFjayBmYWNlLgoKICAgVGhlIGFjY2VudHMgYXJlIHRoZSBMRUNUVVJFIFNMSURFUycgYWNjZW50cywgdmVyYmF0aW0g4oCUIHRoZSBtb2R1bGUgaXMgb25lCiAgIGNvdXJzZSwgc28gdGhlIGNvbG91ciB0aGF0IG1lYW5zICJ0aGUgdGhpbmcgd2UgYXJlIGxvb2tpbmcgYXQiIGhhcyB0byBtZWFuCiAgIGl0IGluIGJvdGggaGFsdmVzLiBDaGFuZ2Ugb25lIG9mIHRoZW0gaGVyZSBhbmQgeW91IG11c3QgY2hhbmdlIGl0IGluCiAgIGFkdi1uZXQtc2NpL3NsaWRlcy9tMDIvZmlndXJlcy9tYWtlX2ZpZ3VyZXMucHkgdG9vLCBhbmQgaW4gZXZlcnkgY2VsbHMvKi5weQogICB0aGF0IGhhcmRjb2RlcyBpdCAodGhleSBhbGwgZG8sIGZvciB0aGVpciBub2RlcyBhbmQgZWRnZXMpLiAqLwoKOnJvb3QgewogIC8qIHBhbGV0dGUg4oCUIHRoZSB0aHJlZSBhY2NlbnRzIGNvbWUgZnJvbSB0aGUgc2xpZGUgZGVjawogICAgIChtYWtlX2ZpZ3VyZXMucHk6IEFDQ0VOVCAvIEFDQ0VOVDIgLyBBQ0NFTlQzKSwgYW5kIHRoZSBwcmVtYWRlIGNlbGxzCiAgICAgaGFyZGNvZGUgdGhlIHNhbWUgaGV4ZXMgZm9yIHRoZWlyIG5vZGVzIGFuZCBlZGdlcywgc28gYSByZXBhaW50IGhlcmUKICAgICBkZXN5bmNzIGJvdGguIFdoYXQgaXMgTk9UIHRoZSBzbGlkZXMnIGlzIHRoZSBwYXBlcjogd2hpdGUgYmVjYW1lIHdhcm0sCiAgICAgYW5kIHRoZSBwZW5jaWwgcnVsZSAoLS1saC1ydWxlKSBpcyBhIG5ldyB0b2tlbiByYXRoZXIgdGhhbiBhIHJlcGFpbnQgb2YKICAgICAtLWxoLWxpbmUsIHdoaWNoIGlzIGEgbm9kZSBmaWxsIGluIGNwMiBhbmQgY3A1LiAqLwogIC0tbGgtcGFwZXI6ICAgI0ZGRkRGNzsKICAtLWxoLWNhcmQ6ICAgICNGRkZGRkY7CiAgLS1saC1zdXJmYWNlOiAjRjZGMkU5OwogIC0tbGgtbGluZTogICAgI0U0RTZFQTsKICAtLWxoLXJ1bGU6ICAgICNEOUQyQzI7CiAgLS1saC1pbms6ICAgICAjMUQxRTIxOwogIC0tbGgtaW5rLTI6ICAgIzM1MzczQzsKICAtLWxoLW11dGVkOiAgICM2QTZENzU7CiAgLS1saC1ibHVlOiAgICAjMjIzMzZCOwogIC0tbGgtYmx1ZS0yOiAgIzM5NTlBNjsKICAtLWxoLXJ1c3Q6ICAgICNCMTQ0MzQ7CgogIC8qIHR5cGUg4oCUIHRoZSBsZWN0dXJlIG5vdGUncyB0aHJlZSBzdGFja3MsIHZlcmJhdGltLiBBbGwgZnJvbSB0aGUgc3lzdGVtOgogICAgIG5vdGhpbmcgaGVyZSBpcyBmZXRjaGVkLiAqLwogIC0tbGgtc2VyaWY6ICAgIklvd2FuIE9sZCBTdHlsZSIsICJQYWxhdGlubyBMaW5vdHlwZSIsIFBhbGF0aW5vLAogICAgICAgICAgICAgICAgIkJvb2sgQW50aXF1YSIsICJIb2VmbGVyIFRleHQiLCBHZW9yZ2lhLAogICAgICAgICAgICAgICAgIlRpbWVzIE5ldyBSb21hbiIsIHNlcmlmOwogIC0tbGgtc2FuczogICAgc3lzdGVtLXVpLCAtYXBwbGUtc3lzdGVtLCAiU2Vnb2UgVUkiLCBSb2JvdG8sCiAgICAgICAgICAgICAgICAiSGVsdmV0aWNhIE5ldWUiLCAiTm90byBTYW5zIiwgIkxpYmVyYXRpb24gU2FucyIsIEFyaWFsLAogICAgICAgICAgICAgICAgc2Fucy1zZXJpZjsKICAtLWxoLW1vbm86ICAgIHVpLW1vbm9zcGFjZSwgU0ZNb25vLVJlZ3VsYXIsICJTRiBNb25vIiwgTWVubG8sIENvbnNvbGFzLAogICAgICAgICAgICAgICAgIkxpYmVyYXRpb24gTW9ubyIsIG1vbm9zcGFjZTsKICAvKiBUaGUgb25lIGhhbmQtd3JpdHRlbiBmYWNlIG9uIHRoZSBwYWdlLCBhbmQgaXQgd3JpdGVzIGV4YWN0bHkgb25lIHRoaW5nOgogICAgIHRoZSBzdHVkZW50J3Mgb3duIGFuc3dlcnMsIGluc2lkZSB0aGUgZm9sZC4gUHJpbnRlZCBub3RlLCBoYW5kd3JpdHRlbgogICAgIG1hcmdpbiDigJQgdGhlIGRpZmZlcmVuY2UgYmV0d2VlbiB0aGUgdHdvIGlzIHRoZSBwb2ludC4gU3lzdGVtIGZhY2VzIG9ubHksCiAgICAgbGlrZSBldmVyeXRoaW5nIGVsc2UgaGVyZTogbWFjT1Mgc2hpcHMgdGhlIGZpcnN0IHR3bywgV2luZG93cyB0aGUgbmV4dAogICAgIHR3bywgYGN1cnNpdmVgIGNhdGNoZXMgdGhlIHJlc3QuICovCiAgLS1saC1oYW5kOiAgICAiQ2hhbGtib2FyZCBTRSIsICJCcmFkbGV5IEhhbmQiLCAiU2Vnb2UgUHJpbnQiLAogICAgICAgICAgICAgICAgIkNvbWljIFNhbnMgTVMiLCBjdXJzaXZlOwoKICAvKiB0aGUgaGFuZC1kcmF3biBraXQ6IHR3byByb3VuZGluZyBzZXRzLCBhbHRlcm5hdGVkIHNvIG5vIHR3byBib3hlcyBvbiB0aGUKICAgICBwYWdlIGhhdmUgdGhlIHNhbWUgY29ybmVycywgYW5kIG9uZSBpbmsgc2hhZG93IHRoYXQgZmFrZXMgYSBzZWNvbmQgcGFzcwogICAgIG9mIHRoZSBwZW4uICovCiAgLS1saC13b2JibGU6ICAgMTRweCA2cHggMTZweCA4cHggLyA4cHggMTZweCA2cHggMTRweDsKICAtLWxoLXdvYmJsZS0yOiA2cHggMTZweCA4cHggMTRweCAvIDE2cHggNnB4IDE0cHggOHB4OwogIC0tbGgtcGVuOiAgICAgIDNweCA0cHggMCAtMXB4IHJnYmEoMzUsIDM0LCA0MywgMC4xNik7CiAgLS1saC1wZW4tc29mdDogMnB4IDNweCAwIC0xcHggcmdiYSgzNSwgMzQsIDQzLCAwLjEyKTsKCiAgLyogYSB3YXZ5IHN0cm9rZSwgdXNlZCBmb3IgdW5kZXJsaW5lcyBhbmQgdGFibGUgcnVsZXMgKi8KICAtLWxoLXN0cm9rZTogdXJsKCJkYXRhOmltYWdlL3N2Zyt4bWwsJTNDc3ZnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Zycgd2lkdGg9JzEyMCcgaGVpZ2h0PSc3JyB2aWV3Qm94PScwIDAgMTIwIDcnJTNFJTNDcGF0aCBkPSdNMSA0LjRDMjAgMS45IDQwIDYuMiA2MCAzLjcgODAgMS40IDEwMCA1LjYgMTE5IDMuMicgZmlsbD0nbm9uZScgc3Ryb2tlPSclMjNCMTQ0MzQnIHN0cm9rZS13aWR0aD0nMicgc3Ryb2tlLWxpbmVjYXA9J3JvdW5kJy8lM0UlM0Mvc3ZnJTNFIik7CiAgLS1saC1zdHJva2UtZmFpbnQ6IHVybCgiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMjAnIGhlaWdodD0nNycgdmlld0JveD0nMCAwIDEyMCA3JyUzRSUzQ3BhdGggZD0nTTEgNC40QzIwIDEuOSA0MCA2LjIgNjAgMy43IDgwIDEuNCAxMDAgNS42IDExOSAzLjInIGZpbGw9J25vbmUnIHN0cm9rZT0nJTIzRDlEMkMyJyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcvJTNFJTNDL3N2ZyUzRSIpOwoKICAvKiBtYXJpbW8gdG9rZW5zICovCiAgLS1iYWNrZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1pbmspOwogIC0tY2FyZDogdmFyKC0tbGgtY2FyZCk7CiAgLS1jYXJkLWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1wb3BvdmVyOiB2YXIoLS1saC1jYXJkKTsKICAtLXBvcG92ZXItZm9yZWdyb3VuZDogdmFyKC0tbGgtaW5rKTsKICAtLW11dGVkOiB2YXIoLS1saC1zdXJmYWNlKTsKICAtLW11dGVkLWZvcmVncm91bmQ6IHZhcigtLWxoLW11dGVkKTsKICAtLWJvcmRlcjogdmFyKC0tbGgtbGluZSk7CiAgLS1pbnB1dDogdmFyKC0tbGgtbGluZSk7CiAgLS1yaW5nOiB2YXIoLS1saC1ibHVlKTsKICAtLXByaW1hcnk6IHZhcigtLWxoLWJsdWUpOwogIC0tcHJpbWFyeS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1zZWNvbmRhcnk6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tc2Vjb25kYXJ5LWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1hY2NlbnQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tYWNjZW50LWZvcmVncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIC0tZGVzdHJ1Y3RpdmU6IHZhcigtLWxoLXJ1c3QpOwogIC0tZGVzdHJ1Y3RpdmUtZm9yZWdyb3VuZDogdmFyKC0tbGgtcGFwZXIpOwogIC0tcmFkaXVzOiAzcHg7CgogIC0tdGV4dC1mb250OiB2YXIoLS1saC1zYW5zKTsKICAtLWhlYWRpbmctZm9udDogdmFyKC0tbGgtc2VyaWYpOwogIC0tY29kZS1mb250OiB2YXIoLS1saC1tb25vKTsKfQoKLyogLS0tLS0tLS0tLSBwYWdlIC0tLS0tLS0tLS0gKi8KCi8qIERvdC1ncmlkLCBub3QgcnVsZWQgbGluZXM6IHRoZSBzYW1lICJ0aGlzIGlzIGEgc2tldGNoYm9vayIgc2lnbmFsLCBidXQgaXQKICAgZG9lcyBub3QgZmlnaHQgYSBsaW5lIG9mIHByb3NlIGZvciB0aGUgc2FtZSBob3Jpem9udGFsIGJhbmQuICovCmJvZHksCiNBcHAgewogIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWxoLXBhcGVyKTsKICBiYWNrZ3JvdW5kLWltYWdlOiByYWRpYWwtZ3JhZGllbnQocmdiYSgzMSwgNTgsIDk1LCAwLjA4NSkgMXB4LCB0cmFuc3BhcmVudCAxcHgpOwogIGJhY2tncm91bmQtc2l6ZTogMjRweCAyNHB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIC13ZWJraXQtZm9udC1zbW9vdGhpbmc6IGFudGlhbGlhc2VkOwp9CgovKiAtLS0tLS0tLS0tIHByb3NlIC0tLS0tLS0tLS0gKi8KCi5tYXJrZG93biwKLnByb3NlIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgZm9udC1zaXplOiAxOHB4OwogIGxpbmUtaGVpZ2h0OiAxLjY1OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgdGV4dC13cmFwOiBwcmV0dHk7CiAgbWF4LXdpZHRoOiA2OGNoOwp9CgovKiBUaGUgbGVjdHVyZSBub3RlJ3Mgc2VyaWYgYW5kIGl0cyBzY2FsZSDigJQgaDEgMi4wNSAvIGgyIDEuNTUgLyBoMyAxLjIyIC8KICAgaDQgMS4wMiBhZ2FpbnN0IGl0cyAxOHB4IHJvb3QuIFdyaXR0ZW4gb3V0IGluIHB4IGJlY2F1c2UgbWFyaW1vJ3Mgcm9vdAogICBzdGF5cyB0aGUgYnJvd3NlcidzIDE2cHgsIHNvIGEgcmVtIGhlcmUgd291bGQgYmUgYSBkaWZmZXJlbnQgc2l6ZSB0aGFuCiAgIHRoZSBzYW1lIHJlbSBvbiB0aGUgbm90ZS4gKi8KLm1hcmtkb3duIGgxLCAubWFya2Rvd24gaDIsIC5tYXJrZG93biBoMywgLm1hcmtkb3duIGg0LAoucHJvc2UgaDEsIC5wcm9zZSBoMiwgLnByb3NlIGgzLCAucHJvc2UgaDQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zZXJpZik7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtaW5rKTsKICBsaW5lLWhlaWdodDogMS4yNTsKICBsZXR0ZXItc3BhY2luZzogMDsKfQoKLm1hcmtkb3duIGgxLCAucHJvc2UgaDEgewogIGZvbnQtc2l6ZTogMzdweDsKICBtYXJnaW46IDAgMCAyMnB4OwogIGxldHRlci1zcGFjaW5nOiAtMC4wMWVtOwp9CgovKiBBIGNoYXB0ZXIgYnJlYWsg4oCUIG9uZSBvZiB0aGUgdHdvIHBsYWNlcyB0aGUgcGVuIHN0aWxsIHdyaXRlcy4gKi8KLm1hcmtkb3duIGgyLCAucHJvc2UgaDIgewogIGZvbnQtc2l6ZTogMjhweDsKICBtYXJnaW46IDUwcHggMCAxNnB4OwogIHBhZGRpbmctYm90dG9tOiAwLjE4ZW07CiAgYmFja2dyb3VuZC1pbWFnZTogdmFyKC0tbGgtc3Ryb2tlKTsKICBiYWNrZ3JvdW5kLXJlcGVhdDogcmVwZWF0LXg7CiAgYmFja2dyb3VuZC1wb3NpdGlvbjogbGVmdCBib3R0b207CiAgYmFja2dyb3VuZC1zaXplOiAxMjBweCA3cHg7Cn0KCi8qIEEgbm90ZSBjZWxsJ3Mgb3duIHRpdGxlIChgIyMjIPCfk48gRGlzdGFuY2UgYW5kIGF2ZXJhZ2UgcGF0aCBsZW5ndGhgKS4gSXQgaXMKICAgc2V0IGxhcmdlciB0aGFuIHRoZSBwcm9zZSBiZW5lYXRoIGl0IHNvIHRoZSBmaW5pc2hlZCBub3RlYm9vayByZWFkcyBhcyBhCiAgIHJ1biBvZiBzZWN0aW9ucywgbm90IG9uZSBsb25nIGNvbHVtbi4gKi8KLm1hcmtkb3duIGgzLCAucHJvc2UgaDMgeyBmb250LXNpemU6IDIycHg7IG1hcmdpbjogMzZweCAwIDEzcHg7IH0KCi8qIFF1aWV0ZXIgdGhhbiBoMzogc2l6ZSBhbmQgd2VpZ2h0IG9ubHksIG5ldmVyIGEgcnVsZS4gKi8KLm1hcmtkb3duIGg0LCAucHJvc2UgaDQgeyBmb250LXNpemU6IDE4cHg7IG1hcmdpbjogMjdweCAwIDlweDsgfQoKLm1hcmtkb3duIGEsIC5wcm9zZSBhIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyB0ZXh0LWRlY29yYXRpb24tY29sb3I6IHZhcigtLWxoLWxpbmUpOyB9Ci5tYXJrZG93biBhOmhvdmVyLCAucHJvc2UgYTpob3ZlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBjdXJyZW50Q29sb3I7IH0KCi5tYXJrZG93biBzdHJvbmcsIC5wcm9zZSBzdHJvbmcgeyBjb2xvcjogdmFyKC0tbGgtaW5rKTsgZm9udC13ZWlnaHQ6IDcwMDsgfQoKLyogQSBxdW90ZSBjYXJyaWVzIE5PIGNocm9tZSBhdCBhbGw6IG5vIGZpbGwsIG5vIGJvcmRlciwgbm90IGV2ZW4gYSBydWxlIGluCiAgIHRoZSBtYXJnaW4g4oCUIGdyZXkgaW5rIGlzIHRoZSB3aG9sZSB0cmVhdG1lbnQuCgogICBJdCBoYXMgYmVlbiB3YWxrZWQgZG93biBvbmUgc3RlcCBhdCBhIHRpbWUgYW5kIGVhY2ggc3RlcCB3YXMgcmlnaHQuIEl0CiAgIHN0YXJ0ZWQgYXMgYSBzY3JhcCBvZiBwYXBlciBwaW5uZWQgdG8gdGhlIHBhZ2UgKGZpbGxlZCwgbmF2eS1ib3JkZXJlZCwKICAgc2hhZG93ZWQsIHRpbHRlZCBhIHF1YXJ0ZXIgZGVncmVlKSwgd2hpY2ggc2FpZCBMT09LIEFUIFRISVMgYWJvdXQgYSBsaW5lCiAgIHRoZSByZWFkZXIgaGFkIGFscmVhZHkgY2xpY2tlZCB0byBvcGVuLiBUaGVuIGEgbWFyZ2luIHJ1bGUsIHdoaWNoIHN0aWxsCiAgIGRyZXcgYSB2ZXJ0aWNhbCBsaW5lIGRvd24gYSBwYWdlIHRoYXQgaGFzIHBsZW50eS4gV2hhdCBpcyBsZWZ0IGlzIHdoYXQKICAgdGhlIHF1b3RlIGFjdHVhbGx5IGlzOiB0aGUgc3R1ZGVudCdzIG93biB3b3JkcywgaW4gdGhlIHBhZ2UncyBxdWlldCBncmV5LAogICB1bmRlciBhIGhlYWRpbmcgdGhhdCBhbHJlYWR5IG5hbWVzIHRoZW0uICM2QTZENzUgb24gd2hpdGUgaXMgNS4yOjEg4oCUCiAgIHF1aWV0IGlzIG5vdCB0aGUgc2FtZSBhcyB1bnJlYWRhYmxlLCBhbmQgdGhpcyBsaW5lIGlzIHRoZSBncmFkZWQgb25lLiAqLwoubWFya2Rvd24gYmxvY2txdW90ZSwKLnByb3NlIGJsb2NrcXVvdGUgewogIG1hcmdpbjogMS40ZW0gMDsKICBwYWRkaW5nOiAwOwogIGJhY2tncm91bmQ6IG5vbmU7CiAgYm9yZGVyOiAwOwogIGJvcmRlci1yYWRpdXM6IDA7CiAgYm94LXNoYWRvdzogbm9uZTsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGZvbnQtc3R5bGU6IG5vcm1hbDsKfQoKLyogLS0tLS0tLS0tLSB0aGUgc3R1ZGVudCdzIG93biBhbnN3ZXIsIGZvbGRlZCAtLS0tLS0tLS0tICovCgovKiBFdmVyeSBub3RlIGNlbGwgZW5kcyB3aXRoIHdoYXQgdGhlIHN0dWRlbnQgc2FpZCwgcXVvdGVkIHZlcmJhdGltLiBMZWZ0CiAgIG9wZW4gaXQgd2FzIHRoZSBsb3VkZXN0IHRoaW5nIG9uIHRoZSBwYWdlIOKAlCBhIGJvcmRlcmVkLCBzaGFkb3dlZCBzbGFiCiAgIHVuZGVyIGV2ZXJ5IHNpbmdsZSBub3RlLCBjb21wZXRpbmcgd2l0aCB0aGUgZmlndXJlIGFib3ZlIGl0IGFuZCB3aXRoIHRoZQogICBleHBsYW5hdGlvbiB0aGUgbm90ZSBleGlzdHMgdG8gZ2l2ZS4gU28gaXQgaXMgZm9sZGVkOiB0aGUgbm90ZSByZWFkcyBhcwogICB0aGUgbGVjdHVyZSBub3RlIGl0IGlzLCBhbmQgdGhlIGFuc3dlciBpcyBvbmUgY2xpY2sgYXdheS4KICAgYG1vLm1kYCByZW5kZXJzIGAvLy8gZGV0YWlscyB8IE15IGFuc3dlcmAgKyBgdHlwZTogbGgtYW5zd2VyYCBpbnRvIHRoaXMuCgogICBDbG9zZWQsIGl0IGlzIGEgZGFzaGVkIHRhYiBpbiB0aGUgbWFyZ2luIGNvbG91ciDigJQgcHJlc2VudCwgcXVpZXQsIGNsZWFybHkKICAgcHJlc3NhYmxlLiBPcGVuLCBpdCBpcyB0aGVpciB3b3JkcyBiZWhpbmQgYSBtYXJnaW4gcnVsZSwgYW5kIG5vdGhpbmcgZWxzZToKICAgYSByZWFkZXIgd2hvIGNsaWNrZWQgdG8gc2VlIHRoZSBhbnN3ZXIgZG9lcyBub3QgYWxzbyBuZWVkIGl0IGJveGVkLiAqLwovKiBtYXJpbW8gZHJlc3NlcyBFVkVSWSBgLm1hcmtkb3duIGRldGFpbHNgIGFzIGFuIGFkbW9uaXRpb24sIGFuZCB0aGVyZSBpcyBubwogICBvcHRpbmcgb3V0IGJ5IG5hbWluZyBhbiB1bmtub3duIHR5cGU6IGEgY2FyZC1jb2xvdXJlZCBiYWNrZ3JvdW5kLCBhIDZweAogICBsZWZ0IHJ1bGUsIGEgY2hldnJvbiBidWlsdCBvdXQgb2YgdHdvIHJvdGF0ZWQgYm9yZGVycyBvbiBgc3VtbWFyeTo6YmVmb3JlYCwKICAgYW5kIGEgMXJlbSBwYWQgb24gZXZlcnkgY2hpbGQgdGhhdCBpcyBub3QgdGhlIHN1bW1hcnkuIE9uIHBhcGVyLWNvbG91cmVkCiAgIHBhZ2VzIHRoYXQgY2FyZCByZWFkcyBhcyBhIGdyZXkgc2xhYiBwYXJrZWQgYmVoaW5kIHRoZSBhbnN3ZXIuIEFsbCBmb3VyIGFyZQogICB1bmRvbmUgaGVyZSDigJQgdGhpcyBmb2xkIGlzIGRyYXduIGZyb20gc2NyYXRjaCwgbm90IHRoZW1lZC4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgewogIG1hcmdpbjogMS4yZW0gMDsKICBiYWNrZ3JvdW5kOiBub25lOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwp9Ci8qIFRoZSAxcmVtIHBhZCBtYXJpbW8gcHV0cyBvbiB0aGUgcXVvdGUuIFRoZSBxdW90ZSBoYXMgaXRzIG93bi4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gKjpub3Qoc3VtbWFyeSksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+ICo6bm90KHN1bW1hcnkpIHsgcGFkZGluZzogMDsgfQoKLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSB7CiAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgYWxpZ24taXRlbXM6IGJhc2VsaW5lOwogIGdhcDogMC40NWVtOwogIHdpZHRoOiBmaXQtY29udGVudDsKICBjdXJzb3I6IHBvaW50ZXI7CiAgcGFkZGluZzogMnB4IDEycHggNHB4OwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXNpemU6IDE0cHg7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGJhY2tncm91bmQ6IHRyYW5zcGFyZW50OwogIGJvcmRlcjogMS41cHggZGFzaGVkIHZhcigtLWxoLXJ1bGUpOwogIGJvcmRlci1yYWRpdXM6IHZhcigtLWxoLXdvYmJsZS0yKTsKICAvKiBCb3RoIHNwZWxsaW5nczogU2FmYXJpIHN0aWxsIHNoaXBzIHRoZSBwc2V1ZG8tZWxlbWVudCwgZXZlcnlvbmUgZWxzZQogICAgIGhvbm91cnMgbGlzdC1zdHlsZS4gTGVmdCBpbiwgdGhlIGRlZmF1bHQgdHJpYW5nbGUgc2l0cyBvdXRzaWRlIHRoZSB0YWIuICovCiAgbGlzdC1zdHlsZTogbm9uZTsKICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lOwogIHVzZXItc2VsZWN0OiBub25lOwogIHRyYW5zaXRpb246IGNvbG9yIDAuMTJzIGVhc2UsIGJvcmRlci1jb2xvciAwLjEycyBlYXNlOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIgeyBkaXNwbGF5OiBub25lOyB9CgovKiBPdXJzLiBtYXJpbW8ncyBjaGV2cm9uIGlzIHR3byByb3RhdGVkIGJvcmRlcnMgd2l0aCBwYWRkaW5nIGFuZCBhIG1hcmdpbiwKICAgc28gZXZlcnkgb25lIG9mIHRob3NlIHByb3BlcnRpZXMgaGFzIHRvIGJlIG5hbWVkIHRvIGJlIHN3aXRjaGVkIG9mZiDigJQKICAgbGVmdCBpbiwgaXRzIDQ1ZGVnIGJveCBsYW5kcyBvbiB0b3Agb2YgdGhpcyBhcnJvdy4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeTo6YmVmb3JlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OjpiZWZvcmUgewogIGNvbnRlbnQ6ICLilrgiOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwogIG1hcmdpbjogMDsKICB0cmFuc2Zvcm06IG5vbmU7CiAgdHJhbnNpdGlvbjogbm9uZTsKICB2ZXJ0aWNhbC1hbGlnbjogYmFzZWxpbmU7CiAgZm9udC1zaXplOiAxMXB4OwogIGxpbmUtaGVpZ2h0OiAxOwogIGNvbG9yOiB2YXIoLS1saC1ibHVlLTIpOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnk6OmJlZm9yZSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyW29wZW5dID4gc3VtbWFyeTo6YmVmb3JlIHsKICBjb250ZW50OiAi4pa+IjsKICB0cmFuc2Zvcm06IG5vbmU7Cn0KCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIgewogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtYmx1ZS0yKTsKfQoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OmZvY3VzLXZpc2libGUsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Zm9jdXMtdmlzaWJsZSB7CiAgb3V0bGluZTogMnB4IHNvbGlkIHZhcigtLWxoLWJsdWUpOwogIG91dGxpbmUtb2Zmc2V0OiAycHg7Cn0KCi8qIE9wZW46IHRoZSB0YWIgaGFuZHMgb3ZlciB0byB0aGUgcXVvdGUsIHNvIGl0IHN0b3BzIGRyYXdpbmcgYSBib3JkZXIuICovCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnkgewogIGJvcmRlci1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgcGFkZGluZy1sZWZ0OiAwOwogIHBhZGRpbmctcmlnaHQ6IDA7Cn0KCi8qIEluc2lkZSB0aGUgZm9sZCwgYW5kIE9OTFkgaW5zaWRlIGl0LCB0aGUgcXVvdGUgaXMgaGFuZHdyaXRpbmcuIFRoYXQgaXMKICAgd2hhdCB0ZWxscyBhIHJlYWRlciBhdCBhIGdsYW5jZSB3aGljaCB3b3JkcyBhcmUgdGhlIG5vdGUncyBhbmQgd2hpY2ggYXJlCiAgIHRoZWlycyDigJQgdGhlIGdyZXkgYWxvbmUgbGVmdCB0aGUgdHdvIGxvb2tpbmcgbGlrZSBvbmUgdm9pY2UuCiAgIFNjb3BlZCB0byB0aGUgZm9sZCBvbiBwdXJwb3NlOiBjcDcgcXVvdGVzIGFuIEFJJ3MgYW5hbHlzaXMgaW4gYQogICBibG9ja3F1b3RlIHRvbywgYW5kIHRoYXQgb25lIGlzIGVtcGhhdGljYWxseSBub3Qgd3JpdHRlbiBieSBoYW5kLiAqLwoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlIHsKICBtYXJnaW4tdG9wOiAwLjNlbTsKICBmb250LWZhbWlseTogdmFyKC0tbGgtaGFuZCk7CiAgLyogVGhlc2UgZmFjZXMgcnVuIHNtYWxsIGZvciB0aGVpciBwb2ludCBzaXplIOKAlCBTZWdvZSBQcmludCBlc3BlY2lhbGx5LiAqLwogIGZvbnQtc2l6ZTogMS4wNmVtOwogIGxpbmUtaGVpZ2h0OiAxLjU7Cn0KCi5tYXJrZG93biBociwgLnByb3NlIGhyIHsKICBib3JkZXI6IDA7CiAgaGVpZ2h0OiA3cHg7CiAgbWFyZ2luOiAyZW0gMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UtZmFpbnQpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGNlbnRlcjsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoKLm1hcmtkb3duIGNvZGU6bm90KHByZSBjb2RlKSwKLnByb3NlIGNvZGU6bm90KHByZSBjb2RlKSB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMC44NmVtOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHBhZGRpbmc6IDAuMWVtIDAuNGVtOwogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB0YWJsZXMgLS0tLS0tLS0tLSAqLwoKLm1hcmtkb3duIHRhYmxlLCAucHJvc2UgdGFibGUgeyBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOyBmb250LXNpemU6IDE2cHg7IH0KLm1hcmtkb3duIHRoLCAucHJvc2UgdGggewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXdlaWdodDogNzAwOwogIGZvbnQtc2l6ZTogMTRweDsKICBsZXR0ZXItc3BhY2luZzogMC4wMmVtOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHRleHQtYWxpZ246IGxlZnQ7CiAgYm9yZGVyLWJvdHRvbTogMDsKICBwYWRkaW5nOiA2cHggMTRweCA4cHggMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGJvdHRvbTsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoubWFya2Rvd24gdGQsIC5wcm9zZSB0ZCB7CiAgcGFkZGluZzogOHB4IDE0cHggOHB4IDA7CiAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkIHZhcigtLWxoLXJ1bGUpOwogIC8qIE51bWJlcnMgc3RheSBtZWNoYW5pY2FsOiBhIGNvbHVtbiB0aGF0IGRvZXMgbm90IGxpbmUgdXAgaXMgYSBjb2x1bW4gdGhhdAogICAgIGNhbm5vdCBiZSBjb21wYXJlZCwgd2hpY2ggaXMgdGhlIHdob2xlIHJlYXNvbiB0aGUgdGFibGUgaXMgdGhlcmUuICovCiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMTVweDsKICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zOwp9CgovKiAtLS0tLS0tLS0tIGNlbGxzIC0tLS0tLS0tLS0gKi8KCi5jZWxsLApbZGF0YS10ZXN0aWQ9ImNlbGwiXSB7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQouY2VsbDpudGgtb2YtdHlwZShldmVuKSwKW2RhdGEtdGVzdGlkPSJjZWxsIl06bnRoLW9mLXR5cGUoZXZlbikgeyBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7IH0KCi5jZWxsOmZvY3VzLXdpdGhpbiwKW2RhdGEtdGVzdGlkPSJjZWxsIl06Zm9jdXMtd2l0aGluIHsKICBib3gtc2hhZG93OiAwIDAgMCAycHggdmFyKC0tbGgtcnVsZSksIHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLmNlbGwtZWRpdG9yLAouY20tZWRpdG9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxMy41cHg7CiAgbGluZS1oZWlnaHQ6IDEuNTU7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7Cn0KCi5jbS1lZGl0b3IgLmNtLWd1dHRlcnMgewogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7CiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tbGgtcnVsZSk7Cn0KCi5jbS1lZGl0b3IuY20tZm9jdXNlZCB7IG91dGxpbmU6IDJweCBzb2xpZCB2YXIoLS1saC1ibHVlKTsgfQouY20tZWRpdG9yIC5jbS1jdXJzb3IgeyBib3JkZXItbGVmdC1jb2xvcjogdmFyKC0tbGgtcnVzdCk7IH0KLmNtLWVkaXRvciAuY20tc2VsZWN0aW9uQmFja2dyb3VuZCwKLmNtLWVkaXRvci5jbS1mb2N1c2VkIC5jbS1zZWxlY3Rpb25CYWNrZ3JvdW5kIHsgYmFja2dyb3VuZDogI0RDRTNFRCAhaW1wb3J0YW50OyB9Ci5jbS1lZGl0b3IgLmNtLWFjdGl2ZUxpbmUgeyBiYWNrZ3JvdW5kOiByZ2JhKDMxLCA1OCwgOTUsIDAuMDQ1KTsgfQoKLyogc3ludGF4ICovCi5jbS1lZGl0b3IgLnRvay1rZXl3b3JkLAouY20tZWRpdG9yIC5jbS1rZXl3b3JkIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyBmb250LXdlaWdodDogNTAwOyB9Ci5jbS1lZGl0b3IgLnRvay1udW1iZXIsCi5jbS1lZGl0b3IgLmNtLW51bWJlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgfQouY20tZWRpdG9yIC50b2stc3RyaW5nLAouY20tZWRpdG9yIC5jbS1zdHJpbmcgeyBjb2xvcjogIzRCNkEzQTsgfQouY20tZWRpdG9yIC50b2stY29tbWVudCwKLmNtLWVkaXRvciAuY20tY29tbWVudCB7IGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7IGZvbnQtc3R5bGU6IGl0YWxpYzsgfQouY20tZWRpdG9yIC50b2stdmFyaWFibGVOYW1lLAouY20tZWRpdG9yIC50b2stcHJvcGVydHlOYW1lIHsgY29sb3I6IHZhcigtLWxoLWluayk7IH0KLmNtLWVkaXRvciAudG9rLW9wZXJhdG9yIHsgY29sb3I6IHZhcigtLWxoLWluay0yKTsgfQoKLyogLS0tLS0tLS0tLSBvdXRwdXQgLS0tLS0tLS0tLSAqLwoKLm91dHB1dC1hcmVhLAoubWFyaW1vLW91dHB1dCB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7Cn0KCi5vdXRwdXQtYXJlYSBwcmUsCnByZS5vdXRwdXQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1tb25vKTsKICBmb250LXNpemU6IDEzcHg7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7CiAgcGFkZGluZzogMTBweCAxMnB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwp9CgovKiBBIGZpZ3VyZSBpcyBhIGRyYXdpbmcgdGFwZWQgb250byB0aGUgcGFnZS4gKi8KLm91dHB1dC1hcmVhIGltZywKLm1hcmltby1vdXRwdXQgaW1nLAoub3V0cHV0LWFyZWEgc3ZnLAoubWFyaW1vLW91dHB1dCBzdmcgewogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB1aSBjaHJvbWUgLS0tLS0tLS0tLSAqLwoKYnV0dG9uLAoubWFyaW1vLWJ1dHRvbiB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQoKLyogQW55dGhpbmcgdGhlIHN0dWRlbnQgYWN0dWFsbHkgcHJlc3NlcyDigJQg4pa2IFJ1biwg8J+TqCBTZW5kIHRvIG15IHR1dG9yLCB0aGUKICAgcmVmZXJlZSdzIGFwcGVhbCDigJQgaXMgZHJhd24sIGFuZCBtb3ZlcyB1bmRlciB0aGUgcHJlc3MuICovCi5tYXJpbW8tcnVuLWJ1dHRvbiwKLm1hcmltby1idXR0b24sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXSwKYnV0dG9uW2RhdGEtdmFyaWFudD0ic2Vjb25kYXJ5Il0sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4pOwogIHRyYW5zaXRpb246IHRyYW5zZm9ybSAwLjA2cyBlYXNlLCBib3gtc2hhZG93IDAuMDZzIGVhc2U7Cn0KLm1hcmltby1ydW4tYnV0dG9uOmFjdGl2ZSwKLm1hcmltby1idXR0b246YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJwcmltYXJ5Il06YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJzZWNvbmRhcnkiXTphY3RpdmUsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXTphY3RpdmUgewogIHRyYW5zZm9ybTogdHJhbnNsYXRlKDJweCwgMi41cHgpOwogIGJveC1zaGFkb3c6IG5vbmU7Cn0KCi5tYXJpbW8tcnVuLWJ1dHRvbiwKYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdIHsKICBiYWNrZ3JvdW5kOiB2YXIoLS1saC1ibHVlKTsKICBjb2xvcjogdmFyKC0tbGgtcGFwZXIpOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtaW5rKTsKfQoubWFyaW1vLXJ1bi1idXR0b246aG92ZXIsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXTpob3ZlciB7IGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUtMik7IH0KCi8qIFNsaWRlcnM6IGEgcGVuY2lsIGxpbmUgd2l0aCBhIGJlYWQgb24gaXQuIFNlbGVjdG9ycyBjb3ZlciBtYXJpbW8ncyBvd24KICAgd2lkZ2V0IGFuZCBhIHBsYWluIHJhbmdlIGlucHV0LCB3aGljaGV2ZXIgdGhlIGJ1aWxkIHJlbmRlcnMuICovCmlucHV0W3R5cGU9InJhbmdlIl0gewogIGFjY2VudC1jb2xvcjogdmFyKC0tbGgtYmx1ZSk7CiAgaGVpZ2h0OiAyMnB4Owp9Cltyb2xlPSJzbGlkZXIiXSwKW2RhdGEtb3JpZW50YXRpb249Imhvcml6b250YWwiXSBbcm9sZT0ic2xpZGVyIl0gewogIGJvcmRlcjogMnB4IHNvbGlkIHZhcigtLWxoLWluayk7CiAgYm9yZGVyLXJhZGl1czogNTglIDQyJSA1MCUgNTAlIC8gNTAlIDUwJSA0MiUgNTglOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIGJveC1zaGFkb3c6IHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLyogVGV4dCB0aGUgc3R1ZGVudCB0eXBlcyBpbnRvOiBhIHJ1bGVkIGJveCwgbm90IGEgY2hyb21lIGZpZWxkLiAqLwppbnB1dFt0eXBlPSJ0ZXh0Il0sCmlucHV0W3R5cGU9Im51bWJlciJdLAp0ZXh0YXJlYSwKLm1hcmltby10ZXh0LWlucHV0IHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtY2FyZCk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7CiAgYm94LXNoYWRvdzogdmFyKC0tbGgtcGVuLXNvZnQpOwp9CgovKiBUaGUgcGhvdG8gZHJvcCBib3gg4oCUIHRoZSBvbmUgcGxhY2Ugb24gdGhlIHBhZ2UgdGhhdCBhc2tzIGZvciBwYXBlci4gKi8KW2RhdGEtdGVzdGlkPSJmaWxlLXVwbG9hZCJdLAoubWFyaW1vLWZpbGUtdXBsb2FkLAouZHJvcHpvbmUgewogIGJvcmRlcjogMi41cHggZGFzaGVkIHZhcigtLWxoLWluaykgIWltcG9ydGFudDsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUpOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWNhcmQpOwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKfQoKLyogc3RhbGUgLyBlcnJvciBzdGF0ZXMgKi8KLmNlbGwuc3RhbGUsCltkYXRhLXN0YWxlPSJ0cnVlIl0geyBib3gtc2hhZG93OiBpbnNldCAzcHggMCAwIHZhcigtLWxoLXJ1c3QpOyB9CgoubWFyaW1vLWVycm9yLAoub3V0cHV0LWFyZWEgLmVycm9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxM3B4OwogIGJhY2tncm91bmQ6ICNGQkVERTc7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVzdCk7CiAgY29sb3I6ICM2RTJGMTQ7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBwYWRkaW5nOiAxMHB4IDEycHg7Cn0KCi8qIHNsaWRlcyAvIGFwcCB2aWV3ICovCi5zbGlkZXMsCltkYXRhLW1vZGU9InByZXNlbnQiXSAubWFya2Rvd24geyBmb250LXNpemU6IDE4cHg7IH0KCi8qIEEgc3R1ZGVudCB3aG8gaGFzIGFza2VkIGZvciBsZXNzIG1vdGlvbiBnZXRzIHRoZSBkcmF3aW5nIHdpdGhvdXQgdGhlCiAgIGJ1dHRvbiB0aGF0IG1vdmVzIHVuZGVyIHRoZSBwcmVzcy4gKi8KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOiByZWR1Y2UpIHsKICAubWFyaW1vLXJ1bi1idXR0b24sCiAgLm1hcmltby1idXR0b24sCiAgYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9InNlY29uZGFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7IHRyYW5zaXRpb246IG5vbmU7IH0KfQo="  # BUILT
    LECTURE_HALL_CSS = base64.b64decode(LECTURE_HALL_CSS_B64).decode("utf-8")

    INK = "#1D1E21"
    RULE = "#D9D2C2"
    BLUE = "#3959A6"
    RUST = "#B14434"
    PAPER = "#FFFDF7"
    MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
    WOBBLE = "7px 4px 8px 5px / 5px 8px 4px 7px"

    # The sheet's town. Sixteen chairs, everybody friends with the two on each
    # side; the two shortcuts are the ones that came home from college. The
    # sheet numbers the chairs 1 to 16 and Python numbers them 0 to 15, so
    # everything here is one lower than the drawing -- said out loud in the
    # notebook, because it is the way to get a right answer and read it wrong.
    TOWN_N = 16
    TOWN_HALF = 2
    TOWN_SHORTCUTS = [(0, 8), (4, 12)]

    # The wave runs here instead, and the checks are run here too: a small town
    # that is NOT a ring, so neither the picture nor the check hands over the
    # rule the student is about to write or the numbers they filled in on the
    # sheet. Seven people, nine friendships.
    DEMO_N = 7
    DEMO_EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    _DEMO_POS = {
        0: (110, 34),
        1: (58, 96),
        2: (162, 96),
        3: (110, 158),
        4: (110, 224),
        5: (58, 288),
        6: (162, 288),
    }

    # A pen, not a plotter: fractal noise pushes every stroke off true by a
    # couple of pixels. Fixed seed, so the drawing keeps the same wobble
    # instead of vibrating as the slider moves. Text is drawn outside the
    # filtered group, because wobbly letters are simply hard to read.
    _PEN = (
        '<defs><filter id="lh-pen" x="-15%" y="-15%" width="130%" height="130%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" '
        'seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" '
        'xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
    )

    # How far out each wave is coloured, palest first. Index 0 is the person
    # the wave started from.
    _WAVE = [RUST, "#C4674F", "#7C86B8", BLUE, "#5A6E9E", "#8894B5"]

    def wave_fill(d):
        if d is None or d < 0:
            return PAPER
        return _WAVE[d] if d < len(_WAVE) else "#A8B0C8"

    def plain_adjacency(edges, n):
        """The kit's own, so the animations run before your code exists."""
        A = np.zeros((n, n), dtype=int)
        for i, j in edges:
            if i == j:
                continue
            A[i, j] = 1
            A[j, i] = 1
        return A

    def kit_ring(n, half):
        """The kit's own ring, for everything that has to run before yours."""
        return [(i, (i + d) % n) for i in range(n) for d in range(1, half + 1)]

    def edges_of(A):
        """A friendship table back to the list of pairs igraph wants."""
        return [(int(i), int(j)) for i, j in zip(*np.triu_indices_from(A, k=1)) if A[i, j]]

    def kit_distances(A, s):
        """The kit's own handshake counts, for the animations and the checks."""
        n = len(A)
        dist = np.full(n, -1)
        dist[s] = 0
        frontier = [s]
        while frontier:
            nxt = []
            for u in frontier:
                for v in np.flatnonzero(A[u]):
                    if dist[v] < 0:
                        dist[v] = dist[u] + 1
                        nxt.append(v)
            frontier = nxt
        return dist

    def kit_local_clustering(A, i):
        nbrs = np.flatnonzero(A[i])
        k = len(nbrs)
        if k < 2:
            return 0.0
        return float(A[np.ix_(nbrs, nbrs)].sum() / 2) / (k * (k - 1) / 2)

    def watts_strogatz(n, half, p, seed):
        """A ring with each friendship moved, with probability p, to a new
        person picked at random. Moved, not added -- which is the thing
        Question 6(b) is about."""
        rng = np.random.default_rng(seed)
        edges = {tuple(sorted(e)) for e in kit_ring(n, half)}
        out = set(edges)
        for i, j in sorted(edges):
            if rng.random() >= p:
                continue
            out.discard((i, j))
            for _ in range(200):
                k = int(rng.integers(n))
                if k != i and tuple(sorted((i, k))) not in out:
                    out.add(tuple(sorted((i, k))))
                    break
            else:
                out.add((i, j))
        return sorted(out)

    def ring_svg(
        n,
        edges,
        size=340,
        fills=None,
        labels=True,
        extra=(),
        node_r=None,
        pad=None,
    ):
        """A town of n people sitting in a circle, drawn the way the sheet
        draws it: person 0 at the top, then clockwise. `fills` colours the
        people; `extra` is a set of edges drawn in the shortcut colour."""
        node_r = node_r or (13 if n <= 20 else max(3.0, 150 / n))
        pad = pad or node_r + 8
        R = size / 2 - pad
        cx = cy = size / 2
        pos = {}
        for i in range(n):
            a = math.radians(90 - i * 360 / n)
            pos[i] = (cx + R * math.cos(a), cy - R * math.sin(a))
        extra = {tuple(sorted(e)) for e in extra}
        out = [
            f'<svg viewBox="0 0 {size} {size}" width="100%" '
            f'style="max-width:{size}px;display:block" '
            'xmlns="http://www.w3.org/2000/svg">',
            _PEN,
            '<g filter="url(#lh-pen)">',
        ]
        for i, j in edges:
            if tuple(sorted((i, j))) in extra:
                continue
            (x1, y1), (x2, y2) = pos[i], pos[j]
            gap = (abs(i - j)) % n
            gap = min(gap, n - gap)
            # Anything reaching further than two chairs is bowed towards the
            # middle, so it reads as a chord and not as part of the rim.
            bow = 0.0 if gap <= 1 else min(0.55, 0.16 * gap)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            qx, qy = cx + (mx - cx) * (1 - bow), cy + (my - cy) * (1 - bow)
            out.append(
                f'<path d="M{x1:.1f},{y1:.1f} Q{qx:.1f},{qy:.1f} {x2:.1f},{y2:.1f}" '
                f'fill="none" stroke="{INK}" stroke-width="{1.7 if n <= 20 else 1.0}" '
                f'opacity="0.42" stroke-linecap="round"/>'
            )
        for i, j in sorted(extra):
            (x1, y1), (x2, y2) = pos[i], pos[j]
            out.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{RUST}" stroke-width="2.6" stroke-linecap="round"/>'
            )
        for i in range(n):
            x, y = pos[i]
            out.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r:.1f}" '
                f'fill="{(fills or {}).get(i, PAPER)}" stroke="{INK}" '
                f'stroke-width="{2.2 if n <= 20 else 1.0}"/>'
            )
        out.append("</g>")
        if labels:
            for i in range(n):
                x, y = pos[i]
                dark = (fills or {}).get(i, PAPER) not in (PAPER, "#FFFFFF")
                out.append(
                    f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" '
                    f'font-size="12" font-family="{SANS}" font-weight="700" '
                    f'fill="{PAPER if dark else INK}">{i}</text>'
                )
        out.append("</svg>")
        return "".join(out)

    def demo_svg(fills=None, lit_edges=(), faint_edges=()):
        """The small town the wave runs on, and the one the pair-counting
        animation uses. Never Ringville."""
        lit = {tuple(sorted(e)) for e in lit_edges}
        faint = {tuple(sorted(e)) for e in faint_edges}
        out = [
            '<svg viewBox="0 0 220 322" width="100%" style="max-width:220px;'
            'display:block" xmlns="http://www.w3.org/2000/svg">',
            _PEN,
            '<g filter="url(#lh-pen)">',
        ]
        for i, j in sorted(faint - lit):
            (x1, y1), (x2, y2) = _DEMO_POS[i], _DEMO_POS[j]
            out.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" '
                'stroke-width="1.6" stroke-dasharray="3 4" opacity="0.5"/>'
            )
        for i, j in DEMO_EDGES:
            (x1, y1), (x2, y2) = _DEMO_POS[i], _DEMO_POS[j]
            hot = tuple(sorted((i, j))) in lit
            out.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{RUST if hot else INK}" '
                f'stroke-width="{3.4 if hot else 2.0}" '
                f'opacity="{1 if hot else 0.35}" stroke-linecap="round"/>'
            )
        for i, (x, y) in _DEMO_POS.items():
            out.append(
                f'<circle cx="{x}" cy="{y}" r="14" '
                f'fill="{(fills or {}).get(i, PAPER)}" stroke="{INK}" '
                'stroke-width="2.4"/>'
            )
        out.append("</g>")
        for i, (x, y) in _DEMO_POS.items():
            dark = (fills or {}).get(i, PAPER) != PAPER
            out.append(
                f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="12" '
                f'font-family="{SANS}" font-weight="700" '
                f'fill="{PAPER if dark else INK}">{i}</text>'
            )
        out.append("</svg>")
        return "".join(out)

    def wave_table_html(dist, upto):
        """Who is how far out, filling up one row per wave."""
        rows = []
        for d in range(0, upto + 1):
            who = sorted(int(i) for i in np.flatnonzero(dist == d))
            rows.append(
                f'<div style="margin:7px 0;line-height:1.5">'
                f'<span style="display:inline-block;width:11px;height:11px;'
                f"border-radius:3px;background:{wave_fill(d)};"
                f'margin-right:9px"></span>'
                f'<span style="opacity:0.6">{d} handshake{"" if d == 1 else "s"} '
                f'away</span>&nbsp; <b style="font-family:{MONO};color:{INK}">'
                f'{{{", ".join(str(i) for i in who)}}}</b></div>'
            )
        for _ in range(upto + 1, 5):
            rows.append('<div style="margin:7px 0;line-height:1.5">&nbsp;</div>')
        return (
            f'<div style="font-family:{SANS};font-size:15px;color:{INK}">'
            + "".join(rows)
            + "</div>"
        )

    def two_col(left, right, left_basis=250):
        return mo.Html(
            '<div style="display:flex;gap:26px;align-items:center;'
            'justify-content:flex-start;flex-wrap:wrap">'
            f'<div style="flex:0 0 {left_basis}px;max-width:100%">{left}</div>'
            f'<div style="flex:0 1 auto">{right}</div></div>'
        )

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">{text}</div>'
        )

    def verdict(ok, good, bad):
        return note(good if ok else bad, BLUE if ok else RUST)

    def big(label, value, tone=RUST):
        return (
            f'<div style="font-family:{SANS};padding-right:26px">'
            f'<div style="font-size:12px;opacity:0.55;font-weight:700">'
            f"{label.upper()}</div>"
            f'<div style="font-size:30px;font-weight:700;color:{tone};'
            f'margin:2px 0">{value}</div></div>'
        )

    WAITING = mo.Html(
        f'<div style="font-family:{SANS};font-size:15px;color:#6A6D75;'
        f'border:1.5px dashed {RULE};border-radius:{WOBBLE};padding:10px 14px;'
        'display:inline-block">Waiting on the cell above.</div>'
    )

    # ---- what the town's numbers are, once your functions exist -------------

    def mean_distance(A, fn, cap=40, seed=0):
        """Average handshakes over every pair, using YOUR distances_from.

        Above `cap` people it averages over `cap` starting points rather than
        all of them, so the dial below stays a dial and not a progress bar.
        """
        n = len(A)
        if n <= cap:
            sources = range(n)
        else:
            sources = np.random.default_rng(seed).choice(n, cap, replace=False)
        edges = edges_of(A)
        tot, cnt = 0.0, 0
        for s in sources:
            d = np.asarray(fn(edges, n, int(s)), dtype=float)
            # Rewiring can cut a town in two, and igraph scores an unreachable
            # person `inf`. Those pairs are left out rather than averaged in.
            reached = d[np.isfinite(d) & (d > 0)]
            tot += float(reached.sum())
            cnt += int(reached.size)
        return tot / cnt if cnt else float("inf")

    def mean_clustering(A, fn):
        return float(np.mean([fn(A, i) for i in range(len(A))]))

    from collections import namedtuple

    Measured = namedtuple(
        "Measured", "n k C L C_rand L_rand C_latt L_latt"
    )

    def measure(A, C_fn, L_fn, seed=0):
        """The six numbers a small-world test can be built out of, all of them
        computed with your two functions."""
        n = len(A)
        k = float(A.sum()) / n
        R = plain_adjacency(kit_ring(n, max(1, int(round(k / 2)))), n)
        return Measured(
            n=n,
            k=k,
            C=mean_clustering(A, C_fn),
            L=mean_distance(A, L_fn, seed=seed),
            C_rand=k / (n - 1),
            L_rand=math.log(n) / math.log(k),
            C_latt=mean_clustering(R, C_fn),
            L_latt=mean_distance(R, L_fn, seed=seed),
        )

    def sigma(m):
        """The textbook small-world index, for the section that breaks it."""
        return (m.C / m.C_rand) / (m.L / m.L_rand)

    # ---- is the cell above filled in yet ------------------------------------

    def ring_ready(fn):
        try:
            got = sorted({tuple(sorted(e)) for e in fn(8, 2)})
        except Exception:
            return False
        return got == sorted({tuple(sorted(e)) for e in kit_ring(8, 2)})

    def distances_ready(fn):
        try:
            got = np.asarray(fn(DEMO_EDGES, DEMO_N, 0), dtype=float)
        except Exception:
            return False
        want = kit_distances(plain_adjacency(DEMO_EDGES, DEMO_N), 0).astype(float)
        return got.shape == want.shape and bool(np.array_equal(got, want))

    def clustering_ready(fn):
        A = plain_adjacency(DEMO_EDGES, DEMO_N)
        try:
            got = [round(float(fn(A, i)), 6) for i in range(DEMO_N)]
        except Exception:
            return False
        return got == [round(kit_local_clustering(A, i), 6) for i in range(DEMO_N)]

    def town_ready(fn):
        """True once ring_edges builds the sheet's town and not another one."""
        if not ring_ready(fn):
            return False
        try:
            A = plain_adjacency(fn(TOWN_N, TOWN_HALF), TOWN_N)
        except Exception:
            return False
        return bool(np.all(A.sum(axis=1) == 4)) and int(A.sum() // 2) == 32


@app.cell(hide_code=True)
def _():
    # Stylesheets are global, so one <style> tag in the first cell dresses the
    # whole notebook -- in the editor, in `marimo run`, and in molab.
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part 5 · Hand the town to the machine

    **On your own**, with the sheet next to the laptop.

    Cells marked ✍️ are yours. Everything else runs itself.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 1 · Watch a handshake count happen

    Here is a different town — seven people, nine friendships, nothing like
    Ringville. Drag the slider and watch the wave go out from person `0`.
    """)
    return


@app.cell(hide_code=True)
def _():
    wave = mo.ui.slider(0, 4, value=0, label="handshakes", show_value=True)
    wave
    return (wave,)


@app.cell(hide_code=True)
def _(wave):
    _d = kit_distances(plain_adjacency(DEMO_EDGES, DEMO_N), 0)
    _fills = {i: wave_fill(int(_d[i])) for i in range(DEMO_N) if _d[i] <= wave.value}
    two_col(
        demo_svg(fills=_fills),
        wave_table_html(_d, wave.value),
        left_basis=220,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "That is all a handshake count is: <b>which wave you were in</b>. "
        "Person 5 lights up on the fourth wave, so person 5 is four handshakes "
        "from person 0 — and the wave found the shortest chain without ever "
        "looking for one, because nobody gets coloured twice.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 2 · ✍️ Build the town

    Thirty-two friendships is too many to type, so write the **rule** instead:
    in a town of `n` people sitting in a circle, everybody is friends with the
    `half` people on each side.

    The two loops are written for you. **One line is yours**: the person sitting
    `d` seats clockwise from person `i`.

    Counting up gets you most of the way — the next chair along is `i + 1`, the
    one after that is `i + 2`. It stops working at the end of the circle. In
    Ringville `15 + 2` is `17`, and this town has no person 17. It has no person
    16 either: the chairs are numbered 0 to 15, and then they start over.

    So a `j` that has run off the end has to come back to the beginning. There
    is more than one way to bring it back, and any of them is fine.
    """)
    return


@app.function
def ring_edges(n, half):
    """Every friendship in a circle of n people with `half` friends each side.

    n     how many people sit in the circle. Ringville has n = 16.
    half  how many friends each person has on ONE side. Ringville has
          half = 2, which is why everybody there ends up with 4 friends:
          two clockwise and two anticlockwise.

    Returns a list of (i, j) pairs.
    """
    edges = []
    for i in range(n):                  # each person in turn
        for d in range(1, half + 1):    # the seat 1 along, then 2 along, ...
            j = ...  # ✍️ replace the ... — who sits d seats clockwise from i?
            edges.append((i, j))
    return edges


@app.cell(hide_code=True)
def _():
    try:
        _e = list(ring_edges(TOWN_N, TOWN_HALF))
    except Exception:
        _e = None
    if _e is None:
        _msg = "Not yet — the cell above still returns nothing."
    elif any(e[1] is Ellipsis or e[0] is Ellipsis for e in _e):
        _msg = (
            "Not yet — <code>j</code> is still <code>...</code>. One line: who "
            "sits <code>d</code> seats clockwise from <code>i</code>?"
        )
    elif any(not (0 <= int(e[1]) < TOWN_N) for e in _e):
        _bad = next(e for e in _e if not (0 <= int(e[1]) < TOWN_N))
        _msg = (
            f"Not yet — your <code>j</code> has reached "
            f"<b>{int(_bad[1])}</b>, and this town stops at person "
            f"<b>{TOWN_N - 1}</b>. <code>j</code> has run off the end of the "
            "circle, and the chairs start over from 0 at that point."
        )
    else:
        _clean = [tuple(sorted(e)) for e in _e if len(tuple(e)) == 2]
        _loops = [e for e in _clean if e[0] == e[1]]
        _A = plain_adjacency(_clean, TOWN_N)
        _deg = _A.sum(axis=1)
        _m = int(_A.sum() // 2)
        if _loops:
            _msg = (
                "Not yet — you have people who are friends with themselves, so "
                "<code>j</code> is coming out equal to <code>i</code>. The "
                "nearest neighbour is <code>d</code> seats away, and "
                "<code>d</code> starts at 1."
            )
        elif not np.all(_deg == 4):
            _bad = int(np.argmax(_deg != 4))
            _msg = (
                f"Not yet — person <code>{_bad}</code> has "
                f"<b>{int(_deg[_bad])}</b> friends. Everybody in Ringville has "
                "<b>4</b>: two on the left and two on the right. If everybody "
                "has 2, you are only going one way round."
            )
        elif _m != 32:
            _msg = (
                f"Not yet — your town has <b>{_m}</b> friendships and "
                "Ringville has <b>32</b>."
            )
        else:
            _msg = None
    if _msg is None:
        _out = mo.vstack(
            [
                note(
                    "<b>That is the town.</b> Thirty-two friendships, four each, "
                    "out of one line of yours. Below is your own town drawn — "
                    "compare it with the circle in Part 1 of the sheet, "
                    "remembering that "
                    "the labels here start at 0.",
                    BLUE,
                ),
                mo.Html(ring_svg(TOWN_N, ring_edges(TOWN_N, TOWN_HALF))),
            ]
        )
    else:
        _out = note(_msg, RUST)
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 3 · Count the handshakes

    You are not going to write the wave. Sending it out is a solved problem,
    and it is solved for you in **igraph**.

    igraph is a library for networks. You hand it a network, and it answers
    questions about it — how far apart two people are, who is in the middle,
    which parts are connected to which. It is written in C and wrapped for
    Python, so it stays fast on networks far larger than Ringville, and it is
    the library the rest of this course uses. Documentation:
    [python.igraph.org](https://python.igraph.org/en/stable/).

    What is worth your time is knowing which call to make and what comes back.
    Two steps, one line each. Both run below on the seven-person town.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Step 1 — an edge list becomes a graph

    A town is a list of pairs. `igraph` turns that into something that can be
    asked questions:

    ```python
    import igraph

    g = igraph.Graph(n=7, edges=[(0, 1), (0, 2), (1, 2), ...])
    ```

    `n` has to be there. Without it igraph sizes the town from the pairs it can
    see, so a person with no friends at all would quietly vanish.
    """)
    return


@app.cell(hide_code=True)
def _():
    _g = igraph.Graph(n=DEMO_N, edges=DEMO_EDGES)
    two_col(
        demo_svg(),
        f'<div style="font-family:{MONO};font-size:14px;line-height:2.0">'
        f'<div style="opacity:0.55">g.vcount()</div><b>{_g.vcount()}</b> people'
        f'<div style="opacity:0.55;margin-top:10px">g.ecount()</div>'
        f"<b>{_g.ecount()}</b> friendships"
        f'<div style="opacity:0.55;margin-top:10px">g.neighbors(0)</div>'
        f"<b>{_g.neighbors(0)}</b></div>",
        left_basis=220,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Step 2 — the graph is asked for handshake counts

    ```python
    g.distances(source=0)
    ```

    One gotcha, and it is the only one. You asked about **one** starting
    person, but `distances` is built to take several, so it always answers with
    a *list of rows* — one row per starting person. Yours is the first and only
    row, so `[0]` on the end is what gets you the row itself.
    ([docs](https://python.igraph.org/en/stable/api/igraph.GraphBase.html#distances))

    **This next cell is a real one, and it is yours.** Change the `0`, run it,
    and check the answer against the picture underneath with your own finger.
    """)
    return


@app.cell
def _():
    # ▶ Try it. Change source to any person from 0 to 6 and run the cell.
    source = 0

    g_demo = igraph.Graph(n=DEMO_N, edges=DEMO_EDGES)
    g_demo.distances(source=source)
    return (source,)


@app.cell(hide_code=True)
def _(source):
    _g = igraph.Graph(n=DEMO_N, edges=DEMO_EDGES)
    _s = int(source) if 0 <= int(source) < DEMO_N else 0
    _row = _g.distances(source=_s)[0]
    _cells = "".join(
        f'<tr><td style="padding:1px 10px 1px 0;opacity:0.55">person {i}</td>'
        f'<td style="padding:1px 0"><b style="color:'
        f'{RUST if i == _s else BLUE}">{int(_row[i])}</b></td></tr>'
        for i in range(DEMO_N)
    )
    two_col(
        demo_svg(fills={i: wave_fill(int(_row[i])) for i in range(DEMO_N)}),
        f'<div style="font-family:{MONO};font-size:14px">'
        f'<div style="opacity:0.55;margin-bottom:6px">'
        f"g.distances(source={_s})[0]</div>"
        f'<table style="border-collapse:collapse">{_cells}</table></div>',
        left_basis=220,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "Pick somebody the picture puts a long way from your starting person "
        "and count the steps along the lines yourself. It is the number igraph "
        "gave them. The colours are the same waves the slider drew in section "
        "1 — all you have changed is who does the counting.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Now the two lines, for any town

    Step 1 then step 2, on whatever town it is handed.
    """)
    return


@app.function
def distances_from(edges, n, s):
    """How many handshakes from person s to everybody else.

    edges  the town's friendships, a list of (i, j) pairs.
    n      how many people are in the town.
    s      the person to count from.

    Returns a LIST of n numbers, one per person, in order: the first is the
    count to person 0, the second to person 1, and so on. Person s gets 0,
    being already there.

    For the seven-person town above, counting from person 0, the list is

        [0, 1, 1, 2, 3, 4, 4]

    which reads: person 1 is one handshake away, person 3 is two away, and
    persons 5 and 6 are four away.
    """
    import igraph

    g = ...  # ✍️ replace the ... — step 1, a graph of n people with these edges
    return ...  # ✍️ replace the ... — step 2, the counts out of person s


@app.cell(hide_code=True)
def _():
    # Checked on the small town, not on Ringville: a row of sixteen right
    # answers sitting here is Question 1(b) filled in for them.
    _A = plain_adjacency(DEMO_EDGES, DEMO_N)
    _want = kit_distances(_A, 0).astype(float)
    try:
        _got = np.asarray(distances_from(DEMO_EDGES, DEMO_N, 0), dtype=float)
    except Exception:
        _got = None
    _ok = _got is not None and _got.shape == _want.shape and np.array_equal(_got, _want)
    if _ok:
        _msg = (
            "<b>Correct on the small town</b> — the same waves the slider drew."
        )
    elif _got is None:
        _msg = (
            "Not yet — the two lines are still <code>...</code>. Step 1 is "
            "<code>igraph.Graph(n=..., edges=...)</code>, step 2 is "
            "<code>g.distances(source=...)</code>."
        )
    elif _got.ndim == 2:
        _msg = (
            "Not yet — you have handed back the <b>list of rows</b>, not the "
            "row. That is the <code>[0]</code> on the end of "
            "<code>g.distances(source=s)</code>."
        )
    elif not np.all(np.isfinite(_got)):
        _msg = (
            "Not yet — some people came back <code>inf</code>, meaning igraph "
            "could not reach them at all. The small town is in one piece, so "
            "the friendships did not all arrive: check that <code>edges</code> "
            "is what you passed to <code>igraph.Graph</code>."
        )
    else:
        _msg = (
            f"Not yet — you get <code>{[int(v) for v in _got]}</code> where the "
            f"slider drew <code>{[int(v) for v in _want]}</code>."
        )
    verdict(_ok, _msg, _msg)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Ringville, then — mark your own Question 1(c) and Question 3

    You worked these six numbers out in pencil. Copy them into the cell below
    exactly as you have them on the sheet, wrong ones included — then your own
    two functions will run on your own town and mark them.

    Getting one wrong here is worth more than getting them all right. It tells
    you which box on the drawing to go back to.
    """)
    return


@app.cell
def _():
    # ▶ Your pencil answers, off the sheet. Leave any you did not get as None.

    # Question 1(c) — Ringville, as it is in Part 1.
    my_total_1c = None  # every number in the boxes, added up
    my_average_1c = None  # that total shared among the other 15
    my_worst_1c = None  # the biggest number in any box

    # Question 3 — the same town with the two shortcuts of Part 2.
    my_total_3 = None
    my_average_3 = None
    my_worst_3 = None
    return (
        my_average_1c,
        my_average_3,
        my_total_1c,
        my_total_3,
        my_worst_1c,
        my_worst_3,
    )


@app.cell(hide_code=True)
def _(
    my_average_1c,
    my_average_3,
    my_total_1c,
    my_total_3,
    my_worst_1c,
    my_worst_3,
):
    if not (town_ready(ring_edges) and distances_ready(distances_from)):
        _out = WAITING
    else:
        _base = list(ring_edges(TOWN_N, TOWN_HALF))
        _mine = [
            (my_total_1c, my_average_1c, my_worst_1c),
            (my_total_3, my_average_3, my_worst_3),
        ]
        _cards, _wrong, _blank = [], 0, 0
        for _k, (_title, _edges) in enumerate(
            [
                ("Part 1 · Ringville", _base),
                ("Part 2 · with the shortcuts", _base + TOWN_SHORTCUTS),
            ]
        ):
            _d = np.asarray(distances_from(_edges, TOWN_N, 0), dtype=float)
            _tot = int(_d[_d > 0].sum())
            _machine = (_tot, _tot / (TOWN_N - 1), int(_d.max()))
            _rows = ""
            for _label, _got, _said in zip(
                ("total", "average", "worst case"), _machine, _mine[_k]
            ):
                if _said is None:
                    _blank += 1
                    _mark, _tone, _yours = "—", INK, "not filled in"
                elif abs(float(_said) - float(_got)) < 0.05:
                    _mark, _tone, _yours = "✓", BLUE, f"{_said}"
                else:
                    _wrong += 1
                    _mark, _tone, _yours = "✗", RUST, f"{_said}"
                _shown = f"{_got:.1f}" if _label == "average" else f"{int(_got)}"
                _rows += (
                    f'<tr><td style="padding:2px 12px 2px 0;opacity:0.55">'
                    f"{_label}</td>"
                    f'<td style="padding:2px 12px 2px 0">your pencil '
                    f'<b style="color:{_tone}">{_yours}</b></td>'
                    f'<td style="padding:2px 12px 2px 0">your code '
                    f'<b style="color:{BLUE}">{_shown}</b></td>'
                    f'<td style="padding:2px 0;font-size:18px;color:{_tone}">'
                    f"{_mark}</td></tr>"
                )
            _cards.append(
                mo.Html(
                    f'<div style="font-family:{SANS};padding-right:30px">'
                    f'<div style="font-size:12px;opacity:0.55;font-weight:700">'
                    f"{_title.upper()}</div>"
                    f'<table style="border-collapse:collapse;font-size:15px">'
                    f"{_rows}</table>"
                    f'<div style="opacity:0.6;font-size:14px;margin-top:6px">'
                    "furthest away: "
                    f"{sorted(int(i) for i in np.flatnonzero(_d == _d.max()))}</div>"
                    "</div>"
                )
            )
        if _blank == 6:
            _verdict = note(
                "Your six numbers go in the cell above. What your code makes of "
                "the town is already in the two columns marked <i>your code</i> "
                "— but read your own sheet first, or there is nothing to mark.",
                INK,
            )
        elif _wrong:
            _verdict = note(
                f"<b>{_wrong} of them disagree.</b> The machine is not "
                "automatically the one that is right: check the boxes on the "
                "drawing before you believe it. What it cannot be is a "
                "different town — you built this one out of your own rule, and "
                "it came out with 32 friendships and 4 friends each.",
                RUST,
            )
        else:
            _verdict = note(
                "<b>Your pencil and your code agree.</b> Two friendships out of "
                "thirty-two — six per cent more wire — and the average fell by a "
                "quarter. The <i>furthest away</i> line is worth a look too: "
                "before the shortcuts three people were tied at the far side, "
                "afterwards only two are, and they are the two the shortcuts "
                "missed.",
                BLUE,
            )
        _out = mo.vstack(
            [
                mo.hstack(_cards, widths=[1, 1], align="start"),
                mo.Html(
                    ring_svg(
                        TOWN_N,
                        _base + TOWN_SHORTCUTS,
                        extra=TOWN_SHORTCUTS,
                        size=300,
                    )
                ),
                _verdict,
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 4 · Pairs of friends, in the small town

    Pick a person. Their friends light up, every **pair** of their friends is
    drawn as a dashed line, and the pairs who really are friends go solid.
    """)
    return


@app.cell(hide_code=True)
def _():
    who = mo.ui.slider(0, DEMO_N - 1, value=4, label="person", show_value=True)
    who
    return (who,)


@app.cell(hide_code=True)
def _(who):
    _A = plain_adjacency(DEMO_EDGES, DEMO_N)
    _nbrs = sorted(int(v) for v in np.flatnonzero(_A[who.value]))
    _pairs = [(a, b) for x, a in enumerate(_nbrs) for b in _nbrs[x + 1 :]]
    _real = [(a, b) for a, b in _pairs if _A[a, b]]
    _fills = {who.value: RUST}
    _fills.update({v: BLUE for v in _nbrs})
    two_col(
        demo_svg(fills=_fills, lit_edges=_real, faint_edges=_pairs),
        f'<div style="font-family:{SANS};font-size:16px;color:{INK}">'
        f'<div style="margin:6px 0"><span style="opacity:0.6">friends of '
        f'{who.value}</span>&nbsp; <b style="font-family:{MONO}">{_nbrs}</b></div>'
        f'<div style="margin:6px 0"><span style="opacity:0.6">pairs of them'
        f'</span>&nbsp; <b style="font-family:{MONO}">{len(_pairs)}</b></div>'
        f'<div style="margin:6px 0"><span style="opacity:0.6">pairs who are '
        f'friends</span>&nbsp; <b style="font-family:{MONO};color:{RUST}">'
        f"{len(_real)}</b></div>"
        + big(
            "fraction",
            f"{len(_real)}/{len(_pairs)}" if _pairs else "—",
            BLUE,
        )
        + "</div>",
        left_basis=220,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ The fraction, as a rule

    What the slider just did, written as a formula. Person $i$ has $k_i$
    friends. Count how many of the pairs among those friends are friends with
    each other — call it $L_i$, the solid lines in the picture — and divide by
    how many pairs there were to begin with:

    $$C_i \;=\; \frac{L_i}{\binom{k_i}{2}} \;=\; \frac{L_i}{k_i\,(k_i - 1)/2}$$

    $\binom{k_i}{2}$ is every dashed line in the picture, solid or not.
    $C_i = 1$ means all of person $i$'s friends know each other, and
    $C_i = 0$ means none of them do.

    The loop over the pairs is written for you — `itertools.combinations` hands
    you each pair of `i`'s friends exactly once, one per dashed line.
    **Two lines are yours.**

    `A` is the town's friendship table: `A[a, b]` is `1` when `a` and `b` are
    friends and `0` when they are not.
    """)
    return


@app.function
def local_clustering(A, i):
    """The fraction of person i's friend-pairs who are friends with each other.

    A  the town's friendship table. A[a, b] is 1 when a and b are friends.
    i  the person to look at.
    """
    import itertools

    import numpy as np

    nbrs = np.flatnonzero(A[i])       # everybody i is friends with
    k = len(nbrs)
    if k < 2:                         # fewer than two friends, so no pairs
        return 0.0

    links = 0
    for a, b in itertools.combinations(nbrs, 2):   # each pair of i's friends
        if ...:  # ✍️ replace the ... — are a and b friends with each other?
            links += 1

    pairs = ...  # ✍️ replace the ... — how many pairs do k friends make?
    return links / pairs


@app.cell(hide_code=True)
def _():
    _A = plain_adjacency(DEMO_EDGES, DEMO_N)
    _want = [round(kit_local_clustering(_A, i), 4) for i in range(DEMO_N)]
    try:
        _got = [round(float(local_clustering(_A, i)), 4) for i in range(DEMO_N)]
    except Exception:
        _got = None
    _ok = _got == _want
    if _ok:
        _msg = "<b>Correct</b> — the same fractions the slider counted."
    elif _got is None:
        _msg = (
            "Not yet — the two blanks are still <code>...</code>, so the last "
            "line has nothing to divide."
        )
    else:
        _bad = next(i for i in range(DEMO_N) if _got[i] != _want[i])
        _msg = (
            f"Not yet — you give person <code>{_bad}</code> "
            f"<b>{_got[_bad]}</b> where the slider counted <b>{_want[_bad]}</b>."
            + (
                " That is exactly double, so <code>pairs</code> is counting "
                "each pair twice: <code>combinations</code> already hands you "
                "each one once, which is what the <code>/ 2</code> is for."
                if _got[_bad] and abs(_got[_bad] - 2 * _want[_bad]) < 1e-6
                else ""
            )
        )
    verdict(_ok, _msg, _msg)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### igraph has this one too

    You wrote the loop because $C_i$ is the thing Part 3 was about, and a
    number you have counted by hand once is a number you can trust. Now that it
    is counted, here is the call you would reach for on any other day:

    ```python
    g.transitivity_local_undirected(mode="zero")
    ```

    It returns $C_i$ for **every** person at once, as a list in person order —
    not one person at a time, the way yours takes an `i`.
    ([docs](https://python.igraph.org/en/stable/api/igraph.GraphBase.html#transitivity_local_undirected))

    `mode="zero"` is the part worth knowing. Somebody with fewer than two
    friends has no pairs, so $C_i$ is a fraction with nothing underneath it.
    Left alone igraph hands back `nan` for those people; `mode="zero"` says to
    call it 0 instead, which is the choice your own function makes on its
    `k < 2` line.

    **Run the cell below** and read it against your own answers underneath.
    """)
    return


@app.cell
def _():
    # ▶ Try it. Change the town if you like — DEMO_EDGES is the seven-person
    #   one drawn above, and ring_edges(16, 2) is your Ringville.
    g_clust = igraph.Graph(n=DEMO_N, edges=DEMO_EDGES)
    g_clust.transitivity_local_undirected(mode="zero")
    return


@app.cell(hide_code=True)
def _():
    _g = igraph.Graph(n=DEMO_N, edges=DEMO_EDGES)
    _theirs = _g.transitivity_local_undirected(mode="zero")
    _A = plain_adjacency(DEMO_EDGES, DEMO_N)
    try:
        _yours = [float(local_clustering(_A, i)) for i in range(DEMO_N)]
    except Exception:
        _yours = None
    if _yours is None:
        _out = note(
            "igraph's answer is above. Yours will appear beside it once the two "
            "blanks in <code>local_clustering</code> are filled in.",
            INK,
        )
    else:
        _rows = "".join(
            f'<tr><td style="padding:2px 14px 2px 0;opacity:0.55">person {i}'
            "</td>"
            f'<td style="padding:2px 14px 2px 0">yours '
            f'<b style="color:{BLUE}">{_yours[i]:.3f}</b></td>'
            f'<td style="padding:2px 14px 2px 0">igraph '
            f'<b style="color:{BLUE}">{_theirs[i]:.3f}</b></td>'
            f'<td style="padding:2px 0;color:'
            f'{BLUE if abs(_yours[i] - _theirs[i]) < 1e-9 else RUST}">'
            f'{"✓" if abs(_yours[i] - _theirs[i]) < 1e-9 else "✗"}</td></tr>'
            for i in range(DEMO_N)
        )
        _same = all(abs(a - b) < 1e-9 for a, b in zip(_yours, _theirs))
        _out = mo.vstack(
            [
                mo.Html(
                    f'<table style="font-family:{SANS};font-size:15px;'
                    f'border-collapse:collapse">{_rows}</table>'
                ),
                note(
                    "<b>Same seven numbers.</b> Which is the point: the library "
                    "is not doing anything you have not just done by hand, it is "
                    "only doing it for the whole town in one line."
                    if _same
                    else "Your loop and igraph disagree, so one of them is not "
                    "counting what you think. Go back to the picture above and "
                    "count one person's dashed and solid lines by eye.",
                    BLUE if _same else RUST,
                ),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    if not (town_ready(ring_edges) and clustering_ready(local_clustering)):
        _out = WAITING
    else:
        _A = plain_adjacency(list(ring_edges(TOWN_N, TOWN_HALF)), TOWN_N)
        _c = [local_clustering(_A, i) for i in range(TOWN_N)]
        _out = mo.vstack(
            [
                mo.Html(
                    big("every person in ringville", f"{_c[0]:.2f}", BLUE)
                    + f'<div style="font-family:{SANS};font-size:16px;color:{INK}">'
                    f"lowest {min(_c):.2f}, highest {max(_c):.2f} — "
                    "which is the darkening you did in Part 3, for all sixteen of them at once."
                    "</div>"
                ),
                note(
                    "Nobody in this town is special, and nothing here mentions "
                    "<b>16</b>. Change <code>TOWN_N</code> to 10,000 and the "
                    "answer does not move — which is Question 5(a), and the "
                    "reason a lattice's clustering is a property of "
                    "<code>half</code> and of nothing else.",
                    BLUE,
                ),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 5 · Turn the dial

    Question 6(b) moved one friendship. Do that to **every** friendship with
    probability `p`, and you have the model the module is named after: `p = 0`
    is Ringville, `p = 1` is a town wired uniformly at random, and the interesting
    part is in between.

    Forty people here, so the picture stays legible and the dial stays a dial.
    """)
    return


@app.cell(hide_code=True)
def _():
    dial = mo.ui.slider(
        steps=[0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0],
        value=0.0,
        label="p",
        show_value=True,
    )
    dial
    return (dial,)


@app.cell(hide_code=True)
def _(dial):
    if not (distances_ready(distances_from) and clustering_ready(local_clustering)):
        _out = WAITING
    else:
        _n = 40
        _edges = watts_strogatz(_n, 2, dial.value, seed=11)
        _A = plain_adjacency(_edges, _n)
        _moved = sorted(
            {tuple(sorted(e)) for e in _edges}
            - {tuple(sorted(e)) for e in kit_ring(_n, 2)}
        )
        _L = mean_distance(_A, distances_from)
        _C = mean_clustering(_A, local_clustering)
        _out = two_col(
            ring_svg(_n, _edges, size=300, labels=False, extra=_moved),
            big("average handshakes  L", f"{_L:.2f}", RUST)
            + big("friends who know each other  C", f"{_C:.2f}", BLUE)
            + f'<div style="font-family:{SANS};font-size:15px;opacity:0.65;'
            f'color:{INK}">{len(_moved)} of {len(_edges)} friendships moved'
            "</div>",
            left_basis=300,
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### The whole sweep

    Both numbers, over the whole dial, each divided by its value at `p = 0` so
    they share an axis. Five hundred people this time — forty is too few for
    `L` to have anywhere to fall. **This is the figure the 1998 paper is famous
    for, and it is coming out of your two functions.**
    """)
    return


@app.cell(hide_code=True)
def _():
    if not (distances_ready(distances_from) and clustering_ready(local_clustering)):
        _out = WAITING
    else:
        _n, _reps = 500, 2
        _ps = [0.0004 * (2500 ** (k / 13)) for k in range(14)]
        _A0 = plain_adjacency(kit_ring(_n, 2), _n)
        _L0 = mean_distance(_A0, distances_from)
        _C0 = mean_clustering(_A0, local_clustering)
        _Ls, _Cs = [], []
        for _p in _ps:
            _l, _c = [], []
            for _r in range(_reps):
                _Ap = plain_adjacency(watts_strogatz(_n, 2, _p, seed=100 * _r + 3), _n)
                _l.append(mean_distance(_Ap, distances_from))
                _c.append(mean_clustering(_Ap, local_clustering))
            _Ls.append(float(np.mean(_l)) / _L0)
            _Cs.append(float(np.mean(_c)) / _C0)
        with plt.rc_context({"path.sketch": (1.4, 80, 2)}):
            _fig, _ax = plt.subplots(figsize=(6.4, 3.9))
            _fig.patch.set_facecolor(PAPER)
            _ax.set_facecolor(PAPER)
            _ax.semilogx(_ps, _Cs, "o-", color=BLUE, lw=2, ms=5, label="C(p) / C(0)")
            _ax.semilogx(_ps, _Ls, "s-", color=RUST, lw=2, ms=5, label="L(p) / L(0)")
            _ax.axvspan(0.002, 0.05, color=BLUE, alpha=0.08, lw=0)
            _ax.set_xlabel("p — chance a friendship is moved", color=INK)
            _ax.set_ylim(-0.03, 1.05)
            _ax.legend(frameon=False)
            for _s in ("top", "right"):
                _ax.spines[_s].set_visible(False)
            _ax.tick_params(colors=INK)
        plt.close(_fig)
        _out = _fig
    _out
    return


@app.cell(hide_code=True)
def _():
    note(
        "The shaded band is the whole point. <b>L has already fallen off a "
        "cliff there and C has barely moved</b> — a handful of moved "
        "friendships buys nearly all of the short paths and costs almost none "
        "of the triangles, which is Question 6(c) drawn as a picture. And it is "
        "a wide band: you do not have to tune anything to land in it, which is "
        "why so many real networks do.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 6 · Finished early? Break the standard test

    Everything below is extra. The lab proper ends above.

    The usual way to certify a small world is one number,

    $$\sigma = \frac{C / C_{\text{rand}}}{L / L_{\text{rand}}},$$

    where the *rand* pair are what the same friendships would give if they were
    thrown in a hat: $C_{\text{rand}} = k/n$ and $L_{\text{rand}} = \ln n / \ln
    k$. More clustered than a hat-drawn town, and no further across, means
    $\sigma > 1$.

    Below, **your** two functions compute $\sigma$ for a plain ring — one
    thousand people, four friends each, and **not one shortcut anywhere**. Drag
    `n` and watch what it says.

    *(Sixteen people is the right size to count by hand and the wrong size to
    test an index on: at n = 16 every town in this module scores about 1.5 and
    nothing can be told apart. That is worth knowing on its own.)*
    """)
    return


@app.cell(hide_code=True)
def _():
    nslider = mo.ui.slider(
        steps=[100, 200, 500, 1000, 2000, 4000], value=1000, label="n", show_value=True
    )
    nslider
    return (nslider,)


@app.cell(hide_code=True)
def _(nslider):
    if not (distances_ready(distances_from) and clustering_ready(local_clustering)):
        _out = WAITING
    else:
        _n = nslider.value
        _m = measure(
            plain_adjacency(kit_ring(_n, 2), _n), local_clustering, distances_from
        )
        _s = sigma(_m)
        _out = mo.vstack(
            [
                mo.Html(
                    big(f"sigma, plain ring of {_n}", f"{_s:.2f}")
                    + f'<div style="font-family:{SANS};font-size:16px;color:{INK}">'
                    f"C = {_m.C:.3f} against C<sub>rand</sub> = {_m.C_rand:.4f}"
                    "&nbsp;&nbsp;·&nbsp;&nbsp; "
                    f"L = {_m.L:.1f} against L<sub>rand</sub> = {_m.L_rand:.2f}"
                    "</div>"
                ),
                note(
                    "Your own code has just certified a town with <b>zero</b> "
                    "shortcuts as a strong small world — and the bigger you make "
                    "the town, the <i>more</i> sure it gets. Something is wrong "
                    "with the number, not with the town.",
                    RUST,
                ),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Why — as a formula in `n`

    **Question**: your own code says a town with no shortcuts is a small world,
    and says it louder as the town grows. Show why, as a formula in `n`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.accordion(
        {
            "Hint 1": mo.md(
                "Write all four quantities as formulas in `n`: `C`, `L`, "
                "`C_rand`, `L_rand`. If you cannot see one of them, move the "
                "`n` slider above and read it off."
            ),
            "Hint 2": mo.md(
                "Of those four, which one has **no `n` in it at all**? Which "
                "one grows only like **`ln n`**?"
            ),
            "Hint 3": mo.md(
                "Write the top of the fraction, `C / C_rand`, as a formula in "
                "`n`. Then the bottom, `L / L_rand`. Then divide."
            ),
            "The answer": mo.md(
                r"""
$$C = \tfrac12,\qquad L \approx \tfrac{n}{8},\qquad
C_{\text{rand}} = \tfrac{k}{n},\qquad L_{\text{rand}} \approx \tfrac{\ln n}{\ln k}$$

$$\frac{C}{C_{\text{rand}}} = \frac{n}{8},\qquad
\frac{L}{L_{\text{rand}}} = \frac{n}{8}\cdot\frac{\ln k}{\ln n},\qquad
\sigma = \frac{n/8}{(n/8)(\ln k / \ln n)} = \frac{\ln n}{\ln k}$$

The `n` **cancels exactly**. A ring is $n/8$ times more clustered than a
hat-drawn town *and* $n/8$ times further across, and $\sigma$ divides one by
the other — so it has measured nothing about this town at all. What survives
the cancellation is the leftover $\ln n / \ln k$, and it is there only because
a hat-drawn town's paths grow like $\ln n$: so slowly that the ring's enormous
path-length penalty gets discounted by that factor, and the clustering side
wins by it.

Which means: **any** network whose clustering does not fall away with `n`
scores $\sigma > 1$ automatically, shortcuts or no shortcuts. A ring's
$C = 1/2$ is exactly that. $\sigma$ was certifying that `C` is constant, not
that shortcuts exist.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Your formula against your code
    """)
    return


@app.cell(hide_code=True)
def _():
    if not (distances_ready(distances_from) and clustering_ready(local_clustering)):
        _out = WAITING
    else:
        _ns = [100, 200, 400, 800, 1600, 3200]
        _meas, _pred = [], []
        for _n in _ns:
            _m = measure(
                plain_adjacency(kit_ring(_n, 2), _n), local_clustering, distances_from
            )
            _meas.append(sigma(_m))
            _pred.append(math.log(_n) / math.log(4))
        with plt.rc_context({"path.sketch": (1.4, 80, 2)}):
            _fig, _ax = plt.subplots(figsize=(6.0, 3.5))
            _fig.patch.set_facecolor(PAPER)
            _ax.set_facecolor(PAPER)
            _ax.semilogx(_ns, _meas, "o", color=RUST, ms=8, label="your code")
            _ax.semilogx(_ns, _pred, "-", color=BLUE, lw=2, label=r"$\ln n / \ln k$")
            _ax.axhline(1, color=INK, lw=1, ls=":", alpha=0.5)
            _ax.set_xlabel("n — people in the plain ring", color=INK)
            _ax.set_ylabel(r"$\sigma$", color=INK)
            _ax.legend(frameon=False)
            for _s in ("top", "right"):
                _ax.spines[_s].set_visible(False)
            _ax.tick_params(colors=INK)
        plt.close(_fig)
        _out = _fig
    _out
    return


@app.cell(hide_code=True)
def _():
    note(
        "Your measurement lands on your formula, and the dotted line at "
        "<b>σ = 1</b> is the threshold everybody quotes. A shortcut-free ring "
        "clears it at every size and clears it by more the bigger it gets.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Build a test that does not fall for it

    **Question**: in one sentence, what did $\sigma$ never look at? Then build
    something that does.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.accordion(
        {
            "Hint": mo.md(
                "$\\sigma$ compares the town to a hat-drawn town, and to "
                "**nothing else**. That a plain ring reaches high clustering "
                "with *zero* shortcuts never enters the calculation — there is "
                "no yardstick in it for the other end of the range."
            )
        }
    )
    return


@app.function
def my_index(m):
    """Your own small-world test. Bigger must mean "more of a small world".

    `m` carries six numbers, all measured with your two functions:

        m.C       m.L           this town
        m.C_rand  m.L_rand      the same friendships thrown in a hat
        m.C_latt  m.L_latt      a plain ring with the same number of friends

    TASK: return one number. The check below never looks at your formula. It
    runs it on four towns and asks two things of the answers.
    """
    ...


@app.cell(hide_code=True)
def _():
    if not (distances_ready(distances_from) and clustering_ready(local_clustering)):
        _out = WAITING
    else:

        def _score(edges, n):
            return float(
                my_index(
                    measure(
                        plain_adjacency(edges, n), local_clustering, distances_from
                    )
                )
            )

        try:
            _n = 1000
            _ring = _score(kit_ring(_n, 2), _n)
            _sw = _score(watts_strogatz(_n, 2, 0.05, seed=5), _n)
            _rand = _score(watts_strogatz(_n, 2, 1.0, seed=5), _n)
            _small = _score(kit_ring(250, 2), 250)
            _large = _score(kit_ring(2000, 2), 2000)
            _err = None
        except Exception as _e:  # a blank cell lands here first
            _err = _e

        if _err is not None:
            _out = note(
                "Not yet — <code>my_index</code> returns nothing to compare "
                f"(<code>{type(_err).__name__}</code>).",
                RUST,
            )
        else:
            _grows = _large > _small + 1e-9
            _ranks = _sw > _ring and _sw > _rand
            _rows = "".join(
                f'<div style="margin:6px 0;font-family:{SANS};font-size:16px">'
                f'<span style="opacity:0.6">{_k}</span>&nbsp; '
                f'<b style="font-family:{MONO};color:{RUST}">{_v:+.3f}</b></div>'
                for _k, _v in [
                    ("plain ring, n=1000", _ring),
                    ("p = 0.05, n=1000", _sw),
                    ("hat-drawn, n=1000", _rand),
                    ("plain ring, n=250", _small),
                    ("plain ring, n=2000", _large),
                ]
            )
            if _grows:
                _msg = (
                    "<b>Not yet.</b> Your index scores a shortcut-free ring "
                    f"<b>{_small:+.3f}</b> at n = 250 and <b>{_large:+.3f}</b> "
                    "at n = 2000 — it likes the ring <i>more</i> as the ring "
                    "gets bigger. That is σ's bug, not a repair for it."
                )
            elif not _ranks:
                _msg = (
                    "<b>Not yet.</b> The town at p = 0.05 has to beat both ends: "
                    f"it scores <b>{_sw:+.3f}</b> against <b>{_ring:+.3f}</b> "
                    f"for the plain ring and <b>{_rand:+.3f}</b> for the "
                    "hat-drawn town."
                )
            else:
                _msg = (
                    "<b>That works.</b> The town in the middle wins, and a "
                    "bigger shortcut-free ring does not score better than a "
                    "small one. σ fails the second of those, whatever size you "
                    "test it at."
                )
            _out = mo.vstack(
                [mo.Html(_rows), note(_msg, BLUE if not _grows and _ranks else RUST)]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.accordion(
        {
            "The two published repairs": mo.md(
                r"""
Both add a **second** yardstick — a lattice, at the other end of the range from
the hat-drawn graph — because "small world" was always a claim about the
*middle* of a range, and $\sigma$ only ever looked at one end.

- **$\omega$** (Telesford et al. 2011): $\;\omega = L_{\text{rand}}/L - C/C_{\text{latt}}$.
  $-1$ is a lattice, $+1$ is random, $0$ is a small world; it stays inside
  $[-1, +1]$ whatever `n` does. As a score where bigger is better, use
  $-\lvert\omega\rvert$.
- **SWI** (Neal 2017):
  $\;\text{SWI} = \frac{L - L_{\text{latt}}}{L_{\text{rand}} - L_{\text{latt}}}
  \cdot \frac{C - C_{\text{rand}}}{C_{\text{latt}} - C_{\text{rand}}}$, from 0 to 1.

At n = 1000, k = 4:

| town | σ | ω | SWI |
|---|---|---|---|
| plain ring, p = 0 | **4.96** ← passes | −0.96 ✓ | 0.00 ✓ |
| p = 0.05 | 47.7 | −0.41 | **0.81** ← largest |
| p = 0.2 | 48.1 | 0.21 | 0.51 |
| hat-drawn, p = 1 | 0.47 ✓ | 0.93 ✓ | 0.00 ✓ |

The same network is a *strong small world* to σ and an *almost perfect
lattice* to ω, and as `n` grows the two run in opposite directions.

**And the repair has a price.** $C_{\text{latt}}$ and $L_{\text{latt}}$ have to
come from somewhere. Here the town *is* a lattice, so `measure` gets them for
free. On a real network you have to build a lattice with the same degree
sequence yourself — lay the nodes on a ring and swap edges until they are as
short as they go — which is not a small job, and is part of why σ is still the
one people quote.

*One more, for real data.* $C_{\text{rand}} = k/n$ is the Erdős–Rényi value,
and ER gives everybody roughly the same number of friends. Real networks do
not, and a spread of degrees raises clustering all by itself — so part of
"more clustered than random" is the degree sequence, not the structure. The
honest baseline keeps the degrees and shuffles only who is joined to whom.
Nothing in this notebook shows it, because every town here is 4-regular and
keeping the degrees changes nothing. It bites on real data.
"""
            )
        }
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
