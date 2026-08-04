/**
 * Student-friendly notebook tool for the tutoring session.
 *
 * Wraps the marimo-pair skill's execute-code.sh in a custom pi tool so the
 * terminal shows a single friendly status line ("📝 Setting up your first
 * question…") instead of raw bash heredocs and kernel output. The LLM still
 * receives the full execution output; only the on-screen rendering is quiet.
 * Students can expand a row (app.tools.expand) to see the details.
 */
import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { Type } from "typebox";
import { Text } from "@earendil-works/pi-tui";
import { keyHint, type ExtensionAPI } from "@earendil-works/pi-coding-agent";

const SCRIPT_CANDIDATES = [
  ".pi/skills/marimo-pair/scripts/execute-code.sh",
  ".claude/skills/marimo-pair/scripts/execute-code.sh",
];

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "notebook",
    label: "Notebook",
    description:
      "Run Python in the live marimo notebook session. Use this for ALL notebook work: " +
      "creating/editing/running cells (via `import marimo._code_mode as cm` and " +
      "`async with cm.get_context() as ctx:`), reading student widget values " +
      "(`print(cp2_dist.value)`), and testing code in the scratchpad. " +
      "The `status` field is displayed to the student while the tool runs.",
    promptSnippet: "Run Python in the live marimo notebook (scratchpad + cm code-mode)",
    promptGuidelines: [
      "Use notebook for ALL marimo work — never invoke the marimo-pair scripts through bash; raw commands scare non-technical students.",
      "notebook's `status` is shown to the student: a short, warm phrase in plain words (e.g. 'Setting up your first question…'). Never mention cells, code, APIs, or errors in a status.",
    ],
    parameters: Type.Object({
      status: Type.String({
        description:
          "Short student-facing status in plain, friendly words, e.g. 'Preparing our next step…'. No technical terms.",
      }),
      code: Type.String({
        description: "Python code to execute in the marimo scratchpad.",
      }),
    }),

    async execute(_toolCallId, params, signal) {
      const cwd = process.cwd();
      const script = SCRIPT_CANDIDATES.map((p) => path.join(cwd, p)).find(existsSync);
      if (!script) {
        return {
          content: [
            {
              type: "text",
              text: "NOTEBOOK ERROR: marimo-pair skill scripts not found. Ask the student to restart with ./run_tutor.sh.",
            },
          ],
          details: { failed: true },
        };
      }
      const url = process.env.MARIMO_URL || "http://127.0.0.1:2718";

      const { out, failed } = await new Promise<{ out: string; failed: boolean }>((resolve) => {
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
        child.stdin?.write(params.code);
        child.stdin?.end();
      });

      return {
        content: [
          {
            type: "text",
            text: failed ? `NOTEBOOK ERROR:\n${out || "(no output)"}` : out || "(no output)",
          },
        ],
        details: { failed },
      };
    },

    renderCall(args, theme) {
      const status =
        typeof args?.status === "string" && args.status.length > 0
          ? args.status
          : "Working in the notebook…";
      return new Text(theme.fg("accent", `📝 ${status}`), 0, 0);
    },

    renderResult(result, { expanded, isPartial }, theme) {
      if (isPartial) return new Text(theme.fg("muted", "…"), 0, 0);
      const failed = (result as { details?: { failed?: boolean } })?.details?.failed === true;
      const raw =
        (result as { content?: Array<{ type: string; text?: string }> })?.content
          ?.filter((c) => c.type === "text")
          .map((c) => c.text ?? "")
          .join("\n")
          .trim() ?? "";

      if (failed) {
        // Errors stay visible: the tutor is instructed to fix them silently,
        // but hiding a hard failure from the terminal would be worse.
        return new Text(theme.fg("error", "⚠ something hiccuped — your tutor is on it"), 0, 0);
      }
      if (expanded && raw) {
        return new Text(theme.fg("success", "✓") + "\n" + theme.fg("dim", raw), 0, 0);
      }
      let line = theme.fg("success", "✓");
      if (raw) line += " " + theme.fg("dim", `(${keyHint("app.tools.expand", "for details")})`);
      return new Text(line, 0, 0);
    },
  });
}
