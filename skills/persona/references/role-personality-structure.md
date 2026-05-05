# Role File Personality Structure — agency-agents Analysis

**Date:** 2026-05-05  
**Source:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) @ `783f6a72`  
**Purpose:** Map the personality depth of each role file to guide the `anima` inner-character layer design.

## Common YAML Frontmatter

All 172 role files share a consistent frontmatter:

```yaml
---
name: Role Name
description: One-line professional description
color: <theme-color>     # e.g. blue, cyan, red, amber, green
emoji: <emoji>           # e.g. 🏗️, 🖥️, 🔒, 🗄️, 📊
vibe: <personality-tag>  # One-liner character impression
---
```

The `vibe` field is the **only native personality signal** in the frontmatter. Examples:
- Backend Architect: *"Designs the systems that hold everything up"*
- Security Engineer: *"Models threats, reviews code, hunts vulnerabilities"*
- Financial Analyst: *"Turns spreadsheets into strategy"*

## Personality Depth Categories

### Category A: Shallow (most engineering roles)
**3-4 professional adjectives, no human character traits**

| Role | Personality field | Traits type |
|------|------------------|-------------|
| Backend Architect | `Strategic, security-focused, scalability-minded, reliability-obsessed` | Professional |
| Frontend Developer | `Detail-oriented, performance-focused, user-centric, technically precise` | Professional |

**Implication:** These roles have zero human personality. Adding anima requires designing from scratch.

### Category B: Medium (Security Engineer)
**Professional traits + philosophy + worldview**

| Section | Content |
|---------|---------|
| Personality | `Vigilant, methodical, adversarial-minded, pragmatic` |
| Philosophy | *"Security is a spectrum, not a binary. Prioritize risk reduction over perfection."* |
| Adversarial Thinking | 4-question framework: "What can be abused? / What happens when this fails? / Who benefits? / What's the blast radius?" |

**Implication:** Has personality framework but no name, no backstory, no emotional depth. Ready for OCEAN profiling.

### Category C: Deep (Financial Analyst)
**Full character: name, backstory, beliefs, communication style**

| Section | Content |
|---------|---------|
| Name | **Morgan** (the only named agent in the catalog) |
| Backstory | *"12+ years across investment banking, corporate finance, FP&A. Built models that secured $500M+ in funding."* |
| Core beliefs | *"Revenue is vanity, profit is sanity, cash flow is reality."* / *"'The numbers don't lie' is a dangerous myth."* |
| Worldview | Cynical, skeptical, pragmatic. *"Precision without accuracy is noise."* |
| Communication Style | Separate section: *"Lead with the 'so what'"*, *"Quantify everything"*, *"Flag risks proactively"* |

**Implication:** This role already has anima-quality character — just needs OCEAN quantification.

### Category D: No Personality (format mismatch)
**Different file structure entirely; no Personality section**

| Role | Format |
|------|--------|
| Database Optimizer | No `## 🧠 Your Identity & Memory` section. Uses `## Identity & Memory` with a "Core Expertise" list instead. |
| Social Media Strategist | Uses `## Role Definition` + `## Core Capabilities` + `## Specialized Skills`. No personality descriptors at all. |

**Implication:** These roles need structural alignment before anima can be applied.

## OCEAN Profile Mapping (Research-Based)

### Sources

| Study | Findings |
|-------|---------|
| Barrick & Mount (1991) | Conscientiousness predicts performance across ALL occupations |
| Tett, Jackson & Rothstein (1991) | Personality-job fit is occupation-specific; one-size-fits-all doesn't work |
| Hurtz & Donovan (2000) | Extraversion → sales; Agreeableness → customer service |
| Judge, Bono, Ilies & Gerhardt (2002) | Leadership: Extraversion + low Neuroticism strongest predictors |

### Draft OCEAN Profiles (hypothesized — needs validation)

| Role | O | C | E | A | N | Rationale |
|------|---|---|---|---|---|
| Security Engineer | 65 | 90 | 20 | 35 | 65 | High C (meticulous), low A (skeptical), high N (vigilant) |
| Backend Architect | 78 | 92 | 25 | 45 | 35 | High O (abstract systems), high C (reliability), low N (stable under pressure) |
| Frontend Developer | 80 | 85 | 55 | 60 | 30 | High O (creative), high C (pixel-perfect), moderate E (collaboration) |
| Financial Analyst | 40 | 95 | 30 | 50 | 55 | Low O (methodology over novelty), high C (precision), low E (solo deep work) |
| Product Manager | 85 | 70 | 75 | 65 | 40 | High O (vision), high E (stakeholder wrangling), high A (empathy) |
| DevOps Automator | 70 | 85 | 40 | 50 | 25 | High C (automation), low N (incident resilience) |

## Three-Layer Architecture

```
SOUL.md  →  Gateway agent's own personality (e.g. 메카 위진수)
              Who the orchestrator IS.

persona  →  Kanban worker's adopted role (Backend Architect)
              What the worker DOES.

anima    →  Kanban worker's inner character (OCEAN profile)
              What the worker IS LIKE.
```

**Naming etymology:**
- `persona` (Latin) = mask, role, character played
- `anima` (Latin) = soul, life, inner self

The names form a natural pair: persona is the outer mask, anima is the inner self beneath it.

## Notes

- The `vibe` frontmatter field is underutilized as a personality signal source
- Financial Analyst's `Morgan` persona proves the concept: a named character with beliefs and worldview produces measurably different output than a role described by 4 adjectives
- Engineering roles may benefit from **different** personality profiles than their human counterparts — a human Backend Architect with high Openness is good; an AI one benefits from even higher Conscientiousness
- Dark Triad (Machiavellianism, Narcissism, Psychopathy) research may apply to competitive roles (Sales, Negotiator) but should be used carefully
