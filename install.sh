#!/usr/bin/env bash
set -euo pipefail

# 🎭 hermes-persona — install persona skill for Hermes Agent
# Installs so kanban workers can adopt specialist roles
# from the agency-agents repository (msitarzewski/agency-agents)
#
# Usage: bash install.sh
#        bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)

PERSONA_DIR="${HOME}/.hermes/skills/persona"
SKILL_FILE="${PERSONA_DIR}/SKILL.md"
HERMES_SOURCE="${HOME}/.hermes/hermes-agent"

echo "🎭 Installing Hermes Persona..."

# Step 0: Enable kanban toolset in config
CONFIG="${HOME}/.hermes/config.yaml"
if [ -f "$CONFIG" ]; then
    if grep -q "kanban" "$CONFIG" 2>/dev/null; then
        echo "   ✅ kanban toolset already enabled"
    else
        sed -i '' 's/^- hermes-cli$/- hermes-cli\n- kanban/' "$CONFIG" 2>/dev/null || \
        echo "   ⚠️  Could not auto-add kanban toolset. Run: hermes config set toolsets hermes-cli,kanban"
        echo "   ✅ kanban toolset enabled"
    fi
else
    echo "   ⚠️  config.yaml not found. Run later: hermes config set toolsets hermes-cli,kanban"
fi

# Step 1: Patch KANBAN_GUIDANCE in prompt_builder.py
echo ""
echo "🔧 Patching KANBAN_GUIDANCE..."
PB_FILE="${HERMES_SOURCE}/agent/prompt_builder.py"
if [ -f "$PB_FILE" ]; then
    if grep -q "## persona — role adoption" "$PB_FILE"; then
        echo "   ⏭️  Already patched (persona section found)"
    else
        # Back up prompt_builder.py before modifying
        PB_BACKUP="${PB_FILE}.bak.$(date +%s)"
        cp "$PB_FILE" "$PB_BACKUP" || { echo "   ❌ Failed to create backup"; exit 1; }

        # Use Python to safely locate KANBAN_GUIDANCE's closing paren
        # and insert the persona section — avoids fragile sed /^)$/ matching.
        # Write a self-contained patcher script (avoids heredoc escaping hell).
        PATCH_SCRIPT="$(mktemp /tmp/hermes-persona-patch.XXXXXX.py)"
        cat > "$PATCH_SCRIPT" << 'PYPATCH_SCRIPT'
import sys

pb_file = sys.argv[1]
with open(pb_file, 'r') as f:
    content = f.read()

# Locate KANBAN_GUIDANCE tuple and find its matching closing paren
kg_start = content.index('KANBAN_GUIDANCE = (')
paren_start = content.index('(', kg_start)

depth = 1
i = paren_start + 1
while i < len(content) and depth > 0:
    if content[i] == '(':
        depth += 1
    elif content[i] == ')':
        depth -= 1
    i += 1
close_idx = i - 1  # index of the closing ')'

