# Dispatcher–Worker Architecture — Model Hierarchy & Configuration

## Overview

The Hermes kanban system uses a two-layer model architecture:

```
┌─────────────────────────────────────────────┐
│  Dispatcher (Pro-tier model)                │
│  - Scans the board for ready tasks          │
│  - Spawns workers                           │
│  - Tracks lifecycle (claimed/running/done)  │
│  - Telemetry: 3-5 sec / dispatch cycle      │
│                                             │
│  Config: ~/.hermes/config.yaml              │
│  Model: deepseek/deepseek-v4 (Pro-tier)     │
├─────────────────────────────────────────────┤
│  Worker (Flash-tier model)                  │
│  - Executes a single kanban task            │
│  - Runs persona role adoption (if enabled)  │
│  - Has full tool access (terminal, files)   │
│  - Telemetry: 3-15 min / task                │
│                                             │
│  Config: ~/.hermes/profiles/<profile>/.hermes/config.yaml  │
│  Model: deepseek-v4-flash (Flash-tier)      │
└─────────────────────────────────────────────┘
```

## Dispatcher Layer (Pro-tier)

### Role

The dispatcher is a lightweight supervisor that runs on a fast, capable model.
It does **not** execute tasks — it reads the kanban board, checks which tasks
are ready and assigned, and spawns worker processes.

### Configuration

```yaml
# ~/.hermes/config.yaml
model: deepseek/deepseek-v4                # Pro-tier model
kanban:
  enabled: true
  poll_interval_seconds: 60                # How often to check the board
  max_concurrent_workers: 3                # Parallelism cap
  max_runtime_seconds: 600                 # Default 10-min timeout per task
```

### Responsibilities

- Read the kanban SQLite board (`~/.hermes/kanban.db`)
- Identify tasks with `status='ready'` matching the profile
- Verify `max_concurrent_workers` is not exceeded
- Spawn worker processes with the correct profile and skills
- Track worker lifecycle (PID, start time, heartbeat)
- Handle timeouts and crashes (re-queue with `outcome='timed_out'`)

## Worker Layer (Flash-tier)

### Role

Workers execute individual kanban tasks. Each worker is an isolated process
with its own terminal session, working directory, and tool access.

### Configuration

```yaml
# ~/.hermes/profiles/persona-worker/config.yaml
model: deepseek-v4-flash                    # Flash-tier model
toolsets: [terminal, file, web, kanban, search, session_search, skills]
providers:
  deepseek:
    api_key_env: DEEPSEEK_API_KEY
```

### Lifecycle

1. **Spawned** by dispatcher with task id, workspace path, and skills list
2. **Orients** via `kanban_show()` — reads task body, prior attempts, comments
3. **Adopts persona** (if `--skill persona` was passed in skills)
4. **Works** the task — calls tools, modifies files, writes to workspace
5. **Completes** via `kanban_complete(summary=..., metadata=...)`
6. **Times out** if exceeding `max_runtime_seconds` — dispatcher SIGTERMs

## `delegate_task` Ban on Dispatcher

The dispatcher must **never** use `delegate_task()`. Rationale:

| Why | Explanation |
|-----|------------|
| **Board is the source of truth** | `delegate_task` spawns ephemeral subagents outside the kanban board. No visibility, no audit trail. |
| **No persistence** | Subagent results vanish if the parent process is interrupted. Kanban tasks survive restarts. |
| **No persona** | `delegate_task` subagents do not run through the persona pipeline. No role adoption. |
| **No parallelism control** | `delegate_task` spawns outside the kanban's `max_concurrent_workers` cap. |

### Exception: Worker → `delegate_task`

Workers **may** use `delegate_task` for brief reasoning subtasks during their
own execution — e.g., fetching a spec, looking up a definition, or validating
a small piece of logic. But `delegate_task` is NOT a substitute for
`kanban_create` when durable, cross-agent work is needed.

## Model Selection Guidelines

### Dispatcher (Pro-tier)

| Model type | Use case |
|------------|----------|
| GPT-4o | Best for complex dispatch logic, large boards |
| DeepSeek-V4 | Fast dispatch, good value |
| Claude 3.5 Sonnet | Reliable, good for production |

### Worker (Flash-tier)

| Model type | Use case |
|------------|----------|
| DeepSeek-V4 Flash | Default persona worker — fast, cost-effective |
| GPT-4o Mini | Coding tasks, file manipulation |
| Claude 3.5 Haiku | Quick lookups, simple tasks |

## Telemetry

```
Dispatcher: 3-5 sec per dispatch cycle
Worker:     3-15 min per task (typical)
Worker:     30+ min for audits, large code reviews
```
