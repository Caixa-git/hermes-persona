# 🎭 hermes-persona

**Specialist role adoption system for [Hermes Agent](https://hermes-agent.nousresearch.com)**

Hermes Persona bridges [Hermes Agent](https://github.com/NousResearch/hermes-agent)'s kanban task workers with [agency-agents](https://github.com/msitarzewski/agency-agents)'s 210+ expert role definitions.

---

## How it works

```
kanban worker spawns
  → loads persona skill (--skill persona)
  → curl GitHub raw → agency-agents/README.md
  → analyzes task ↔ 210+ role catalog
  → picks the best-fitting expert role
  → loads that role's full .md specification
  → becomes that specialist for the task
```

**Zero local storage.** No clones, no pulls. Pure GitHub raw URLs.

## Usage

```bash
# Install
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)

# Use
hermes kanban create 'Build a REST API with JWT auth' --skill persona
# → Worker automatically picks "Backend Architect"
```

## What's inside

| Path | Description |
|------|-------------|
| `skills/persona/SKILL.md` | Hermes Agent skill — worker loads this to adopt a role |
| `install.sh` | One-command installer |

## Shoutouts

### [agency-agents](https://github.com/msitarzewski/agency-agents) by msitarzewski 🏆

> A complete AI agency at your fingertips — From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables.

210+ meticulously crafted specialist role definitions across 17 domains. The heart of the persona system.

### [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research 🏆

> The self-improving AI agent built by Nous Research. Multi-agent orchestration with kanban-based task distribution and skill injection. Runs on a $5 VPS, GPU cluster, or serverless infrastructure.

The runtime that makes role adoption practical — workers spawn with persona skills, read task context, and execute as specialists.

---

## Roadmap

- [x] Basic role adoption — README scan + .md load
- [ ] **Intelligent role selection** — task analysis using agent/occupational psychology research to pick the optimal role
- [ ] Multi-role composition — split tasks across complementary specialists
- [ ] Role performance feedback loop

---

🎭 *Pick your mask. Become the expert.*
Created by [Caixa-git](https://github.com/Caixa-git)
