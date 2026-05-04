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

# Create persona skill directory
mkdir -p "$PERSONA_DIR"

# Write SKILL.md
cat > "$SKILL_FILE" << 'SKILL'
---
name: persona
description: "🎭 Automatic persona system — kanban workers analyze tasks and pick the best of 172 expert roles"
---

# 🎭 persona — role adoption system

This skill does not need to be loaded manually. When Hermes Persona is installed, every kanban worker automatically:

1. Analyzes its task
2. Fetches the agency-agents catalog (GitHub raw)
3. Picks the best-fitting role
4. Announces via kanban_heartbeat
5. Loads the role's .md specification
6. Works as that specialist

If no matching role exists, the worker proceeds as a generalist.

## Reference URLs

- Catalog: https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md
- Role file: https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md

## Project repo

https://github.com/Caixa-git/hermes-persona
SKILL

echo "   ✅ persona skill created at ${SKILL_FILE}"

# Patch KANBAN_GUIDANCE — already done in prompt_builder.py
echo "   ✅ KANBAN_GUIDANCE patched (persona section is now built-in)"
echo ""
echo "🎭 Installation complete!"
echo ""
echo "From now on, every kanban worker will automatically"
echo "pick the best-fitting expert persona for its task."
echo ""
echo "No additional setup or flags needed."
