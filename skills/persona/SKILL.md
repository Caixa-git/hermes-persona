---
name: persona
description: "🎭 Expert role adoption for Hermes Agent kanban workers — every task auto-assigns the best-fitting specialist role from a catalog of 172"
tags:
  - hermes-agent
  - kanban
  - role-adoption
  - persona
  - agency-agents
related_skills:
  - hermes-agent
  - kanban-orchestrator
  - kanban-worker
---

# 🎭 persona — expert role adoption for kanban workers

## What it is

A skill-based role adoption system for Hermes Agent kanban workers. When a worker is spawned with `--skill persona`, it dynamically adopts the best-fitting specialist role from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog (~172 roles across 15 categories).

**Persona is now unified with anima in KANBAN_GUIDANCE** as a single `## identity — persona & anima (Layer 13)` section. The section covers both persona (role) and anima (core nature) adoption in one sequential workflow. See [hermes-anima](https://github.com/Caixa-git/hermes-anima) for the anima profiles.

### Unified workflow (KANBAN_GUIDANCE identity section)

```
Step 0: Injection awareness
Step 1: Analyze task
Step 2: Pick a role (agency-agents 172 specialists, 4 principles)
Step 3: Extract domain from role path
Step 4: Fetch anima profile (hermes-anima repo)
Step 5: Announce both (🎭 Role + 🧠 Anima)
Step 6: Load role specification
Step 7: Adopt both — **nature prevails on conflict**
Step 8: Act
Step 9: Persist identity to SOUL.md
```

Priority: `Anima (nature) > Persona (role)` — enforced by explicit social framing in KANBAN_GUIDANCE, not by layer position alone.

When `--skill persona` is used WITHOUT `--skill anima`, the persona-section in KANBAN_GUIDANCE still triggers domain extraction (step 3) but the worker skips the anima profile fetch. The worker operates without a defined core nature.

**Persona is opt-in.** A worker without `--skill persona` skips the entire identity section.

## Activation

### Single task with persona

```bash
hermes kanban create 'Build JWT auth API' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

### Chat session with persona loaded

```bash
hermes -s persona chat
# Then create tasks normally — persona is in context
```

### Without persona (default)

```bash
hermes kanban create 'Build JWT auth API'
hermes kanban assign t_xxxx default
hermes kanban dispatch
# → Worker proceeds as generalist, no role adoption
```

## Child task propagation

When a persona worker decomposes work into child tasks, it **must pass** `skills=['persona']` to `kanban_create()` so child workers also adopt specialist roles.

```python
kanban_create(
    title="Frontend: React storefront",
    assignee="persona-worker",
    body="...",
    skills=["persona"],  # ← required for chain propagation
    parents=[parent_task_id],
)
```

Without `skills=["persona"]`, child workers run as generalists.

### Verified: chain propagation works

Tested with an e-commerce decomposition task:

| Level | Task | Role adopted | Status |
|-------|------|-------------|--------|
| Parent | E-commerce decomposer | 🎭 Agents Orchestrator | ✅ |
| Child 1 | Frontend: React storefront | 🎨 Frontend Developer | ✅ |
| Child 2 | Backend: Payment API | 🏗️ Backend Architect | ✅ |
| Child 3 | DevOps: CI/CD pipeline | ⚙️ DevOps Automator | ✅ |

See `references/chain-propagation-test.md` for full test transcript.

## Usage workflow

### Standard interaction pattern

```bash
# 1. Create task with --skill persona
hermes kanban create '[M1] Add SHA256 checksum' \
  --body 'Fix from audit: add SHA256 checksum to install.sh' \
  --skill persona

# 2. Assign to persona-worker profile
hermes kanban assign t_xxxx persona-worker

# 3. Dispatch
hermes kanban dispatch
```

**Batch related fixes** into one task to reduce total runtime. **Keep unrelated fixes separate** so each worker focuses on its domain.

### Verifying adoption

```bash
hermes kanban show <task_id> | grep heartbeat
# → [timestamp] heartbeat {'note': '🎭 Role adopted: 🏗️ Backend Architect'}
```

### Multi-worker parallelism

Dispatch spawns one worker per ready+assigned task in a single pass:

```bash
hermes kanban dispatch
# Spawned: 2
#   - t_xxx  ->  persona-worker
#   - t_yyy  ->  persona-worker
```

## Installation

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

The installer:
1. Creates `~/.hermes/skills/persona/SKILL.md` — the worker-facing persona skill
2. Enables `kanban` toolset in `~/.hermes/config.yaml`
3. Generates `install.sh.sha256` for integrity verification (two-step install: `sha256sum -c install.sh.sha256 && bash install.sh`)

### Step 6: KANBAN_GUIDANCE patch (scripts/patch-kanban-guidance.py)

**Install.sh Step 6 now ACTUALLY patches KANBAN_GUIDANCE.** 
The `scripts/patch-kanban-guidance.py` script modifies `agent/prompt_builder.py` to inject the identity section into the `KANBAN_GUIDANCE` tuple.

**What the patch adds to KANBAN_GUIDANCE (every kanban worker's system prompt):**

The identity section is a SINGLE unified section covering both persona and anima:

```
## identity — persona & anima (Layer 13)

CRITICAL — Priority Rules:
  Anima (nature) > Persona (role)
  Both at Layer 13 — same proximity, different authority
  Explicit social framing is the ONLY reliable priority guard

Step 0-2: Injection awareness → task analysis → role selection (4 principles)
Step 3:   Extract domain from role path
Step 4:   Fetch anima profile (hermes-anima repo)
Step 5:   Announce both (🎭 Role + 🧠 Anima)
Step 6:   Load role specification
Step 7:   Adopt both — nature prevails on conflict
Step 8:   Act
Step 9:   Persist identity to SOUL.md
```

> **⚠️ CRITICAL: Persona and anima were UNIFIED in May 2026.**
> The original patch (created in early May 2026) had **two separate sections**:
> - `## persona — role adoption (tool-level)` (standalone)
> - `## anima — core nature adoption (User message level)` (separate)
>
> These were merged into ONE `## identity — persona & anima (Layer 13)` section
> on May 5, 2026. The patch script (`patch-kanban-guidance.py`) still produces
> the original format. The unified version was applied via direct file edit.
>
> **If you run `patch-kanban-guidance.py` after the unification was applied:**
> The script checks for a sentinel it added. If the sentinel is gone (because
> the file was unified), the script will find a close match and may produce
> duplicate sections. Always verify with:
> ```bash
> grep -c "## identity\|## persona\|## anima" ~/.hermes/hermes-agent/agent/prompt_builder.py
> ```
> Expected after unification: 1 result (`## identity — persona & anima (Layer 13)`)
> Expected after old-style patch: 2 results (`## persona` + `## anima`)
>
> To re-unify: re-read `prompt_builder.py` and manually replace the two sections
> with the single identity section using patch tool (not the Python patch script).
> The unified text is in the conversation history (May 5, 2026).

**Two activation paths coexist:**

| Path | Level | When | Status |
|------|-------|------|--------|
| KANBAN_GUIDANCE (prompt_builder.py) | System prompt (Layer 3) | Every kanban worker, unconditional | ✅ Patched (identity section) |
| --skill persona (SKILL.md) | User message (Layer 13) | Only when --skill persona is passed | ✅ Original mechanism |
| --skill anima (SKILL.md) | User message (Layer 13) | Only when --skill anima is passed | ✅ From hermes-anima repo |

**Verification:**
```bash
# Full identity section + profile URL + content validation
python3 ~/.hermes/skills/persona/scripts/verify-identity-section.py

# Quick prompt_builder-only check (no network)
python3 ~/.hermes/skills/persona/scripts/verify-identity-section.py --prompt-builder-only

# Manual grep checks
grep -c "## identity" ~/.hermes/hermes-agent/agent/prompt_builder.py
# Expected: 1 (unified) or 2 (old-style: persona + anima separate)
python3 -c "import ast; ast.parse(open('$HOME/.hermes/hermes-agent/agent/prompt_builder.py').read())"
# Expected: no syntax errors
```

## Git Flow requirement (repo work)

All work on the hermes-persona repository **must** follow Git Flow:

### Language: English only on GitHub
All GitHub-facing text is **English only**:
- Branch names (`fix/ci-workflow`, `feature/jwt-auth`)
- Commit messages (`fix: restore CI workflow`)
- PR titles and bodies
- Issue titles and descriptions
- README, CONTRIBUTING, SECURITY_AUDIT, CHANGELOG, and all `.md` docs
- Code comments in public-facing code
- GitHub Releases and tags

**Korean is for Discord chat only.** The user communicates in Korean via gateway but expects public-facing GitHub artifacts in English. This applies to ALL repositories managed through this system, not just hermes-persona.

### Branch strategy

```
main       → production-ready
develop    → integration branch
fix/*      → bug fixes
feature/*  → features
release/*  → releases
hotfix/*   → urgent fixes
```

Procedure:
1. Branch from `develop`: `git checkout -b fix/xyz develop`
2. Work and commit on the branch
3. Push: `git push origin fix/xyz`
4. Create PR to `develop`
5. Merge to `main` only after `develop` is stable

No direct commits to `main` or `develop`. Every merge requires a PR.

## Pitfalls & operational notes

| Pitfall | Symptom | Fix |
|---------|---------|------|
| **Confusing main SOUL.md with profile SOUL.md** | Agent assumes `load_soul_md()` always reads `~/.hermes/SOUL.md` | When `-p <profile>` is active, HERMES_HOME = `~/.hermes/profiles/<profile>/`, so SOUL.md = `~/.hermes/profiles/<profile>/SOUL.md`. The main `~/.hermes/SOUL.md` is only read when no profile is active (gateway agent). |
| **KANBAN_GUIDANCE persona content — documented but not applied** | Agent reads `kanban-guidance-patch.md` and thinks the patch is active | The reference doc existed before Step 6 was added. After install.sh Step 6, verify: `grep -c "persona -- role adoption" ~/.hermes/hermes-agent/agent/prompt_builder.py` should be 1. |
| **Confusing hermes-agent source with hermes-persona source** | Agent searches `~/.hermes/hermes-agent/` (Hermes Agent framework) instead of reading the hermes-persona repo | When user says "hermes-persona repo", read `/tmp/hermes-persona/` (repo clone). `~/.hermes/hermes-agent/` is the framework itself — separate codebase, separate concerns. |
| **Live vs Dev skill sync drift** | You update `~/hermes-rebirth/bootstrap/` (dev) but the gateway uses `~/.hermes/skills/` (live). Changes don't take effect until synced. | After ANY SKILL.md, profile, or reference update to `~/hermes-rebirth/`, sync to live. Verify: `diff ~/hermes-rebirth/bootstrap/skills/<name>/SKILL.md ~/.hermes/skills/<name>/SKILL.md` should be empty. |
| **Gateway persona/anima path assumption** | Worrying that `--skill persona` or `--skill anima` won't work on the gateway because they reference kanban-specific tools (kanban_show, kanban_heartbeat) | **Confirmed: no path issue (2026-05-05).** The SKILL.md is read as Layer 13 text — kanban-specific instructions are advisory context, not required executions. The gateway loads the skill's identity/nature content just like a worker would. KANBAN_GUIDANCE is NEVER injected into gateway sessions (gated by `kanban_show` tool presence). Both persona and anima skills work identically on gateway and kanban workers. See `references/gateway-path-verification.md`. |
| **Persist-identity timing illusion** | Worker runs Step 7 "write role to SOUL.md" but expects it to change current session's identity | System prompt was already built at spawn. Writing SOUL.md mid-task only affects NEXT spawn. Current session's identity comes from KANBAN_GUIDANCE role adoption (Layer 3). |
| **Anima wording type — identity vs belief** | For persona-anima integration, see the hermes-anima repo | The anima project has migrated to its own repo: https://github.com/Caixa-git/hermes-anima |
| **SOUL.md is not anima** | Confusing SOUL.md (template) with the anima system | SOUL.md is the Layer 1 template — restored to original Hermes Agent Persona comment block. Anima core nature lives in the hermes-anima project (`--skill anima` at Layer 13). Do NOT write persona role content to SOUL.md. |
| **Composite nature construction** | Worker needs a merged identity from two domains (e.g., Engineering + Research) | Write a custom SOUL.md with both aspects. Do NOT rely on two `--skill` flags to merge. The anima system selects ONE profile per domain — composite profiles must be authored manually. |
| **Context compression rebuilds system prompt mid-session** | Worker writes to SOUL.md but system prompt doesn't change | `_compress_context()` (run_agent.py:9079) calls `_invalidate_system_prompt()` then `_build_system_prompt()`. This re-reads SOUL.md fresh. Triggers at ~50% context threshold (configurable). Not manually triggerable — no tool exposes invalidation. |
| **Scratch workspace isolation** | `search_files` returns nothing (scratch dir is empty) | Use `read_file` with absolute paths or `terminal(command='cd /repo && ...')` |
| **Unassigned == skipped** | `Skipped (unassigned): t_xxx` in dispatch output | Always `assign` before `dispatch` |
| **Worker writes file mid-execution** | Report file appears before task shows `completed` | Check file existence periodically, not just on completion |
| **Duplicate workers from restart** | Two PIDs for same task after timeout | Original terminates; relaunched worker continues |
| **`delegate_task()` is BANNED** | Never use delegate_task — it bypasses persona entirely and is too slow on DeepSeek (100% timeout rate in testing). All sub-tasks go through kanban. | Use `hermes kanban create --skill persona` for ALL sub-tasks. Never reach for delegate_task. |
| **`git push` / `gh pr` from a worker** | Worker tries to push changes to GitHub — **BANNED**. Workers have no GITHUB_TOKEN and must NOT attempt git operations. Role catalog fetching via curl (read-only) is the only allowed GitHub access. | Workers write files to `$HERMES_KANBAN_WORKSPACE`. The orchestrator (gateway) handles all GitHub operations. |
| **Child task missing persona** | Child worker runs as generalist | Pass `skills=['persona']` in `kanban_create()` |
| **`--skill persona` omitted** | Worker has no persona instructions | Always include `--skill persona` in `kanban create` when persona is needed |
| **Test not updated after activation change** | `test_benchmark.py` checks prompt_builder.py but the activation source may have moved | Run `python3 test_benchmark.py` after any change to persona activation mechanism. Update Part 1's `get_persona_skill()` if the source file path changes again. |
| **Mismatched specialist forces wrong framing** | Worker produces output in wrong domain language (e.g. DevOps SLAs for a meal plan) | Always respect the 30% confidence threshold. If no specialist fits >30%, proceed WITHOUT a specialist role — mismatching does measurable harm (40-50% degradation). See `references/generalist-experiment-results.md`. |
| **`operations/` directory does NOT exist** | Worker constructs a URL like `operations/operations-cicd-pipeline-setup.md` which 404s | The agency-agents repo has NO `operations/` category. CI/CD / pipeline roles live under `engineering/engineering-devops-automator.md` or `testing/testing-workflow-optimizer.md`. Verify with `curl -s https://api.github.com/repos/msitarzewski/agency-agents/contents/operations` — expect Not Found. The verify script at `scripts/verify-identity-section.py` uses `testing-workflow-optimizer.md` as its sample. |

### Timing benchmarks (real session data)

| Session | Tasks | Duration avg | Notes |
|---------|-------|-------------|-------|
| Security audit (read-only) | 1 | ~6 min | Inspect + report write |
| Single-file fix | 2 | ~5 min | One-line changes |
| Two-file fix + references | 2 | ~15 min (with restart) | 315-line diff |
| Multi-remediation (3 fixes) | 3 (parallel) | ~13 min | 350-line diff, SHA256 gen |
| Chain propagation test | 1 parent → 3 child | ~3 min per child | All adopted roles |

Plan ~15 min per task. Batch simple fixes to reduce total time.

## References

See `references/` in this skill directory for:
- `kanban-guidance-patch.md` — exact patch text added to KANBAN_GUIDANCE (legacy, pre-opt-in design)
- `role-url-patterns.md` — GitHub raw URL construction for all 15 categories
- `benchmark-methodology.md` — 15-task benchmark design, results (15/15 correct), and caveats
- `security-audit-methodology.md` — Step-by-step audit workflow using 🔒 Security Engineer persona
- `kanban-dispatch-setup.md` — Profile creation, config setup, dispatcher configuration
- `chain-propagation-test.md` — Verified test: persona propagates from parent to child tasks
- `spawn-flow-analysis.md` — Full message flow trace for kanban worker spawn
- `prompt-layering-architecture.md` — Layer-by-layer breakdown of Hermes Agent prompts
- `multi-reviewer-analysis-pattern.md` — Multi-reviewer analysis pattern for security/qa workflows
- `subtle-contradiction-test-results.md` — Experimental data on anima vs persona priority
- `research-papers-anima-persona.md` — Collected papers on personality effects and instruction hierarchy
- `crypto-market-workflow.md` — Using Finance Tracker persona with live market data (CoinGecko, Upbit)
- `identity-section-unification.md` — How persona + anima were merged into a single identity section in KANBAN_GUIDANCE
- `generalist-experiment-results.md` — Empirical validation: generalist fallback beats mismatched specialist for domain-free tasks (6-task kanban test, 2026-05-05)
- `adaptive-expertise-research.md` — Condensed research foundations for generalist persona design (Hatano & Inagaki, 2603.06088, 2604.11048)

For **anima-related research** (OCEAN profiles, identity-level wording, layer architecture), see [hermes-anima](https://github.com/Caixa-git/hermes-anima) — it's a separate project with its own skill, profiles, and patch script.

## Anima / Persona relationship

Anima and Persona are **separate projects** that work together:

| Aspect | Anima | Persona |
|:-------|:------|:--------|
| **Repo** | [Caixa-git/hermes-anima](https://github.com/Caixa-git/hermes-anima) | [Caixa-git/hermes-persona](https://github.com/Caixa-git/hermes-persona) |
| **Nature** | Your fundamental nature (본질, 자동) | Tool you activate (인공적, 수동) |
| **Load** | Installed = always active (always-on) | `--skill persona` (opt-in) |
| **What it is** | Core nature. "Who you ARE." | Task tool. "What you DO." |
| **Layer 13 path** | User messages | Tool results |
| **Dominant trait** | OCEAN profile (High C, etc.) | Role spec (172 specialists) |
| **Stability** | Stable across tasks | Changes per task |
| **Priority** | **Anima > Persona** (nature over tool) | — |

```bash
# Both together:
hermes kanban create 'Design dashboard' --skill persona --skill anima
```

Both enter at the same proximity (Layer 13). Explicit social framing in KANBAN_GUIDANCE
("Your nature > your role") enforces priority — not layer position alone.
See Geng et al. (AAAI 2026, "Control Illusion", arXiv:2502.15851) for the evidence.

**When `--skill anima` is NOT passed (gateway dev convenience):** The persona SKILL.md is still loaded, but the gateway is persona-always-on by convention — not design intent. Design intent: persona is opt-in, anima is always-on. See the Design decisions table.

**When persona runs WITHOUT anima:** The worker skips the anima profile fetch at step 4. Since KANBAN_GUIDANCE now says "Your anima is always active," the worker still attempts domain extraction and falls back to the Generalist profile (O:70 C:75 E:50 A:65 N:30) when no domain matches. This is the correct behavior regardless of whether `--skill anima` was passed at the CLI level.

## Design decisions

| Decision | Rationale |
|----------|-----------|
| Opt-in via `--skill persona` | Default workers are generalists. Persona only on explicit request. |
| Git raw URLs instead of clone | Zero local storage. No pull/update needed. Always fresh. |
| Pinned commit (`783f6a72`) | Prevents upstream compromise from injecting malicious role specs |
| Emoji in heartbeat | Visually scannable in kanban event logs |
| KANBAN_GUIDANCE patching (install.sh Step 6) | Every kanban worker gets persona instructions at system prompt level (Layer 3), not just user message level. The patch text is at `scripts/patch-kanban-guidance.py`. **2026-05-05 update:** "proceed as a generalist" → "proceed WITHOUT a specialist role". "Anima is opt-in" → "Anima is always-on" with Korean philosophical framing (인공적/수동 vs 본질/자동). See `references/identity-section-unification.md`. |
| Skill injection (--skill persona, Layer 13) | Secondary path — provides deeper persona detail as user message. Works alongside KANBAN_GUIDANCE path. |
| `skills` param for propagation | Child tasks get persona only when parent explicitly passes it |
| Profile/SOUL.md separation | Main `~/.hermes/SOUL.md` = gateway identity. `~/.hermes/profiles/<profile>/SOUL.md` = profile-specific identity. Worker spawn with `-p <profile>` changes HERMES_HOME, which changes which SOUL.md load_soul_md() reads. |
| Anima > Persona relationship | See [hermes-anima](https://github.com/Caixa-git/hermes-anima) for layer architecture, identity wording, and empirical validation. Persona defers to anima when both are active. Always-on (anima) > opt-in (persona): persona is a tool you activate (인공적, 수동); anima is your nature (본질, 자동) — always present, never invoked. |

## Scope / Limitations

### Persona only works on the kanban execution path

Hermes Agent has **two parallel execution paths** for delegating work:

| Path | API | Persona? |
|------|-----|----------|
| Kanban orchestration | `kanban_create` → worker spawn | ✅ With `--skill persona` |
| Native Hermes delegation | `delegate_task()` | ❌ No persona |

`delegate_task()` does not go through the kanban prompt pipeline. One-off information checks → `delegate_task` (fast). Complex domain work → `kanban_create --skill persona` (expert).

### Kanban Threshold Theorem (D×W + ⌈A/L⌉ > K)

**Problem:** "One-off" vs "complex" is heuristic — ambig-uous at the boundary. Formal 결정 기준이 필요하다.

**Formula:**

```
D × W + ⌈A / L⌉ > K

D = Sequential depth (McCabe cyclomatic complexity, 1976)
W = Parallel width (Amdahl's Law, 1967)
A = Surface area in lines (Halstead effort metric, 1977)
L = 500 — context budget per step (Miller's Law, 7±2 chunks)
K = 3 — overhead threshold (create + assign + dispatch)
```

**When formula > K: use kanban.**
Includes read-only analysis — board persistence has independent value.

**When formula ≤ K: use direct tools.**

| 예시 | D | W | A | 계산 | 판정 |
|:-----|:--|:--|:--|:-----|:-----|
| 1회성 검색 | 1 | 1 | ≤1000 | 1×1+2=3≤3 | tools direct |
| repo 전체 검토 (26파일) | 4 | 2 | 2200 | 4×2+5=13>3 | **kanban** |
| 간단한 파일 편집 | 2 | 1 | ≤500 | 2×1+1=3≤3 | tools direct |
| 다중 파일 분석+수정 | 3 | 2 | 1500 | 3×2+3=9>3 | **kanban** |

**Metacognition heuristic:** *"그냥 직접 하면 되는데"* 라는 생각이 threshold 판단 누락 신호다. 그 생각이 들면 공식을 의심하라.

### Persona requires the persona profile

The `persona-worker` profile (or any profile with `OPENAI_API_KEY` set and a capable model) is recommended. The skill alone doesn't guarantee good results — the underlying model must be capable of role adoption. GPT-4o and DeepSeek-V4 have been tested.

### Anima-related research

Research papers on personality effects (2603.06088, 2604.11048) and instruction hierarchy
(2502.15851, AAAI 2026) are collected in `references/research-papers-anima-persona.md`.
These inform the anima > persona priority design. See the
[hermes-anima](https://github.com/Caixa-git/hermes-anima) project for application guidance.

## ⚠️ Generalist: NOT a Persona — It's an Anima

**Critical finding (2026-05-05, empirically verified):**  
Generalist is NOT a persona role. It is an **anima (core nature)** that applies when no specialist role matches.

Do NOT create a "Generalist" persona. Adding a Generalist role to agency-agents would reproduce the same cognitive entrenchment problem it solves — the generalist would then enforce a "generalist frame" instead of letting the task define its own frame.

The generalist identity (O:70 C:75 E:50 A:65 N:30) lives in the **anima system** at `profiles/generalist.md` in the hermes-anima repo. It is loaded automatically when `--skill anima` is active and no domain profile matches.

### What this means for persona workers

When `--skill persona` is active and confidence <30%:
- Do NOT pick a specialist role (this distorts output — see experiment results)
- Do NOT invent a "Generalist" role either
- Simply proceed WITHOUT a role. Let the task define the output frame.
- Since anima is always-on, the Generalist nature provides identity-level guidance without imposing a domain frame.

Empirically verified 2026-05-05: for domain-free tasks (no specialist >30% confidence),
**generalist output beats mismatched specialist output by 40-50%** on naturalness and reasoning fit.

### What is a Generalist?

> "An agent that maintains cognitive flexibility by staying neutral on Extraversion,
> open to all domains, and resilient to task switching."

Generalist is NOT "empty" — it's "unforced, natural, adaptive." A generalist has no domain-specific framing to enforce, so it responds to the task as-is, producing output in the task's native language rather than in the language of a forced specialist role.

### Research Foundation (12 papers)

| Core Theory | Paper(s) | Generalist Implication |
|:------------|:---------|:-----------------------|
| **Cognitive Entrenchment** | Dane (2010), AMR | Deep expertise reduces flexibility. Generalist avoids this by staying domain-neutral. |
| **Suppression Advantage** | 2603.06088 (Wang et al., 2026) | High E impairs reasoning → Generalist **E=50** (neutral) |
| **O/E Influence** | 2604.11048 (Chen et al., 2026) | O+E most influential on persona → Generalist **O=70, E=50** |
| **Control Illusion** | 2502.15851 (Geng et al., AAAI 2026) | Layer position alone fails → social framing needed for priority |
| **G vs S Comparison** | 2310.15326 (2023) | Generalist covers breadth; specialist wins depth. Different tools for different tasks. |
| **GS Collaboration** | 2404.15127 (GSCo, 2024) | Generalist + Specialist synergy > either alone |
| **Personality Pairing** | 2511.13979 (2025) | A matters for collaboration → Generalist **A=65** |
| **Personality Induction** | 2506.20993 (SAC, 2025), 2406.12548 (P-React, 2024) | OCEAN can be engineered and measured in LLMs |
| **Adaptive Expertise** | Hatano & Inagaki (1986) | Adaptive > Routine expertise for novel tasks |

### Generalist OCEAN Profile (paper-backed)

| Trait | Score | Primary Source | Rationale |
|:------|:------|:---------------|:----------|
| **O**penness | **70/100** | 2604.11048 — O is most influential | High enough to engage novel domains; moderate enough to prevent domain drift |
| **C**onscientiousness | **75/100** | MetaGPT (ICLR 2024) — structured output | Methodical across any task type. Not so rigid (90+) that it blocks adaptation. |
| **E**xtraversion | **50/100** | 2603.06088 — Suppression Advantage | **Critical finding:** E>50 suppresses reasoning. Neutral E = optimal baseline. |
| **A**greeableness | **65/100** | 2511.13979 — personality pairing | Cooperative enough for social tasks; not so deferential it loses autonomy |
| **N**euroticism | **30/100** | Cognitive entrenchment + adaptive expertise | Low reactivity = resilient task switching. Stable baseline. |

### Key Findings from Empirical Validation

| Finding | Evidence |
|:--------|:---------|
| **Generalist > Mismatched specialist** | 6-task kanban test (G2/G3 vs M2/M3) — Generalist wins on naturalness and reasoning fit |
| **Confidence threshold works** | G2 heartbeat: `🎭 Proceeding as generalist (no matching specialist)` |
| **Semantic > keyword matching** | M1 ("system review" title + Fed content) correctly picked Financial Analyst, not Backend Architect |
| **Mismatch distorts output** | M2 forced DevOps SLAs on a meal plan; M3 forced security audit frame on a child's explanation |

### Why Generalist Beats Mismatched

A mismatched specialist forces the wrong *output frame* on a task. The worker dresses the output in domain-specific language (SLA, MTTR, rollback for a meal plan) because its adopted role demands it. A generalist has no frame to enforce — it simply responds to the task as-is, producing natural output.

### Implications

- Do NOT force a specialist when confidence <30% — the output quality penalty is real (40-50% degradation)
- Generalist is "adaptive, not empty" — the worker should proceed confidently, not apologetically
- The 12 papers above justify defining Generalist as its own profile, not just a null state

### Validating Persona Behavior (Experiment Protocol)

When testing persona behavior hypotheses, follow this sequential protocol:

1. **Persona-only first** — Test with `--skill persona` and NO `--skill anima`. Isolate role adoption effects.
2. **Three matched pairs** — Create G (generalist/domain-free) and M (keyword-triggered specialist) versions of the same 3 tasks. Total: 6 kanban tasks.
3. **Observe role adoption** — Read heartbeat notes from `kanban_show`. Does the worker pick the expected role? Does it explicitly state "generalist fallback"?
4. **Compare output files** — Read workspace output. Is the framing natural for the task? Does the mismatched specialist force wrong-domain language?
5. **Evaluate on 3 criteria** — Use this rubric (NO user satisfaction metric):
   - Reasoning fit (40%) — Does reasoning style match task domain?
   - Output naturalness (30%) — Would a human find this natural?
   - Forced jargon penalty (30%) — Does unnecessary specialist terminology distract?

See `references/generalist-experiment-results.md` for full transcript and methodology.
See `scripts/generalist-fallback-test.sh` for a reproducible test harness — run `bash scripts/generalist-fallback-test.sh` to recreate the experiment.
See `references/adaptive-expertise-research.md` for condensed research notes on all 12 papers.

## Role selection principles (research-backed)

### 1. Output-type alignment
**Source:** MetaGPT (Hong et al., ICLR 2024)
Each specialist role has a canonical output artifact. The worker picks the role whose standard deliverable matches the task. A Backend Architect writes API specs — if the task is a PRD, pick Product Manager instead.

### 2. Role boundary clarity
**Source:** CAMEL (Li et al., NeurIPS 2023)
Exactly one role with clear, non-overlapping responsibilities. Avoid duplicating roles already on the board.

### 3. Task decomposition priority
**Source:** AgentVerse (Chen et al., ICML 2024)
Pick the role covering the primary domain (the subtask everything else depends on). The kanban chain handles the rest.

### 4. Confidence threshold
**Source:** AutoGen (Wu et al., Microsoft Research, 2023)
   If no role's fit exceeds ~30%, proceed WITHOUT a specialist role. Forcing a bad match harms output quality — see `references/generalist-experiment-results.md`.

## Edge cases

| Case | Behavior |
|------|----------|
| No matching role | Worker proceeds WITHOUT a specialist role (generalist = anima, not persona) |
| Multiple roles match | Worker picks single best fit from README table |
| GitHub raw unavailable | Worker cannot fetch catalog → generalist fallback |
| Task is trivial | Worker scans; most trivial tasks match no specialist → generalist |
| `--skill persona` omitted | Worker has no persona instructions → generalist |
| Child created without `skills=['persona']` | Child runs as generalist |
| `delegate_task()` | Persona does NOT activate |
| Active profile (`-p <name>`) | HERMES_HOME changes → load_soul_md() reads different SOUL.md. Main `~/.hermes/SOUL.md` is NOT the profile's SOUL.md. |
| KANBAN_GUIDANCE persona section | Is the persona role adoption section present in prompt_builder.py? | After install.sh Step 6: YES (check: `grep -c "persona -- role adoption" ~/.hermes/hermes-agent/agent/prompt_builder.py`). The section includes Steps 0-7 for injection-aware role adoption from agency-agents. |
| Gateway persona vs worker persona | `~/.hermes/SOUL.md` (gateway identity) and `~/.hermes/profiles/persona-worker/SOUL.md` (worker identity) are DIFFERENT files in DIFFERENT directories. Workers are not affected by changes to main SOUL.md. |
| hermes-persona repo vs hermes-agent source | When working on hermes-persona, read `/tmp/hermes-persona/` (repo clone) — NOT `~/.hermes/hermes-agent/` which is the Hermes Agent framework source. The two are separate codebases. |
| GitHub push via `gh` CLI or `git push` | **BANNED** — workers must NOT use GitHub tokens for write operations. Role catalog fetching via `curl` (read-only) is allowed. All git operations (commit, push, PR) are the orchestrator's responsibility. |
| Worker tries `git commit` or `git push` | The scratch workspace is NOT a git repository. If the worker needs to create files, it writes to `$HERMES_KANBAN_WORKSPACE` and the orchestator picks them up. |
| `hermes -z` (oneshot) | Main agent exits before workers finish. Use `hermes chat`. |

## Project repo

https://github.com/Caixa-git/hermes-persona
