---
name: persona
description: "🎭 Automatic persona system — kanban workers analyze tasks and pick the best of 172 expert roles"
---

# 🎭 persona — role adoption system

This skill does not need to be loaded manually. When Hermes Persona is installed, every kanban worker automatically:

1. Analyzes its task
2. Fetches the agency-agents catalog (GitHub raw)
3. Picks the best-fitting role
4. Announces via `kanban_heartbeat`
5. Loads the role's .md specification
6. Works as that specialist

If no matching role exists, the worker proceeds as a generalist.

## Reference URLs

- Catalog: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`
- Role file: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`

## Project repo

https://github.com/Caixa-git/hermes-persona
