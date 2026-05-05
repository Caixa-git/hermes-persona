<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/hermes--persona-%F0%9F%8E%AD-1a1a2e?style=for-the-badge">
    <img src="https://img.shields.io/badge/hermes--persona-%F0%9F%8E%AD-1a1a2e?style=for-the-badge">
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/kanban-automated-blueviolet?style=flat-square">
  <img src="https://img.shields.io/badge/roles-172-2ea44f?style=flat-square">
  <img src="https://img.shields.io/badge/categories-15-ff6b6b?style=flat-square">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square">
</p>

<p align="center">
  <b>Every kanban worker auto-adopts the best-fitting specialist role.</b><br>
  172 roles · 15 categories · zero config · one keyword
</p>

---

## ⚡ Quick start

```bash
# In chat — just say:
use persona

# Or from CLI:
hermes kanban create 'Security audit' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

**That's it.** The worker fetches [agency-agents](https://github.com/msitarzewski/agency-agents), picks the role that matches your task, and announces via heartbeat.

> `🎭 Role adopted: 🔒 Security Engineer` — appears in kanban event logs.

## 🧠 How it works

```
Task comes in → analyze title + body → scan 172 roles (15 categories)
                                    ↓
                    ┌── confidence >30% ──→ adopt specialist role
                    │
                    └── confidence <30% ──→ proceed without role
                                             (generalist anima takes over)
```

**4 selection principles:**

| # | Principle | Source | Rule |
|:-:|:----------|:-------|:-----|
| 1 | **Output alignment** | MetaGPT (ICLR 2024) | Match deliverable to task — a Backend Architect writes API specs, not PRDs |
| 2 | **Boundary clarity** | CAMEL (NeurIPS 2023) | Exactly one role, non-overlapping. No duplicate specialists per task |
| 3 | **Decomposition priority** | AgentVerse (ICML 2024) | Pick the primary domain — the subtask everything else depends on |
| 4 | **Confidence threshold** | AutoGen (Microsoft 2023) | Below 30%? No role. Forcing a mismatch degrades output by 40-50% |

## 🎭 Persona vs 🧠 Anima

| | Persona | Anima |
|---|---|---|
| **Nature** | Social role (인공적, 수동) | Core identity (본질, 자동) |
| **Activation** | `use persona` — opt-in | Installed = always active |
| **Scope** | Changes per task | Stable across tasks |
| **Priority** | — | **Anima > Persona** on conflict |

> Nature prevails over role. Both sit at Layer 13 — social framing enforces the priority, not position alone (Geng et al., AAAI 2026).

[Explore hermes-anima →](https://github.com/Caixa-git/hermes-anima)

## 📦 Install

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer:
1. Writes `skills/persona/SKILL.md` — the core persona system
2. Enables the `kanban` toolset in `config.yaml`
3. Patches `KANBAN_GUIDANCE` so every worker gets identity context
4. Generates `install.sh.sha256` for integrity verification

## 🗂️ Structure

```
hermes-persona/
├── skills/persona/SKILL.md    ← The persona prompt (this)
├── install.sh                  ← One-line installer
├── test_benchmark.py           ← CI: 37 tests
├── SECURITY_AUDIT.md
├── CONTRIBUTING.md
└── README.md
```

## ✅ Validation

```bash
python3 test_benchmark.py   # 37 tests, all pass
```

## 📚 Related

| Project | Description |
|:--------|:------------|
| [hermes-anima](https://github.com/Caixa-git/hermes-anima) | 🧠 Core nature — always-on identity with OCEAN profiles |
| [hermes-agency](https://github.com/Caixa-git/hermes-agency) | 🤖 Multi-agent orchestration |
| [agency-agents](https://github.com/msitarzewski/agency-agents) | 📋 Source catalog — 172 specialist roles |

## 📄 License

MIT — see [LICENSE](LICENSE).
