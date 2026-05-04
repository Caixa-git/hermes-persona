<p align="center">
  <img src="https://img.shields.io/badge/automatically_picks_the_right_expert_for_every_task-8A2BE2?style=flat-square" alt="tagline">
</p>

<p align="center">
  <samp>
    <big><strong>🎭 Hermes Persona</strong></big><br>
    <br>
    <sub>
      Every kanban worker automatically adopts<br>
      the best-fitting specialist role for its task
    </sub>
  </samp>
</p>

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent">
    <img src="https://img.shields.io/badge/runs_on-Hermes_Agent-8A2BE2?style=flat-square&logo=robot" alt="Hermes Agent">
  </a>
  <a href="https://github.com/msitarzewski/agency-agents">
    <img src="https://img.shields.io/badge/roles_from-agency_agents_172_experts-FF6B6B?style=flat-square" alt="Agency Agents">
  </a>
  <img src="https://img.shields.io/badge/tests-32_passing-22c55e?style=flat-square" alt="32 tests">
  <img src="https://img.shields.io/badge/setup-one_command-grey?style=flat-square" alt="setup">
</p>

<br>

> *"The greatest efficiency is obtained by dividing the work in such a manner that each worker is given a limited number of tasks to perform."*  
> — Frederick Winslow Taylor, *The Principles of Scientific Management* (1911)

---

## What it does

When Hermes Agent processes a kanban task, it analyzes the work and automatically picks the most suitable expert role from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog — **172 specialists across 15 domains**.

Each specialist comes with its own rules, workflows, and quality standards. The worker doesn't just execute the task — it executes it *as that expert*.

---

## What it looks like

```bash
# Start a chat session
hermes chat

# Then just say what you want naturally:
# 👤 "Build an e-commerce platform with payment integration"
#
# The system automatically:
#   1. Creates a planner task
#   2. Planner adopts 🏛️ Software Architect role
#   3. Planner decomposes the work into sub-tasks
#   4. Each sub-task gets its own expert

# To check progress from another terminal:
hermes kanban list
```

```
▶ t_...  ready   🏛️ Software Architect      E-commerce platform
▶ t_...  ready   🎨 Frontend Developer       Storefront UI
▶ t_...  ready   🏗️ Backend Architect        Payment API + JWT auth
▶ t_...  ready   🗄️ Database Optimizer       Product catalog schema
▶ t_...  ready   🚀 DevOps Automator         AWS deployment
```

No flags. No `--skill persona`. Every worker picks its own role automatically.

| Your task | The worker adopts |
|-----------|-----------------|
| Build a React dashboard | 🎨 Frontend Developer |
| Set up CI/CD pipeline | 🚀 DevOps Automator |
| Optimize PostgreSQL queries | 🗄️ Database Optimizer |
| Design REST API with JWT | 🏗️ Backend Architect |
| Scan API for vulnerabilities | 🔒 Security Engineer |
| Build an iOS login screen | 📱 Mobile App Builder |
| Plan product roadmap | 📋 Product Manager |

---

## How it works

Every kanban worker reads the built-in role adoption section in `KANBAN_GUIDANCE` (injected by Hermes Agent into every worker's system prompt):

```
Worker spawns
  → reads KANBAN_GUIDANCE (persona section built-in)
  → fetches agency-agents README via GitHub raw
  → scans 172 roles, picks the best match
  → logs "🎭 Role adopted: 🏗️ Backend Architect" via kanban_heartbeat
  → downloads the role's full .md specification
  → executes the task as that specialist
```

No local repo, no cloning, no management overhead. All role data is fetched on demand.

---

## Caveats

| Limitation | Detail |
|------------|--------|
| **`-z` / --oneshot** | Kanban orchestration requires a persistent session. `hermes -z` is one-shot and exits before workers finish. Use `hermes chat` and tell it what you want naturally. |
| **`delegate_task()`** | Native Hermes sub-agents don't go through the kanban pipeline — persona only activates for kanban workers. |

---

## Installation

Hermes Agent must be installed first. Then run:

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer:
- Adds the `kanban` toolset to your config (so chat can create tasks)
- Patches KANBAN_GUIDANCE with the persona role adoption section
- Places a reference skill at `~/.hermes/skills/persona/`

---

## Credits

| Project | Author | Role |
|---------|--------|------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | [msitarzewski](https://github.com/msitarzewski) | 172 expert role definitions across 15 domains |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [Nous Research](https://nousresearch.com) | Kanban-based multi-agent orchestration framework |

All 172 specialist role definitions are sourced from the agency-agents repository — a meticulously crafted collection of AI agent personalities with deep domain expertise, production-ready workflows, and measurable deliverables.

---

## Roadmap

- [x] Automatic role selection — 172 experts, no flags, immediate
- [x] Emoji identification — roles are visible in the kanban task list
- [ ] **Smarter matching** — multi-dimensional scoring (domain, activity, tech stack, complexity)

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>Created by <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
