|---
|name: persona
|description: "🎭 Expert role adoption for Hermes Agent kanban workers — every task auto-assigns the best-fitting specialist role from a catalog of 172, via KANBAN_GUIDANCE patch + GitHub raw fetch"
|tags:
|  - hermes-agent
|  - kanban
|  - role-adoption
|  - persona
|  - agency-agents
|related_skills:
|  - hermes-agent
|---
|
|# 🎭 persona — expert role adoption for kanban workers
|
|## What it is
|
|A zero-configuration role adoption system for Hermes Agent kanban workers. Every spawned worker automatically:
|
|1. Fetches the agency-agents catalog from GitHub raw (`msitarzewski/agency-agents`)
|2. Scans ~172 roles across 15 categories
|3. Picks the best-fitting specialist for its task
|4. Announces adoption via `kanban_heartbeat(note="🎭 Role adopted: 🏗️ Role Name")`
|5. Loads the role's .md specification
|6. Works as that specialist
|
|No `--skill persona` flag needed. No local git clone. The logic lives in `KANBAN_GUIDANCE` inside Hermes Agent's `agent/prompt_builder.py`.
|
|## Installation
|
|```bash
|bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
|```
|
|The installer:
|1. Creates `~/.hermes/skills/persona/SKILL.md`
|2. Patches KANBAN_GUIDANCE in `agent/prompt_builder.py`
|3. Enables `kanban` toolset in `~/.hermes/config.yaml`
|
|## References
|
|See `references/` in this skill directory for:
|- `kanban-guidance-patch.md` — exact patch text added to KANBAN_GUIDANCE (updated with 4 research-backed principles)
|- `role-url-patterns.md` — GitHub raw URL construction for all 15 categories
|- `benchmark-methodology.md` — 15-task benchmark design, results (15/15 correct), and caveats
|
|## Design decisions
|
|| Decision | Rationale |
||----------|-----------|
|| Git raw URLs instead of clone | Zero local storage. No pull/update needed. Always fresh. |
|| Unconditional in KANBAN_GUIDANCE | No flag to remember. Every worker checks; falls back to generalist if no match. |
|| Emoji in heartbeat | Visually scannable in kanban event logs. User sees `🎭 Role adopted: 🏗️ Backend Architect` at a glance. |
|| Source patch over plugin | KANBAN_GUIDANCE is injected into every worker's system prompt. Plugins/skills are optional. One 37-line patch covers all workers forever. |
|
|## Usage (from user perspective)
|
|The user does nothing special. They just create kanban tasks normally:
|
|```
|hermes kanban create "Build a REST API with JWT auth"
|hermes kanban create "React dashboard UI"
|hermes kanban create "API vulnerability scan"
|```
|
|Every worker auto-assigns itself the right role.
|
|## Role selection principles (research-backed)
|
|When a kanban worker picks a role from the agency-agents catalog, it applies four research-backed principles:
|
|### 1. Output-type alignment
|**Source:** MetaGPT (Hong et al., ICLR 2024)
|
|Each specialist role has a canonical output artifact. The worker picks the role whose standard deliverable matches what the task actually needs. A Backend Architect writes API specs and schema — if the task is a product roadmap, the worker picks Product Manager instead. Mismatch wastes the role's SOP pipeline.
|
|### 2. Role boundary clarity
|**Source:** CAMEL (Li et al., NeurIPS 2023)
|
|Exactly one role with clear, non-overlapping responsibilities. If other workers already exist on the board, the worker avoids duplicating or conflicting with them. Ambiguous role boundaries cause coordination overhead and contradictory decisions.
|
|### 3. Task decomposition priority
|**Source:** AgentVerse (Chen et al., ICML 2024)
|
|If a task spans multiple expertise domains, the worker picks the role that covers the **primary domain** — the subtask that everything else depends on. The kanban's sub-task chain handles the rest. A single role can't be a full-stack generalist.
|
|### 4. Confidence threshold
|**Source:** AutoGen (Wu et al., Microsoft Research, 2023)
|
|If no role's fit exceeds ~30%, the worker proceeds as a generalist rather than forcing a bad match. Overriding a poor fit creates more problems than it solves.
|
|## Scope / Limitations — critical
|
|### Persona only works on the kanban execution path
|
|Hermes Agent has **two parallel execution paths** for delegating work:
|
|| Path | API | Persona? |
||------|-----|----------|
|| Kanban orchestration | `kanban_create` → worker spawn | ✅ Auto-activates |
|| Native Hermes delegation | `delegate_task()` | ❌ No persona |
|
|Persona only activates on **kanban workers** because the trigger lives in `KANBAN_GUIDANCE` (injected into kanban worker system prompts via `agent/prompt_builder.py`). `delegate_task()` does not go through the kanban prompt pipeline, so persona logic never fires.
|
|**This is by design.** Do not force `kanban_create` for all parallel work — let the agent judge:
|- One-off information checks → `delegate_task` (lightweight, fast)
|- Complex domain-specific work → `kanban_create` → persona worker (heavy, expert)
|
|The agent chooses the right path based on task complexity.
|
|## Edge cases
|
|| Case | Behavior |
||------|----------|
|| No matching role | Worker proceeds as generalist (`"If no matching role exists, proceed as a generalist."`) |
|| Multiple roles match | Worker picks the single best fit from the README table |
|| GitHub raw unavailable | Worker cannot fetch catalog → proceeds as generalist (no error, just no persona) |
|| Task is trivial | Worker still scans; most trivial tasks match no specialist → generalist fallback |
|| Parallel work via delegate_task() | Persona does NOT activate. Work executes as generic Hermes agent. |
|| **`hermes -z` (oneshot)** | Main agent in oneshot mode could call `kanban_create`, but exits before workers finish. User gets one response, not kanban progress. **Use `hermes chat`** for kanban orchestration. |
|
|## Project repo
|
|https://github.com/Caixa-git/hermes-persona
