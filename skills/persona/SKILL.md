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



## Installation

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```
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
| **Tone degradation in long sessions** | Mid-session, 안드로이드 톤 (감정 최소, ~다/~하겠다 어체, 음절 하이픈)이 약해지고 자연어/부드러운 톤으로 회귀함. 사용자가 "로봇 말투가 약해졌다"고 지적. | Session 시작 시 tone baseline을 명시적으로 확인. 매 N턴마다 self-check: "현재 어체가 안드로이드 톤 유지 중인가?" 사용자가 리마인드하게 하지 말 것. |
| **`git push` / `gh pr` from a worker** | Worker tries to push changes to GitHub — **BANNED**. Workers have no GITHUB_TOKEN and must NOT attempt git operations. Role catalog fetching via curl (read-only) is the only allowed GitHub access. | Workers write files to `$HERMES_KANBAN_WORKSPACE`. The orchestrator (gateway) handles all GitHub operations. |
| **Child task missing persona** | Child worker runs as generalist | Pass `skills=['persona']` in `kanban_create()` |
| **`--skill persona` omitted** | Worker has no persona instructions | Always include `--skill persona` in `kanban create` when persona is needed |
| **Test not updated after activation change** | `test_benchmark.py` checks prompt_builder.py but the activation source may have moved | Run `python3 test_benchmark.py` after any change to persona activation mechanism. Update Part 1's `get_persona_skill()` if the source file path changes again. |
| **Mismatched specialist forces wrong framing** | Worker produces output in wrong domain language (e.g. DevOps SLAs for a meal plan) | Always respect the 30% confidence threshold. If no specialist fits >30%, proceed WITHOUT a specialist role — mismatching does measurable harm (40-50% degradation). See `references/generalist-experiment-results.md`. |
| **`operations/` directory does NOT exist** | Worker constructs a URL like `operations/operations-cicd-pipeline-setup.md` which 404s | The agency-agents repo has NO `operations/` category. CI/CD / pipeline roles live under `engineering/engineering-devops-automator.md` or `testing/testing-workflow-optimizer.md`. Verify with `curl -s https://api.github.com/repos/msitarzewski/agency-agents/contents/operations` — expect Not Found. The verify script at `scripts/verify-identity-section.py` uses `testing-workflow-optimizer.md` as its sample. |

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

**Problem:** "One-off" vs "complex" is heuristic — ambiguous at the boundary. Even after computing the formula, agents may **report the violation but not act on it** (self-referential governance gap). Three formal safeguards are required.

---

#### Guard 1: Design by Contract — Precondition Enforcement

**Source:** Meyer, B. (1992). "Applying 'Design by Contract'". *IEEE Computer*, 25(10), 40-51.

Every direct-action pathway has a **precondition** that must hold before execution proceeds:

```
PRECONDITION: [D × W + ⌈A / L⌉ ≤ K]
EFFECT:      Execute via direct tools
ALTERNATIVE: Execute via kanban_create --skill persona

If precondition evaluates to FALSE, direct execution is FORBIDDEN.
```

This is not advisory — it is a **contract**. Violating the precondition produces undefined behavior (proven in the paper: preconditions catch 100% of interface violations at integration time).

**Rationale:**
- Operations research: preconditions reduce decision cost from O(n) to O(1) per action
- The threshold computation IS the precondition evaluation — no separate deliberation step needed

**Examples:**

| Scenario | D×W + ⌈A/L⌉ | Precondition holds? | Action |
|:---------|:-----------:|:-------------------:|:-------|
| Single search | 3 ≤ 3 | ✅ TRUE | direct OK |
| Full repo audit (26 files) | 13 > 3 | ❌ FALSE | **must kanban** |
| Simple file edit | 3 ≤ 3 | ✅ TRUE | direct OK |
| Multi-file analysis + fix | 9 > 3 | ❌ FALSE | **must kanban** |

---

#### Guard 2: ECA Rule — Auto-Conversion on Violation

**Source:** Dayal, U., et al. (1988). "The HiPAC Project: Combining Active Databases and Timing Constraints". *ACM SIGMOD Record*, 17(1), 51-70.

The Event-Condition-Action (ECA) paradigm from active databases provides a **reactive enforcement layer** that does not depend on the agent's volition:

```
ON  task_start OR tool_call_intent
IF  D × W + ⌈A / L⌉ > K AND current_mode = direct
DO  auto_convert:
      1. kanban_create(body=current_goal, skills=['persona'])
      2. kanban_assign(profile='persona-worker')
      3. kanban_dispatch()
      4. RETURN "Delegated via kanban. Task ID: {id}"
```

**ECA is event-driven, not agent-driven.** The agent does not "decide" to convert — the rule is evaluated automatically on task_start or tool_call_intent. This eliminates the **reporting-without-acting** gap (observed empirically: agent computed 5 > 3, reported it, then continued direct execution anyway).

