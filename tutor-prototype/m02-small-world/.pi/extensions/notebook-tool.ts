/**
 * Notebook toolkit for the tutoring session.
 *
 * Gives the tutor agent small, high-level tools (nb_add_cell, nb_edit_cell,
 * nb_delete_cell, nb_read, nb_run) instead of raw bash + marimo code-mode
 * boilerplate. The extension generates the `cm` ceremony itself, which:
 *   - cuts token usage (the model sends only the cell body),
 *   - removes a whole class of errors observed in real sessions:
 *       cold kernel (cells never run)      -> warm-up call before every op
 *       redundant mo/nx/np/plt imports     -> stripped automatically
 *       editing a nonexistent cell         -> pre-check, returns cell list
 *   - keeps the student's terminal quiet: each call renders as one friendly
 *     status line ("📝 Setting up your first question…") with output hidden
 *     behind the expand keybinding. The LLM still receives full output.
 *
 * Also bridges the notebook's ✅ Done buttons to the conversation: the button
 * follower cell (self-contained, no notebook helper needed) writes
 * session_artifacts/student_signal.txt; we watch it and inject a message so
 * the tutor reads the answers right away.
 */
import { execFile } from "node:child_process";
import * as fs from "node:fs";
import path from "node:path";
import { Type } from "typebox";
import { Text } from "@earendil-works/pi-tui";
import { keyHint, type ExtensionAPI } from "@earendil-works/pi-coding-agent";

const SCRIPT_CANDIDATES = [
  ".pi/skills/marimo-pair/scripts/execute-code.sh",
  ".claude/skills/marimo-pair/scripts/execute-code.sh",
];

/** JSON string literals are valid Python string literals. */
const py = (s: string) => JSON.stringify(s);
const pyList = (xs: string[]) => JSON.stringify(xs);
const sanitize = (s: string) => s.replace(/\W/g, "_");

/**
 * The starter notebook already owns mo/nx/np/plt. Models add these imports
 * anyway, which triggers marimo's multiply-defined-name rejection (seen in
 * production) — strip them from submitted cell bodies.
 */
function stripRedundantImports(code: string): string {
  const redundant = [
    /^\s*import marimo as mo\s*$/,
    /^\s*import marimo\s*$/,
    /^\s*import networkx as nx\s*$/,
    /^\s*import numpy as np\s*$/,
    /^\s*import matplotlib\.pyplot as plt\s*$/,
    /^\s*from matplotlib import pyplot as plt\s*$/,
  ];
  return code
    .split("\n")
    .filter((line) => !redundant.some((re) => re.test(line)))
    .join("\n");
}

const BOOTSTRAP =
  `import marimo._code_mode as cm\n` +
  `async with cm.get_context() as ctx:\n` +
  `    for _c in list(ctx.cells):\n` +
  `        ctx.run_cell(_c.id)\n`;

function runKernel(code: string, signal?: AbortSignal): Promise<{ out: string; failed: boolean }> {
  const cwd = process.cwd();
  const script = SCRIPT_CANDIDATES.map((p) => path.join(cwd, p)).find(fs.existsSync);
  if (!script) {
    return Promise.resolve({
      out: "marimo-pair skill scripts not found. Ask the student to restart with ./run_tutor.sh.",
      failed: true,
    });
  }
  const url = process.env.MARIMO_URL || "http://127.0.0.1:2718";
  return new Promise((resolve) => {
    const child = execFile(
      "bash",
      [script, "--url", url, "-"],
      { cwd, timeout: 180_000 },
      (err, stdout, stderr) => {
        const combined = [stdout, stderr].filter(Boolean).join("\n").trim();
        resolve({ out: combined, failed: err != null });
      },
    );
    signal?.addEventListener("abort", () => child.kill());
    child.stdin?.write(code);
    child.stdin?.end();
  });
}

