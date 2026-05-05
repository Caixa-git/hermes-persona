# Prompt Layering Architecture — Hermes Agent System Prompt Priority

**Source:** `run_agent.py:_build_system_prompt()` (`~4869`), `agent/prompt_builder.py`, `hermes_cli/kanban_db.py` (`~2631`), `hermes_constants.py` (`~14`), `hermes_cli/profiles.py` (`~219`)
**Date:** 2026-05-05 (corrected)
**Purpose:** Document the exact order and mechanism of system prompt assembly for both normal sessions and kanban workers.

## Two SOUL.md contexts

`load_soul_md()` (prompt_builder.py:1034) reads from `get_hermes_home() / "SOUL.md"`.
`get_hermes_home()` (hermes_constants.py:14) returns the `HERMES_HOME` env var, or `~/.hermes`.

Crucially, when `hermes -p <profile>` activates a profile, `HERMES_HOME` is set to
`~/.hermes/profiles/<profile>/` (profiles.py:219-223). This means:

| Profile active | `HERMES_HOME` | SOUL.md loaded by `load_soul_md()` | Used by |
|---------------|---------------|-------------------------------------|---------|
| No (gateway, default) | `~/.hermes/` | `~/.hermes/SOUL.md` | Gateway/orchestrator agent |
| `-p persona-worker` | `~/.hermes/profiles/persona-worker/` | `~/.hermes/profiles/persona-worker/SOUL.md` | Kanban worker |

**Main `~/.hermes/SOUL.md`** = the gateway/orchestrator agent's identity.
**Profile `~/.hermes/profiles/<name>/SOUL.md`** = the kanban worker's identity (when spawned via `-p`).

## Base Agent (normal `hermes chat` session)

`_build_system_prompt()` assembles the prompt in this exact order:

| Layer | Source | Code Location | Condition |
|-------|--------|---------------|-----------|
| **1. Identity** | `load_soul_md()` → `$HERMES_HOME/SOUL.md` or `DEFAULT_AGENT_IDENTITY` | `run_agent.py:4890-4898`, `prompt_builder.py:1034-1059` | SOUL.md exists + has content → use it; else hardcoded "You are Hermes Agent..." |
| **2. Hermes help guidance** | `HERMES_AGENT_HELP_GUIDANCE` | `prompt_builder.py:150` | Always included |
| **3. Tool guidance** | `MEMORY_GUIDANCE`, `SESSION_SEARCH_GUIDANCE`, `SKILLS_GUIDANCE`, `KANBAN_GUIDANCE` | `run_agent.py:4904-4918` | Per-tool: only when tool is in `valid_tool_names` |
| **4. Tool-use enforcement** | `TOOL_USE_ENFORCEMENT_GUIDANCE`, `GOOGLE_MODEL_OPERATIONAL_GUIDANCE`, `OPENAI_MODEL_EXECUTION_GUIDANCE` | `run_agent.py:4930-4954` | Model-dependent: gpt/codex/gemini get extra discipline |
| **5. User system message** | Passed by caller (gateway, cron, etc.) | `run_agent.py:4960-4961` | `system_message is not None` |
| **6. Persistent memory** | MemPalace / built-in memory store | `run_agent.py:4963-4972` | `_memory_enabled` or `_user_profile_enabled` |
| **7. External memory** | Plugin-based memory providers | `run_agent.py:4975-4981` | `_memory_manager` not None |
| **8. Skills manifest** | `build_skills_system_prompt()` | `run_agent.py:4983-4999` | Skill tools enabled (`skills_list`/`skill_view`/`skill_manage`) |
| **9. Context files** | `.hermes.md` > `AGENTS.md` > `CLAUDE.md` > `.cursorrules` | `run_agent.py:5001-5010` | `skip_context_files=False`; skips SOUL.md when already loaded as identity |
| **10. Timestamp + model info** | System clock + config | `run_agent.py:5012-5021` | Always |
| **11. Environment hints** | `build_environment_hints()` | `run_agent.py:5037-5039` | WSL/Termux detection |
| **12. Platform hints** | `PLATFORM_HINTS` dict | `run_agent.py:5041-5050` | Platform key matches (discord/telegram/slack/etc.) |

## Kanban Worker — spawn mechanism

The dispatcher spawns a worker as a subprocess (kanban_db.py:2631):

```python
cmd = [
    "hermes",
    "-p", profile_arg,              # e.g. "persona-worker" → HERMES_HOME = ~/.hermes/profiles/persona-worker/
    "--skills", "kanban-worker",    # always loaded (mandatory lifecycle reference)
    # + per-task .skills from kanban_create (e.g. --skills persona)
    "chat",
    "-q", "work kanban task {task.id}",
]
```

