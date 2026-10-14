# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# GENERATED FILE -- do not edit. Run
#
#     python tools/build_lab_notebooks.py m06-centrality
#
# which fills in every blank of lab.py and writes this. The student's copy is
# lab.py; edit that one.
#
# The Module 6 lab, done alone at a laptop: what "central" means.
#
# One small network, eleven nodes, chosen so that four different questions
# crown four different nodes: who has the most friends, who is nearest to
# everyone, who lies on the most shortest routes, whose friends matter most.
# The student types each answer in igraph, then the notebook unlocks a reward:
# the same four questions asked of the Roman Empire.
#
#   * the kit     -- the setup block: the SVG drawing, the two networks, the
#                   answers the checks mark against. Hidden.
#   * the cells   -- they run themselves.
#   * the blanks  -- five cells that say `...`: build the network, then the
#                   degree, the average distance, the betweenness and the
#                   settled score game. All typed from a block on the page that
#                   cannot be selected, so it cannot be pasted.
#
# Rules this file obeys, learned on m01 and m02:
#
#   * No cell prints the edge list. The network is a picture with the nodes
#     numbered, and the student reads the pairs off it.
#   * The checks mark against answers held in the hidden kit, and each check
#     names the mistake rather than saying "wrong".
#   * A waiting card, not an exception, for anything downstream of a blank.
#   * The stylesheet travels inside the file. molab ignores css_file
#     (marimo-team/marimo#8467), so lecture-hall.css is carried here as
#     base64 and injected by the first cell. Refresh it with
#     `python tools/build_lab_notebooks.py m06-centrality` after editing it.
#   * Nothing is fetched at run time. Rome's twelve cities, their positions
#     and their roads are typed in below: they follow the course's Module 6
#     map (slides/m06/figures/verify_numbers.py), which records every edge
#     as a documented Roman road or sea lane.
#   * igraph is pinned to the version the coding notebooks already use
#     (python-igraph==0.11.9).

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

    def card(text):
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:15px;color:{MUTED};'
            f'border:1.5px dashed {RULE};border-radius:{WOBBLE};padding:10px 14px;'
            f'display:inline-block">{text}</div>'
        )

    WAITING = card("Waiting on the cells above.")

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

    def ask(text, code):
        """A line of words above a block to type."""
        return mo.vstack([mo.md(_inspect.cleandoc(text)), type_me(code)])

    def as_numbers(x, n):
        """x as a float array, or None if it is not n numbers."""
        try:
            a = np.asarray(x, dtype=float)
        except (TypeError, ValueError):
            return None
        return a if a.shape == (n,) else None

    # ---- the network: eleven nodes, four different crowns --------------------
    # Found by search: of all the small connected networks, this is one where
    # the most friends, the shortest distances, the most shortest routes and
    # the settled score game each pick a different node (1, 6, 8 and 4), by a
    # clear margin. The picture is drawn with no crossing lines.
    NET_N = 11
    _NET_EDGES = [
        (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 7), (4, 5), (4, 6),
        (5, 6), (6, 8), (7, 8), (8, 9), (9, 10),
    ]
    NET_M = len(_NET_EDGES)
    _NET_POS = {
        0: (60, 150), 1: (140, 150), 2: (190, 70), 3: (200, 240), 4: (250, 150),
        5: (280, 70), 6: (340, 110), 7: (350, 240), 8: (410, 150), 9: (470, 100),
        10: (510, 50),
    }

    # The answers, held here so the marking cells never carry them.
    _net = igraph.Graph(n=NET_N, edges=_NET_EDGES)
    NET_TRUTH = {
        "degree": np.array(_net.degree(), dtype=float),
        "avg": np.asarray(_net.distances(), dtype=float).sum(axis=1) / (NET_N - 1),
        "betweenness": np.array(_net.betweenness(), dtype=float),
    }
    _net_A = np.zeros((NET_N, NET_N), dtype=float)
    for _i, _j in _NET_EDGES:
        _net_A[_i, _j] = _net_A[_j, _i] = 1.0

    def net_rounds(k):
        """The score game after k rounds, divided by the biggest each round."""
        c = np.ones(NET_N)
        for _ in range(k):
            c = _net_A @ c
            c = c / c.max()
        return c

    NET_SETTLED = net_rounds(100)

    def order_indices(values):
        """Indices best first, ties broken by position so both sides of a
        comparison agree."""
        v = np.asarray(values, float)
        return list(np.lexsort((np.arange(len(v)), -np.where(np.isfinite(v), v, -np.inf))))

    def net_ready(g):
        """True once the cell above built the network."""
        try:
            if g.vcount() != NET_N or g.ecount() != NET_M:
                return False
            mine = sorted(tuple(sorted(e)) for e in g.get_edgelist())
            return mine == sorted(_NET_EDGES)
        except Exception:
            return False

    def net_missing(g):
        """The first pair a wrong build is missing or inventing."""
        mine = {tuple(sorted(e)) for e in g.get_edgelist()}
        want = {tuple(sorted(e)) for e in _NET_EDGES}
        missing, extra = sorted(want - mine), sorted(mine - want)
        hint = ""
        if missing:
            hint = f"the pair {missing[0][0]}–{missing[0][1]} is missing"
        if extra:
            more = f"{extra[0][0]}–{extra[0][1]} is not in the picture"
            hint = f"{hint}, and {more}" if hint else more
        return hint

    def ok_degree(x):
        v = as_numbers(x, NET_N)
        return v is not None and np.allclose(v, NET_TRUTH["degree"], atol=1e-9)

    def ok_avg(x):
        v = as_numbers(x, NET_N)
        return v is not None and np.allclose(v, NET_TRUTH["avg"], atol=1e-6)

    def ok_betweenness(x):
        v = as_numbers(x, NET_N)
        return v is not None and np.allclose(v, NET_TRUTH["betweenness"], atol=1e-6)

    def ok_settled(x):
        v = as_numbers(x, NET_N)
        return v is not None and (
            np.allclose(v, NET_SETTLED, atol=1e-6)
            or order_indices(v) == order_indices(NET_SETTLED)
        )

    def all_green(g, degree, avg_distance, betweenness, settled):
        if any(x is ... for x in (g, degree, avg_distance, betweenness, settled)):
            return False
        return (
            net_ready(g)
            and ok_degree(degree)
            and ok_avg(avg_distance)
            and ok_betweenness(betweenness)
            and ok_settled(settled)
        )

    # ---- Rome: the course's twelve cities ------------------------------------
    # The Module 6 deck's map: every edge a documented Roman road or a
    # documented sea lane, positions the real longitude and latitude.
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
    _ROMA_N = len(ROMA_CITIES)
    ROMA_IDX = {c: i for i, c in enumerate(ROMA_CITIES)}
    _ROMA_LABEL = {  # which side of its disc each name sits on
        "Londinium": "d", "Colonia": "r", "Lugdunum": "l", "Massilia": "d",
        "Tarraco": "r", "Mediolanum": "r", "Roma": "d", "Carthago": "l",
        "Thessalonica": "u", "Athenae": "d", "Byzantium": "l", "Alexandria": "l",
    }
    _ROMA_G = igraph.Graph(
        n=_ROMA_N, edges=[(ROMA_IDX[a], ROMA_IDX[b]) for a, b in ROMA_EDGES]
    )
    ROMA_MEASURES = {
        "degree": np.array(_ROMA_G.degree(), dtype=float),
        "closeness": np.array(_ROMA_G.closeness(), dtype=float),
        "betweenness": np.array(_ROMA_G.betweenness(), dtype=float),
        "eigenvector": np.array(_ROMA_G.eigenvector_centrality(), dtype=float),
    }

    # ---- drawing --------------------------------------------------------------

    def _svg(width, height, body):
        return (
            f'<svg viewBox="0 0 {width} {height}" width="100%" '
            f'style="max-width:{width}px;display:block" '
            f'xmlns="http://www.w3.org/2000/svg">{_PEN}'
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="{PAPER}"/>'
            f'<g filter="url(#lh-pen)">{body}</g></svg>'
        )

    def _edge_lines(edges, pos, width=2.0, opacity=0.4):
        return "".join(
            f'<line x1="{pos[i][0]:.1f}" y1="{pos[i][1]:.1f}" '
            f'x2="{pos[j][0]:.1f}" y2="{pos[j][1]:.1f}" stroke="{INK}" '
            f'stroke-width="{width}" opacity="{opacity}" stroke-linecap="round"/>'
            for i, j in edges
        )

    def _radii(values, lo, span):
        """Discs from lo to lo + span, the smallest value to the biggest."""
        v = np.asarray(values, float)
        v = np.where(np.isfinite(v), v, 0.0)
        spread = v.max() - v.min()
        return (lo + span * (v - v.min()) / (spread if spread else 1)).tolist()

    def net_svg(values=None, hot=(), fmt="{:g}"):
        """The network, nodes numbered. With `values`, discs are sized by them
        and each number is written above its disc; `hot` nodes are filled."""
        r = [15.0] * NET_N if values is None else _radii(values, 11, 11)
        body = [_edge_lines(_NET_EDGES, _NET_POS)]
        for i in range(NET_N):
            x, y = _NET_POS[i]
            fill = RUST if i in hot else PAPER
            body.append(
                f'<circle cx="{x}" cy="{y}" r="{r[i]:.1f}" fill="{fill}" '
                f'stroke="{INK}" stroke-width="2.2"/>'
            )
        body.append("</g>")
        for i in range(NET_N):
            x, y = _NET_POS[i]
            label = PAPER if i in hot else INK
            body.append(
                f'<text x="{x}" y="{y + 4:.0f}" text-anchor="middle" font-size="12" '
                f'font-family="{SANS}" font-weight="700" fill="{label}">{i}</text>'
            )
            if values is not None:
                body.append(
                    f'<text x="{x}" y="{y - r[i] - 6:.0f}" text-anchor="middle" '
                    f'font-family="{MONO}" font-size="12" fill="{RUST}">'
                    f"{fmt.format(values[i])}</text>"
                )
        return _svg(560, 280, "".join(body))

    def roma_xy(width=620, height=470, pad=16):
        """Longitude and latitude into the box, north up: no tiles to fetch."""
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

    def roma_svg(values, crown, w=620, h=470):
        """The empire: roads and sea lanes, cities sized by `values`, the
        winning city's disc filled."""
        pos = roma_xy(w, h)
        edges = [(ROMA_IDX[a], ROMA_IDX[b]) for a, b in ROMA_EDGES]
        body = [_edge_lines(edges, pos, width=1.7, opacity=0.5)]
        r = _radii(values, 7, 10)
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


