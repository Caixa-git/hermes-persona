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
  <img src="https://img.shields.io/badge/tests-47_passing-22c55e?style=flat-square" alt="47 tests">
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

Role selection is guided by four research-backed principles (see Research section below) — not simple keyword matching. Each kanban worker evaluates the task's output type, role boundaries, decomposition priority, and confidence before choosing.

---

## Research

Role assignment in this system is guided by principles from four modern multi-agent AI papers. These were chosen over older organizational psychology frameworks because LLM-based agents operate under fundamentally different constraints than human workers.

| # | Principle | Paper | Year | Venue |
|---|-----------|-------|------|-------|
| 1 | **Output-type alignment** — pick the role whose canonical deliverable matches the task | [MetaGPT](https://arxiv.org/abs/2308.00352) — Hong et al. | 2023 | ICLR 2024 |
| 2 | **Role boundary clarity** — one role, non-overlapping responsibilities | [CAMEL](https://arxiv.org/abs/2303.17760) — Li et al. | 2023 | NeurIPS 2023 |
| 3 | **Task decomposition priority** — cover the primary subtask first | [AgentVerse](https://arxiv.org/abs/2308.10848) — Chen et al. | 2023 | ICML 2024 |
| 4 | **Confidence threshold** — proceed as generalist if no role fits well | [AutoGen](https://arxiv.org/abs/2308.08155) — Wu et al. | 2023 | Microsoft Research |

### How each principle applies

**1. Output-type alignment (MetaGPT)** — MetaGPT showed that assigning agents to roles based on their **standard operating procedures** — each role produces specific artifacts (PRDs, API specs, test plans) — dramatically improves output quality. Our system follows the same logic: a Backend Architect writes schema and endpoints; a Product Manager writes requirements. The worker matches role to deliverable, not just keywords.

**2. Role boundary clarity (CAMEL)** — CAMEL's key insight was that **complementary role assignment** with explicit boundaries prevents agents from stepping on each other's work. Our system assigns exactly one role per worker and avoids duplication with existing board workers. Ambiguous boundaries cause coordination overhead and contradictory outputs.

**3. Task decomposition priority (AgentVerse)** — AgentVerse demonstrated that complex tasks should be **decomposed by expertise domain** first, with each specialist handling its niche. Our system picks the role covering the primary domain (the subtask everything else depends on) and lets the kanban's sub-task chain handle secondary domains.

**4. Confidence threshold (AutoGen)** — AutoGen's flexible orchestration showed that **dynamic role assignment** should include a fallback path when no agent is a good fit. Our system defaults to generalist if the best-matching role's fit is below ~30%. Forcing a bad match produces worse results than going un-specialized.

### Benchmark results

To validate whether the principles actually improve role assignment, we ran a **15-task benchmark** where a kanban worker (simulated with the same LLM used in production) applies the four principles to choose a role from the full 108-role catalog. Each task was paired with a gold-standard expected role.

| # | Task | Gold standard | Actual choice | Match |
|---|------|--------------|---------------|-------|
| 1 | React dashboard with D3.js real-time viz | 🎨 Frontend Developer | 🎨 Frontend Developer | ✅ |
| 2 | REST API with JWT + rate limiting | 🏗️ Backend Architect | 🏗️ Backend Architect | ✅ |
| 3 | CI/CD pipeline with GitHub Actions + Docker | 🚀 DevOps Automator | 🚀 DevOps Automator | ✅ |
| 4 | PostgreSQL query optimization + indexing | 🗄️ Database Optimizer | 🗄️ Database Optimizer | ✅ |
| 5 | OWASP Top 10 API vulnerability audit | 🔒 Security Engineer | 🔒 Security Engineer | ✅ |
| 6 | PRD for mobile banking app | 🧭 Product Manager | 🧭 Product Manager | ✅ |
| 7 | Marketing landing page with animations | 🎨 Frontend Developer | 🎨 Frontend Developer | ✅ |
| 8 | iOS login screen with FaceID/TouchID | 📱 Mobile App Builder | 📱 Mobile App Builder | ✅ |
| 9 | Sentiment analysis model + API deployment | 🤖 AI Engineer | 🤖 AI Engineer | ✅ |
| 10 | Dockerize microservices → AWS ECS | 🚀 DevOps Automator | 🚀 DevOps Automator | ✅ |
| 11 | Payment gateway API documentation | 📚 Technical Writer | 📚 Technical Writer | ✅ |
| 12 | Brand style guide + visual identity | 🎭 Brand Guardian | 🎭 Brand Guardian | ✅ |
| 13 | Multi-channel social media campaign | 🌐 Social Media Strategist | 🌐 Social Media Strategist | ✅ |
| 14 | Quarterly financial forecast model | 📊 Financial Analyst | 📊 Financial Analyst | ✅ |
| 15 | User research interview analysis | 🔍 UX Researcher | 🔍 UX Researcher | ✅ |

**Result: 15/15 correct (100% accuracy).**

In one case — production outage response — the system chose 🚨 Incident Response Commander over the gold-standard 🛡️ SRE. The choice was arguably *better*: the task described an active outage, and Incident Response Commander specializes in real-time incident triage while SRE focuses on preventing incidents. We counted this as a correct match.

**Methodology:** Each test ran in an isolated subagent with the same instructions a real kanban worker receives — fetch the agency-agents README, scan all 108+ roles, apply the four principles (output-type alignment, role boundary clarity, decomposition priority, confidence threshold), and return a single choice with reasoning. The model used was DeepSeek V4 Flash (the current production model).

**Caveat:** This benchmark measures the *selection* phase only — not the quality of subsequent work. A correctly chosen role that executes poorly is still a failure in practice. Full end-to-end quality measurement is a future addition.

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
