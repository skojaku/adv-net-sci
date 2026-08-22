# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "tabulate",
#     "python-igraph==0.11.9",
#     "matplotlib==3.10.3",
# ]
# ///
#
# GENERATED FILE -- do not edit. Run
#
#     python tools/build_lab_notebooks.py m01-euler_tour
#
# which fills in every blank of lab.py and writes this. The student's copy is
# lab.py; edit that one.
#
# Part 4 of the Module 1 pen-and-paper sheet, done alone at a laptop.
#
# It is the mini-project's notebook with the group work taken out and the city
# nailed down: the four Upstate New York cities and seven highways the student
# has just spent an hour drawing on. Everything asked here is something they
# have already written in pencil, which is the point -- the machine agrees with
# them, or one of the two is wrong and they find out which.
#
# The map drawing is deliberately the sheet's map, down to the bends in the
# roads, so a student looking from paper to screen sees the same thing twice.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The drawing kit. Nothing here is yours to edit.
    import base64

    import marimo as mo
    import numpy as np
    import pandas as pd
    import igraph
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

    # The sheet's map. Cities are numbered the way the edge list needs them,
    # 0 to 3. Nothing in the notebook ever prints this list: reading it off the
    # picture is the first thing the student is asked to do.
    NY_NAMES = ["Ithaca", "Syracuse", "Binghamton", "Albany"]
    NY_EDGES = [(0, 1), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 3)]
    NY_ROADS = ["NY-13", "NY-34", "NY-79", "I-81", "I-90", "I-88", "NY-7"]
    # Question 1(b): US-11 runs beside I-81, so it joins the same two cities.
    US11_EDGE = (1, 2)

    # The worked example, and deliberately not the map they have to write down:
    # a village on a river, three places, four bridges, one pair of them
    # doubled so that the two-bridges-one-pair rule is met here rather than
    # discovered halfway through their own list.
    DEMO_NAMES = ["North bank", "South bank", "Mill Island"]
    DEMO_EDGES = [(0, 2), (0, 2), (1, 2), (0, 1)]
    DEMO_NOTES = [
        "north bank -- island",
        "north bank -- island, the second bridge",
        "south bank -- island",
        "north bank -- south bank, round the downstream bend",
    ]
    _DM_POS = {0: (110, 44), 1: (110, 180), 2: (110, 112)}
    _DM_LABEL_POS = {0: (110, 22), 1: (110, 208), 2: (88, 116)}
    _DM_PATHS = [
        "M110,44 Q56,78 110,112",
        "M110,44 Q164,78 110,112",
        "M110,180 Q56,146 110,112",
        "M110,44 Q268,112 110,180",
    ]

    # The four-node network from Part 3 of the sheet. On paper it is numbered
    # 1 to 4; here it is 0 to 3, which is the first thing to go wrong.
    SHEET_EDGES = [(0, 1), (1, 2), (1, 3), (2, 3)]

    # Pixel positions lifted from the sheet's TikZ, so the two maps look alike.
    _NY_POS = {0: (54, 151), 1: (150, 43), 2: (132, 193), 3: (348, 121)}
    _NY_LABEL_POS = {0: (36, 156), 1: (150, 26), 2: (132, 214), 3: (348, 104)}
    _NY_PATHS = [
        "M54,151 Q130,120 150,43",
        "M54,151 Q74,74 150,43",
        "M54,151 Q93,190 132,193",
        "M150,43 Q165,118 132,193",
        "M150,43 Q249,58 348,121",
        "M132,193 Q240,127 348,121",
        "M132,193 Q240,187 348,121",
    ]
    _NY_SHIELD_POS = [
        (116, 108),
        (88, 86),
        (93, 181),
        (152, 126),
        (249, 70),
        (240, 142),
        (240, 172),
    ]
    _US11_PATH = "M150,43 Q215,118 132,193"
    _US11_SHIELD = (196, 118)

    # A pen, not a plotter: fractal noise pushes every stroke off true by a
    # couple of pixels. Fixed seed, so the drawing keeps the same wobble instead
    # of vibrating as the slider moves. Text is drawn outside the filtered
    # group, because wobbly letters are simply hard to read.
    _PEN = (
        '<defs><filter id="lh-pen" x="-15%" y="-15%" width="130%" height="130%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" '
        'seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" '
        'xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
    )

    def _shield(x, y, text, hot=False):
        """A route marker, drawn outside the wobble so the number stays legible."""
        w = 8 + 6.2 * len(text)
        return (
            f'<rect x="{x - w / 2:.0f}" y="{y - 8}" width="{w:.0f}" height="16" '
            f'rx="3" fill="{RUST if hot else PAPER}" stroke="{INK}" '
            f'stroke-width="1.4" opacity="0.96"/>'
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="10" '
            f'font-family="{SANS}" font-weight="700" '
            f'fill="{PAPER if hot else INK}">{text}</text>'
        )

    def ny_svg(done=(), live=None, lit_nodes=(), us11=False):
        """The sheet's map. `done` are roads behind you, `live` is the one now."""
        out = [
            # The box reaches left of zero so that Ithaca's name, which hangs off
            # the westernmost city, is inside the drawing.
            '<svg viewBox="-30 0 430 232" width="100%" style="max-width:430px;'
            'display:block" xmlns="http://www.w3.org/2000/svg">',
            _PEN,
            '<g filter="url(#lh-pen)">',
            f'<path d="M-30,0 H150 Q90,30 -30,52 Z" fill="{BLUE}" opacity="0.10"/>',
        ]
        paths = list(_NY_PATHS) + ([_US11_PATH] if us11 else [])
        for k, d in enumerate(paths):
            if k == live:
                color, width, opacity = RUST, 5.5, 1
            elif k in done:
                color, width, opacity = BLUE, 3.5, 1
            else:
                color, width, opacity = INK, 2.5, 0.2
            out.append(
                f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
                f'opacity="{opacity}" stroke-linecap="round"/>'
            )
        for i, (x, y) in _NY_POS.items():
            out.append(
                f'<circle cx="{x}" cy="{y}" r="13" '
                f'fill="{RUST if i in lit_nodes else PAPER}" '
                f'stroke="{INK}" stroke-width="2.5"/>'
            )
        out.append("</g>")
        out.append(
            f'<text x="30" y="20" font-size="10" font-family="{SANS}" '
            f'fill="{INK}" opacity="0.45" transform="rotate(-13 30 20)">'
            "Lake Ontario</text>"
        )
        shields = list(zip(_NY_SHIELD_POS, NY_ROADS)) + (
            [(_US11_SHIELD, "US-11")] if us11 else []
        )
        for k, ((x, y), name) in enumerate(shields):
            out.append(_shield(x, y, name, hot=(k == live)))
        for i, (x, y) in _NY_POS.items():
            out.append(
                f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="12" '
                f'font-family="{SANS}" font-weight="700" '
                f'fill="{PAPER if i in lit_nodes else INK}">{i}</text>'
            )
        for i, (x, y) in _NY_LABEL_POS.items():
            anchor = {0: "end"}.get(i, "middle")
            out.append(
                f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                f'font-size="11" font-family="{SANS}" font-weight="700" '
                f'fill="{INK}" opacity="0.75">{NY_NAMES[i]}</text>'
            )
        out.append("</svg>")
        return "".join(out)

    def demo_svg(done=(), live=None, lit_nodes=()):
        """The village. `done` are bridges behind you, `live` is the one now."""
        out = [
            '<svg viewBox="0 0 320 224" width="100%" style="max-width:320px;'
            'display:block" xmlns="http://www.w3.org/2000/svg">',
            _PEN,
            '<g filter="url(#lh-pen)">',
        ]
        for y in (66, 128):
            out.append(
                f'<rect x="0" y="{y}" width="320" height="30" fill="{BLUE}" '
                'opacity="0.08"/>'
            )
        for k, d in enumerate(_DM_PATHS):
            if k == live:
                color, width, opacity = RUST, 5.5, 1
            elif k in done:
                color, width, opacity = BLUE, 3.5, 1
            else:
                color, width, opacity = INK, 2.5, 0.2
            out.append(
                f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
                f'opacity="{opacity}" stroke-linecap="round"/>'
            )
        for i, (x, y) in _DM_POS.items():
            out.append(
                f'<circle cx="{x}" cy="{y}" r="13" '
                f'fill="{RUST if i in lit_nodes else PAPER}" '
                f'stroke="{INK}" stroke-width="2.5"/>'
            )
        out.append("</g>")
        for i, (x, y) in _DM_POS.items():
            out.append(
                f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="12" '
                f'font-family="{SANS}" font-weight="700" '
                f'fill="{PAPER if i in lit_nodes else INK}">{i}</text>'
            )
        for i, (x, y) in _DM_LABEL_POS.items():
            anchor = {2: "end"}.get(i, "middle")
            out.append(
                f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                f'font-size="11" font-family="{SANS}" fill="{INK}" opacity="0.7">'
                f"{DEMO_NAMES[i]}</text>"
            )
        out.append("</svg>")
        return "".join(out)

    def demo_edgelist_html(upto, live=None):
        """The village's edge list filling up. Always four lines tall, so it
        never jumps."""
        rows = []
        for k in range(len(DEMO_EDGES)):
            i, j = DEMO_EDGES[k]
            if k == live:
                style = f"color:{RUST};font-weight:700"
            elif k < upto:
                style = f"color:{BLUE}"
            else:
                style = "opacity:0.15"
            text = f"({i}, {j})," if (k < upto or k == live) else "&nbsp;"
            hint = f"  # {DEMO_NOTES[k]}" if k == live else ""
            rows.append(
                f'<div style="{style};line-height:1.7;white-space:pre">    {text}{hint}</div>'
            )
        return (
            f'<div style="font-family:{MONO};font-size:13px;line-height:1.7;'
            f'color:{INK}">bridges = [' + "".join(rows) + "]</div>"
        )

    def matrix_html(A, lit=(), lit_row=None, show_sums=False, names=None):
        """The adjacency matrix as a hand-ruled table."""
        n = len(A)
        lit = set(lit)
        hstyle = (
            f"padding:2px 6px;font-size:11px;font-family:{SANS};"
            "opacity:0.55;font-weight:700"
        )
        head = '<th style="width:24px"></th>' + "".join(
            f'<th style="{hstyle}">{j}</th>' for j in range(n)
        )
        if show_sums:
            head += f'<th style="{hstyle};padding-left:14px">degree</th>'
        rows = [f"<tr>{head}</tr>"]
        for i in range(n):
            hot = i == lit_row
            cells = [
                f'<th style="{hstyle};text-align:right;'
                f'opacity:{0.9 if hot else 0.55}">{i}</th>'
            ]
            for j in range(n):
                if (i, j) in lit:
                    bg, fg = RUST, PAPER
                elif hot:
                    bg, fg = "rgba(57,89,166,0.14)", INK
                else:
                    bg, fg = "transparent", INK
                cells.append(
                    f'<td style="padding:6px 10px;text-align:center;background:{bg};'
                    f"color:{fg};font-family:{MONO};font-size:14px;"
                    f'border:1.5px solid {RULE};border-radius:{WOBBLE}">{int(A[i][j])}</td>'
                )
            if show_sums:
                cells.append(
                    f'<td style="padding:6px 10px 6px 16px;text-align:center;'
                    f"font-weight:700;font-family:{MONO};font-size:14px;"
                    f'color:{RUST if hot else INK};opacity:{1 if hot else 0.45}">'
                    f"{int(sum(A[i]))}</td>"
                )
            rows.append("<tr>" + "".join(cells) + "</tr>")
        html = (
            '<table style="border-collapse:separate;border-spacing:2px;margin:0">'
            + "".join(rows)
            + "</table>"
        )
        if names is not None and lit_row is not None:
            html += (
                f'<div style="margin-top:10px;font-size:14px;font-family:{SANS};'
                f'color:{INK}"><b>{names[lit_row]}</b> &rarr; degree '
                f'<b style="color:{RUST}">{int(sum(A[lit_row]))}</b></div>'
            )
        return html

    def two_col(left, right, left_basis=320):
        return mo.Html(
            '<div style="display:flex;gap:26px;align-items:center;'
            'justify-content:flex-start;flex-wrap:wrap">'
            f'<div style="flex:0 0 {left_basis}px;max-width:100%">{left}</div>'
            f'<div style="flex:0 1 auto">{right}</div></div>'
        )

    def step_slider(stop, label):
        """Short on purpose: full width for seven steps reads as a progress bar
        rather than as something to drag."""
        return mo.ui.slider(0, stop, value=0, label=label, show_value=True)

    def plain_adjacency(edges, n):
        """The kit's own, so the animations run before your code exists."""
        A = np.zeros((n, n), dtype=int)
        for i, j in edges:
            A[i, j] += 1
            A[j, i] += 1
        return A

    def draw(edges, n, title=""):
        """Draw any edge list, in pen. Nodes carry their NUMBER, never their
        name: a long label either runs off the figure or lands on a road. The
        key beside the drawing says which number is which."""
        n = max(n, 1 + max(max(e) for e in edges))
        g = igraph.Graph(n=n, edges=[tuple(e) for e in edges], directed=False)
        g.vs["label"] = [str(i) for i in range(n)]
        igraph.autocurve(g, attribute="curved")
        with plt.rc_context({"path.sketch": (1.6, 70, 2)}):
            fig, ax = plt.subplots(figsize=(5.2, 4.2))
            fig.patch.set_facecolor(PAPER)
            igraph.plot(
                g,
                target=ax,
                layout=g.layout("kk"),
                vertex_size=42,
                vertex_color=PAPER,
                vertex_frame_color=INK,
                vertex_frame_width=2.2,
                vertex_label_size=12,
                vertex_label_color=INK,
                edge_width=2.2,
                edge_color=INK,
                edge_curved=g.es["curved"],
                margin=34,
            )
            ax.set_title(title, color=INK, fontsize=12)
            ax.set_axis_off()
        plt.close(fig)
        return fig

    def key_html(names, deg=None):
        """Which number is which city, and optionally its degree."""
        rows = []
        for i, nm in enumerate(names):
            tail = (
                f'<span style="color:{RUST};font-family:{MONO}">'
                f"&nbsp;&nbsp;{int(deg[i])}</span>"
                if deg is not None
                else ""
            )
            rows.append(
                f'<div style="margin:5px 0;line-height:1.4">'
                f'<b style="font-family:{MONO};color:{BLUE}">{i}</b>&nbsp; {nm}{tail}</div>'
            )
        head = (
            f'<div style="font-size:11px;opacity:0.55;font-weight:700;'
            f'letter-spacing:0.02em">CITY{"  ·  DEGREE" if deg is not None else ""}</div>'
        )
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:14px;color:{INK}">'
            f"{head}{''.join(rows)}</div>"
        )

    def is_connected(A):
        """True if every city can be reached from every other one."""
        g = igraph.Graph.Adjacency(np.asarray(A).tolist(), mode="undirected")
        return g.is_connected()

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">{text}</div>'
        )

    WAITING = mo.Html(
        f'<div style="font-family:{SANS};font-size:15px;color:#6A6D75;'
        f'border:1.5px dashed {RULE};border-radius:{WOBBLE};padding:10px 14px;'
        'display:inline-block">Waiting on the cell above.</div>'
    )

    def roads_ready(roads):
        """True once ROADS is the map on the sheet, in any order."""
        try:
            return sorted(tuple(sorted(e)) for e in roads) == sorted(
                tuple(sorted(e)) for e in NY_EDGES
            )
        except Exception:
            return False

    def adjacency_ready(fn):
        try:
            return np.array_equal(
                fn([(0, 1), (0, 1), (1, 2)], 3),
                np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]]),
            )
        except Exception:
            return False

    def degrees_ready(fn):
        try:
            return list(np.asarray(fn(plain_adjacency(DEMO_EDGES, 3))).ravel()) == [
                3,
                2,
                3,
            ]
        except Exception:
            return False

    def euler_ready(fn):
        try:
            return fn(plain_adjacency([(0, 1), (1, 2), (2, 0)], 3)) == "circuit"
        except Exception:
            return False