@app.cell(hide_code=True)
def _():
    # Stylesheets are global, so one <style> tag in the first cell dresses the
    # whole notebook -- in the editor, in `marimo run`, and in molab.
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Lab · Who is central? — worked copy

    Eleven nodes, four ways to ask which one matters most.
    Cells marked ✍️ are yours. Everything else runs itself.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 1 · ✍️ The network

    Which node looks the most central? Pick one before you compute anything.
    """)
    return


@app.cell(hide_code=True)
def _():
    guess = mo.ui.dropdown(
        options=[str(i) for i in range(NET_N)], label="my guess: node"
    )
    mo.vstack([mo.Html(net_svg()), guess])
    return (guess,)


@app.cell(hide_code=True)
def _():
    ask(
        """
        Now build it: one pair per line in the picture. igraph turns a list of
        pairs into a network:
        """,
        "my_net = igraph.Graph(n=5, edges=[(0, 1), (0, 2)])",
    )
    return


@app.cell
def _():
    # ✍️ Build the network.
    g = igraph.Graph(
        n=NET_N,
        edges=[
            (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 7), (4, 5), (4, 6),
            (5, 6), (6, 8), (7, 8), (8, 9), (9, 10),
        ],
    )
    return (g,)


@app.cell(hide_code=True)
def _(g):
    if g is ...:
        _out = WAITING
    elif net_ready(g):
        _out = mo.md(f"**{NET_N} nodes, {NET_M} lines.** That is the network.")
    else:
        try:
            _n, _m = g.vcount(), g.ecount()
        except Exception:
            _n = _m = None
        if _n is None:
            _out = note("Not yet — <code>g</code> should be an igraph network.", RUST)
        elif _n != NET_N:
            _out = note(
                f"Not yet — the picture has <b>{NET_N} nodes</b>, your network "
                f"has {_n}. The number after <code>n=</code> is the node count.",
                RUST,
            )
        elif _m != NET_M:
            _out = note(
                f"Not yet — the picture has <b>{NET_M} lines</b>, your list has "
                f"{_m}: {net_missing(g) or 'check every node'}.",
                RUST,
            )
        else:
            _out = note(
                f"Not yet — right counts, wrong pairs: {net_missing(g)}.", RUST
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 2 · ✍️ Four questions

    Type each block, with `g` where it says `my_net`.

    ## Degree · who has the most friends?
    """)
    return


