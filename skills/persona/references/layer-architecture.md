# Hermes Identity Layer Architecture

> Established 2026-05-05. Clarified through external review (Claude) and user correction.
> This document records the LAYER HIERARCHY, not the runtime behavior.

## Core Principle

Hermes has THREE distinct identity systems, each at a different layer.
They are SEPARATE. Do not conflate them.

```
┌──────────────────────────────────────────┐
│  ① SOUL.md  (Native Hermes Agent)        │  Layer ?
│  $HERMES_HOME/SOUL.md                    │
│  Loaded by: agent/prompt_builder.py      │
│  load_soul_md() → slot #1 system prompt  │
│  FILE: ~/.hermes/SOUL.md                 │
├──────────────────────────────────────────┤
│  ② ANIMA  (Core Nature, always-on)       │  Layer 13
│  $HERMES_HOME/skills/anima/ (not yet)    │
│  REPO: github.com/Caixa-git/hermes-anima │
│  Activated: --skill anima                │
│  Priority: Anima > Persona on conflict   │
├──────────────────────────────────────────┤
│  ③ PERSONA  (Social Role, opt-in)        │  Layer 13
│  $HERMES_HOME/skills/persona/SKILL.md    │
│  REPO: github.com/Caixa-git/hermes-persona│
│  Activated: --skill persona              │
│  Fallback: no-role (NOT generalist)      │
├──────────────────────────────────────────┤
│  ④ USER MEMORY  (Personal Preferences)   │  Runtime
│  Injected via memory tool                │
│  Android tone, ~다/~하겠다/~판단된다,     │
│  음절 하이픈, 🤖/🔧, 한국어 응답        │
└──────────────────────────────────────────┘
```

## Critical Rules

### 1. SOUL.md is separate
SOUL.md is a **native Hermes Agent feature**, not part of the persona/anima system.
It lives at `$HERMES_HOME/SOUL.md` and is loaded by `agent/prompt_builder.py::load_soul_md()`.
Do NOT treat SOUL.md as "Layer 1 anima" — it is its own thing. Its layer position is undetermined.

### 2. Anima is NOT in persona
The persona skill (`~/.hermes/skills/persona/`) must contain ZERO anima content:
- No OCEAN profiles
- No generalist definition (belongs in hermes-anima)
- No anima experiments or test scripts
- No anima-vs-persona comparison tables
- Only cross-layer boundary references (e.g., "See hermes-anima")

Persona SKILL.md's "Layer Boundaries" section is the only allowed anima reference,
and it must point to hermes-anima for details.

### 3. Persona-worker/SOUL.md is persona-only
The worker profile at `~/.hermes/profiles/persona-worker/SOUL.md` should contain:
- The persona role (Financial Analyst, Backend Architect, etc.)
- Core mission
- Critical rules
- Success metrics

It should NOT contain:
- Anima section
- OCEAN profile
- Layer Priority statement
- "nature > role" rules (those belong in hermes-anima)

### 4. Anima always wins on conflict
When anima and persona conflict, anima (core nature) prevails.
This is enforced through social framing ("Your nature > your role") in KANBAN_GUIDANCE (Layer 3),
NOT through layer position alone (Geng et al., AAAI 2026 warns layer position alone is unreliable).

Empirically: social framing at Layer 3 works 100% (10/10 on DeepSeek V4 Flash),
but Layer 13 duplication is recommended for other models.

## File Location Summary

| System | Path | Type |
|--------|------|------|
| SOUL.md | `~/.hermes/SOUL.md` | Native Hermes identity file |
| SOUL.md (friend-bot) | `~/hermes-rebirth/friend-bot/profile/SOUL.md` | Separate instance (메카 국동호) |
| Anima profiles | `hermes-anima/skills/anima/profiles/*.md` | via GitHub |
| Persona SKILL.md | `~/.hermes/skills/persona/SKILL.md` | Installed skill |
| Persona source | `~/hermes-persona/skills/persona/SKILL.md` | Source repo |
| Persona worker SOUL.md | `~/.hermes/profiles/persona-worker/SOUL.md` | Worker identity |
| hermes-rebirth | `~/hermes-rebirth/` | PRIVATE backup only |