@app.cell(hide_code=True)
def _():
    # Stylesheets are global, so one <style> tag in the first cell dresses the
    # whole notebook -- in the editor, in `marimo run`, and in molab.
    mo.Html(f"<style>{LECTURE_HALL_CSS}</style>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part 4 · Hand the map to the machine — worked copy

    **Every ✍️ cell below is filled in.** The blank one, the one the students
    open, is `lab.py` next to this file.

    Every number this notebook asks for is one you have already written in
    pencil. When the screen and the sheet disagree, one of them is wrong, and
    finding out which is the exercise.

    The route of 1(a) is one of several; any of them starts at Ithaca
    and finishes at Albany.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 1 · Write a map down

    A map becomes a **list of pairs** — one line per bridge, one line per road.

    Here is somewhere else first: a village on a river. Three places, numbered
    `0`–`2`, and four bridges. Drag the slider and watch the list fill up:
    """)
    return


@app.cell(hide_code=True)
def _():
    anim1 = step_slider(3, "bridge")
    anim1
    return (anim1,)


@app.cell(hide_code=True)
def _(anim1):
    two_col(
        demo_svg(done=set(range(anim1.value)), live=anim1.value),
        demo_edgelist_html(upto=anim1.value, live=anim1.value),
        left_basis=320,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "Bridge 1 writes <code>(0, 2)</code> a <b>second time</b>. Not a typo — "
        "there really are two bridges there, and a list that mentions them once "
        "is a list of a different village."
        "<br><b>Wherever two places are joined twice, the pair goes in twice.</b>"
        " Your map has a pair like that on it. Find it before you start typing.",
        RUST,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Now your own map

    The four cities and seven highways off the sheet. Nothing below prints its
    edge list: **you read it off the picture.** The number inside a circle is
    the number you write down.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.Html(ny_svg(done=set(range(7))))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ The seven roads

    One is written for you. Add the other six, one line per road. The order does
    not matter; the pairs do.
    """)
    return


