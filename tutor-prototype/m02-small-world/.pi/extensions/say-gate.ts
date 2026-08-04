/**
 * Say gate — every tutor utterance passes checks; tempo comes first.
 *
 * The tutor must speak through the `say` tool (enforced by AGENTS.md).
 * Mechanical rules (length, sentence count, one question) are checked
 * locally with zero latency and block delivery. The LLM reviewer (iron
 * rules: never state what the student hasn't produced, etc.) runs in the
 * BACKGROUND by default — messages display instantly, and a violation
 * becomes an invisible coach note before the next turn. Set
 * TUTOR_REVIEW_MODE=strict to block on the reviewer (slow), or =off to
 * disable the LLM review entirely.
 *
 * Fail-open by design: if the reviewer is unreachable, the message is
 * delivered (a tutoring session must not die on a gate). Every verdict is
 * appended to session_artifacts/reviewer_log.jsonl for the instructor.
 *
 * Config (env): TUTOR_REVIEW_URL   (default https://api.deepseek.com/chat/completions)
 *               TUTOR_REVIEW_MODEL (default deepseek-v4-flash)
 *               TUTOR_REVIEW_KEY   (default $DEEPSEEK_API_KEY)
 */
import * as fs from "node:fs";
import path from "node:path";
import { Type } from "typebox";
import { Text } from "@earendil-works/pi-tui";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const REVIEW_URL = process.env.TUTOR_REVIEW_URL || "https://api.deepseek.com/chat/completions";
const REVIEW_MODEL = process.env.TUTOR_REVIEW_MODEL || "deepseek-v4-flash";
const REVIEW_KEY = process.env.TUTOR_REVIEW_KEY || process.env.DEEPSEEK_API_KEY || "";
/**
 * Review mode — blocking review killed the conversational tempo, so the
 * default is now non-blocking:
 *   "async"  (default) deliver instantly; LLM review runs in the background
 *            and violations become an invisible coach note before the next turn
 *   "strict" block until the reviewer approves (old behavior)
 *   "off"    no LLM review (instant local checks still apply)
 */
const REVIEW_MODE = process.env.TUTOR_REVIEW_MODE || "async";

/** 0-latency checks for the mechanical iron rules. */
function localCheck(draft: string): { ok: boolean; reason?: string } {
  if (draft.length > 450) return { ok: false, reason: "over 450 characters — speak in short breaths" };
  const sentences = draft.split(/[.!?…](?:\s|$)/).filter((s) => s.trim().length > 0).length;
  if (sentences > 3) return { ok: false, reason: `${sentences} sentences — max 3` };
  const questions = (draft.match(/\?/g) ?? []).length;
  if (questions > 2) return { ok: false, reason: "more than one question at a time" };
  return { ok: true };
}

const REVIEWER_PROMPT =
  "You review one outgoing message from a Socratic tutor to a beginner student. " +
  "Reject ONLY if a rule is clearly broken:\n" +
  "1. BREVITY: more than 3 sentences, or clearly not how a human speaks out loud.\n" +
  "2. REVEALING: it states a number, distance, sum, average, list of results, or a " +
  "conclusion that the student has not already said in the transcript. Asking for the " +
  "next small piece is always fine; confirming a piece the student just said is fine.\n" +
  "3. It asks more than one question.\n" +
  'Reply with ONLY JSON: {"approved": true} or {"approved": false, "reason": "<one short sentence naming the rule>"}';

const textOf = (raw: unknown): string =>
  typeof raw === "string"
    ? raw
    : (Array.isArray(raw) ? raw : [])
        .filter((c: any) => c?.type === "text")
        .map((c: any) => c.text ?? "")
        .join("\n");

