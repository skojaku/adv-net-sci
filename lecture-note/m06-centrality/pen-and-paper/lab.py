# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# The Module 6 lab, done alone at a laptop: the sheet by machine, then Rome.
#
# The pen-and-paper sheet ("Who's the Big Cheese in the University Clubs?")
# ranks thirteen students four different ways with a pencil: count the
# friends, measure the distances, ask who is indispensable, pass scores
# around. This notebook runs the same four questions by machine, checks the
# pencil answers, and then asks the empire the same four questions — the
# course's twelve-city Roman map, where the Golden Milestone's city takes
# every crown but one.
#
# The notebook is in three layers, and only the top one is a student's:
#
#   * the kit     -- everything in the setup block: the SVG drawing, the two
#                   networks, the answers the checks mark against. Hidden.
#   * the cells   -- the warm-up, the figures, the Rome map, the cut
#                   experiment. They run themselves.
#   * the blanks  -- five cells that say `...`: build the club network, then
#                   Question 4's count, Question 5's average distance,
#                   Question 6's pairs cut off, and Question 7's game played
#                   forever. All typed from a block on the page that cannot
#                   be selected, so it cannot be pasted.
#
# Rules this file obeys, learned on m01 and m02:
#
#   * The teaching figure is not the student's task. The warm-up and every
#     worked figure run on the five-node network from the lecture notes (a
#     triangle and a tail, numbered from 0), never on the club network —
#     because a coloured-in club network is Question 4's answer sitting on
#     the screen. The club network appears as a picture with the students
#     numbered, and no cell anywhere prints its edge list.
#   * The checks mark against answers held in the hidden kit, so unfolding a
#     marking cell does not hand over the answer it marks against, and each
#     check names the mistake rather than saying "wrong".
#   * A waiting card, not an exception, for anything downstream of a blank.
#   * The stylesheet travels inside the file. molab ignores css_file
#     (marimo-team/marimo#8467), so lecture-hall.css is carried here as
#     base64 and injected by the first cell. Refresh it with
#     `python tools/build_lab_notebooks.py m06-centrality` after editing it.
#   * Nothing is fetched at run time. Rome's twelve cities, their positions
#     and their roads are typed in below: they follow the course's Module 6
#     map (slides/m06/figures/verify_numbers.py), which records every edge
#     as a documented Roman road or sea lane. A bigger Roman road network
#     lives in the repository under data/roman-roads; this lab does not use
#     it.
#   * igraph is pinned to the version the coding notebooks already use
#     (python-igraph==0.11.9), so the idiom a student meets here is the one
#     they meet there.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import base64
    import html
    import inspect as _inspect

    import igraph
    import marimo as mo
    import numpy as np

    # The look travels inside the notebook rather than beside it. molab ignores
    # a notebook's css_file setting (marimo-team/marimo#8467) and this file is
    # uploaded there on its own, so lecture-hall.css is carried here, base64 so
    # that no quote or backslash in it can break the Python, and injected as a
    # <style> tag by the first cell. Refresh it with tools/build_lab_notebooks.py.
    LECTURE_HALL_CSS_B64 = "LyogTGVjdHVyZSBIYWxsIOKAlCBtYXJpbW8gY3VzdG9tIENTUywgZHJhd24gYnkgaGFuZAogICBVc2FnZTogcHV0IHRoaXMgbmV4dCB0byB5b3VyIG5vdGVib29rIGFuZCBhZGQgdG8gdGhlIG5vdGVib29rJ3MgY29uZmlnOgogICAgIFtkaXNwbGF5XSBjc3NfZmlsZSA9ICJsZWN0dXJlLWhhbGwuY3NzIgogICBvciBpbiBtYXJpbW8udG9tbCB1bmRlciBbZGlzcGxheV0uCgogICBUaGUgbm90ZWJvb2sgaXMgYSBsZWN0dXJlIG5vdGUgdGhlIHN0dWRlbnQgYW5kIHRoZSB0dXRvciBmaWxsIGluIHRvZ2V0aGVyLAogICBzbyBpdCBpcyBkcmVzc2VkIGFzIG9uZTogZG90LWdyaWQgcGFwZXIsIHdvYmJseSBpbmsgYm9yZGVycywgYW5kIHNlY3Rpb24KICAgcnVsZXMgZHJhd24gd2l0aCBhIHBlbi4KCiAgIFRIRSBIQU5EIElTIElOIFRIRSBMSU5FUywgTk9UIElOIFRIRSBMRVRURVJTLiBBIGhhbmR3cml0aW5nIGZhY2UgZm9yIHRoZQogICBwcm9zZSB3YXMgdGlyaW5nIHRvIHJlYWQgb3ZlciBuaW5ldHkgbWludXRlcyBhbmQgbWFkZSB0aGUgcGFnZSBsb29rIGxpa2UgYQogICBncmVldGluZyBjYXJkIHJhdGhlciB0aGFuIGEgbGVjdHVyZSBub3RlLiBTbyB0aGUgdHlwZSBpcyBleGFjdGx5IHRoZSBjb3Vyc2UKICAgbGVjdHVyZSBub3RlJ3MgKGFkdi1uZXQtc2NpL2xlY3R1cmUtbm90ZS9zY3NzL21pbmltYWwuc2Nzcyk6IGEgc3lzdGVtIHNhbnMKICAgZm9yIHRoZSBib2R5LCBhIHN5c3RlbSBzZXJpZiBmb3IgdGhlIGhlYWRpbmdzLCAxOHB4LzEuNjUg4oCUIHRoZSBzYW1lCiAgIHJlYWRpbmcgZXhwZXJpZW5jZSBvbiBib3RoIGhhbHZlcyBvZiB0aGUgY291cnNlLiBXaGF0IHN0YXlzIGhhbmQtZHJhd24gaXMKICAgZXZlcnl0aGluZyB0aGF0IGlzIG5vdCByZWFkIGFzIGEgd29yZDogdGhlIHdhdnkgc2VjdGlvbiBydWxlcywgdGhlIHdvYmJseQogICBib3JkZXJzIGFuZCBwZW4gc2hhZG93cywgdGhlIHNrZXRjaGVkIG1hdHBsb3RsaWIgc3Ryb2tlcywgYW5kIG5ldHZpeidzCiAgIHR1cmJ1bGVudCBlZGdlcy4KCiAgIE5vIHdlYmZvbnQsIG5vIG5ldHdvcmsgcmVxdWVzdDogYSBzdHVkZW50IG9uIGEgcGxhbmUgZ2V0cyB0aGUgc2FtZSBwYWdlLAogICBhbmQgdGhlcmUgaXMgbm8gZmlyc3QtcGFpbnQgZmxhc2ggb2YgYSBmYWxsYmFjayBmYWNlLgoKICAgVGhlIGFjY2VudHMgYXJlIHRoZSBMRUNUVVJFIFNMSURFUycgYWNjZW50cywgdmVyYmF0aW0g4oCUIHRoZSBtb2R1bGUgaXMgb25lCiAgIGNvdXJzZSwgc28gdGhlIGNvbG91ciB0aGF0IG1lYW5zICJ0aGUgdGhpbmcgd2UgYXJlIGxvb2tpbmcgYXQiIGhhcyB0byBtZWFuCiAgIGl0IGluIGJvdGggaGFsdmVzLiBDaGFuZ2Ugb25lIG9mIHRoZW0gaGVyZSBhbmQgeW91IG11c3QgY2hhbmdlIGl0IGluCiAgIGFkdi1uZXQtc2NpL3NsaWRlcy9tMDIvZmlndXJlcy9tYWtlX2ZpZ3VyZXMucHkgdG9vLCBhbmQgaW4gZXZlcnkgY2VsbHMvKi5weQogICB0aGF0IGhhcmRjb2RlcyBpdCAodGhleSBhbGwgZG8sIGZvciB0aGVpciBub2RlcyBhbmQgZWRnZXMpLiAqLwoKOnJvb3QgewogIC8qIHBhbGV0dGUg4oCUIHRoZSB0aHJlZSBhY2NlbnRzIGNvbWUgZnJvbSB0aGUgc2xpZGUgZGVjawogICAgIChtYWtlX2ZpZ3VyZXMucHk6IEFDQ0VOVCAvIEFDQ0VOVDIgLyBBQ0NFTlQzKSwgYW5kIHRoZSBwcmVtYWRlIGNlbGxzCiAgICAgaGFyZGNvZGUgdGhlIHNhbWUgaGV4ZXMgZm9yIHRoZWlyIG5vZGVzIGFuZCBlZGdlcywgc28gYSByZXBhaW50IGhlcmUKICAgICBkZXN5bmNzIGJvdGguIFdoYXQgaXMgTk9UIHRoZSBzbGlkZXMnIGlzIHRoZSBwYXBlcjogd2hpdGUgYmVjYW1lIHdhcm0sCiAgICAgYW5kIHRoZSBwZW5jaWwgcnVsZSAoLS1saC1ydWxlKSBpcyBhIG5ldyB0b2tlbiByYXRoZXIgdGhhbiBhIHJlcGFpbnQgb2YKICAgICAtLWxoLWxpbmUsIHdoaWNoIGlzIGEgbm9kZSBmaWxsIGluIGNwMiBhbmQgY3A1LiAqLwogIC0tbGgtcGFwZXI6ICAgI0ZGRkRGNzsKICAtLWxoLWNhcmQ6ICAgICNGRkZGRkY7CiAgLS1saC1zdXJmYWNlOiAjRjZGMkU5OwogIC0tbGgtbGluZTogICAgI0U0RTZFQTsKICAtLWxoLXJ1bGU6ICAgICNEOUQyQzI7CiAgLS1saC1pbms6ICAgICAjMUQxRTIxOwogIC0tbGgtaW5rLTI6ICAgIzM1MzczQzsKICAtLWxoLW11dGVkOiAgICM2QTZENzU7CiAgLS1saC1ibHVlOiAgICAjMjIzMzZCOwogIC0tbGgtYmx1ZS0yOiAgIzM5NTlBNjsKICAtLWxoLXJ1c3Q6ICAgICNCMTQ0MzQ7CgogIC8qIHR5cGUg4oCUIHRoZSBsZWN0dXJlIG5vdGUncyB0aHJlZSBzdGFja3MsIHZlcmJhdGltLiBBbGwgZnJvbSB0aGUgc3lzdGVtOgogICAgIG5vdGhpbmcgaGVyZSBpcyBmZXRjaGVkLiAqLwogIC0tbGgtc2VyaWY6ICAgIklvd2FuIE9sZCBTdHlsZSIsICJQYWxhdGlubyBMaW5vdHlwZSIsIFBhbGF0aW5vLAogICAgICAgICAgICAgICAgIkJvb2sgQW50aXF1YSIsICJIb2VmbGVyIFRleHQiLCBHZW9yZ2lhLAogICAgICAgICAgICAgICAgIlRpbWVzIE5ldyBSb21hbiIsIHNlcmlmOwogIC0tbGgtc2FuczogICAgc3lzdGVtLXVpLCAtYXBwbGUtc3lzdGVtLCAiU2Vnb2UgVUkiLCBSb2JvdG8sCiAgICAgICAgICAgICAgICAiSGVsdmV0aWNhIE5ldWUiLCAiTm90byBTYW5zIiwgIkxpYmVyYXRpb24gU2FucyIsIEFyaWFsLAogICAgICAgICAgICAgICAgc2Fucy1zZXJpZjsKICAtLWxoLW1vbm86ICAgIHVpLW1vbm9zcGFjZSwgU0ZNb25vLVJlZ3VsYXIsICJTRiBNb25vIiwgTWVubG8sIENvbnNvbGFzLAogICAgICAgICAgICAgICAgIkxpYmVyYXRpb24gTW9ubyIsIG1vbm9zcGFjZTsKICAvKiBUaGUgb25lIGhhbmQtd3JpdHRlbiBmYWNlIG9uIHRoZSBwYWdlLCBhbmQgaXQgd3JpdGVzIGV4YWN0bHkgb25lIHRoaW5nOgogICAgIHRoZSBzdHVkZW50J3Mgb3duIGFuc3dlcnMsIGluc2lkZSB0aGUgZm9sZC4gUHJpbnRlZCBub3RlLCBoYW5kd3JpdHRlbgogICAgIG1hcmdpbiDigJQgdGhlIGRpZmZlcmVuY2UgYmV0d2VlbiB0aGUgdHdvIGlzIHRoZSBwb2ludC4gU3lzdGVtIGZhY2VzIG9ubHksCiAgICAgbGlrZSBldmVyeXRoaW5nIGVsc2UgaGVyZTogbWFjT1Mgc2hpcHMgdGhlIGZpcnN0IHR3bywgV2luZG93cyB0aGUgbmV4dAogICAgIHR3bywgYGN1cnNpdmVgIGNhdGNoZXMgdGhlIHJlc3QuICovCiAgLS1saC1oYW5kOiAgICAiQ2hhbGtib2FyZCBTRSIsICJCcmFkbGV5IEhhbmQiLCAiU2Vnb2UgUHJpbnQiLAogICAgICAgICAgICAgICAgIkNvbWljIFNhbnMgTVMiLCBjdXJzaXZlOwoKICAvKiB0aGUgaGFuZC1kcmF3biBraXQ6IHR3byByb3VuZGluZyBzZXRzLCBhbHRlcm5hdGVkIHNvIG5vIHR3byBib3hlcyBvbiB0aGUKICAgICBwYWdlIGhhdmUgdGhlIHNhbWUgY29ybmVycywgYW5kIG9uZSBpbmsgc2hhZG93IHRoYXQgZmFrZXMgYSBzZWNvbmQgcGFzcwogICAgIG9mIHRoZSBwZW4uICovCiAgLS1saC13b2JibGU6ICAgMTRweCA2cHggMTZweCA4cHggLyA4cHggMTZweCA2cHggMTRweDsKICAtLWxoLXdvYmJsZS0yOiA2cHggMTZweCA4cHggMTRweCAvIDE2cHggNnB4IDE0cHggOHB4OwogIC0tbGgtcGVuOiAgICAgIDNweCA0cHggMCAtMXB4IHJnYmEoMzUsIDM0LCA0MywgMC4xNik7CiAgLS1saC1wZW4tc29mdDogMnB4IDNweCAwIC0xcHggcmdiYSgzNSwgMzQsIDQzLCAwLjEyKTsKCiAgLyogYSB3YXZ5IHN0cm9rZSwgdXNlZCBmb3IgdW5kZXJsaW5lcyBhbmQgdGFibGUgcnVsZXMgKi8KICAtLWxoLXN0cm9rZTogdXJsKCJkYXRhOmltYWdlL3N2Zyt4bWwsJTNDc3ZnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Zycgd2lkdGg9JzEyMCcgaGVpZ2h0PSc3JyB2aWV3Qm94PScwIDAgMTIwIDcnJTNFJTNDcGF0aCBkPSdNMSA0LjRDMjAgMS45IDQwIDYuMiA2MCAzLjcgODAgMS40IDEwMCA1LjYgMTE5IDMuMicgZmlsbD0nbm9uZScgc3Ryb2tlPSclMjNCMTQ0MzQnIHN0cm9rZS13aWR0aD0nMicgc3Ryb2tlLWxpbmVjYXA9J3JvdW5kJy8lM0UlM0Mvc3ZnJTNFIik7CiAgLS1saC1zdHJva2UtZmFpbnQ6IHVybCgiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxMjAnIGhlaWdodD0nNycgdmlld0JveD0nMCAwIDEyMCA3JyUzRSUzQ3BhdGggZD0nTTEgNC40QzIwIDEuOSA0MCA2LjIgNjAgMy43IDgwIDEuNCAxMDAgNS42IDExOSAzLjInIGZpbGw9J25vbmUnIHN0cm9rZT0nJTIzRDlEMkMyJyBzdHJva2Utd2lkdGg9JzInIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcvJTNFJTNDL3N2ZyUzRSIpOwoKICAvKiBtYXJpbW8gdG9rZW5zICovCiAgLS1iYWNrZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1pbmspOwogIC0tY2FyZDogdmFyKC0tbGgtY2FyZCk7CiAgLS1jYXJkLWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1wb3BvdmVyOiB2YXIoLS1saC1jYXJkKTsKICAtLXBvcG92ZXItZm9yZWdyb3VuZDogdmFyKC0tbGgtaW5rKTsKICAtLW11dGVkOiB2YXIoLS1saC1zdXJmYWNlKTsKICAtLW11dGVkLWZvcmVncm91bmQ6IHZhcigtLWxoLW11dGVkKTsKICAtLWJvcmRlcjogdmFyKC0tbGgtbGluZSk7CiAgLS1pbnB1dDogdmFyKC0tbGgtbGluZSk7CiAgLS1yaW5nOiB2YXIoLS1saC1ibHVlKTsKICAtLXByaW1hcnk6IHZhcigtLWxoLWJsdWUpOwogIC0tcHJpbWFyeS1mb3JlZ3JvdW5kOiB2YXIoLS1saC1wYXBlcik7CiAgLS1zZWNvbmRhcnk6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tc2Vjb25kYXJ5LWZvcmVncm91bmQ6IHZhcigtLWxoLWluayk7CiAgLS1hY2NlbnQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIC0tYWNjZW50LWZvcmVncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIC0tZGVzdHJ1Y3RpdmU6IHZhcigtLWxoLXJ1c3QpOwogIC0tZGVzdHJ1Y3RpdmUtZm9yZWdyb3VuZDogdmFyKC0tbGgtcGFwZXIpOwogIC0tcmFkaXVzOiAzcHg7CgogIC0tdGV4dC1mb250OiB2YXIoLS1saC1zYW5zKTsKICAtLWhlYWRpbmctZm9udDogdmFyKC0tbGgtc2VyaWYpOwogIC0tY29kZS1mb250OiB2YXIoLS1saC1tb25vKTsKfQoKLyogLS0tLS0tLS0tLSBwYWdlIC0tLS0tLS0tLS0gKi8KCi8qIERvdC1ncmlkLCBub3QgcnVsZWQgbGluZXM6IHRoZSBzYW1lICJ0aGlzIGlzIGEgc2tldGNoYm9vayIgc2lnbmFsLCBidXQgaXQKICAgZG9lcyBub3QgZmlnaHQgYSBsaW5lIG9mIHByb3NlIGZvciB0aGUgc2FtZSBob3Jpem9udGFsIGJhbmQuICovCmJvZHksCiNBcHAgewogIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWxoLXBhcGVyKTsKICBiYWNrZ3JvdW5kLWltYWdlOiByYWRpYWwtZ3JhZGllbnQocmdiYSgzMSwgNTgsIDk1LCAwLjA4NSkgMXB4LCB0cmFuc3BhcmVudCAxcHgpOwogIGJhY2tncm91bmQtc2l6ZTogMjRweCAyNHB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIC13ZWJraXQtZm9udC1zbW9vdGhpbmc6IGFudGlhbGlhc2VkOwp9CgovKiAtLS0tLS0tLS0tIHByb3NlIC0tLS0tLS0tLS0gKi8KCi5tYXJrZG93biwKLnByb3NlIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgZm9udC1zaXplOiAxOHB4OwogIGxpbmUtaGVpZ2h0OiAxLjY1OwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7CiAgdGV4dC13cmFwOiBwcmV0dHk7CiAgbWF4LXdpZHRoOiA2OGNoOwp9CgovKiBUaGUgbGVjdHVyZSBub3RlJ3Mgc2VyaWYgYW5kIGl0cyBzY2FsZSDigJQgaDEgMi4wNSAvIGgyIDEuNTUgLyBoMyAxLjIyIC8KICAgaDQgMS4wMiBhZ2FpbnN0IGl0cyAxOHB4IHJvb3QuIFdyaXR0ZW4gb3V0IGluIHB4IGJlY2F1c2UgbWFyaW1vJ3Mgcm9vdAogICBzdGF5cyB0aGUgYnJvd3NlcidzIDE2cHgsIHNvIGEgcmVtIGhlcmUgd291bGQgYmUgYSBkaWZmZXJlbnQgc2l6ZSB0aGFuCiAgIHRoZSBzYW1lIHJlbSBvbiB0aGUgbm90ZS4gKi8KLm1hcmtkb3duIGgxLCAubWFya2Rvd24gaDIsIC5tYXJrZG93biBoMywgLm1hcmtkb3duIGg0LAoucHJvc2UgaDEsIC5wcm9zZSBoMiwgLnByb3NlIGgzLCAucHJvc2UgaDQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zZXJpZik7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtaW5rKTsKICBsaW5lLWhlaWdodDogMS4yNTsKICBsZXR0ZXItc3BhY2luZzogMDsKfQoKLm1hcmtkb3duIGgxLCAucHJvc2UgaDEgewogIGZvbnQtc2l6ZTogMzdweDsKICBtYXJnaW46IDAgMCAyMnB4OwogIGxldHRlci1zcGFjaW5nOiAtMC4wMWVtOwp9CgovKiBBIGNoYXB0ZXIgYnJlYWsg4oCUIG9uZSBvZiB0aGUgdHdvIHBsYWNlcyB0aGUgcGVuIHN0aWxsIHdyaXRlcy4gKi8KLm1hcmtkb3duIGgyLCAucHJvc2UgaDIgewogIGZvbnQtc2l6ZTogMjhweDsKICBtYXJnaW46IDUwcHggMCAxNnB4OwogIHBhZGRpbmctYm90dG9tOiAwLjE4ZW07CiAgYmFja2dyb3VuZC1pbWFnZTogdmFyKC0tbGgtc3Ryb2tlKTsKICBiYWNrZ3JvdW5kLXJlcGVhdDogcmVwZWF0LXg7CiAgYmFja2dyb3VuZC1wb3NpdGlvbjogbGVmdCBib3R0b207CiAgYmFja2dyb3VuZC1zaXplOiAxMjBweCA3cHg7Cn0KCi8qIEEgbm90ZSBjZWxsJ3Mgb3duIHRpdGxlIChgIyMjIPCfk48gRGlzdGFuY2UgYW5kIGF2ZXJhZ2UgcGF0aCBsZW5ndGhgKS4gSXQgaXMKICAgc2V0IGxhcmdlciB0aGFuIHRoZSBwcm9zZSBiZW5lYXRoIGl0IHNvIHRoZSBmaW5pc2hlZCBub3RlYm9vayByZWFkcyBhcyBhCiAgIHJ1biBvZiBzZWN0aW9ucywgbm90IG9uZSBsb25nIGNvbHVtbi4gKi8KLm1hcmtkb3duIGgzLCAucHJvc2UgaDMgeyBmb250LXNpemU6IDIycHg7IG1hcmdpbjogMzZweCAwIDEzcHg7IH0KCi8qIFF1aWV0ZXIgdGhhbiBoMzogc2l6ZSBhbmQgd2VpZ2h0IG9ubHksIG5ldmVyIGEgcnVsZS4gKi8KLm1hcmtkb3duIGg0LCAucHJvc2UgaDQgeyBmb250LXNpemU6IDE4cHg7IG1hcmdpbjogMjdweCAwIDlweDsgfQoKLm1hcmtkb3duIGEsIC5wcm9zZSBhIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyB0ZXh0LWRlY29yYXRpb24tY29sb3I6IHZhcigtLWxoLWxpbmUpOyB9Ci5tYXJrZG93biBhOmhvdmVyLCAucHJvc2UgYTpob3ZlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgdGV4dC1kZWNvcmF0aW9uLWNvbG9yOiBjdXJyZW50Q29sb3I7IH0KCi5tYXJrZG93biBzdHJvbmcsIC5wcm9zZSBzdHJvbmcgeyBjb2xvcjogdmFyKC0tbGgtaW5rKTsgZm9udC13ZWlnaHQ6IDcwMDsgfQoKLyogQSBxdW90ZSBjYXJyaWVzIE5PIGNocm9tZSBhdCBhbGw6IG5vIGZpbGwsIG5vIGJvcmRlciwgbm90IGV2ZW4gYSBydWxlIGluCiAgIHRoZSBtYXJnaW4g4oCUIGdyZXkgaW5rIGlzIHRoZSB3aG9sZSB0cmVhdG1lbnQuCgogICBJdCBoYXMgYmVlbiB3YWxrZWQgZG93biBvbmUgc3RlcCBhdCBhIHRpbWUgYW5kIGVhY2ggc3RlcCB3YXMgcmlnaHQuIEl0CiAgIHN0YXJ0ZWQgYXMgYSBzY3JhcCBvZiBwYXBlciBwaW5uZWQgdG8gdGhlIHBhZ2UgKGZpbGxlZCwgbmF2eS1ib3JkZXJlZCwKICAgc2hhZG93ZWQsIHRpbHRlZCBhIHF1YXJ0ZXIgZGVncmVlKSwgd2hpY2ggc2FpZCBMT09LIEFUIFRISVMgYWJvdXQgYSBsaW5lCiAgIHRoZSByZWFkZXIgaGFkIGFscmVhZHkgY2xpY2tlZCB0byBvcGVuLiBUaGVuIGEgbWFyZ2luIHJ1bGUsIHdoaWNoIHN0aWxsCiAgIGRyZXcgYSB2ZXJ0aWNhbCBsaW5lIGRvd24gYSBwYWdlIHRoYXQgaGFzIHBsZW50eS4gV2hhdCBpcyBsZWZ0IGlzIHdoYXQKICAgdGhlIHF1b3RlIGFjdHVhbGx5IGlzOiB0aGUgc3R1ZGVudCdzIG93biB3b3JkcywgaW4gdGhlIHBhZ2UncyBxdWlldCBncmV5LAogICB1bmRlciBhIGhlYWRpbmcgdGhhdCBhbHJlYWR5IG5hbWVzIHRoZW0uICM2QTZENzUgb24gd2hpdGUgaXMgNS4yOjEg4oCUCiAgIHF1aWV0IGlzIG5vdCB0aGUgc2FtZSBhcyB1bnJlYWRhYmxlLCBhbmQgdGhpcyBsaW5lIGlzIHRoZSBncmFkZWQgb25lLiAqLwoubWFya2Rvd24gYmxvY2txdW90ZSwKLnByb3NlIGJsb2NrcXVvdGUgewogIG1hcmdpbjogMS40ZW0gMDsKICBwYWRkaW5nOiAwOwogIGJhY2tncm91bmQ6IG5vbmU7CiAgYm9yZGVyOiAwOwogIGJvcmRlci1yYWRpdXM6IDA7CiAgYm94LXNoYWRvdzogbm9uZTsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGZvbnQtc3R5bGU6IG5vcm1hbDsKfQoKLyogLS0tLS0tLS0tLSB0aGUgc3R1ZGVudCdzIG93biBhbnN3ZXIsIGZvbGRlZCAtLS0tLS0tLS0tICovCgovKiBFdmVyeSBub3RlIGNlbGwgZW5kcyB3aXRoIHdoYXQgdGhlIHN0dWRlbnQgc2FpZCwgcXVvdGVkIHZlcmJhdGltLiBMZWZ0CiAgIG9wZW4gaXQgd2FzIHRoZSBsb3VkZXN0IHRoaW5nIG9uIHRoZSBwYWdlIOKAlCBhIGJvcmRlcmVkLCBzaGFkb3dlZCBzbGFiCiAgIHVuZGVyIGV2ZXJ5IHNpbmdsZSBub3RlLCBjb21wZXRpbmcgd2l0aCB0aGUgZmlndXJlIGFib3ZlIGl0IGFuZCB3aXRoIHRoZQogICBleHBsYW5hdGlvbiB0aGUgbm90ZSBleGlzdHMgdG8gZ2l2ZS4gU28gaXQgaXMgZm9sZGVkOiB0aGUgbm90ZSByZWFkcyBhcwogICB0aGUgbGVjdHVyZSBub3RlIGl0IGlzLCBhbmQgdGhlIGFuc3dlciBpcyBvbmUgY2xpY2sgYXdheS4KICAgYG1vLm1kYCByZW5kZXJzIGAvLy8gZGV0YWlscyB8IE15IGFuc3dlcmAgKyBgdHlwZTogbGgtYW5zd2VyYCBpbnRvIHRoaXMuCgogICBDbG9zZWQsIGl0IGlzIGEgZGFzaGVkIHRhYiBpbiB0aGUgbWFyZ2luIGNvbG91ciDigJQgcHJlc2VudCwgcXVpZXQsIGNsZWFybHkKICAgcHJlc3NhYmxlLiBPcGVuLCBpdCBpcyB0aGVpciB3b3JkcyBiZWhpbmQgYSBtYXJnaW4gcnVsZSwgYW5kIG5vdGhpbmcgZWxzZToKICAgYSByZWFkZXIgd2hvIGNsaWNrZWQgdG8gc2VlIHRoZSBhbnN3ZXIgZG9lcyBub3QgYWxzbyBuZWVkIGl0IGJveGVkLiAqLwovKiBtYXJpbW8gZHJlc3NlcyBFVkVSWSBgLm1hcmtkb3duIGRldGFpbHNgIGFzIGFuIGFkbW9uaXRpb24sIGFuZCB0aGVyZSBpcyBubwogICBvcHRpbmcgb3V0IGJ5IG5hbWluZyBhbiB1bmtub3duIHR5cGU6IGEgY2FyZC1jb2xvdXJlZCBiYWNrZ3JvdW5kLCBhIDZweAogICBsZWZ0IHJ1bGUsIGEgY2hldnJvbiBidWlsdCBvdXQgb2YgdHdvIHJvdGF0ZWQgYm9yZGVycyBvbiBgc3VtbWFyeTo6YmVmb3JlYCwKICAgYW5kIGEgMXJlbSBwYWQgb24gZXZlcnkgY2hpbGQgdGhhdCBpcyBub3QgdGhlIHN1bW1hcnkuIE9uIHBhcGVyLWNvbG91cmVkCiAgIHBhZ2VzIHRoYXQgY2FyZCByZWFkcyBhcyBhIGdyZXkgc2xhYiBwYXJrZWQgYmVoaW5kIHRoZSBhbnN3ZXIuIEFsbCBmb3VyIGFyZQogICB1bmRvbmUgaGVyZSDigJQgdGhpcyBmb2xkIGlzIGRyYXduIGZyb20gc2NyYXRjaCwgbm90IHRoZW1lZC4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgewogIG1hcmdpbjogMS4yZW0gMDsKICBiYWNrZ3JvdW5kOiBub25lOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwp9Ci8qIFRoZSAxcmVtIHBhZCBtYXJpbW8gcHV0cyBvbiB0aGUgcXVvdGUuIFRoZSBxdW90ZSBoYXMgaXRzIG93bi4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gKjpub3Qoc3VtbWFyeSksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+ICo6bm90KHN1bW1hcnkpIHsgcGFkZGluZzogMDsgfQoKLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeSB7CiAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgYWxpZ24taXRlbXM6IGJhc2VsaW5lOwogIGdhcDogMC40NWVtOwogIHdpZHRoOiBmaXQtY29udGVudDsKICBjdXJzb3I6IHBvaW50ZXI7CiAgcGFkZGluZzogMnB4IDEycHggNHB4OwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXNpemU6IDE0cHg7CiAgZm9udC13ZWlnaHQ6IDYwMDsKICBjb2xvcjogdmFyKC0tbGgtbXV0ZWQpOwogIGJhY2tncm91bmQ6IHRyYW5zcGFyZW50OwogIGJvcmRlcjogMS41cHggZGFzaGVkIHZhcigtLWxoLXJ1bGUpOwogIGJvcmRlci1yYWRpdXM6IHZhcigtLWxoLXdvYmJsZS0yKTsKICAvKiBCb3RoIHNwZWxsaW5nczogU2FmYXJpIHN0aWxsIHNoaXBzIHRoZSBwc2V1ZG8tZWxlbWVudCwgZXZlcnlvbmUgZWxzZQogICAgIGhvbm91cnMgbGlzdC1zdHlsZS4gTGVmdCBpbiwgdGhlIGRlZmF1bHQgdHJpYW5nbGUgc2l0cyBvdXRzaWRlIHRoZSB0YWIuICovCiAgbGlzdC1zdHlsZTogbm9uZTsKICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lOwogIHVzZXItc2VsZWN0OiBub25lOwogIHRyYW5zaXRpb246IGNvbG9yIDAuMTJzIGVhc2UsIGJvcmRlci1jb2xvciAwLjEycyBlYXNlOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Oi13ZWJraXQtZGV0YWlscy1tYXJrZXIgeyBkaXNwbGF5OiBub25lOyB9CgovKiBPdXJzLiBtYXJpbW8ncyBjaGV2cm9uIGlzIHR3byByb3RhdGVkIGJvcmRlcnMgd2l0aCBwYWRkaW5nIGFuZCBhIG1hcmdpbiwKICAgc28gZXZlcnkgb25lIG9mIHRob3NlIHByb3BlcnRpZXMgaGFzIHRvIGJlIG5hbWVkIHRvIGJlIHN3aXRjaGVkIG9mZiDigJQKICAgbGVmdCBpbiwgaXRzIDQ1ZGVnIGJveCBsYW5kcyBvbiB0b3Agb2YgdGhpcyBhcnJvdy4gKi8KLm1hcmtkb3duIGRldGFpbHMubGgtYW5zd2VyID4gc3VtbWFyeTo6YmVmb3JlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OjpiZWZvcmUgewogIGNvbnRlbnQ6ICLilrgiOwogIGJvcmRlcjogMDsKICBwYWRkaW5nOiAwOwogIG1hcmdpbjogMDsKICB0cmFuc2Zvcm06IG5vbmU7CiAgdHJhbnNpdGlvbjogbm9uZTsKICB2ZXJ0aWNhbC1hbGlnbjogYmFzZWxpbmU7CiAgZm9udC1zaXplOiAxMXB4OwogIGxpbmUtaGVpZ2h0OiAxOwogIGNvbG9yOiB2YXIoLS1saC1ibHVlLTIpOwp9Ci5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnk6OmJlZm9yZSwKLnByb3NlIGRldGFpbHMubGgtYW5zd2VyW29wZW5dID4gc3VtbWFyeTo6YmVmb3JlIHsKICBjb250ZW50OiAi4pa+IjsKICB0cmFuc2Zvcm06IG5vbmU7Cn0KCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6aG92ZXIgewogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtYmx1ZS0yKTsKfQoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBzdW1tYXJ5OmZvY3VzLXZpc2libGUsCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlciA+IHN1bW1hcnk6Zm9jdXMtdmlzaWJsZSB7CiAgb3V0bGluZTogMnB4IHNvbGlkIHZhcigtLWxoLWJsdWUpOwogIG91dGxpbmUtb2Zmc2V0OiAycHg7Cn0KCi8qIE9wZW46IHRoZSB0YWIgaGFuZHMgb3ZlciB0byB0aGUgcXVvdGUsIHNvIGl0IHN0b3BzIGRyYXdpbmcgYSBib3JkZXIuICovCi5tYXJrZG93biBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnksCi5wcm9zZSBkZXRhaWxzLmxoLWFuc3dlcltvcGVuXSA+IHN1bW1hcnkgewogIGJvcmRlci1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgcGFkZGluZy1sZWZ0OiAwOwogIHBhZGRpbmctcmlnaHQ6IDA7Cn0KCi8qIEluc2lkZSB0aGUgZm9sZCwgYW5kIE9OTFkgaW5zaWRlIGl0LCB0aGUgcXVvdGUgaXMgaGFuZHdyaXRpbmcuIFRoYXQgaXMKICAgd2hhdCB0ZWxscyBhIHJlYWRlciBhdCBhIGdsYW5jZSB3aGljaCB3b3JkcyBhcmUgdGhlIG5vdGUncyBhbmQgd2hpY2ggYXJlCiAgIHRoZWlycyDigJQgdGhlIGdyZXkgYWxvbmUgbGVmdCB0aGUgdHdvIGxvb2tpbmcgbGlrZSBvbmUgdm9pY2UuCiAgIFNjb3BlZCB0byB0aGUgZm9sZCBvbiBwdXJwb3NlOiBjcDcgcXVvdGVzIGFuIEFJJ3MgYW5hbHlzaXMgaW4gYQogICBibG9ja3F1b3RlIHRvbywgYW5kIHRoYXQgb25lIGlzIGVtcGhhdGljYWxseSBub3Qgd3JpdHRlbiBieSBoYW5kLiAqLwoubWFya2Rvd24gZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlLAoucHJvc2UgZGV0YWlscy5saC1hbnN3ZXIgPiBibG9ja3F1b3RlIHsKICBtYXJnaW4tdG9wOiAwLjNlbTsKICBmb250LWZhbWlseTogdmFyKC0tbGgtaGFuZCk7CiAgLyogVGhlc2UgZmFjZXMgcnVuIHNtYWxsIGZvciB0aGVpciBwb2ludCBzaXplIOKAlCBTZWdvZSBQcmludCBlc3BlY2lhbGx5LiAqLwogIGZvbnQtc2l6ZTogMS4wNmVtOwogIGxpbmUtaGVpZ2h0OiAxLjU7Cn0KCi5tYXJrZG93biBociwgLnByb3NlIGhyIHsKICBib3JkZXI6IDA7CiAgaGVpZ2h0OiA3cHg7CiAgbWFyZ2luOiAyZW0gMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UtZmFpbnQpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGNlbnRlcjsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoKLm1hcmtkb3duIGNvZGU6bm90KHByZSBjb2RlKSwKLnByb3NlIGNvZGU6bm90KHByZSBjb2RlKSB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMC44NmVtOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHBhZGRpbmc6IDAuMWVtIDAuNGVtOwogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB0YWJsZXMgLS0tLS0tLS0tLSAqLwoKLm1hcmtkb3duIHRhYmxlLCAucHJvc2UgdGFibGUgeyBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOyBmb250LXNpemU6IDE2cHg7IH0KLm1hcmtkb3duIHRoLCAucHJvc2UgdGggewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKICBmb250LXdlaWdodDogNzAwOwogIGZvbnQtc2l6ZTogMTRweDsKICBsZXR0ZXItc3BhY2luZzogMC4wMmVtOwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwogIHRleHQtYWxpZ246IGxlZnQ7CiAgYm9yZGVyLWJvdHRvbTogMDsKICBwYWRkaW5nOiA2cHggMTRweCA4cHggMDsKICBiYWNrZ3JvdW5kLWltYWdlOiB2YXIoLS1saC1zdHJva2UpOwogIGJhY2tncm91bmQtcmVwZWF0OiByZXBlYXQteDsKICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBsZWZ0IGJvdHRvbTsKICBiYWNrZ3JvdW5kLXNpemU6IDEyMHB4IDdweDsKfQoubWFya2Rvd24gdGQsIC5wcm9zZSB0ZCB7CiAgcGFkZGluZzogOHB4IDE0cHggOHB4IDA7CiAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkIHZhcigtLWxoLXJ1bGUpOwogIC8qIE51bWJlcnMgc3RheSBtZWNoYW5pY2FsOiBhIGNvbHVtbiB0aGF0IGRvZXMgbm90IGxpbmUgdXAgaXMgYSBjb2x1bW4gdGhhdAogICAgIGNhbm5vdCBiZSBjb21wYXJlZCwgd2hpY2ggaXMgdGhlIHdob2xlIHJlYXNvbiB0aGUgdGFibGUgaXMgdGhlcmUuICovCiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLW1vbm8pOwogIGZvbnQtc2l6ZTogMTVweDsKICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zOwp9CgovKiAtLS0tLS0tLS0tIGNlbGxzIC0tLS0tLS0tLS0gKi8KCi5jZWxsLApbZGF0YS10ZXN0aWQ9ImNlbGwiXSB7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQouY2VsbDpudGgtb2YtdHlwZShldmVuKSwKW2RhdGEtdGVzdGlkPSJjZWxsIl06bnRoLW9mLXR5cGUoZXZlbikgeyBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7IH0KCi5jZWxsOmZvY3VzLXdpdGhpbiwKW2RhdGEtdGVzdGlkPSJjZWxsIl06Zm9jdXMtd2l0aGluIHsKICBib3gtc2hhZG93OiAwIDAgMCAycHggdmFyKC0tbGgtcnVsZSksIHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLmNlbGwtZWRpdG9yLAouY20tZWRpdG9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxMy41cHg7CiAgbGluZS1oZWlnaHQ6IDEuNTU7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7Cn0KCi5jbS1lZGl0b3IgLmNtLWd1dHRlcnMgewogIGJhY2tncm91bmQ6IHZhcigtLWxoLXN1cmZhY2UpOwogIGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7CiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tbGgtcnVsZSk7Cn0KCi5jbS1lZGl0b3IuY20tZm9jdXNlZCB7IG91dGxpbmU6IDJweCBzb2xpZCB2YXIoLS1saC1ibHVlKTsgfQouY20tZWRpdG9yIC5jbS1jdXJzb3IgeyBib3JkZXItbGVmdC1jb2xvcjogdmFyKC0tbGgtcnVzdCk7IH0KLmNtLWVkaXRvciAuY20tc2VsZWN0aW9uQmFja2dyb3VuZCwKLmNtLWVkaXRvci5jbS1mb2N1c2VkIC5jbS1zZWxlY3Rpb25CYWNrZ3JvdW5kIHsgYmFja2dyb3VuZDogI0RDRTNFRCAhaW1wb3J0YW50OyB9Ci5jbS1lZGl0b3IgLmNtLWFjdGl2ZUxpbmUgeyBiYWNrZ3JvdW5kOiByZ2JhKDMxLCA1OCwgOTUsIDAuMDQ1KTsgfQoKLyogc3ludGF4ICovCi5jbS1lZGl0b3IgLnRvay1rZXl3b3JkLAouY20tZWRpdG9yIC5jbS1rZXl3b3JkIHsgY29sb3I6IHZhcigtLWxoLWJsdWUpOyBmb250LXdlaWdodDogNTAwOyB9Ci5jbS1lZGl0b3IgLnRvay1udW1iZXIsCi5jbS1lZGl0b3IgLmNtLW51bWJlciB7IGNvbG9yOiB2YXIoLS1saC1ydXN0KTsgfQouY20tZWRpdG9yIC50b2stc3RyaW5nLAouY20tZWRpdG9yIC5jbS1zdHJpbmcgeyBjb2xvcjogIzRCNkEzQTsgfQouY20tZWRpdG9yIC50b2stY29tbWVudCwKLmNtLWVkaXRvciAuY20tY29tbWVudCB7IGNvbG9yOiB2YXIoLS1saC1tdXRlZCk7IGZvbnQtc3R5bGU6IGl0YWxpYzsgfQouY20tZWRpdG9yIC50b2stdmFyaWFibGVOYW1lLAouY20tZWRpdG9yIC50b2stcHJvcGVydHlOYW1lIHsgY29sb3I6IHZhcigtLWxoLWluayk7IH0KLmNtLWVkaXRvciAudG9rLW9wZXJhdG9yIHsgY29sb3I6IHZhcigtLWxoLWluay0yKTsgfQoKLyogLS0tLS0tLS0tLSBvdXRwdXQgLS0tLS0tLS0tLSAqLwoKLm91dHB1dC1hcmVhLAoubWFyaW1vLW91dHB1dCB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGNvbG9yOiB2YXIoLS1saC1pbmstMik7Cn0KCi5vdXRwdXQtYXJlYSBwcmUsCnByZS5vdXRwdXQgewogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1tb25vKTsKICBmb250LXNpemU6IDEzcHg7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtc3VyZmFjZSk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVsZSk7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4tc29mdCk7CiAgcGFkZGluZzogMTBweCAxMnB4OwogIGNvbG9yOiB2YXIoLS1saC1pbmspOwp9CgovKiBBIGZpZ3VyZSBpcyBhIGRyYXdpbmcgdGFwZWQgb250byB0aGUgcGFnZS4gKi8KLm91dHB1dC1hcmVhIGltZywKLm1hcmltby1vdXRwdXQgaW1nLAoub3V0cHV0LWFyZWEgc3ZnLAoubWFyaW1vLW91dHB1dCBzdmcgewogIGJvcmRlci1yYWRpdXM6IDZweCAzcHggN3B4IDRweCAvIDRweCA3cHggM3B4IDZweDsKfQoKLyogLS0tLS0tLS0tLSB1aSBjaHJvbWUgLS0tLS0tLS0tLSAqLwoKYnV0dG9uLAoubWFyaW1vLWJ1dHRvbiB7CiAgZm9udC1mYW1pbHk6IHZhcigtLWxoLXNhbnMpOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKfQoKLyogQW55dGhpbmcgdGhlIHN0dWRlbnQgYWN0dWFsbHkgcHJlc3NlcyDigJQg4pa2IFJ1biwg8J+TqCBTZW5kIHRvIG15IHR1dG9yLCB0aGUKICAgcmVmZXJlZSdzIGFwcGVhbCDigJQgaXMgZHJhd24sIGFuZCBtb3ZlcyB1bmRlciB0aGUgcHJlc3MuICovCi5tYXJpbW8tcnVuLWJ1dHRvbiwKLm1hcmltby1idXR0b24sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXSwKYnV0dG9uW2RhdGEtdmFyaWFudD0ic2Vjb25kYXJ5Il0sCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3gtc2hhZG93OiB2YXIoLS1saC1wZW4pOwogIHRyYW5zaXRpb246IHRyYW5zZm9ybSAwLjA2cyBlYXNlLCBib3gtc2hhZG93IDAuMDZzIGVhc2U7Cn0KLm1hcmltby1ydW4tYnV0dG9uOmFjdGl2ZSwKLm1hcmltby1idXR0b246YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJwcmltYXJ5Il06YWN0aXZlLApidXR0b25bZGF0YS12YXJpYW50PSJzZWNvbmRhcnkiXTphY3RpdmUsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXTphY3RpdmUgewogIHRyYW5zZm9ybTogdHJhbnNsYXRlKDJweCwgMi41cHgpOwogIGJveC1zaGFkb3c6IG5vbmU7Cn0KCi5tYXJpbW8tcnVuLWJ1dHRvbiwKYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdIHsKICBiYWNrZ3JvdW5kOiB2YXIoLS1saC1ibHVlKTsKICBjb2xvcjogdmFyKC0tbGgtcGFwZXIpOwogIGJvcmRlci1jb2xvcjogdmFyKC0tbGgtaW5rKTsKfQoubWFyaW1vLXJ1bi1idXR0b246aG92ZXIsCmJ1dHRvbltkYXRhLXZhcmlhbnQ9InByaW1hcnkiXTpob3ZlciB7IGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUtMik7IH0KCi8qIFNsaWRlcnM6IGEgcGVuY2lsIGxpbmUgd2l0aCBhIGJlYWQgb24gaXQuIFNlbGVjdG9ycyBjb3ZlciBtYXJpbW8ncyBvd24KICAgd2lkZ2V0IGFuZCBhIHBsYWluIHJhbmdlIGlucHV0LCB3aGljaGV2ZXIgdGhlIGJ1aWxkIHJlbmRlcnMuICovCmlucHV0W3R5cGU9InJhbmdlIl0gewogIGFjY2VudC1jb2xvcjogdmFyKC0tbGgtYmx1ZSk7CiAgaGVpZ2h0OiAyMnB4Owp9Cltyb2xlPSJzbGlkZXIiXSwKW2RhdGEtb3JpZW50YXRpb249Imhvcml6b250YWwiXSBbcm9sZT0ic2xpZGVyIl0gewogIGJvcmRlcjogMnB4IHNvbGlkIHZhcigtLWxoLWluayk7CiAgYm9yZGVyLXJhZGl1czogNTglIDQyJSA1MCUgNTAlIC8gNTAlIDUwJSA0MiUgNTglOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWJsdWUpOwogIGJveC1zaGFkb3c6IHZhcigtLWxoLXBlbi1zb2Z0KTsKfQoKLyogVGV4dCB0aGUgc3R1ZGVudCB0eXBlcyBpbnRvOiBhIHJ1bGVkIGJveCwgbm90IGEgY2hyb21lIGZpZWxkLiAqLwppbnB1dFt0eXBlPSJ0ZXh0Il0sCmlucHV0W3R5cGU9Im51bWJlciJdLAp0ZXh0YXJlYSwKLm1hcmltby10ZXh0LWlucHV0IHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtc2Fucyk7CiAgYmFja2dyb3VuZDogdmFyKC0tbGgtY2FyZCk7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtaW5rKTsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUtMik7CiAgYm94LXNoYWRvdzogdmFyKC0tbGgtcGVuLXNvZnQpOwp9CgovKiBUaGUgcGhvdG8gZHJvcCBib3gg4oCUIHRoZSBvbmUgcGxhY2Ugb24gdGhlIHBhZ2UgdGhhdCBhc2tzIGZvciBwYXBlci4gKi8KW2RhdGEtdGVzdGlkPSJmaWxlLXVwbG9hZCJdLAoubWFyaW1vLWZpbGUtdXBsb2FkLAouZHJvcHpvbmUgewogIGJvcmRlcjogMi41cHggZGFzaGVkIHZhcigtLWxoLWluaykgIWltcG9ydGFudDsKICBib3JkZXItcmFkaXVzOiB2YXIoLS1saC13b2JibGUpOwogIGJhY2tncm91bmQ6IHZhcigtLWxoLWNhcmQpOwogIGZvbnQtZmFtaWx5OiB2YXIoLS1saC1zYW5zKTsKfQoKLyogc3RhbGUgLyBlcnJvciBzdGF0ZXMgKi8KLmNlbGwuc3RhbGUsCltkYXRhLXN0YWxlPSJ0cnVlIl0geyBib3gtc2hhZG93OiBpbnNldCAzcHggMCAwIHZhcigtLWxoLXJ1c3QpOyB9CgoubWFyaW1vLWVycm9yLAoub3V0cHV0LWFyZWEgLmVycm9yIHsKICBmb250LWZhbWlseTogdmFyKC0tbGgtbW9ubyk7CiAgZm9udC1zaXplOiAxM3B4OwogIGJhY2tncm91bmQ6ICNGQkVERTc7CiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tbGgtcnVzdCk7CiAgY29sb3I6ICM2RTJGMTQ7CiAgYm9yZGVyLXJhZGl1czogdmFyKC0tbGgtd29iYmxlKTsKICBwYWRkaW5nOiAxMHB4IDEycHg7Cn0KCi8qIHNsaWRlcyAvIGFwcCB2aWV3ICovCi5zbGlkZXMsCltkYXRhLW1vZGU9InByZXNlbnQiXSAubWFya2Rvd24geyBmb250LXNpemU6IDE4cHg7IH0KCi8qIEEgc3R1ZGVudCB3aG8gaGFzIGFza2VkIGZvciBsZXNzIG1vdGlvbiBnZXRzIHRoZSBkcmF3aW5nIHdpdGhvdXQgdGhlCiAgIGJ1dHRvbiB0aGF0IG1vdmVzIHVuZGVyIHRoZSBwcmVzcy4gKi8KQG1lZGlhIChwcmVmZXJzLXJlZHVjZWQtbW90aW9uOiByZWR1Y2UpIHsKICAubWFyaW1vLXJ1bi1idXR0b24sCiAgLm1hcmltby1idXR0b24sCiAgYnV0dG9uW2RhdGEtdmFyaWFudD0icHJpbWFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9InNlY29uZGFyeSJdLAogIGJ1dHRvbltkYXRhLXZhcmlhbnQ9Im91dGxpbmUiXSB7IHRyYW5zaXRpb246IG5vbmU7IH0KfQo="  # BUILT
    LECTURE_HALL_CSS = base64.b64decode(LECTURE_HALL_CSS_B64).decode("utf-8")

    INK = "#1D1E21"
    RULE = "#D9D2C2"
    BLUE = "#3959A6"
    RUST = "#B14434"
    PAPER = "#FFFDF7"
    GREY = "#BDB8AA"
    MUTED = "#6A6D75"
    MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
    WOBBLE = "7px 4px 8px 5px / 5px 8px 4px 7px"

    # The pen: one wobbly filter, named so several drawings can share it.
    _PEN = (
        '<defs><filter id="lh-pen" x="-15%" y="-15%" width="130%" height="130%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" '
        'seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" '
        'xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
    )

    # ---- words and boxes ------------------------------------------------------

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">{text}</div>'
        )

    WAITING = mo.Html(
        f'<div style="font-family:{SANS};font-size:15px;color:{MUTED};'
        f'border:1.5px dashed {RULE};border-radius:{WOBBLE};padding:10px 14px;'
        'display:inline-block">Waiting on the cells above.</div>'
    )

    def type_me(src):
        """A block of code to read and type. It cannot be selected, so it
        cannot be pasted."""
        return mo.Html(
            f'<pre style="user-select:none;-webkit-user-select:none;cursor:default;'
            f"font-family:{MONO};font-size:13.5px;line-height:1.5;margin:10px 0;"
            f"padding:10px 14px;background:{PAPER};border:1.5px solid {RULE};"
            f'border-radius:{WOBBLE};color:{INK};overflow-x:auto">'
            f"{html.escape(_inspect.cleandoc(src))}</pre>"
        )

    def two_col(left, right, left_basis=320):
        return mo.Html(
            '<div style="display:flex;gap:26px;align-items:center;'
            'justify-content:flex-start;flex-wrap:wrap">'
            f'<div style="flex:0 0 {left_basis}px;max-width:100%">{left}</div>'
            f'<div style="flex:0 1 auto;min-width:170px">{right}</div></div>'
        )

    def as_numbers(x, n):
        """x as a float array, or None if it is not n numbers."""
        try:
            a = np.asarray(x, dtype=float)
        except (TypeError, ValueError):
            return None
        return a if a.shape == (n,) else None

    # ---- the worked network: the lecture notes' five nodes -------------------
    # Nodes 1-5 of the running example in 01-concepts.qmd, renumbered from 0
    # because that is how Python counts. A triangle and a tail, with the
    # three-way degree tie (nodes 0, 1 and 3) that every measure breaks
    # differently. It is the network of every worked figure in this file, and
    # the club network never appears in one.
    FIVE_N = 5
    FIVE_EDGES = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
    _FIVE_POS = {0: (52, 74), 1: (52, 166), 2: (150, 120), 3: (248, 120), 4: (346, 120)}

    def five_adjacency():
        A = np.zeros((FIVE_N, FIVE_N), dtype=float)
        for i, j in FIVE_EDGES:
            A[i, j] = A[j, i] = 1.0
        return A

    def five_scores(k):
        """The sheet's Question 7 game on the worked network, run raw: everyone
        starts with one point; each round, every node takes the sum of its
        friends' scores. No division, so the student watching the slider sees
        the numbers run away — Question 12's question."""
        c = np.ones(FIVE_N)
        for _ in range(k):
            c = five_adjacency() @ c
        return c

    # ---- the student's network: the sheet's thirteen students ----------------
    # Sarah, Mike, Emma and the rest, in the order of the sheet's tables. The
    # edge list is the kit's own copy: the checks mark against it, the picture
    # is drawn from it, and no cell ever prints it.
    NAMES = [
        "Sarah", "Mike", "Emma", "Alex", "Olivia", "James", "Sophia",
        "Ethan", "Ava", "Noah", "Lily", "Lucas", "Henry",
    ]
    CLUB_N = 13
    _CLUB_EDGES = [
        (0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (3, 6), (4, 5),
        (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9), (9, 10), (9, 11), (9, 12),
    ]
    _EDGE_CLUB = {
        (0, 1): "Drama Club", (0, 2): "Drama Club", (1, 2): "Drama Club",
        (2, 3): "Art Club", (3, 4): "Volunteer Club", (3, 5): "Volunteer Club",
        (4, 5): "Volunteer Club", (3, 6): "Sailing Club", (6, 7): "Chess Club",
        (6, 8): "Chess Club", (6, 9): "Chess Club", (7, 8): "Chess Club",
        (7, 9): "Chess Club", (8, 9): "Chess Club", (9, 10): "Debate Team",
        (9, 11): "Math Club", (9, 12): "Tennis Club",
    }

    # The sheet's page-3 drawing, same places, scaled into a box.
    _CLUB_POS = {
        0: (30, 80), 1: (30, 182), 2: (86, 131), 3: (176, 131), 4: (239, 60),
        5: (310, 60), 6: (264, 131), 7: (336, 80), 8: (336, 182), 9: (400, 131),
        10: (473, 80), 11: (484, 131), 12: (473, 182),
    }

    # The pencil answers, held here so the marking cells never carry them.
    # Every list is in NAMES order; Question 7's two rounds are the sheet's own
    # Question 7 columns, and the settled game is the same loop run to a
    # hundred rounds, normalised by the biggest each round.
    CLUB_M = len(_CLUB_EDGES)
    CLUB_TRUTH = {
        "degree": [2, 2, 3, 4, 2, 2, 4, 3, 3, 6, 1, 1, 1],
        "avg": [3.3333333333333335, 3.3333333333333335, 2.5, 1.9166666666666667,
                2.75, 2.75, 1.8333333333333333, 2.3333333333333335, 2.3333333333333335,
                2.0833333333333335, 3.0, 3.0, 3.0],
        "cut": [0, 0, 20, 41, 0, 0, 36, 0, 0, 30, 0, 0, 0],
    }
    _club_A = np.zeros((CLUB_N, CLUB_N), dtype=float)
    for _i, _j in _CLUB_EDGES:
        _club_A[_i, _j] = _club_A[_j, _i] = 1.0
    CLUB_ROUND2 = _club_A @ (_club_A @ np.ones(CLUB_N))  # the sheet's Question 7
    _settled = np.ones(CLUB_N)
    for _ in range(100):
        _settled = _club_A @ _settled
        _settled = _settled / _settled.max()
    CLUB_SETTLED = _settled  # the game settled: eigenvector centrality, Noah = 1

    def club_ready(g):
        """True once the cell above built the sheet's network."""
        try:
            if g.vcount() != CLUB_N or g.ecount() != CLUB_M:
                return False
            mine = sorted(tuple(sorted(e)) for e in g.get_edgelist())
            want = sorted(tuple(sorted(e)) for e in _CLUB_EDGES)
            return mine == want
        except Exception:
            return False

    def club_missing(g):
        """The first pair a wrong build is missing or inventing, with its club.
        Only called once the node count is right."""
        mine = {tuple(sorted(e)) for e in g.get_edgelist()}
        want = {tuple(sorted(e)) for e in _CLUB_EDGES}
        missing = sorted(want - mine)
        extra = sorted(mine - want)
        hint = ""
        if missing:
            i, j = missing[0]
            hint = f"the {_EDGE_CLUB[missing[0]]} pair {NAMES[i]}\u2013{NAMES[j]} is missing"
        if extra:
            i, j = extra[0]
            more = f"{NAMES[i]}\u2013{NAMES[j]} is not a pair on the sheet"
            hint = f"{hint}, and {more}" if hint else f"{more}"
        return hint

    # ---- Rome: the course's twelve cities ------------------------------------
    # The Module 6 deck's map: every edge a documented Roman road or a
    # documented sea lane, positions the real longitude and latitude. The
    # Channel crossing is the deck's cut: the only edge whose loss strands a
    # city.
    ROMA_CITIES = [
        "Londinium", "Colonia", "Lugdunum", "Massilia", "Tarraco", "Mediolanum",
        "Roma", "Carthago", "Thessalonica", "Athenae", "Byzantium", "Alexandria",
    ]
    ROMA_LONLAT = {
        "Londinium": (-0.1, 51.5), "Colonia": (6.9, 50.9), "Lugdunum": (4.8, 45.8),
        "Massilia": (5.4, 43.3), "Tarraco": (1.3, 41.1), "Mediolanum": (9.2, 45.5),
        "Roma": (12.5, 41.9), "Carthago": (10.3, 36.9), "Thessalonica": (22.9, 40.6),
        "Athenae": (23.7, 38.0), "Byzantium": (29.0, 41.0), "Alexandria": (29.9, 31.2),
    }
    ROMA_EDGES = [
        ("Roma", "Mediolanum"), ("Roma", "Massilia"), ("Roma", "Carthago"),
        ("Roma", "Thessalonica"), ("Roma", "Alexandria"), ("Mediolanum", "Lugdunum"),
        ("Mediolanum", "Colonia"), ("Lugdunum", "Massilia"), ("Lugdunum", "Colonia"),
        ("Colonia", "Londinium"), ("Massilia", "Tarraco"), ("Tarraco", "Carthago"),
        ("Carthago", "Alexandria"), ("Thessalonica", "Byzantium"),
        ("Thessalonica", "Athenae"), ("Athenae", "Byzantium"),
        ("Athenae", "Alexandria"), ("Byzantium", "Alexandria"),
    ]
    CHANNEL = ("Colonia", "Londinium")  # the sea route the cut experiment removes
    _ROMA_N = len(ROMA_CITIES)
    ROMA_IDX = {c: i for i, c in enumerate(ROMA_CITIES)}
    _ROMA_LABEL = {  # which side of its disc each name sits on
        "Londinium": "r", "Colonia": "r", "Lugdunum": "l", "Massilia": "d",
        "Tarraco": "r", "Mediolanum": "r", "Roma": "d", "Carthago": "l",
        "Thessalonica": "u", "Athenae": "d", "Byzantium": "l", "Alexandria": "l",
    }

    def roma_graph(cut=False):
        g = igraph.Graph(
            n=_ROMA_N,
            edges=[
                (ROMA_IDX[a], ROMA_IDX[b])
                for a, b in ROMA_EDGES
                if not (cut and {a, b} == set(CHANNEL))
            ],
        )
        g.vs["name"] = ROMA_CITIES
        return g

    # ---- drawing --------------------------------------------------------------

    def _svg(width, height, body):
        return (
            f'<svg viewBox="0 0 {width} {height}" width="100%" '
            f'style="max-width:{width}px;display:block" '
            f'xmlns="http://www.w3.org/2000/svg">{_PEN}'
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="{PAPER}"/>'
            f'<g filter="url(#lh-pen)">{body}</g></svg>'
        )

    def _edge_lines(edges, pos, dashed=(), width=2.0, opacity=0.4):
        out = []
        for i, j in edges:
            (x1, y1), (x2, y2) = pos[i], pos[j]
            if tuple(sorted((i, j))) in dashed:
                out.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{RUST}" stroke-width="{width + 1}" stroke-dasharray="6 6" '
                    f'stroke-linecap="round" opacity="0.9"/>'
                )
            else:
                out.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{INK}" stroke-width="{width}" opacity="{opacity}" '
                    f'stroke-linecap="round"/>'
                )
        return "".join(out)

    def five_svg(scores=None):
        """The worked network, discs scaled by the scores of the round shown."""
        scores = np.ones(FIVE_N) if scores is None else np.asarray(scores, float)
        top = scores.max() if scores.max() else 1
        r = 13 + 11 * scores / top
        body = [_edge_lines(FIVE_EDGES, _FIVE_POS)]
        for i in range(FIVE_N):
            x, y = _FIVE_POS[i]
            body.append(
                f'<circle cx="{x}" cy="{y}" r="{r[i]:.1f}" fill="{PAPER}" '
                f'stroke="{INK}" stroke-width="2.4"/>'
            )
        body.append("</g>")
        for i in range(FIVE_N):
            x, y = _FIVE_POS[i]
            body.append(
                f'<text x="{x}" y="{y + 4:.0f}" text-anchor="middle" font-size="12" '
                f'font-family="{SANS}" font-weight="700" fill="{INK}">{i}</text>'
                f'<text x="{x:.0f}" y="{y - r[i] - 7:.0f}" text-anchor="middle" '
                f'font-family="{MONO}" font-size="12" fill="{RUST}">'
                f"{scores[i]:g}</text>"
            )
        return _svg(400, 220, "".join(body))

    def club_svg(values=None, hot=()):
        """The sheet's network: students numbered 0 to 12, names beside, discs
        scaled by `values` (one number per student; None for plain)."""
        if values is None:
            r = [15.0] * CLUB_N
            shown = None
        else:
            v = np.asarray(values, float)
            v = np.where(np.isfinite(v), v, 0.0)
            top = np.abs(v).max() if np.abs(v).max() else 1
            r = (11 + 12 * np.abs(v) / top).tolist()
            shown = v
        body = [_edge_lines(_CLUB_EDGES, _CLUB_POS)]
        for i in range(CLUB_N):
            x, y = _CLUB_POS[i]
            fill = RUST if i in hot else PAPER
            body.append(
                f'<circle cx="{x}" cy="{y}" r="{r[i]:.1f}" fill="{fill}" '
                f'stroke="{INK}" stroke-width="2.2"/>'
            )
        body.append("</g>")
        for i in range(CLUB_N):
            x, y = _CLUB_POS[i]
            label_color = PAPER if i in hot else INK
            body.append(
                f'<text x="{x}" y="{y + 4:.0f}" text-anchor="middle" font-size="11" '
                f'font-family="{SANS}" font-weight="700" fill="{label_color}">{i}</text>'
                f'<text x="{x:.0f}" y="{y - r[i] - 6:.0f}" text-anchor="middle" '
                f'font-size="10.5" font-family="{SANS}" fill="{MUTED}">{NAMES[i]}</text>'
            )
            if shown is not None:
                side = "start" if x < 250 else "end"
                dx = r[i] + 5 if x < 250 else -(r[i] + 5)
                body.append(
                    f'<text x="{x + dx:.0f}" y="{y + 4:.0f}" text-anchor="{side}" '
                    f'font-family="{MONO}" font-size="11.5" fill="{RUST}">'
                    f"{shown[i]:g}</text>"
                )
        return _svg(514, 214, "".join(body))

    def roma_xy(width=620, height=470, pad=16):
        """Longitude and latitude into the box, north up: the exercise
        notebook's flat map, no tiles to fetch."""
        lons = [p[0] for p in ROMA_LONLAT.values()]
        lats = [p[1] for p in ROMA_LONLAT.values()]
        lo, hi = min(lons), max(lons)
        top, bot = max(lats), min(lats)
        return {
            ROMA_IDX[c]: (
                pad + (lon - lo) / (hi - lo) * (width - 2 * pad),
                pad + (top - lat) / (top - bot) * (height - 2 * pad),
            )
            for c, (lon, lat) in ROMA_LONLAT.items()
        }

    def roma_svg(values=None, cut=False, crown=(), w=620, h=470):
        """The empire: roads and sea lanes, cities sized by `values`, the
        winning cities' discs filled, the Channel crossing dashed when cut."""
        pos = roma_xy(w, h)
        edges = [(ROMA_IDX[a], ROMA_IDX[b]) for a, b in ROMA_EDGES]
        dashed = {tuple(sorted((ROMA_IDX[CHANNEL[0]], ROMA_IDX[CHANNEL[1]])))} if cut else set()
        body = [_edge_lines(edges, pos, dashed=dashed, width=1.7, opacity=0.5)]
        if values is None:
            r = [9.0] * _ROMA_N
        else:
            v = np.asarray(values, float)
            v = np.where(np.isfinite(v), v, 0.0)
            top = np.abs(v).max() if np.abs(v).max() else 1
            r = (7 + 10 * np.abs(v) / top).tolist()
        for i in range(_ROMA_N):
            x, y = pos[i]
            fill = RUST if ROMA_CITIES[i] in crown else PAPER
            body.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r[i]:.1f}" fill="{fill}" '
                f'stroke="{INK}" stroke-width="1.9"/>'
            )
        body.append("</g>")
        for i in range(_ROMA_N):
            x, y = pos[i]
            c = ROMA_CITIES[i]
            side = _ROMA_LABEL[c]
            if side == "r":
                tx, ty, anchor = x + r[i] + 4, y + 3.5, "start"
            elif side == "l":
                tx, ty, anchor = x - r[i] - 4, y + 3.5, "end"
            elif side == "d":
                tx, ty, anchor = x, y + r[i] + 12, "middle"
            else:
                tx, ty, anchor = x, y - r[i] - 5, "middle"
            body.append(
                f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" '
                f'font-size="11" font-family="{SANS}" fill="{INK}">{c}</text>'
            )
        return _svg(w, h, "".join(body))

    def bars_html(values, labels, fmt="{:g}", width=250, top=None):
        """One bar per entry, capped by `top` so wild rounds stay readable."""
        v = np.asarray(values, float)
        v = np.where(np.isfinite(v), v, 0.0)
        hi = top if top else (np.abs(v).max() if np.abs(v).max() else 1)
        rows = []
        for i, x in enumerate(v):
            frac = min(1.0, abs(x) / (hi if hi else 1))
            rows.append(
                f'<div style="display:flex;align-items:center;gap:8px;margin:2.5px 0">'
                f'<span style="width:86px;text-align:right;font-size:11.5px;'
                f'font-family:{SANS};color:{INK};overflow:hidden;'
                f'white-space:nowrap">{labels[i]}</span>'
                f'<span style="flex:0 0 {width}px;height:12px;'
                f'background:{PAPER};border:1px solid {RULE};'
                f'border-radius:4px 2px 3px 2px">'
                f'<span style="display:block;height:100%;width:{100 * frac:.1f}%;'
                f'background:{BLUE};border-radius:3px 1px 2px 1px"></span></span>'
                f'<span style="font-family:{MONO};font-size:11.5px;color:{INK}">'
                f"{fmt.format(x)}</span></div>"
            )
        return f'<div style="font-family:{SANS}">{''.join(rows)}</div>'

    def winner_name(values, smallest=False):
        """The names holding the best value, ties included."""
        v = np.asarray(values, float)
        best = np.nanmin(v) if smallest else np.nanmax(v)
        return ", ".join(NAMES[i] for i in np.flatnonzero(v == best))

    def order_indices(values):
        """Indices best first, ties broken by position so both sides of a
        comparison agree."""
        v = np.asarray(values, float)
        return list(np.lexsort((np.arange(len(v)), -np.where(np.isfinite(v), v, -np.inf))))


