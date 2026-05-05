# Matching algorithm — improvement research

## Current approach: keyword scoring

Scans agency-agents README table for keyword overlap with the task description. Picks the single best match.

**Limitations identified:**
- Surface-level only. "PostgreSQL tuning" and "data pipeline" both match Database roles but require different competencies
- Single dimension — one role per task, no multi-role decomposition
- Complexity ignored. "Simple CRUD" vs "10M req/s distributed API" both map to Backend Architect
- Tech stack blind. FastAPI vs Go vs Java — not considered

## Academic foundations for improvement

### Person-Job Fit Theory
Kristof-Brown, A. L. (2005). *Consequences of Individuals' Fit at Work: A Meta-Analysis of Person–Job, Person–Organization, Person–Group, and Person–Supervisor Fit*. Personnel Psychology, 58(2), 281–342.

**Core idea:** Fit is multi-dimensional — demands-abilities (task requires X, role provides X) AND needs-supplies (role offers Y, task needs Y).

**Application:** Score each role on a competency matrix across ~10 dimensions (frontend, backend, security, data, devops, mobile, ML, design, product, QA). Task is parsed for competency requirements → cosine similarity against role vectors.

### Task-role competency matrix

```
                Frontend  Backend  Security  Data  DevOps
Frontend Dev      0.95     0.10     0.05     0.10   0.10
Backend Arch     0.10     0.90     0.30     0.40   0.40
Security Eng     0.05     0.30     0.95     0.10   0.30
DB Optimizer     0.00     0.40     0.10     0.95   0.10
DevOps Auto      0.10     0.30     0.30     0.10   0.95
```

Each cell = expert rating (0.0-1.0) of how relevant that role is to that competency domain. Agency-agents .md descriptions can be parsed with an LLM to extract these vectors.

### Multi-role decomposition
For complex tasks (breadth score > threshold), decompose into sub-tasks first, then assign best role per sub-task. Uses an LLM call to analyze the task description and produce sub-task breakdown with competency requirements.

## Implementation strategies ranked

| Strategy | Complexity | Accuracy gain | Latency cost |
|----------|-----------|---------------|-------------|
| **Embedding similarity** (text-embedding-3-small) | Medium | High | +200ms per task |
| **Competency matrix + cosine** | Low | Medium | +10ms (precomputed) |
| **LLM-based task analysis** | High | Highest | +1-2s per task |
| **Multi-role decomposition** | High | Highest (for complex) | +2-3s per task |

## Recommendation

Start with **competency matrix + cosine** — zero extra API calls, just a matrix lookup and a dot product. Then add embedding similarity if accuracy isn't enough. LLM-based analysis is overkill for the 95% case where the role is obvious (Frontend Dev → React dashboard).
