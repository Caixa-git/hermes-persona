# Docker Smoke Test — Persona in Clean Environment

## Purpose

Validate that the persona skill installs and functions correctly in a clean
Docker environment using `python:3.12-slim`. This tests:
1. `install.sh` portability across operating systems
2. Three-scenario verification: generalist, persona, and child propagation
3. Compatibility with hermes-agent 0.12.0 on `python:3.12-slim`

## Test Image

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*
RUN pip install hermes-agent==0.12.0

# Install the persona skill
COPY install.sh /tmp/install.sh
RUN bash /tmp/install.sh

# Configure the persona-worker profile
RUN mkdir -p ~/.hermes/profiles/persona-worker && \
    echo 'openai_api_key: $OPENAI_API_KEY' > ~/.hermes/profiles/persona-worker/config.yaml
```

## Three-Scenario Verification

### Scenario 1: Generalist (no `--skill persona`)

**Expected behavior:** Worker runs without role adoption. No heartbeat with
🎭 emoji is emitted. The worker processes the task using Hermes Agent's default
system prompt.

```bash
hermes kanban create 'Benchmark: system health check' --assign persona-worker
hermes kanban dispatch
# → Worker runs as generalist, no role adoption
```

**Verification:**

```bash
hermes kanban show <task_id> | grep "heartbeat" | grep "🎭"
# → No output (no role was adopted)
```

### Scenario 2: Persona (`--skill persona`)

**Expected behavior:** Worker fetches the agency-agents catalog, analyzes the
task body, picks a matching role, and announces adoption via heartbeat.

```bash
hermes kanban create 'Security audit: OWASP top 10' --skill persona --assign persona-worker
hermes kanban dispatch
# → Worker adopts 🔒 Security Engineer role
```

**Verification:**

```bash
hermes kanban show <task_id> | grep "heartbeat"
# → [timestamp] heartbeat {'note': '🎭 Role adopted: 🔒 Security Engineer'}
```

### Scenario 3: Child Propagation

**Expected behavior:** A persona-activated parent creates children with
`skills=['persona']` and each child independently adopts its own role.

```bash
hermes kanban create 'Build web app decomposer' --skill persona --assign persona-worker
# Parent decomposes into:
#   - Frontend: React storefront
#   - Backend: Payment API
# Each child gets skills=['persona']
```

**Verification:**

```bash
hermes kanban show <child_1_id> | grep "heartbeat"
# → 🎭 Role adopted: 🎨 Frontend Developer
hermes kanban show <child_2_id> | grep "heartbeat"
# → 🎭 Role adopted: 🏗️ Backend Architect
```

## install.sh Portability Checks

The persona installer must work on:

| OS | Shell | Status |
|----|-------|--------|
| Ubuntu 22.04 (Docker) | bash | ✅ Tested |
| macOS 14 (Sonoma) | zsh | ✅ Tested |
| Debian 12 | bash | ✅ Verified |
| Alpine 3.19 | ash | ⚠️ Requires bash |

### Key portability features

- Uses `set -euo pipefail` for strict error handling
- `--dry-run` flag for preview without modification
- SHA256 checksum validation via `install.sh.sha256`
- No hardcoded paths — uses `$HOME` and `~/.hermes/skills/`
- No OS-specific commands (no `sed -i` on macOS — uses Python or heredoc)

## Runtime profile (hermes-agent 0.12.0)

| Metric | Value |
|--------|-------|
| Image size (base) | ~130 MB |
| Install time | ~15 seconds |
| Task startup time | ~8 seconds |
| Role adoption latency | ~3 seconds (catalog fetch) |

## Known issues

- **Alpine Linux:** The default `ash` shell does not support `set -o pipefail`.
  Use `bash` explicitly: `bash install.sh`.
- **Network dependency:** The first run of a persona worker requires fetching
  the agency-agents catalog from `raw.githubusercontent.com`. If network is
  unavailable, the worker falls back to generalist mode.
- **Environment variables:** `OPENAI_API_KEY` (or equivalent provider key) must
  be set in the profile config for the worker to make LLM calls during role
  adoption.
