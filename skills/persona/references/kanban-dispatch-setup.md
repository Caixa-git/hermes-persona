# Kanban dispatch — profile setup & worker spawning

## The problem

Persona adoption happens inside **kanban workers** — processes spawned by the kanban dispatcher to process board tasks. Without a running gateway daemon (`hermes gateway start`), the dispatcher doesn't auto-spawn.

## Solution: manual dispatch pass

Even without the gateway, you can trigger a one-shot dispatch:

```bash
1. hermes kanban create "Build a REST API with JWT"
2. hermes kanban assign t_<id> <profile-name>    # e.g. persona-worker
3. hermes kanban dispatch                         # spawns worker, returns PID
```

The dispatcher runs `hermes -p <profile> --skills kanban-worker chat -q "work kanban task <id>"` as a subprocess. The worker reads KANBAN_GUIDANCE (persona section built-in), fetches agency-agents, picks a role, emits a heartbeat.

## Verify persona adoption

```bash
hermes kanban show t_<id>        # Check events — look for heartbeat
hermes kanban log t_<id>         # Full worker output
grep 'Role adopted'              # In show output: 🎭 Role adopted: 🏗️ Role Name
```

Example event sequence from a successful run:

```
[17:34] created
[17:34] assigned → persona-worker
[17:34] claimed  (run 9)
[17:34] spawned  (PID: 96773)
[17:34] heartbeat 🎭 Role adopted: 🏗️ Backend Architect
```

## Profile setup: .env inheritance

Worker profiles need API keys to run LLM inference. The kanban dispatcher sets `HERMES_HOME` to the profile directory before running the worker, so the profile must be able to find provider credentials.

**The fix**: symlink the main `.env` into the profile:

```bash
ln -sf ~/.hermes/.env ~/.hermes/profiles/<profile-name>/.env
```

Without this, the profile worker won't find `DEEPSEEK_API_KEY` (or whichever provider key is in use) and will fail with:

```
RuntimeError: Provider 'deepseek' is set in config.yaml but no API key was found.
```

## Profile creation

```bash
hermes profile create <name>            # e.g. persona-worker
# Creates ~/.hermes/profiles/<name>/ + wrapper script at ~/.local/bin/<name>
ln -sf ~/.hermes/.env ~/.hermes/profiles/<name>/.env   # API key inheritance
```

## Board hygiene

Old test tasks accumulate on the board. Clean them up:

```bash
# Archive stale ready tasks
hermes kanban list | grep '▶' | awk '{print $1}' | xargs hermes kanban archive

# Check stats
hermes kanban stats

# Remove archived workspace data
hermes kanban gc
```

## Full pipeline command sequence

```bash
# 1. Create profile (one-time setup)
hermes profile create persona-worker
ln -sf ~/.hermes/.env ~/.hermes/profiles/persona-worker/.env

# 2. Create and process a task
hermes kanban create "Design REST API with JWT auth"
# → copy task ID from output: t_<hex>

# 3. Assign to worker profile
hermes kanban assign t_<hex> persona-worker

# 4. Dispatch (spawns worker)
hermes kanban dispatch
# → Look for "Spawned: 1" in output

# 5. Wait ~10-20s, then verify
hermes kanban show t_<hex> | grep 'Role adopted'
# → Expected: 🎭 Role adopted: 🏗️ Backend Architect
```
