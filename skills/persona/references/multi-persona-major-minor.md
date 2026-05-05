# Multi-Persona "Major+Minor" — Implemented

An extension of the persona system beyond single-role-per-task by introducing a **primary (major) + supplementary (minor)** expertise structure. Designed and implemented on 2026-05-05 (user: 위진수).

## The Concept (전공+부전공)

```
Single persona:  🏗️ Backend Architect → 순수 아키텍처 설계
Multi-persona:   🏗️ Backend Architect (major)
                   + 🎨 Frontend Developer (minor, 향만 주입)
                 → 아키텍처 문서인데 UX 감각이 살짝 묻어남
```

The minor provides **향 (flavor)** — not oversight. The major retains 100% decision authority. The minor's experience·personality·memory fields influence the output sympathetically, without explicit validation or checklist-style review.

**Key distinction from chained/sequential multi-agent:** minor is NOT a separate execution step. It is a simultaneous perceptual filter applied to the major's output frame.

## Implementation (in persona SKILL.md)

### Layer 13 injection

```yaml
main:  Full role spec incl. mission (tokens = ~200)
minor: experience·personality·memory ONLY — NO mission (tokens = ~30)
```

Minor receives exactly 3 fields from the agency-agents role file:
- **Personality** (e.g. "scalability-minded, security-focused")
- **Memory** (e.g. "You remember successful architecture patterns...")
- **Experience** (e.g. "You've seen systems fail through technical shortcuts")

Mission is excluded — the minor does NOT act, it influences.

### Control Variables (paper-backed)

| Variable | Range | Effect | Paper |
|----------|-------|--------|-------|
| **Token Ratio** R = t(main) / t(minor) | [1, ∞) | R=1: equal influence; R=10: main-dominant | DiPT (Just et al., 2024) |
| **Priority Weight** P | [0.5, 1.0] | P=0.85: minor 향이 살짝; P=0.6: minor가 뚜렷 | HIPO (2603.16152) |
| **Authority Asymmetry** A | [0.7, 1.0] | A=1.0: main sole decision-maker; A=0.7: minor can suggest | Control Illusion (Geng et al., AAAI 2026) |

**Default:** R=8, P=0.85, A=1.0 — minor 향이 살짝 느껴지는 수준.

### Minor Threshold (deterministic gate)

Not every task benefits from a minor. Overuse wastes tokens and degrades role boundary clarity (CAMEL). A deterministic gate fires before any minor injection:

```
PRECONDITION:
  Σ(sim(w_i, C_major) < 0.5 for w_i in task_keywords) ≥ 2
```

| Task | Major | Outside keywords | Minor? |
|------|-------|:----------------:|:------:|
| `'Build JWT auth middleware'` | Backend Architect | — | ❌ |
| `'Design investor dashboard with charts'` | Backend Architect | "dashboard", "charts" | ✅ |
| `'Deploy ML pipeline'` | DevOps Automator | "ML" (1 only) | ❌ |
| `'Fintech app with fraud detection UX'` | Backend Architect | "fraud", "UX" | ✅ |

Keyword source: agency-agents category names + role name/description. TF-IDF or wordnet-based similarity suffices — no LLM call needed for the gate decision.

## Key Design Decisions

### Why NOT checklist/review model

초기 설계는 "부전공이 전공의 결정을 검토한다"는 접근이었다. 그러나:

1. **The Reasoning Trap** (Shin, 2026): 같은 모델에 다른 역할을 부여해도 진정으로 다른 관점이 나오지 않음
2. **사용자 피드백**: "구체적 체크리스트를 동적으로 만들기 어려운 거 알잖아" — 부전공이 동적으로 체크리스트를 생성하는 것은 정보 비대칭 없이 불가능
3. **해결책**: mission/checklist 없이 경험·성격·기억만 주입 → 행동 강제 없이 향만 전달. 비판적 검토자가 아닌 조미료 역할.

### Why NOT information asymmetry model

검토 모델은 전공과 부전공이 서로 다른 정보를 보는 구조가 필요하지만, 동일한 모델 인스턴스 내에서는 정보 분리가 불가능. 대신 **mission 제거**로 역할을 참조 수준으로 낮춤.

## Supported Papers

### DiPT — Diversified Perspective-Taking (Just et al., 2024)
**arXiv:2409.06241**

> "DiPT complements current reasoning methods by explicitly incorporating diversified viewpoints... enhances reasoning performance and stability."

**Relevance:** The minor persona provides a diversified viewpoint that complements the major's single-path reasoning.

### The Instruction Hierarchy (OpenAI, 2024)
**arXiv:2404.13208 — 310 citations**

Priority-ordered instruction stacks. Technical mechanism for enforcing "major > minor" priority.

### HIPO (2026)
**arXiv:2603.16152**

Priority-ordered instruction stack via constrained reinforcement learning. Enables `<priority level="primary/secondary">` tags with calibratable weights.

### Control Illusion (Geng et al., AAAI 2026)
**arXiv:2502.15851 — 21 citations**

Layer position alone fails — social framing needed for priority. Applied to: Anima > Persona (main SKILL.md), Major > Minor (multi-persona).

### The Reasoning Trap (Shin, 2026)
**arXiv:2605.01704**

> "When copies of the same model are prompted to debate, they produce diverse phrasings of one perspective rather than diverse perspectives."

**Mitigation:** Minor receives experience·personality·memory only (no mission). This forces genuine viewpoint differentiation because the minor has no action mandate — merely a perceptual filter.

## Open Questions

1. **R × P × A empirical calibration** — sweep needed per task type to find optimal settings
2. **Multi-minor** — 1 major + 2+ minors (e.g. Architect + Security + DevOps). Does N > 1 dilute the major too much?
3. **Minor selection** — currently manual via `--skill persona:main=X,minor=Y`. Could be automated via semantic task→category matching.

## References

- Just et al. (2024). *DiPT.* arXiv:2409.06241
- OpenAI (2024). *Instruction Hierarchy.* arXiv:2404.13208
- (2026). *HIPO.* arXiv:2603.16152
- Geng et al. (2025). *Control Illusion.* arXiv:2502.15851
- Shin (2026). *The Reasoning Trap.* arXiv:2605.01704