@app.cell(hide_code=True)
def _():
    type_me("degree = my_net.degree()")
    return


@app.cell
def _():
    # ✍️ Type the code above.
    degree = g.degree()
    return (degree,)


@app.cell(hide_code=True)
def _(degree, g):
    if degree is ...:
        _out = WAITING
    elif g is ... or not net_ready(g):
        _out = note("Build the network in section 1 first.", RUST)
    else:
        _v = as_numbers(degree, NET_N)
        _t = NET_TRUTH["degree"]
        if _v is None:
            _out = note(
                f"Not yet — <code>degree</code> should be {NET_N} numbers, one "
                "per node.", RUST,
            )
        elif not ok_degree(degree):
            _i = int(np.flatnonzero(~np.isclose(_v, _t))[0])
            _out = note(
                f"Not yet — you have node {_i} with {_v[_i]:g} friends, not "
                f"{_t[_i]:g}. {net_missing(g) or 'Count the lines at it again.'}",
                RUST,
            )
        else:
            _top = int(np.argmax(_v))
            _out = mo.vstack(
                [
                    mo.Html(net_svg(_v, hot={_top})),
                    mo.md(
                        f"**Node {_top}** has the most friends: {_v[_top]:g}. "
                        "That count is **degree centrality**."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    ask(
        """
        ## Closeness · who is near everyone?

        Add up a node's distances to the other ten and divide by ten. Small
        means close.
        """,
        """
        distances = np.asarray(my_net.distances())
        avg_distance = distances.sum(axis=1) / (my_net.vcount() - 1)
        """,
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    distances = np.asarray(g.distances())
    avg_distance = distances.sum(axis=1) / (g.vcount() - 1)
    return (avg_distance,)


@app.cell(hide_code=True)
def _(avg_distance, g):
    if avg_distance is ...:
        _out = WAITING
    elif g is ... or not net_ready(g):
        _out = note("Build the network in section 1 first.", RUST)
    else:
        _v = as_numbers(avg_distance, NET_N)
        _t = NET_TRUTH["avg"]
        if _v is None:
            _out = note(
                f"Not yet — <code>avg_distance</code> should be {NET_N} "
                "numbers, one per node.", RUST,
            )
        elif np.allclose(_v, _t * (NET_N - 1) / NET_N, atol=1e-9):
            _out = note(
                f"Not yet — divide by <b>{NET_N - 1}</b>, the other nodes, not "
                f"by {NET_N}.", RUST,
            )
        elif not ok_avg(avg_distance):
            _i = int(np.flatnonzero(~np.isclose(_v, _t, atol=1e-6))[0])
            _out = note(
                f"Not yet — node {_i} is {_v[_i]:.2f} steps from the others on "
                f"average, not {_t[_i]:.2f}. Sum one row of the distance "
                "table, then divide.",
                RUST,
            )
        else:
            _best = int(np.argmin(_v))
            _out = mo.vstack(
                [
                    mo.Html(net_svg(_v, hot={_best}, fmt="{:.2f}")),
                    mo.md(
                        f"**Node {_best}** is closest to everyone: {_v[_best]:.1f} "
                        "steps on average. Turned upside down, this is "
                        "**closeness centrality**."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    ask(
        """
        ## Betweenness · who is on the way?

        Take every pair of other nodes and look at their shortest routes. A
        node that sits on many of them is a bridge.
        """,
        "betweenness = my_net.betweenness()",
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    betweenness = g.betweenness()
    return (betweenness,)


@app.cell(hide_code=True)
def _(betweenness, g):
    if betweenness is ...:
        _out = WAITING
    elif g is ... or not net_ready(g):
        _out = note("Build the network in section 1 first.", RUST)
    else:
        _v = as_numbers(betweenness, NET_N)
        _t = NET_TRUTH["betweenness"]
        if _v is None:
            _out = note(
                f"Not yet — <code>betweenness</code> should be {NET_N} "
                "numbers, one per node.", RUST,
            )
        elif not ok_betweenness(betweenness):
            _i = int(np.flatnonzero(~np.isclose(_v, _t, atol=1e-6))[0])
            _out = note(
                f"Not yet — you have node {_i} on {_v[_i]:g} routes, not "
                f"{_t[_i]:g}. Check that you called <code>betweenness()</code> "
                "on your network.",
                RUST,
            )
        else:
            _top = int(np.argmax(_v))
            _out = mo.vstack(
                [
                    mo.Html(net_svg(_v, hot={_top}, fmt="{:.1f}")),
                    mo.md(
                        f"**Node {_top}** lies on the most shortest routes: "
                        f"{_v[_top]:g}. That is **betweenness centrality**."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    ask(
        """
        ## Eigenvector · whose friends matter?

        Everyone starts with 1 point. Each round, a node takes the sum of its
        friends' scores; then divide everyone by the biggest score. A hundred
        rounds:
        """,
        """
        A = np.asarray(my_net.get_adjacency().data, dtype=float)
        settled = np.ones(my_net.vcount())
        for _ in range(100):
            settled = A @ settled
            settled = settled / settled.max()
        """,
    )
    return


@app.cell
def _():
    # ✍️ Type the code above.
    A = np.asarray(g.get_adjacency().data, dtype=float)
    settled = np.ones(g.vcount())
    for _ in range(100):
        settled = A @ settled
        settled = settled / settled.max()
    return (settled,)


@app.cell(hide_code=True)
def _(g, settled):
    if settled is ...:
        _out = WAITING
    elif g is ... or not net_ready(g):
        _out = note("Build the network in section 1 first.", RUST)
    else:
        _v = as_numbers(settled, NET_N)
        if _v is None:
            _out = note(
                f"Not yet — <code>settled</code> should be {NET_N} numbers, one "
                "per node.", RUST,
            )
        elif not ok_settled(settled):
            _out = note(
                f"Not yet — your leader is node {int(np.argmax(_v))}. Play a "
                "hundred rounds, and divide by the biggest each round.",
                RUST,
            )
        else:
            _top = int(np.argmax(_v))
            _deg = NET_TRUTH["degree"]
            _out = mo.vstack(
                [
                    mo.Html(net_svg(_v, hot={_top}, fmt="{:.2f}")),
                    mo.md(
                        f"**Node {_top}** settles on top with {_deg[_top]:g} "
                        f"friends, while node {int(np.argmax(_deg))} has "
                        f"{_deg.max():g}. A friend counts for more when that "
                        "friend is important: **eigenvector centrality**."
                    ),
                ]
            )
    _out
    return


@app.cell(hide_code=True)
def _():
    rounds = mo.ui.slider(1, 12, value=1, label="rounds", show_value=True)
    return (rounds,)


@app.cell(hide_code=True)
def _(g, rounds, settled):
    if settled is ... or g is ... or not net_ready(g) or not ok_settled(settled):
        _out = mo.md("")
    else:
        _s = net_rounds(rounds.value)
        _lead = int(np.argmax(_s))
        _say = (
            "Round 1 is just the friend count."
            if rounds.value == 1
            else "Keep dragging."
            if rounds.value < 12
            else "The leader has stopped changing."
        )
        _out = mo.vstack(
            [
                mo.md("Watch the leader change as the rounds go by:"),
                rounds,
                mo.Html(net_svg(_s, hot={_lead}, fmt="{:.2f}")),
                mo.md(f"After {rounds.value} round{'s' if rounds.value != 1 else ''}, "
                      f"the leader is **node {_lead}**. {_say}"),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _(betweenness, avg_distance, degree, g, guess, settled):
    if not all_green(g, degree, avg_distance, betweenness, settled):
        _out = WAITING
    else:
        _w = {
            "most friends · degree": int(np.argmax(NET_TRUTH["degree"])),
            "nearest to everyone · closeness": int(np.argmin(NET_TRUTH["avg"])),
            "on the most routes · betweenness": int(np.argmax(NET_TRUTH["betweenness"])),
            "highest settled score · eigenvector": int(np.argmax(NET_SETTLED)),
        }
        _rows = "".join(
            f"<tr><td style='padding:5px 22px 5px 0;color:{MUTED}'>{k}</td>"
            f"<td><b>node {v}</b></td></tr>"
            for k, v in _w.items()
        )
        _guess = (
            ""
            if guess.value is None
            else f" Your guess, node {guess.value}, won "
            f"{sum(int(guess.value) == v for v in _w.values())} of the four."
        )
        _out = mo.vstack(
            [
                mo.md("---\n\n# 3 · Four questions, four answers"),
                mo.Html(
                    f'<div style="font-family:{SANS};font-size:15.5px;color:{INK};'
                    f"border:1.5px dashed {RULE};border-radius:{WOBBLE};"
                    'padding:12px 18px;display:inline-block">'
                    "<table style='border-collapse:collapse'>"
                    + _rows
                    + "</table></div>"
                ),
                mo.md(
                    f"**{len(set(_w.values()))} different nodes.** Same network, "
                    f"different question.{_guess}"
                ),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    reward = mo.ui.radio(
        options={
            "friends (degree)": "degree",
            "closeness": "closeness",
            "betweenness": "betweenness",
            "settled score (eigenvector)": "eigenvector",
        },
        value="friends (degree)",
        inline=True,
    )
    return (reward,)


@app.cell(hide_code=True)
def _(betweenness, avg_distance, degree, g, reward, settled):
    if not all_green(g, degree, avg_distance, betweenness, settled):
        _out = mo.vstack(
            [
                mo.md("---\n\n# 4 · 🏛️ Reward"),
                card("Unlocks when the four cells above are green."),
            ]
        )
    else:
        _v = ROMA_MEASURES[reward.value]
        _top = ROMA_CITIES[int(np.argmax(_v))]
        _all = {ROMA_CITIES[int(np.argmax(m))] for m in ROMA_MEASURES.values()}
        _verdict = (
            f"**{_top}** wins all four questions. All roads lead to Rome."
            if _all == {_top}
            else f"**{_top}** wins this one."
        )
        _out = mo.vstack(
            [
                mo.md(
                    "---\n\n# 4 · 🏛️ All roads lead to Rome\n\n"
                    "In 20 BC Augustus set up the Golden Milestone in the Forum, "
                    "and the empire's roads were measured from it. Twelve "
                    "cities, the roads and sea lanes between them, and your "
                    "four questions:"
                ),
                reward,
                mo.Html(roma_svg(_v, crown={_top})),
                mo.md(_verdict),
            ]
        )
    _out
    return


if __name__ == "__main__":
    app.run()
