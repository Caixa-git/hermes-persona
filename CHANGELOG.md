# Changelog

All notable changes to Hermes Persona are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-05-05

### Added

- **Persona role adoption system** — every kanban worker automatically analyzes the task and adopts the best-fitting specialist role from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog
- **172 specialist roles across 15 domains** — from Frontend Developer to Security Engineer, DevOps Automator to Product Manager. Each role comes with its own rules, workflows, and quality standards
- **Research-backed role selection** — role matching guided by 4 published principles: output-type alignment (MetaGPT), role boundary clarity (CAMEL), task decomposition priority (AgentVerse), and confidence threshold (AutoGen)
- **15-task benchmark for role selection** — 47-test automated suite verifying role assignment accuracy (15/15 correct, 100%)
- **Opt-in `--skill persona` design** — persona activates per-kanban-task via explicit skill flag, not automatic injection
- **Installation script (`install.sh`)** — patches KANBAN_GUIDANCE with persona section, places reference skill, prompts per-profile for `.env` symlink
- **SHA256 checksum verification** for `install.sh` — two-step install flow with `sha256sum -c`
- **Reference skill** at `~/.hermes/skills/persona/` — full SKILL.md with rules, triggers, and workflows
- **12 reference documents** in `skills/persona/references/` covering benchmark methodology, chain propagation, dispatcher-worker architecture, docker smoke test, external system integration, kanban dispatch setup, kanban-guidance patch, Korean usage patterns, matching improvement research, multi-agent cross-validation, role URL patterns, and security audit methodology
- **CI/CD pipeline** — GitHub Actions workflow running on push/PR to develop/main with Python 3.11, reference doc audit, and shell syntax check
- **`pyproject.toml`** with isort + black configuration
- **SBOM generation script** (`scripts/generate-sbom.py`)
- **CONTRIBUTING.md** — Git Flow conventions, local dev setup, PR checklist
- **Emoji role identification** — roles display with emoji identifiers in the kanban task list (🎭, 🏗️, 🎨, 🚀, 🔒, etc.)

### Fixed

- **SHA256 checksums** — `install.sh` now includes proper checksum verification (M1)
- **`.env` symlink made opt-in** — per-profile prompt instead of automatic symlinking (M2)
- **Agency-agents pinned to commit `783f6a7`** — role specs fetched from this exact snapshot, not `main` branch (M6)
- **Injection prevention** — M4 injection vectors mitigated (M4)
- **SBOM UUID/purl/version corrections** — proper UUID generation, package URLs, version strings (I1-I4)
- **`test_benchmark.py`** — reads from `SKILL.md` instead of `prompt_builder.py` for maintainable test source
- **9 missing reference documents created** — closed documentation gap discovered by review audit
- **`install.sh` SKILL.md heredoc updated** — replaced old design with current opt-in `--skill persona` design
- **Code quality fixes** — removed dead code (`status_map` in main.py, `eventListeners` in app.js, `.desk-leg` CSS), added `PORT` env var support, added `pyproject.toml`
- **CI workflow removed and re-added** — token lacked `workflow` scope; re-created for v1.0.0 release

### Security

- **Full security audit report (SECURITY_AUDIT.md)** — comprehensive audit of install process, credential handling, dependency chain, and codebase
- **14 findings resolved** — all original findings marked resolved with verification notes
- **Post-fix follow-up audit** — no remaining unaddressed findings
- **SHA256 checksum verification** for `install.sh` download (prevents tampered-installer attacks)
- **Per-profile `.env` opt-in** (reduces credential blast radius)
- **Pinned upstream dependency** (prevents supply-chain role injection)

[1.0.0]: https://github.com/Caixa-git/hermes-persona/releases/tag/v1.0.0
