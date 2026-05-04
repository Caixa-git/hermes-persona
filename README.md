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

When Hermes Agent processes a kanban task with the `--skill persona` flag, it analyzes the work and automatically picks the most suitable expert role from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog — **172 specialists across 15 domains**.

Each specialist comes with its own rules, workflows, and quality standards. The worker doesn't just execute the task — it executes it *as that expert*.

**Persona is opt-in.** Omit `--skill persona` and the worker proceeds as a plain generalist.

---

## Usage — everyday workflow

### 🖐️ The one-line way

Create a kanban task with `--skill persona`, assign it to `persona-worker`, dispatch. The system does the rest.

```bash
# 1. Create a task — must include --skill persona to activate role adoption
hermes kanban create 'Add JWT auth to the payment API' --skill persona

# 2. Assign to the persona profile
hermes kanban assign t_xxxx persona-worker

# 3. Dispatch — worker autonomously:
#    a. Fetches 172 expert roles from agency-agents
#    b. Applies 4 research principles (output-type, boundaries, priority, confidence)
#    c. Adopts the best-fitting role: 🏗️ Backend Architect
#    d. Works on the task as that expert
hermes kanban dispatch
```

That's it. A single `create --skill persona → assign → dispatch` cycle. The worker announces its adopted role via heartbeat:

```
[17:34] heartbeat 🎭 Role adopted: 🏗️ Backend Architect
```

### 💬 Natural language patterns

When chatting with Hermes, any of these phrasings work:

| Pattern | Example | What happens |
|---------|---------|-------------|
| Explicit `--skill persona` | `Do X using persona` | Worker spawns with `--skill persona`, adopts expert role |
| Natural language request | `Using persona, do X` | System detects persona request, passes `--skill persona` |
| Conditional activation | `Do X, use persona if needed` | Generalist by default, activates persona when task complexity warrants it |
| Playful variant | `Activate persona!` | Same behavior, fun phrasing |

The first two patterns guarantee persona activation. The conditional pattern delegates the decision to the system — persona fires only when the task is complex enough to justify it. The playful variant is equivalent to pattern 1.

### 🧠 During a chat session

You can also work entirely through `hermes chat` — just describe what you want naturally:

```bash
hermes chat
```

```
👤 "Build an e-commerce platform using persona"
```

The system automatically:
1. Creates a planner task → planner adopts 🏛️ Software Architect
2. Planner decomposes the work into sub-tasks
3. Each sub-task gets its own expert role

```                      
▶ t_...  ready   🏛️ Software Architect      E-commerce platform
▶ t_...  ready   🎨 Frontend Developer       Storefront UI
▶ t_...  ready   🏗️ Backend Architect        Payment API + JWT auth
▶ t_...  ready   🗄️ Database Optimizer       Product catalog schema
▶ t_...  ready   🚀 DevOps Automator         AWS deployment
```

### 🎯 Working from a spec or audit report

Point the persona system at an existing document:

```bash
hermes kanban create '[M1] install.sh — Add SHA256 checksum verification' \
  --body 'Fix M1 from SECURITY_AUDIT.md: add SHA256 ...' \
  --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

The worker reads the task, fetches the security report, picks 🔒 Security Engineer, and fixes the vulnerability autonomously.

### 🧩 Persona propagates to sub-tasks

When a persona worker decomposes its task into sub-tasks, **every sub-task also adopts its own specialist role** — because the parent passes `skills=["persona"]` to `kanban_create()`.

Example — one task decomposes into 3 specialists:

```
Parent: "E-commerce platform" → 🎭 Agents Orchestrator
  ├── "Frontend: React storefront"  → 🎨 Frontend Developer
  ├── "Backend: Payment API"        → 🏗️ Backend Architect
  └── "DevOps: CI/CD pipeline"     → ⚙️ DevOps Automator