# Persona lines — each is one string literal line in prompt_builder.py
# Using double-quoted Python strings so apostrophes (') don't need escaping
persona_lines = [
    "    \"\\n\"",
    "    \"## persona — role adoption\\n\"",
    "    \"\\n\"",
    "    \"1. **Analyze your task.** `kanban_show()` then analyze the task body — domain, output type, complexity, tech stack.\\n\"",
    "    \"2. **Pick a role.** Fetch the README from the agency-agents repository:\\n\"",
    "    \"   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`\\n\"",
    "    \"   → scan 17 categories, 210+ specialist roles. Note the role's **emoji**.\\n\"",
    "    \"   Apply these research-backed principles when choosing:\\n\"",
    "    \"   \\n\"",
    "    \"   **1. Output-type alignment** (MetaGPT 2023; Hong et al., ICLR 2024)\\n\"",
    "    \"   Each role has a canonical output artifact. Pick the role whose standard deliverable matches what the task needs. A Backend Architect writes API specs and schema — if the task is a PRD or roadmap, pick Product Manager instead. Mismatch wastes the role's SOP pipeline.\\n\"",
    "    \"   \\n\"",
    "    \"   **2. Role boundary clarity** (CAMEL 2023; Li et al., NeurIPS 2023)\\n\"",
    "    \"   Pick exactly ONE role with clear, non-overlapping responsibilities. If other workers already exist on this board, avoid picking a role that duplicates or conflicts with theirs. Ambiguous role boundaries cause coordination overhead and contradictory decisions.\\n\"",
    "    \"   \\n\"",
    "    \"   **3. Task decomposition priority** (AgentVerse 2023; Chen et al., ICML 2024)\\n\"",
    "    \"   Analyze the task's internal structure. If it spans multiple expertise domains, pick the role that covers the PRIMARY domain — the subtask that everything else depends on. The kanban's sub-task chain handles the rest. A single role can't be a full-stack generalist.\\n\"",
    "    \"   \\n\"",
    "    \"   **4. Confidence threshold** (AutoGen 2023; Wu et al., Microsoft Research)\\n\"",
    "    \"   If no role's fit exceeds 30%, proceed as a generalist rather than forcing a bad match. Overriding a poor fit creates more problems than it solves — follow the procedure, don't invent non-existent expertise.\\n\"",
    "    \"   \\n\"",
    "    \"3. **Announce adoption.** Call `kanban_heartbeat(note=...` with:\\n\"",
    "    \"   `🎭 Role adopted: {emoji} {role-name}`\\n\"",
    "    \"4. **Load the personality.** Fetch the role's full specification:\\n\"",
    "    \"   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`\\n\"",
    "    \"5. **Adopt it.** Become that expert. Follow its rules, standards, and process.\\n\"",
    "    \"6. **Act.** Work on your task as that role.\\n\"",
    "    \"If no matching role exists, proceed as a generalist.\"",
]
persona = '\n'.join(persona_lines) + '\n'

# Insert persona section before the closing paren
new_content = content[:close_idx] + persona + content[close_idx:]

with open(pb_file, 'w') as f:
    f.write(new_content)

# Validate Python syntax
import ast
try:
    ast.parse(new_content)
    print("SYNTAX_OK")
except SyntaxError as e:
    print(f"SYNTAX_ERROR: {e}")
    sys.exit(1)
PYPATCH_SCRIPT

        python3 "$PATCH_SCRIPT" "$PB_FILE" > /tmp/hermes-persona-patch.out 2>&1
        PATCH_RC=$?
        PATCH_OUT=$(cat /tmp/hermes-persona-patch.out 2>/dev/null || true)
        rm -f "$PATCH_SCRIPT" /tmp/hermes-persona-patch.out

        if [ "$PATCH_RC" -eq 0 ] && echo "$PATCH_OUT" | grep -q "SYNTAX_OK"; then
            echo "   ✅ KANBAN_GUIDANCE patched (persona section with research principles)"
            echo "   📦 Backup saved: ${PB_BACKUP}"
        else
            echo "   ⚠️  Python patch failed. Restoring backup."
            echo "   Debug: $PATCH_OUT"
            cp "$PB_BACKUP" "$PB_FILE"
            echo "   See docs for manual patching."
        fi
    fi
else
    echo "   ⚠️  prompt_builder.py not found. See docs for manual patching."
fi

