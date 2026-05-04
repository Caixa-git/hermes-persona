# Chain Propagation Test — Persona from Parent to Child Tasks

## Overview

This document records the verified test proving that the persona skill correctly
propagates from a parent kanban task to its child tasks. When a worker operating
under `--skill persona` decomposes work via `kanban_create()`, child workers
must also adopt specialist roles — provided the parent passes `skills=['persona']`.

## Test: E-Commerce Decomposition

### Setup

A parent task titled "E-commerce decomposer" was dispatched with `--skill persona`
to the `persona-worker` profile. The parent adopted the 🎭 Agents Orchestrator
role and created three child tasks, each with `skills=['persona']`:

```python
kanban_create(
    title="Frontend: React storefront",
    assignee="persona-worker",
    skills=["persona"],
    parents=[parent_task_id],
)
```

### Result

| Level | Task | Role Adopted | Status |
|-------|------|-------------|--------|
| Parent | E-commerce decomposer | 🎭 Agents Orchestrator | ✅ |
| Child 1 | Frontend: React storefront | 🎨 Frontend Developer | ✅ |
| Child 2 | Backend: Payment API | 🏗️ Backend Architect | ✅ |
| Child 3 | DevOps: CI/CD pipeline | ⚙️ DevOps Automator | ✅ |

All three children independently scanned the agency-agents catalog (pinned to
commit `783f6a72`), picked the best-fitting role for their specific task, and
announced adoption via `kanban_heartbeat(note="🎭 Role adopted: ...")`.

## Propagation mechanism

1. **Parent task** is created with `--skill persona`:
   ```bash
   hermes kanban create 'E-commerce decomposer' --skill persona --assign persona-worker
   ```

2. **Parent worker** loads the persona skill, adopts a role, and begins work.

3. **Parent decomposes** the task into sub-tasks using `kanban_create()` with
   `skills=['persona']` in the call. This is the critical step — without this
   parameter, child workers receive no persona guidance.

4. **Dispatcher picks up** child tasks from the kanban board, sees
   `skills=['persona']`, and spawns workers with `--skill persona` injected.

5. **Each child worker** independently runs the role-adoption protocol: fetch
   the agency-agents catalog, apply the 4 research-backed principles, and
   announce the role.

## Failure modes

### Missing `skills=['persona']`

If the parent creates child tasks without passing `skills=['persona']`:

```python
kanban_create(
    title="Frontend: React storefront",
    assignee="persona-worker",
    parents=[parent_task_id],
    # No skills parameter → child gets NO persona guidance
)
```

The child spawns without `--skill persona` and proceeds as a **generalist**.
No role adoption occurs. The child never even sees the persona protocol.

### Using `delegate_task()` instead of `kanban_create()`

`delegate_task()` bypasses the kanban prompt pipeline entirely. It spawns a
subagent in a separate context that never touches the persona skill or the
kanban board. Persona is a **kanban-only** feature.

### Verification

```bash
# Check that a child task adopted a role
hermes kanban show <child_task_id> | grep heartbeat
# → [timestamp] heartbeat {'note': '🎭 Role adopted: 🎨 Frontend Developer'}

# Confirm child has persona loaded
hermes kanban show <child_task_id> | grep skills
# → skills: {'persona'}
```

## Design notes

- **Opt-in by design.** Persona propagation requires explicit `skills=['persona']`
  at every level. This prevents accidental activation of role adoption on tasks
  where generalist behavior is appropriate.
- **Each level re-evaluates independently.** A child task does not inherit the
  parent's role. It re-scans the full agency-agents catalog and picks the best
  role for its own task body.
- **Pinned catalog.** All fetches use commit `783f6a72` of the agency-agents
  repository. This ensures deterministic role selection regardless of upstream
  changes.
