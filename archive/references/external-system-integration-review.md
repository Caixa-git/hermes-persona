# External System Integration Review — Methodology

## Purpose

A structured methodology for evaluating whether an external project or system
can improve a system you maintain. This document uses the example of evaluating
[MemPalace](https://github.com/msitarzewski/mempalace) as a potential
improvement to Hermes Agent's memory subsystem, but the methodology applies
to any integration.

## The 5-Step Review Process

### Step 1: Define the Gap

Before investigating any external project, articulate the gap in your current
system as a concrete, testable claim.

**Example — Hermes Agent memory gap:**

| Current behavior | Desired behavior | Gap |
|-----------------|------------------|-----|
| Memory is flat key-value store with no retrieval ranking | Memory should rank results by relevance to current context | No ranking/scoring algorithm |
| No cross-session memory consolidation | Multiple related facts should be auto-merged into a summary | No consolidation logic |
| User must explicitly `memory save` | System should auto-extract and suggest memorable facts | No auto-extraction |

**Template:**

```
Current: <what happens now>
Desired: <what should happen>
Gap:     <what's missing (code, algorithm, data structure)>
```

### Step 2: Survey the Landscape

Search for projects that solve the gap. Sources:

- GitHub (README, issues, stars, last commit date)
- arXiv / academic papers
- Hacker News / Reddit / relevant communities
- Existing integrations in similar tools

For each candidate, collect:

| Field | Value |
|-------|-------|
| Project name | e.g., MemPalace |
| Repository | URL |
| Stars | Approximate community size |
| Last commit | Recency of maintenance |
| License | Compatibility with your project |
| Dependencies | What does it pull in? |
| API surface | How do you interact with it? |

### Step 3: Evaluate Fit

Score each candidate against your gap. Use these dimensions:

**1. Functional coverage (0-5)**
Does the project solve the gap? For MemPalace → Hermes memory:
- Does it have relevance ranking? (Yes — vector cosine similarity)
- Does it support consolidation? (Yes — summarization trigger)
- Does it auto-extract? (No — must be called explicitly)

Score: 3/5 (covers 2 of 3 gaps)

**2. Integration cost (0-5, higher = easier)**
- Is it a library or a service?
- Does it require a database (PostgreSQL, Redis)?
- How many lines of glue code needed?
- Does it need runtime dependencies the host system lacks?

Score: 4/5 (pure Python, no DB needed, ~50 lines of glue)

**3. Maintenance risk (0-5, higher = safer)**
- How active is the maintainer?
- Are there open issues about bugs?
- Is there a test suite?
- Would you fork or depend on pip?

Score: 3/5 (small team, moderate activity)

**4. Security surface (0-5, higher = safer)**
- Does the project make network calls?
- Does it execute user-provided code?
- Does it read/write arbitrary files?
- Are its dependencies audited?

Score: 4/5 (no network calls, no code execution)

### Step 4: Prototype Integration

Build a minimal proof-of-concept. Do not commit to full integration until
the prototype validates the approach.

**Minimal POC checklist:**

```
[ ] Install the dependency
[ ] Write a 20-line test that exercises the core gap
[ ] Verify the output is better than your current behavior
[ ] Measure performance (latency, memory)
[ ] Fail the prototype if it doesn't improve on the baseline
```

### Step 5: Decide

| Total score | Decision |
|-------------|----------|
| 16-20 | Integrate (low risk, high payoff) |
| 10-15 | Fork or adapt (good idea, needs changes) |
| 0-9 | Skip (not worth the complexity) |

For the MemPalace example: 3+4+3+4 = **14/20** → Fork or adapt.

## Pitfalls

- **Shiny object syndrome.** Not every cool project needs to be a dependency.
  Every dependency is a maintenance liability.
- **Not-invented-here bias.** If a 50-line library solves your gap perfectly,
  don't build a 500-line internal version.
- **Integration mode matters.** A library you import is different from a CLI
  you call is different from a service you run. Prefer the lightest coupling
  that achieves the goal.
- **License compatibility.** If your project is MIT, a GPL dependency
  contaminates the entire distribution. Check before protoyping.
- **Abandonment risk.** A project with 1 commit and 0 stars may solve your gap
  today but be unmaintained tomorrow. Fork it for stability.

## Persona integration

When evaluating external systems as a persona worker, adopt the appropriate
specialist role:

| Integration type | Role |
|-----------------|------|
| Backend/service integration | 🏗️ Backend Architect |
| Memory/knowledge systems | 🤖 AI Engineer |
| Build/deploy pipeline | ⚙️ DevOps Automator |
| Security review | 🔒 Security Engineer |

The Security Engineer persona should review the external project's code before
any integration is merged. See `security-audit-methodology.md` for the full
audit workflow.
