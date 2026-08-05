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
 * Upload boxes carry a 📨 Send to my tutor button: pressing it appends to
 * session_artifacts/student_signal.txt, which the watcher below turns into a
 * turn, so the tutor never has to ask whether the photo is up. Everything
 * else the student explores (sliders, widgets) has no button — they say so
 * in the terminal and the tutor reads the values with nb_read.
 */
import { execFile } from "node:child_process";
import * as fs from "node:fs";
import path from "node:path";
import { Type } from "typebox";
import { uuidv7 } from "@earendil-works/pi-ai";
import { complete } from "@earendil-works/pi-ai/compat";
import { Text } from "@earendil-works/pi-tui";
import { keyHint, type ExtensionAPI } from "@earendil-works/pi-coding-agent";

// How every nb_* call reaches the marimo kernel. The script ships inside the
// marimo-pair skill, but under pi the SKILL must not be installed: the model
// reaches for it mid-hint and a bare "[skill] marimo-pair" line lands in the
// student's terminal. So run_tutor.sh stages just the scripts outside any
// skills directory, and that copy is tried first. (Deleting the skill without
// staging the bridge was briefly shipped and killed every notebook call.)
const SCRIPT_CANDIDATES = [
  ".pi/marimo-bridge/scripts/execute-code.sh",
  ".pi/skills/marimo-pair/scripts/execute-code.sh",
  ".claude/skills/marimo-pair/scripts/execute-code.sh",
];

/** JSON string literals are valid Python string literals. */
const py = (s: string) => JSON.stringify(s);

/**
 * The argument of an `mo.md(...)` call, as a RAW triple-quoted literal.
 *
 * `py()` is wrong here, and silently so. marimo recognises a markdown cell
 * when it saves the file and rewrites it as a triple-quoted literal, copying
 * the r/f prefix from the ORIGINAL source token — so a note created as
 * `mo.md("…\\frac…")` is written back as a NON-raw `mo.md("""…\frac…""")`,
 * and the next reload lets Python eat `\f`, `\a`, `\r`, `\t`. That is how
 * the module's central definition ended up on screen as
 * `C_i = rac{ ext{friendships…}}`, and $L = 7/6 pprox 1.17$ beside it.
 * Every note skeleton is full of LaTeX, so this hit the keepsake hardest.
 *
 * A raw string cannot contain `"""` and cannot end in a backslash, so the
 * text is split into raw chunks glued together with ordinary literals. In
 * the normal case (no triple quote anywhere) that is exactly the
 * `r"""…"""` marimo writes for itself.
 *
 * The prefix marimo copies is the LAST string token's, so that token must be
 * raw no matter what the text ends with — and a note ends with the student's
 * own words, which can perfectly well end in a quotation mark. Padding the
 * final chunk with one newline (invisible in markdown) keeps it raw instead
 * of peeling it into an ordinary literal and losing the prefix again.
 */
function pyMd(markdown: string): string {
  const chunk = (s: string): string => {
    if (!s) return '""';
    // Neither a quote nor a backslash may sit against the closing """ —
    // peel any trailing run of them into an ordinary escaped literal.
    const tail = /["\\]+$/.exec(s);
    if (!tail) return `r"""${s}"""`;
    const head = s.slice(0, s.length - tail[0].length);
    return head ? `r"""${head}""" ${py(tail[0])}` : py(tail[0]);
  };
  const parts = markdown.replace(/\r\n/g, "\n").split('"""');
  const last = parts.length - 1;
  if (parts[last] === "" || /["\\]$/.test(parts[last])) parts[last] += "\n";
  return parts.map(chunk).join(` '"""' `);
}
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
      out:
        "The notebook bridge (.pi/marimo-bridge/scripts/execute-code.sh) is missing, so " +
        "nothing can reach the notebook. Tell the student, in one warm sentence, that the " +
        "notebook needs restarting with ./run_tutor.sh — then keep teaching in the terminal.",
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
    "Short student-facing status in plain, friendly words, e.g. 'Preparing our next step…'. " +
    "No technical terms, no cell/code/error talk — and NEVER a fact the checkpoint you are " +
    "on is asking them to find (it is shown at the moment you build that checkpoint).",
});

// ── Chapter orchestration (the deterministic "lead agent") ──────────────────
// The lesson is split into chapters (lesson/index.json). The tutor holds only
// the CURRENT chapter's script in context; chapter_done builds a handoff
// brief, injects the next script, and trims the old conversation via
// compaction — same session, same visible transcript, fresh LLM context.
type Chapter = {
  id: string;
  file: string;
  title: string;
  /** Lecture-note prose rendered under the chapter heading (see chapterOpening). */
  opening?: string;
  checkpoints: string[];
};

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
  // Repeated, because a looping tutor produced "cp0_welcome_extra_extra" —
  // one strip left an id no lookup could match, which silently disabled the
  // ordering guard and the note skeleton for every later round.
  let out = id;
  for (let i = 0; i < 8; i++) {
    const next = out.replace(/_extra(_?\d+)?$/, "");
    if (next === out) break;
    out = next;
  }
  return out;
}

function isScriptedCheckpoint(id: string): boolean {
  return checkpointOrder().includes(baseCheckpointId(id));
}

/** The checkpoint the tutor is expected to work next, or null if unknown. */
/**
 * Where to go after closing `id`: the first scripted checkpoint with no log
 * row, treating `id` as logged (checkpoint_done sets this before it appends).
 *
 * Positional "the next one in the list" was wrong once resume learned to
 * pick up AT a gap. A log that reached cp8 with three checkpoints missing
 * resumed correctly at the first gap and was then walked forward through six
 * checkpoints it had already done — and could not skip them, because the
 * build-ordering guard refuses a forward jump. Each re-close appended a
 * second row while the note cell kept the first answer: 18 rows in a
 * 12-checkpoint record, six of them contradicting their own note.
 */
function nextCheckpointId(id: string): string | null {
  const order = checkpointOrder();
  const done = new Set<string>([baseCheckpointId(id)]);
  try {
    for (const e of readSessionLog()) {
      if (e?.type === "checkpoint" && e.id) done.add(baseCheckpointId(String(e.id)));
    }
  } catch {
    // No log to read — the positional answer below is the whole truth.
  }
  const gap = order.find((o) => !done.has(o));
  if (gap) return gap;
  // Everything is logged. Fall back to the positional answer so a normal
  // session (where the row for `id` is written a moment later) still knows
  // there is nothing after the last checkpoint.
  const i = order.indexOf(baseCheckpointId(id));
  return i >= 0 ? (order[i + 1] ?? null) : null;
}

/**
 * Is `cpId` a checkpoint the tutor has not reached yet? This — not mere
 * inequality — is what the build-ordering guard must refuse: inserting a
 * LATER checkpoint's build while the current one is open strands its note
 * cell after that build. Re-inserting an EARLIER one (a reveal figure added
 * after the checkpoint was closed) is harmless and must stay allowed.
 */
function isAheadOf(cpId: string, openId: string): boolean {
  const order = checkpointOrder();
  const a = order.indexOf(cpId);
  const b = order.indexOf(openId);
  return a >= 0 && b >= 0 && a > b;
}

function chapterScriptMessage(ch: Chapter, num: number, total: number): string {
  const src = fs.readFileSync(path.join(process.cwd(), "lesson", ch.file), "utf-8");
  const last = ch.checkpoints[ch.checkpoints.length - 1];
  return (
    `CHAPTER SCRIPT ${num}/${total} — "${ch.title}" (invisible to the student). ` +
    `This is your curriculum right now:\n\n${src}\n\n` +
    (chapterOpening(ch)
      ? `The chapter's opening paragraph is ALREADY in their notebook, above ` +
        `your first build — do not read it out or paraphrase it. It says:\n` +
        `"${chapterOpening(ch)}"\n\n`
      : "") +
    `Work its checkpoints in order, ending each one with checkpoint_done. ` +
    `After checkpoint_done for the final checkpoint (${last}), call chapter_done ` +
    `with short handoff notes.`
  );
}

/**
 * The chapter's instructor-authored `opening:` prose, from the `chapter:`
 * block at the top of its script. This is what turns the notebook from a
 * pile of experiments into a lecture note: a heading alone tells a cold
 * reader nothing about why the next four cells exist.
 *
 * It renders BEFORE the chapter's first question, so an opening that
 * answers one is an answer leak — the scripts carry a comment saying so.
 */
function chapterOpening(ch: Chapter): string {
  return String(ch.opening ?? "").trim();
}

/**
 * Deterministic notebook structure: a "## Chapter N — Title" markdown cell
 * plus the chapter's opening prose, at every chapter start, so the finished
 * notebook reads as a document the student can re-learn from.
 * Skip-if-exists; cosmetic — never blocks.
 */
async function insertChapterHeader(
  ch: Chapter,
  num: number,
  total: number,
  signal?: AbortSignal,
): Promise<boolean> {
  try {
    const warm = await ensureWarm(signal);
    if (warm) return false;
    const name = `${ch.id}_header`;
    const opening = chapterOpening(ch);
    const heading = `## Chapter ${num} of ${total} — ${ch.title}`;
    const body = `mo.md(${pyMd(opening ? `${heading}\n\n${opening}` : heading)})`;
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
    return true;
  } catch {
    // headers are cosmetic — never block the lesson
    return false;
  }
}

/**
 * Chapter 1's header is the one nobody else retries: chapters 2-5 get theirs
 * from chapter_done, long after the kernel is warm, but chapter 1's fires
 * once at session start — and the kernel stays cold until a browser client
 * connects. A student who opens the page late (the D7 notebook-down path)
 * used to lose that header for good, leaving a notebook whose first heading
 * says "Chapter 2 of 5". Keep trying until it lands, the chapter moves on,
 * or we give up after ~5 minutes. create_cell is skip-if-exists, so a late
 * success can never duplicate it.
 */
/**
 * No named cell may land before its chapter header. The scheduled attempt is
 * on a timer, and cp0_welcome builds nothing — so its note cell (a greeting
 * and one dialog later) could be created first and push "Chapter 1 of 5"
 * below it. Called before every insert that creates a named cell; skip-if-
 * exists makes it a no-op after the first success.
 */
async function ensureChapterHeader(signal?: AbortSignal): Promise<void> {
  const chapters = loadChapters();
  if (chapters.length === 0) return;
  const id = currentChapterId() ?? chapters[0].id;
  const idx = chapters.findIndex((c) => c.id === id);
  if (idx < 0) return;
  await insertChapterHeader(chapters[idx], idx + 1, chapters.length, signal);
}

