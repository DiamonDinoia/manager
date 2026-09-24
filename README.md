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

Claude Code and Codex (both read Claude marketplaces):

```
/plugin marketplace add DiamonDinoia/manager
/plugin install manager@manager
```

opencode:

```
git clone https://github.com/DiamonDinoia/manager ~/repos/manager
~/repos/manager/install-opencode.sh
```

Restart the harness after installing. `/manager <task>` starts the role;
"stop manager" ends it.
