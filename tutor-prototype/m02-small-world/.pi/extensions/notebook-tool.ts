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
 * The student signals "ready" by typing in the terminal — there is no
 * in-notebook Done button; the tutor just reads notebook values with
 * nb_read once the student says they're done.
 */
import { execFile } from "node:child_process";
import * as fs from "node:fs";
import path from "node:path";
import { Type } from "typebox";
import { uuidv7 } from "@earendil-works/pi-ai";
import { complete } from "@earendil-works/pi-ai/compat";
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
    /^\s*import igraph as ig\s*$/,
    /^\s*import seaborn as sns\s*$/,
    /^\s*import altair as alt\s*$/,
    /^\s*import pandas as pd\s*$/,
  ];
  return code
    .split("\n")
    .filter((line) => !redundant.some((re) => re.test(line)))
    .join("\n");
}

/**
 * Ask the browser to bring a cell into view (marimo's focus-cell op) — new
 * content should greet the student, not hide below the fold. Wrapped in
 * try/except so a marimo-internals change can never fail the operation.
 */
const focusCellCode = (cellIdExpr: string, indent: string) =>
  `${indent}try:\n` +
  `${indent}    from marimo._messaging.notification import FocusCellNotification as _FCN\n` +
  `${indent}    ctx.broadcast_raw_notification(_FCN(cell_id=${cellIdExpr}))\n` +
  `${indent}except Exception:\n` +
  `${indent}    pass\n`;

/**
 * Python source of the improvised-cell review (nb_review.py), prepended to
 * the kernel call that creates the cell. Missing file = review skipped.
 */
let reviewSrcCache: string | null = null;
function reviewSource(): string {
  if (reviewSrcCache === null) {
    try {
      reviewSrcCache = fs.readFileSync(
        path.join(process.cwd(), ".pi", "extensions", "nb_review.py"),
        "utf-8",
      );
    } catch {
      reviewSrcCache = "";
    }
  }
  return reviewSrcCache;
}