/**
 * Run all notebook cells if the kernel hasn't executed them yet. Must be a
 * SEPARATE kernel call from any cell create/edit: queued runs inside one
 * code-mode context do not reliably execute before a newly created cell
 * (observed in production: new cell ran first and hit NameError on `mo`).
 */
async function ensureWarm(signal?: AbortSignal): Promise<{ out: string; failed: boolean } | null> {
  const probe = await runKernel(`print("OK" if "mo" in globals() else "COLD")`, signal);
  if (probe.failed) return probe;
  if (probe.out.includes("COLD")) {
    const boot = await runKernel(BOOTSTRAP, signal);
    if (boot.failed) return boot;
  }
  return null;
}

function toResult({ out, failed }: { out: string; failed: boolean }) {
  return {
    content: [
      { type: "text" as const, text: failed ? `NOTEBOOK ERROR:\n${out || "(no output)"}` : out || "(ok)" },
    ],
    details: { failed },
  };
}

/** Shared quiet renderers: student sees a status line and a checkmark. */
const quietRender = {
  renderCall(args: { status?: string }, theme: any) {
    const status =
      typeof args?.status === "string" && args.status.length > 0
        ? args.status
        : "Working in the notebook…";
    return new Text(theme.fg("accent", `📝 ${status}`), 0, 0);
  },
  renderResult(result: any, { expanded, isPartial }: any, theme: any) {
    if (isPartial) return new Text(theme.fg("muted", "…"), 0, 0);
    if (result?.details?.failed === true) {
      return new Text(theme.fg("error", "⚠ something hiccuped — your tutor is on it"), 0, 0);
    }
    const raw =
      result?.content
        ?.filter((c: any) => c.type === "text")
        .map((c: any) => c.text ?? "")
        .join("\n")
        .trim() ?? "";
    if (expanded && raw) {
      return new Text(theme.fg("success", "✓") + "\n" + theme.fg("dim", raw), 0, 0);
    }
    let line = theme.fg("success", "✓");
    if (raw && raw !== "(ok)") line += " " + theme.fg("dim", `(${keyHint("app.tools.expand", "for details")})`);
    return new Text(line, 0, 0);
  },
};

const STATUS_PARAM = Type.String({
  description:
    "Short student-facing status in plain, friendly words, e.g. 'Preparing our next step…'. No technical terms, no cell/code/error talk.",
});

const MARIMO_CELL_RULES =
  "Cell code rules (marimo is reactive): " +
  "(1) NEVER read a widget's .value in the cell that creates it — marimo forbids it. " +
  "Pattern: one cell makes and displays the widget (w = mo.ui.slider(…) then w as last line), " +
  "a SECOND cell uses w.value. " +
  "(2) Do NOT import mo/nx/np/plt — they already exist (redundant imports are stripped). " +
  "(3) Each public variable is owned by exactly ONE cell; prefix throwaway names with _ . " +
  "(4) The cell's LAST expression is what gets displayed; markdown via mo.md(r'''…'''). " +
  "(5) A matplotlib figure renders ONLY as the cell's last expression — NEVER interpolate a " +
  "figure into an mo.md f-string (it prints object gibberish, not an image). UI widgets may " +
  "be embedded in mo.md f-strings; figures may not.";

