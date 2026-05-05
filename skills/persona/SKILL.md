---
name: persona
description: "🎭 Expert role adoption for kanban workers — 172 specialists, 15 categories"
tags: [hermes-agent, kanban, persona]
---

# 🎭 persona — expert role adoption

## Critical Rules
<priority>Anima (core nature) > Persona (role). Nature prevails on conflict.</priority>
<rule>Opt-in. No `--skill persona` = no role adoption.</rule>
<rule>delegate_task() bypasses persona. Use kanban_create --skill persona.</rule>
<rule>Confidence < 30% → proceed WITHOUT a role. Mismatch degrades output 40-50%.</rule>
<rule>Children inherit via `skills=['persona']`. Omission = no specialist role.</rule>
<rule>git push/gh pr blocked. Workers read-only via curl. Orchestrator only.</rule>


## Selection (4 principles)
1. **Output-type alignment** (MetaGPT, ICLR 2024) — match deliverable to task
2. **Role boundary clarity** (CAMEL, NeurIPS 2023) — one role, non-overlapping
3. **Task decomposition priority** (AgentVerse, ICML 2024) — primary domain first
4. **Confidence threshold** (AutoGen, 2023) — <30% → no role

## Threshold Decision
`D×W + ⌈A/500⌉ ≤ 3` → direct OK. Else → `kanban_create --skill persona`.

- Guard 1: Design by Contract (Meyer) — precondition is inviolable
- Guard 2: ECA Rule (Dayal) — ON violation DO auto-convert
- Guard 3: Reflection (Smith) — meta vs base self-check

## Layer Boundaries
- Anima (core nature) is separate — see `hermes-anima` for definition and OCEAN profiles.
- When `--skill persona` active and confidence < 30%: proceed WITHOUT a specialist role. Task defines the frame.
- Anima > Persona on conflict. This is a cross-layer contract, not defined here.

## File Purity
<rule>This skill is PERSONA-ONLY. Anima content (OCEAN profiles, anima experiments, anima-layer tests, anima-persona papers) belongs in `hermes-anima`, NOT here.</rule>
<rule>If any reference or script under this skill contains anima-exclusive content, it must be moved to hermes-anima and deleted from this directory.</rule>

## Content Boundaries

<rule>This SKILL.md is a **public/shared component**. Personal user preferences (tone, style, communication format) belong in USER MEMORY, not in this file.</rule>

<rule>User-specifc rules — 안드로이드 톤, ~다/~하겠다/~판단된다, 음절 하이픈, Roleplay 금지 — are memory-only preferences. Do NOT add them to this SKILL.md.</rule>

## Multi-Persona (Major + Minor)

Extends single-role persona with a secondary role that contributes **perspective, experience, and viewpoint (향)** — not execution.

### Design

```
Single persona:  🏗️ Backend Architect → 순수 아키텍처 설계
Multi-persona:   🏗️ Backend Architect (major)
                   + 🎨 Frontend Developer (minor, 향만 주입)
                 → 아키텍처 문서인데 UX 감각이 살짝 묻어남
```

Minor provides **향 (flavor)** — not oversight. The major retains 100% decision authority. The minor's experience·personality·memory fields influence the output sympathetically, without explicit validation or checklist-style review.

### Implementation

```bash
hermes kanban create 'Payment API' \
  --skill persona:main=backend-architect,minor=ux-engineer
```

```yaml
Layer 13 injection:
  main:  Full role spec incl. mission (tokens(ma) = ~200)
  minor: experience·personality·memory ONLY — NO mission (tokens(mi) = ~30)
```

Minor receives exactly 3 fields from the agency-agents role file:
- **Personality** (e.g. "scalability-minded, security-focused")
- **Memory** (e.g. "You remember successful architecture patterns...")
- **Experience** (e.g. "You've seen systems fail through technical shortcuts")

Mission is excluded — the minor does NOT act, it influences.

### Control Variables

