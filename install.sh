#!/usr/bin/env bash
# Hermes Persona Skill Installer
# 
# Usage:
#   bash install.sh              Install persona skill
#   bash install.sh --dry-run    Preview installation
#   bash install.sh --update     Update existing installation
#   bash install.sh --uninstall  Remove persona skill
#   bash install.sh --help       Show this help

set -euo pipefail

REPO="https://raw.githubusercontent.com/Caixa-git/hermes-persona/main"
DEST="${HOME}/.hermes/skills/persona"
ROLES_DEST="${HOME}/.hermes/skills/persona/roles/agency-agents"
AGENCY_REPO="https://github.com/msitarzewski/agency-agents"
AGENCY_SHA="783f6a72bfd7f3135700ac273c619d92821b419a"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ACTION="install"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) ACTION="dry-run"; shift ;;
    --update)  ACTION="update"; shift ;;
    --uninstall) ACTION="uninstall"; shift ;;
    -h|--help)
      echo "Hermes Persona Skill Installer"
      echo ""
      echo "Usage: bash install.sh [OPTION]"
      echo ""
      echo "Options:"
      echo "  --dry-run     Preview what would be installed"
      echo "  --update      Update existing installation"
      echo "  --uninstall   Remove persona skill"
      echo "  -h, --help    Show this help"
      echo ""
      echo "Without options, installs the persona skill to:"
      echo "  $DEST"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: bash install.sh [--dry-run|--update|--uninstall|--help]"
      exit 1
      ;;
  esac
done

# ── Uninstall ────────────────────────────────────────────────────────────
if [ "$ACTION" = "uninstall" ]; then
  echo "🗑️  Uninstalling persona skill..."
  if [ -f "$DEST/SKILL.md" ] || [ -d "$ROLES_DEST" ]; then
    rm -f "$DEST/SKILL.md"
    rm -rf "$ROLES_DEST"
    echo -e "${GREEN}✅${NC} Persona skill removed from $DEST"
  else
    echo -e "${YELLOW}⚠${NC} Persona skill not found at $DEST"
  fi
  exit 0
fi

# ── Dry-run ──────────────────────────────────────────────────────────────
if [ "$ACTION" = "dry-run" ]; then
  echo "🔍 Dry-run: would install persona skill"
  echo ""
  echo "  Files to create/update:"
  echo "    $DEST/SKILL.md                   ← hermes-persona/skills/persona/SKILL.md"
  echo "    $ROLES_DEST/                      ← git clone $AGENCY_REPO (SHA: ${AGENCY_SHA::8})"
  echo "    $ROLES_DEST/README.md"
  echo "    $ROLES_DEST/{category}/*.md       (172+ role files)"
  echo ""
  echo "  Destination: $DEST"
  echo "  Role catalog: $ROLES_DEST"
  echo "  Total size:   ~2MB (SKILL.md + role catalog)"
  exit 0
fi

# ── Update ───────────────────────────────────────────────────────────────
if [ "$ACTION" = "update" ]; then
  echo "🔄 Updating persona skill..."
  if [ ! -f "$DEST/SKILL.md" ]; then
    echo -e "${YELLOW}⚠${NC} No existing installation at $DEST — performing fresh install"
  fi
  # Fall through to install
fi

# ── Install ──────────────────────────────────────────────────────────────
echo "📦 Installing persona skill..."

mkdir -p "$DEST"

# 1. Fetch SKILL.md
echo -n "  Fetching SKILL.md... "
if curl -sSL "$REPO/skills/persona/SKILL.md" -o "$DEST/SKILL.md"; then
  echo -e "${GREEN}done${NC}"
else
  echo -e "${RED}failed${NC}"
  exit 1
fi

# 2. Clone role catalog (if not already present)
echo -n "  Role catalog... "
if [ -f "$ROLES_DEST/README.md" ]; then
  cd "$ROLES_DEST" && git fetch --depth=1 origin "$AGENCY_SHA" 2>/dev/null && git checkout "$AGENCY_SHA" 2>/dev/null && echo -e "${GREEN}up to date${NC}" || echo -e "${YELLOW}cached${NC}"
else
  mkdir -p "${HOME}/.hermes/skills/persona/roles"
  if git clone --depth=1 "$AGENCY_REPO" "$ROLES_DEST" 2>/dev/null; then
    echo -e "${GREEN}done${NC}"
  else
    echo -e "${YELLOW}GitHub unavailable — will use fallback at runtime${NC}"
  fi
fi

# 3. Deploy durable constants module
echo -n "  Durable constants... "
if [ -d "${HOME}/.hermes/hermes-agent/agent" ]; then
  cp "$(dirname "$0")/../agent/anima_persona.py" "${HOME}/.hermes/hermes-agent/agent/anima_persona.py" 2>/dev/null
  # Ensure prompt_builder.py imports from the durable module
  PB="${HOME}/.hermes/hermes-agent/agent/prompt_builder.py"
  if [ -f "$PB" ]; then
    if ! grep -q "from agent.anima_persona import" "$PB" 2>/dev/null; then
      # Add import after utils import
      sed -i '' '/^from utils import/a\\nfrom agent.anima_persona import ANIMA_PERSONA_LOADED, GATEWAY_PLATFORMS, GATEWAY_ANIMA_PERSONA_IDENTITY  # noqa: F401' "$PB" 2>/dev/null || \\\n      sed -i '/^from utils import/a\\nfrom agent.anima_persona import ANIMA_PERSONA_LOADED, GATEWAY_PLATFORMS, GATEWAY_ANIMA_PERSONA_IDENTITY  # noqa: F401' "$PB" 2>/dev/null
    fi
    echo -e "${GREEN}done${NC}"
  else
    echo -e "${YELLOW}prompt_builder.py not found${NC}"
  fi
else
  echo -e "${YELLOW}hermes-agent not found${NC}"
fi

# 4. Validate
echo ""
if [ -f "$DEST/SKILL.md" ]; then
  echo -e "${GREEN}✅${NC} hermes-persona installed"
  echo ""
  echo "Usage:"
  echo "  hermes kanban create 'Build auth API' --skill persona"
  echo "  hermes kanban assign t_xxxx persona-worker"
  echo "  hermes kanban dispatch"
  echo ""
  echo "Health check:"
  echo "  ${HOME}/.hermes/hermes-agent/scripts/anima-doctor.sh"
else
  echo -e "${RED}❌${NC} Installation failed" >&2
  exit 1
fi
