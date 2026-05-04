<p align="center">
  <img src="https://img.shields.io/badge/auto--assigns_the_right_expert_for_every_task-8A2BE2?style=flat-square" alt="subtitle">
</p>

<p align="center">
  <samp>
    <big><strong>🎭 Hermes Persona</strong></big><br>
    <br>
    <sub>
      Every kanban task automatically gets<br>
      the best-fitting specialist persona
    </sub>
  </samp>
</p>

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent">
    <img src="https://img.shields.io/badge/runs_on-Hermes_Agent-8A2BE2?style=flat-square&logo=robot" alt="Hermes Agent">
  </a>
  <a href="https://github.com/msitarzewski/agency-agents">
    <img src="https://img.shields.io/badge/uses-agency_agents-FF6B6B?style=flat-square" alt="Agency Agents">
  </a>
  <img src="https://img.shields.io/badge/172_expert_roles-FFD700?style=flat-square" alt="172 experts">
  <img src="https://img.shields.io/badge/install_in_1s-grey?style=flat-square" alt="install">
</p>

<br>

---

**Hermes Persona** automatically picks the right expert persona for every kanban task.

When Hermes Agent spawns a worker for a task, the system analyzes the task description, scans 172 specialist roles, and selects the best match. The worker then adopts that expert's workflow, rules, and standards — no flags, no configuration.

<br>

## 📖 How it works

| Task | Expert selected |
|----------|---------------|
| Build an online store | 🏗️ Backend Architect |
| Design a dashboard UI | 🎨 Frontend Developer |
| Security audit a server | 🔒 Security Engineer |
| Set up CI/CD pipelines | 🚀 DevOps Automator |
| Optimize database queries | 🗄️ Database Optimizer |
| Build a mobile app | 📱 Mobile App Builder |

Each expert has their own rules, checklists, and working principles. The worker doesn't just complete the task — it completes it *as that specialist*.

<br>

## 🔄 Flow

```
Task assigned → worker reads the task
    → scans 172 roles from the catalog
    → picks the best-fitting expert
    → records "🎭 Role adopted: 🏗️ Backend Architect"
    → loads the specialist's full specification
    → works as that expert
```

All role data is fetched on demand from GitHub raw — nothing to clone or manage locally.

<br>

## 📦 Install

Make sure [Hermes Agent](https://github.com/NousResearch/hermes-agent) is installed, then run:

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

That's it. No flags, no config, no setup — everything works automatically after install.

<br>

## 🗺️ Roadmap

- [x] Automatic role selection — 172 roles, zero configuration
- [x] Emoji role display — visible in kanban event logs
- [ ] **Smarter matching** — multi-dimensional scoring for better accuracy

<br>

## 🙏 Credits

| Project | Author | Description |
|----------|--------|-------------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | msitarzewski | 172 expert AI personas across 15 domains |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | Multi-agent orchestration framework with kanban |

<br>

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>Made by <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