@app.cell(hide_code=True)
def _():
    # Stylesheets are global, so one <style> tag in the first cell dresses the
    # whole notebook -- in the editor, in `marimo run`, and in molab.
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Lab · The Big Cheese, by machine

    **On your own**, with the sheet next to the laptop.

    Every number this notebook asks for is one you have already written in
    pencil. When the screen and the sheet disagree, one of them is wrong, and
    finding out which is the exercise. At the end, the machine asks the Roman
    Empire the same questions the sheet asked your university clubs.

    Cells marked ✍️ are yours. Everything else runs itself.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 1 · Watch the scores go around

    Here is a different network first, nothing like yours: five nodes, a
    triangle and a tail — the one from the lecture notes. Everyone starts
    with one point. Each round, every node throws its own score away and
    takes **the sum of its friends' scores** instead.
    """)
    return


@app.cell(hide_code=True)
def _():
    anim = mo.ui.slider(0, 12, value=0, label="rounds", show_value=True)
    anim
    return (anim,)


@app.cell(hide_code=True)
def _(anim):
    two_col(
        five_svg(five_scores(anim.value)),
        bars_html(
            five_scores(anim.value),
            [f"node {i}" for i in range(FIVE_N)],
            top=max(2.0, float(five_scores(anim.value).max()) * 0.6),
        ),
    )
    return


@app.cell(hide_code=True)
def _(anim):
    if anim.value == 0:
        _text = (
            "Everyone starts with one point. Drag the slider."
        )
    elif anim.value == 1:
        _text = (
            "Round 1 <b>is</b> the friends count — Question 4 on your sheet, which the "
            "notes call <b>degree</b>. Drag on."
        )
    elif anim.value == 2:
        _text = (
            "Round 2 is the score-passing game — Question 7 on your sheet, and its "
            "answer for this network. Keep dragging."
        )
    elif anim.value >= 12:
        _text = (
            "The <b>order</b> stopped changing several rounds ago — another round now "
            "multiplies every score by the same number, so the ranking never moves "
            "again. That settled ranking is the **eigenvector centrality** of the "
            "lecture notes. And the numbers themselves have run away, which is "
            "Question 12's question: the recipe needs one more line, <i>divide by "
            "the biggest</i>, to run forever."
        )
    else:
        _text = (
            "Watch the numbers grow — and watch node 2 pull away. The order settles "
            "long before round 12; drag there to see it stand still."
        )
    note(_text, RUST if anim.value in (1, 2) else BLUE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Node 2 wins every question on this little network — most friends, shortest
    distances, most paths through it, best-connected friends. The notes use it
    to check arithmetic and warn that it is a bad place to learn what
    centrality *is*. Your thirteen students argue with each other far better.

    ---

    # 2 · ✍️ Your own network

    The thirteen students and eight clubs off your sheet. Nothing below prints
    the friendships: **you read them off the picture**, which is your sheet's
    drawing with the students numbered `0` to `12` in the order of its tables.
    One pair per friendship — wherever two students share a club they are
    friends, and a pair who share two clubs are still friends just once.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.Html(club_svg())
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
    A network is a list of pairs. igraph turns the list into a network:
    """),
            type_me("my_net = igraph.Graph(n=5, edges=[(0, 1), (0, 2)])"),
        ]
    )
    return