The worker is an independent Hermes Agent process. `_build_system_prompt()` runs identically,
but with a different `HERMES_HOME` (profile path) and different tools enabled.

### How SOUL.md resolves for kanban workers

1. `-p persona-worker` → `HERMES_HOME` = `~/.hermes/profiles/persona-worker/`
2. `load_soul_md()` → `~/.hermes/profiles/persona-worker/SOUL.md` → **Layer 1 Identity**
3. If profile SOUL.md is empty/missing → `DEFAULT_AGENT_IDENTITY` fallback

This means **the kanban worker's Layer 1 identity comes from the PROFILE's SOUL.md**,
not from the main `~/.hermes/SOUL.md`. The two are independent.

### How --skills are injected (CLI level, not system prompt)

The `--skills` flag is processed by the CLI layer (`cli.py` / `hermes_cli/`), NOT by
`_build_system_prompt()`. Skills are loaded as **user messages** (not system prompt parts):

- `agent/skill_commands.py` reads `~/.hermes/skills/<name>/SKILL.md` for each `--skills <name>` flag
- Content is injected as a user message into the conversation history
- This preserves prefix caching (system prompt stays immutable)
- But it means skills content has lower priority than ALL system prompt layers

### KANBAN_GUIDANCE current state

`KANBAN_GUIDANCE` (prompt_builder.py:191-247) contains:

```
- Kanban task execution protocol (Lifecycle: orient → work → heartbeat → block → complete)
- Orchestrator mode (decomposition via kanban_create)
- Do NOTs (no shell out to kanban CLI, no delegate_task substitute)
```

**If the hermes-persona Step 6 has been run**, the tuple also contains a `"## persona — role adoption"` section (see "KANBAN_GUIDANCE persona patch" below).

It is injected into Layer 3 (Tool guidance) only when `"kanban_show" in valid_tool_names`
(run_agent.py:4915-4916), which is the case for kanban workers.

### KANBAN_GUIDANCE identity section (hermes-persona + hermes-anima, unified)

**As of May 5, 2026**, the KANBAN_GUIDANCE has a single unified `## identity — persona & anima (Layer 13)` section covering both persona (role) and anima (core nature) adoption.

The unified section is NOT produced by any patch script — it was applied via direct file edit. The original `patch-kanban-guidance.py` script still produces the old two-section format (`## persona` + `## anima`). The unified version must be reapplied if overwritten.

The unified section adds:

```
## identity — persona & anima (Layer 13)

CRITICAL — Priority Rules:
  Anima (nature) > Persona (role)
  Both at Layer 13 — same proximity, different authority

Step 0: Injection awareness
Step 1: Analyze task
Step 2: Pick a role (agency-agents, 4 research principles)
Step 3: Extract domain from role path
Step 4: Fetch anima profile (hermes-anima repo)
Step 5: Announce both (🎭 Role + 🧠 Anima)
Step 6: Load role specification
Step 7: Adopt both — nature prevails on conflict
Step 8: Act
Step 9: Persist identity to SOUL.md
Available anima domains: 15 divisions
```

**Key changes from the original persona-only section:**
- `## persona` and `## anima` were TWO separate sections → now ONE `## identity` section
- Step 3 (domain extraction) was added between role selection and adoption
- Step 4 fetches anima profile from `hermes-anima` repo
- Step 5 announces both persona AND anima
- Step 7 explicitly states "nature prevails on conflict"
- Priority rules are now at the top of the section (social framing)
- Layer 13 same-proximity explanation was added

**Verification:**
```bash
grep -c "## identity" ~/.hermes/hermes-agent/agent/prompt_builder.py
# Expected: 1 (unified)
# If 0: needs reapplication (git checkout may have reverted it)
```

**Two separate projects, one unified section:**
| Project | Github | Responsibility |
|---------|--------|---------------|
| hermes-persona | Caixa-git/hermes-persona | Role adoption (agency-agents 172 roles) |
| hermes-anima | Caixa-git/hermes-anima | Core nature (15 OCEAN-backed profiles) |
| KANBAN_GUIDANCE | (patched in hermes-agent) | Unified identity section combining both |

### Post-spawn injection limits

After a worker spawns and `_build_system_prompt()` has cached the system prompt,
the highest layer available for injecting persona content is the **user message**
layer (where `--skills` content and tool results land). System prompt layers (1-12)
are immutable for the session's duration.

Two escape hatches exist, both limited:

