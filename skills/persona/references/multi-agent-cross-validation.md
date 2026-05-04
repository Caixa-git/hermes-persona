# Multi-Agent Cross-Validation — Parallel Workers with Consensus Tracking

## Overview

Multi-agent cross-validation runs N parallel workers on the same task, each
adopting a different specialist role. Their outputs are collected by an
orchestrator and synthesized into a unified result with explicit consensus
and disagreement tracking.

This technique catches blind spots that a single specialist would miss — a
Security Engineer focuses on vulnerabilities while a Backend Architect evaluates
the architecture, and the orchestrator reconciles the two perspectives.

## Workflow

```
┌──────────────────────────────────────────────────────────┐
│  Orchestrator Worker                                     │
│  - Creates N child tasks with different role focuses     │
│  - Waits for all children to complete                    │
│  - Collects and synthesizes results                      │
│  - Produces consensus/disagreement matrix                │
└─────┬────────────────────────┬───────────────────────────┘
      │                        │
      ▼                        ▼
┌──────────┐             ┌──────────┐
│ Worker A │             │ Worker B │      ... Worker N
│ Role: 🔒 │             │ Role: 🏗️ │
│ Focus:   │             │ Focus:   │
│ Security │             │ Arch     │
└──────────┘             └──────────┘
```

## Running a Cross-Validation

### Step 1: Orchestrator Setup

The orchestrator creates N child tasks, each with a specific focus. The task
body should describe the same system/codebase from different perspectives.

```bash
hermes kanban create 'Cross-validate: API authentication system' \
  --body 'Run cross-validation on the JWT auth system' \
  --skill persona \
  --assign persona-worker
```

### Step 2: Child Tasks with Focused Roles

```python
# Inside the orchestrator (adopts 🎭 Agents Orchestrator or proceeds as generalist)
kanban_create(
    title="[Security] JWT auth system review",
    assignee="persona-worker",
    body="Review JWT auth system for security vulnerabilities...",
    skills=["persona"],
    parents=[parent_id],
)

kanban_create(
    title="[Architecture] JWT auth system review",
    assignee="persona-worker",
    body="Review JWT auth system architecture and scalability...",
    skills=["persona"],
    parents=[parent_id],
)

kanban_create(
    title="[Performance] JWT auth system review",
    assignee="persona-worker",
    body="Review JWT auth system performance bottlenecks...",
    skills=["persona"],
    parents=[parent_id],
)
```

### Step 3: Parallel Execution

When all parents are ready, the dispatcher spawns workers for each child
simultaneously (up to `max_concurrent_workers`). Each worker independently
adopts a role matching its focus area.

### Step 4: Synthesis

The orchestrator collects all child results and produces a synthesis.

## Consensus Tracking

After collecting results, the orchestrator creates a consensus matrix:

| Finding | Worker A (🔒) | Worker B (🏗️) | Worker C (⚙️) | Consensus |
|---------|-------------|-------------|-------------|-----------|
| JWT secret hardcoded | ✅ Found | ✅ Found | ❌ Not in scope | ✅ Consensus |
| Token refresh missing | ✅ Found | ✅ Found | ✅ Found | ✅ Consensus |
| Rate limiting needed | ❌ Not focus | ✅ Raised | ✅ Raised | ⚠️ Partial |
| Cache strategy absent | ❌ Not focus | ❌ Not focus | ✅ Raised | ❌ Single |

**Consensus levels:**

| Level | Definition | Action |
|-------|-----------|--------|
| ✅ Full consensus | 2+ workers independently identified the same issue | High priority |
| ⚠️ Partial | Some workers agree, others out of scope | Medium priority |
| ❌ Single | Only one worker found it (possibly narrow focus) | Review and triage |
| 🚨 Disagreement | Workers actively contradicted each other | Escalate to human |

## Disagreement Resolution

When workers disagree:

1. **Check role scope.** Is the disagreement because one role's focus area
   doesn't cover the issue? (Expected — Security Engineer doesn't evaluate
   CSS framework choices.)

2. **Verify evidence.** Does each worker cite code evidence for its position?
   Unexplained opinions are less reliable.

3. **Escalate real contradictions.** If one worker says "use Redis" and another
   says "use Postgres for that data," document both positions with trade-offs
   and escalate for human decision.

## Practical Scenarios

### Code Review Cross-Validation

| Worker | Role | Focus |
|--------|------|-------|
| A | 🔒 Security Engineer | Vulnerabilities, injection, auth |
| B | 🏗️ Backend Architect | Design, coupling, data flow |
| C | 👁️ Code Reviewer | Style, maintainability, tests |

### Deployment Readiness Review

| Worker | Role | Focus |
|--------|------|-------|
| A | ⚙️ DevOps Automator | CI/CD, infrastructure, monitoring |
| B | 🔒 Security Engineer | Secrets, network policies, audit |
| C | 🛡️ SRE | SLOs, error budgets, capacity |

## Limitations

| Limitation | Mitigation |
|------------|------------|
| **Cost.** N workers = N× LLM calls | Keep N small (2-4). Use Flash-tier models for workers. |
| **Latency.** Sequential if `max_concurrent_workers` < N | Increase parallelism. Each worker takes 3-15 min. |
| **Overlapping findings.** Workers may duplicate work | Deduplicate in the synthesis step. |
| **Role misalignment.** Worker may adopt wrong role for its focus | Set explicit body guidance per child task. |
| **Not for urgent fixes.** Cross-validation is slower than single-worker | Use for high-stakes changes only. |