@app.cell
def _():
    ROADS = [
        (0, 1),  # NY-13, Ithaca -- Syracuse
        (0, 1),  # NY-34, Ithaca -- Syracuse, the other way round
        (0, 2),  # NY-79, Ithaca -- Binghamton
        (1, 2),  # I-81,  Syracuse -- Binghamton
        (1, 3),  # I-90,  Syracuse -- Albany
        (2, 3),  # I-88,  Binghamton -- Albany
        (2, 3),  # NY-7,  Binghamton -- Albany, the other way round
    ]
    return (ROADS,)


@app.cell(hide_code=True)
def _(ROADS):
    _clean = [e for e in ROADS if isinstance(e, (tuple, list)) and len(e) == 2]
    if roads_ready(_clean):
        _msg = f'<b style="color:{BLUE}">That is the map.</b>'
    elif len(_clean) != 7:
        _msg = (
            f'<b style="color:{RUST}">You have {len(_clean)} roads; the map has '
            "seven.</b>"
        )
    else:
        _deg = plain_adjacency(_clean, 4).sum(axis=1)
        _want = [3, 4, 4, 3]
        _bad = [
            f"{NY_NAMES[i]} touches {int(_deg[i])} of your roads, not {_want[i]}"
            for i in range(4)
            if int(_deg[i]) != _want[i]
        ]
        _msg = f'<b style="color:{RUST}">Not yet.</b>' + (
            '<div style="font-size:14px;opacity:0.75;margin-top:6px">'
            + "; ".join(_bad)
            + " — the counts are Question 3 on the sheet.</div>"
            if _bad
            else '<div style="font-size:14px;opacity:0.75;margin-top:6px">The '
            "degrees are right but the roads are not: two cities are joined by "
            "the wrong number of them.</div>"
        )
    mo.Html(f'<div style="font-family:{SANS};font-size:16px;color:{INK}">{_msg}</div>')
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 2 · Look at it

    The same seven roads, drawn by the machine. It puts the cities wherever it
    likes — **the layout is not geography**, and that is the point: Ithaca is
    still the city with three roads whether you draw it west or upside down.
    """)
    return


@app.cell(hide_code=True)
def _(ROADS):
    if not roads_ready([e for e in ROADS if isinstance(e, (tuple, list))]):
        _out = WAITING
    else:
        _out = mo.hstack(
            [draw(ROADS, 4, "Upstate New York"), key_html(NY_NAMES)],
            widths=[3, 2],
            align="center",
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 3 · Matrix, then degree

    A grid where row `i`, column `j` holds **how many roads join i and j**. It
    is the grid you filled in for Question 5(a). Back to the village, where it
    fits on one screen:
    """)
    return


