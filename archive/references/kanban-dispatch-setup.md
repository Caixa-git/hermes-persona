# Kanban Dispatch Setup — Profile Creation & Configuration

## Overview

This guide covers how to set up the persona kanban dispatch pipeline from
scratch: creating the `persona-worker` profile, configuring the dispatcher,
and running your first persona task.

## Prerequisites

- Hermes Agent installed (v0.12.0+)
- An API key for a capable LLM provider (OpenAI, DeepSeek, Anthropic, etc.)
- Git for repository-based tasks

## Step 1: Install the Persona Skill

```bash
# Two-step install for integrity verification
curl -sSLO https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh
curl -sSLO https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh.sha256
sha256sum -c install.sh.sha256
# → install.sh: OK

# Run the installer
bash install.sh
```

The installer:
1. Creates `~/.hermes/skills/persona/SKILL.md` — the persona skill definition
2. Enables the `kanban` toolset in `~/.hermes/config.yaml`
3. Generates `install.sh.sha256` for future verification
4. Does **not** patch any Hermes Agent source files — persona is skill-based

### Verify installation

```bash
ls -la ~/.hermes/skills/persona/SKILL.md
# → Should exist and be readable

grep "kanban" ~/.hermes/config.yaml
# → Should show kanban in toolsets list
```

## Step 2: Create the Persona-Worker Profile

Create a profile directory and config file:

```bash
mkdir -p ~/.hermes/profiles/persona-worker
```

```yaml
# ~/.hermes/profiles/persona-worker/config.yaml
model: deepseek-v4-flash     # Flash-tier model for workers
toolsets:
  - terminal
  - file
  - kanban
  - web
  - search
  - session_search
  - skills

providers:
  deepseek:
    api_key_env: DEEPSEEK_API_KEY
```

### Environment variables

Set the API key for your chosen provider:

```bash
export DEEPSEEK_API_KEY=sk-...
# Or add to ~/.zshrc / ~/.bashrc for persistence
```

### Profile verification

```bash
hermes config --profile persona-worker
```

## Step 3: Configure the Dispatcher

Configure the kanban dispatcher in your main Hermes config:

```yaml
# ~/.hermes/config.yaml
model: deepseek/deepseek-v4    # Pro-tier model for dispatcher

kanban:
  enabled: true
  poll_interval_seconds: 60
  max_concurrent_workers: 3
  max_runtime_seconds: 600

toolsets:
  - kanban
```

## Step 4: Run Your First Persona Task

```bash
# Create a task with persona enabled
hermes kanban create 'Security audit: check file permissions' \
  --body 'Review all scripts in the repo for 755 executable permissions and unsafe umask values' \
  --skill persona

# Note the task ID from output (e.g., t_abc12345)

# Assign to the persona-worker profile
hermes kanban assign t_abc12345 persona-worker

# Dispatch
hermes kanban dispatch
```

Expected output:

```
Dispatching...
  t_abc12345 → persona-worker (--skill persona)

Task t_abc12345: running
Worker spawned (PID: 12345)
```

Check results:

```bash
hermes kanban show t_abc12345
# → Shows status, heartbeat with role adoption, completion
```

## Step 5: Verify Role Adoption

```bash
hermes kanban show t_abc12345 | grep heartbeat
# → [timestamp] heartbeat {'note': '🎭 Role adopted: 🔒 Security Engineer'}

hermes kanban show t_abc12345 | grep "status: done"
# → status: done (or running, or blocked)
```

## Configuration Reference

### Profile settings

| Setting | Default | Recommended for persona |
|---------|---------|------------------------|
| `model` | (none) | `deepseek-v4-flash` or `gpt-4o-mini` |
| `toolsets` | `[terminal]` | `[terminal, file, kanban, web, search, session_search, skills]` |
| `providers` | (inherits main) | Provider matching your API key |

### Dispatcher settings

| Setting | Default | Description |
|---------|---------|-------------|
| `kanban.enabled` | `false` | Must be `true` for dispatch to work |
| `poll_interval_seconds` | `60` | How often dispatcher checks the board |
| `max_concurrent_workers` | `3` | Parallel task limit |
| `max_runtime_seconds` | `600` | Per-task timeout before SIGTERM |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Skipped (unassigned): t_xxx` | Task not assigned to any profile | Run `hermes kanban assign t_xxx persona-worker` |
| Worker spawns but produces no output | Missing API key | Check `DEEPSEEK_API_KEY` env var in profile config |
| `Skill not found: persona` | Persona skill not installed | Run `bash install.sh` from the hermes-persona repo |
| `kanban` tool not available | `kanban` not in toolsets | Add `kanban` to `~/.hermes/config.yaml` toolsets |
| Child runs as generalist | Missing `skills=['persona']` | Add `skills=['persona']` to `kanban_create()` |
