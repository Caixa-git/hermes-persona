#!/usr/bin/env bash
set -euo pipefail

# 🎭 persona — Hermes Agent role adoption system
# Installs the persona skill so kanban workers can adopt specialist roles
# from the agency-agents repository (nicepkg/agency-agents)
#
# Usage: bash install.sh
#        curl -sSL https://raw.githubusercontent.com/nicepkg/agency-agents/main/... | bash

PERSONA_DIR="${HOME}/.hermes/skills/persona"
SKILL_FILE="${PERSONA_DIR}/SKILL.md"
HERMES_SOURCE=""

echo "🎭 Installing persona skill for Hermes Agent..."

# 1. Find Hermes source for KANBAN_GUIDANCE
if python3 -c "import hermes_cli.kanban_db" 2>/dev/null; then
    HERMES_SOURCE=$(python3 -c "import hermes_cli.prompt_builder; import os; print(os.path.dirname(hermes_cli.prompt_builder.__file__))" 2>/dev/null || true)
fi
if [ -z "$HERMES_SOURCE" ]; then
    HERMES_SOURCE=$(python3 -c "import agent.prompt_builder; import os; print(os.path.dirname(agent.prompt_builder.__file__))" 2>/dev/null || true)
fi

# 2. Create persona skill directory
mkdir -p "$PERSONA_DIR"

# 3. Write SKILL.md
cat > "$SKILL_FILE" << 'SKILL'
---
name: persona
description: "🎭 210+ 전문가 페르소나 — GitHub raw에서 README 스캔 후 적합 역할 .md 로드"
---

# 🎭 persona

## How to adopt a specialist role

1. **Read the catalog**
   ```
   curl -s https://raw.githubusercontent.com/nicepkg/agency-agents/main/README.md
   ```
   → 17 categories, 210+ expert roles

2. **Pick your role**
   Analyze your task. Choose the best-fitting role from the catalog.

3. **Load the personality**
   Construct the raw URL and fetch the role's full specification:
   ```
   curl -s https://raw.githubusercontent.com/nicepkg/agency-agents/main/{category}/{filename}.md
   ```
   Examples:
   - `engineering/engineering-backend-architect.md`
   - `design/design-ui-designer.md`
   - `testing/testing-qa-engineer.md`
   - `project-management/project-management-pmo.md`
   - `game-development/game-development-game-designer.md`
   - `academic/academic-research-scientist.md`
   - `finance/finance-financial-analyst.md`
   - `marketing/marketing-brand-strategist.md`
   - `sales/sales-sales-engineer.md`
   - `support/support-technical-support.md`
   - `product/product-product-manager.md`
   - `specialized/{slug}.md`
   - `strategy/{slug}.md`
   - `spatial-computing/spatial-computing-{slug}.md`
   - `paid-media/paid-media-{slug}.md`

4. **Become that expert**
   Follow its rules, standards, philosophy, and process faithfully.
   Embody the role completely for the duration of this task.

5. **Act**
   Execute your task as that specialist.

---

🎭 *Pick your mask. Become the expert.*
SKILL

echo "   ✅ persona skill created at ${SKILL_FILE}"

# 4. Patch KANBAN_GUIDANCE in Hermes source (if found)
if [ -n "$HERMES_SOURCE" ]; then
    PB_FILE="${HERMES_SOURCE}/prompt_builder.py"
    # Fallback: search for prompt_builder.py
    if [ ! -f "$PB_FILE" ]; then
        PB_FILE=$(find "$(python3 -c "import sys; print(next(p for p in sys.path if 'site-packages' in p))" 2>/dev/null)" -name "prompt_builder.py" -path "*hermes*" 2>/dev/null | head -1 || true)
    fi
    if [ -f "$PB_FILE" ] && grep -q 'hermes-persona' "$PB_FILE" 2>/dev/null; then
        echo "   ⚠️  KANBAN_GUIDANCE references old 'hermes-persona' — please update manually or reinstall Hermes."
    fi
    if [ -f "$PB_FILE" ] && grep -q '## persona — role adoption' "$PB_FILE" 2>/dev/null; then
        echo "   ✅ KANBAN_GUIDANCE already has persona section."
    elif [ -f "$PB_FILE" ]; then
        echo "   ⚠️  KANBAN_GUIDANCE needs manual patch: add '## persona — role adoption' section."
        echo "      Edit: ${PB_FILE}"
        echo "      See:  https://hermes-agent.nousresearch.com/docs/persona"
    fi
else
    echo "   ⚠️  Hermes source not found. Install Hermes first, then run this script again."
fi

echo ""
echo "🎭 Installation complete!"
echo ""
echo "Usage:"
echo "  hermes kanban create 'Build a REST API' --skill persona"
echo "  → Worker reads agency-agents/README.md, picks Backend Architect, loads its .md"
echo "  → Becomes that expert for the task"