@app.cell(hide_code=True)
def _():
    anim2 = step_slider(3, "bridge")
    anim2
    return (anim2,)


@app.cell(hide_code=True)
def _(anim2):
    _i, _j = DEMO_EDGES[anim2.value]
    two_col(
        demo_edgelist_html(upto=anim2.value, live=anim2.value),
        matrix_html(
            plain_adjacency(DEMO_EDGES[: anim2.value + 1], 3), lit={(_i, _j), (_j, _i)}
        ),
        left_basis=250,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "A pair is a <b>coordinate</b>. <code>(0, 2)</code> is row 0, column 2."
        "<br>It lights <b>two</b> cells — the grid is a mirror."
        "<br>The second bridge made it <b>2, not 1</b> — add, do not set.",
        RUST,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Fill in the two lines
    """)
    return


@app.function
def to_adjacency(edges, n):
    """A[i, j] = how many roads join city i and city j."""
    A = np.zeros((n, n), dtype=int)
    for i, j in edges:
        A[i, j] += 1
        A[j, i] += 1
    return A


@app.cell(hide_code=True)
def _():
    # Checked on the village, not on their map: a four-by-four grid of the
    # right answer sitting here would be the edge list they were asked to read
    # off the picture, written out in another notation.
    _A = to_adjacency(DEMO_EDGES, 3)
    _ok = isinstance(_A, np.ndarray) and np.array_equal(
        _A, plain_adjacency(DEMO_EDGES, 3)
    )
    two_col(
        matrix_html(_A if isinstance(_A, np.ndarray) else np.zeros((3, 3), int)),
        f'<div style="font-family:{SANS};font-size:16px;color:{INK}">'
        + (
            f'<b style="color:{BLUE}">The village, as a grid.</b>'
            if _ok
            else f'<b style="color:{RUST}">Not yet.</b>'
            '<div style="font-size:14px;opacity:0.75;margin-top:6px">A '
            "<code>1</code> where the animation showed <code>2</code> means you "
            "are setting, not adding. A grid that is not a mirror means you "
            "filled one cell of the two.</div>"
        )
        + "</div>",
        left_basis=200,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Degree** — how many roads touch a place — is now a row, added up. That is
    Question 5(b), and it is also the counting you did in Question 3.
    """)
    return


