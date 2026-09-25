#!/usr/bin/env bash
# Symlink the five orchestration skills, the /manager command shim and the tier
# agents into opencode. Writes only opencode's own directories: claude and codex
# get these skills from the plugin marketplace instead (no duplicate installs).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p ~/.config/opencode/skills ~/.config/opencode/commands ~/.config/opencode/agents

for skill in manager team brainstorm spec parallel; do
  ln -sfn "$ROOT/skills/$skill" ~/.config/opencode/skills/"$skill"
done
ln -sfn "$ROOT/.opencode/command/manager.md" ~/.config/opencode/commands/manager.md
for tier in intern junior senior principal; do
  ln -sfn "$ROOT/.opencode/agents/$tier.md" ~/.config/opencode/agents/"$tier.md"
done

echo "linked; restart opencode to pick the skills up"
