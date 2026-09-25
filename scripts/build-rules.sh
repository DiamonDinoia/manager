#!/usr/bin/env bash
# Generate the rule-only harness files from skills/manager/SKILL.md.
# The skill body is the single source of truth; run this after editing it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$ROOT/skills/manager/SKILL.md"

body="$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$SKILL")"

gate="Apply this role only when the user invokes it: \`/manager\`, \"act as manager\",
\"orchestrate this\". It stays inactive otherwise. Where the harness has no subagent
mechanism, act as the cheapest tier that can do the job instead of dispatching."

plain="$gate

$body"

write() {
  mkdir -p "$(dirname "$1")"
  printf '%s\n' "$2" > "$1"
}

write "$ROOT/.clinerules/manager.md"  "$plain"
write "$ROOT/.windsurf/rules/manager.md" "$plain"
write "$ROOT/.qoder/rules/manager.md"    "$plain"
write "$ROOT/.agents/rules/manager.md"   "$plain"
write "$ROOT/AGENTS.md"                  "$plain"

write "$ROOT/.cursor/rules/manager.mdc" "---
description: Manager orchestrator mode. Pins down a checkable spec, dispatches work to tiered subagents, keeps its own context small. Applies only when the user invokes it.
globs:
alwaysApply: true
---

$plain"

write "$ROOT/.kiro/steering/manager.md" "---
title: Manager orchestrator mode
inclusion: always
---

$plain"

# OpenClaw / ClawHub: same body, short one-line description, homepage + license.
write "$ROOT/.openclaw/skills/manager/SKILL.md" "---
name: manager
description: \"Manager orchestrator: pins down a checkable spec, dispatches work to tiered subagents, keeps its own context small.\"
homepage: https://github.com/DiamonDinoia/skill-orchestration
license: MIT
---
$body"

echo "built rule copies from $SKILL"