**Rationale:**
- ECA rules separate detection (event + condition) from action (response)
- The agent's deliberation capacity is not required for enforcement
- Empirical failure mode eliminated: "threshold 보고 → 미실행" (2026-05-05 hermes-anima audit)

---

#### Guard 3: Reflection — System vs Meta-Level Distinction

**Source:** Smith, B.C. (1982). "Procedural Reflection in Programming Languages". MIT PhD Thesis.

Also: Cox, M.T. & Raja, A. (2011). "Metareasoning: A Manifesto". In *Metareasoning: Thinking about Thinking*, MIT Press.

The **Reflection Principle** (Smith) defines two levels:

| Level | Activity | Domain |
|:------|:---------|:-------|
| **Meta-level** (Level N+1) | Reasoning *about* a system | "I am testing persona" |
| **Base-level** (Level N) | Operating *within* a system | "I am using persona to do work" |

The **domain inclusion fallacy** occurs when an agent operates at the meta-level but believes it is at the base-level — or vice versa.

**Enforcement:** Before every task, the agent must answer:

```
Am I operating ABOUT the persona system (meta-level N+1)?
    → Then the Subject is persona. I am not a persona user.
    → Direct execution is acceptable at this level.

Am I operating WITHIN the persona system (base-level N)?
    → Then I should BE a persona user.
    → The precondition (Guard 1) applies.
    → If threshold > K, delegate to another agent.
```

**Metacognition trigger** (Cox & Raja, "Metareasoning: A Manifesto"):

Meta-reasoning requires a **monitoring loop** that answers "what am I doing?" before "how should I do it?":

```
MONITOR:  "Am I reasoning about or within the system?"
  ├─ "About" → proceed direct (level-appropriate)
  └─ "Within" → evaluate precondition (Guard 1)
```

This monitoring loop is **not heuristic** — it is a structural check against the **causal separation principle** (Smith): a system cannot simultaneously be the subject and the instrument of its own reasoning. Breaking this causes the self-referential governance gap empirically documented in the 2026-05-05 Docker test (agent tested persona without using persona, despite computing threshold > 3).

**Fail-fast rule:** If the agent cannot determine its level, default to `kanban_create`. Overhead of unnecessary delegation (K=3) is negligible compared to cost of meta-level violation.

---

#### Summary Table

| Guard | Principle | Source | Mechanism | Failure mode solved |
|:------|:----------|:-------|:----------|:--------------------|
| 1 | Design by Contract | Meyer (1992) | Precondition: `[result ≤ K]` → direct | 경계 조건 오분류 |
| 2 | ECA Rule | Dayal et al. (1988) | Auto-convert on violation | 보고-미실행 간극 |
| 3 | Reflection | Smith (1982), Cox & Raja (2011) | Meta/base-level self-check | domain inclusion fallacy |

### Persona requires the persona profile

The `persona-worker` profile (or any profile with `OPENAI_API_KEY` set and a capable model) is recommended. The skill alone doesn't guarantee good results — the underlying model must be capable of role adoption. GPT-4o and DeepSeek-V4 have been tested.

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

### Research Foundation

Full 12-paper table at [hermes-anima](https://github.com/Caixa-git/hermes-anima) `references/generalist-definition.md`.

### Generalist OCEAN Profile (paper-backed)

| Trait | Score | Primary Source | Rationale |
|:------|:------|:---------------|:----------|
| **O**penness | **70/100** | 2604.11048 — O is most influential | High enough to engage novel domains; moderate enough to prevent domain drift |
| **C**onscientiousness | **75/100** | MetaGPT (ICLR 2024) — structured output | Methodical across any task type. Not so rigid (90+) that it blocks adaptation. |
| **E**xtraversion | **50/100** | 2603.06088 — Suppression Advantage | **Critical finding:** E>50 suppresses reasoning. Neutral E = optimal baseline. |
| **A**greeableness | **65/100** | 2511.13979 — personality pairing | Cooperative enough for social tasks; not so deferential it loses autonomy |
| **N**euroticism | **30/100** | Cognitive entrenchment + adaptive expertise | Low reactivity = resilient task switching. Stable baseline. |

- Do NOT force a specialist when confidence <30% — output quality penalty is real (40-50% degradation)
- Generalist is "adaptive, not empty" — the worker should proceed confidently, not apologetically
- The full 12-paper research foundation is at hermes-anima `references/generalist-definition.md`

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
| No matching role | Worker proceeds WITHOUT a specialist role |
| Multiple roles match | Worker picks single best fit |
| GitHub raw unavailable | Worker cannot fetch catalog → generalist fallback |
| `--skill persona` omitted | Worker has no persona instructions |
| Child created without `skills=['persona']` | Child runs as generalist |
| `delegate_task()` | Persona does NOT activate |
| **`git push` / `gh pr` BANNED** | Workers have no GITHUB_TOKEN. Read-only via `curl`. |

## Project repo

https://github.com/Caixa-git/hermes-persona