function scheduleChapterHeader(ch: Chapter, num: number, total: number): void {
  let attempts = 0;
  const tick = async () => {
    attempts += 1;
    if (currentChapterId() !== ch.id) return;
    const ok = await insertChapterHeader(ch, num, total);
    if (ok || attempts >= 20) return;
    const t = setTimeout(() => void tick(), 15_000);
    (t as any).unref?.();
  };
  const first = setTimeout(() => void tick(), 15_000);
  (first as any).unref?.();
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
// Every pi.sendMessage injection lands in the transcript with role "user".
// Anything added here MUST start with one of these prefixes, or it is filed
// as the student's own words and quoted back at them in the graded record.
const INJECTED_PREFIX =
  /^(CHAPTER SCRIPT|RESUME CONTEXT|=== TUTORING HANDOFF|The student clicked|Please start the tutoring session|── Chapter |NOTE \(invisible to the student\))/;

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

/**
 * A picker answer never becomes a transcript message, so until now the graded
 * record had NO independent evidence of it — and a live run logged
 * "Comfortable with Python" for a student who had picked "I don't code",
 * miscalibrating the whole session and putting the opposite of their answer
 * in the artifact they submit. These are captured straight off the
 * ask_user_question tool result instead.
 */
const pickedAnswers: string[] = [];
let pickedMark = 0;
/**
 * Set while the resume brief is in flight. The continue-or-fresh dialog is
 * session mechanics, not an answer to a lesson question, so its result is
 * dropped instead of riding into the next checkpoint's `student_picked`.
 */
let awaitingResumeChoice = false;

function recordPickedAnswer(event: any): void {
  try {
    if (!/ask.?user.?question/i.test(String(event?.toolName ?? ""))) return;

    const text = (event?.content ?? [])
      .filter((c: any) => c?.type === "text" && typeof c.text === "string")
      .map((c: any) => c.text)
      .join("\n")
      .trim();
    if (!text) return;
    let picked = text;
    try {
      const parsed = JSON.parse(text);
      const answers = parsed?.answers ?? parsed;
      const flat = Array.isArray(answers)
        ? answers
        : answers && typeof answers === "object"
          ? Object.values(answers)
          : [];
      const joined = flat
        .map((a: any) => (typeof a === "string" ? a : (a?.answer ?? a?.value ?? "")))
        .filter(Boolean)
        .join(" · ");
      if (joined) picked = joined;
    } catch {
      // Not JSON. The dialog package hands back a sentence of plumbing —
      //   User has answered your questions: "How do you feel about
      //   Python?"="tried a little". You can now continue …
      // — and storing that whole sentence put a machine's voice inside the
      // student's own `*You chose:*` line in the submitted notebook. Keep
      // only the answers: every "question"="answer" pair's right-hand side.
      const pairs = [...text.matchAll(/"([^"]*)"\s*=\s*"([^"]*)"/g)].map((m) => m[2].trim());
      if (pairs.length) picked = pairs.filter(Boolean).join(" · ");
    }
    // The continue-or-fresh answer is session mechanics, not a lesson
    // answer. Match it by CONTENT rather than "whatever dialog comes first
    // after a resume": if the tutor asks continue-or-fresh in plain text,
    // the flag would otherwise swallow the next real prediction instead —
    // and a re-asked resume dialog would slip the original one through.
    if (
      awaitingResumeChoice &&
      /continue|fresh|left off|pick (things )?up|no input/i.test(picked)
    ) {
      awaitingResumeChoice = false;
      return;
    }
    pickedAnswers.push(picked.slice(0, 300));
  } catch {
    // capture is best-effort; never break a turn
  }
}

function pickedSince(commit = true): string[] {
  const fresh = pickedAnswers.slice(pickedMark);
  if (commit) pickedMark = pickedAnswers.length;
  return fresh;
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
  // Structural labels a tutor puts around a multi-part answer — the note
  // skeletons say «their answers, verbatim» (plural) for the 3-6 part
  // checkpoints, so "Idea: … Count: … Fraction: …" is the natural shape and
  // must not read as invented content.
  "idea", "answer", "answers", "count", "counts", "fraction", "result", "work",
  "note", "first", "second", "third", "final", "total", "corrected", "then",
]);

