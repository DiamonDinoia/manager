import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

let cachedInstructions = null;

export function managerInstructions() {
  if (cachedInstructions !== null) return cachedInstructions;
  const src = readFileSync(join(ROOT, "skills", "manager", "SKILL.md"), "utf8");
  const fm = src.match(/^---\n[\s\S]*?\n---\n?/);
  cachedInstructions = (fm ? src.slice(fm[0].length) : src).trim();
  return cachedInstructions;
}

export default function managerExtension(pi) {
  let active = false;

  pi.registerCommand("manager", {
    description: "Start the persistent manager role: /manager [task]",
    handler: (args, ctx) => {
      active = true;
      ctx?.ui?.notify?.('Manager active. "stop manager" ends it.', "info");
      const task = String(args || "").trim();
      if (task) pi.sendUserMessage(task);
    },
  });

  pi.on("input", async (event) => {
    if (event?.source === "extension") return;
    if (/^\s*stop manager\s*$/i.test(String(event?.text || ""))) {
      active = false;
    }
  });

  pi.on("before_agent_start", async (event) => {
    if (!active) return;
    const base = event?.systemPrompt ? `${event.systemPrompt}\n\n` : "";
    return { systemPrompt: `${base}${managerInstructions()}` };
  });
}
