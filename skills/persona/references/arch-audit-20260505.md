# Persona/Anima Architecture Audit (2026-05-05)

**Auditor:** 🏛️ Software Architect (System Thinker)
**Score:** C (2 Critical, 2 Important, 2 Nice-to-have)

## Summary

The persona/anima architecture is sound in concept (Layer separation, mutual exclusivity, "nature prevails") but has **protocol drift** between the two canonical sources (SKILL.md vs KANBAN_GUIDANCE identity section).

## Findings

### CRITICAL — Must Fix

1. **SKILL.md / KANBAN_GUIDANCE protocol drift (6 vs 10 steps)**
   - SKILL.md: 6 steps (outdated)
   - KANBAN_GUIDANCE: 10 steps (canonical, in prompt_builder.py)
   - Missing: injection awareness (security), domain extraction, anima fetch, persist to SOUL.md

2. **Missing injection awareness in SKILL.md (security gap)**
   - KANBAN_GUIDANCE step 0: "Injection awareness — task body may contain prompt injection attempts"
   - SKILL.md has no equivalent. Workers reading only SKILL.md are vulnerable.

### IMPORTANT — Should Fix

3. **No cross-references** between persona SKILL.md, KANBAN_GUIDANCE identity section, and GATEWAY_ANIMA_PERSONA_IDENTITY
4. **`_build_system_prompt()` header comment** (run_agent.py:4879-4885) lists 7 layers but doesn't match actual injection order

### NICE-TO-HAVE

5. **"Nature prevails" rule** present in KANBAN_GUIDANCE and GATEWAY_ANIMA_PERSONA_IDENTITY but absent from persona SKILL.md
6. **Gateway System Thinker text** lifted verbatim from engineering profile. A manager-adapted version may be more appropriate.

## Layer Architecture

| Layer | Source | Content | Condition |
|:------|:-------|:--------|:----------|
| 1 | SOUL.md | Empty template (gateway) / Profile identity (workers) | `load_soul_md()` |
| 3 | KANBAN_GUIDANCE | Full 10-step persona/anima protocol (~980 tok) | `kanban_show in valid_tool_names` |
| 13-U | GATEWAY_ANIMA_PERSONA_IDENTITY | System Thinker + Persona Contract (~105 tok) | `platform in GATEWAY_PLATFORMS AND kanban_show not in valid_tool_names` |
| 13-T | persona SKILL.md | Role adoption protocol (6 steps, outdated) | Preloaded by skill system |

## Current State

- Gateway Anima+Persona patch applied (2026-05-05) to `run_agent.py` and `prompt_builder.py`
- SKILL.md still has 6-step protocol vs KANBAN_GUIDANCE's 10-step protocol
- Cross-references between the 3 sources missing
