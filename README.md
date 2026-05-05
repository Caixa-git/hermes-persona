<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/hermes-persona-logo.svg">
    <img alt="hermes-persona" src=".github/hermes-persona-logo.svg" width="100" height="100">
  </picture>
</p>

<p align="center">
  <h2 align="center">hermes-persona</h2>
  <p align="center">Every kanban worker auto-adopts the best-fitting specialist role —<br>172 roles across 15 categories, zero config, one keyword.</p>
</p>

<p align="center">
  <a href="https://github.com/msitarzewski/agency-agents"><img src="https://img.shields.io/badge/roles-172-2ea44f?style=flat-square" alt="roles"></a>
  <a href="https://github.com/msitarzewski/agency-agents"><img src="https://img.shields.io/badge/categories-15-8b5cf6?style=flat-square" alt="categories"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="license"></a>
  <a href="https://github.com/Caixa-git/hermes-persona/releases"><img src="https://img.shields.io/github/v/release/Caixa-git/hermes-persona?style=flat-square" alt="release"></a>
</p>

---

## Quick start

```bash
# In chat
use persona

# From CLI
hermes kanban create 'Audit OWASP top 10' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
# → 🎭 Role adopted: 🔒 Security Engineer
```

---

## How it works

```
Task ──→ scan 172 roles ──→ confidence >30%? ──→ adopt specialist
                                       ↓
                                  <30%? ──→ generalist (no role)
```

| Principle | Source |
|-----------|--------|
| Output alignment | MetaGPT (ICLR 2024) |
| Boundary clarity | CAMEL (NeurIPS 2023) |
| Decomposition priority | AgentVerse (ICML 2024) |
| Confidence threshold | AutoGen (2023) |

---

## Persona & Anima

| | Persona | Anima |
|---|---|---|
| Nature | Social role (인공적) | Core identity (본질) |
| Activation | `--skill persona` — opt-in | Always active |
| Priority | — | Anima > Persona |

[hermes-anima](https://github.com/Caixa-git/hermes-anima) → always-on OCEAN identity.

---

## Install

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

Verification: `python3 test_benchmark.py` (37 tests).

---

## Structure

```
skills/persona/SKILL.md    ← Core system (56 lines)
test_benchmark.py           ← 37 tests
install.sh                  ← One-line installer
```

---

<p align="center">
  <a href="https://github.com/Caixa-git/hermes-anima">hermes-anima</a> ·
  <a href="https://github.com/msitarzewski/agency-agents">agency-agents</a> ·
  <a href="./CONTRIBUTING.md">contributing</a>
</p>
