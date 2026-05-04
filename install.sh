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

# Detect Hermes installation and check KANBAN_GUIDANCE
HERMES_PB=""
if python3 -c "import agent.prompt_builder" 2>/dev/null; then
    HERMES_PB=$(python3 -c "import agent.prompt_builder, os; print(os.path.dirname(agent.prompt_builder.__file__) + '/prompt_builder.py')" 2>/dev/null || true)
fi
if [ -z "$HERMES_PB" ] && python3 -c "import hermes_cli" 2>/dev/null; then
    # Try to find prompt_builder in the Hermes source path
    HERMES_PB=$(find "$(python3 -c "import sys; paths=[p for p in sys.path if 'hermes' in p.lower()]; print(paths[0] if paths else '')")" -name "prompt_builder.py" 2>/dev/null | head -1 || true)
fi

if [ -n "$HERMES_PB" ] && [ -f "$HERMES_PB" ]; then
    if grep -q '## persona — role adoption' "$HERMES_PB" 2>/dev/null; then
        echo "   ✅ KANBAN_GUIDANCE already has persona section."
    else
        echo ""
        echo "   ⚠️  KANBAN_GUIDANCE needs a persona section."
        echo "      Edit: ${HERMES_PB}"
        echo "      Add a '## persona — role adoption' section right before"
        echo "      TOOL_USE_ENFORCEMENT_GUIDANCE. See the hermes-persona repo README."
        echo ""
    fi
else
    echo "   ℹ️  Hermes source not found. KANBAN_GUIDANCE patch skipped."
    echo "      Install Hermes Agent first: curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
fi

echo ""
echo "🎭 Installation complete!"
echo ""
echo "Usage:"
echo "  hermes kanban create 'Build a REST API' --skill persona"
echo "  → Worker fetches agency-agents/README.md from GitHub raw"
echo "  → Picks the best-fitting role"
echo "  → Loads that role's full .md specification"
echo "  → Becomes that expert for the task"
echo ""
echo "Repo: https://github.com/msitarzewski/agency-agents"
echo "Docs: https://github.com/Caixa-git/hermes-persona"