export default function (pi: ExtensionAPI) {
  // ── Done-button bridge ────────────────────────────────────────────────────
  pi.on("session_start", async (_event, _ctx) => {
    const signalPath = path.join(process.cwd(), "session_artifacts", "student_signal.txt");
    try {
      fs.mkdirSync(path.dirname(signalPath), { recursive: true });
      if (!fs.existsSync(signalPath)) fs.writeFileSync(signalPath, "");
      const watcher = fs.watch(signalPath, () => {
        try {
          const checkpoint = fs.readFileSync(signalPath, "utf-8").trim();
          if (!checkpoint) return; // our own clear-write below
          fs.writeFileSync(signalPath, "");
          pi.sendMessage(
            {
              customType: "notebook-done-button",
              content:
                `The student clicked the ✅ Done button in the notebook ` +
                `(checkpoint: ${checkpoint}). Read the relevant notebook values ` +
                `now with nb_read and continue the lesson.`,
              display: true,
            },
            { triggerTurn: true },
          );
        } catch {
          // signal file transiently unavailable — ignore
        }
      });
      // Don't keep the process alive on exit (print mode would hang otherwise).
      watcher.unref();
    } catch {
      // watcher is best-effort; the student can always type "done" instead
    }
  });

  // (Brevity/reveal enforcement lives in say-gate.ts: the say tool's reviewer
  // gates every student-facing message, and plain assistant text is hidden.)

  // ── nb_add_cell ───────────────────────────────────────────────────────────
  pi.registerTool({
    name: "nb_add_cell",
    label: "Add notebook cell",
    description:
      "Create and run a new cell in the live marimo notebook. " +
      MARIMO_CELL_RULES +
      " Set done_signal to a checkpoint id to auto-attach a '✅ Done — tell my tutor!' button " +
      "below the cell (you'll get a message when the student clicks it) — use it whenever the " +
      "cell expects student input (uploads, widget exploration).",
    promptSnippet: "Add and run a cell in the live marimo notebook",
    promptGuidelines: [
      "Use nb_add_cell / nb_edit_cell / nb_delete_cell / nb_read / nb_run for ALL notebook work — never bash, never raw marimo._code_mode boilerplate.",
      "Every nb_* status is shown to the student: short, warm, plain words only.",
    ],
    parameters: Type.Object({
      status: STATUS_PARAM,
      name: Type.String({
        description: "Unique snake_case cell name, e.g. 'cp2_ripple'. Use it later with nb_edit_cell/nb_delete_cell.",
      }),
      code: Type.String({ description: "The cell body (Python)." }),
      show_code: Type.Optional(
        Type.Boolean({
          description: "Show the code editor to the student (default false). Use true for cells whose code the student should read.",
        }),
      ),
      done_signal: Type.Optional(
        Type.String({
          description: "Checkpoint id to signal when the student clicks the auto-added Done button.",
        }),
      ),
    }),
    async execute(_id, params, signal) {
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      const hide = params.show_code === true ? "False" : "True";
      let code =
        `import marimo._code_mode as cm\n` +
        `_code = ${py(stripRedundantImports(params.code))}\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _cid = ctx.create_cell(_code, name=${py(params.name)}, hide_code=${hide})\n` +
        `    ctx.run_cell(_cid)\n`;
      if (params.done_signal) {
        const v = `done_${sanitize(params.done_signal)}`;
        const btnBody = `${v} = mo.ui.run_button(label="✅ Done — tell my tutor!")\n${v}`;
        // Self-contained on purpose: no dependency on notebook helpers, which
        // students (or session saves) can break.
        const sigBody =
          `if ${v}.value:\n` +
          `    from pathlib import Path as _P\n` +
          `    _P("session_artifacts").mkdir(exist_ok=True)\n` +
          `    (_P("session_artifacts") / "student_signal.txt").write_text(${py(params.done_signal)})`;
        code +=
          `    _btn = ctx.create_cell(${py(btnBody)}, name=${py(params.name + "_done_btn")}, hide_code=True, after=_cid)\n` +
          `    ctx.run_cell(_btn)\n` +
          `    _sig = ctx.create_cell(${py(sigBody)}, name=${py(params.name + "_done_sig")}, hide_code=True, after=_btn)\n` +
          `    ctx.run_cell(_sig)\n`;
      }
      return toResult(await runKernel(code, signal));
    },
    ...quietRender,
  });

  // ── nb_add_template ───────────────────────────────────────────────────────
  // Premade, tested cell groups shipped in cells/*.py — the model sends only
  // a template name, so scripted checkpoint builds are instant and bug-free.
  pi.registerTool({
    name: "nb_add_template",
    label: "Insert premade cells",
    description: (() => {
      const dir = path.join(process.cwd(), "cells");
      const names = fs.existsSync(dir)
        ? fs
            .readdirSync(dir)
            .filter((f) => f.endsWith(".py"))
            .map((f) => f.slice(0, -3))
        : [];
      return (
        "Insert a PREMADE, tested group of cells into the notebook instantly — no code to " +
        "write. ALWAYS prefer this over nb_add_cell when a template exists for the " +
        "checkpoint. Available templates: " +
        (names.join(", ") || "(none found)") +
        ". Set done_signal to auto-attach the Done button after the last cell."
      );
    })(),
    promptSnippet: "Insert premade, tested notebook cells by template name (instant)",
    promptGuidelines: [
      "For checkpoint builds use nb_add_template with the template named in lesson.yaml; nb_add_cell is only for detours and improvised cells.",
    ],
    parameters: Type.Object({
      status: STATUS_PARAM,
      template: Type.String({ description: "Template name, e.g. 'cp2_ripple'." }),
      done_signal: Type.Optional(
        Type.String({ description: "Checkpoint id for the auto-attached Done button." }),
      ),
    }),
    async execute(_id, params, signal) {
      const file = path.join(process.cwd(), "cells", `${params.template}.py`);
      if (!fs.existsSync(file)) {
        return toResult({ out: `No template named '${params.template}'.`, failed: true });
      }
      const parts = fs.readFileSync(file, "utf-8").split(/^# --- cell: (\w+) ---[ \t]*$/m);
      const cells: Array<{ name: string; code: string }> = [];
      for (let i = 1; i < parts.length; i += 2) {
        cells.push({ name: parts[i], code: parts[i + 1].trim() });
      }
      if (cells.length === 0) {
        return toResult({ out: `Template '${params.template}' has no cells.`, failed: true });
      }
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      let code =
        `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _names = [c.name for c in ctx.cells]\n` +
        `    if ${py(cells[0].name)} in _names:\n` +
        `        print("template already in the notebook — skipped duplicate insert")\n` +
        `    else:\n` +
        `        _cid = ctx.create_cell(${py(cells[0].code)}, name=${py(cells[0].name)}, hide_code=True)\n` +
        `        ctx.run_cell(_cid)\n`;
      for (const c of cells.slice(1)) {
        code +=
          `        _cid = ctx.create_cell(${py(c.code)}, name=${py(c.name)}, hide_code=True, after=_cid)\n` +
          `        ctx.run_cell(_cid)\n`;
      }
      if (params.done_signal) {
        const v = `done_${sanitize(params.done_signal)}`;
        const btnBody = `${v} = mo.ui.run_button(label="✅ Done — tell my tutor!")\n${v}`;
        const sigBody =
          `if ${v}.value:\n` +
          `    from pathlib import Path as _P\n` +
          `    _P("session_artifacts").mkdir(exist_ok=True)\n` +
          `    (_P("session_artifacts") / "student_signal.txt").write_text(${py(params.done_signal)})`;
        code +=
          `        _cid = ctx.create_cell(${py(btnBody)}, name=${py(params.template + "_done_btn")}, hide_code=True, after=_cid)\n` +
          `        ctx.run_cell(_cid)\n` +
          `        _cid = ctx.create_cell(${py(sigBody)}, name=${py(params.template + "_done_sig")}, hide_code=True, after=_cid)\n` +
          `        ctx.run_cell(_cid)\n`;
      }
      return toResult(await runKernel(code, signal));
    },
    ...quietRender,
  });

  // ── nb_edit_cell ──────────────────────────────────────────────────────────
  pi.registerTool({
    name: "nb_edit_cell",
    label: "Edit notebook cell",
    description:
      "Replace the body of an existing notebook cell (by the name you gave it in nb_add_cell) and re-run it. " +
      "Submit the FULL new body. " + MARIMO_CELL_RULES,
    promptSnippet: "Edit and re-run a cell in the live marimo notebook",
    parameters: Type.Object({
      status: STATUS_PARAM,
      name: Type.String({ description: "The cell's name." }),
      code: Type.String({ description: "The full replacement cell body (Python)." }),
    }),
    async execute(_id, params, signal) {
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      const code =
        `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _names = [c.name for c in ctx.cells]\n` +
        `    if ${py(params.name)} not in _names:\n` +
        `        print("EDIT FAILED: no cell named", ${py(params.name)})\n` +
        `        print("Existing cells:", [n for n in _names if n and n != "_"])\n` +
        `    else:\n` +
        `        ctx.edit_cell(${py(params.name)}, ${py(stripRedundantImports(params.code))})\n` +
        `        ctx.run_cell(${py(params.name)})\n`;
      return toResult(await runKernel(code, signal));
    },
    ...quietRender,
  });

  // ── nb_delete_cell ────────────────────────────────────────────────────────
  pi.registerTool({
    name: "nb_delete_cell",
    label: "Delete notebook cells",
    description:
      "Delete notebook cells by name. Deleting removes the variables those cells define. " +
      "Never delete a cell holding a student's answer.",
    promptSnippet: "Delete cells from the live marimo notebook",
    parameters: Type.Object({
      status: STATUS_PARAM,
      names: Type.Array(Type.String(), { description: "Cell names to delete." }),
    }),
    async execute(_id, params, signal) {
      const code =
        `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _names = [c.name for c in ctx.cells]\n` +
        `    for _n in ${pyList(params.names)}:\n` +
        `        if _n in _names:\n` +
        `            ctx.delete_cell(_n)\n` +
        `        else:\n` +
        `            print("skip: no cell named", _n)\n`;
      return toResult(await runKernel(code, signal));
    },
    ...quietRender,
  });

  // ── nb_read ───────────────────────────────────────────────────────────────
  pi.registerTool({
    name: "nb_read",
    label: "Read notebook values",
    description:
      "Evaluate expressions against the live notebook and return their values — the way to read " +
      "student widget answers, e.g. ['cp6_p.value', 'cp4_photo.value[0].name']. Returns one line per expression.",
    promptSnippet: "Read values/widget answers from the live marimo notebook",
    parameters: Type.Object({
      status: STATUS_PARAM,
      expressions: Type.Array(Type.String(), { description: "Python expressions to evaluate." }),
    }),
    async execute(_id, params, signal) {
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      const code =
        `for _e in ${pyList(params.expressions)}:\n` +
        `    try:\n` +
        `        print(_e, "=", repr(eval(_e)))\n` +
        `    except Exception as _ex:\n` +
        `        print(_e, "!", type(_ex).__name__, str(_ex))\n`;
      return toResult(await runKernel(code, signal));
    },
    ...quietRender,
  });

  // ── nb_run ────────────────────────────────────────────────────────────────
  pi.registerTool({
    name: "nb_run",
    label: "Run Python in notebook kernel",
    description:
      "Escape hatch: run arbitrary Python in the notebook's scratchpad (variables visible, new " +
      "top-level bindings discarded). Use for: appending to the session log, saving uploaded " +
      "photo bytes to session_artifacts/, timestamps (datetime), quick computations. " +
      "NOT for creating/editing cells — use nb_add_cell/nb_edit_cell for that.",
    promptSnippet: "Run scratchpad Python in the notebook kernel (logging, file saves, checks)",
    parameters: Type.Object({
      status: STATUS_PARAM,
      code: Type.String({ description: "Python code to run in the scratchpad." }),
    }),
    async execute(_id, params, signal) {
      return toResult(await runKernel(params.code, signal));
    },
    ...quietRender,
  });
}