const indentBlock = (s: string, n: number) =>
  s
    .split("\n")
    .map((l) => (l.trim() ? " ".repeat(n) + l : l))
    .join("\n");

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
  // Guard against a garbage env value (a broken grep once exported
  // "Binary file ... matches" as the URL and every call failed).
  const envUrl = process.env.MARIMO_URL ?? "";
  const url = /^https?:\/\/\S+$/.test(envUrl) ? envUrl : "http://127.0.0.1:2718";
  return new Promise((resolve) => {
    const child = execFile(
      "bash",
      [script, "--url", url, "-"],
      // maxBuffer: nb_view_image pipes a base64 JPEG (~0.5MB) through stdout;
      // node's 1MB default would kill the call mid-stream.
      { cwd, timeout: 180_000, maxBuffer: 16 * 1024 * 1024 },
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

/**
 * The tutor model (deepseek v4 flash) is text-only — nb_view_image delegates
 * "seeing" to a separate vision-capable model. Resolution order:
 *   1. TUTOR_VISION_MODEL env ("provider/model-id", as pi knows it)
 *   2. an image-capable model on the tutor's own provider (same billing)
 *   3. any zero-cost image-capable model (local servers are safe to auto-pick)
 * None found -> the tool tells the tutor to ask for a verbal description.
 */
function resolveVisionModel(ctx: any): any | null {
  const reg = ctx?.modelRegistry;
  if (!reg) return null;
  const all: any[] = reg.getAvailable?.() ?? [];
  const pinned = (process.env.TUTOR_VISION_MODEL ?? "").trim();
  if (pinned.includes("/")) {
    const i = pinned.indexOf("/");
    const m = reg.find?.(pinned.slice(0, i), pinned.slice(i + 1));
    if (m) return m;
    // Router model ids contain slashes themselves ("openrouter/minimax/minimax-m3");
    // accept the full provider/id form or the bare router slug, case-insensitively.
    const want = pinned.toLowerCase();
    const byId = all.find(
      (c) =>
        `${c.provider}/${c.id}`.toLowerCase() === want || String(c.id).toLowerCase() === want,
    );
    if (byId) return byId;
  }
  const canSee = (m: any) => Array.isArray(m?.input) && m.input.includes("image");
  const sameProvider = all.find((m) => canSee(m) && m.provider === ctx?.model?.provider);
  if (sameProvider) return sameProvider;
  return (
    all.find((m) => canSee(m) && m?.cost && m.cost.input === 0 && m.cost.output === 0) ?? null
  );
}

async function describeImage(
  ctx: any,
  b64jpeg: string,
  task: string,
  question: string,
): Promise<{ text: string; model?: string; failed: boolean }> {
  const noVisionAdvice =
    "Ask the student to describe their drawing in words instead (e.g. which dots " +
    "they connected and why), then judge their words — that is a perfectly valid pass.";
  const model = resolveVisionModel(ctx);
  if (!model) {
    return {
      failed: true,
      text:
        `NO VISION MODEL: you are text-only and no vision-capable model is configured ` +
        `(instructor: set TUTOR_VISION_MODEL=provider/model-id). ${noVisionAdvice}`,
    };
  }
  try {
    const auth = await ctx.modelRegistry.getApiKeyAndHeaders(model);
    if (!auth?.ok) throw new Error(auth?.error ?? "no credentials for vision model");
    // A bare "describe the image" fails on messy hand drawings (a chord two
    // steps apart was reported as "already neighbors" in production). The
    // model needs the TASK to know what to look for, and a forced
    // shape-by-shape / line-by-line trace before answering.
    const prompt =
      "You are the eyes of a text-only tutor looking at a student's photo.\n" +
      `What the student was asked to do: ${task}\n` +
      "Work carefully:\n" +
      "1. Count the main shapes (dots, boxes...) and name each by its position — " +
      "clock positions work well for anything arranged in a circle.\n" +
      "2. Trace EVERY line one at a time; for each, name the two things it connects.\n" +
      "3. Then answer the tutor's question using those position names.\n" +
      "If you are unsure about anything, say so explicitly instead of guessing.\n" +
      "Describe only — never grade or judge. Under 150 words.\n" +
      `Tutor's question: ${question}`;
    const response = await complete(
      model,
      {
        messages: [
          {
            role: "user" as const,
            content: [
              { type: "text" as const, text: prompt },
              { type: "image" as const, data: b64jpeg, mimeType: "image/jpeg" },
            ],
            timestamp: Date.now(),
          },
        ],
      },
      {
        apiKey: auth.apiKey,
        headers: auth.headers,
        env: auth.env,
        // Vision models that can think should: tracing lines in a wobbly
        // hand drawing is exactly what fails without it.
        ...(model.reasoning ? { reasoningEffort: "medium" as const } : {}),
        cacheRetention: "none",
        sessionId: uuidv7(),
      },
    );
    const text = (response?.content ?? [])
      .filter((c: any) => c.type === "text")
      .map((c: any) => c.text)
      .join("\n")
      .trim();
    if (!text) throw new Error("vision model returned no text");
    return { failed: false, model: `${model.provider}/${model.id}`, text };
  } catch (e: any) {
    return {
      failed: true,
      text:
        `VISION FAILED (${e?.message ?? e}): you cannot see the image this time. ` +
        `Do not retry more than once and do not debug. ${noVisionAdvice}`,
    };
  }
}

function toResult({ out, failed }: { out: string; failed: boolean }) {
  let text = failed ? `NOTEBOOK ERROR:\n${out || "(no output)"}` : out || "(ok)";
  if (failed) {
    // Tell the model exactly what to do — otherwise it starts "debugging"
    // with skills, shell, and log files in front of the student.
    text += out.includes("No active sessions")
      ? `\nRECOVERY: the notebook tab isn't open in the browser. Ask the student to open ` +
        `or refresh the notebook page, wait for their reply, then retry this call.`
      : `\nRECOVERY: retry this call ONCE. If it fails again, tell the student the ` +
        `whiteboard is unavailable and continue in terminal-only mode (AGENTS.md) — ` +
        `do NOT investigate with skills, shell, or log files.`;
  }
  return {
    content: [{ type: "text" as const, text }],
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

// ── Chapter orchestration (the deterministic "lead agent") ──────────────────
// The lesson is split into chapters (lesson/index.json). The tutor holds only
// the CURRENT chapter's script in context; chapter_done builds a handoff
// brief, injects the next script, and trims the old conversation via
// compaction — same session, same visible transcript, fresh LLM context.
type Chapter = { id: string; file: string; title: string; checkpoints: string[] };

function loadChapters(): Chapter[] {
  try {
    const raw = fs.readFileSync(path.join(process.cwd(), "lesson", "index.json"), "utf-8");
    return (JSON.parse(raw).chapters ?? []) as Chapter[];
  } catch {
    return [];
  }
}

/** Flat checkpoint order across all chapters — the script is the authority. */
function checkpointOrder(): string[] {
  return loadChapters().flatMap((c) => c.checkpoints);
}

/** "cp2_distance_extra" (an improvised practice round) → "cp2_distance". */
function baseCheckpointId(id: string): string {
  return id.replace(/_extra\d*$/, "");
}

function isScriptedCheckpoint(id: string): boolean {
  return checkpointOrder().includes(baseCheckpointId(id));
}

/** The checkpoint the tutor is expected to work next, or null if unknown. */
function nextCheckpointId(id: string): string | null {
  const order = checkpointOrder();
  const i = order.indexOf(baseCheckpointId(id));
  return i >= 0 ? (order[i + 1] ?? null) : null;
}

function chapterScriptMessage(ch: Chapter, num: number, total: number): string {
  const src = fs.readFileSync(path.join(process.cwd(), "lesson", ch.file), "utf-8");
  const last = ch.checkpoints[ch.checkpoints.length - 1];
  return (
    `CHAPTER SCRIPT ${num}/${total} — "${ch.title}" (invisible to the student). ` +
    `This is your curriculum right now:\n\n${src}\n\n` +
    `Work its checkpoints in order, ending each one with checkpoint_done. ` +
    `After checkpoint_done for the final checkpoint (${last}), call chapter_done ` +
    `with short handoff notes.`
  );
}

/**
 * Deterministic notebook structure: a "## Chapter N — Title" markdown cell
 * at every chapter start, so the finished notebook reads as a document the
 * student can re-learn from. Skip-if-exists; cosmetic — never blocks.
 */
async function insertChapterHeader(
  ch: Chapter,
  num: number,
  total: number,
  signal?: AbortSignal,
): Promise<void> {
  try {
    const warm = await ensureWarm(signal);
    if (warm) return;
    const name = `${ch.id}_header`;
    const body = `mo.md(${JSON.stringify(`## Chapter ${num} of ${total} — ${ch.title}`)})`;
    await runKernel(
      `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _names = [c.name for c in ctx.cells]\n` +
        `    if ${py(name)} not in _names:\n` +
        `        _cid = ctx.create_cell(${py(body)}, name=${py(name)}, hide_code=True)\n` +
        `        ctx.run_cell(_cid)\n` +
        focusCellCode("_cid", "        "),
      signal,
    );
  } catch {
    // headers are cosmetic — never block the lesson
  }
}

function chapterStatePath(): string {
  return path.join(process.cwd(), "session_artifacts", "chapter_state.json");
}

function currentChapterId(): string | null {
  try {
    return JSON.parse(fs.readFileSync(chapterStatePath(), "utf-8")).current ?? null;
  } catch {
    return null;
  }
}

function writeChapterState(id: string) {
  try {
    fs.mkdirSync(path.dirname(chapterStatePath()), { recursive: true });
    fs.writeFileSync(chapterStatePath(), JSON.stringify({ current: id }));
  } catch {
    // best-effort
  }
}

function readSessionLog(): any[] {
  try {
    return fs
      .readFileSync(path.join(process.cwd(), "session_artifacts", "session_log.jsonl"), "utf-8")
      .split("\n")
      .filter((l) => l.trim())
      .map((l) => {
        try {
          return JSON.parse(l);
        } catch {
          return null;
        }
      })
      .filter(Boolean);
  } catch {
    return [];
  }
}

function progressBrief(entries: any[]): string {
  const cps = entries.filter((e) => e?.type === "checkpoint" && e.id);
  if (cps.length === 0) return "(no checkpoints logged yet)";
  return cps
    .map(
      (e) =>
        `${e.id}: ${e.judgment ?? "?"}` +
        (e.student_response ? ` — "${String(e.student_response).slice(0, 120)}"` : ""),
    )
    .join("\n");
}

function sessionLogPath(): string {
  return path.join(process.cwd(), "session_artifacts", "session_log.jsonl");
}

/** The tutor no longer hand-writes JSON: the extension owns the graded log. */
function appendLog(entry: Record<string, unknown>): boolean {
  try {
    fs.mkdirSync(path.dirname(sessionLogPath()), { recursive: true });
    fs.appendFileSync(
      sessionLogPath(),
      JSON.stringify({ ts: new Date().toISOString(), ...entry }) + "\n",
    );
    return true;
  } catch {
    return false;
  }
}

/**
 * Ground truth for the graded artifact: the student's own messages, read
 * straight from the transcript, so a logged answer can never drift into
 * paraphrase. Returns what they typed since the previous checkpoint.
 */
let studentSaidMark = 0;
const INJECTED_PREFIX =
  /^(CHAPTER SCRIPT|RESUME CONTEXT|=== TUTORING HANDOFF|The student clicked|Please start the tutoring session|── Chapter )/;

function allStudentMessages(ctx: any): string[] {
  const entries: any[] = ctx?.sessionManager?.getBranch?.() ?? [];
  const out: string[] = [];
  for (const e of entries) {
    if (e?.type !== "message" || e?.message?.role !== "user") continue;
    const c = e.message.content;
    const text =
      typeof c === "string"
        ? c
        : Array.isArray(c)
          ? c
              .filter((p: any) => p?.type === "text" && typeof p.text === "string")
              .map((p: any) => p.text)
              .join("\n")
          : "";
    const s = text.trim();
    if (!s || INJECTED_PREFIX.test(s)) continue;
    out.push(s);
  }
  return out;
}

function studentSaidSince(ctx: any, commit = true): string[] {
  try {
    const all = allStudentMessages(ctx);
    const fresh = all.slice(studentSaidMark);
    if (commit) studentSaidMark = all.length;
    return fresh;
  } catch {
    return [];
  }
}

/**
 * The note cell's «slots» are the graded artifact's centerpiece: they must be
 * the STUDENT's words, not the tutor's prose. A live session produced
 * "A–D = 2, and the average over all 6 pairs = 7/6 ≈ 1.17" from a student who
 * had typed only "yes", "2", "7/6" — a fabricated number presented as their
 * work. So the extension checks the fills against what the student actually
 * said (transcript capture + the tutor's own verbatim field) and refuses once.
 *
 * Tolerant by design: word order, joining and connective words are free; what
 * it catches is invented content — any number they never gave, or several
 * added content words.
 */
const SLOT_GLUE = new Set([
  "a", "an", "and", "the", "of", "to", "in", "on", "at", "is", "are", "was", "were",
  "it", "its", "i", "my", "me", "we", "our", "you", "your", "that", "this", "these",
  "those", "so", "then", "for", "with", "as", "but", "or", "if", "not", "be", "been",
  "there", "here", "each", "every", "both", "than", "when", "because", "about",
]);

function slotTokens(s: string): string[] {
  const norm = s
    .toLowerCase()
    .replace(/[‐-―−]/g, "-")
    .replace(/[*_`>#]/g, " ");
  return norm.match(/[a-z0-9](?:[a-z0-9._/-]*[a-z0-9])?/g) ?? [];
}

/** Content tokens in `fill` that the student never produced. */
function slotDrift(fill: string, studentPool: string[]): { numbers: string[]; words: string[] } {
  const pool = new Set(studentPool.flatMap(slotTokens));
  const numbers: string[] = [];
  const words: string[] = [];
  for (const t of new Set(slotTokens(fill))) {
    if (pool.has(t) || SLOT_GLUE.has(t)) continue;
    if (/\d/.test(t)) numbers.push(t);
    else words.push(t);
  }
  return { numbers, words };
}

/**
 * Pull a checkpoint's instructor-authored `note:` block out of its chapter
 * YAML (block scalar, dedented). The tutor fills «slots», not prose.
 */
function noteSkeleton(cpId: string): string {
  try {
    const chapter = loadChapters().find((c) => c.checkpoints.includes(cpId));
    if (!chapter) return "";
    const lines = fs
      .readFileSync(path.join(process.cwd(), "lesson", chapter.file), "utf-8")
      .split("\n");
    const idRe = new RegExp(`^\\s*-\\s+id:\\s*${cpId}\\s*$`);
    const start = lines.findIndex((l) => idRe.test(l));
    if (start < 0) return "";
    let end = lines.length;
    for (let i = start + 1; i < lines.length; i++) {
      if (/^\s*-\s+id:\s/.test(lines[i])) {
        end = i;
        break;
      }
    }
    for (let i = start; i < end; i++) {
      const m = /^(\s*)note:\s*\|/.exec(lines[i]);
      if (!m) continue;
      const keyIndent = m[1].length;
      const block: string[] = [];
      for (let j = i + 1; j < end; j++) {
        const l = lines[j];
        if (!l.trim()) {
          block.push("");
          continue;
        }
        if (l.length - l.trimStart().length <= keyIndent) break;
        block.push(l);
      }
      const indents = block.filter((l) => l.trim()).map((l) => l.length - l.trimStart().length);
      const base = indents.length ? Math.min(...indents) : 0;
      return block.map((l) => l.slice(base)).join("\n").trim();
    }
    return "";
  } catch {
    return "";
  }
}

/** The «…» markers of a note skeleton, in order. */
function slotMarkers(skeleton: string): string[] {
  return skeleton.match(/«[^»]*»/g) ?? [];
}

function fillSlots(skeleton: string, slots: string[], fallback: string): string {
  let i = 0;
  return skeleton.replace(/«[^»]*»/g, () => {
    const v = slots[i] ?? fallback;
    i += 1;
    return v;
  });
}

/** Insert (or skip, if present) a markdown cell and scroll the page to it. */
async function insertMarkdownCell(
  name: string,
  markdown: string,
  signal?: AbortSignal,
): Promise<{ out: string; failed: boolean }> {
  const warm = await ensureWarm(signal);
  if (warm) return warm;
  const body = `mo.md(${py(markdown)})`;
  return runKernel(
    `import marimo._code_mode as cm\n` +
      `async with cm.get_context() as ctx:\n` +
      `    _names = [c.name for c in ctx.cells]\n` +
      `    if ${py(name)} in _names:\n` +
      `        print("note cell already there — skipped")\n` +
      `    else:\n` +
      `        _cid = ctx.create_cell(${py(body)}, name=${py(name)}, hide_code=True)\n` +
      `        ctx.run_cell(_cid)\n` +
      focusCellCode("_cid", "        "),
    signal,
  );
}

/** The closing record + summary are DERIVED from the log, never retyped. */
function buildSessionRecord(entries: any[]): string {
  const cps = entries.filter((e) => e?.type === "checkpoint" && e.id);
  const detours = entries.filter((e) => e?.type === "detour");
  const lines = [
    "## 📋 Session record",
    "",
    "*Your own words, exactly as you said them — this is what gets reviewed,*",
    "*not the code. Hints are never held against you.*",
    "",
  ];
  for (const e of cps) {
    const hints = Number(e.hints_used ?? 0);
    lines.push(
      `**${e.id}** · ${e.judgment ?? "?"}${hints ? ` · ${hints} hint${hints > 1 ? "s" : ""}` : ""}`,
      "",
      `*${String(e.question ?? "").trim()}*`,
      "",
      `> ${String(e.student_response ?? "").trim().replace(/\n+/g, " ")}`,
      "",
    );
    if (e.notes) lines.push(`${String(e.notes).trim()}`, "");
  }
  if (detours.length) {
    lines.push(`### 🧭 Your own questions (${detours.length})`, "");
    for (const d of detours) lines.push(`- *${String(d.question ?? "").trim()}*`);
    lines.push("");
  }
  return lines.join("\n");
}

function buildSessionSummary(entries: any[], allCheckpoints: string[]): string {
  const cps = entries.filter((e) => e?.type === "checkpoint" && e.id);
  const done = new Set(cps.map((e) => e.id));
  const missing = allCheckpoints.filter((id) => !done.has(id));
  const out = [
    "# Session summary",
    "",
    `Checkpoints completed: ${done.size} of ${allCheckpoints.length}`,
    `Detours (student's own questions): ${entries.filter((e) => e?.type === "detour").length}`,
    "",
  ];
  for (const e of cps) {
    out.push(
      `## ${e.id} — ${e.judgment ?? "?"} (${Number(e.hints_used ?? 0)} hints)`,
      `Question: ${String(e.question ?? "").trim()}`,
      `Answer (verbatim): ${String(e.student_response ?? "").trim()}`,
    );
    if (Array.isArray(e.student_said_verbatim) && e.student_said_verbatim.length) {
      out.push(`Typed by the student: ${JSON.stringify(e.student_said_verbatim)}`);
    }
    if (e.notes) out.push(`Tutor's note: ${String(e.notes).trim()}`);
    out.push("");
  }
  if (missing.length) {
    out.push(`## Where to pick up`, `Next checkpoint: ${missing[0]}`, "");
  }
  return out.join("\n");
}

const JUDGMENTS = ["pass", "pass_with_hints", "guided", "prediction"];

const MARIMO_CELL_RULES =
  "Cell code rules (marimo is reactive): " +
  "(1) NEVER read a widget's .value in the cell that creates it — marimo forbids it. " +
  "Pattern: one cell makes and displays the widget (w = mo.ui.slider(…) then w as last line), " +
  "a SECOND cell uses w.value. " +
  "(2) Do NOT import mo/nx/np/plt/ig/sns/alt/pd — they already exist (redundant imports are " +
  "stripped); netviz(edges, highlight=[...]) is also predefined for themed D3 network drawings. " +
  "(3) Each public variable is owned by exactly ONE cell; prefix throwaway names with _ . " +
  "(4) The cell's LAST expression is what gets displayed; markdown via mo.md(r'''…'''). " +
  "(5) A matplotlib figure renders ONLY as the cell's last expression — NEVER interpolate a " +
  "figure into an mo.md f-string (it prints object gibberish, not an image). UI widgets may " +
  "be embedded in mo.md f-strings; figures may not. " +
  "(6) Text AND a figure in ONE cell: end with mo.vstack([mo.md(r'''…'''), <figure or " +
  "netviz(...)>]). NEVER draw a diagram as ASCII art inside markdown — a tiny netviz " +
  "(it even draws self-loops) or matplotlib figure always looks better.";

export default function (pi: ExtensionAPI) {
  // Guards against a checkpoint's build landing in the wrong place: if the
  // tutor starts building checkpoint B before closing checkpoint A with
  // checkpoint_done, A's note cell gets created LATE and lands after B's
  // build cells instead of before them (seen in production — a "welcome"
  // note appeared after the next checkpoint's image). nb_add_template (and
  // nb_add_exercise, when tagged) check this before inserting.
  //
  // The open checkpoint is armed from the SCRIPT, not from the build: a
  // checkpoint with `build: none` (cp0_welcome, cp5_tension) never inserts a
  // cell, so arming on insert left exactly those unguarded — which is how
  // cp0's welcome note landed after cp1's image. Armed at session start and
  // advanced to the next scripted id by checkpoint_done.
  let pendingCheckpoint: string | null = null;
  // A slot-drift refusal fires at most once per checkpoint, so a model that
  // cannot satisfy it can never trap the student in a retry loop.
  const slotDriftWarned = new Set<string>();

  pi.on("session_start", async (_event, _ctx) => {
    // ── Chapter start + resume brief ──────────────────────────────────────
    // Determine the current chapter (from progress or saved state), inject
    // its script, and — when previous progress exists — a resume brief that
    // asks the student continue-or-fresh.
    try {
      const chapters = loadChapters();
      if (chapters.length > 0) {
        const entries = readSessionLog();
        const cps = entries.filter((e: any) => e.type === "checkpoint" && e.id);
        let chapter =
          chapters.find((c) => c.id === currentChapterId()) ?? chapters[0];
        pendingCheckpoint = chapter.checkpoints[0] ?? null;
        if (cps.length > 0) {
          const order = chapters.flatMap((c) => c.checkpoints);
          const lastId = baseCheckpointId(cps[cps.length - 1].id);
          const nextId = order[order.indexOf(lastId) + 1] ?? order[order.length - 1];
          chapter = chapters.find((c) => c.checkpoints.includes(nextId)) ?? chapter;
          pendingCheckpoint = nextId;
          pi.sendMessage(
            {
              customType: "resume-brief",
              content:
                `RESUME CONTEXT (invisible to the student — never mention this message): ` +
                `a previous session exists. Progress so far:\n${progressBrief(entries)}\n` +
                `FIRST, greet the student and ask with ask_user_question: continue where you left ` +
                `off, or start fresh? If they choose fresh: call nb_fresh_start and follow ` +
                `its instructions (chapter 1 reloads automatically — do not improvise). ` +
                `If they continue: do NOT rebuild existing notebook cells ` +
                `(nb_add_template skips duplicates automatically), remind them in one ` +
                `sentence where you two left off, and continue at checkpoint ${nextId} ` +
                `(chapter "${chapter.title}").`,
              display: false,
            },
            { deliverAs: "nextTurn" },
          );
        }
        writeChapterState(chapter.id);
        const num = chapters.findIndex((c) => c.id === chapter.id) + 1;
        pi.sendMessage(
          {
            customType: "chapter-script",
            content: chapterScriptMessage(chapter, num, chapters.length),
            display: false,
          },
          { deliverAs: "nextTurn" },
        );
        // Delayed: the kernel is likely still booting at session start. Guard
        // against staleness — if the student chose "start fresh" (or a
        // chapter transition otherwise happened) before this fires, the
        // chapter this timer was scheduled for is no longer current, and
        // inserting its header would land a stray "Chapter N" heading in
        // the middle of a different chapter's cells (seen in production).
        const scheduledForChapterId = chapter.id;
        const headerTimer = setTimeout(() => {
          if (currentChapterId() !== scheduledForChapterId) return;
          void insertChapterHeader(chapter, num, chapters.length);
        }, 15_000);
        (headerTimer as any).unref?.();
      }
    } catch {
      // chapter injection is best-effort; AGENTS.md tells the tutor how to cope
    }
  });

  // Chapter dividers render as a single accent line in the transcript.
  pi.registerMessageRenderer("chapter-divider", (message: any, _opts: any, theme: any) => {
    return new Text(theme.fg("accent", String(message.content ?? "")), 0, 0);
  });

  // Custom compaction at chapter boundaries: the handoff brief IS the summary
  // (deterministic, no extra LLM call).
  let pendingHandoffBrief: string | null = null;
  pi.on("session_before_compact", async (event: any) => {
    if (!pendingHandoffBrief) return;
    const summary = pendingHandoffBrief;
    pendingHandoffBrief = null;
    return {
      compaction: {
        summary,
        firstKeptEntryId: event.preparation.firstKeptEntryId,
        tokensBefore: event.preparation.tokensBefore,
      },
    };
  });

  // ── chapter_done ──────────────────────────────────────────────────────────
  pi.registerTool({
    name: "chapter_done",
    label: "Chapter done",
    description:
      "Call when the current chapter's FINAL checkpoint has been logged. Pass short handoff " +
      "notes for the next part of the lesson (student's style, anchors worth reusing like " +
      "'their cable was the long one', anything to watch). The next chapter script loads " +
      "automatically — after calling, say ONE short bridge sentence and wait.",
    promptSnippet: "Finish the current chapter and load the next (with handoff notes)",
    parameters: Type.Object({
      status: STATUS_PARAM,
      handoff: Type.String({
        description: "2-4 sentences: student profile updates, anchors, watch-outs.",
      }),
    }),
    async execute(_id, params, _signal, _onUpdate, ctx: any) {
      const chapters = loadChapters();
      const curId = currentChapterId() ?? chapters[0]?.id;
      const idx = chapters.findIndex((c) => c.id === curId);
      const next = chapters[idx + 1];

      // ── Forced chapter-end follow-up ────────────────────────────────────
      // Enforced here, not by prompt: a chapter boundary is the one moment
      // the student must get an unhurried "anything first?" — the tutor was
      // racing past questions and requests for extra practice.
      const READY = next ? "I'm ready for the next chapter" : "I'm ready to wrap up";
      const ASK_Q = "I have a question first";
      const MORE = "Give me one more practice problem";
      if (ctx?.ui?.select) {
        const title = chapters[idx]?.title ?? "this part";
        const choice = await ctx.ui.select(`Before we leave "${title}" — anything first?`, [
          READY,
          ASK_Q,
          MORE,
        ]);
        if (choice !== READY) {
          const text =
            choice === ASK_Q
              ? `The student has a QUESTION. Do NOT advance. Ask them in plain text what it ` +
                `is, answer it properly, leave a souvenir cell (mo.vstack: note + netviz/figure ` +
                `— never ASCII art), log the detour, then call chapter_done again.`
              : choice === MORE
                ? `The student wants MORE PRACTICE. Do NOT advance. Improvise ONE problem of ` +
                  `the same kind on NEW data, reusing this module's objects (the 4-person ` +
                  `network, the 8-dot ring) so the numbers stay comparable. Guide, judge, log ` +
                  `it as extra practice (never a fail), then call chapter_done again.`
                : `The student closed the picker without choosing — they may want to say ` +
                  `something in their own words. Ask them in plain text what they'd like to do, ` +
                  `handle it, then call chapter_done again.`;
          return { content: [{ type: "text" as const, text }], details: { gated: true } };
        }
      }

      if (!next) {
        // The closing artifacts are DERIVED from the log — never retyped from
        // the model's memory of the session (that is the graded record).
        const entries = readSessionLog();
        const allCps = chapters.flatMap((c) => c.checkpoints);
        let done = "";
        const rec = await insertMarkdownCell("session_record", buildSessionRecord(entries), _signal);
        done += rec.failed ? "session_record cell FAILED. " : "Closing record added to their notebook. ";
        try {
          fs.writeFileSync(
            path.join(process.cwd(), "session_artifacts", "session_summary.md"),
            buildSessionSummary(entries, allCps),
          );
          done += "Summary written. ";
        } catch {
          done += "Summary write failed. ";
        }
        return {
          content: [
            {
              type: "text" as const,
              text:
                `That was the FINAL chapter. ${done}Nothing to write yourself — just say ` +
                `goodbye: tell them plainly what they can now do, that their answers (not ` +
                `code) are what gets reviewed, and that the notebook is theirs to keep and ` +
                `keep playing with.`,
            },
          ],
          details: {},
        };
      }
      writeChapterState(next.id);
      const brief =
        `=== TUTORING HANDOFF (chapter transition, invisible to the student) ===\n` +
        `You are the SAME tutor, mid-session. Conversation so far, summarized:\n` +
        `Progress:\n${progressBrief(readSessionLog())}\n` +
        `Tutor's notes: ${params.handoff}\n` +
        `The notebook already contains every cell built so far — never rebuild them. ` +
        `Continue warmly with the same voice; your new CHAPTER SCRIPT message has the curriculum.`;
      pendingHandoffBrief = brief;
      // The next chapter must load AFTER compaction: injecting before it
      // races the session reload (the fresh turn gets aborted and nothing
      // restarts — seen in production) and the script could be summarized
      // away. loadOnce also serves as the fallback when compaction errors
      // (e.g. nothing to compact) or never calls back.
      const num = idx + 2;
      let loaded = false;
      const loadOnce = () => {
        if (loaded) return;
        loaded = true;
        void insertChapterHeader(next, num, chapters.length);
        pi.sendMessage(
          {
            customType: "chapter-divider",
            content: `── Chapter ${num} · ${next.title} ──`,
            display: true,
          },
          { deliverAs: "followUp" },
        );
        pi.sendMessage(
          {
            customType: "chapter-script",
            content: chapterScriptMessage(next, num, chapters.length),
            display: false,
          },
          { deliverAs: "followUp", triggerTurn: true },
        );
      };
      try {
        ctx?.compact?.({
          customInstructions: "chapter handoff",
          onComplete: loadOnce,
          onError: () => {
            pendingHandoffBrief = null;
            loadOnce();
          },
        });
        const timer = setTimeout(loadOnce, 20_000);
        (timer as any).unref?.();
      } catch {
        pendingHandoffBrief = null;
        loadOnce();
      }
      return {
        content: [
          {
            type: "text" as const,
            text:
              `Handoff recorded. Say ONE short, warm bridge sentence to the student ` +
              `(no new questions) and END YOUR TURN — chapter "${next.title}" loads automatically.`,
          },
        ],
        details: {},
      };
    },
    ...quietRender,
  });

  // ── Runaway guard ─────────────────────────────────────────────────────────
  // Silent safety net only (style is steered by AGENTS.md, not enforced):
  // flash-class models can fall into degenerate repetition loops. Abort the
  // generation if a single message runs absurdly long, and nudge a restart.
  const RUNAWAY_CHARS = 1600;
  let runawayFired = false;
  pi.on("message_update", async (event: any, ctx: any) => {
    const msg = event?.message;
    if (msg?.role !== "assistant" || runawayFired) return;
    const raw = msg.content;
    const t =
      typeof raw === "string"
        ? raw
        : (Array.isArray(raw) ? raw : [])
            .filter((c: any) => c?.type === "text")
            .map((c: any) => c.text ?? "")
            .join("\n");
    if (t.length <= RUNAWAY_CHARS) return;
    runawayFired = true;
    try {
      ctx.abort();
    } catch {
      // best-effort
    }
    pi.sendMessage(
      {
        customType: "runaway-guard",
        content:
          "NOTE (invisible to the student): your message ran away and was cut off. " +
          "Continue with one short message.",
        display: false,
      },
      { deliverAs: "followUp", triggerTurn: true },
    );
  });
  pi.on("message_end", async () => {
    runawayFired = false;
  });

  // Fixed-choice questions go through the ask_user_question tool
  // (@juicesharp/rpiv-ask-user-question package, declared in .pi/settings.json).

  // ── checkpoint_done ───────────────────────────────────────────────────────
  // One call replaces the whole per-checkpoint ceremony: the extension writes
  // the graded log (with the student's own messages captured from the
  // transcript), renders the note cell from the chapter script's `note:`
  // skeleton, and runs the transition ask itself. The tutor supplies only
  // what a model can: the verbatim answer and the judgment.
  pi.registerTool({
    name: "checkpoint_done",
    label: "Checkpoint done",
    description:
      "Finish a checkpoint: this ONE call logs it (graded artifact), adds the notebook note " +
      "cell from the chapter script's note: skeleton, and asks the student whether to move " +
      "on. Call it right after you judge their answer — never hand-write log JSON, never " +
      "hand-write the note cell. The result tells you what the student chose: only 'ready' " +
      "means you may start the next checkpoint.",
    promptSnippet: "Log a checkpoint, add its note cell, and ask the student what's next",
    promptGuidelines: [
      "End EVERY checkpoint with checkpoint_done — it replaces hand-written log JSON, the note cell, and the transition question.",
    ],
    parameters: Type.Object({
      status: STATUS_PARAM,
      id: Type.String({ description: "Checkpoint id from the script, e.g. 'cp2_distance'." }),
      question: Type.String({ description: "The question as you actually asked it." }),
      student_response: Type.String({
        description: "Their answer VERBATIM — their words, not your summary.",
      }),
      judgment: Type.String({
        description: "One of: pass | pass_with_hints | guided | prediction.",
      }),
      hints_used: Type.Number({ description: "How many hints you gave (0 is fine and normal)." }),
      notes: Type.String({ description: "One line: what their answer showed." }),
      note_slots: Type.Optional(
        Type.Array(Type.String(), {
          description:
            "Fills for the «slots» in the script's note: skeleton, in order (usually the " +
            "student's own words). Missing ones default to student_response.",
        }),
      ),
      note_markdown: Type.Optional(
        Type.String({
          description:
            "Only when the script has no note: skeleton — the full note cell markdown " +
            "(plain-words title, 2-4 sentences with $math$, then their quoted answer).",
        }),
      ),
    }),
    async execute(_id, params, signal, _onUpdate, ctx: any) {
      const id = String(params.id ?? "").trim();
      const judgment = String(params.judgment ?? "").trim();
      if (!JUDGMENTS.includes(judgment)) {
        return toResult({
          out: `NOT LOGGED — judgment must be one of ${JUDGMENTS.join(" | ")}, got "${judgment}". Call again.`,
          failed: false,
        });
      }
      const response = String(params.student_response ?? "").trim();
      if (!response) {
        return toResult({
          out: `NOT LOGGED — student_response is empty. Log their actual words (or "(no answer — moved on)") and call again.`,
          failed: false,
        });
      }
      // Peek, don't consume: a refusal below must leave the transcript mark
      // where it was, or the retry would log an empty student_said_verbatim.
      const said = studentSaidSince(ctx, false);
      const slots = (params.note_slots ?? []).map((s: unknown) => String(s ?? ""));
      const pool = [...said, response];
      // Only slots the instructor marked «… verbatim» are held to the
      // student's exact words; «their pick» (a dialog choice) and free
      // commentary slots are the tutor's to phrase.
      const markers = slotMarkers(noteSkeleton(id));
      const drifted = slots
        .map((fill, i) => ({ i, fill, drift: slotDrift(fill, pool) }))
        .filter(
          (d) =>
            /verbatim/i.test(markers[d.i] ?? "") &&
            (d.drift.numbers.length > 0 || d.drift.words.length >= 2),
        );
      if (drifted.length > 0 && !slotDriftWarned.has(id)) {
        slotDriftWarned.add(id);
        const offenders = drifted
          .map(
            (d) =>
              `slot ${d.i + 1} ("${d.fill.slice(0, 80)}") adds ` +
              [...d.drift.numbers, ...d.drift.words].map((t) => `"${t}"`).join(", "),
          )
          .join("; ");
        return toResult({
          out:
            `NOT LOGGED — a note «slot» is the student's own words, and these are not in ` +
            `anything they said: ${offenders}.\nWhat they actually said: ` +
            `${pool.map((s) => `"${s}"`).join(", ")}.\nRewrite the slots with only their ` +
            `words — quote, don't polish, and never add a number they didn't give — then ` +
            `call checkpoint_done again.`,
          failed: false,
        });
      }
      // The next scripted checkpoint is now the open one, even if it builds
      // nothing — that is what keeps its note cell ahead of the next build.
      pendingCheckpoint = nextCheckpointId(id);
      studentSaidSince(ctx, true);

      const logged = appendLog({
        type: "checkpoint",
        id,
        question: String(params.question ?? ""),
        student_response: response,
        judgment,
        hints_used: Number(params.hints_used ?? 0),
        notes: String(params.notes ?? ""),
        student_said_verbatim: said,
        ...(drifted.length > 0 ? { note_slot_drift: true } : {}),
      });

      const skeleton = noteSkeleton(id);
      const md = skeleton
        ? fillSlots(skeleton, params.note_slots ?? [], response)
        : String(params.note_markdown ?? "").trim();
      let noteLine: string;
      if (!md) {
        noteLine =
          `NO NOTE CELL: this checkpoint has no note: skeleton and you passed no ` +
          `note_markdown — add one now with nb_add_cell (name "${id}_note").`;
      } else {
        const r = await insertMarkdownCell(`${id}_note`, md, signal);
        noteLine = r.failed
          ? `Note cell FAILED — retry once with nb_add_cell (name "${id}_note").`
          : `Note cell added.`;
      }

      const READY = "Ready for the next question";
      const ASK_Q = "I have a question first";
      const MORE = "Give me another one like that";
      let nextLine =
        `No picker available — ask the student in plain text whether to move on, ` +
        `and wait for their answer.`;
      if (ctx?.ui?.select) {
        const choice = await ctx.ui.select("Where to next?", [READY, ASK_Q, MORE]);
        nextLine =
          choice === READY
            ? `The student is READY — start the next checkpoint from your script.`
            : choice === ASK_Q
              ? `The student has a QUESTION. Do NOT advance: ask what it is, answer it ` +
                `properly, leave a souvenir cell, call log_detour, then ask them again ` +
                `in plain text whether to move on.`
              : choice === MORE
                ? `The student wants MORE PRACTICE. Do NOT advance: improvise ONE problem ` +
                  `of the same kind on NEW data, reusing this module's objects (the 4-person ` +
                  `network, the 8-dot ring) so the numbers stay comparable. Guide, then ` +
                  `checkpoint_done again with id "${id}_extra" (never a fail).`
                : `The student closed the picker — ask in plain text what they'd like to do.`;
      }

      return toResult({
        out:
          `Logged${logged ? "" : " (LOG WRITE FAILED — tell no one, keep teaching)"}. ` +
          `${noteLine}\n${nextLine}`,
        failed: false,
      });
    },
    ...quietRender,
  });

  // ── log_detour ────────────────────────────────────────────────────────────
  pi.registerTool({
    name: "log_detour",
    label: "Log detour",
    description:
      "Record a student question you answered off-script (their curiosity is graded as " +
      "engagement) and leave the souvenir in their notebook. Pass souvenir_markdown for a " +
      "text-only souvenir; if you already built a richer cell with nb_add_cell, pass its " +
      "cell_name instead.",
    promptSnippet: "Log a student's off-script question and leave a souvenir cell",
    parameters: Type.Object({
      status: STATUS_PARAM,
      question: Type.String({ description: "Their question VERBATIM." }),
      what_you_did: Type.String({ description: "One line: how you answered it." }),
      souvenir_markdown: Type.Optional(
        Type.String({ description: "Markdown for a 🧭 Detour note cell (quote their question)." }),
      ),
      cell_name: Type.Optional(
        Type.String({ description: "Name of the souvenir cell you already added." }),
      ),
    }),
    async execute(_id, params, signal, _onUpdate, ctx: any) {
      const question = String(params.question ?? "").trim();
      appendLog({
        type: "detour",
        question,
        what_you_did: String(params.what_you_did ?? ""),
        cell: String(params.cell_name ?? ""),
        student_said_verbatim: studentSaidSince(ctx),
      });
      const md = String(params.souvenir_markdown ?? "").trim();
      if (!md) {
        return toResult({
          out: params.cell_name
            ? `Logged. Souvenir cell "${params.cell_name}" noted.`
            : `Logged — but NO souvenir cell yet. Add one now (nb_add_cell, name ` +
              `"detour_<topic>"): their question quoted plus the idea, with a picture ` +
              `(mo.vstack + netviz) when one helps.`,
          failed: false,
        });
      }
      const slug = sanitize(question.toLowerCase().split(/\s+/).slice(0, 4).join("_")).slice(0, 40);
      const r = await insertMarkdownCell(`detour_${slug || "note"}`, md, signal);
      return toResult({
        out: r.failed ? `Logged. Souvenir cell FAILED — add it with nb_add_cell.` : `Logged and the souvenir is in their notebook.`,
        failed: false,
      });
    },
    ...quietRender,
  });

  // ── nb_add_cell ───────────────────────────────────────────────────────────
  pi.registerTool({
    name: "nb_add_cell",
    label: "Add notebook cell",
    description:
      "Create and run a new cell in the live marimo notebook. " +
      MARIMO_CELL_RULES,
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
    }),
    async execute(_id, params, signal) {
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      const hide = params.show_code === true ? "False" : "True";
      let inner =
        `async with cm.get_context() as ctx:\n` +
        `    _cid = ctx.create_cell(_code, name=${py(params.name)}, hide_code=${hide})\n` +
        `    ctx.run_cell(_cid)\n`;
      inner += focusCellCode("_cid", "    ");
      // Improvised cells go through the review (nb_review.py) — it catches the
      // displays marimo would silently drop before the student sees a cell
      // with a missing figure.
      const review = reviewSource();
      const code =
        `import marimo._code_mode as cm\n` +
        (review ? review + "\n" : "") +
        `_code = ${py(stripRedundantImports(params.code))}\n` +
        (review
          ? `_code, _note, _fatal = _nb_review(_code)\n` +
            `if _fatal:\n` +
            `    print(_fatal)\n` +
            `else:\n` +
            indentBlock(inner, 4) +
            `    if _note:\n` +
            `        print(_note)\n`
          : inner);
      return toResult(await runKernel(code, signal));
    },
    ...quietRender,
  });

  // ── nb_add_exercise ───────────────────────────────────────────────────────
  // Fill-in coding, app-view friendly: instructions + a pre-filled code box
  // (mo.ui.code_editor) + a ▶ Run button that executes via the notebook's
  // run_student_code helper (stdout + last expression, friendly errors).
  // The student never needs the cell editor.
  pi.registerTool({
    name: "nb_add_exercise",
    label: "Add coding exercise",
    description:
      "Give the student a fill-in coding exercise INSIDE the notebook page: instructions, " +
      "a code box pre-filled with your scaffold (numbered # steps with ... blanks), and a " +
      "▶ Run button that executes it and shows output or a friendly error. They can run as " +
      "often as they like. Read their attempt with nb_read('<name>_ed.value'). env_vars " +
      "lists notebook variables their code may use (e.g. a graph G you set up earlier). " +
      "ALWAYS use this instead of asking the student to edit cells. Pass checkpoint when this " +
      "exercise IS a checkpoint's build (not a detour) — lets the tool catch a checkpoint you " +
      "started but never closed with checkpoint_done.",
    promptSnippet: "Insert a fill-in coding exercise (code box + Run button) into the notebook",
    parameters: Type.Object({
      status: STATUS_PARAM,
      name: Type.String({ description: "Base name, e.g. 'cs1_code'." }),
      instructions: Type.String({
        description: "1-3 sentences shown above the code box (markdown, $math$ ok).",
      }),
      scaffold: Type.String({
        description: "Pre-filled Python: numbered # instructions + ... blanks to fill.",
      }),
      env_vars: Type.Optional(
        Type.Array(Type.String(), {
          description: "Notebook variable names the student's code may use.",
        }),
      ),
      checkpoint: Type.Optional(
        Type.String({
          description: "Checkpoint id this build is for, e.g. 'cp6_large_n_experiment'. Omit for detours.",
        }),
      ),
    }),
    async execute(_id, params, signal) {
      const name = String(params.name ?? "").trim();
      if (!/^[A-Za-z_]\w*$/.test(name)) {
        return toResult({ out: `'${name}' is not a valid cell name.`, failed: true });
      }
      // Stretch/off-script ids (cs1_code) are not in the chapter order and are
      // deliberately unguarded — the guard only enforces the scripted sequence.
      const exCpId = baseCheckpointId(String(params.checkpoint ?? "").trim());
      if (exCpId && isScriptedCheckpoint(exCpId) && pendingCheckpoint && pendingCheckpoint !== exCpId) {
        return toResult({
          out:
            `NOT INSERTED — checkpoint '${pendingCheckpoint}' is still open. ` +
            `Call checkpoint_done for '${pendingCheckpoint}' first (its note cell must land ` +
            `before this build), then retry this insert.`,
          failed: false,
        });
      }
      const envVars = (params.env_vars ?? []).filter((v: string) => /^[A-Za-z_]\w*$/.test(v));
      const envDict = `{${envVars.map((v: string) => `${py(v)}: ${v}`).join(", ")}}`;
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      const edBody =
        `${name}_ed = mo.ui.code_editor(value=${py(params.scaffold)}, language="python", min_height=140)\n` +
        `${name}_run = mo.ui.run_button(label="▶ Run my code")\n` +
        `mo.vstack([mo.md(${py(params.instructions)}), ${name}_ed, ${name}_run])`;
      const outBody =
        `if ${name}_run.value:\n` +
        `    _res = run_student_code(${name}_ed.value, ${envDict})\n` +
        `else:\n` +
        `    _res = mo.md("*Press ▶ Run when you're ready.*")\n` +
        `_res`;
      let code =
        `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _names = [c.name for c in ctx.cells]\n` +
        `    if ${py(name)} in _names:\n` +
        `        print("exercise already in the notebook — skipped duplicate insert")\n` +
        `    else:\n` +
        `        _cid = ctx.create_cell(${py(edBody)}, name=${py(name)}, hide_code=True)\n` +
        `        ctx.run_cell(_cid)\n` +
        `        _first = _cid\n` +
        `        _cid = ctx.create_cell(${py(outBody)}, name=${py(name + "_out")}, hide_code=True, after=_cid)\n` +
        `        ctx.run_cell(_cid)\n`;
      code += focusCellCode("_first", "        ");
      const result = await runKernel(code, signal);
      if (!result.failed) {
        result.out =
          `Exercise inserted. The student sees your instructions, a runnable code box, and ` +
          `a ▶ Run button; results appear right below it. Read their attempt with ` +
          `nb_read(['${name}_ed.value']).\n` + result.out;
      }
      return toResult(result);
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
        ". REFUSES to insert if an earlier checkpoint was started but never closed with " +
        "checkpoint_done — close it first, its note cell must land before this build."
      );
    })(),
    promptSnippet: "Insert premade, tested notebook cells by template name (instant)",
    promptGuidelines: [
      "For checkpoint builds use nb_add_template with the template named in lesson.yaml; nb_add_cell is only for detours and improvised cells.",
      "Always pass checkpoint — the id of the checkpoint this build is for, from the script.",
    ],
    parameters: Type.Object({
      status: STATUS_PARAM,
      template: Type.String({ description: "Template name, e.g. 'cp2_ripple'." }),
      checkpoint: Type.String({
        description:
          "Checkpoint id from the script this build is for, e.g. 'cp2_distance'. Required — " +
          "lets the tool catch a checkpoint you started but never closed with checkpoint_done.",
      }),
    }),
    async execute(_id, params, signal) {
      const cpId = baseCheckpointId(String(params.checkpoint ?? "").trim());
      if (!cpId) {
        return toResult({
          out: `NOT INSERTED — pass checkpoint: the id of the checkpoint this build is for.`,
          failed: false,
        });
      }
      // Stretch/off-script ids are not in the chapter order and stay unguarded.
      if (pendingCheckpoint && isScriptedCheckpoint(cpId) && pendingCheckpoint !== cpId) {
        return toResult({
          out:
            `NOT INSERTED — checkpoint '${pendingCheckpoint}' is still open. ` +
            `Call checkpoint_done for '${pendingCheckpoint}' first (its note cell must land ` +
            `before this build), then retry this insert.`,
          failed: false,
        });
      }
      const file = path.join(process.cwd(), "cells", `${params.template}.py`);
      if (!fs.existsSync(file)) {
        return toResult({ out: `No template named '${params.template}'.`, failed: true });
      }
      const src = fs.readFileSync(file, "utf-8");
      // Factual description the tutor can safely echo — prevents the model
      // from misdescribing the artifact (e.g. calling a 4-person network
      // "5-person", seen in production).
      const describe = /^# describe: (.+)$/m.exec(src)?.[1] ?? "";
      const parts = src.split(/^# --- cell: (\w+) ---[ \t]*$/m);
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
        `        ctx.run_cell(_cid)\n` +
        `        _first = _cid\n`;
      for (const c of cells.slice(1)) {
        code +=
          `        _cid = ctx.create_cell(${py(c.code)}, name=${py(c.name)}, hide_code=True, after=_cid)\n` +
          `        ctx.run_cell(_cid)\n`;
      }
      code += focusCellCode("_first", "        ");
      const result = await runKernel(code, signal);
      if (!result.failed && describe) {
        // Upload widgets are named per template (cp4_photo, cp2_paperwork_photo,
        // cp5_ring_paperwork_photo…). The tutor cannot know which one it just
        // inserted, and nb_view_image with the wrong name blows up in the
        // kernel — so the insert result names it.
        const uploads = cells
          .filter((c) => /\bmo\.ui\.file\s*\(/.test(c.code))
          .map((c) => c.name);
        const uploadLine = uploads.length
          ? `When they say the photo is up, call nb_view_image(widget="${uploads[0]}", …).\n`
          : "";
        result.out =
          `Inserted. The student now sees: ${describe}\n` +
          `(Describe it to the student ONLY from this line — never guess counts or details.)\n` +
          uploadLine +
          result.out;
      }
      return toResult(result);
    },
    ...quietRender,
  });

  // ── nb_fresh_start ────────────────────────────────────────────────────────
  // Conversational reset: archives the previous notebook + session log, then
  // deletes every tutor-made cell from the LIVE notebook (template cells are
  // unnamed and survive). Called when the student chooses "start fresh".
  pi.registerTool({
    name: "nb_fresh_start",
    label: "Fresh start",
    description:
      "Reset the session at the student's request: archives the previous notebook and " +
      "session log to session_artifacts/, then clears all tutor-made cells from the live " +
      "notebook. Call ONLY after the student chose to start fresh (ask_user_question).",
    promptSnippet: "Archive the previous session and clear the notebook (student chose fresh start)",
    parameters: Type.Object({
      status: STATUS_PARAM,
    }),
    async execute(_id, params, signal) {
      const stamp = new Date()
        .toISOString()
        .replace(/[-:]/g, "")
        .replace(/\..*/, "")
        .replace("T", "-");
      const dir = path.join(process.cwd(), "session_artifacts");
      try {
        fs.mkdirSync(dir, { recursive: true });
        const nb = path.join(process.cwd(), "notebook.py");
        if (fs.existsSync(nb)) fs.copyFileSync(nb, path.join(dir, `notebook-${stamp}.py`));
        const log = path.join(dir, "session_log.jsonl");
        if (fs.existsSync(log)) fs.renameSync(log, path.join(dir, `session_log-${stamp}.jsonl`));
      } catch {
        // archiving is best-effort; clearing the notebook is what matters
      }
      // Back to chapter 1 with a fresh script in context. triggerTurn so the
      // tutor starts cp0 from the script once it arrives — without this, the
      // model improvises checkpoints from memory (seen in production).
      try {
        const chapters = loadChapters();
        if (chapters.length > 0) {
          writeChapterState(chapters[0].id);
          // Re-arm the open-checkpoint guard on cp0 — a fresh start rewinds
          // the script, so a stale pending id would refuse cp1's build.
          pendingCheckpoint = chapters[0].checkpoints[0] ?? null;
          slotDriftWarned.clear();
          pi.sendMessage(
            {
              customType: "chapter-script",
              content: chapterScriptMessage(chapters[0], 1, chapters.length),
              display: false,
            },
            { deliverAs: "followUp", triggerTurn: true },
          );
        }
      } catch {
        // best-effort
      }
      let code =
        `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    for _c in list(ctx.cells):\n` +
        `        if _c.name and _c.name != "_":\n` +
        `            ctx.delete_cell(_c.id)\n`;
      // Same kernel call as the wipe so the chapter header lands first,
      // before any cp0/cp1 build cells.
      try {
        const chapters = loadChapters();
        if (chapters.length > 0) {
          const h = `${chapters[0].id}_header`;
          const body = `mo.md(${JSON.stringify(`## Chapter 1 of ${chapters.length} — ${chapters[0].title}`)})`;
          code +=
            `    _cid = ctx.create_cell(${py(body)}, name=${py(h)}, hide_code=True)\n` +
            `    ctx.run_cell(_cid)\n`;
        }
      } catch {
        // header is cosmetic
      }
      const result = await runKernel(code, signal);
      if (!result.failed) {
        result.out =
          `Fresh start complete. The Chapter 1 script arrives next — END YOUR TURN NOW ` +
          `(at most one short welcome line first). Treat this as a brand-new session: ` +
          `begin at cp0_welcome FROM THE INCOMING SCRIPT; do not improvise checkpoints ` +
          `from memory.\n` + result.out;
      }
      return toResult(result);
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

  // ── nb_view_image ─────────────────────────────────────────────────────────
  // The tutor model is text-only; this tool is its eyes. Kernel side: pull the
  // upload bytes, save the original (graded artifact), EXIF-rotate + downscale
  // (phone photos are huge and often sideways), show the photo back in the
  // notebook. Extension side: send the small JPEG to a vision model and hand
  // the tutor a factual description to judge.
  pi.registerTool({
    name: "nb_view_image",
    label: "View student image",
    description:
      "Look at a student-uploaded image — you are text-only, so this is your ONLY way to " +
      "see one (never nb_read image bytes). Give the upload widget name (e.g. 'cp4_photo') " +
      "or a file path, what the task was, and the question you need answered. It saves the " +
      "original to session_artifacts/, shows the photo in the notebook for the student, and " +
      "returns a factual description from a vision model. The description is a machine's " +
      "reading, not ground truth — confirm the key detail with the student before building " +
      "on it. If it reports no vision is available, follow its advice instead.",
    promptSnippet: "See a student-uploaded image through a vision model (the tutor is text-only)",
    parameters: Type.Object({
      status: STATUS_PARAM,
      widget: Type.Optional(
        Type.String({ description: "Upload widget name, e.g. 'cp4_photo'." }),
      ),
      file: Type.Optional(Type.String({ description: "Or: path to an image file." })),
      task: Type.String({
        description:
          "What the student was asked to draw/do, in 1-2 sentences copied from the " +
          "checkpoint — the vision model needs this to know what to look for.",
      }),
      question: Type.String({
        description: "What you need to know, e.g. 'Which two dots does the extra line connect?'",
      }),
    }),
    async execute(_id, params, signal, _onUpdate, ctx: any) {
      const widget = String(params.widget ?? "").trim();
      const file = String(params.file ?? "").trim();
      if (!widget && !file) {
        return toResult({ out: "Pass widget (e.g. 'cp4_photo') or file.", failed: true });
      }
      if (widget && !/^[A-Za-z_]\w*$/.test(widget)) {
        return toResult({ out: `'${widget}' is not a widget name.`, failed: true });
      }
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);

      const base = sanitize(widget || path.basename(file).replace(/\.[^.]*$/, ""));
      // assets/, not session_artifacts/: the photo is the student's own figure
      // in the keepsake notebook, so it has to travel WITH the module. The
      // archive folder is gitignored evidence and may not be carried along —
      // a notebook pointing there throws FileNotFoundError on reopen.
      const viewRel = `assets/uploads/${base}_view.jpg`;
      const viewCell = `${base}_view`;
      // Self-contained display cell: the student sees exactly what the vision
      // model was sent (survives notebook reloads; deleted by fresh_start).
      const cellBody =
        `from pathlib import Path as _P\n` +
        `mo.image(_P(${py(viewRel)}).read_bytes(), width=420)`;
      const source = widget
        ? `_files = list(${widget}.value or [])\n` +
          `if not _files:\n` +
          `    print("NO_IMAGE: nothing uploaded yet")\n` +
          `else:\n` +
          `    _name, _raw = _files[0].name, _files[0].contents\n`
        : `_p = _P(${py(file)})\n` +
          `if not _p.exists():\n` +
          `    print("NO_IMAGE: no such file:", ${py(file)})\n` +
          `else:\n` +
          `    _name, _raw = _p.name, _p.read_bytes()\n`;
      const code =
        `import base64 as _b64, io as _io\n` +
        `from pathlib import Path as _P\n` +
        `_P("assets/uploads").mkdir(parents=True, exist_ok=True)\n` +
        `_raw = None\n` +
        source +
        `if _raw is not None:\n` +
        `    from PIL import Image as _Image, ImageOps as _ImageOps\n` +
        `    _ext = _P(_name).suffix.lower() or ".png"\n` +
        `    (_P("assets/uploads") / (${py(base + "_upload")} + _ext)).write_bytes(_raw)\n` +
        `    _img = _Image.open(_io.BytesIO(_raw))\n` +
        `    _img = (_ImageOps.exif_transpose(_img) or _img).convert("RGB")\n` +
        `    _img.thumbnail((1280, 1280))\n` +
        `    _out = _io.BytesIO()\n` +
        `    _img.save(_out, "JPEG", quality=80)\n` +
        `    _P(${py(viewRel)}).write_bytes(_out.getvalue())\n` +
        `    print("FILE:", _name, "->", str(_img.size[0]) + "x" + str(_img.size[1]))\n` +
        `    import marimo._code_mode as cm\n` +
        `    async with cm.get_context() as ctx:\n` +
        `        _names = [c.name for c in ctx.cells]\n` +
        `        if ${py(viewCell)} in _names:\n` +
        `            ctx.edit_cell(${py(viewCell)}, ${py(cellBody)})\n` +
        `        else:\n` +
        `            ctx.create_cell(${py(cellBody)}, name=${py(viewCell)}, hide_code=True)\n` +
        `        ctx.run_cell(${py(viewCell)})\n` +
        focusCellCode(`ctx.cells[${py(viewCell)}].id`, "        ") +
        `    print("B64:" + _b64.b64encode(_out.getvalue()).decode())\n`;
      const result = await runKernel(code, signal);
      if (result.failed) return toResult(result);
      if (result.out.includes("NO_IMAGE")) {
        return toResult({
          out:
            result.out +
            `\nAsk the student to upload their photo in the notebook first (then tell you ` +
            `here when it's up), or to describe the drawing in words here.`,
          failed: false,
        });
      }
      const b64 = /^B64:([A-Za-z0-9+/=]+)\s*$/m.exec(result.out)?.[1];
      const fileLine = /^FILE:.*$/m.exec(result.out)?.[0] ?? "";
      if (!b64) {
        return toResult({
          out:
            `Could not extract the image. Ask the student to describe their drawing ` +
            `in words instead and judge that.\n${result.out.slice(0, 500)}`,
          failed: true,
        });
      }
      const vision = await describeImage(
        ctx,
        b64,
        String(params.task ?? "").trim(),
        String(params.question ?? "").trim(),
      );
      if (vision.failed) return toResult({ out: `${fileLine}\n${vision.text}`, failed: false });
      return toResult({
        out:
          `${fileLine} — saved, and the student now sees their photo in the notebook.\n` +
          `VISION REPORT from ${vision.model} (a machine description — judge it against ` +
          `the checkpoint yourself; respond to a concrete detail from it, don't echo it ` +
          `wholesale):\n${vision.text}`,
        failed: false,
      });
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
      const result = await runKernel(params.code, signal);
      // Hand-written log JSON is obsolete and drifts (schema, timestamps,
      // paraphrased answers) — redirect to the tool that owns the record.
      if (/session_log|session_summary/.test(params.code)) {
        result.out =
          (result.out ? result.out + "\n" : "") +
          `NOTE: do NOT write the session log or summary by hand — checkpoint_done ` +
          `logs checkpoints (and adds the note cell and the transition ask), ` +
          `log_detour logs questions, and chapter_done writes the closing summary.`;
      }
      return toResult(result);
    },
    ...quietRender,
  });

  // ── waiting-time trivia ───────────────────────────────────────────────────
  // The student stares at "Working…" during model calls, notebook round-trips
  // and chapter handoffs. Replace it with a rotating network-science tidbit —
  // dead air becomes a tiny extra lesson.
  const TRIVIA = [
    "Euler invented network theory in 1736 to settle a stroll — the 7 bridges of Königsberg.",
    "The 'six degrees' idea first appeared in a 1929 short story by Frigyes Karinthy.",
    "Milgram's packets reached the Boston stockbroker in about 6 hops — 64 of 160 made it.",
    "In 2011 Facebook measured 721 million users: average distance, just 4.74 friendships.",
    "A 2003 email rerun of Milgram's experiment landed on the same answer: about 6 steps.",
    "Your friends have more friends than you do, on average — the friendship paradox.",
    "Watts & Strogatz, 1998: a few random rewires make a big world small.",
    "The original three small worlds of 1998: film actors, the power grid, and a worm's brain.",
    "The C. elegans worm's entire nervous system is mapped — 302 neurons, and it's a small world.",
    "Zachary's karate club split in two in 1977 — and became network science's favorite dataset.",
    "Find the karate-club split at a network conference and you can win an actual trophy.",
    "Erdős number: your coauthor distance to Paul Erdős. Most mathematicians sit within 5.",
    "Erdős number + Bacon number = the Erdős–Bacon number. Natalie Portman's is 6.",
    "Kevin Bacon isn't Hollywood's center — hundreds of actors are better connected.",
    "Granovetter, 1973: people find jobs through acquaintances, not close friends. Weak ties win.",
    "Triadic closure: your friend's friend tends to become your friend. That's where triangles come from.",
    "High clustering AND short paths = small world. Neither a ring nor a random graph has both.",
    "Airlines fly hub-and-spoke because a few long shortcuts shrink every route.",
    "Diseases ride shortcuts too: one flight can outrun a thousand local contacts.",
    "The web, citation networks, and Hollywood all share one shape: a few superstar hubs.",
    "Hub networks shrug off random failures — but fall fast to targeted attacks on hubs.",
    "Dunbar's number: human brains manage roughly 150 stable relationships.",
    "PageRank is network centrality: where an endlessly clicking web surfer ends up.",
    "You know about 0.000002% of humanity — yet you can reach anyone in about 6 steps.",
    "Your brain is a small-world network too: tight local clusters, short paths between regions.",
  ];
  let triviaIdx = Math.floor(Math.random() * TRIVIA.length);
  let triviaTimer: ReturnType<typeof setInterval> | null = null;
  const showTrivia = (ctx: any) => {
    try {
      const line = `Tip: ${TRIVIA[triviaIdx++ % TRIVIA.length]}`;
      ctx.ui.setWorkingMessage(ctx.ui.theme.fg("dim", line));
    } catch {
      // cosmetic only — never let trivia break a turn
    }
  };
  pi.on("turn_start", async (_event, ctx: any) => {
    if (!ctx.hasUI) return;
    showTrivia(ctx);
    if (triviaTimer) clearInterval(triviaTimer);
    // Long waits (vision calls, compaction) get a new tidbit mid-spin.
    triviaTimer = setInterval(() => showTrivia(ctx), 12_000);
    (triviaTimer as any).unref?.(); // never keep the process alive (print mode)
  });
  pi.on("turn_end", async () => {
    if (triviaTimer) {
      clearInterval(triviaTimer);
      triviaTimer = null;
    }
  });
}