function slotTokens(s: string): string[] {
  const norm = s
    .toLowerCase()
    .replace(/[‐-―−]/g, "-")
    .replace(/[*_`>#]/g, " ");
  return norm.match(/[a-z0-9](?:[a-z0-9._/-]*[a-z0-9])?/g) ?? [];
}

/**
 * A "figure": 7/6, 1.17, 4.74, 0.61, 9:30 — a compound or multi-digit
 * number. Bare single digits are NOT figures: they are how a subscript
 * ($L_0$ → "l", "0") and an ordinary label ("dot 1 to dot 5") tokenize, and
 * flagging those refused faithful records.
 */
function isFigure(token: string): boolean {
  return /^\d+([./:,-]\d+)+$|^\d{2,}$/.test(token);
}

/**
 * Character-bigram overlap (Dice), 0–1. Used to spot a RETYPED answer: a
 * live session logged "becuase tirangles are ipormtat" for a student who
 * typed "becuase tirangles are ipmortat" — the model copied their sentence
 * out by hand and re-scrambled their own typo along the way. Word-level
 * drift cannot see that (one odd token), and it is exactly the kind of
 * silent edit the graded record must not carry.
 */
function bigramDice(a: string, b: string): number {
  const grams = (s: string) => {
    const t = s.toLowerCase().replace(/\s+/g, " ").trim();
    const out = new Set<string>();
    for (let i = 0; i + 1 < t.length; i += 1) out.add(t.slice(i, i + 2));
    return out;
  };
  const A = grams(a);
  const B = grams(b);
  if (A.size === 0 || B.size === 0) return 0;
  let hits = 0;
  for (const g of A) if (B.has(g)) hits += 1;
  return (2 * hits) / (A.size + B.size);
}

/**
 * If `response` is a near-copy of one of the student's own messages, return
 * that message instead — their words, character for character.
 *
 * Similarity alone is not enough to act on. Joining several short answers
 * into one ("A–D is 2, and the average is 7/6 over all six pairs") is the
 * sanctioned shape — the skeletons say «their answers, verbatim», plural —
 * and it scores nearly as high against its longest fragment as a retype
 * does against the whole message. Snapping there would delete half the
 * student's answer from the graded record, so a candidate must also be
 * about the same LENGTH: a retype is, a swallowed fragment is not.
 */
function snapToTranscript(response: string, said: string[]): string | null {
  const flat = (s: string) => s.replace(/\s+/g, " ").trim().toLowerCase();
  if (said.some((s) => flat(s) === flat(response) || flat(s).includes(flat(response)))) return null;
  let best: { score: number; text: string } | null = null;
  for (const s of said) {
    const score = bigramDice(s, response);
    if (!best || score > best.score) best = { score, text: s };
  }
  if (!best || best.score < 0.8) return null;
  const longest = Math.max(best.text.length, response.length);
  return Math.abs(best.text.length - response.length) <= 0.15 * longest ? best.text : null;
}

/** Content tokens in `fill` that the student never produced. */
function slotDrift(fill: string, studentPool: string[]): { numbers: string[]; words: string[] } {
  const pool = new Set(studentPool.flatMap(slotTokens));
  const numbers: string[] = [];
  const words: string[] = [];
  for (const t of new Set(slotTokens(fill))) {
    if (pool.has(t) || SLOT_GLUE.has(t)) continue;
    if (isFigure(t)) numbers.push(t);
    else words.push(t);
  }
  return { numbers, words };
}

/**
 * Pull a checkpoint's instructor-authored `note:` block out of its chapter
 * YAML (block scalar, dedented). The tutor fills «slots», not prose.
 */
// Exact id only. A practice round (`cp2_distance_extra`) is the same QUESTION
// on new DATA, so its base checkpoint's skeleton is wrong for it: cp2's says
// "$L = 7/6$", while the practice variant is a star ($L = 9/6$). The tutor
// writes note_markdown for those, per AGENTS.md.
function checkpointBlock(cpId: string, key: string): string {
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
      const m = new RegExp(`^(\\s*)${key}:\\s*\\|`).exec(lines[i]);
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

/** A checkpoint's instructor-authored `note:` skeleton. */
function noteSkeleton(cpId: string): string {
  return checkpointBlock(cpId, "note");
}

/**
 * `note: none` in the script — this checkpoint gets NO note cell. Some
 * checkpoints are session mechanics, not lecture: cp0 calibrates how much
 * code the student wants to see, and a cell about that is the first thing a
 * cold reader meets in a document that has not begun. The answer still gets
 * logged and still lands in the closing session_record.
 */
function noteSuppressed(cpId: string): boolean {
  try {
    const chapter = loadChapters().find((c) => c.checkpoints.includes(baseCheckpointId(cpId)));
    if (!chapter) return false;
    const lines = fs
      .readFileSync(path.join(process.cwd(), "lesson", chapter.file), "utf-8")
      .split("\n");
    const start = lines.findIndex((l) =>
      new RegExp(`^\\s*-\\s+id:\\s*${baseCheckpointId(cpId)}\\s*$`).test(l),
    );
    if (start < 0) return false;
    for (let i = start + 1; i < lines.length; i++) {
      if (/^\s*-\s+id:\s/.test(lines[i])) break;
      if (/^\s*note:\s*none\s*$/.test(lines[i])) return true;
    }
    return false;
  } catch {
    return false;
  }
}

/** Does the script offer a practice variant for this checkpoint? */
function hasFreshVariants(cpId: string): boolean {
  return checkpointBlock(cpId, "fresh_variants").trim().length > 0;
}

/**
 * The cell names a checkpoint's `build:` promises — every
 * `nb_add_template("X")` in it, resolved through `cells/X.py`'s
 * `# --- cell: NAME ---` markers.
 *
 * Used to catch a build the tutor simply never did. cp5_ring_formula asks
 * seven things in sequence and the seventh is "photograph that page"; in a
 * live run the model reached the end of the reasoning, decided the answer
 * was complete, and closed the checkpoint — the upload area was never
 * inserted and the student was never asked for the photo at all. The
 * hand-worked page is the point of those checkpoints, so a promise in the
 * script is checked rather than trusted.
 */
function scriptedBuildCells(cpId: string): string[] {
  const build = checkpointBlock(cpId, "build");
  if (!build.trim() || /^\s*none\s*$/i.test(build)) return [];
  const out: string[] = [];
  // Tolerate the argument form the tool itself asks for —
  // nb_add_template("x", checkpoint="cp4") — and a named first argument.
  // Requiring the bare one-arg call meant an instructor aligning a build:
  // line with the tool contract silently switched this guard off.
  for (const m of build.matchAll(/nb_add_template\(\s*(?:template\s*=\s*)?["']([\w-]+)["']/g)) {
    try {
      const src = fs.readFileSync(path.join(process.cwd(), "cells", `${m[1]}.py`), "utf-8");
      for (const c of src.matchAll(/^#\s*---\s*cell:\s*(\w+)\s*---/gm)) out.push(c[1]);
    } catch {
      // an unknown template name is nb_add_template's problem, not ours
    }
  }
  return out;
}

/** The «…» markers of a note skeleton, in order. */
function slotMarkers(skeleton: string): string[] {
  return skeleton.match(/«[^»]*»/g) ?? [];
}

/**
 * Fill a note skeleton's «slots» in order.
 *
 * An unsupplied slot falls back to `student_response` — but only the FIRST
 * one. Padding every empty slot with it printed the same sentence under
 * three different labels once the skeletons were split into a slot per part
 * ("The ring world: …", "The random world: <same sentence>", "Which one I
 * live in: <same sentence>"), which reads as the student saying something
 * they never said. checkpoint_done nudges for the missing fills before it
 * ever gets here; this is the shape when it has nudged twice and given up.
 */
function fillSlots(skeleton: string, slots: string[], fallback: string): string {
  let i = 0;
  let usedFallback = false;
  return skeleton.replace(/«[^»]*»/g, () => {
    const supplied = slots[i];
    i += 1;
    if (supplied !== undefined && supplied !== "") return supplied;
    if (usedFallback) return "*(not answered)*";
    usedFallback = true;
    return fallback;
  });
}

/**
 * A souvenir cell opens with the student's own question, quoted. Every live
 * session so far produced detour cells that answered a question the notebook
 * never states — unreadable months later, and the personalization is the
 * whole point of a souvenir. So the extension puts the quote there itself
 * rather than trusting the model to remember, and skips it when the markdown
 * already carries the question. The line goes under a leading heading if
 * there is one, so "### 🧭 Detour: …" stays first.
 */
function withQuotedQuestion(markdown: string, question: string): string {
  if (!question) return markdown;
  // Same normalisation souvenirGap uses, or the two halves of the contract
  // disagree: a cell that quotes "can't" against a question typed "cant"
  // satisfies that check and then gets a SECOND copy of the question
  // prepended by this one.
  const flat = (s: string) =>
    s
      .toLowerCase()
      .replace(/['\u2018\u2019\u02BC"\u201C\u201D]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  if (flat(markdown).includes(flat(question))) return markdown;
  const quote = `> 🧭 **You asked:** “${question}”`;
  const lines = markdown.split("\n");
  if (/^\s*#{1,6}\s/.test(lines[0] ?? "")) {
    return [lines[0], "", quote, ...lines.slice(1)].join("\n");
  }
  return `${quote}\n\n${markdown}`;
}

/** Names of every cell currently in the notebook, or null if unreadable. */
async function notebookCellNames(signal?: AbortSignal): Promise<string[] | null> {
  const r = await runKernel(
    `import marimo._code_mode as cm\n` +
      `async with cm.get_context() as ctx:\n` +
      `    print("CELLS<<" + ",".join(str(getattr(c, "name", "")) for c in ctx.cells) + ">>")\n`,
    signal,
  );
  if (r.failed) return null;
  const m = /CELLS<<(.*)>>/.exec(r.out);
  return m ? m[1].split(",").filter(Boolean) : null;
}

/**
 * The source of a named cell, or null when it cannot be read (kernel cold,
 * marimo API shifted). Used to CHECK a souvenir the tutor built itself —
 * the `cell_name` path was the unchecked half of the contract, and it is
 * the path the model actually takes.
 */
async function readCellSource(name: string, signal?: AbortSignal): Promise<string | null> {
  const r = await runKernel(
    `import marimo._code_mode as cm\n` +
      `async with cm.get_context() as ctx:\n` +
      `    _c = None\n` +
      `    for _x in ctx.cells:\n` +
      `        if getattr(_x, "name", None) == ${py(name)}:\n` +
      `            _c = _x\n` +
      `    if _c is None:\n` +
      `        print("SOUVENIR_MISSING")\n` +
      `    else:\n` +
      `        _src = ""\n` +
      `        for _a in ("code", "source", "text"):\n` +
      `            _v = getattr(_c, _a, None)\n` +
      `            if isinstance(_v, str) and _v.strip():\n` +
      `                _src = _v\n` +
      `                break\n` +
      `        print("SOUVENIR_SRC<<")\n` +
      `        print(_src)\n` +
      `        print(">>SOUVENIR_SRC")\n`,
    signal,
  );
  if (r.failed) return null;
  if (r.out.includes("SOUVENIR_MISSING")) return "";
  const m = /SOUVENIR_SRC<<\n([\s\S]*?)\n>>SOUVENIR_SRC/.exec(r.out);
  const src = m?.[1] ?? "";
  // Empty means the attribute walk found nothing — unknown, not empty. A
  // check that cannot see the cell must stand down, never accuse.
  return src.trim() ? src : null;
}

/** What a souvenir cell is missing, or "" when it honours the contract. */
function souvenirGap(src: string, question: string): string {
  if (!src) return "does not exist in the notebook";
  const shows = /netviz\s*\(|mo\.ui\.|mo\.image\s*\(|alt\.Chart|sns\.\w+\s*\(|plt\.\w+\s*\(|mo\.carousel|mo\.accordion/.test(
    src,
  );
  // Quoting is judged on words, not bytes. The suggested template wraps the
  // question in typographic quotes, a model rewrites "what's" as "what’s"
  // or drops the trailing "?", and a byte-exact match then bounced a
  // souvenir that plainly does quote the question — and stamped it
  // `souvenir_gap` in the log afterwards.
  // Apostrophes are DELETED, not turned into spaces: a student types "cant"
  // and the souvenir quotes "can't", which is the same word and the right
  // thing for the model to have written. Collapsing the apostrophe to a
  // space made it two tokens against the student's one, and the honest
  // souvenir was bounced and then stamped `souvenir_gap` in the log.
  const flat = (s: string) =>
    s
      .toLowerCase()
      .replace(/['‘’ʼ"“”]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  // Strip the word the 40-char slice cut in half — but ONLY when it did cut
  // one. Doing it unconditionally shrank a short question ("Why triangles?")
  // to the single word "why", which any prose souvenir contains by accident.
  const asked = flat(question);
  const needle = asked.length > 40 ? asked.slice(0, 40).replace(/\s+\S*$/, "") : asked;
  const quotes = needle.length > 0 && flat(src).includes(needle);
  if (!shows && !quotes) return "is prose only, and never quotes their question";
  if (!shows) return "is prose only — nothing to look at or play with";
  if (!quotes) return "never quotes the question it answers";
  return "";
}

/** Insert (or skip, if present) a markdown cell and scroll the page to it. */
async function insertMarkdownCell(
  name: string,
  markdown: string,
  signal?: AbortSignal,
): Promise<{ out: string; failed: boolean }> {
  const warm = await ensureWarm(signal);
  if (warm) return warm;
  if (name !== "session_record") await ensureChapterHeader(signal);
  const body = `mo.md(${pyMd(markdown)})`;
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
    "*Your answer to each question, and every word you typed while working on*",
    "*it — this is what gets reviewed, not the code. Hints are never held*",
    "*against you.*",
    "",
  ];
  for (const e of cps) {
    const hints = Number(e.hints_used ?? 0);
    // Two separate things, never conflated. The quote is the tutor's record
    // of the ANSWER — which for a picker choice or a drawing is the only
    // record there is. Beneath it, verbatim, goes everything the student
    // actually typed while working on this checkpoint, straight from the
    // transcript. Printing the capture AS the answer was wrong: a stray
    // "ok" typed while a dialog was open would have become their answer.
    const saidRaw: string[] = Array.isArray(e.student_said_verbatim)
      ? e.student_said_verbatim.map((s: unknown) => String(s ?? "").trim()).filter(Boolean)
      : [];
    const quote = String(e.student_response ?? "").trim();
    lines.push(
      `**${e.id}** · ${e.judgment ?? "?"}${hints ? ` · ${hints} hint${hints > 1 ? "s" : ""}` : ""}`,
      "",
      `*${String(e.question ?? "").trim()}*`,
      "",
      `> ${quote.replace(/\n+/g, " ")}`,
      "",
    );
    const pickedRaw: string[] = Array.isArray(e.student_picked)
      ? e.student_picked.map((s: unknown) => String(s ?? "").trim()).filter(Boolean)
      : [];
    if (pickedRaw.length) {
      lines.push(`*You chose:* ${pickedRaw.map((s) => `"${s}"`).join(" · ")}`, "");
    }
    if (saidRaw.length) {
      lines.push(
        `*You typed:* ${saidRaw.map((s) => `"${s.replace(/\n+/g, " ")}"`).join(" · ")}`,
        "",
      );
    }
    if (e.notes) lines.push(`*Tutor's note:* ${String(e.notes).trim()}`, "");
    // A drift the tutor was warned about twice and logged anyway belongs in
    // the submitted artifact, not only in the log the student never opens.
    if (Array.isArray(e.verbatim_drift) && e.verbatim_drift.length) {
      lines.push(
        `*⚠ Quoting check: the wording above was flagged as not matching what you typed — ` +
          `your own words are the line above it.*`,
        "",
      );
    }
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
  // Count the SCRIPT's checkpoints, not the log rows: a practice round is
  // logged under its own `_extra` id, and counting those produced
  // "Checkpoints completed: 13 of 12" on the first full run — a summary the
  // grader cannot read as anything but a bug. Extra rounds are worth
  // reporting, just not as progress through the module.
  const done = new Set(cps.map((e) => baseCheckpointId(String(e.id))));
  const extras = cps.filter((e) => /_extra/.test(String(e.id))).length;
  const missing = allCheckpoints.filter((id) => !done.has(id));
  const out = [
    "# Session summary",
    "",
    `Checkpoints completed: ${allCheckpoints.filter((id) => done.has(id)).length} of ${allCheckpoints.length}`,
    ...(extras ? [`Extra practice rounds asked for: ${extras}`] : []),
    `Detours (student's own questions): ${entries.filter((e) => e?.type === "detour").length}`,
    "",
  ];
  for (const e of cps) {
    out.push(
      `## ${e.id} — ${e.judgment ?? "?"} (${Number(e.hints_used ?? 0)} hint${Number(e.hints_used ?? 0) === 1 ? "" : "s"})`,
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
  const slotDriftWarned = new Map<string, number>();
  // Same idea for the souvenir contract: a text-only detour cell is bounced
  // once, then accepted, so a detour that genuinely has no picture in it can
  // still be recorded.
  const detourTextOnlyWarned = new Set<string>();
  // Improvised-cell review refusals, per cell name — capped like the rest.
  const cellReviewWarned = new Map<string, number>();
  // Upload widgets nb_view_image has actually looked at. Cell presence is
  // not evidence that the photo was ASKED for: cp5's script builds the drop
  // area up front, so the area exists from question 1 and a tutor that then
  // skips the "photograph that page" step closes a paper checkpoint with no
  // paper in it — which is exactly what a live run did.
  const viewedPhotos = new Set<string>();

  pi.on("tool_result", async (event: any) => {
    recordPickedAnswer(event);
  });

  // ── The student's "Send to my tutor" button ───────────────────────────
  // marimo runs in its own process, so a button in the page cannot call a
  // tool. The upload templates append the widget's name to
  // session_artifacts/student_signal.txt instead, and this watcher turns
  // each new line into a turn. Without it the student has to type "it's up"
  // in the terminal — one more thing to explain, and one more place for a
  // nervous beginner to sit waiting for permission.
  //
  // The message starts with "The student clicked", which INJECTED_PREFIX
  // filters: a button press is the student acting, but it is not their
  // words, and it must never be logged as something they said.
  const signalPath = () =>
    path.join(process.cwd(), "session_artifacts", "student_signal.txt");
  const readSignalLines = (): string[] => {
    try {
      return fs
        .readFileSync(signalPath(), "utf-8")
        .split("\n")
        .map((l) => l.trim())
        .filter(Boolean);
    } catch {
      return [];
    }
  };
  // Whatever is already in the file belongs to an earlier session.
  let signalMark = readSignalLines().length;
  const signalTimer = setInterval(() => {
    try {
      const lines = readSignalLines();
      if (lines.length < signalMark) signalMark = lines.length; // reset/archived
      if (lines.length <= signalMark) return;
      const widget = lines[lines.length - 1];
      signalMark = lines.length;
      if (!/^[A-Za-z_]\w*$/.test(widget)) return;
      // Two kinds of box send: a photo drop area, and an exercise code box
      // (whose widget name ends in _ed). They need opposite instructions —
      // one is read with the vision model, the other with nb_read — and a
      // tutor told to call nb_view_image on a code box burns a turn on an
      // error the student then watches it recover from.
      const isCode = /_ed$/.test(widget);
      pi.sendMessage(
        {
          customType: "student-signal",
          content: isCode
            ? `The student clicked "Send my code to my tutor" in the notebook: they have ` +
              `run their code and are handing it in. Read it with ` +
              `nb_read(["${widget}.value"]) now — do not ask them to paste it. Their ` +
              `output is already on screen under the box; react to what THEIR code and ` +
              `chart actually show, and ask the checkpoint's question about it. If the ` +
              `code does not run or does not do the task, say so warmly and point at the ` +
              `one line to change — they can edit and press ▶ Run again as often as they ` +
              `like, then send again.`
            : `The student clicked "Send to my tutor" in the notebook: their photo is ` +
              `uploaded and showing in the "${widget}" box. Call ` +
              `nb_view_image(widget="${widget}", …) now — do not ask them whether it is ` +
              `up. Judge what you see against the task, and say something specific about ` +
              `THEIR picture. If it does not show what the checkpoint asked for, say so ` +
              `warmly and ask them to redo it and drop the new photo into the same box; ` +
              `they can replace it as many times as they need.`,
          display: false,
        },
        { deliverAs: "followUp", triggerTurn: true },
      );
    } catch {
      // the button is a convenience — never let it break a turn
    }
  }, 2000);
  (signalTimer as any).unref?.();

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
        // An empty log means the module has NOT started, whatever
        // chapter_state.json says — that file outlives the log it belongs
        // to. A fresh start archives the log; if the saved chapter were
        // still trusted after that, the "clean slate" session would open in
        // the middle of the module, on top of whatever cells the wipe left
        // behind. Seen exactly that way: no log, chapter_state "ch3", and a
        // notebook whose first cell was chapter 3's heading.
        let chapter =
          cps.length > 0
            ? (chapters.find((c) => c.id === currentChapterId()) ?? chapters[0])
            : chapters[0];
        pendingCheckpoint = chapter.checkpoints[0] ?? null;
        let moduleFinished = false;
        if (cps.length > 0) {
          const order = chapters.flatMap((c) => c.checkpoints);
          // Where to pick up = the FIRST checkpoint with no log row, not the
          // one after the last row. Two earlier shapes of this both failed:
          // "after the last logged" walked a student who had a gap in the
          // middle past it, and answering "is the last one logged?" separately
          // from "where next?" produced a brief that said "continue at
          // checkpoint undefined". One question, asked once — and off-script
          // rows (a stretch, a typo) simply are not in `order`, so they can no
          // longer drag the answer anywhere.
          const doneIds = new Set(cps.map((e: any) => baseCheckpointId(String(e.id))));
          const nextId = order.find((o: string) => !doneIds.has(o));
          // No next id means every scripted checkpoint has a row: the module
          // is finished. Do NOT fall back to the last checkpoint — that tells
          // the tutor to re-run cp8, whose re-close silently skips the
          // existing session_record while overwriting session_summary.md, and
          // the two then disagree.
          const finished = !nextId;
          moduleFinished = finished;
          chapter = (nextId && chapters.find((c) => c.checkpoints.includes(nextId))) || chapter;
          pendingCheckpoint = nextId ?? null;
          // The continue-or-fresh answer below is session mechanics, not a
          // lesson answer, and nothing drains the pick buffer until the next
          // checkpoint_done — so without this it rode into that checkpoint's
          // record and printed as *You chose: "Continue where we left off"*
          // under a lecture question in the submitted notebook.
          awaitingResumeChoice = true;
          pi.sendMessage(
            {
              customType: "resume-brief",
              content:
                `RESUME CONTEXT (invisible to the student — never mention this message): ` +
                `a previous session exists. Progress so far:\n${progressBrief(entries)}\n` +
                `FIRST, greet the student and ask with ask_user_question: continue where you left ` +
                `off, or start fresh? If they choose fresh: call nb_fresh_start and follow ` +
                `its instructions (chapter 1 reloads automatically — do not improvise). ` +
                (finished
                  ? (fs.existsSync(path.join(process.cwd(), "session_artifacts", "session_summary.md"))
                      ? `If they continue: they already FINISHED this module — do not re-run any ` +
                        `checkpoint and do not call chapter_done. Say so warmly, offer to answer ` +
                        `questions or replay any experiment in the notebook, and log anything you ` +
                        `answer with log_detour.`
                      // Every checkpoint is logged but the closing record was never
                      // written — the last session ended between the final answer and
                      // chapter_done. Seen live: the tutor said a warm goodbye and the
                      // student's notebook shipped with no session_record and no
                      // summary, the two things the grader opens first.
                      : `If they continue: every checkpoint is logged but this module was ` +
                        `never CLOSED — there is no session_record cell and no summary. Do ` +
                        `not re-run any checkpoint. Say one warm line that you are just ` +
                        `filing their work, call chapter_done to write the closing record, ` +
                        `and then say goodbye.`)
                  : `If they continue: do NOT rebuild existing notebook cells ` +
                    `(nb_add_template skips duplicates automatically), remind them in one ` +
                    `sentence where you two left off, and continue at checkpoint ${nextId} ` +
                    `(chapter "${chapter.title}").`),
              display: false,
            },
            { deliverAs: "nextTurn" },
          );
        }
        writeChapterState(chapter.id);
        const num = chapters.findIndex((c) => c.id === chapter.id) + 1;
        // A finished module gets NO chapter script: it ends "work its
        // checkpoints in order... then call chapter_done", which is the exact
        // opposite of the resume brief above, and re-running cp8 appends a
        // duplicate log row against a note cell that skips as already there.
        if (!moduleFinished) {
          pi.sendMessage(
            {
              customType: "chapter-script",
              content: chapterScriptMessage(chapter, num, chapters.length),
              display: false,
            },
            { deliverAs: "nextTurn" },
          );
        }
        // Delayed and retried: the kernel is still booting at session start,
        // and stays cold until a browser client connects. Each attempt
        // re-checks that this chapter is still current — if the student
        // chose "start fresh" (or a chapter transition otherwise happened),
        // inserting its header would land a stray "Chapter N" heading in
        // the middle of a different chapter's cells (seen in production).
        scheduleChapterHeader(chapter, num, chapters.length);
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

      // ── The chapter must actually have been taught ──────────────────────
      // A chapter transition compacts the conversation, and a model that
      // comes out of compaction disoriented can call chapter_done a second
      // time. That happened in a live session: two transitions fired back to
      // back and the student went from chapter 1 straight into chapter 3's
      // pen-and-paper task, having never met distance or clustering. The
      // student picker below cannot catch it — they were asked "anything
      // first?" about a chapter that had not happened.
      const cur = chapters[idx];
      if (cur) {
        const loggedIds = new Set(
          readSessionLog()
            .filter((e: any) => e?.type === "checkpoint" && e.id)
            .map((e: any) => baseCheckpointId(String(e.id))),
        );
        const missing = cur.checkpoints.filter((c) => !loggedIds.has(c));
        if (missing.length > 0) {
          return {
            content: [
              {
                type: "text" as const,
                text:
                  `NOT ADVANCED — "${cur.title}" is not finished. These checkpoints have ` +
                  `never been logged: ${missing.join(", ")}. Say nothing about this to the ` +
                  `student; just carry on with "${missing[0]}" from your CHAPTER SCRIPT, ` +
                  `ending it with checkpoint_done, and call chapter_done again once the ` +
                  `chapter's last checkpoint is logged.`,
              },
            ],
            details: { gated: true },
          };
        }
      }

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
      // Re-arm the build-ordering guard on the new chapter's first
      // checkpoint, so it keeps working across the transition instead of
      // still pointing at the chapter that just ended.
      pendingCheckpoint = next.checkpoints[0] ?? pendingCheckpoint;
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
            "Fills for the «slots» in the script's note: skeleton — ONE per slot, in " +
            "order, in the student's own words. Most skeletons have several (a slot per " +
            "part of the ask); sending fewer is refused, and after two refusals the " +
            "unfilled ones are printed as '(not answered)' in the graded notebook.",
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
      let response = String(params.student_response ?? "").trim();
      if (!response) {
        return toResult({
          out: `NOT LOGGED — student_response is empty. Log their actual words (or "(no answer — moved on)") and call again.`,
          failed: false,
        });
      }
      // A checkpoint whose script promises a build cannot be closed while
      // that build is missing. cp5_ring_formula asks seven things and the
      // seventh is "photograph that page"; a live run answered the first
      // six, decided the reasoning was complete, and closed — the upload
      // area was never inserted and the photo never asked for, on a
      // checkpoint whose whole point is the page in the student's own hand.
      // Capped like the rest, so a dead notebook cannot strand anyone.
      const wantCells = scriptedBuildCells(baseCheckpointId(id));
      let missingBuild: string[] = [];
      if (wantCells.length > 0) {
        const have = await notebookCellNames(signal);
        if (have) missingBuild = wantCells.filter((c) => !have.includes(c));
      }
      const buildStrikes = slotDriftWarned.get(`${id}:build`) ?? 0;
      if (missingBuild.length > 0 && buildStrikes < 2) {
        slotDriftWarned.set(`${id}:build`, buildStrikes + 1);
        return toResult({
          out:
            `NOT LOGGED — this checkpoint's build never happened: ${missingBuild
              .map((c) => `"${c}"`)
              .join(", ")} ${missingBuild.length > 1 ? "are" : "is"} missing from the ` +
            `notebook. Read your script's build: line for "${baseCheckpointId(id)}", run ` +
            `the nb_add_template it names, and work the part of the ask that goes with it ` +
            `— on a paper checkpoint that means asking for the photo and WAITING for the ` +
            `📨 Send press. Then call checkpoint_done again.`,
          failed: false,
        });
      }
      // The build existing is not the same as the page being asked for. On a
      // checkpoint whose build inserts a drop area, either a photo came
      // through (nb_view_image saw it) or the student said they cannot take
      // one — and in that case the record should say so. One nudge, then it
      // logs either way with the gap on the row.
      const wantPhotos = wantCells.filter((c) => /_photo$/.test(c));
      // The in-memory set dies with the process, but the photo itself does
      // not: nb_view_image saves the original under assets/uploads/. Consult
      // both, or a resume after a photo was already read re-fires the
      // refusal and stamps a false `photo_missing` on the graded row.
      const uploadedOnDisk = (w: string): boolean => {
        try {
          return fs
            .readdirSync(path.join(process.cwd(), "assets", "uploads"))
            .some((f) => f.startsWith(`${w}_upload`) || f.startsWith(`${w}_view`));
        } catch {
          return false;
        }
      };
      const photoMissing =
        wantPhotos.length > 0 &&
        !wantPhotos.some((w) => viewedPhotos.has(w) || uploadedOnDisk(w));
      if (photoMissing && (slotDriftWarned.get(`${id}:photo`) ?? 0) < 1) {
        slotDriftWarned.set(`${id}:photo`, 1);
        return toResult({
          out:
            `NOT LOGGED — this is a pen-and-paper checkpoint and no photo has reached ` +
            `me for "${wantPhotos[0]}". If you have not asked yet: SAY THE ASK OUT LOUD ` +
            `to the student now — the page and nothing else — and only then end your ` +
            `turn. Never end a turn on this without speaking: a silent turn is a frozen ` +
            `screen, and in a live run it left a student waiting ten minutes. Their 📨 ` +
            `Send press starts the next turn, and you read it with nb_view_image.\n` +
            `If they have already told you they cannot photograph, that is fine and their ` +
            `typed work counts — say so in notes ("camera broken, typed instead") and ` +
            `call checkpoint_done again; it will log.`,
          failed: false,
        });
      }
      // Peek, don't consume: a refusal below must leave the transcript mark
      // where it was, or the retry would log an empty student_said_verbatim.
      const said = studentSaidSince(ctx, false);
      const picked = pickedSince(false);
      const slots = (params.note_slots ?? []).map((s: unknown) => String(s ?? ""));
      // Note «slots» the instructor marked «… verbatim» are held to the
      // student's own words. «their pick» (a picker choice, which never
      // reaches the transcript) and free commentary slots are the tutor's to
      // phrase, and are not checked. The bar is deliberately low — reordering
      // and joining and labelling are all fine — so that only invention
      // trips it: a figure they never gave, or three added content words.
      //
      // The pool is the transcript plus the QUESTION's own vocabulary —
      // echoing the words of the question ("distance", "average") is
      // labelling, not fabrication. student_response is deliberately NOT in
      // it: it is model-authored, so including it let the model whitelist
      // its own paraphrase by writing the same text into both fields, which
      // is exactly the failure the check exists to catch.
      //
      // With nothing typed there is nothing to check against, so the check
      // stands down rather than guessing. Checkpoints answered by drawing or
      // photograph are marked in the script instead: their slots do not say
      // «verbatim», because the tutor legitimately writes what the picture
      // shows there, and holding that to the transcript refused honest
      // records (it did, for every photo checkpoint).
      // `picked` belongs in the pool as much as `said` does: a dialog choice
      // IS the student's own answer. Leaving it out refused cp1's honest
      // record twice ("about 20" — the figure 20 appears in neither the
      // typed follow-up nor the question) and then stamped a false quoting
      // warning on it in the submitted notebook.
      const pool = [...said, ...picked, String(params.question ?? "")];
      const markers = slotMarkers(noteSkeleton(id));
      const problems: string[] = [];
      // One fill per slot. The skeletons ask for a slot per part of the ask
      // precisely so the keepsake quotes the ANSWER and not whichever
      // fragment came last — under-filling turns that back into one sentence
      // repeated under three labels.
      const slotStrikes = slotDriftWarned.get(`${id}:slots`) ?? 0;
      // No note_markdown exemption: the renderer ignores note_markdown
      // whenever a skeleton exists, so taking that escape hatch discarded the
      // tutor's note and printed "*(not answered)*" under slots the student
      // had answered. Count NON-EMPTY fills — padding with "" satisfied a
      // length check and produced the same placeholder.
      const filled = slots.filter((f) => f.trim()).length;
      if (markers.length > 1 && filled < markers.length && slotStrikes < 2) {
        slotDriftWarned.set(`${id}:slots`, slotStrikes + 1);
        return toResult({
          out:
            `NOT LOGGED — this checkpoint's note has ${markers.length} slots and you sent ` +
            `${filled} filled. One fill each, in this order:\n` +
            markers
              .map(
                (m, i) =>
                  `  ${i + 1}. ${m.replace(/[«»]/g, "").replace(/\s+/g, " ").trim()}`,
              )
              .join("\n") +
            `\nQuote them for each part separately — the slots exist so the notebook holds ` +
            `their ANSWER and not just whichever fragment came last. Then call ` +
            `checkpoint_done again.`,
          failed: false,
        });
      }
      // A skeleton that asks for the student's own words, on a checkpoint
      // where the student never typed any, means the question that was
      // supposed to get those words was skipped. cp1 is the case that
      // showed it: answered entirely through the picker, its reveal asks
      // one typed follow-up, and when the tutor jumped straight to
      // checkpoint_done the slot fell back to student_response and the
      // notebook read "**My guess:** about 60 — about 60". Photo and
      // drawing checkpoints are exempt by construction: their slots are
      // deliberately not marked «verbatim».
      if (said.length === 0 && markers.some((m) => /verbatim/i.test(m))) {
        problems.push(
          `this checkpoint's note quotes the student's own words, but they have not ` +
            `typed anything here yet — ask them the question your script's reveal_after ` +
            `names, in plain text, and wait for their answer`,
        );
      }
      // student_response is the headline quote of the graded record, so it
      // gets the same treatment as a «verbatim» slot — plus a repair the
      // slots do not need. A near-copy is snapped back to the transcript
      // silently (the correction is recorded in the log, not paraded at the
      // student), and only real invention — a figure or three content words
      // they never produced — is bounced back to the model.
      let responseSnappedFrom: string | null = null;
      if (said.length > 0) {
        const snapped = snapToTranscript(response, said);
        if (snapped) {
          responseSnappedFrom = response;
          response = snapped;
        }
        const d = slotDrift(response, pool);
        if (d.numbers.length > 0 || d.words.length >= 3) {
          problems.push(
            `student_response ("${response.slice(0, 80)}") adds ` +
              [...d.numbers, ...d.words].map((t) => `"${t}"`).join(", "),
          );
        }
      }
      // When the answer came ONLY from a picker, student_response must be the
      // option they actually chose. This is the one case the transcript can't
      // police and the one a live run got backwards.
      if (said.length === 0 && picked.length > 0) {
        const pool = new Set(picked.flatMap(slotTokens));
        const shared = slotTokens(response).some((t) => pool.has(t) && !SLOT_GLUE.has(t));
        if (!shared) {
          problems.push(
            `student_response ("${response.slice(0, 80)}") does not match what they picked: ` +
              picked.map((p) => `"${p}"`).join(", "),
          );
        }
      }
      // The slots are the ask's parts, in order, and so are the messages the
      // student typed. A live run filled them shifted by one — every quote
      // was something they really said, so the drift check passed, but each
      // slot answered the previous question and the LAST answer (the
      // synthesis the checkpoint exists for) was dropped from the keepsake
      // entirely. The cheap invariant that catches the shift: the final
      // «verbatim» slot has to come from their final message.
      const lastVerbatim = markers.reduce(
        (acc, m, i) => (/verbatim/i.test(m) ? i : acc),
        -1,
      );
      if (
        lastVerbatim >= 0 &&
        markers.filter((m) => /verbatim/i.test(m)).length > 1 &&
        said.length > 1 &&
        slots[lastVerbatim] &&
        (slotDriftWarned.get(`${id}:order`) ?? 0) < 1
      ) {
        const tail = said[said.length - 1];
        const flatten = (x: string) => x.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
        const fits =
          flatten(slots[lastVerbatim]).includes(flatten(tail)) ||
          flatten(tail).includes(flatten(slots[lastVerbatim])) ||
          bigramDice(slots[lastVerbatim], tail) >= 0.5;
        if (!fits) {
          slotDriftWarned.set(`${id}:order`, 1);
          return toResult({
            out:
              `NOT LOGGED — the slots are the parts of the ask IN ORDER, and so are the ` +
              `messages they typed. The last slot ` +
              `(${markers[lastVerbatim].replace(/[«»]/g, "").replace(/\s+/g, " ").trim()}) ` +
              `does not hold their last answer, which means the fills are shifted and ` +
              `their final answer is about to be dropped from the notebook.\n` +
              `In order, they said: ${said.map((x, i) => `[${i + 1}] "${x.slice(0, 90)}"`).join("  ")}\n` +
              `Map each slot to the reply that ANSWERED that part, then call ` +
              `checkpoint_done again.`,
            failed: false,
          });
        }
      }
      for (const [i, fill] of slots.entries()) {
        if (said.length === 0) break;
        if (!/verbatim/i.test(markers[i] ?? "")) continue;
        const d = slotDrift(fill, pool);
        if (d.numbers.length === 0 && d.words.length < 3) continue;
        problems.push(
          `note slot ${i + 1} ("${fill.slice(0, 80)}") adds ` +
            [...d.numbers, ...d.words].map((t) => `"${t}"`).join(", "),
        );
      }

      // Two refusals per checkpoint, then it logs anyway with the drift
      // flagged for the grader: a model that cannot satisfy the check must
      // never be able to strand the student mid-lesson.
      const strikes = slotDriftWarned.get(id) ?? 0;
      if (problems.length > 0 && strikes < 2 && said.length === 0) {
        slotDriftWarned.set(id, strikes + 1);
        return toResult({
          out:
            `NOT LOGGED — ${problems.join("; ")}.\n` +
            `Do not write that line for them and do not call checkpoint_done again ` +
            `until they have answered. SAY THE QUESTION OUT LOUD in plain text — never ` +
            `end this turn without speaking, a silent turn is a frozen screen — then ` +
            `wait, and log what they type.`,
          failed: false,
        });
      }
      if (problems.length > 0 && strikes < 2) {
        slotDriftWarned.set(id, strikes + 1);
        return toResult({
          out:
            `NOT LOGGED — student_response and every «verbatim» note slot are the ` +
            `student's own words, and these are not in anything they said: ` +
            `${problems.join("; ")}.\n` +
            `What they actually typed: ${said.map((s) => `"${s}"`).join(", ")}.\n` +
            `Quote them, don't polish — no figure they didn't give, no sentence built out ` +
            `of your own summary. Your reading of a drawing, or a number a widget showed, ` +
            `belongs in notes.` +
            (picked.length
              ? ` They picked: ${picked.map((p) => `"${p}"`).join(", ")} — record THAT.`
              : "") +
            ` Then call checkpoint_done again.`,
          failed: false,
        });
      }
      // The next scripted checkpoint is now the open one, even if it builds
      // nothing — that is what keeps its note cell ahead of the next build.
      // Off-script ids (a stretch, a typo) must NOT null it out: that would
      // switch the ordering guard off for the rest of the session.
      if (isScriptedCheckpoint(id)) pendingCheckpoint = nextCheckpointId(id);
      // The resume window closes with the first checkpoint: past this point
      // every dialog answer is a lesson answer.
      awaitingResumeChoice = false;
      studentSaidSince(ctx, true);
      pickedSince(true);

      // A checkpoint that needed hints is `pass_with_hints`, whatever the
      // model typed. It logged plain `pass` with hints_used 2 in a live run —
      // not dishonesty, just two fields the model has to keep agreeing, so
      // the extension makes them agree. Hints are never penalised; the point
      // is that the record says what happened.
      let hintsOut = Math.max(0, Math.round(Number(params.hints_used ?? 0) || 0));
      // The two fields must agree, whichever way round they were typed. A
      // `guided` checkpoint is by definition one the tutor walked them
      // through, so zero hints there is a miscount, not a cleaner record.
      const judgmentOut =
        judgment === "pass" && hintsOut > 0
          ? "pass_with_hints"
          : judgment === "pass_with_hints" && hintsOut === 0
            ? "pass"
            : judgment;
      if (judgmentOut === "guided" && hintsOut === 0) hintsOut = 1;
      const logged = appendLog({
        type: "checkpoint",
        id,
        question: String(params.question ?? ""),
        student_response: response,
        judgment: judgmentOut,
        hints_used: hintsOut,
        notes: String(params.notes ?? ""),
        student_said_verbatim: said,
        ...(picked.length > 0 ? { student_picked: picked } : {}),
        ...(responseSnappedFrom ? { response_retyped_as: responseSnappedFrom } : {}),
        ...(photoMissing ? { photo_missing: true } : {}),
        ...(problems.length > 0 ? { verbatim_drift: problems } : {}),
      });

      const suppressed = noteSuppressed(id);
      const skeleton = suppressed ? "" : noteSkeleton(id);
      const md = suppressed
        ? ""
        : skeleton
          ? fillSlots(skeleton, params.note_slots ?? [], response)
          : String(params.note_markdown ?? "").trim();
      let noteLine: string;
      if (suppressed) {
        noteLine =
          `No note cell for this one, by design (the script says note: none) — it is ` +
          `logged and appears in the closing record. Do NOT add one yourself.`;
      } else if (!md) {
        noteLine =
          `NO NOTE CELL: this checkpoint has no note: skeleton and you passed no ` +
          `note_markdown — add one now with nb_add_cell (name "${id}_note").`;
      } else {
        const r = await insertMarkdownCell(`${id}_note`, md, signal);
        noteLine = r.failed
          ? `Note cell FAILED — retry once with nb_add_cell (name "${id}_note").`
          : `Note cell added.`;
      }

      // Every branch NAMES the checkpoint to go to. Without that, a small
      // model three practice rounds deep loses the thread: in a live run it
      // answered READY by inventing yet another warm-up and logging
      // cp0_welcome_extra, then _extra_extra — the student could not leave
      // cp0 at all. "Start the next checkpoint from your script" is not an
      // instruction a flash model can act on; "start cp1_milgram" is.
      const nextId = nextCheckpointId(id);
      // "Find it in your CHAPTER SCRIPT" is only true while the next id is in
      // THIS chapter. At every chapter boundary it named a checkpoint the
      // script in context does not contain, contradicting the script's own
      // closing line ("call chapter_done") in the same turn — and the tool
      // result is the instruction a flash model actually follows.
      const thisChapter = loadChapters().find((c) => c.checkpoints.includes(baseCheckpointId(id)));
      const nextIsHere = !!nextId && !!thisChapter && thisChapter.checkpoints.includes(nextId);
      const goNext = !nextId
        ? `That was the last checkpoint of the module — call chapter_done next.`
        : nextIsHere
          ? `Start checkpoint "${nextId}" NOW: find it in your CHAPTER SCRIPT and ask its ` +
            `first question. Do not revisit "${baseCheckpointId(id)}".`
          : `That was the last checkpoint of this chapter — call chapter_done next. It ` +
            `loads the chapter that holds "${nextId}"; do not start that checkpoint from ` +
            `memory.`;
      const READY = "Ready for the next question";
      const ASK_Q = "I have a question first";
      const MORE = "Give me another one like that";
      let nextLine =
        `No picker available — ask the student in plain text whether to move on, ` +
        `and wait for their answer. When they say yes: ${goNext}`;
      if (ctx?.ui?.select) {
        const choice = await ctx.ui.select("Where to next?", [READY, ASK_Q, MORE]);
        const practiceRound = /_extra/.test(id);
        nextLine =
          choice === READY
            ? `The student is READY. ${goNext}`
            : choice === ASK_Q
              ? `The student has a QUESTION. Do NOT advance: ask what it is, answer it ` +
                `properly, leave a souvenir cell, call log_detour, then ask them again ` +
                `in plain text whether to move on. When they are ready: ${goNext}`
              : choice === MORE
                ? // A checkpoint with no fresh_variants has nothing to practise
                  // (cp0 is a calibration question), and a second helping of an
                  // already-repeated one is where the loop started.
                  !hasFreshVariants(baseCheckpointId(id))
                  ? `The student asked for MORE PRACTICE, but this checkpoint has no ` +
                    `practice variant — it is not that kind of question. Say so warmly in ` +
                    `ONE sentence, then: ${goNext}`
                  : practiceRound
                    ? `They have already had a practice round here. Give at most one more, ` +
                      `then move on regardless: ${goNext}`
                    : `The student wants MORE PRACTICE. Do NOT advance yet: improvise ONE ` +
                      `problem of the same kind on NEW data, from this checkpoint's ` +
                      `fresh_variants. Guide, then checkpoint_done again with id ` +
                      `"${baseCheckpointId(id)}_extra" (never a fail). After that: ${goNext}`
                : `The student closed the picker — ask in plain text what they'd like to do. ` +
                  `If they want to move on: ${goNext}`;
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
      "engagement) and leave the souvenir in their notebook. Build the souvenir with " +
      "nb_add_cell first — text AND a picture in one mo.vstack, or a playable demo — and " +
      "pass its cell_name. souvenir_markdown is the fallback for an idea no picture helps.",
    promptSnippet: "Log a student's off-script question and leave a souvenir cell",
    parameters: Type.Object({
      status: STATUS_PARAM,
      question: Type.String({ description: "Their question VERBATIM." }),
      what_you_did: Type.String({ description: "One line: how you answered it." }),
      souvenir_markdown: Type.Optional(
        Type.String({
          description:
            "Fallback only: markdown for a text-only 🧭 Detour cell. Prefer nb_add_cell " +
            "+ cell_name, so the souvenir has something to look at or play with.",
        }),
      ),
      cell_name: Type.Optional(
        Type.String({ description: "Name of the souvenir cell you already added." }),
      ),
    }),
    async execute(_id, params, signal, _onUpdate, ctx: any) {
      const question = String(params.question ?? "").trim();
      const md0 = String(params.souvenir_markdown ?? "").trim();
      const cellName = String(params.cell_name ?? "").trim();
      // A souvenir is a keepsake, not a log line: the notebook's whole promise
      // is that a curious student's copy looks different from everyone else's,
      // and four text-only blobs in one live session is what that failure
      // looks like. Bounced ONCE, with both ways out spelled out, then
      // accepted — some ideas really are just words.
      //
      // The cell the tutor built ITSELF is checked the same way. Trusting
      // that path was the hole: every detour in the failing session arrived
      // as a cell_name, and every one of them was prose that never quoted
      // the question it answered.
      let gap = "";
      if (cellName) {
        const src = await readCellSource(cellName, signal);
        if (src !== null) gap = souvenirGap(src, question);
      }
      if (gap && !detourTextOnlyWarned.has(question)) {
        detourTextOnlyWarned.add(question);
        return toResult({
          out:
            `NOT LOGGED YET — the souvenir cell "${cellName}" ${gap}. Fix it with ` +
            `nb_edit_cell so it is ONE cell holding both: their question quoted ` +
            `("${question.slice(0, 60)}") and something to see or try —\n` +
            `  mo.vstack([mo.md(r"""> 🧭 **You asked:** “…”\n\n…"""), netviz(edges, highlight=[…])])\n` +
            `— or an nb_add_exercise box if the idea is playable. Then call log_detour ` +
            `again with the same cell_name.\n` +
            `If words genuinely are the whole answer here, call log_detour again as it ` +
            `is and it will be accepted.`,
          failed: false,
        });
      }
      if (!cellName && md0 && !detourTextOnlyWarned.has(question)) {
        detourTextOnlyWarned.add(question);
        return toResult({
          out:
            `NOT LOGGED YET — a text-only souvenir is the weakest kind of keepsake. Build ` +
            `the cell first with nb_add_cell (name "detour_<topic>"), text and picture in ` +
            `ONE cell: mo.vstack([mo.md(r"""…"""), netviz(edges, highlight=[…])]) — or an ` +
            `nb_add_exercise box if the idea is something they can try. Then call ` +
            `log_detour again with cell_name.\n` +
            `If a picture genuinely adds nothing to this one, call log_detour again with ` +
            `the same souvenir_markdown and it will be accepted as it is.`,
          failed: false,
        });
      }
      appendLog({
        type: "detour",
        question,
        what_you_did: String(params.what_you_did ?? ""),
        cell: String(params.cell_name ?? ""),
        // Peek, never consume: a detour normally happens mid-checkpoint, and
        // consuming the mark here would move the student's checkpoint answer
        // into the detour record — leaving checkpoint_done with an empty
        // student_said_verbatim and a drift check with nothing to match.
        student_said_verbatim: studentSaidSince(ctx, false),
        // Accepted on the retry despite the gap — the grader sees what the
        // souvenir was missing rather than the tool pretending it was fine.
        ...(gap ? { souvenir_gap: gap } : {}),
      });
      if (!md0) {
        return toResult({
          out: cellName
            ? `Logged. Souvenir cell "${cellName}" noted.`
            : `Logged — but NO souvenir cell yet. Add one now (nb_add_cell, name ` +
              `"detour_<topic>"): their question quoted plus the idea, text and picture ` +
              `together in ONE cell (mo.vstack + netviz).`,
          failed: false,
        });
      }
      const md = withQuotedQuestion(md0, question);
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
      await ensureChapterHeader(signal);
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
      // Two refusals per cell name, then it goes in with the complaint
      // attached — the same backstop every other guard here has. A review
      // the model cannot satisfy must never be able to strand the student
      // in a retry loop; a cell with one bad formula is the smaller harm,
      // and nb_edit_cell can still fix it.
      const strikes = cellReviewWarned.get(params.name) ?? 0;
      const enforce = review && strikes < 2;
      if (review && !enforce) cellReviewWarned.delete(params.name);
      else if (review) cellReviewWarned.set(params.name, strikes + 1);
      const code =
        `import marimo._code_mode as cm\n` +
        (review ? review + "\n" : "") +
        `_code = ${py(stripRedundantImports(params.code))}\n` +
        (review
          ? `_code, _note, _fatal = _nb_review(_code)\n` +
            (enforce
              ? `if _fatal:\n` +
                `    print(_fatal)\n` +
                `else:\n` +
                indentBlock(inner, 4) +
                `    if _note:\n` +
                `        print(_note)\n`
              : indentBlock(inner, 0) +
                `if _fatal or _note:\n` +
                `    print("INSERTED ANYWAY (third attempt) —", _fatal or _note, ` +
                `"Fix it with nb_edit_cell rather than retrying.")\n`)
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
      "is ONLY for variables another notebook cell already defines (a graph G you built " +
      "earlier) — never the scaffold's own variables, which live inside the code box. " +
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
      const exCpId = String(params.checkpoint ?? "").trim();
      if (exCpId && pendingCheckpoint && isAheadOf(exCpId, pendingCheckpoint)) {
        return toResult({
          out:
            `NOT INSERTED — '${exCpId}' comes after '${pendingCheckpoint}', which is still ` +
            `open. Call checkpoint_done for '${pendingCheckpoint}' first (its note cell ` +
            `must land before this build), then retry this insert.`,
          failed: false,
        });
      }
      // env_vars becomes a REAL reference in the generated cell, which is
      // how marimo passes a notebook variable into the exercise — and how a
      // name that does not exist takes the whole notebook down. A live run
      // listed the scaffold's OWN variables (N, k, p_values, L0, C0, rows,
      // df), which live only inside the editor's text, and the export died
      // with "name 'p_values' is not defined" on a cell the student cannot
      // even see. So only names the kernel actually defines get through.
      const asked = (params.env_vars ?? []).filter((v: string) => /^[A-Za-z_]\w*$/.test(v));
      let envVars = asked;
      let droppedEnv: string[] = [];
      if (asked.length) {
        const probe = await runKernel(
          `print("DEFINED<<" + ",".join(_n for _n in ${pyList(asked)} if _n in globals()) + ">>")\n`,
          signal,
        );
        const m = /DEFINED<<(.*)>>/.exec(probe.out ?? "");
        if (!probe.failed && m) {
          const defined = new Set(m[1].split(",").filter(Boolean));
          envVars = asked.filter((v) => defined.has(v));
          droppedEnv = asked.filter((v) => !defined.has(v));
        }
      }
      const envDict = `{${envVars.map((v: string) => `${py(v)}: ${v}`).join(", ")}}`;
      const warm = await ensureWarm(signal);
      if (warm) return toResult(warm);
      await ensureChapterHeader(signal);
      const edBody =
        `${name}_ed = mo.ui.code_editor(value=${py(params.scaffold)}, language="python", min_height=140)\n` +
        `${name}_run = mo.ui.run_button(label="▶ Run my code")\n` +
        `mo.vstack([mo.md(${pyMd(params.instructions)}), ${name}_ed, ${name}_run])`;
      // Every ▶ Run writes the code to assets/exercises/<name>.py. marimo
      // does NOT serialise a code_editor's value, so without this the one
      // coding checkpoint left nothing in the submitted notebook: reopen it
      // and the box is back to the scaffold, the chart is gone, and the
      // grader sees `...` blanks where the student's work was. Same cure as
      // the photo view cell — save the artifact, render it from disk.
      const savedPath = `assets/exercises/${name}.py`;
      const outBody =
        `from pathlib import Path as _P\n` +
        `_saved = _P(${py(savedPath)})\n` +
        `${name}_send = mo.ui.run_button(\n` +
        `    label="📨 Send my code to my tutor",\n` +
        `    disabled=not (${name}_run.value or _saved.exists()),\n` +
        `)\n` +
        `if ${name}_run.value:\n` +
        `    _saved.parent.mkdir(parents=True, exist_ok=True)\n` +
        `    _saved.write_text(${name}_ed.value)\n` +
        `    _res = mo.vstack([\n` +
        `        run_student_code(${name}_ed.value, ${envDict}),\n` +
        `        mo.md(\n` +
        `            "<span style='color:#6A6D75;font-size:13px'>Run it as many times "\n` +
        `            "as you like. When it does what you want, press 📨 — that is what "\n` +
        `            "hands it in and tells your tutor to look.</span>"\n` +
        `        ),\n` +
        `        ${name}_send,\n` +
        `    ])\n` +
        `elif _saved.exists():\n` +
        `    _res = mo.vstack([\n` +
        `        mo.md(\n` +
        `            "<span style='color:#6A6D75;font-size:13px'>The code I wrote and "\n` +
        `            "ran — press ▶ Run again after an edit to refresh this:</span>"\n` +
        `            "\\n\\n\`\`\`python\\n"\n` +
        `            + _saved.read_text()\n` +
        `            + "\\n\`\`\`"\n` +
        `        ),\n` +
        `        run_student_code(_saved.read_text(), ${envDict}),\n` +
        `        ${name}_send,\n` +
        `    ])\n` +
        `else:\n` +
        `    _res = mo.md("*Press ▶ Run when you're ready.*")\n` +
        `_res`;
      const sentBody =
        `from pathlib import Path as _P\n` +
        `if ${name}_send.value:\n` +
        `\n` +
        `    _P("session_artifacts").mkdir(exist_ok=True)\n` +
        `    with open("session_artifacts/student_signal.txt", "a") as _f:\n` +
        `        _f.write(${py(name + "_ed")} + "\\n")\n` +
        `    _sent = mo.md("✅ **Handed in.** Your tutor is reading your code now.")\n` +
        `else:\n` +
        // Not mo.md(""): an empty markdown node is a blank cell in the
        // keepsake, and reopening it always lands on this branch.
        // Only once the button is actually on screen — before the first
        // ▶ Run the out cell renders "Press ▶ Run when you're ready" and no
        // 📨 button at all, and pointing at it then is one more thing for a
        // nervous beginner to hunt for.
        `    _sent = mo.md(\n` +
        `        "<span style='color:#6A6D75;font-size:13px'>*Press 📨 above once the "\n` +
        `        "chart looks right — that is what hands your code in.*</span>"\n` +
        `        if _P(${py(savedPath)}).exists()\n` +
        `        else "<span style='color:#6A6D75;font-size:13px'>*A 📨 hand-in button "\n` +
        `        "appears here once you have pressed ▶ Run.*</span>"\n` +
        `    )\n` +
        `_sent`;
      let code =
        `import marimo._code_mode as cm\n` +
        `from pathlib import Path as _P\n` +
        `async with cm.get_context() as ctx:\n` +
        `    _names = [c.name for c in ctx.cells]\n` +
        `    if ${py(name + "_ed")} in _names:\n` +
        `        print("exercise already in the notebook — skipped duplicate insert")\n` +
        `    else:\n` +
        // Handing out the box means starting it. Any saved file here belongs
        // to someone else's session (or, once, to a solved copy committed by
        // mistake), and the out cell renders whatever it finds under "The
        // code I wrote and ran" — which would show this student the answer
        // before they typed a character, in their own voice.
        `        _P(${py(savedPath)}).unlink(missing_ok=True)\n` +
        `        _cid = ctx.create_cell(${py(edBody)}, name=${py(name + "_ed")}, hide_code=True)\n` +
        `        ctx.run_cell(_cid)\n` +
        `        _first = _cid\n` +
        `        _cid = ctx.create_cell(${py(outBody)}, name=${py(name + "_out")}, hide_code=True, after=_cid)\n` +
        `        ctx.run_cell(_cid)\n` +
        `        _cid = ctx.create_cell(${py(sentBody)}, name=${py(name + "_sent")}, hide_code=True, after=_cid)\n` +
        `        ctx.run_cell(_cid)\n`;
      code += focusCellCode("_first", "        ");
      const result = await runKernel(code, signal);
      if (!result.failed) {
        result.out =
          `Exercise inserted. The student sees your instructions, a runnable code box, a ` +
          (droppedEnv.length
            ? `Ignored env_vars the notebook does not define: ${droppedEnv.join(", ")} — ` +
              `those are your scaffold's own variables and belong inside the code box.\n`
            : "") +
          `▶ Run button, and — once they have run it — a 📨 Send button that hands the ` +
          `code in. Ask for the code, then WAIT: their press starts your turn. Every run ` +
          `saves the code to ${savedPath}, so it is still in the notebook months later.\n` +
          result.out;
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
      const cpId = String(params.checkpoint ?? "").trim();
      if (!cpId) {
        return toResult({
          out: `NOT INSERTED — pass checkpoint: the id of the checkpoint this build is for.`,
          failed: false,
        });
      }
      if (pendingCheckpoint && isAheadOf(cpId, pendingCheckpoint)) {
        return toResult({
          out:
            `NOT INSERTED — '${cpId}' comes after '${pendingCheckpoint}', which is still ` +
            `open. Call checkpoint_done for '${pendingCheckpoint}' first (its note cell ` +
            `must land before this build), then retry this insert.`,
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
      await ensureChapterHeader(signal);
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
          ? `Ask for the photo, then WAIT — never ask whether it is up. Their 📨 Send ` +
            `to my tutor press starts your turn; then call ` +
            `nb_view_image(widget="${uploads[0]}", …).\n`
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
    async execute(_id, params, signal, _onUpdate, ctx: any) {
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
        // The summary belongs to the run that produced it. Left in place it
        // outlives its log and describes checkpoints the new session never did.
        const sum = path.join(dir, "session_summary.md");
        if (fs.existsSync(sum)) fs.renameSync(sum, path.join(dir, `session_summary-${stamp}.md`));
        // Delete, don't rewrite: the saved chapter belongs to the log that
        // was just archived, and anything left in that file would be read
        // back as progress this session never made.
        fs.rmSync(chapterStatePath(), { force: true });
        // The student's saved exercise code goes with it. Left behind, the
        // next run of the coding checkpoint opens showing the PREVIOUS
        // student's code under "The code I wrote and ran" — someone else's
        // work, in this student's voice.
        // Both directories, for the same reason: they are the previous
        // student's work, and the photo guard reads assets/uploads as
        // evidence that a page arrived — stale files there disarm it before
        // the new student has taken a photo.
        for (const [rel, label] of [
          ["exercises", `exercises-${stamp}`],
          ["uploads", `uploads-${stamp}`],
        ] as const) {
          const src = path.join(process.cwd(), "assets", rel);
          if (fs.existsSync(src)) fs.renameSync(src, path.join(dir, label));
        }
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
          detourTextOnlyWarned.clear();
          // A fresh start rewinds the record too: anything picked before it
          // (the resume dialog, a previous run's answers) must not surface
          // in the new session's first checkpoint.
          pickedAnswers.length = 0;
          pickedMark = 0;
          awaitingResumeChoice = false;
          cellReviewWarned.clear();
          viewedPhotos.clear();
          // Same rewind for the transcript mark: without it, whatever the
          // student typed before choosing "start fresh" is filed as the new
          // cp0's own words.
          studentSaidSince(ctx, true);
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
        `            ctx.delete_cell(_c.id)\n` +
        // Say out loud what survived. A wipe that silently leaves a cell
        // behind is how a "clean slate" notebook opens on the middle of the
        // module — the tutor must know before it starts building.
        `    _left = [c.name for c in ctx.cells if c.name and c.name != "_"]\n` +
        `    if _left:\n` +
        `        print("STILL THERE (delete failed):", ", ".join(_left))\n`;
      // Same kernel call as the wipe so the chapter header lands first,
      // before any cp0/cp1 build cells.
      try {
        const chapters = loadChapters();
        if (chapters.length > 0) {
          const h = `${chapters[0].id}_header`;
          const heading = `## Chapter 1 of ${chapters.length} — ${chapters[0].title}`;
          const op = chapterOpening(chapters[0]);
          const body = `mo.md(${pyMd(op ? `${heading}\n\n${op}` : heading)})`;
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
      "original to assets/uploads/ so it travels with the notebook, shows the photo in the " +
      "notebook for the student, and " +
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
      // The caption is not decoration — an uncaptioned phone photo in the
      // middle of a lecture note is a mystery to anyone reading it cold,
      // including the student in three months. `task` already holds the ask
      // in the tutor's own words, so the cell states what the page shows.
      const taskLine = String(params.task ?? "")
        .replace(/\s+/g, " ")
        .trim()
        .replace(/["']/g, "");
      const caption =
        `<span style='color:#6A6D75;font-size:13px'>📷 My own work on paper` +
        (taskLine ? ` — the task: ${taskLine}` : "") +
        `</span>`;
      const cellBody =
        `from pathlib import Path as _P\n` +
        `mo.vstack([\n` +
        `    mo.image(_P(${py(viewRel)}).read_bytes(), width=420),\n` +
        `    mo.md(${pyMd(caption)}),\n` +
        `])`;
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
        // The upload box's live preview reads mo.ui.file.value, which marimo
        // does NOT serialise — reopen the keepsake and the student's own
        // hand-worked page is gone, replaced by "your photo appears here".
        // So the saved file gets its own cell after all. The two do not
        // disagree after a redo: this cell is EDITED on every nb_view_image
        // call, so the preview shows what is in the box and this shows the
        // page the tutor actually read and graded.
        `        if ${py(viewCell)} in _names:\n` +
        `            ctx.edit_cell(${py(viewCell)}, ${py(cellBody)})\n` +
        `            ctx.run_cell(${py(viewCell)})\n` +
        focusCellCode(`ctx.cells[${py(viewCell)}].id`, "            ") +
        `        else:\n` +
        `            ctx.create_cell(${py(cellBody)}, name=${py(viewCell)}, hide_code=True)\n` +
        `            ctx.run_cell(${py(viewCell)})\n` +
        focusCellCode(`ctx.cells[${py(viewCell)}].id`, "            ") +
        `    print("B64:" + _b64.b64encode(_out.getvalue()).decode())\n`;
      const result = await runKernel(code, signal);
      if (result.failed) return toResult(result);
      if (result.out.includes("NO_IMAGE")) {
        return toResult({
          out:
            result.out +
            `\nThe drop box is EMPTY — they pressed Send before the photo attached, so ` +
            `they are waiting on you and do not know why. Say so warmly in one line ` +
            `("the box came through empty — drop the photo in and press send again"), ` +
            `then end your turn. Never answer this one with silence: they just pressed ` +
            `a button and a quiet screen reads as broken.`,
          failed: false,
        });
      }
      const b64 = /^B64:([A-Za-z0-9+/=]+)\s*$/m.exec(result.out)?.[1];
      const fileLine = /^FILE:.*$/m.exec(result.out)?.[0] ?? "";
      // A photo actually reached the tutor for this widget — the one piece
      // of evidence checkpoint_done can use to tell "asked for the page" from
      // "never mentioned it".
      if (widget) viewedPhotos.add(widget);
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
  //
  // HARD RULE — these lines are shown at random, so any one of them can land
  // while any checkpoint is open. NOTHING here may state a fact this module
  // asks the student to find: no hop count for Milgram or Facebook (cp1),
  // no "put the cable across the ring" (cp4), no friendship/triangle counts
  // (cp3, cp5), no "clustering stays while distance collapses" mechanism
  // (cp6), and no "high clustering AND short paths" definition (cp5_tension,
  // cp7). Context and history are fine; answers are not.
  const TRIVIA = [
    "Euler invented network theory in 1736 to settle a stroll — the 7 bridges of Königsberg.",
    "Two of Königsberg's seven bridges were lost in 1944, and the puzzle's answer changed with them.",
    "Frigyes Karinthy dreamed up the question behind this whole module in a 1929 short story, 'Chains'.",
    "Stanley Milgram ran his letter experiment out of Harvard in the 1960s, with paper and stamps.",
    "In 2003 a team reran Milgram's experiment by email: 24,163 chains, 18 targets, 166 countries.",
    "Your friends have more friends than you do, on average — the friendship paradox.",
    "Watts & Strogatz published their network model in Nature in 1998; it has been cited over 50,000 times.",
    "The original three networks studied in 1998: film actors, the US power grid, and a worm's brain.",
    "The C. elegans worm's entire nervous system is mapped — all 302 neurons of it.",
    "Zachary's karate club split in two in 1977 — and became network science's favorite dataset.",
    "Find the karate-club split at a network conference and you can win an actual trophy.",
    "Erdős number: your coauthor distance to Paul Erdős, who has number 0 and 500-odd coauthors.",
    "Erdős number + Bacon number = the Erdős–Bacon number. Natalie Portman has one.",
    "Kevin Bacon isn't Hollywood's center — hundreds of actors are better connected.",
    "Granovetter, 1973: people find jobs through acquaintances, not close friends. Weak ties win.",
    "Triadic closure: your friend's friend tends to become your friend. That's where triangles come from.",
    "Leonhard Euler wrote roughly 850 papers — and kept publishing after going blind.",
    "The web, citation networks, and Hollywood all share one shape: a few superstar hubs.",
    "Hub networks shrug off random failures — but fall fast to targeted attacks on hubs.",
    "Dunbar's number: human brains manage roughly 150 stable relationships.",
    "PageRank is network centrality: where an endlessly clicking web surfer ends up.",
    "You personally know about 0.000002% of the people alive today.",
    "The word 'graph' for a network comes from Sylvester, 1878 — borrowed from chemistry diagrams.",
    "Moreno drew the first social network by hand in 1933; the New York Times covered it.",
    "Network scientists call a network's own map of itself a 'sociogram' — Moreno's word, still in use.",
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
