# Multi-Reviewer Analysis Pattern

Reusable pattern for analyzing documents, code, or proposals through 3 specialized reviewers + cross-synthesis. Originally developed for legal document review, applicable to security audits, design reviews, architecture proposals, etc.

## Pattern Overview

```
                   ┌─────────────────┐
                   │  Source Document │
                   │  + Full Context  │
                   └────────┬────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Reviewer ①   │ │ Reviewer ②   │ │ Reviewer ③   │
    │ (Security)   │ │ (Defense)    │ │ (Improvement)│
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            ▼
                   ┌─────────────────┐
                   │  Synthesis ④    │
                   │  (Cross-verify) │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │  Final Report   │
                   └─────────────────┘
```

## How to Dispatch

**DO NOT use `delegate_task`** — it times out with reasoning models (see hermes-agent skill pitfall). Use `kanban_create` with linked tasks:

```bash
# 1. Create 3 reviewer tasks
hermes kanban create "[분석-①] 위험성: <document> 취약점 분석" --skill persona
hermes kanban create "[분석-②] 방어: <document> 대응 전략 분석" --skill persona
hermes kanban create "[분석-③] 보강: <document> 개선 사항 분석" --skill persona

# 2. Create synthesis task (depends on all 3)
hermes kanban create "[종합] <document> 교차 검증 — 3개 분석 결과 종합" --skill persona
hermes kanban link <task1_id> <synthesis_id>
hermes kanban link <task2_id> <synthesis_id>
hermes kanban link <task3_id> <synthesis_id>
```

## Reviewer Roles

### ① Risk/Security Reviewer
- Finds what could go wrong, what's dangerous, what's missing
- Severity grading: CRITICAL > HIGH > MEDIUM
- Each finding: what, why, counter-argument scenario, fix
- Mindset: adversarial, worst-case thinker

### ② Defense/Resilience Reviewer  
- Predicts attacks/objections and prepares counter-arguments
- Identifies gaps that could be exploited
- Suggests defensive additions
- Mindset: protective, anticipates opposition

### ③ Improvement/Reinforcement Reviewer
- Finds missing strengths that should be added
- Suggests stronger framing of existing points
- Identifies evidence gaps and collection strategies
- Mindset: constructive, maximizes impact

### ④ Synthesis Reviewer
- Cross-verifies 3 analyses for agreement/conflict
- Resolves contradictions between reviewers
- Produces unified prioritized action list
- Mindset: integrative, finds consensus

## Context is Critical

Each reviewer MUST receive the FULL context, not just the document under review. For legal documents, this means case timeline, evidence list, party statements. For code reviews, this means architecture docs, related PRs, design decisions.

**Anti-pattern:** Giving reviewers just the document → they miss context-dependent risks.
**Correct:** Giving reviewers the document + comprehensive context document → informed analysis.

## Output Format

Each reviewer outputs JSON to a known path, plus a Korean-language summary in their kanban heartbeat. The synthesis reviewer reads all 3 JSON files and produces a unified report.

## Domain Adaptation

| Domain | Reviewer ① | Reviewer ② | Reviewer ③ |
|--------|-----------|-----------|-----------|
| Legal | 위험성 (Risk) | 방어 (Defense) | 보강 (Reinforcement) |
| Security Audit | Vulnerability | Exploitability | Mitigation |
| Design Review | Usability | Accessibility | Aesthetics |
| Architecture | Scalability | Reliability | Maintainability |
| Code Review | Bugs | Security | Performance |

## Pitfalls

1. **DeepSeek + delegate_task = 100% failure.** Always use kanban for this pattern.
2. **Missing context.** Reviewers who only see the document miss context-dependent issues.
3. **Synthesis skipped.** 3 reviews without synthesis = conflicting advice with no resolution.
4. **No file output.** Reviewers must write JSON to a shared path so synthesis can read it.
