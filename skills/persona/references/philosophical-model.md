# Philosophical Model — Anima as Nature, Persona as Job

## Core Principle

```
Anima = birth (출산). Assigned by the creator/gateway at spawn time.
        The worker DOES NOT choose its nature. It IS its nature.
        The gateway pre-loads anima via the persona-worker profile.

Persona = job (직무). Self-selected by the worker for each task.
         The gateway CANNOT force a persona on the worker.
         The worker independently fetches the role catalog and picks.
```

## Architectural Constraints (Empirically Verified)

| Action | Mechanism | Result |
|:-------|:----------|:-------|
| Gateway assigns anima | Pre-load anima skill in persona-worker profile | ✅ Works. Worker heartbeats: "🧠 Anima: System Thinker" |
| Gateway forces persona | `skills=["persona:main=X,minor=Y"]` in kanban_create | ❌ Rejected: "Unknown skill(s): persona:main=X,minor=Y" |
| Gateway suggests persona | Task body includes role suggestion context | ✅ Informs worker without coercion |
| Worker self-selects persona | KANBAN_GUIDANCE step 2 → fetches catalog → picks | ✅ Verified via heartbeat: "🎭 Role adopted: 🏛️ Software Architect" |

## CDPD Evaluation Ownership

The Cross-Domain Persona Decision (CDPD) model is evaluated by the **WORKER**, not the gateway. The gateway's role is to:

1. Provide a well-structured task body (clear keywords enable accurate CDPD)
2. Verify adoption via heartbeat after spawning
3. Trust the worker's persona selection

## Persona/Anima Comparison

| Dimension | Persona | Anima |
|:----------|:--------|:------|
| Activation | Opt-in (`--skill persona`) | Always-on (installed → active) |
| Nature | 인공적(artificial), 수동(manual) | 본질(essence), 자동(automatic) |
| Role | Tool you activate for a task | Who you are at core |
| On conflict | Defers | **PREVAILS** |

## Priority Rule

- Your fundamental nature (anima) defines who you are.
- The role you adopt (persona) is a tool you use to accomplish tasks.
- When nature and role conflict, **YOUR NATURE PREVAILS.**
  _Canonical source: `hermes-anima/spec/priority-contract.md`_

## References

- Control Illusion (Geng et al., AAAI 2026 / arXiv:2502.15851)
- Experiences Build Characters (Wang et al., arXiv:2603.06088)
- Persona Steering Impact (Chen et al., arXiv:2604.11048)