export default function (pi: ExtensionAPI) {
  /** Rolling transcript so the reviewer can judge "already said by student". */
  const transcript: Array<{ role: string; text: string }> = [];
  const remember = (role: string, text: string) => {
    if (!text) return;
    transcript.push({ role, text });
    if (transcript.length > 14) transcript.shift();
  };
  let consecutiveRejections = 0;
  let strayTextNagged = false;

  // ── Runaway watchdog ──────────────────────────────────────────────────────
  // Flash-class models can fall into degenerate repetition loops in plain
  // text (seen in production: the same sentence streamed 50+ times). Abort
  // the generation as soon as plain text exceeds the budget, then restart
  // the turn with an invisible corrective instruction.
  const RUNAWAY_CHARS = 800;
  let runawayAborts = 0;
  let runawayFiredForThisMessage = false;
  pi.on("message_update", async (event: any, ctx: any) => {
    const msg = event?.message;
    if (msg?.role !== "assistant") return;
    if (runawayFiredForThisMessage) return;
    const t = textOf(msg.content);
    if (t.length <= RUNAWAY_CHARS) return;
    runawayFiredForThisMessage = true;
    runawayAborts++;
    try {
      ctx.abort();
    } catch {
      // abort unavailable — the message_end collapse still hides the text
    }
    if (runawayAborts <= 3) {
      pi.sendMessage(
        {
          customType: "say-gate-coach",
          content:
            "COACH (invisible to the student — never mention this): your plain-text output " +
            "ran away and was cut off. NEVER write plain text — reason with one short think " +
            "note, speak with say. Now continue the lesson exactly where you left off.",
          display: false,
        },
        { deliverAs: "followUp", triggerTurn: true },
      );
    }
  });

  pi.on("message_end", async (event: any) => {
    const msg = event?.message;
    if (!msg) return;
    runawayFiredForThisMessage = false;
    if (msg.role === "user") {
      remember("student", textOf(msg.content).trim());
      strayTextNagged = false;
      return;
    }
    if (msg.role !== "assistant") return;
    const t = textOf(msg.content).trim();
    if (!t) return;
    remember("tutor (private note)", t);
    // Plain assistant text is a wall of deliberation the student shouldn't
    // read (seen in production). Nag once per turn to use think()/say() …
    if (t.length > 150 && !strayTextNagged) {
      strayTextNagged = true;
      pi.sendMessage(
        {
          customType: "say-gate-coach",
          content:
            "COACH (invisible to the student — never mention this): you wrote a wall of plain " +
            "text; it was hidden from the student. Reason with the think tool (short notes), " +
            "speak with say. Keep plain text empty.",
          display: false,
        },
        { deliverAs: "nextTurn" },
      );
    }
    // … and strip the text entirely so the transcript shows nothing at all.
    // (An empty text block stands in when the message had no tool calls, so
    // provider serialization still sees valid content.)
    const kept = (Array.isArray(msg.content) ? msg.content : []).filter(
      (c: any) => c?.type !== "text",
    );
    return {
      message: {
        ...msg,
        content: kept.length > 0 ? kept : [{ type: "text", text: "" }],
      },
    };
  });

  // Sanctioned private-reasoning channel: renders as a single dim dot.
  pi.registerTool({
    name: "think",
    label: "Think",
    description:
      "Private reasoning scratchpad — the student never sees it. Use a SHORT note (1–3 " +
      "sentences) when you need to decide something, then act. Not for messages to the " +
      "student (use say).",
    promptSnippet: "Jot a private reasoning note (hidden from the student)",
    parameters: Type.Object({
      thought: Type.String({ description: "Your short private note." }),
    }),
    async execute(_id, _params) {
      return { content: [{ type: "text" as const, text: "ok" }], details: {} };
    },
    renderShell: "self",
    renderCall(_args: any, theme: any) {
      return new Text(theme.fg("dim", "·"), 0, 0);
    },
    renderResult(_result: any, _opts: any, _theme: any) {
      return new Text("", 0, 0);
    },
  });

  function logReview(entry: Record<string, unknown>) {
    try {
      const dir = path.join(process.cwd(), "session_artifacts");
      fs.mkdirSync(dir, { recursive: true });
      fs.appendFileSync(path.join(dir, "reviewer_log.jsonl"), JSON.stringify(entry) + "\n");
    } catch {
      // logging is best-effort
    }
  }

  async function review(
    draft: string,
    signal?: AbortSignal,
  ): Promise<{ approved: boolean; reason?: string; error?: string }> {
    if (!REVIEW_KEY) return { approved: true, error: "no reviewer api key" };
    const tail = transcript
      .slice(-8)
      .map((t) => `${t.role}: ${t.text}`)
      .join("\n");
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 20_000);
      signal?.addEventListener("abort", () => controller.abort());
      const res = await fetch(REVIEW_URL, {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${REVIEW_KEY}` },
        body: JSON.stringify({
          model: REVIEW_MODEL,
          temperature: 0,
          max_tokens: 120,
          messages: [
            { role: "system", content: REVIEWER_PROMPT },
            {
              role: "user",
              content:
                `Transcript (most recent last):\n${tail || "(session start)"}\n\n` +
                `Tutor's DRAFT message:\n${draft}`,
            },
          ],
        }),
        signal: controller.signal,
      });
      clearTimeout(timer);
      if (!res.ok) return { approved: true, error: `reviewer http ${res.status}` };
      const data: any = await res.json();
      const content = data?.choices?.[0]?.message?.content ?? "";
      const m = /\{[\s\S]*\}/.exec(content);
      if (!m) return { approved: true, error: "unparseable reviewer output" };
      const verdict = JSON.parse(m[0]);
      return { approved: verdict.approved !== false, reason: verdict.reason };
    } catch (e: any) {
      return { approved: true, error: String(e?.message ?? e) };
    }
  }

  pi.registerTool({
    name: "say",
    label: "Say to student",
    description:
      "The ONLY way to speak to the student. Write the message exactly as you want the " +
      "student to read it (max 3 short spoken sentences, one question). A reviewer checks it " +
      "first: if the result says NOT DELIVERED, the student saw nothing — rewrite following " +
      "the reason and call say again.",
    promptSnippet: "Speak to the student (reviewed before display)",
    promptGuidelines: [
      "ALL student-facing prose goes through say — keep your plain assistant text empty.",
      "If say returns NOT DELIVERED, rewrite (shorter, next small piece only) and call say again; never give up and never paste the draft as plain text.",
    ],
    parameters: Type.Object({
      message: Type.String({ description: "The message for the student, ready to display." }),
    }),
    async execute(_id, params, signal) {
      const draft = String(params.message ?? "").trim();

      // 1. Instant local check — no latency, catches the mechanical rules.
      const local = localCheck(draft);
      if (!local.ok && consecutiveRejections < 2) {
        consecutiveRejections++;
        logReview({ ts: new Date().toISOString(), draft, approved: false, reason: local.reason, mode: "local" });
        return {
          content: [
            {
              type: "text" as const,
              text: `NOT DELIVERED — ${local.reason}. Rewrite (shorter; only the next small piece) and call say again.`,
            },
          ],
          details: { approved: false },
        };
      }

      // 2. Strict mode: block until the reviewer approves (slow — opt-in).
      if (REVIEW_MODE === "strict") {
        const verdict = await review(draft, signal);
        logReview({ ts: new Date().toISOString(), draft, mode: "strict", ...verdict });
        if (!verdict.approved && consecutiveRejections < 2) {
          consecutiveRejections++;
          return {
            content: [
              {
                type: "text" as const,
                text:
                  `NOT DELIVERED — reviewer rejected: ${verdict.reason ?? "rule violation"}. ` +
                  `Rewrite (shorter; ask only for the next small piece; never state what the ` +
                  `student hasn't said) and call say again.`,
              },
            ],
            details: { approved: false },
          };
        }
      } else if (REVIEW_MODE !== "off" && REVIEW_KEY) {
        // 3. Async mode (default): deliver NOW, review in the background —
        // violations arrive as an invisible coach note before the next turn.
        void review(draft).then((verdict) => {
          logReview({ ts: new Date().toISOString(), draft, mode: "async", ...verdict });
          if (!verdict.approved) {
            pi.sendMessage(
              {
                customType: "say-gate-coach",
                content:
                  `COACH (invisible to the student — never mention this): the reviewer flagged ` +
                  `your last message: ${verdict.reason}. Tighten the next one — shorter, and ` +
                  `never state what the student hasn't said.`,
                display: false,
              },
              { deliverAs: "nextTurn" },
            );
          }
        });
      }

      consecutiveRejections = 0;
      remember("tutor", draft);
      return {
        content: [{ type: "text" as const, text: "Delivered." }],
        details: { approved: true, message: draft },
      };
    },
    // Self shell: no tool box / background — approved messages must read as
    // ordinary tutor speech, not as tool output.
    renderShell: "self",
    renderCall(_args: any, _theme: any) {
      // Draft args stream here — never show them; the student only sees the
      // approved message in renderResult.
      return new Text("", 0, 0);
    },
    renderResult(result: any, { isPartial }: any, theme: any) {
      if (isPartial) return new Text(theme.fg("muted", "…"), 0, 0);
      if (result?.details?.approved === true) {
        return new Text(String(result?.details?.message ?? ""), 0, 0);
      }
      // Rejected draft: a quiet pencil, nothing readable.
      return new Text(theme.fg("dim", "✎"), 0, 0);
    },
  });
}