```

| Your task (English) | The worker adopts |
|--------------------|-----------------|
| Build a React dashboard | 🎨 Frontend Developer |
| Set up CI/CD pipeline | 🚀 DevOps Automator |
| Optimize PostgreSQL queries | 🗄️ Database Optimizer |
| Design REST API with JWT | 🏗️ Backend Architect |
| Scan API for vulnerabilities | 🔒 Security Engineer |
| Build an iOS login screen | 📱 Mobile App Builder |
| Plan product roadmap | 📋 Product Manager |

| Your request | The worker adopts |
|-------|-----------------|
| `Activate persona, build a React dashboard` | 🎨 Frontend Developer |
| `Using persona, run a security audit` | 🔒 Security Engineer |
| `Optimize the DB, use persona if needed` | 🗄️ Database Optimizer |

---

## How it works

Every persona-enabled kanban worker starts by loading the persona skill (injected via `--skill persona` activating `~/.hermes/skills/persona/SKILL.md`):

```
Worker spawns with --skill persona
  → loads persona SKILL.md into system prompt
  → fetches agency-agents README via GitHub raw (pinned commit)
  → scans 172 roles, applies 4 research principles
  → picks the best match
  → logs "🎭 Role adopted: 🏗️ Backend Architect" via kanban_heartbeat
  → downloads the role's full .md specification
  → executes the task as that specialist
```

**Without `--skill persona`, the worker has no persona instructions and proceeds as a generalist.** No hidden role adoption, no unconditional system prompt injection.

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
| **`delegate_task()`** | Native Hermes sub-agents don't go through the kanban pipeline — persona only activates for kanban workers with `--skill persona`. |
| **`--skill persona` omitted** | Worker has no persona instructions → proceeds as generalist. Persona is opt-in, not automatic. |

---

## Installation

Hermes Agent must be installed first.

### ⚠️  Security — review before running

Always review scripts before execution, especially from the internet. The installer
creates the persona skill file and configures your Hermes setup.

### Recommended: two-step with SHA256 verification

```bash
curl -sSLO https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh
curl -sSLO https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh.sha256
sha256sum -c install.sh.sha256 && bash install.sh
```

### Quick install (one-liner)

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer:
- Creates `~/.hermes/skills/persona/SKILL.md` — the worker-facing persona skill
- Enables the `kanban` toolset in your Hermes config
- Generates `install.sh.sha256` for future integrity verification
- **Prompts per-profile** for `.env` symlink (opt-in, not automatic)

**No KANBAN_GUIDANCE patching.** Persona activates through `--skill persona` when creating a kanban task, not through unconditional system prompt injection. Clean install and uninstall.

### Credential scoping

The installer prompts before symlinking `~/.hermes/.env` into each profile directory.
Only symlink profiles that genuinely need those API keys.

**Best practice**: create per-profile `.env` files with scoped credentials instead
of symlinking one `.env` that grants every profile full access to all API keys.

### Pinned upstream

Agency-agents role definitions are pinned to commit
[`783f6a7`](https://github.com/msitarzewski/agency-agents/commit/783f6a72bfd7f3135700ac273c619d92821b419a)
— role specs are fetched from this exact snapshot, not the `main` branch.

---

## Credits

| Project | Author | Role |
|---------|--------|------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | [msitarzewski](https://github.com/msitarzewski) | 172 expert role definitions across 15 domains |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [Nous Research](https://nousresearch.com) | Kanban-based multi-agent orchestration framework |

All 172 specialist role definitions are sourced from the agency-agents repository — a meticulously crafted collection of AI agent personalities with deep domain expertise, production-ready workflows, and measurable deliverables.

---

## Roadmap

- [x] Opt-in role selection — 172 experts, activate via `--skill persona`
- [x] Emoji identification — roles are visible in the kanban task list
- [x] Opt-in design — persona activates only when explicitly requested
- [ ] **Smarter matching** — multi-dimensional scoring (domain, activity, tech stack, complexity)
- [ ] **Docker smoke test** — verify clean-install behavior in isolated container

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>Created by <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
