"""Deterministic review for improvised notebook cells (nb_add_cell).

Runs inside the marimo kernel, before the cell is created. It exists because
marimo renders ONLY a cell's last expression: a tutor that writes

    netviz(...)          # the picture
    mo.md("...")         # the caption

silently loses the picture — seen in production, twice in one session. The
review either fixes that (wrapping the displays in one mo.vstack) or refuses
the insert with an instruction, so a broken cell never reaches the student.

_nb_review(src) -> (possibly rewritten src, note for the tutor, fatal error)
A non-empty fatal means: do not create the cell.
"""

import ast
import re

# Expressions marimo will actually render. Deliberately conservative: a call
# whose root is nx/plt/ax/sns (nx.draw_networkx_nodes(...), ax.set_title(...))
# is a side effect, not a display, and must never be swept into a vstack.
_DISPLAY_ROOTS = ("mo", "alt")
_DISPLAY_FUNCS = ("netviz",)


def _renders(node):
    if isinstance(node, ast.Name):  # bare variable: `_fig`, `my_slider`
        return True
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Name):
            return func.id in _DISPLAY_FUNCS
        root = func
        while isinstance(root, ast.Attribute):
            root = root.value
        return isinstance(root, ast.Name) and root.id in _DISPLAY_ROOTS
    return False


def _unraw_markdown(tree, src):
    """An mo.md(...) literal holding LaTeX that is not a raw string.

    `mo.md("$C_i = \\frac{a}{b}$")` is already wrong when Python parses it:
    `\\f` is a formfeed, `\\a` a bell, `\\r` a carriage return. The cell
    renders `C_i = rac{a}{b}` and nothing downstream can recover the text.
    The extension's own note cells are emitted raw for exactly this reason;
    an improvised cell has to ask for the same. Refuse rather than rewrite:
    adding an `r` to a literal that meant `\\n` as a newline would change it.

    Returns the line number of the first offender, or None.
    """
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and node.args):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name != "md":
            continue
        for arg in node.args:
            if not isinstance(arg, (ast.Constant, ast.JoinedStr)):
                continue
            seg = ast.get_source_segment(src, arg) or ""
            prefix = re.match(r"[A-Za-z]*", seg).group(0).lower()
            if "r" in prefix:
                continue
            # A backslash before a letter is LaTeX here — markdown that wants
            # a newline uses a real one.
            if re.search(r"\\[a-zA-Z]", seg):
                return arg.lineno
    return None


def _looks_like_ascii_art(lines):
    """Lines made only of drawing characters — a hand-built diagram.

    One such line is usually a markdown table separator (|---|---|), so
    require two before complaining.
    """
    drawing = re.compile(r"^[\s/\\|_+*.\-=~^<>—–─│┌┐└┘├┤┬┴┼]{3,}$")
    hits = [ln for ln in lines if ln.strip() and drawing.match(ln)]
    return len(hits) >= 2


def _nb_review(src):
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return (
            src,
            "",
            "CELL NOT INSERTED — Python syntax error on line "
            f"{e.lineno}: {e.msg}. Fix it and call nb_add_cell again.",
        )

    unraw = _unraw_markdown(tree, src)
    if unraw is not None:
        return (
            src,
            "",
            "CELL NOT INSERTED — the mo.md(...) text on line "
            f"{unraw} has a backslash command in a NON-raw string, so Python "
            "eats it before marimo ever sees it (\\f, \\a, \\r, \\t) and the "
            'formula renders as "rac{...}". Write it raw — mo.md(r\"\"\"...\"\"\"), '
            'or rf\"\"\"...\"\"\" for an f-string — and call nb_add_cell again.',
        )

    lines = src.split("\n")
    body = tree.body

    # The trailing run of bare expressions: everything marimo could display.
    i = len(body)
    while i > 0 and isinstance(body[i - 1], ast.Expr):
        i -= 1
    run = body[i:]
    displays = [s for s in run if _renders(s.value)]

    # A display stranded earlier in the cell can never render, and moving it
    # is not safe to do automatically.
    early = [s for s in body[:i] if isinstance(s, ast.Expr) and _renders(s.value)]
    if early:
        return (
            src,
            "",
            "CELL NOT INSERTED — marimo renders ONLY the cell's last "
            f"expression, so the display on line {early[0].lineno} would be "
            "silently dropped. Put every display in ONE final "
            "mo.vstack([...]), or split them into separate cells, then call "
            "nb_add_cell again.",
        )

    note = ""
    if len(displays) >= 2:
        if len(displays) != len(run):
            return (
                src,
                "",
                "CELL NOT INSERTED — several displays at the end of the cell "
                "are mixed with side-effect calls, and only the last one would "
                "render. End the cell with a single "
                "mo.vstack([<display>, <display>]) and call nb_add_cell again.",
            )
        # Splice the original source (keeps triple-quoted markdown intact).
        parts = ["\n".join(lines[s.lineno - 1 : s.end_lineno]) for s in run]
        head = lines[: run[0].lineno - 1]
        src = ("\n".join(head) + "\n" if head else "") + (
            "mo.vstack([\n" + ",\n".join(parts) + ",\n])"
        )
        note = (
            f"REVIEW: this cell ended with {len(run)} separate displays — marimo "
            "would have shown only the last one (the figure would have vanished). "
            "Wrapped them in mo.vstack([...]) so they all show. Write it that way "
            "yourself next time."
        )

    if _looks_like_ascii_art(lines):
        note += (
            " REVIEW: this looks like an ASCII-art diagram. Redo it with "
            "netviz(edges, highlight=[...]) — it draws real nodes, edges and "
            "self-loops — and edit the cell with nb_edit_cell."
        )

    return src, note.strip(), ""