@app.cell(hide_code=True)
def _():
    anim3 = step_slider(2, "place")
    anim3
    return (anim3,)


@app.cell(hide_code=True)
def _(anim3):
    two_col(
        demo_svg(
            done={k for k, e in enumerate(DEMO_EDGES) if anim3.value in e},
            lit_nodes={anim3.value},
        ),
        matrix_html(
            plain_adjacency(DEMO_EDGES, 3),
            lit_row=anim3.value,
            show_sums=True,
            names=DEMO_NAMES,
        ),
        left_basis=320,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "The island is touched by three bridges and the row adds up to three. "
        "Two of the village's three places are odd, which is the shape of an "
        "answer you have already met on paper.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Degree
    """)
    return


@app.function
def degrees(A):
    """How many roads touch each city.

    One line, no loop: every road at city i left a count somewhere in row i.
    """
    return np.asarray(A).sum(axis=1)


@app.cell(hide_code=True)
def _(ROADS):
    if not (
        roads_ready([e for e in ROADS if isinstance(e, (tuple, list))])
        and adjacency_ready(to_adjacency)
        and degrees_ready(degrees)
    ):
        _out = WAITING
    else:
        _deg = degrees(to_adjacency(ROADS, 4))
        _out = mo.md(
            f"""
    {pd.DataFrame({"city": NY_NAMES, "degree": _deg}).to_markdown(index=False)}

    Degrees add up to **{int(np.sum(_deg))}**, and seven roads must give 14.
    **{int(np.sum(np.asarray(_deg) % 2 == 1))}** cities are odd — the ones you
    marked as having a left-over road.
    """
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 4 · Two-step routes

    Question 5 used a smaller network — four nodes, four lines. On paper you
    numbered them **1 to 4**. Python counts from **0**, so paper node 1 is row
    `0` here, paper node 3 is row `2`, and everything is shifted by one. This is
    the single most common way to get a right answer and read it wrong.
    """)
    return


