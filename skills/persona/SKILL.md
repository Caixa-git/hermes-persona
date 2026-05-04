---
name: persona
description: "🎭 Expert role adoption for Hermes Agent kanban workers — every task auto-assigns the best-fitting specialist role from a catalog of 172"
tags:
  - hermes-agent
  - kanban
  - role-adoption
  - persona
  - agency-agents
related_skills:
  - hermes-agent
  - kanban-orchestrator
  - kanban-worker
---

# 🎭 persona — expert role adoption for kanban workers

## What it is

A skill-based role adoption system for Hermes Agent kanban workers. When a worker is spawned with `--skill persona`, it dynamically adopts the best-fitting specialist role from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog (~172 roles across 15 categories).

Each worker:
1. Fetches the agency-agents catalog from GitHub raw (pinned commit `783f6a72`)
2. Scans ~172 roles
3. Picks the best-fitting specialist for its task using 4 research-backed principles
4. Announces adoption via `kanban_heartbeat(note="🎭 Role adopted: 🏗️ Role Name")`
5. Loads the role's full specification
6. Works as that specialist

**Persona is opt-in.** A worker without `--skill persona` proceeds as a plain generalist.

## Activation

### Single task with persona

```bash
hermes kanban create 'Build JWT auth API' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

### Chat session with persona loaded

```bash
hermes -s persona chat
# Then create tasks normally — persona is in context
```

### Without persona (default)

```bash
hermes kanban create 'Build JWT auth API'
hermes kanban assign t_xxxx default
hermes kanban dispatch
# → Worker proceeds as generalist, no role adoption
```

## Child task propagation

When a persona worker decomposes work into child tasks, it **must pass** `skills=['persona']` to `kanban_create()` so child workers also adopt specialist roles.

```python
kanban_create(
    title="Frontend: React storefront",
    assignee="persona-worker",
    body="...",
    skills=["persona"],  # ← required for chain propagation
    parents=[parent_task_id],
)
```

Without `skills=["persona"]`, child workers run as generalists.

### Verified: chain propagation works

Tested with an e-commerce decomposition task:

| Level | Task | Role adopted | Status |
|-------|------|-------------|--------|
| Parent | E-commerce decomposer | 🎭 Agents Orchestrator | ✅ |
| Child 1 | Frontend: React storefront | 🎨 Frontend Developer | ✅ |
| Child 2 | Backend: Payment API | 🏗️ Backend Architect | ✅ |
| Child 3 | DevOps: CI/CD pipeline | ⚙️ DevOps Automator | ✅ |

See `references/chain-propagation-test.md` for full test transcript.

## Usage workflow

### Standard interaction pattern

```bash
# 1. Create task with --skill persona
hermes kanban create '[M1] Add SHA256 checksum' \
  --body 'Fix from audit: add SHA256 checksum to install.sh' \
  --skill persona

# 2. Assign to persona-worker profile
hermes kanban assign t_xxxx persona-worker

