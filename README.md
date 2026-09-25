# manager

A persistent manager role for agent harnesses: it pins down a checkable spec with
the user, dispatches every unit of work to subagents by difficulty tier, and keeps
its own context small under a hard budget.

## Tiers

The skill names a tier, never a model. Each harness maps tiers to its own models.

| Tier | Takes |
|------|-------|
| `intern` | Mechanical: grep, filters, boilerplate, one-line checks |
| `junior` | Well-specified implementation |
| `senior` | Implementation with judgment calls; code review (default) |
| `principal` | Numerics, SIMD, concurrency, performance, unclosed debugging, open-ended design |

## Context budget

Subagent reports cap at 30 lines; evidence over 10 lines goes to a file and returns
a path; diffs and logs travel as path plus counts; follow-ups resume the producing
agent's session; dispatches batch per round-trip.

## Install

| Harness | Install |
|---------|---------|
| Claude Code | `/plugin marketplace add DiamonDinoia/manager` then `/plugin install manager@manager` |
| Codex | same as Claude Code (Codex reads Claude marketplaces) |
| opencode | `git clone https://github.com/DiamonDinoia/manager ~/repos/manager && ~/repos/manager/install-opencode.sh` |
| Gemini CLI | `gemini extensions install https://github.com/DiamonDinoia/manager` |
| Cursor | copy `.cursor/rules/manager.mdc` into the project's `.cursor/rules/` |
| Windsurf | copy `.windsurf/rules/manager.md` into the project's `.windsurf/rules/` |
| Cline | copy `.clinerules/manager.md` into the project's `.clinerules/` |
| Kiro | copy `.kiro/steering/manager.md` into the project's `.kiro/steering/` |
| Qoder | install via the Qoder plugin flow from this repo (`./.qoder-plugin/`) |
| Amp / `AGENTS.md` harnesses | point the harness at this repo's `AGENTS.md`, or use `./.agents/` |
| Devin | `./.devin-plugin/` |
| Grok | `./.grok-plugin/` |

Restart the harness after installing. `/manager <task>` starts the role;
"stop manager" ends it.

Harnesses with real subagents (Claude Code, Codex, opencode) dispatch to the four
tier agents. Rule-only harnesses get a self-gated rule: it activates on `/manager`
and acts as the cheapest tier itself instead of dispatching. Not yet covered:
OpenClaw, pi.

