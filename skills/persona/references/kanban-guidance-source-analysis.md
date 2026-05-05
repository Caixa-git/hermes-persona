# KANBAN_GUIDANCE Source Analysis — Current State vs Intended Design

**Date:** 2026-05-05
**Source:** Conversation between user and Hermes Agent gateway, analyzing hermes-persona repo (commit `783f6a72`) and hermes-agent source (`run_agent.py`, `prompt_builder.py`, `kanban_db.py`)
**Purpose:** Document the gap between what the persona SKILL.md claims and what the source code actually does.

## Current State (source-verified)

### KANBAN_GUIDANCE (prompt_builder.py:191-247)

Contains ONLY:
- Kanban task execution protocol (6-step lifecycle: orient → work → heartbeat → block → complete → create)
- Orchestrator mode (decomposition via kanban_create)
- Do NOTs (no shell, no delegate_task substitute, no scope creep)

**Does NOT contain:**
- Persona/role adoption instructions
- Agency-agents references
- Research-backed principles (MetaGPT, CAMEL, AgentVerse, AutoGen)
- Any mention of fetching role files from GitHub

### install.sh (hermes-persona repo)

| Step | Action | Actual behavior |
|------|--------|----------------|
| 0 | Enable kanban toolset | `sed` on config.yaml — works |
| 1 | Injection protection check | `grep -q "_check_kanban_task_threats"` — READ ONLY, no modification |
| 2 | .env symlink | Interactive prompt per profile |
| 3 | Create persona/ dir | `mkdir -p` |
| 4 | Write SKILL.md | Heredoc creates `SKILL.md` at `~/.hermes/skills/persona/SKILL.md` |
| 5 | Create references | Creates `kanban-guidance-patch.md`, `role-url-patterns.md`, `benchmark-methodology.md` |

**install.sh does NOT patch KANBAN_GUIDANCE.** The `kanban-guidance-patch.md` reference document contains the exact Python string that SHOULD be inserted into `prompt_builder.py`, but install.sh never applies it. The install.sh is architecturally incomplete.

### Persona activation mechanism

Currently: `--skill persona` → loads SKILL.md as **user message** (not system prompt)
- This is lower priority than all system prompt layers
- Persona instructions can be lost in context compression
- Requires explicit `--skill persona` flag on every task

Intended (architecturally complete): KANBAN_GUIDANCE patch → persona instructions at **system prompt level**
- Every kanban worker sees persona logic unconditionally
- No --skill persona flag needed
- Higher priority (system prompt over user message)

### Worker spawn flow (kanban_db.py:2586-2691)

```python
cmd = ["hermes", "-p", profile_arg, "--skills", "kanban-worker"]
if task.skills:
    for sk in task.skills:
        if sk and sk != "kanban-worker":
            cmd.extend(["--skills", sk])
cmd.extend(["chat", "-q", f"work kanban task {task.id}"])
```

Key: `-p <profile>` → HERMES_HOME = `~/.hermes/profiles/<profile>/` → `load_soul_md()` reads profile-specific SOUL.md

### SOUL.md loading (prompt_builder.py:1034-1059)

```python
def load_soul_md() -> Optional[str]:
    soul_path = get_hermes_home() / "SOUL.md"
    # get_hermes_home() returns HERMES_HOME env var or ~/.hermes
    # When -p is active, HERMES_HOME → profile directory
```

**Profile SOUL.md locations:**

| Context | HERMES_HOME | SOUL.md read |
|---------|-------------|--------------|
| Gateway (no profile) | `~/.hermes` | `~/.hermes/SOUL.md` |
| persona-worker | `~/.hermes/profiles/persona-worker/` | `~/.hermes/profiles/persona-worker/SOUL.md` |
| coder | `~/.hermes/profiles/coder/` | `~/.hermes/profiles/coder/SOUL.md` |

## Three-Layer Architecture

```
LAYER 1: SOUL.md (~/.hermes/SOUL.md)
  → Gateway agent's own personality and tone
  → "Who the gateway IS" — e.g. 메카 위진수
  → Loaded every message; defines the orchestrator's voice

LAYER 2: persona SKILL.md + KANBAN_GUIDANCE (partially implemented)
  → Kanban worker's adopted role
  → "What the worker DOES" — e.g. Backend Architect
  → Currently: SKILL.md only (user message level via --skill persona)
  → Intended: KANBAN_GUIDANCE patch (system prompt level, unconditional)

LAYER 3: anima (planned)
  → Kanban worker's inner character
  → "What the worker IS LIKE" — OCEAN personality profile
  → Research direction only
```

## Key Gaps to Close

1. **install.sh should patch prompt_builder.py** — apply the persona section to KANBAN_GUIDANCE
2. **No `--role` flag on install.sh** — the `--role "Backend Architect"` mechanism does not exist and was not intended
3. **SOUL.md vs profile-SOUL.md confusion** — these are separate files and must be treated as such
4. **hermes-agent source vs hermes-persona source** — when working on hermes-persona, read the repo at `/tmp/hermes-persona/`, not `~/.hermes/hermes-agent/`

## Verification commands

```bash
# Check if KANBAN_GUIDANCE has persona content
grep -c "persona — role adoption" ~/.hermes/hermes-agent/agent/prompt_builder.py
# Expected (currently): 0
# Expected (after patch): 1

# Check install.sh completeness
grep -c "prompt_builder" ~/.hermes/hermes-persona/install.sh
# Should find the patch application step (added)