@app.cell(hide_code=True)
def _():
    if not adjacency_ready(to_adjacency):
        _out = WAITING
    else:
        _A = to_adjacency(SHEET_EDGES, 4)
        _out = mo.hstack(
            [
                mo.vstack(
                    [
                        mo.md("**$A$** — your Question 5(a) grid"),
                        mo.Html(matrix_html(_A)),
                    ]
                ),
                mo.vstack(
                    [
                        mo.md("**$A^2$** — your Question 5(d) prediction"),
                        mo.Html(matrix_html(_A @ _A)),
                    ]
                ),
            ],
            widths=[1, 1],
            align="start",
            gap=2,
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    note(
        "Row 0, column 2 of $A^2$ is the number of 2-step routes from paper node "
        "<b>1</b> to paper node <b>3</b>. Row 0, column 1 says why you could not "
        "find any from 1 to 2. The diagonal is the degrees again — a 2-step "
        "route that comes back is one road out and the same road home.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 5 · The rule

    A drive passing *through* a city uses roads in pairs, so an **odd** city has
    one left over — you must **start** or **end** there. A drive has one start
    and one end.

    | odd cities | you get | return |
    |---|---|---|
    | 0 | drive every road once, finish where you began | `"circuit"` |
    | 2 | drive every road once, finish elsewhere | `"path"` |
    | anything else | nothing | `"impossible"` |

    `"path"` here is Euler's traditional name, not the name from Question 4.
    That drive revisits cities, so by your own table it is a **trail**.

    A map in two pieces is **always** impossible, whatever the degrees say.
    `is_connected(A)` is written for you — check it first.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Euler's rule
    """)
    return


@app.function
def euler_status(A):
    """Return "circuit", "path", or "impossible" for the map A.

    Connectivity first, then the parity of the odd count: a map in two
    pieces has no tour however even every one of its degrees is.
    """
    if not is_connected(A):
        return "impossible"
    odd = int(np.sum(np.asarray(degrees(A)) % 2 == 1))
    if odd == 0:
        return "circuit"
    if odd == 2:
        return "path"
    return "impossible"


@app.cell(hide_code=True)
def _():
    _cases = [
        (DEMO_EDGES, 3, "path"),
        ([(0, 1), (1, 2), (2, 0)], 3, "circuit"),
        ([(0, 1), (2, 3)], 4, "impossible"),  # two pieces: degrees alone lie
    ]
    _ok = all(euler_status(plain_adjacency(_e, _n)) == _w for _e, _n, _w in _cases)
    note(
        "Correct, on the village and on a map in two pieces."
        if _ok
        else "Not yet. The village should say path, a triangle circuit — and two "
        "roads in different worlds impossible, however even the degrees are.",
        BLUE if _ok else RUST,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## The verdict, twice

    Question 1(a) was the seven roads. Question 1(b) added **US-11** beside
    I-81. Your rule now answers both, and it never looked at a picture.
    """)
    return


@app.cell(hide_code=True)
def _(ROADS):
    if not (
        roads_ready([e for e in ROADS if isinstance(e, (tuple, list))])
        and adjacency_ready(to_adjacency)
        and degrees_ready(degrees)
        and euler_ready(euler_status)
    ):
        _out = WAITING
    else:
        _story = {
            "circuit": "Drive every road once and come home.",
            "path": "Drive every road once, but you cannot come home — start at "
            "one odd city and finish at the other.",
            "impossible": "A drive has one start and one end, and that is not "
            "enough left-over roads to go round.",
        }
        _cards = []
        for _title, _edges in [
            ("1(a) · seven roads", list(ROADS)),
            ("1(b) · with US-11", list(ROADS) + [US11_EDGE]),
        ]:
            _A = to_adjacency(_edges, 4)
            _deg = np.asarray(degrees(_A))
            _odd = int(np.sum(_deg % 2 == 1))
            _status = euler_status(_A)
            _cards.append(
                mo.Html(
                    f'<div style="font-family:{SANS};padding-right:26px">'
                    f'<div style="font-size:12px;opacity:0.55;font-weight:700">'
                    f"{_title.upper()}</div>"
                    f'<div style="font-size:32px;font-weight:700;color:{RUST};'
                    f'margin:4px 0">{_status}</div>'
                    f'<div style="font-size:16px;color:{INK}">{_odd} odd cities. '
                    f'{_story.get(_status, "That is not one of the three strings.")}'
                    "</div></div>"
                )
            )
        _out = mo.hstack(_cards, widths=[1, 1], align="start")
    _out
    return


@app.cell(hide_code=True)
def _(ROADS):
    if not roads_ready([e for e in ROADS if isinstance(e, (tuple, list))]):
        _out = WAITING
    else:
        _out = two_col(
            ny_svg(done=set(range(7)), us11=False),
            ny_svg(done=set(range(8)), us11=True),
            left_basis=330,
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Finished early? Break your own rule

    Every place even was supposed to promise a **circuit**: leave home, drive
    every road once, come home. Below is a triangle, which keeps that promise.

    ### ✍️ Break it

    Change the list into a map where **every place still has an even number of
    roads** and there is still **no tour at all**. Nothing here is a trick; the
    counterexample is small.
    """)
    return


@app.cell
def _():
    CHALLENGE = [
        (0, 1),
        (1, 2),
        (2, 0),
        (3, 4),  # a second triangle, with no road to the first
        (4, 5),
        (5, 3),
    ]
    return (CHALLENGE,)


@app.cell(hide_code=True)
def _(CHALLENGE):
    _edges = [
        tuple(e) for e in CHALLENGE if isinstance(e, (tuple, list)) and len(e) == 2
    ]
    if not _edges or not euler_ready(euler_status):
        _out = WAITING
    else:
        _n = 1 + max(max(e) for e in _edges)
        _A = plain_adjacency(_edges, _n)
        _deg = _A.sum(axis=1)
        _even = bool(np.all(_deg % 2 == 0))
        _one_piece = is_connected(_A)
        _says = euler_status(_A)
        if not _even:
            _odds = [str(i) for i in range(_n) if _deg[i] % 2]
            _reading = (
                f"Not yet — place {_odds[0]} has an odd number of roads."
                if len(_odds) == 1
                else f"Not yet — places {', '.join(_odds)} have an odd number "
                "of roads."
            )
            _tone = RUST
        elif _one_piece:
            _reading = (
                "All even and all in one piece, so the promise holds and there "
                "is a circuit. The counterexample is not about parity: ask what "
                "else a tour needs."
            )
            _tone = RUST
        elif _says == "impossible":
            _reading = (
                "Found it. Every degree even, and still no tour, because no "
                "drive gets from one piece to the other — <b>and your rule knew"
                "</b>. That is what <code>is_connected(A)</code> is doing in it."
            )
            _tone = BLUE
        else:
            _reading = (
                f"Found it — and your rule missed it. It says <b>{_says}</b>, "
                "because it counted parities and never asked whether the map is "
                "in one piece. Go back and fix <code>euler_status</code>."
            )
            _tone = RUST
        _facts = "".join(
            f'<div style="margin:7px 0"><span style="opacity:0.55">{_k}</span>'
            f'&nbsp; <b style="font-family:{MONO};color:{RUST}">{_v}</b></div>'
            for _k, _v in [
                ("every degree even", "yes" if _even else "no"),
                ("in one piece", "yes" if _one_piece else "no"),
                ("your euler_status says", _says),
            ]
        )
        _out = mo.vstack(
            [
                mo.hstack(
                    [
                        draw(_edges, _n),
                        mo.Html(
                            f'<div style="font-family:{SANS};font-size:15px;'
                            f'color:{INK}">{_facts}</div>'
                        ),
                    ],
                    widths=[3, 2],
                    align="center",
                ),
                note(_reading, _tone),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Then put it back together and watch the same three lines move. One road
    joining the two halves makes its own two ends odd, so the answer is
    `path`. A second road beside it, between the same two places, makes
    everything even again — and that one is the `circuit`.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