# 3. Dispatch
hermes kanban dispatch
```

**Batch related fixes** into one task to reduce total runtime. **Keep unrelated fixes separate** so each worker focuses on its domain.

### Verifying adoption

```bash
hermes kanban show <task_id> | grep heartbeat
# → [timestamp] heartbeat {'note': '🎭 Role adopted: 🏗️ Backend Architect'}
```

### Multi-worker parallelism

Dispatch spawns one worker per ready+assigned task in a single pass:

```bash
hermes kanban dispatch
# Spawned: 2
#   - t_xxx  ->  persona-worker
#   - t_yyy  ->  persona-worker
```

## Installation

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer:
1. Creates `~/.hermes/skills/persona/SKILL.md` — the worker-facing persona skill
2. Enables `kanban` toolset in `~/.hermes/config.yaml`
3. Generates `install.sh.sha256` for integrity verification (two-step install: `sha256sum -c install.sh.sha256 && bash install.sh`)

**No KANBAN_GUIDANCE patching.** Persona activates through `--skill persona`, not through unconditional system prompt injection.

## Git Flow requirement (repo work)

All work on the hermes-persona repository **must** follow Git Flow:

```
main       → production-ready
develop    → integration branch
fix/*      → bug fixes
feature/*  → features
release/*  → releases
hotfix/*   → urgent fixes
```

Procedure:
1. Branch from `develop`: `git checkout -b fix/xyz develop`
2. Work and commit on the branch
3. Push: `git push origin fix/xyz`
4. Create PR to `develop`
5. Merge to `main` only after `develop` is stable

No direct commits to `main` or `develop`. Every merge requires a PR.

## Pitfalls & operational notes

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Worker timeout (10 min default)** | Worker disappears mid-task; dispatcher auto-restarts | Set `--max-runtime 30m` for long audits |
| **Scratch workspace isolation** | `search_files` returns nothing (scratch dir is empty) | Use `read_file` with absolute paths or `terminal(command='cd /repo && ...')` |
| **Unassigned == skipped** | `Skipped (unassigned): t_xxx` in dispatch output | Always `assign` before `dispatch` |
| **Worker writes file mid-execution** | Report file appears before task shows `completed` | Check file existence periodically, not just on completion |
| **Duplicate workers from restart** | Two PIDs for same task after timeout | Original terminates; relaunched worker continues |
| **`delegate_task()` bypasses persona** | Worker runs as generic Hermes | Use `kanban create` for domain tasks; `delegate_task` for quick lookups |
| **Child task missing persona** | Child worker runs as generalist | Pass `skills=['persona']` in `kanban_create()` |
| **`--skill persona` omitted** | Worker has no persona instructions | Always include `--skill persona` in `kanban create` when persona is needed |

### Timing benchmarks (real session data)

| Session | Tasks | Duration avg | Notes |
|---------|-------|-------------|-------|
| Security audit (read-only) | 1 | ~6 min | Inspect + report write |
| Single-file fix | 2 | ~5 min | One-line changes |
| Two-file fix + references | 2 | ~15 min (with restart) | 315-line diff |
| Multi-remediation (3 fixes) | 3 (parallel) | ~13 min | 350-line diff, SHA256 gen |
| Chain propagation test | 1 parent → 3 child | ~3 min per child | All adopted roles |

Plan ~15 min per task. Batch simple fixes to reduce total time.

## References

See `references/` in this skill directory for:
- `kanban-guidance-patch.md` — exact patch text added to KANBAN_GUIDANCE (legacy, pre-opt-in design)
- `role-url-patterns.md` — GitHub raw URL construction for all 15 categories
- `benchmark-methodology.md` — 15-task benchmark design, results (15/15 correct), and caveats
- `security-audit-methodology.md` — Step-by-step audit workflow using 🔒 Security Engineer persona
- `kanban-dispatch-setup.md` — Profile creation, config setup, dispatcher configuration
- `chain-propagation-test.md` — Verified test: persona propagates from parent to child tasks

## Design decisions

| Decision | Rationale |
|----------|-----------|
| Opt-in via `--skill persona` | Default workers are generalists. Persona only on explicit request. |
| Git raw URLs instead of clone | Zero local storage. No pull/update needed. Always fresh. |
| Pinned commit (`783f6a72`) | Prevents upstream compromise from injecting malicious role specs |
| Emoji in heartbeat | Visually scannable in kanban event logs |
| Skill injection over system patch | No hermetic agent source modification. Cleaner install/uninstall. |
| `skills` param for propagation | Child tasks get persona only when parent explicitly passes it |

## Scope / Limitations

### Persona only works on the kanban execution path

Hermes Agent has **two parallel execution paths** for delegating work:

| Path | API | Persona? |
|------|-----|----------|
| Kanban orchestration | `kanban_create` → worker spawn | ✅ With `--skill persona` |
| Native Hermes delegation | `delegate_task()` | ❌ No persona |

`delegate_task()` does not go through the kanban prompt pipeline. One-off information checks → `delegate_task` (fast). Complex domain work → `kanban_create --skill persona` (expert).

### Persona requires the persona profile

The `persona-worker` profile (or any profile with `OPENAI_API_KEY` set and a capable model) is recommended. The skill alone doesn't guarantee good results — the underlying model must be capable of role adoption. GPT-4o and DeepSeek-V4 have been tested.

## Role selection principles (research-backed)

### 1. Output-type alignment
**Source:** MetaGPT (Hong et al., ICLR 2024)
Each specialist role has a canonical output artifact. The worker picks the role whose standard deliverable matches the task. A Backend Architect writes API specs — if the task is a PRD, pick Product Manager instead.

### 2. Role boundary clarity
**Source:** CAMEL (Li et al., NeurIPS 2023)
Exactly one role with clear, non-overlapping responsibilities. Avoid duplicating roles already on the board.

### 3. Task decomposition priority
**Source:** AgentVerse (Chen et al., ICML 2024)
Pick the role covering the primary domain (the subtask everything else depends on). The kanban chain handles the rest.

### 4. Confidence threshold
**Source:** AutoGen (Wu et al., Microsoft Research, 2023)
If no role's fit exceeds ~30%, proceed as generalist. Forcing a bad match harms output quality.

## Edge cases

| Case | Behavior |
|------|----------|
| No matching role | Worker proceeds as generalist |
| Multiple roles match | Worker picks single best fit from README table |
| GitHub raw unavailable | Worker cannot fetch catalog → generalist fallback |
| Task is trivial | Worker scans; most trivial tasks match no specialist → generalist |
| `--skill persona` omitted | Worker has no persona instructions → generalist |
| Child created without `skills=['persona']` | Child runs as generalist |
| Parallel work via `delegate_task()` | Persona does NOT activate |
| `hermes -z` (oneshot) | Main agent exits before workers finish. Use `hermes chat`. |

## Project repo

https://github.com/Caixa-git/hermes-persona
