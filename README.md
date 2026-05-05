<p align="center">
  <img src="https://img.shields.io/badge/hermes--persona-%F0%9F%8E%AD-1a1a2e?style=for-the-badge">
  <img src="https://img.shields.io/badge/roles-172-2ea44f?style=flat-square">
  <img src="https://img.shields.io/badge/categories-15-ff6b6b?style=flat-square">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square">
</p>

```
            ,;/       \`.                ,'/       \`.
           ::(         ) :              : (         ) :
           |:::._____,'  |              |  `._____,'  |
           |:::::::      |              |             |
           |:::::::  _   |              |   _     _   |
           |:: |              |   |
           |::::::|      |              |      |      |
           |::::::|      |              |      |      |
           :::|.`:|,'/|  :              :  |.`.|,'/|  :
           :::| `-'-' |  ;              :  | `---' |  ;
            \::       ; /                \ :       ; /
             \:\     / /                  \ \     / /
              \::-.-' /                    \ `---' /
               `::| ,'                      `.   ,'
                 `:'                         `.'
```

<p align="center">
  <b>Every kanban worker auto-adopts the best-fitting specialist role.</b><br>
  172 roles × 15 categories × zero config × one keyword
</p>

---

## ⚡ Use persona

```bash
# In chat:
use persona

# From CLI:
hermes kanban create 'Audit OWASP top 10' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

Worker fetches [agency-agents](https://github.com/msitarzewski/agency-agents), picks the best-fit specialist, and announces via heartbeat.

```
🎭 Role adopted: 🔒 Security Engineer
```

## 🧠 How it works

```
Task in ─→ analyze title + body ─→ scan 172 roles (15 categories)
                                         ↓
                          ┌── confidence >30% ──→ adopt specialist role
                          │
                          └── confidence <30% ──→ proceed without a role
                                                   (generalist anima fallback)
```

**4 selection principles:**

| # | Principle | Source | Rule |
|:-:|:----------|:-------|:-----|
| 1 | **Output alignment** | MetaGPT (ICLR 2024) | Match deliverable to task — a Backend Architect writes API specs, not PRDs |
| 2 | **Boundary clarity** | CAMEL (NeurIPS 2023) | Exactly one role, non-overlapping |
| 3 | **Decomposition priority** | AgentVerse (ICML 2024) | Pick the primary domain first |
| 4 | **Confidence threshold** | AutoGen (2023) | Below 30%? No role. Mismatch degrades output 40-50% |

## 🎭 Persona vs 🧠 Anima

| | Persona | Anima |
|---|---|---|
| **Nature** | Social role (인공적, 수동) | Core identity (본질, 자동) |
| **Activation** | `--skill persona` — opt-in | Installed = always active |
| **Scope** | Changes per task | Stable across tasks |
| **Priority** | — | **Anima > Persona** on conflict |

> Nature prevails over role. Both at Layer 13 — social framing enforces priority, not position alone (Geng et al., AAAI 2026).

👉 [Explore hermes-anima →](https://github.com/Caixa-git/hermes-anima)

## 📦 Install

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

Installer:
1. Writes `skills/persona/SKILL.md` — the core persona system
2. Enables `kanban` toolset in `config.yaml`
3. Patches `KANBAN_GUIDANCE` for worker identity context
4. Generates `install.sh.sha256` for integrity verification

## 🗂️ Structure

```
hermes-persona/
├── skills/persona/SKILL.md    ← The persona system
├── install.sh                  ← One-line installer
├── test_benchmark.py           ← CI: 37 tests
├── SECURITY_AUDIT.md
├── CONTRIBUTING.md
└── README.md
```

## ✅ Validation

```bash
python3 test_benchmark.py
```

## 📚 Related

| Project | Description |
|:--------|:------------|
| [hermes-anima](https://github.com/Caixa-git/hermes-anima) | 🧠 Core nature — always-on OCEAN identity |
| [hermes-agency](https://github.com/Caixa-git/hermes-agency) | 🤖 Multi-agent orchestration |
| [agency-agents](https://github.com/msitarzewski/agency-agents) | 📋 172 specialist roles (source catalog) |

## 📄 License

MIT — see [LICENSE](LICENSE).
