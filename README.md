# persona

> Expert role adoption for kanban workers — 172 specialists across 15 categories, auto-selected by task context.

[![roles](https://img.shields.io/badge/roles-172-6366f1?style=flat-square&labelColor=1a1a2e)](https://github.com/msitarzewski/agency-agents)
[![categories](https://img.shields.io/badge/categories-15-a78bfa?style=flat-square&labelColor=1a1a2e)](https://github.com/msitarzewski/agency-agents)
[![CI](https://img.shields.io/github/actions/workflow/status/Caixa-git/hermes-persona/ci.yml?style=flat-square&labelColor=1a1a2e&color=22c55e&label=CI)](https://github.com/Caixa-git/hermes-persona/actions)
[![release](https://img.shields.io/github/v/release/Caixa-git/hermes-persona?style=flat-square&labelColor=1a1a2e&color=06b6d4)](https://github.com/Caixa-git/hermes-persona/releases)
[![license](https://img.shields.io/badge/license-MIT-3b82f6?style=flat-square&labelColor=1a1a2e)](./LICENSE)

## Purpose

Every kanban worker needs the right frame to solve a task. A security audit calls for a Security Engineer, not a generalist. A payment API calls for a Backend Architect, not a Frontend Developer. `persona` auto-selects the best-fitting specialist role from a catalog of 172 — and when no role fits well enough, it proceeds without one, rather than forcing a mismatch that degrades output (40–50% penalty, empirically verified).

## Quick start

```bash
# In chat — just ask
use persona

# From CLI — create a task with persona loaded
hermes kanban create 'Audit OWASP top 10' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
# → 🎭 Security Engineer
```

## How it works

```
Task ──→ scan 172 roles ──→ fit >30%? ──→ adopt specialist role
                                  ↓
                             ≤30%? ──→ no role (generalist fallback)
```

Four research-backed selection principles determine the role:

| Principle | Reference |
|-----------|-----------|
| Output-type alignment — match deliverable to task | MetaGPT (ICLR 2024) |
| Role boundary clarity — exactly one role, non-overlapping | CAMEL (NeurIPS 2023) |
| Task decomposition priority — primary domain first | AgentVerse (ICML 2024) |
| Confidence threshold — ≤30% → no role, avoid mismatch harm | AutoGen (2023) |

## Persona & Anima

Persona works alongside [anima](https://github.com/Caixa-git/hermes-anima), the always-on core identity. Both enter at the same prompt layer — social framing enforces priority (Geng et al., AAAI 2026), not layer position alone.

| Dimension | Persona | Anima |
|-----------|---------|-------|
| Nature | Social role (인공적, 수동) | Core identity (본질, 자동) |
| Activation | `--skill persona` — opt-in | Always active |
| Scope | Changes per task | Stable across tasks |
| Priority | — | **Anima > Persona** on conflict |

## Status

| Badge | Meaning |
|-------|---------|
| ![CI](https://img.shields.io/github/actions/workflow/status/Caixa-git/hermes-persona/ci.yml?style=flat-square&labelColor=1a1a2e&color=22c55e&label=CI) | Tests pass on `main` (CI badge) |
| ![release](https://img.shields.io/github/v/release/Caixa-git/hermes-persona?style=flat-square&labelColor=1a1a2e&color=06b6d4) | Latest tagged release |
| ![license](https://img.shields.io/badge/license-MIT-3b82f6?style=flat-square&labelColor=1a1a2e) | MIT — free to use, modify, distribute |

## Install

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer writes `skills/persona/SKILL.md` to your Hermes Agent skills directory, enables the `kanban` toolset, and patches KANBAN_GUIDANCE for worker identity context.

## Post-install verification

```bash
# Quick check (offline-safe)
python3 test_benchmark.py --offline

# Identity section verification
python3 skills/persona/scripts/verify-identity-section.py --prompt-builder-only

# Full suite (requires network)
python3 test_benchmark.py
```

## References

- [agency-agents](https://github.com/msitarzewski/agency-agents) — 172 specialist roles catalog
- [hermes-anima](https://github.com/Caixa-git/hermes-anima) — always-on OCEAN core identity
- Prana et al. (2018). *Categorizing the Content of GitHub README Files.* arXiv:1802.06997
- Gaughan et al. (2025). *The Introduction of README and CONTRIBUTING Files in OSS.* arXiv:2502.18440
