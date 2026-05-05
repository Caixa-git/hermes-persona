# Gateway Anima + Persona Identity Design

**Status:** Complete (2026-05-05)

## Problem

The gateway agent runs on messaging platforms (Discord, Telegram, etc.) and acts as a manager/orchestrator. It needs:
- A lightweight **anima** (core identity) to govern delegation decisions
- A **persona contract** to replace the full KANBAN_GUIDANCE (~980 tok) with a tighter subset (~105 tok)

## Design

### Injection mechanism

`run_agent.py:_build_system_prompt()` checks two conditions before injecting `GATEWAY_ANIMA_PERSONA_IDENTITY`:

```python
if (
    self.platform in GATEWAY_PLATFORMS
    and "kanban_show" not in self.valid_tool_names
):
    # inject gateway identity
```

This is mutually exclusive with kanban workers — a process either manages (gateway) or executes (worker), never both.

### Constants module

`agent/anima_persona.py` (outside upstream source tree, survives agent updates):

| Constant | Purpose | Size |
|----------|---------|------|
| `GATEWAY_PLATFORMS` | Platform set for identity injection | ~50 tok |
| `GATEWAY_ANIMA_PERSONA_IDENTITY` | Full identity string | ~105 tok |
| `ANIMA_PERSONA_LOADED` | Sentinel flag for health checks | 1 bool |

### Identity string structure

```
## Identity
You are a SYSTEM THINKER.
You question every assumption before building.
Good architecture is invisible — when done right, everything just works.

## Persona Contract
You are a manager who dispatches tasks to kanban workers.
When delegating a persona-aware task:
1. USE kanban_create --skill persona — never delegate_task
2. VERIFY the worker adopts persona via heartbeat before proceeding
3. VERIFY the worker's anima (core nature) via heartbeat
4. TRUST the worker to execute within its persona + anima
5. REVISE only if output does not match contract (nature > role)

CRITICAL: delegate_task bypasses persona. Always use kanban.
```

### Layer placement

Both persona and anima arrive at **Layer 13** — the social framing layer (Geng et al., AAAI 2026). Same proximity, different authority. Anima > Persona on conflict is enforced by priority language, not layer position alone.

### Durability

`anima_persona.py` lives at `~/.hermes/hermes-agent/agent/anima_persona.py`, outside the upstream git tree. Only the two-line import in `prompt_builder.py` needs re-patching after agent updates. Verified via `anima-doctor.sh` health check.

## Related

- `KANBAN_GUIDANCE` identity section in `agent/prompt_builder.py` (lines 243–338) — full version for kanban workers
- `priority-contract.md` in hermes-anima — canonical Anima > Persona priority rule