@app.cell
def _():
    # ✍️ Build the club network. One pair per friendship, read off the picture.
    g_clubs = ...  # TASK
    return (g_clubs,)


@app.cell(hide_code=True)
def _(g_clubs):
    if g_clubs is ...:
        _out = WAITING
    elif not club_ready(g_clubs):
        try:
            _n, _m = g_clubs.vcount(), g_clubs.ecount()
        except Exception:
            _out = note(
                "Not yet — <code>g_clubs</code> should be an igraph network, "
                "as in the block above.", RUST,
            )
            _n = _m = None
        if _n is not None:
            if _n != CLUB_N:
                _out = note(
                    f"Not yet — the sheet has <b>{CLUB_N} students</b>, and your "
                    f"network has {_n}. The number after <code>n=</code> is how "
                    "many nodes there are.", RUST,
                )
            elif _m != CLUB_M:
                _out = note(
                    f"Not yet — the sheet's eight clubs leave <b>{CLUB_M} "
                    f"friendships</b>, and your list has {_m}. "
                    f"{club_missing(g_clubs) or 'Read every club off the picture, one pair at a time.'}",
                    RUST,
                )
            else:
                _out = note(
                    f"Not yet — {CLUB_N} students and {CLUB_M} pairs, but not "
                    f"the sheet's {CLUB_M}: {club_missing(g_clubs)}.", RUST,
                )
    else:
        _out = mo.vstack(
            [
                mo.Html(club_svg()),
                mo.md(
                    f"**{CLUB_N} students, {CLUB_M} friendships, one network.** "
                    "The machine has it. Nothing about it changes for the rest "
                    "of the lab — only the questions do."
                ),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 3 · The sheet's four questions

    ## Question 4 · Count the friends

    One line of igraph, typed from the block. `my_net` is a stand-in; your
    network is `g_clubs`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
    The count of each student's friends, one per student, in the order of the
    tables:
    """),
            type_me("friends = my_net.degree()"),
        ]
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    friends = ...  # TASK
    return (friends,)


@app.cell(hide_code=True)
def _(friends, g_clubs):
    if friends is ...:
        _out = WAITING
    elif not club_ready(g_clubs):
        _out = note(
            "Build the network in section 2 first — the check up there is still "
            "asking for it.", RUST,
        )
    else:
        _vals = as_numbers(friends, CLUB_N)
        _truth = np.asarray(CLUB_TRUTH["degree"], dtype=float)
        if _vals is None:
            _out = note(
                "Not yet. <code>friends</code> should hold one count per student — "
                "thirteen of them, like Question 4's table.", RUST,
            )
        elif not np.allclose(_vals, _truth, atol=1e-9):
            _bad = np.flatnonzero(~np.isclose(_vals, _truth, atol=1e-9))
            _i = int(_bad[0])
            _out = note(
                f"Not yet — your {NAMES[_i]} has {_vals[_i]:g} friends, not "
                f"{_truth[_i]:g}. {club_missing(g_clubs) or 'Count the club roster again.'}",
                RUST,
            )
        else:
            _top = int(np.argmax(_vals))
            _second = np.unique(np.sort(_vals))[-2]
            _tied = np.flatnonzero(_vals == _second)
            _verb = "come" if len(_tied) > 1 else "comes"
            _each = f" at {_second:g} each" if len(_tied) > 1 else ""
            _out = mo.vstack(
                [
                    mo.Html(club_svg(values=friends, hot={_top})),
                    mo.md(
                        f"**{NAMES[_top]}** has the most friends: {_vals[_top]:g}. "
                        + ", ".join(NAMES[i] for i in _tied)
                        + f" {_verb} next{_each} — the candidates your sheet "
                        "sent onward, exactly the ones it asks about."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
    ## Question 5 · How far is everyone

    The sheet counted the steps from each candidate to the other twelve and
    divided by twelve. The machine does all thirteen at once.
    `distances()` hands back the whole table of shortest-path lengths; sum
    each row and divide by the twelve others:
    """),
            type_me(
                """
                distances = np.asarray(my_net.distances())
                avg_distance = distances.sum(axis=1) / (my_net.vcount() - 1)
                """
            ),
        ]
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    avg_distance = ...  # TASK
    return (avg_distance,)


