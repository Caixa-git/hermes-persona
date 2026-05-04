---
name: persona
description: "🎭 Reference for the persona role adoption system — automatically activated for all kanban workers via KANBAN_GUIDANCE"
---

# 🎭 persona — role adoption (reference)

This skill is **no longer required** via `--skill persona`.

The persona role adoption system is now **built into KANBAN_GUIDANCE** — every kanban worker automatically:

1. Reads the task with `kanban_show()`
2. Fetches the agency-agents README from GitHub raw
3. Picks the best-fitting role
4. Announces adoption with `kanban_heartbeat(note="🎭 Role adopted: 🏗️ Backend Architect")`
5. Loads the role's .md specification
6. Acts as that specialist

If no matching role exists, the worker proceeds as a generalist.

## Why this works

The role adoption logic lives **directly in the Hermes Agent source** (`agent/prompt_builder.py`), inside `KANBAN_GUIDANCE`. Every spawned worker reads it.

The agency-agents repository is accessed **on demand via GitHub raw URL** — no local clone needed.

## Reference URLs

- Catalog: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`
- Role .md: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`

## Project repo

https://github.com/Caixa-git/hermes-persona
