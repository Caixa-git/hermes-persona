# Multi-Agent Cross-Validation (Persona Round-Table)

> Run N parallel persona workers with different review focuses, collect results via a parent orchestrator that synthesizes findings, flags consensus vs disagreement, and produces a unified action plan.

## When to use

- Document review requiring multiple independent perspectives (legal, technical, security)
- Any task where "one reviewer might miss something" — parallel specialists catch blind spots
- Quality assurance: 3 reviewers > 1, even when all use the same underlying model

## Prerequisites

- **If the source document is binary** (docx, PDF): extract text first. Python libraries:
  - docx: `python3 -c "import zipfile, xml.etree.ElementTree as ET; ..."` (see `python-debugpy` skill or use `ocr-and-documents`)
  - PDF: `pymupdf` (fitz) for structured extraction
  - Include the extracted text content (or path to it) in each review task's body so every worker reads from the same source
- **File path must be absolute** — workers have scratch workspaces and can't resolve relative paths
- **Max runtime** — complex reviews may exceed the 10-min default. Use `--max-runtime 15m`

## Pattern

### Step 1: Create N focused review tasks

Each task has a DIFFERENT body focus so workers naturally adopt different angles:

```bash
# Task A: Risk scanning — find adversarial weaknesses
hermes kanban create '[검토①] 위험성: 문서 내 불리한 표현 분석' \
  --body 'Focus on identifying statements that could be used against us...' \
  --skill persona

# Task B: Defense strategy — evaluate resilience against counter-arguments  
hermes kanban create '[검토②] 방어: 방어 전략 및 반박 대비 분석' \
  --body 'Focus on how well the document withstands expected counter-arguments...' \
  --skill persona

# Task C: Claims reinforcement — identify strengthening opportunities
hermes kanban create '[검토③] 보강: 청구 근거 보강 검토' \
  --body 'Focus on strengthening the claim and filling structural gaps...' \
  --skill persona
```

### Step 2: Assign and dispatch (all at once → parallel execution)

```bash
hermes kanban assign t_xxx persona-worker
hermes kanban assign t_yyy persona-worker
hermes kanban assign t_zzz persona-worker
hermes kanban dispatch
# → All 3 spawn simultaneously
```

### Step 3: Create orchestrator cross-synthesis task

Create a parent task whose body contains SUMMARIES of all 3 reviews (include key findings inline so the orchestrator doesn't need workspace access to child task files):

```bash
hermes kanban create '[종합] 3개 분석 교차 검증 — 일치/이견 종합' \
  --body '## Three Review Summaries\n### Review 1: ...\n### Review 2: ...\n### Review 3: ...\n## Instructions\n1. Analyze each review'\''s findings\n2. Identify consensus (agreed by 2+) vs disagreements\n3. Rank priority fixes\n4. Output synthesis_report.json' \
  --max-runtime 15m \
  --skill persona
```

### Step 4: Collect results

The orchestrator worker writes a synthesis report (`synthesis_report.json`) with:

## Output structure

```json
{
  "consensus_findings": [
    {"id": "C1", "issue": "...", "severity": "CRITICAL|HIGH|MEDIUM",
     "reviewers_agreeing": [1, 2, 3], "consensus_action": "..."}
  ],
  "disagreements": [
    {"id": "D1", "issue": "...",
     "analysis": "Why reviewers disagree", "recommendation": "..."}
  ],
  "priority_fixes": [
    {"rank": 1, "target": "P10", "action": "DELETE", "impact": "..."}
  ],
  "recommended_action_plan": {
    "phase_1_urgent": {"steps": [...]},
    "phase_2_credibility": {"steps": [...]},
    "phase_3_strengthening": {"steps": [...]}
  },
  "overall_assessment": {
    "unanimous_verdict": "NOT SUBMITTABLE | READY | NEEDS_WORK",
    "must_fix_count": 5,
    "estimated_revision_effort": "~2-3 hours"
  }
}
```

## Real session data

| Metric | Value |
|--------|-------|
| Tasks created | 3 parallel + 1 synthesizer |
| Wall-clock time | ~8 min (3 parallel at ~5 min each + synthesizer at ~4 min) |
| Total worker time | ~18 min |
| Consensus findings | 5 (all 3 agreed) |
| Disagreements | 4 (different focus areas) |
| Priority fixes | 5 ranked items |
| Action plan steps | 12 (4 phases) |
| Report size | ~18 KB, 256 lines |

## Differences from single-review approach

| Aspect | Single review | Cross-validation |
|--------|--------------|-----------------|
| Blind spots | One reviewer's bias/flaw | 🟢 Multiple angles catch more |
| Consensus flagging | Not possible | 🟢 Explicit: "all 3 agree" vs "2 only" |
| False positives | Risk of over-flagging | 🟢 Disagreement section prevents over-correction |
| Time | ~5 min | ~8 min (marginally longer) |
| Cost | N workers × 1 | N workers × N |
| Orchestration | None needed | Need synthesizer task |