@app.cell(hide_code=True)
def _(avg_distance, g_clubs):
    if avg_distance is ...:
        _out = WAITING
    elif not club_ready(g_clubs):
        _out = note("Build the network in section 2 first.", RUST)
    else:
        _vals = as_numbers(avg_distance, CLUB_N)
        _truth = np.asarray(CLUB_TRUTH["avg"])
        if _vals is None:
            _out = note(
                "Not yet. <code>avg_distance</code> should hold one number per "
                "student — thirteen of them.", RUST,
            )
        elif np.allclose(_vals, _truth * 12 / 13, atol=1e-9):
            _out = note(
                "Not yet — divide by <b>twelve</b>, the other students, not by "
                "thirteen. Question 5's table has twelve columns that count.",
                RUST,
            )
        elif not np.allclose(_vals, _truth, atol=1e-6):
            _bad = np.flatnonzero(~np.isclose(_vals, _truth, atol=1e-6))
            _i = int(_bad[0])
            _out = note(
                f"Not yet — your {NAMES[_i]} is {_vals[_i]:.2f} steps on average, "
                f"not {_truth[_i]:.2f}. The shortest path is the shortest one; "
                "count the clubs along the way.",
                RUST,
            )
        else:
            _best = int(np.argmin(_vals))
            _clo = np.asarray(g_clubs.closeness(), dtype=float)
            _clo_best = int(np.argmax(_clo))
            _out = mo.vstack(
                [
                    mo.Html(club_svg(values=-_vals, hot={_best})),
                    mo.md(
                        f"**{NAMES[_best]}** is closest to everybody: "
                        f"{_vals[_best]:.2f} steps on average. Turn the number "
                        f"upside down — {CLUB_N - 1} divided by the total — and "
                        "you have **closeness centrality**: igraph's "
                        f"<code>g_clubs.closeness()</code> crowns {NAMES[_clo_best]} "
                        f"too, at {_clo[_best]:.2f}. Same question, asked right "
                        "side up."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
    ## Question 6 · Who is indispensable

    Cover a student and their friendships; some pairs of the rest can no
    longer reach each other *at all*. Count those pairs. If the groups left
    behind have sizes $2, 3, 4$, the pairs cut off number $2\times3 + 2\times4 +
    3\times4 = 26$ — every cross-product, once. The sheet did it for three
    candidates; the machine does it for all thirteen:
    """),
            type_me(
                """
                cut_off = []
                for name in NAMES:
                    h = my_net.copy()
                    h.delete_vertices(NAMES.index(name))
                    sizes = [len(c) for c in h.components()]
                    cut_off.append(
                        sum(sizes[a] * sizes[b]
                            for a in range(len(sizes))
                            for b in range(a + 1, len(sizes)))
                    )
                """
            ),
        ]
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    cut_off = ...  # TASK
    return (cut_off,)


@app.cell(hide_code=True)
def _(cut_off, g_clubs):
    if cut_off is ...:
        _out = WAITING
    elif not club_ready(g_clubs):
        _out = note("Build the network in section 2 first.", RUST)
    else:
        _vals = as_numbers(cut_off, CLUB_N)
        _truth = np.asarray(CLUB_TRUTH["cut"], dtype=float)
        if _vals is None:
            _out = note(
                "Not yet. <code>cut_off</code> should hold one number per "
                "student — thirteen of them.", RUST,
            )
        elif np.all(_vals == 0):
            _out = note(
                "Not yet — everybody zero. <code>sizes</code> is the middle column "
                "of Question 6's table: the groups left behind. The pairs are "
                "every cross-product of two different groups.",
                RUST,
            )
        elif not np.allclose(_vals, _truth, atol=1e-9):
            _bad = np.flatnonzero(~np.isclose(_vals, _truth, atol=1e-9))
            _i = int(_bad[0])
            _out = note(
                f"Not yet — covering {NAMES[_i]} cuts off {_truth[_i]:g} pairs, "
                f"not {_vals[_i]:g}. Delete the student, list the groups left "
                "behind, then multiply across.",
                RUST,
            )
        else:
            _best = int(np.argmax(_vals))
            _btw = np.asarray(g_clubs.betweenness(), dtype=float)
            _agree = np.allclose(_btw, _truth, atol=1e-9)
            _cands = sorted(
                [(NAMES[i], CLUB_TRUTH["cut"][i]) for i in (9, 6, 3)],
                key=lambda t: -t[1],
            )
            _tail = (
                f"{NAMES[int(np.argmax(_btw))]} at {np.max(_btw):g} — and on this "
                "network it agrees with the sheet's count exactly, number for "
                "number. That agreement is this network's luck, not a law."
                if _agree
                else "the cousin of the sheet's count, not its twin."
            )
            _out = mo.vstack(
                [
                    mo.Html(club_svg(values=cut_off, hot={_best})),
                    mo.md(
                        f"Covering **{NAMES[_best]}** cuts off the most pairs: "
                        f"{_vals[_best]:g}. The candidates finish "
                        + ", ".join(f"{n} at {p:g}" for n, p in _cands)
                        + " — Question 6's winner, by machine."
                    ),
                    note(
                        "The lecture notes' name for the cousin of this count is "
                        "<b>betweenness centrality</b> — credit for lying on "
                        "shortest paths. igraph's <code>betweenness()</code> gives "
                        + _tail
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
    ## Question 7 · Pass the scores around — forever

    Question 7 played the game for two rounds; Question 12 asked for the
    recipe a computer could run forever. Here it is. One round is one
    multiplication: the adjacency matrix times the score vector sums each
    node's friends' scores. Divide by the biggest each round so the numbers
    do not run away:
    """),
            type_me(
                """
                A = np.asarray(my_net.get_adjacency().data, dtype=float)
                scores = np.ones(my_net.vcount())
                for _ in range(100):
                    scores = A @ scores
                    scores = scores / scores.max()
                """
            ),
        ]
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    settled = ...  # TASK
    return (settled,)


@app.cell(hide_code=True)
def _(g_clubs, settled):
    if settled is ...:
        _out = WAITING
    elif not club_ready(g_clubs):
        _out = note("Build the network in section 2 first.", RUST)
    else:
        _vals = as_numbers(settled, CLUB_N)
        if _vals is None:
            _out = note(
                "Not yet. <code>settled</code> should hold one number per "
                "student — thirteen of them.", RUST,
            )
        elif np.allclose(_vals, CLUB_SETTLED, atol=1e-6) or (
            order_indices(_vals) == order_indices(CLUB_SETTLED)
        ):
            _best = int(np.argmax(_vals))
            _r2 = CLUB_ROUND2
            _r2_best = int(np.argmax(_r2))
            _eig = np.asarray(g_clubs.eigenvector_centrality(), dtype=float)
            _caveat = (
                ""
                if np.allclose(_vals, CLUB_SETTLED, atol=1e-6)
                else " *(You normalised differently from the block — fine; the "
                "ranking is what the game settles, and yours has settled right.)*"
            )
            _out = mo.vstack(
                [
                    two_col(
                        bars_html(_r2, NAMES, top=_r2.max()),
                        bars_html(_vals, NAMES, top=_vals.max(), fmt="{:.2f}"),
                        left_basis=300,
                    ),
                    mo.md(
                        f"After **two rounds** the sheet's winner is "
                        f"**{NAMES[_r2_best]}** ({_r2[_r2_best]:g}). Played to a "
                        f"hundred, the game settles and **{NAMES[_best]}** takes "
                        "the lead. Both answers are right — they are answers to "
                        "different questions, which is Question 12's point."
                        + _caveat
                    ),
                    note(
                        "igraph's name for the settled ranking is "
                        "<b>eigenvector centrality</b>: "
                        f"<code>g_clubs.eigenvector_centrality()</code> puts "
                        f"{NAMES[int(np.argmax(_eig))]} first, the same order "
                        "your loop found."
                    ),
                ]
            )
        else:
            _mine = int(np.argmax(_vals))
            _out = note(
                f"Not yet — your settled winner is {NAMES[_mine]}, but the game "
                "played forever does not stop at Question 7's two rounds. Play a "
                "hundred, and divide by the biggest each round so the arithmetic "
                "stays exact.",
                RUST,
            )
    _out
    return


@app.cell(hide_code=True)
def _(avg_distance, cut_off, friends, g_clubs, settled):
    if (
        friends is ...
        or avg_distance is ...
        or cut_off is ...
        or settled is ...
        or not club_ready(g_clubs)
    ):
        _out = WAITING
    else:
        _ok = (
            np.allclose(np.asarray(friends, dtype=float), CLUB_TRUTH["degree"], atol=1e-9)
            and np.allclose(
                np.asarray(avg_distance, dtype=float), CLUB_TRUTH["avg"], atol=1e-6
            )
            and np.allclose(np.asarray(cut_off, dtype=float), CLUB_TRUTH["cut"], atol=1e-9)
            and (
                np.allclose(np.asarray(settled, dtype=float), CLUB_SETTLED, atol=1e-6)
                or order_indices(settled) == order_indices(CLUB_SETTLED)
            )
        )
        if not _ok:
            _out = note(
                "This box reads your four lists — fix the cells the checks are "
                "still complaining about first.", RUST,
            )
        else:
            _w4 = winner_name(friends)
            _w5 = winner_name(avg_distance, smallest=True)
            _w6 = winner_name(cut_off)
            _w7 = winner_name(CLUB_ROUND2)
            _names = {_w4, _w5, _w6, _w7}
            _rows = [
                ("most friends (Q4)", _w4),
                ("shortest average distance (Q5)", _w5),
                ("most pairs cut off (Q6)", _w6),
                ("highest after two rounds (Q7)", _w7),
            ]
            _table = "".join(
                f"<tr><td style='padding:5px 22px 5px 0;color:{MUTED}'>{k}</td>"
                f"<td><b>{v}</b></td></tr>"
                for k, v in _rows
            )
            _out = mo.vstack(
                [
                    mo.md(r"## Question 8 · The point of the whole sheet"),
                    mo.Html(
                        f'<div style="font-family:{SANS};font-size:16px;'
                        f'color:{INK};border:1.5px dashed {RULE};'
                        f'border-radius:{WOBBLE};padding:12px 18px;'
                        'display:inline-block">'
                        f"<table style='border-collapse:collapse;font-size:15.5px'>"
                        + _table
                        + "</table></div>"
                    ),
                    mo.md(
                        f"**{len(_names)} different name"
                        f"{'s' if len(_names) != 1 else ''} in four boxes.** "
                        "Nothing about the network changed between them; only "
                        "the question did. That is the whole module — and now "
                        "the machine can ask the same questions where pencil "
                        "cannot: on the empire."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 4 · All roads lead to Rome

    The *Milliarium Aureum* — the **Golden Milestone** — stood in the Forum
    Romanum. Emperor Augustus set it up in 20 BC, and the distances on all
    the empire's major roads were said to be counted from it: power had a
    single center, and it was central in exactly the sense of your sheet's
    Question 5 — close to everyone.

    Here is the course's map of that empire: twelve cities, and the
    documented roads and sea lanes between them. Every number below is
    computed by the cell that shows it.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.Html(roma_svg())
    return


@app.cell(hide_code=True)
def _():
    _g = roma_graph()
    _deg = np.asarray(_g.degree(), dtype=float)
    _best = int(np.argmax(_deg))
    _alex = ROMA_IDX["Alexandria"]
    _lon = ROMA_IDX["Londinium"]
    mo.vstack(
        [
            mo.md("## How many roads"),
            two_col(
                roma_svg(values=_deg, crown={ROMA_CITIES[_best]}),
                bars_html(_deg, ROMA_CITIES, top=_deg.max()),
                left_basis=430,
            ),
            mo.md(
                f"**{ROMA_CITIES[_best]}** has the most roads: {_deg[_best]:g} of "
                f"them. Alexandria has {_deg[_alex]:g}, and "
                f"{ROMA_CITIES[_lon]} has {_deg[_lon]:g} — one sea lane, the "
                "Channel crossing. Question 4, asked of an empire."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    _g = roma_graph()
    _clo = np.asarray(_g.closeness(), dtype=float)
    _best = int(np.argmax(_clo))
    _ecc = np.asarray(_g.eccentricity(), dtype=float)
    _best_ecc = np.flatnonzero(_ecc == _ecc.min())
    mo.vstack(
        [
            mo.md("## How far is everyone — the Milestone's own question"),
            two_col(
                roma_svg(values=_clo, crown={ROMA_CITIES[_best]}),
                bars_html(_clo, ROMA_CITIES, top=_clo.max(), fmt="{:.2f}"),
                left_basis=430,
            ),
            mo.md(
                f"**{ROMA_CITIES[_best]}** is closest to everybody: closeness "
                f"{_clo[_best]:.2f}. The Golden Milestone stands in the right "
                "place. On the worst case — the distance to your *farthest* "
                "city, the notes' eccentricity — Roma can only share the crown: "
                + ", ".join(ROMA_CITIES[i] for i in _best_ecc)
                + f" all sit {_ecc.min():g} steps from their farthest. "
                "Question 5, asked of an empire."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    _g = roma_graph()
    _btw = np.asarray(_g.betweenness(), dtype=float)
    _deg = np.asarray(_g.degree(), dtype=float)
    _order = np.argsort(-_btw)
    _best = int(_order[0])
    _second = int(_order[1])
    _alex = ROMA_IDX["Alexandria"]
    _bridges = []
    for e in _g.get_edgelist():
        _h = _g.copy()
        _h.delete_edges([e])
        if not _h.is_connected():
            _bridges.append(e)
    _bridge_names = " and ".join(
        f"{ROMA_CITIES[i]}\u2013{ROMA_CITIES[j]}" for i, j in _bridges
    )
    mo.vstack(
        [
            mo.md("## Who is indispensable"),
            two_col(
                roma_svg(values=_btw, crown={ROMA_CITIES[_best]}),
                bars_html(_btw, ROMA_CITIES, top=_btw.max(), fmt="{:.1f}"),
                left_basis=430,
            ),
            mo.md(
                f"**{ROMA_CITIES[_best]}** lies on the most routes between the "
                f"others. The runner-up is **{ROMA_CITIES[_second]}**, with "
                f"{_deg[_second]:g} roads against Alexandria's {_deg[_alex]:g} — "
                "a broker: few roads, but all the northern routes through it. "
                "And the empire has one road whose loss strands a city: "
                f"**{_bridge_names}** is the only bridge on the map. Question 6, "
                "asked of an empire."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    _g = roma_graph()
    _eig = np.asarray(_g.eigenvector_centrality(), dtype=float)
    _best = int(np.argmax(_eig))
    _alex = ROMA_IDX["Alexandria"]
    _gap = 1 - _eig[_alex] / _eig[_best]
    mo.vstack(
        [
            mo.md("## The scores, settled"),
            two_col(
                roma_svg(values=_eig, crown={ROMA_CITIES[_best]}),
                bars_html(_eig, ROMA_CITIES, top=_eig.max(), fmt="{:.2f}"),
                left_basis=430,
            ),
            mo.md(
                f"**{ROMA_CITIES[_best]}** wins the settled game too. The nearest "
                f"rival is Alexandria, within {100 * _gap:.0f}% — one road short "
                "of Roma's five, and holding its own on importance. Question 7 "
                "played forever, asked of an empire: every crown in the empire's "
                "four boxes reads the same name, which is what it means to say "
                "all roads lead to Rome."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Break it: the Channel crossing

    Question 11 broke your club network with one new club, and one of the
    candidates went from indispensable to dispensable. The empire's version:
    the one sea lane to Londinium.
    """)
    return


@app.cell(hide_code=True)
def _():
    cut_switch = mo.ui.switch(label="cut the Channel crossing")
    cut_switch
    return (cut_switch,)


@app.cell(hide_code=True)
def _(cut_switch):
    _g = roma_graph(cut=cut_switch.value)
    _clo = np.asarray(_g.closeness(), dtype=float)
    _har = np.asarray(_g.harmonic_centrality(), dtype=float)
    _pieces = [sorted(ROMA_CITIES[i] for i in c) for c in _g.components()]
    _har_best = int(np.nanargmax(_har))
    if not cut_switch.value:
        _say = note(
            "Flip the switch. The Channel crossing — Colonia to Londinium — is "
            "the only bridge on the map, which is Question 11's hint: break the "
            "one road a city hangs by, and everything downstream changes."
        )
    else:
        _nan = int(np.sum(~np.isfinite(_clo)))
        _say = mo.md(
            f"Londinium is an island: {len(_pieces)} pieces, one city on its "
            "own. By the notes' definition, closeness needs every distance, and "
            "one unreachable city makes every sum infinite — igraph, asked "
            f"anyway, answers only for who you can still reach ({_nan} of the "
            "twelve give no answer at all; the rest are ranked among the "
            "reachable only). **Harmonic centrality just drops Londinium's "
            f"contribution and carries on**: {ROMA_CITIES[_har_best]} still "
            f"first at {_har[_har_best]:.2f}. The whole difference is taking the "
            "reciprocal *before* the sum instead of after — which is why the "
            "notes keep harmonic centrality around."
        )
    mo.vstack(
        [
            two_col(
                roma_svg(values=_har, cut=cut_switch.value, crown={ROMA_CITIES[_har_best]}),
                roma_svg(values=_clo, cut=cut_switch.value),
                left_basis=430,
            ),
            mo.md(
                "left: harmonic centrality, which survives the cut · right: "
                "closeness, which does not"
            ),
            _say,
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Your own network

    Any network you can write as a list of pairs, `igraph.Graph(n=..., edges=...)`
    will take — and every question this lab asked is one `g.`-call away:
    `.degree()`, `.distances()`, `.components()`, `.betweenness()`,
    `.eigenvector_centrality()`. The matching question is yours to pick; the
    notes' closing table is the menu.

    *Data.* The twelve cities, their positions and their roads follow the
    course's Module 6 map (`slides/m06/figures/verify_numbers.py`), which
    records every edge as a documented Roman road or sea lane. A bigger Roman
    road network — a hundred-odd places — lives in the repository under
    `data/roman-roads`, and the hands-on notebook uses it.
    """)
    return


if __name__ == "__main__":
    app.run()