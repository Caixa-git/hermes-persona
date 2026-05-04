# Contributing to Hermes Persona

Thank you for your interest in contributing! This guide covers everything you need to know to work on the hermes-persona project effectively.

---

## Table of Contents

- [Git Flow Workflow](#git-flow-workflow)
- [Local Development Setup](#local-development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Test Execution Guide](#test-execution-guide)
- [Pull Request Lifecycle](#pull-request-lifecycle)
- [PR Checklist Template](#pr-checklist-template)
- [Reference Docs Contribution Guide](#reference-docs-contribution-guide)
- [Getting Help](#getting-help)

---

## Git Flow Workflow

This project follows **Git Flow** with strict branch isolation.

### Branch Naming

| Branch pattern | Purpose | Source | PR merges to |
|---|---|---|---|
| `main` | Production releases | — | — |
| `develop` | Integration branch | — | `main` (via release PR) |
| `feature/<slug>` | New features | `develop` | `develop` |
| `fix/<slug>` | Bug fixes | `develop` | `develop` |
| `release/<version>` | Release candidates | `develop` | `develop` + `main` |
| `hotfix/<slug>` | Urgent production fixes | `main` | `main` + `develop` |

Slugs should be kebab-case, e.g., `feature/jwt-auth` or `fix/home-path-bug`.

### Rules

- **No direct commits** to `main` or `develop` — all changes go through a pull request.
- **Feature branches** branch from `develop`, PR back to `develop`.
- **Hotfix branches** branch from `main`, PR back to both `main` and `develop`.
- **Rebase before PR** — rebase your branch onto the target branch and resolve conflicts locally. Do not create PRs with merge conflicts.
- **Squash commits** on merge when the branch contains messy WIP history. Use a descriptive squash message.

### Merge Strategy

- `develop` → `main`: **merge commit** (preserves the release boundary)
- feature/fix branches → `develop`: **squash merge** (kept tidy)
- `hotfix/` → `main`: **merge commit** (marks the production fix point)
- `hotfix/` → `develop`: **merge commit** or **squash** (whichever is cleaner)

---

## Local Development Setup

### Prerequisites

- **Python 3.11+** (the project targets 3.11; see `pyproject.toml`)
- **Git** configured with your SSH key or HTTPS token
- **Hermes Agent** (for full kanban integration) — see the [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs)

### 1. Clone the repository

```bash
git clone git@github.com:Caixa-git/hermes-persona.git
cd hermes-persona
```

### 2. (Optional) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No third-party dependencies are required to run the benchmark — the test suite uses only Python stdlib (`os`, `sys`, `json`, `re`, `urllib.request`).

### 3. Install the project (Hermes users)

If you want to use the persona system with Hermes Agent:

```bash
# Two-step with SHA256 verification (recommended)
curl -sSLO https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh
curl -sSLO https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh.sha256
sha256sum -c install.sh.sha256 && bash install.sh

# Or quick one-liner
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

### 4. Verify the setup

```bash
python3 test_benchmark.py
bash -n install.sh
```

---

## Code Style Guidelines

### Python

| Tool | Rule |
|---|---|
| **Formatter** | [Black](https://black.readthedocs.io/) — line length **100** |
| **Import sorter** | [isort](https://pycqa.github.io/isort/) — `profile = "black"`, same line length |
| **Target Python** | 3.11 |
| **Naming** | `snake_case` for functions/variables, `UPPER_CASE` for constants, `PascalCase` for classes |
| **Type hints** | Strongly encouraged on all public functions |
| **Docstrings** | Use `"""triple double quotes"""`. Module-level docstring describes what the file does. |
| **Linter (optional)** | [Ruff](https://docs.astral.sh/ruff/) — see `pyproject.toml` for config |

Before committing Python code:

```bash
# Format
black --line-length=100 .
isort --profile=black --line-length=100 .

# Check (no auto-fix)
black --check --line-length=100 .
isort --check --profile=black --line-length=100 .
```

### Shell

All shell scripts (`.sh` files) must pass syntax validation:

```bash
bash -n install.sh
```

Avoid the following in shell scripts:
- Unquoted variable expansions (use `"$var"` instead of `$var`)
- `eval` on untrusted input
- `set -euo pipefail` at the top of every script

### Markdown / Documentation

- Wrap lines at **100 characters** for readability
- Use ATX headings (`##`, `###`, etc.) — not underlined `===`
- Use fenced code blocks with language tags (` ```bash `, ` ```python `)
- All links must be relative within the repo or pinned to a commit SHA on GitHub
- Tables must be valid GFM (pipe alignment)

---

## Test Execution Guide

### Running the Benchmark

```bash
python3 test_benchmark.py
```

This executes **47 tests** across 6 sections:

| Section | What it checks |
|---|---|
| [1/6] Persona SKILL.md | All 4 research principles present + citations |
| [2/6] Agency-agents catalog | README fetchable, 14 key roles exist |
| [3/6] Task-to-role mappings | 15 benchmark mappings validated |
| [4/6] Kanban toolset in config | `kanban` found in `config.yaml` toolsets |
| [5/6] Persona skill file | SKILL.md has research principle keywords |
| [6/6] Essential repo files | LICENSE, install.sh, README.md, .gitignore present |

### Understanding Results

```
============================================================
🎭 Hermes Persona — Role Selection Benchmark
============================================================

📋 [1/3] Persona SKILL.md — Research principles present
--------------------------------------------------
  ✅ Principle present: Output-type alignment
  ✅ Principle present: Role boundary clarity
  ✅ Principle present: Task decomposition priority
  ✅ Principle present: Confidence threshold
  ...

============================================================
📊 Result: 47/47 passed (100%)
============================================================
```

- **All pass (47/47)**: The system is fully operational
- **Part 4 (kanban toolset) failure**: Hermes Agent isn't configured with `kanban` in its toolsets — run `hermes config set toolsets.to_use '[..., "kanban"]'` or re-run `install.sh`
- **Part 2 (catalog) failure**: Network issue — the test fetches the agency-agents README from GitHub raw. Ensure you have internet access and the pinned commit SHA is still valid
- **Part 1 (principles) failure**: The persona `SKILL.md` is missing or corrupted — re-run `install.sh`

### Test Metadata for CI

Each run prints one line per test with emoji status. The exit code is `0` if all tests pass, `1` if any fail. This makes it CI-native — no adapter needed.

```yaml
# .github/workflows/ci.yml example
- name: Run tests
  run: python3 test_benchmark.py
```

### Environment Notes

- The test suite reads the persona skill from `~/.hermes/skills/persona/SKILL.md`. If this file doesn't exist (e.g., in CI without `install.sh`), Part 1 will fail. The CI workflow skips this limitation by not checking `$HOME` in CI context.
- **Known issue**: When running inside profile contexts where `HOME` is redirected to `~/.hermes/profiles/<profile>/home/`, `os.path.expanduser("~")` may resolve to the wrong directory. If tests fail unexpectedly, check that `~/.hermes/skills/persona/SKILL.md` is accessible from your active profile's home.

---

## Pull Request Lifecycle

1. **Branch** — create a feature or fix branch from `develop`
2. **Code** — write your changes following the [code style guidelines](#code-style-guidelines)
3. **Test** — run the full benchmark suite: `python3 test_benchmark.py`
4. **Lint** — `black --check`, `isort --check`, `bash -n install.sh`
5. **Rebase** — rebase onto the latest `develop` (or `main` for hotfixes)
6. **PR** — open a pull request to `develop` (or `main` for hotfixes) with a descriptive title and link to the related issue
7. **Review** — at least one maintainer must approve. Address all feedback
8. **Merge** — squash-merge to `develop` (or merge-commit to `main`)
9. **Clean up** — delete the feature branch after merge

### PR Title Format

```
<type>(<scope>): <short description>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`

Examples:
```
feat(core): add confidence threshold fallback for low-match roles
fix(benchmark): correct HOME path resolution in profile contexts
docs(references): add docker-smoke-test reference doc
```

---

## PR Checklist Template

Copy this checklist into your pull request description:

```markdown
- [ ] Tests pass: `python3 test_benchmark.py` — 47/47
- [ ] Shell syntax valid: `bash -n install.sh`
- [ ] Code formatted: `black --check --line-length=100` and `isort --check --profile=black --line-length=100`
- [ ] Reference docs match SKILL.md mentions (if docs changed)
- [ ] Branch follows Git Flow naming (`feature/`, `fix/`, `hotfix/`, `release/`)
- [ ] Commits reference issue number (e.g., `Refs #42`)
- [ ] Rebased onto latest `develop` (or `main` for hotfixes)
- [ ] No merge conflicts with target branch
- [ ] Self-review: no debug prints, no commented-out code, no TODOs without a linked issue
```

---

## Reference Docs Contribution Guide

The `skills/persona/references/` directory contains supplementary documentation for the persona system. Each reference doc is a `.md` file covering a specific subtopic.

### When to create a reference doc

- A topic is too detailed for the main `SKILL.md` but too small for its own standalone document
- The topic is referenced from multiple places (SKILL.md, install.sh comments, test_benchmark.py comments)
- The topic explains *how* something works (architecture, protocol, methodology) rather than *what* the project does

### Required frontmatter

Every reference doc must start with:

```yaml
---
title: Your Title Here
description: One-sentence description of the document's purpose
---
```

### Naming convention

- Kebab-case filenames: `benchmark-methodology.md`, `chain-propagation-test.md`
- One file per topic — don't split a single concept across multiple files

### Content standards

- Start with a one-paragraph summary of the topic
- Use level-2 headings (`##`) for major sections, level-3 (`###`) for subsections
- Include code examples where relevant (fenced with language tag)
- Keep each doc focused on one subject — cross-link to other docs via relative paths

### Where reference docs are checked

The CI pipeline (`reference-audit` job in `.github/workflows/ci.yml`) verifies that all expected reference docs exist. When you add or remove a reference doc, update the CI workflow accordingly.

### Example

```yaml
---
title: Benchmark Methodology
description: How the 15-task role-selection benchmark is designed and scored
---

## Overview

The benchmark validates that the persona role-adoption system correctly...
```

---

## Getting Help

- **Issues**: Open a [GitHub Issue](https://github.com/Caixa-git/hermes-persona/issues) for bugs, feature requests, or questions
- **Hermes Agent docs**: [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs)
- **Agency-agents catalog**: [github.com/msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (pinned to commit `783f6a7`)
