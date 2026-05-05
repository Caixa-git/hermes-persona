# Gateway Path Verification — Persona & Anima

> **2026-05-05** — Verified that `--skill persona` and `--skill anima` work identically on the gateway (main chat agent) and kanban workers.

## The Question

Does the gateway agent (Discord chat) correctly load persona and anima skills, given that:
- The SKILL.md files reference kanban-specific tools (`kanban_heartbeat`, `kanban_show`, agency-agents fetch)
- KANBAN_GUIDANCE is a kanban-worker-only system prompt section
- SOUL.md sits at Layer 1, persona/anima at Layer 13

## What Was Checked

| Check | Finding |
|:------|:--------|
| `run_agent.py:4916` — KANBAN_GUIDANCE injection gate | `if "kanban_show" in self.valid_tool_names:` — gateway has no kanban tools → KANBAN_GUIDANCE **never injected** into gateway sessions |
| `prompt_builder.py:1129` — SOUL.md path resolution | `get_hermes_home() / "SOUL.md"` — for gateway: `~/.hermes/SOUL.md`; for profile worker: `~/.hermes/profiles/<name>/SOUL.md`. Persona/anima don't depend on SOUL.md content. |
| Persona SKILL.md kanban-specific instructions | `kanban_heartbeat`, `kanban_create` calls in SKILL.md are **advisory context** — the LLM reads them and adapts. Gateway doesn't crash or fail; it just can't execute those specific steps, which is benign. |
| Anima SKILL.md profile fetch | `curl` to hermes-anima repo works from any context (gateway or worker) |
| Live `~/.hermes/skills/` path | Persona SKILL.md at `~/.hermes/skills/persona/SKILL.md`, Anima at `~/.hermes/skills/anima/SKILL.md` — both paths resolve identically regardless of caller |

## Conclusion

> **No path issue exists.** Both `--skill persona` and `--skill anima` work identically on gateway and kanban workers. The skills are loaded as Layer 13 user message text regardless of context. Kanban-specific instructions in the SKILL.md are advisory and don't cause errors on the gateway.

## Active Pitfall

After updating `~/hermes-rebirth/bootstrap/skills/` (dev), sync to `~/.hermes/skills/` (live). Verify with `diff`.
