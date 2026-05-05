# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-05-06

### Added
- SKILL.md refactored: Gateway Contract and Philosophical Model extracted to separate reference files (457→379 lines)
- `test_benchmark.py --offline` flag: skips network-dependent tests with explicit message
- Part 4 in test_benchmark.py: pyproject.toml version check + reference doc existence validation
- `.gitignore`: Python standard entries (pycache, venv, .env, IDE)
- `CONTRIBUTING.md`: expanded from 9 to 64 lines — PR workflow, checklist, design principles
- `CHANGELOG.md`: this file
- GitHub Actions: `sha-check.yml` — weekly SHA pin verification + auto-issue creation on failure

### Fixed
- `pyproject.toml` version: 0.1.0 → 1.0.0 (regression from repo simplification commit)
- `README.md`: stale "37 tests pass" reference removed; table formatting fixed
- `install.sh`: dual-sed fallback replaced with OS-detected single sed; git error visibility improved
- `agent/anima_persona.py`: added `#!/usr/bin/env python3` shebang

### Removed
- `develop` branch: stale branch deleted (behind `main` by 10+ commits)
- `scripts/patch-gateway-anima-persona.py`: fragile exact-string markers replaced with multi-strategy patching (exact → regex → AST fallback)

## [1.0.0] - 2026-05-05

### Added
- Initial release: 172-specialist role adoption for Hermes Agent kanban workers
- Single persona adoption protocol (10 steps)
- Multi-persona (major + minor) with CDPD decision model
- Gateway identity injection (GATEWAY_ANIMA_PERSONA_IDENTITY, ~105 tokens)
- `install.sh` with --dry-run/--update/--uninstall support
- `test_benchmark.py` (37+ tests covering SKILL.md integrity, catalog, role mappings)
- 6 reference documents (CDPD model, multi-persona experiment, identity conventions, etc.)
- `SECURITY_AUDIT.md` documenting risk assessment
