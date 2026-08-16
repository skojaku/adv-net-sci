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


# A LaTeX command, matched in the SOURCE text (before Python decodes it).
# Naming them one by one is the only way to tell `\times` from a tab and
# `\nu` from a newline: `\\[a-zA-Z]` cannot, and flagging that pattern
# refused every ordinary "line one\n\nline two" markdown in the module.
_LATEX_CMD = re.compile(
    r"\\(frac|dfrac|tfrac|text|mathrm|mathbb|mathcal|times|cdot|to|rightarrow"
    r"|leftarrow|leftrightarrow|approx|sim|propto|neq|leq|geq|ll|gg|infty"
    r"|alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota"
    r"|kappa|lambda|mu|nu|xi|rho|varrho|sigma|tau|upsilon|phi|varphi|chi|psi"
    r"|omega|Gamma|Delta|Theta|Lambda|Sigma|Phi|Psi|Omega"
    r"|sum|prod|int|sqrt|binom|log|ln|exp|min|max|langle|rangle|lvert|rvert"
    r"|bar|hat|tilde|vec|dot|underline|overline|left|right|quad|qquad"
    r"|begin|end|ldots|cdots|dots|forall|exists|in|notin|subset|cup|cap)"
    # NOT \b: a subscript follows a command constantly ($\tau_i$, $\rho_{ij}$),
    # and \b treats `_` as a word character, so every subscripted greek letter
    # slipped through — and \t, \r, \n leave no control character for the
    # backstop below to catch.
    r"(?![A-Za-z])"
)
# Characters no markdown ever wants, and the unmistakable fingerprint of a
# swallowed backslash: \a \b \f \v \0. A LaTeX command outside the list
# above still trips this one.
_EATEN = re.compile(r"[\x00\x07\x08\x0b\x0c]")


def _unraw_markdown(tree, src):
    """An mo.md(...) literal holding LaTeX that is not a raw string.

    `mo.md("$C_i = \\frac{a}{b}$")` is already wrong when Python parses it:
    `\\f` is a formfeed, `\\a` a bell, `\\r` a carriage return. The cell
    renders `C_i = rac{a}{b}` and nothing downstream can recover the text.
    The extension's own note cells are emitted raw for exactly this reason;
    an improvised cell has to ask for the same.

    Ordinary escapes are left alone: `"**A**\\n\\n<span>"` is how half the
    shipped templates write a two-line caption, and making that raw would
    put the two characters backslash-n into the keepsake instead.

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
            if "r" in re.match(r"[A-Za-z]*", seg).group(0).lower():
                continue
            if _LATEX_CMD.search(seg):
                return arg.lineno
            try:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if _EATEN.search(arg.value):
                        return arg.lineno
            except Exception:
                pass
    return None


def _looks_like_ascii_art(lines):
    """Hand-built diagrams, labelled or not.

    A line made ONLY of drawing characters was the original test, and it
    missed the shape a tutor actually improvises: "A---B" over "|   |" over
    "C---D" carries labels, so no line is pure. So a line also counts when
    drawing characters dominate it — three or more of them, and the letters
    and digits a minority. One line is usually a markdown table separator
    (|---|---|), so two are needed before complaining.
    """
    chars = "/\\|_+*.-=~^<>—–─│┌┐└┘├┤┬┴┼"
    # The characters that JOIN two things. A markdown table has plenty of
    # pipes and no connectors, which is what keeps it out of this net.
    connectors = "-_/\\─—–"
    pure = re.compile(r"^[\s" + re.escape(chars) + r"]{3,}$")
    def _table_row(t):
        # "| p | L/L0 | C/C0 |" — pipes around cells that have words in them.
        # A diagram's "|   |" and "|______|" have no letters between the pipes,
        # so they are not exempt. Without this, a results table headed with
        # this module's own notation (L/L0, C/C0, N/k) read as two connectors
        # and got flagged as hand-drawn.
        return t.startswith("|") and t.endswith("|") and t.count("|") >= 2 and any(
            c.isalnum() for c in t
        )

    # The detector reads SOURCE lines, so the first line of a markdown block
    # arrives fused to its call: `mo.md(r"""| N | k | N/k |`. That no longer
    # starts with a pipe, so the table exemption missed it and the prefix's
    # own punctuation pushed it over the bar.
    _open = re.compile(r'^\s*\w*\.?\w*\(\s*[rf]?["\']{1,3}')
    hits = 0
    for ln in lines:
        t = _open.sub("", ln).strip()
        if not t:
            continue
        if _table_row(t):
            continue
        if pure.match(ln):
            hits += 1
            continue
        drawn = sum(1 for c in t if c in chars)
        joined = sum(1 for c in t if c in connectors)
        alnum = sum(1 for c in t if c.isalnum())
        if drawn >= 3 and joined >= 2 and alnum <= max(3, len(t) * 0.4):
            hits += 1
    return hits >= 2


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
            f"{unraw} has a LaTeX command in a NON-raw string, so Python eats "
            "the backslash before marimo ever sees it (\\f, \\a, \\r, \\t) and "
            '$\\frac{a}{b}$ renders as "rac{a}{b}". Write it raw — '
            'mo.md(r\"\"\"...\"\"\"), or rf\"\"\"...\"\"\" for an f-string — with REAL '
            "line breaks inside the triple quotes, not \\n. Then call "
            "nb_add_cell again.",
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