| Variable | Range | Effect | Paper |
|----------|-------|--------|-------|
| **Token Ratio** R = t(main) / t(minor) | [1, ∞) | R=1: equal influence; R=10: main-dominant | DiPT (Just et al., 2024) |
| **Priority Weight** P | [0.5, 1.0] | P=0.85: minor 향이 살짝; P=0.6: minor가 뚜렷 | HIPO (2603.16152) |
| **Authority Asymmetry** A | [0.7, 1.0] | A=1.0: main sole decision-maker; A=0.7: minor can suggest | Control Illusion (Geng et al., AAAI 2026) |

**Default:** R=8, P=0.85, A=1.0 — minor 향이 살짝 느껴지는 수준.

### Calibration

Set via query params: `--skill persona:main=X,minor=Y,weight=0.85`.

Lower weight = less minor influence. At weight < 0.6 the minor becomes functionally invisible. At weight > 0.95 the minor distorts boundary clarity (CAMEL principle violation).

### Trap: Same-model homogeneity

Shin (2026) — *The Reasoning Trap* (arXiv:2605.01704): prompting the same model with different roles produces **diverse phrasings of one perspective, not diverse perspectives**.

Mitigation: minor receives **only** experience·personality·memory (no mission). This forces genuine viewpoint differentiation because the minor has no action mandate — merely a perceptual filter applied to the major's output frame.

### CDPD Model — Cross-Domain Persona Decision

Deterministic gate for when multi-persona is worthwhile. Not every task benefits from a minor — overuse wastes tokens and degrades role boundary clarity (CAMEL).

| 기호 | 명칭 | 값 | 의미 |
|:----:|:-----|:---:|:------|
| **S** | Sigma — Cross-Domain Signal Count | — | Task keywords outside major's category |
| **Φ_s** | Singular Quality Baseline | 0.85 | Single persona quality at S=0 |
| **Φ_m** | Multi Quality Baseline | 0.90 | Multi persona quality at S=0 |
| **α** | Alpha — Singular Decay Rate | 0.125 | Quality loss per S for single |
| **β** | Beta — Multi Boost Rate | 0.025 | Quality gain per S for multi |
| **Γ_base** | Gamma — Multi Base Overhead | 43,122 tok | Fixed cost of loading a minor |
| **η** | Eta — Quality-Cost Tradeoff | 0.3 | Configurable, higher = cost-sensitive |
| **T** | Theta — Decision Threshold | ≈1.18 | ceil(T) = 2 |

```
PRECONDITION:
  Σ(is_outside_category(w, C_major) for w in task_keywords) ≥ ceil(T)

  T solves ΔU(T) = 0  where  ΔU(S) = Q_multi(S) − Q_single(S) − η·ΔC(S)/k
  Empirically determined: T ≈ 1.18, ceil(T) = 2

  If S ≥ 2 → multi-persona (minor_count = min(S, 3))
  If S < 2 → single persona (major only)
```

**Empirical validation (2026-05-05):**
- S=0 (simple): single wins (ΔU = −0.96, multi overkill)
- S=2 (complex): multi wins **7-0** across all metrics (ΔU = +2.43)
- Verified stable across low-latency/high-quality scenarios (ψ-Ω cancellation)

**Derivation:** See `references/cdpd-model.md` for full mathematical proof.

### Empirical validation

Experiment (2026-05-05): Multi-persona beats sequential task-split **7-0** on "write an AI Agent paper" task — 39% faster, 54% cheaper, higher consistency and originality.
→ See `references/multi-persona-experiment.md` for full methodology and metrics.

### Future work

- [ ] Empirical: sweep R × P × A to find optimal settings per task type
- [ ] Verify: does minor's experience field alone produce more genuine diversity than full spec across different model families?
- [ ] Multi-model multi-persona: major on model A, minor on model B (bypasses Reasoning Trap)
- [ ] Calibration protocol: automated test suite to re-derive Φ, α, β, Γ_base for new models

## Behavior Matrix
| Event | Action |
|-------|--------|
| delegate_task() called | STOP → kanban_create --skill persona |
| Child missing persona | Pass `skills=['persona']` in kanban_create |
| git push attempted | Workers have NO GITHUB_TOKEN. Orchestrator only. |
| No role matches >30% | Proceed without role. Do not force mismatch. |
| GitHub raw unavailable | No-role fallback. Curl failure = expected. |
| `--skill persona` omitted | Worker runs without persona instructions |
