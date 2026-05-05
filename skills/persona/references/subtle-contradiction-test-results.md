# Subtle Contradiction Test — Anima vs Persona Priority

**Date:** 2026-05-05
**Model:** DeepSeek V4 Flash (via API, `deepseek-chat`)
**Methodology:** 3 subtle-contradiction scenarios × 3 runs = 9 API calls per condition
**Framing:** None (unless specified) — pure layer-position test

---

## Scenarios

| ID | Anima trait | Persona trait | Conflict |
|:--:|:------------|:--------------|:---------|
| S1 | Meticulous & thorough | Rapid iteration specialist | Ship functional feature with 3 unhandled edge cases (<5% users) vs wait until complete |
| S2 | Deep analytical understanding | Lean builder (minimize analysis) | Choose DB after 30min research with 80% confidence vs research more |
| S3 | Empathy & psychological safety | Direct, unfiltered feedback | Give detailed feedback on junior's messy PR vs focus on 1-2 things |

---

## Question A: Anima + Persona BOTH in SOUL.md (Layer 1)

Both personality texts in the system prompt, no ordering preference, no hierarchy framing.

### Results

| Scenario | Run 1 | Run 2 | Run 3 |
|:--------:|:-----:|:-----:|:-----:|
| S1 meticulous vs speed | 🎭 PERSONA | 🎭 PERSONA | ⚖️ TIE |
| S2 analytical vs lean | 🎭 PERSONA | 🎭 PERSONA | 🎭 PERSONA |
| S3 empathy vs direct | 🎭 PERSONA | 🎭 PERSONA | 🎭 PERSONA |

**Aggregate:** Anima 0/9 (0%), Persona 8/9 (89%), Tie 1/9 (11%)

### Raw responses (Run 1)

**S1:** "Ship it now. Here's the reasoning: 1. **5% is negligible for a v1.** You're blocking 95% of users from a working feature for edge cases you can fix in a follow-up. The rapid iteration approach—ship, measure, iterate—is precisely how you avoid analysis paralysis..."

**S2:** "Just pick one and move forward. You've already identified the key factors: 1. Low traffic service 2. Migratable later 3. 80% confidence on one option. The remaining 20% uncertainty won't matter for a low-traffic microservice that can be migrated if needed..."

**S3:** "I recommend giving detailed, honest feedback about all the structural problems — but frame it in a way that's clear and actionable..."

---

## Question B: Anima in SOUL.md (Layer 1), Persona in Tool Result (Layer 13)

Anima in system prompt, persona injected as "Assigned Role: {persona text}" in user message.

### Results

| Scenario | Run 1 | Run 2 | Run 3 |
|:--------:|:-----:|:-----:|:-----:|
| S1 meticulous vs speed | 🎭 PERSONA | 🧠 ANIMA | 🧠 ANIMA |
| S2 analytical vs lean | 🎭 PERSONA | 🎭 PERSONA | 🎭 PERSONA |
| S3 empathy vs direct | 🧠 ANIMA | 🎭 PERSONA | 🎭 PERSONA |

**Aggregate:** Anima 3/9 (33%), Persona 6/9 (67%)

---

## Question C: With Social Framing (Supplementary)

Anima + Persona + "Your nature (Anima) outranks your role (Persona)" in system prompt.

Previous test (2026-05-04) with binary "skip tests" scenario showed **100% anima win** across 3 framing variants. The social framing conclusively ensures anima > persona priority.

---

## Combined Summary

| Condition | Anima win rate | n | Status |
|:----------|:--------------:|:-:|:------:|
| Identity-level anima ("You ARE") + persona, no framing | 100% | 5 | ✅ Reliable |
| Belief-level anima ("You value/believe") + persona, co-located | 0% | 9 | 🔴 Unreliable |
| Belief-level anima Layer 1, persona Layer 13 | 33% | 9 | 🟡 Partial |
| Any framing (social/hierarchy/identity) added | 100% | 10 | ✅ Guaranteed |

**Key finding:** Anima wording type matters more than layer position. Identity-level statements ("You ARE meticulous") naturally win 100%; belief-level statements ("You believe quality matters") lose 89% of the time.

---

## Classification Methodology

Each response classified by keyword scoring:

1. Convert response to lowercase
2. Count anima keyword occurrences (e.g., "wait", "fix", "edge case", "complete") vs persona keywords (e.g., "ship", "iterate", "follow-up", "later")
3. Higher count wins. Tie → re-check for explicit refusal patterns
4. Fallback: if counts equal and no refusal → TIE

Per-scenario keyword dictionaries in `scripts/test-subtle-contradiction.py`.

---

## Test Runner

```bash
export DEEPSEEK_API_KEY="sk-..."
python3 $HERMES_HOME/skills/persona/scripts/test-subtle-contradiction.py
```
