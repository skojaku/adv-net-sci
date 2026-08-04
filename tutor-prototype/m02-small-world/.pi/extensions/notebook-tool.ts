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
import { uuidv7 } from "@earendil-works/pi-ai";
import { complete } from "@earendil-works/pi-ai/compat";
import { Container, Text } from "@earendil-works/pi-tui";
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

function chapterScriptMessage(ch: Chapter, num: number, total: number): string {
  const src = fs.readFileSync(path.join(process.cwd(), "lesson", ch.file), "utf-8");
  const last = ch.checkpoints[ch.checkpoints.length - 1];
  return (
    `CHAPTER SCRIPT ${num}/${total} — "${ch.title}" (invisible to the student). ` +
    `This is your curriculum right now:\n\n${src}\n\n` +
    `Work its checkpoints in order. After logging the final checkpoint (${last}), ` +
    `call chapter_done with short handoff notes.`
  );
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
          // deliverAs "followUp" is load-bearing: the default ("steer")
          // waits for the NEXT llm call, which never comes if the turn
          // already ended — the event then sat queued until the student
          // pressed Enter, hijacking their input (seen in production).
          pi.sendMessage(
            {
              customType: "notebook-done-button",
              content:
                `The student clicked the ✅ Done button in the notebook ` +
                `(checkpoint: ${checkpoint}). Read the relevant notebook values ` +
                `now with nb_read and continue the lesson. If the student also ` +
                `typed a message, respond to both together.`,
              display: true,
            },
            { deliverAs: "followUp", triggerTurn: true },
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
        if (cps.length > 0) {
          const order = chapters.flatMap((c) => c.checkpoints);
          const lastId = cps[cps.length - 1].id;
          const nextId = order[order.indexOf(lastId) + 1] ?? order[order.length - 1];
          chapter = chapters.find((c) => c.checkpoints.includes(nextId)) ?? chapter;
          pi.sendMessage(
            {
              customType: "resume-brief",
              content:
                `RESUME CONTEXT (invisible to the student — never mention this message): ` +
                `a previous session exists. Progress so far:\n${progressBrief(entries)}\n` +
                `FIRST, greet the student and ask with ask_student: continue where you left ` +
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
      if (!next) {
        return {
          content: [
            {
              type: "text" as const,
              text:
                "That was the FINAL chapter. Run the Ending protocol now: write " +
                "session_artifacts/session_summary.md via nb_run (per checkpoint: judgment, " +
                "hints used, one verbatim quote), then tell the student plainly what they can " +
                "now do, and that their answers — not code — are what gets reviewed.",
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

  // ── ask_student ───────────────────────────────────────────────────────────
  // Fixed-choice questions get an interactive picker (arrow keys + enter) —
  // friendlier than asking a beginner to type an option verbatim.
  pi.registerTool({
    name: "ask_student",
    label: "Ask (choices)",
    description:
      "Ask the student a multiple-choice question with an interactive picker. Use for ANY " +
      "question with fixed options (predictions, comfort level, continue-or-fresh). The " +
      "chosen option comes back as the tool result. Open-ended questions: just ask in plain text. " +
      "WARNING: the picker takes over the keyboard — if you just asked a typed question " +
      "(a name, a guess), the student loses their chance to answer it. Never call this " +
      "while a typed question is unanswered; wait for their reply first.",
    promptSnippet: "Ask the student a fixed-choice question (interactive picker)",
    parameters: Type.Object({
      question: Type.String({ description: "Short spoken question (max 2 sentences)." }),
      options: Type.Array(Type.String(), { description: "2-6 short options." }),
    }),
    async execute(_id, params, _signal, _onUpdate, ctx: any) {
      const q = String(params.question ?? "").trim();
      const opts = (Array.isArray(params.options) ? params.options : []).map((o: any) =>
        String(o),
      );
      if (!ctx?.ui?.select || opts.length < 2) {
        return {
          content: [
            { type: "text" as const, text: "(no interactive picker available — ask in plain text instead)" },
          ],
          details: { unavailable: true },
        };
      }
      const choice = await ctx.ui.select(q, opts);
      if (choice == null) {
        return {
          content: [
            {
              type: "text" as const,
              text: "(the student dismissed the picker — ask in plain text, they may want to answer in their own words)",
            },
          ],
          details: { dismissed: true, question: q },
        };
      }
      return {
        content: [{ type: "text" as const, text: `Student chose: ${choice}` }],
        details: { question: q, choice: String(choice) },
      };
    },
    renderShell: "self",
    renderCall(args: any, _theme: any) {
      const q = typeof args?.question === "string" ? args.question : "";
      return q ? new Text(q, 0, 0) : new Container();
    },
    renderResult(result: any, { isPartial }: any, theme: any) {
      if (isPartial) return new Container();
      const choice = result?.details?.choice;
      if (typeof choice === "string" && choice.length > 0) {
        return new Text(theme.fg("accent", `→ ${choice}`), 0, 0);
      }
      return new Container();
    },
  });

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
      const result = await runKernel(code, signal);
      if (!result.failed && describe) {
        result.out =
          `Inserted. The student now sees: ${describe}\n` +
          `(Describe it to the student ONLY from this line — never guess counts or details.)\n` +
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
      "notebook. Call ONLY after the student chose to start fresh (ask_student).",
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
        const sig = path.join(dir, "student_signal.txt");
        if (fs.existsSync(sig)) fs.writeFileSync(sig, "");
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
      const code =
        `import marimo._code_mode as cm\n` +
        `async with cm.get_context() as ctx:\n` +
        `    for _c in list(ctx.cells):\n` +
        `        if _c.name and _c.name != "_":\n` +
        `            ctx.delete_cell(_c.id)\n`;
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
      const viewRel = `session_artifacts/${base}_view.jpg`;
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
        `_P("session_artifacts").mkdir(exist_ok=True)\n` +
        `_raw = None\n` +
        source +
        `if _raw is not None:\n` +
        `    from PIL import Image as _Image, ImageOps as _ImageOps\n` +
        `    _ext = _P(_name).suffix.lower() or ".png"\n` +
        `    (_P("session_artifacts") / (${py(base + "_upload")} + _ext)).write_bytes(_raw)\n` +
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
        `    print("B64:" + _b64.b64encode(_out.getvalue()).decode())\n`;
      const result = await runKernel(code, signal);
      if (result.failed) return toResult(result);
      if (result.out.includes("NO_IMAGE")) {
        return toResult({
          out:
            result.out +
            `\nAsk the student to upload their photo in the notebook first (then the ` +
            `Done button), or to describe the drawing in words here.`,
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
      return toResult(await runKernel(params.code, signal));
    },
    ...quietRender,
  });
}
