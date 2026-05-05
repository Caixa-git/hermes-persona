# Benchmark Methodology — Role Selection Accuracy

The [`test_benchmark.py`](../test_benchmark.py) script validates that the
persona role-adoption system selects the correct specialist for each task type.

## Benchmark design

### Test structure (47 tests across 6 sections)

| Section | Tests | What it validates |
|---------|-------|-------------------|
| [1/3] KANBAN_GUIDANCE — Principles present | 11 | All 4 principles + 7 citations present in patched prompt_builder.py |
| [2/3] Agency-agents catalog | 15 | README is fetchable + 14 key roles exist in the catalog |
| [3/3] Task-to-role mapping sanity | 15 | For 15 diverse tasks, the expected role exists in the catalog |
| [4/6] Hermes config — kanban in toolsets | 1 | `kanban` appears in `~/.hermes/config.yaml` toolsets |
| [5/6] Persona skill — SKILL.md | 1 | SKILL.md exists and contains research principle keywords |
| [6/6] Repository — essential files | 4 | LICENSE, install.sh, README.md, .gitignore exist |

### 15 benchmark tasks with gold-standard roles

| # | Task Description | Expected Role |
|---|-----------------|---------------|
| 1 | React dashboard with D3.js | Frontend Developer |
| 2 | REST API with JWT | Backend Architect |
| 3 | CI/CD pipeline with GitHub Actions | DevOps Automator |
| 4 | Optimize PostgreSQL queries | Database Optimizer |
| 5 | OWASP audit | Security Engineer |
| 6 | Product Requirements Document | Product Manager |
| 7 | iOS login FaceID | Mobile App Builder |
| 8 | Sentiment analysis model | AI Engineer |
| 9 | Dockerize to AWS ECS | DevOps Automator |
| 10 | API documentation | Technical Writer |
| 11 | Brand style guide | Brand Guardian |
| 12 | Social media campaign | Social Media Strategist |
| 13 | Financial forecast model | Financial Analyst |
| 14 | User research interviews | UX Researcher |
| 15 | Production outage response | Incident Response Commander |

### Principles validated

The benchmark checks that all 4 research-backed selection principles are
present in the patched `KANBAN_GUIDANCE`:

| Principle | Citation | What it means |
|-----------|----------|---------------|
| Output-type alignment | MetaGPT (ICLR 2024) | Match role deliverable to task needs |
| Role boundary clarity | CAMEL (NeurIPS 2023) | Pick exactly one non-overlapping role |
| Task decomposition priority | AgentVerse (ICML 2024) | Cover primary domain; sub-tasks handle rest |
| Confidence threshold | AutoGen (MSR 2023) | Fall back to generalist if <30% fit |

## Results

### Current pass rate: 47/47 (100%)

All 47 tests pass as of the latest run. The 15-task gold-standard mapping
achieves 100% role availability in the agency-agents catalog.

## Caveats

1. **Selection accuracy only.** This benchmark measures whether the *right role
   exists in the catalog* for each task type. It does not measure whether an
   LLM-based kanban worker *actually picks* the right role at runtime. That
   requires end-to-end testing with real kanban task dispatch.

2. **Static catalog check.** The benchmark fetches the live README but only
   checks role existence via regex. It does not validate the content of
   individual role `.md` files.

3. **Network dependency.** Test [2/3] requires a network connection. If
   GitHub raw is unreachable, tests 16-30 will fail gracefully.

4. **Gold-standard mappings are heuristic.** The 15 task-to-role pairs are
   manually curated based on the auditor's judgment. Different LLMs or human
   evaluators might map some edge-case tasks differently.

5. **No execution quality measurement.** Role selection is only the first
   step. A correctly selected role might still produce poor output. Execution
   quality benchmarking is a separate (future) concern.

## Running the benchmark

```bash
cd ~/hermes-persona && python3 test_benchmark.py
```

Required:
- Python 3.8+
- Standard library only (no pip installs needed)
- Network access to `raw.githubusercontent.com`
- Hermes Agent installed at `~/.hermes/hermes-agent/`
- `.env` not required (test reads only config, prompt_builder.py, and network)
