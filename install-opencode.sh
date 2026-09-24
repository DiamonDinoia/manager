#!/usr/bin/env bash
# Symlink the manager skill, /manager command shim and tier agents into opencode.
# opencode auto-loads skills from ~/.claude/skills, so one link serves all harnesses.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p ~/.claude/skills ~/.codex/skills ~/.config/opencode/commands ~/.config/opencode/agents

ln -sfn "$ROOT/skills/manager" ~/.claude/skills/manager
ln -sfn "$ROOT/skills/manager" ~/.codex/skills/manager
ln -sfn "$ROOT/.opencode/command/manager.md" ~/.config/opencode/commands/manager.md
for tier in intern junior senior principal; do
  ln -sfn "$ROOT/.opencode/agents/$tier.md" ~/.config/opencode/agents/"$tier.md"
done

echo "linked; restart opencode (and claude/codex) to pick the skill up"
