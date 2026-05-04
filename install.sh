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

echo "🎭 Installing persona skill for Hermes Agent..."

# Create persona skill directory
mkdir -p "$PERSONA_DIR"

# Write SKILL.md
cat > "$SKILL_FILE" << 'SKILL'
---
name: persona
description: "🎭 210+ expert roles — scan agency-agents catalog via GitHub raw, pick the best fit, load full .md specification"
---

# 🎭 persona — role adoption

Load this skill when you need to adopt a specialist role from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog (172 roles across 15 categories).

## How to adopt

1. **Analyze your task.** Read with `kanban_show()`. Identify the domain, activity type (build/audit/research/manage), output, and scope.

2. **Read the catalog.** Fetch the full README from GitHub raw:
   ```
   curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md
   ```
   → 17 categories, 210+ specialist roles with use-case tables.
   Each role has an emoji. Note it.

3. **Pick your role.** Choose the best-fitting specialist. Note its **emoji** from the table.

4. **Announce adoption.** Immediately call:
   ```
   kanban_heartbeat(note="🎭 Role adopted: {emoji} {role-name}")
   ```

5. **Load the personality.** Fetch the role's full .md specification:
   ```
   curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md
   ```

6. **Adopt it.** Follow its rules, standards, philosophy, and process faithfully. Embody the role completely.

7. **Act.** Execute your task as that specialist.

---

🎭 *Pick your mask. Become the expert.*
SKILL

echo "   ✅ persona skill created at ${SKILL_FILE}"

# Patch KANBAN_GUIDANCE — already done in prompt_builder.py
echo "   ✅ KANBAN_GUIDANCE patched (persona section is now built-in)"
echo ""
echo "🎭 Installation complete!"
echo ""
echo "All kanban workers will now automatically:"
echo "  1. Analyze their task"
echo "  2. Fetch agency-agents catalog from GitHub raw"
echo "  3. Pick the best-fitting specialist role"
echo "  4. Announce via kanban_heartbeat (🎭 Role adopted: 🏗️ Role Name)"
echo "  5. Load the role's .md and act as that expert"
echo ""
echo "No --skill persona flag needed. Just create tasks normally:"
echo "  hermes kanban create 'Build a REST API'"
echo ""
echo "Repo: https://github.com/msitarzewski/agency-agents"
echo "Docs: https://github.com/Caixa-git/hermes-persona"
