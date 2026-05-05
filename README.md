<p align="center">
  <img alt="persona" src=".github/hermes-persona-logo.svg" width="100" height="100">
</p>

<p align="center">
  <h2 align="center">persona</h2>
  <p align="center"><strong>Expert role adoption</strong> for kanban workers —<br>172 specialists across 15 categories, auto-selected by task context.</p>
</p>

<p align="center">
  <a href="https://github.com/msitarzewski/agency-agents"><img src="https://img.shields.io/badge/roles-172-6366f1?style=flat-square&labelColor=1a1a2e" alt="roles"></a>
  <a href="https://github.com/msitarzewski/agency-agents"><img src="https://img.shields.io/badge/categories-15-a78bfa?style=flat-square&labelColor=1a1a2e" alt="categories"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-3b82f6?style=flat-square&labelColor=1a1a2e" alt="license"></a>
  <a href="https://github.com/Caixa-git/hermes-persona/releases"><img src="https://img.shields.io/github/v/release/Caixa-git/hermes-persona?style=flat-square&labelColor=1a1a2e&color=06b6d4" alt="release"></a>
  <a href="https://github.com/Caixa-git/hermes-persona/actions"><img src="https://img.shields.io/github/actions/workflow/status/Caixa-git/hermes-persona/ci.yml?style=flat-square&labelColor=1a1a2e&color=22c55e&label=CI" alt="CI"></a>
</p>

<p align="center">
  <img alt="persona in action" src=".github/hero-terminal.svg" width="720">
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
# → 🎭 Security Engineer
```

---

## How it works

```
Task ──→ scan 172 roles ──→ fit >30%? ──→ adopt specialist
                                  ↓
                             ≤30%? ──→ no role (generalist fallback)
```

| Principle | Paper |
|-----------|-------|
| Output alignment | MetaGPT (ICLR 2024) |
| Boundary clarity | CAMEL (NeurIPS 2023) |
| Decomposition priority | AgentVerse (ICML 2024) |
| Confidence threshold | AutoGen (2023) |

---

## Persona vs Anima

| | Persona | Anima |
|---|---|---|
| **Nature** | Social role (인공적) | Core identity (본질) |
| **Activation** | `--skill persona` — opt-in | Always active |
| **Priority** | — | Anima > Persona |

[hermes-anima](https://github.com/Caixa-git/hermes-anima) → always-on OCEAN identity.

---

## Install

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

Verify: `python3 test_benchmark.py` (37 tests).

---

<p align="center">
  <a href="https://github.com/Caixa-git/hermes-anima">anima</a> ·
  <a href="https://github.com/msitarzewski/agency-agents">agency-agents</a> ·
  <a href="./CONTRIBUTING.md">contributing</a>
</p>
