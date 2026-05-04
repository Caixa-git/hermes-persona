# Matching Improvement Research — Role Selection Accuracy

## Research Context

The persona system uses 4 research-backed principles to match tasks to
specialist roles from the [agency-agents](https://github.com/msitarzewski/agency-agents)
catalog. This document captures research notes on how role matching accuracy
could be improved, based on analysis of benchmark results and real-world task
outcomes.

## Current Performance

The benchmark (`test_benchmark.py`) validates that for 15 gold-standard task
types, the expected specialist role exists in the agency-agents catalog and
can be identified. **Current pass rate: 15/15 (100%).**

However, as noted in `benchmark-methodology.md`:

> "This benchmark measures whether the *right role exists in the catalog* for
> each task type. It does not measure whether an LLM-based kanban worker
> *actually picks* the right role at runtime."

The real matching accuracy — the LLM's ability to consistently pick the
correct role given a task body — is the open question.

## Improvement Dimensions

### 1. Role Selection Prompt Structure

**Current approach:** The persona skill's SKILL.md presents the 4 research
principles as a numbered list with inline explanations. The worker reads this
and applies them during role selection.

**Potential improvement:** Add concrete decision trees to the skill:

```markdown
# Role selection decision tree
Is this task creating code?      → Engineering division
  Is it UI/frontend?             → 🎨 Frontend Developer
  Is it API/backend?             → 🏗️ Backend Architect
  Is it CI/CD/infra?             → ⚙️ DevOps Automator
Is this task reviewing code?     → 👁️ Code Reviewer
  Is it security-focused?        → 🔒 Security Engineer
Is this task designing?          → 🎨 Design division
Is this task managing product?   → 📊 Product division
...
```

**Expected impact:** Higher consistency across different LLMs. Reduces
reliance on the model's internal knowledge of the agency-agents catalog.

### 2. Role Boundary Disambiguation

**Current approach:** Each worker independently scans all ~172 roles and picks
the best match. This works for single-worker tasks but can produce overlapping
role selections in multi-worker scenarios.

**Potential improvement:** Pre-filter the catalog by task type before the
worker sees it:

```
Task type "security audit" → only roles in: Engineering division,
Security Engineer, Incident Response Commander
```

This reduces the selection space and ambiguity.

**Expected impact:** Fewer boundary conflicts in multi-worker scenarios.
Workers are more likely to pick different (complementary) roles.

### 3. Task Body Feature Extraction

**Current approach:** The worker reads the full task body and applies the 4
principles subjectively. No structured feature extraction.

**Potential improvement:** Add a structured template to the task body that
extracts key signals:

```yaml
Task type: security-audit
Tech stack: [Python, PostgreSQL, FastAPI]
Domain: backend
Output: report
```

The worker could use these explicit signals alongside the free-text body.

**Expected impact:** More consistent matching for tasks with clear types.
Less sensitive to body phrasing variations.

### 4. Role Experience Weighting

**Current approach:** All roles are treated equally — the worker picks the
best match based on description text alone.

**Potential improvement:** Add metadata fields to role specifications that
indicate task type affinity:

```yaml
# In role spec frontmatter
task_affinities:
  - security-audit
  - code-review
  - threat-modeling
  - vulnerability-assessment
```

Workers could score roles based on explicit affinity matches, not just
description similarity.

**Expected impact:** Dramatically improved matching for common task types.
Adds a deterministic signal alongside the LLM's subjective judgment.

### 5. Feedback Loop

**Current approach:** No feedback mechanism. If a worker picks the wrong role,
there's no record or correction.

**Potential improvement:** Add a `role_selected` metadata field to
`kanban_complete()` and a post-task check:

```python
kanban_complete(
    metadata={
        "role_selected": "Backend Architect",
        "role_confidence": "high",
        "task_type": "api-design",
    }
)
```

A review worker could periodically audit role selections and flag mismatches.

**Expected impact:** Continuous improvement through data collection. Enables
tuning role recommendations based on actual outcomes.

## Research Priorities

| Priority | Improvement | Effort | Impact |
|----------|------------|--------|--------|
| P0 | Decision tree in skill | Low (doc change) | High |
| P0 | Pre-filter catalog by type | Medium (code change) | High |
| P1 | Structured task body template | Low (convention) | Medium |
| P1 | Role affinity metadata | High (catalog change) | High |
| P2 | Feedback loop | Medium (tool change) | Medium |

## Open Questions

1. **Role count sensitivity:** Does accuracy degrade as the agency-agents
   catalog grows from 172 to 500+ roles? At what point does the LLM's
   selection quality drop?

2. **Model sensitivity:** Do different models (DeepSeek-V4 Flash vs GPT-4o)
   produce different role selections for the same task body? Early data
   suggests yes — Flash-tier models benefit more from structured decision
   trees than Pro-tier models.

3. **Task body length:** Do longer task bodies improve or degrade matching?
   Intuitively, more context helps — but noisy or irrelevant detail may
   distract the selection process.

4. **Non-English tasks:** Does role matching accuracy differ for non-English
   task bodies? The catalog is English-only, so Korean/Japanese task bodies
   rely on the model's translation ability during role selection.
