#!/usr/bin/env bash
set -euo pipefail

REPO="https://raw.githubusercontent.com/Caixa-git/hermes-persona/main"
DEST="${HOME}/.hermes/skills/persona"

for arg in "$@"; do
  case "$arg" in
    --help|-h) echo "Usage: bash install.sh"; echo "Installs hermes-persona skill."; exit 0 ;;
  esac
done

mkdir -p "$DEST"

# fetch SKILL.md — the only runtime artifact
if curl -sSL "$REPO/skills/persona/SKILL.md" -o "$DEST/SKILL.md"; then
  echo "✅ hermes-persona installed"
  echo ""
  echo "Usage:"
  echo "  hermes kanban create 'Build auth API' --skill persona"
  echo "  hermes kanban assign t_xxxx persona-worker"
  echo "  hermes kanban dispatch"
else
  echo "❌ Failed to fetch SKILL.md" >&2
  exit 1
fi