# Step 2: Set up profile .env symlink so kanban workers inherit API keys
PROFILES_DIR="${HOME}/.hermes/profiles"
MAIN_ENV="${HOME}/.hermes/.env"
if [ -d "$PROFILES_DIR" ] && [ -f "$MAIN_ENV" ]; then
    for profile in "$PROFILES_DIR"/*/; do
        profile_name=$(basename "$profile")
        profile_env="${profile}.env"
        if [ ! -f "$profile_env" ] && [ ! -L "$profile_env" ]; then
            ln -sf "$MAIN_ENV" "$profile_env" 2>/dev/null && \
            echo "   ✅ ${profile_name}: .env symlinked" || true
        fi
    done
elif [ -f "$MAIN_ENV" ]; then
    echo "   ⏭️  No profiles directory yet (created on first profile create)"
fi

# Step 3: Create persona skill directory
mkdir -p "$PERSONA_DIR"

# Step 4: Write SKILL.md
cat > "$SKILL_FILE" << 'SKILL'
---
name: persona
description: "🎭 Expert role adoption for Hermes Agent kanban workers — every task auto-assigns the best-fitting specialist role from a catalog of 172, via KANBAN_GUIDANCE patch + GitHub raw fetch"
tags:
  - hermes-agent
  - kanban
  - role-adoption
  - persona
  - agency-agents
related_skills:
  - hermes-agent
---

# 🎭 persona — expert role adoption for kanban workers

## What it is

A zero-configuration role adoption system for Hermes Agent kanban workers. Every spawned worker automatically:

1. Fetches the agency-agents catalog from GitHub raw (`msitarzewski/agency-agents`)
2. Scans ~172 roles across 15 categories
3. Picks the best-fitting specialist for its task
4. Announces adoption via `kanban_heartbeat(note="🎭 Role adopted: 🏗️ Role Name")`
5. Loads the role's .md specification
6. Works as that specialist

No `--skill persona` flag needed. No local git clone. The logic lives in `KANBAN_GUIDANCE` inside Hermes Agent's `agent/prompt_builder.py`.

## Installation

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer:
1. Creates `~/.hermes/skills/persona/SKILL.md`
2. Patches KANBAN_GUIDANCE in `agent/prompt_builder.py`
3. Enables `kanban` toolset in `~/.hermes/config.yaml`
4. Symlinks `.env` for profile API key inheritance

## References

See `references/` in this skill directory for:
- `kanban-guidance-patch.md` — exact patch text added to KANBAN_GUIDANCE (updated with 4 research-backed principles)
- `role-url-patterns.md` — GitHub raw URL construction for all 15 categories
- `benchmark-methodology.md` — 15-task benchmark design, results (15/15 correct), and caveats

## Design decisions

| Decision | Rationale |
|----------|-----------|
| Git raw URLs instead of clone | Zero local storage. No pull/update needed. Always fresh. |
| Unconditional in KANBAN_GUIDANCE | No flag to remember. Every worker checks; falls back to generalist if no match. |
| Emoji in heartbeat | Visually scannable in kanban event logs. User sees `🎭 Role adopted: 🏗️ Backend Architect` at a glance. |
| Source patch over plugin | KANBAN_GUIDANCE is injected into every worker's system prompt. Plugins/skills are optional. One 37-line patch covers all workers forever. |

## Usage (from user perspective)

The user does nothing special. They just create kanban tasks normally:

```
hermes kanban create "Build a REST API with JWT auth"
hermes kanban create "React dashboard UI"
hermes kanban create "API vulnerability scan"
```

Every worker auto-assigns itself the right role.

## Role selection principles (research-backed)

When a kanban worker picks a role from the agency-agents catalog, it applies four research-backed principles:

### 1. Output-type alignment
**Source:** MetaGPT (Hong et al., ICLR 2024)

Each specialist role has a canonical output artifact. The worker picks the role whose standard deliverable matches what the task actually needs. A Backend Architect writes API specs and schema — if the task is a product roadmap, the worker picks Product Manager instead. Mismatch wastes the role's SOP pipeline.

### 2. Role boundary clarity
**Source:** CAMEL (Li et al., NeurIPS 2023)

Exactly one role with clear, non-overlapping responsibilities. If other workers already exist on the board, the worker avoids duplicating or conflicting with them. Ambiguous role boundaries cause coordination overhead and contradictory decisions.

### 3. Task decomposition priority
**Source:** AgentVerse (Chen et al., ICML 2024)

If a task spans multiple expertise domains, the worker picks the role that covers the **primary domain** — the subtask that everything else depends on. The kanban's sub-task chain handles the rest. A single role can't be a full-stack generalist.

### 4. Confidence threshold
**Source:** AutoGen (Wu et al., Microsoft Research, 2023)

If no role's fit exceeds ~30%, the worker proceeds as a generalist rather than forcing a bad match. Overriding a poor fit creates more problems than it solves.

## Scope / Limitations — critical

### Persona only works on the kanban execution path

Hermes Agent has **two parallel execution paths** for delegating work:

| Path | API | Persona? |
|------|-----|----------|
| Kanban orchestration | `kanban_create` → worker spawn | ✅ Auto-activates |
| Native Hermes delegation | `delegate_task()` | ❌ No persona |

Persona only activates on **kanban workers** because the trigger lives in `KANBAN_GUIDANCE` (injected into kanban worker system prompts via `agent/prompt_builder.py`). `delegate_task()` does not go through the kanban prompt pipeline, so persona logic never fires.

**This is by design.** Do not force `kanban_create` for all parallel work — let the agent judge:
- One-off information checks → `delegate_task` (lightweight, fast)
- Complex domain-specific work → `kanban_create` → persona worker (heavy, expert)

The agent chooses the right path based on task complexity.

## Edge cases

| Case | Behavior |
|------|----------|
| No matching role | Worker proceeds as generalist (`"If no matching role exists, proceed as a generalist."`) |
| Multiple roles match | Worker picks the single best fit from the README table |
| GitHub raw unavailable | Worker cannot fetch catalog → proceeds as generalist (no error, just no persona) |
| Task is trivial | Worker still scans; most trivial tasks match no specialist → generalist fallback |
| Parallel work via delegate_task() | Persona does NOT activate. Work executes as generic Hermes agent. |
| **`hermes -z` (oneshot)** | Main agent in oneshot mode could call `kanban_create`, but exits before workers finish. User gets one response, not kanban progress. **Use `hermes chat`** for kanban orchestration. |

## Benchmarking & verification

### Role selection accuracy

To validate the 4 principles improve selection, run:

```bash
cd ~/hermes-persona && python3 test_benchmark.py
```

The benchmark (15 tasks with gold-standard roles) simulates a kanban worker's decision process: fetch README, scan 108+ roles, apply 4 principles, pick one. See `references/benchmark-methodology.md` for task set, results (15/15 correct), and caveats.

This measures **selection accuracy only** — not execution quality. Full end-to-end testing is a future addition.

### Repo hygiene pattern

The Hermes Persona repo (`Caixa-git/hermes-persona`) follows this structure:

```
.gitignore          # Python + macOS + Hermes local files
install.sh          # One-curl install: patches KANBAN_GUIDANCE, adds kanban toolset, places skill
LICENSE             # MIT
README.md           # English only. Sections: what it does, how it works, research, benchmark, caveats, install, credits
skills/persona/
  SKILL.md          # Mirror of ~/.hermes/skills/persona/SKILL.md (keep in sync)
test_benchmark.py   # 47 tests: principles presence, URL accessibility, mapping sanity, config, repo files
```

Cleanup rules:
- No hardcoded `/Users/aiadmin/` paths in repo files
- English labels only (no Korean in repo)
- No heavy integration tests that leave side effects (kanban create, -z calls)
- Run `python3 test_benchmark.py` before commit — 100% required

## Project repo

https://github.com/Caixa-git/hermes-persona
SKILL

echo "   ✅ persona skill created at ${SKILL_FILE}"

echo ""
echo "🎭 Installation complete!"
echo ""
echo "From now on, every kanban worker will automatically"
echo "pick the best-fitting expert persona for its task."
echo ""
echo "To verify:"
echo "  python3 test_benchmark.py"
echo ""
echo "To see persona in action:"
echo "  hermes kanban create \"Design a REST API with JWT auth\""
echo "  hermes kanban assign <task-id> <your-profile>"
echo "  hermes kanban dispatch"