1. **`_invalidate_system_prompt()`** (run_agent.py:5417) — invalidates the cache,
   forcing a rebuild on the next API call. Called automatically by context compression
   events. If SOUL.md was modified mid-session, the rebuild picks up the new content.
   **Not externally triggerable** by the worker (private method).

2. **`ephemeral_system_prompt`** (run_agent.py:914) — appended to the cached system
   prompt at API-call time. Set at AIAgent construction; **not modifiable after spawn**.

**Practical implication:** "Persist identity to SOUL.md" after role adoption only
affects the *next* spawn, not the current session. The current session's identity is
already frozen at Layer 1 by the time the worker runs.

### Summary: kanban worker prompt layers

| Layer | Source | What it provides |
|-------|--------|-----------------|
| **1. Identity** | Profile SOUL.md (`~/.hermes/profiles/<name>/SOUL.md`) | The worker's core identity |
| **2-12** | Same as base agent (above) | Standard Hermes Agent system prompt |
| **--skills** | CLI-injected user messages | Persona SKILL.md, kanban-worker SKILL.md, etc. (lower priority) |
| **kanban_show()** | First tool call result | Task context: title, body, parent handoffs, comments |

## Distinction from older docs

Earlier versions of this document (and the persona SKILL.md's Three-layer model) described
SOUL.md as "the gateway agent's personality only." This was correct for the **main**
`~/.hermes/SOUL.md`, but **profile-specific** SOUL.md files exist and are the Identity
source for kanban workers.

Correct model:
- `~/.hermes/SOUL.md` — gateway agent identity (runs without `-p`)
- `~/.hermes/profiles/<name>/SOUL.md` — worker identity (runs with `-p <name>`)
- Both feed through the same `load_soul_md()` code path
- KANBAN_GUIDANCE adds lifecycle rules but currently zero persona content

## Key Code Paths

```python
# run_agent.py:4869
def _build_system_prompt(self, system_message: str = None) -> str:
    # 1. Identity: load_soul_md() → $HERMES_HOME/SOUL.md or DEFAULT_AGENT_IDENTITY
    # 2. Hermes help guidance
    # 3. Tool-specific guidance (MEMORY, SESSION_SEARCH, SKILLS, KANBAN)
    # 4. Tool-use enforcement (model-dependent)
    # 5. User system message
    # 6. Persistent memory + user profile
    # 7. External memory plugin
    # 8. Skills manifest (via build_skills_system_prompt)
    # 9. Context files (.hermes.md > AGENTS.md > CLAUDE.md > .cursorrules)
    # 10. Timestamp, model, provider
    # 11. Environment hints
    # 12. Platform hints

# kanban_db.py:2631 — worker spawn
cmd = ["hermes", "-p", profile_arg, "--skills", "kanban-worker", "chat", "-q", ...]
# → -p sets HERMES_HOME → load_soul_md() reads profile/SOUL.md

# profiles.py:219-223 — profile → HERMES_HOME resolution
def get_profile_dir(name):
    return _get_profiles_root() / normalize_profile_name(name)
# → HERMES_HOME = ~/.hermes/profiles/persona-worker/
```

### Runtime rebuild note

After spawn, neither SOUL.md (Layer 1) nor any system prompt layer can be modified externally. However:

**Context compression** (`_compress_context` at run_agent.py:9079) calls `_invalidate_system_prompt()` then `_build_system_prompt(system_message)` — this **re-reads SOUL.md from disk** and rebuilds the full system prompt (run_agent.py:9142-9144). So if the worker writes to `$HERMES_HOME/SOUL.md` during a session, the new identity takes effect on the **next compression event** (~50% context window threshold by default).

There is NO tool or mechanism to manually trigger `_invalidate_system_prompt()` from inside a worker session. The kanban-adopt-role tool concept remains unimplemented.

## Priority Summary

```
Highest priority:   Profile SOUL.md / DEFAULT_AGENT_IDENTITY (Layer 1)
                    ↓
                    Tool-use enforcement (Layer 4)
                    ↓
                    User system message (Layer 5)
                    ↓
                    Persistent memory (Layer 6)
                    ↓
                    Skills manifest (Layer 8)
                    ↓
                    KANBAN_GUIDANCE (Layer 3, but lifecycle only)
                    ↓
                    --skills injected as user messages (CLI level)
                    ↓
Lowest priority:    Platform hints (Layer 12)
```

Later layers don't override earlier ones—they accumulate. The model sees the entire
assembled prompt. Priority matters when instructions **contradict**: earlier layers
(identity, enforcement) carry more weight than later layers (platform hints, skills).
