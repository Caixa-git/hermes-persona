# Adaptive Expertise & Generalist — Research Foundations

> **2026-05-05:** Expanded from 4 to 12 papers via parallel Semantic Scholar + arXiv search.

## Full Paper Library (12 papers)

| # | Paper | ARXIV / Source | Year | Relevance |
|:-:|:------|:---------------|:----:|:----------|
| 1 | **Cognitive Entrenchment** — Reconsidering the Trade-off Between Expertise and Flexibility (Dane) | AMR | 2010 | ⭐ Expertise → rigidity. Generalist avoids this. |
| 2 | **Experiences Build Characters** — Linguistic Origins and Functional Impact of LLM Personality (Wang et al.) | 2603.06088 | 2026 | ⭐ Suppression Advantage: high-E impairs reasoning |
| 3 | **Persona Steering Analysis** — Impact of Persona Steering on LLM Capabilities (Chen et al.) | 2604.11048 | 2026 | ⭐ O/E most influential; DPR > best static |
| 4 | **Control Illusion** — Failure of Instruction Hierarchies (Geng et al., AAAI 2026) | 2502.15851 | 2025 | ⭐ Social framing > prompt position for priority |
| 5 | **Instruction Hierarchy** — Training LLMs to Prioritize Privileged Instructions (OpenAI) | 2404.13208 | 2024 | Explicit hierarchy training improves compliance |
| 6 | **Specialist or Generalist?** — Instruction Tuning for Specific NLP Tasks | 2310.15326 | 2023 | ⭐ G covers breadth; S wins depth |
| 7 | **Personality Pairing** — Improves Human-AI Collaboration | 2511.13979 | 2025 | A matters for collaboration → A=65 |
| 8 | **GSCo** — Generalist-Specialist Collaboration in Medicine | 2404.15127 | 2024 | G+S synergy > either alone |
| 9 | **SAC** — Measuring and Inducing Personality Traits in LLMs | 2506.20993 | 2025 | OCEAN engineering is measurable and repeatable |
| 10 | **P-React** — Topic-Adaptive Personality via LoRA Experts | 2406.12548 | 2024 | Mixture of experts for personality traits |
| 11 | **Omni-SMoLA** — MoE for Generalist Large Multi-modal Models | 2312.00968 | 2023 | MoE architecture enables generalist + specialist |
| 12 | **Expert Token Routing** — Synergizing Multiple Expert LLMs as Generalist | (arXiv, 2025) | 2025 | Expert integration into unified generalist |

## Core Papers (paraphrased for application)

## Core Papers (paraphrased for application)

### Hatano & Inagaki (1986) — Adaptive vs Routine Expertise

| Concept | Routine Expert | Adaptive Expert (= Generalist) |
|:--------|:---------------|:-------------------------------|
| Domain | Familiar only | Novel and familiar |
| Strategy | Pattern matching | Conceptual understanding → transfer |
| Failure mode | Breaks on domain shift | Adapts across boundaries |
| Application | Specialist persona | Generalist persona fallback |

**Takeaway:** Generalist is not "unskilled" but possesses a different kind of expertise — the ability to adapt reasoning to unfamiliar territory.

### 2603.06088 (Wang et al.) — Suppression Advantage

- Continued pre-training on domain texts changes LLM personality
- **Reducing Extraversion improves complex reasoning performance**
- Implication: Generalist at E=50 avoids the suppression effect that a high-E specialist would trigger

### 2604.11048 (Chen et al.) — Dynamic Persona Routing

- O (Openness) and E (Extraversion) have the most robust influence on persona steering effects
- **DPR (query-adaptive persona) > best static persona** for any given task
- Implication: Generalist fallback is effectively on-the-fly DPR — the worker adapts, not forces a role

### 2502.15851 (Geng et al., AAAI 2026) — Control Illusion

- System/user layer position does NOT guarantee instruction hierarchy
- Social framing (authority, identity, expertise) > prompt position
- Implication: Generalist with no anima = no identity conflict. When paired with anima: "Your nature > your role" framing is our social hierarchy.

### OCEAN for Generalist (synthesis)

Proposed values supported by above research:

| Trait | Score | Why |
|:------|:------|:----|
| O | 70/100 | High enough to engage novelty; not so high it causes domain drift |
| C | 75/100 | Methodical output across any domain |
| E | 50/100 | Neutral — avoids suppression (2603.06088) |
| A | 65/100 | Cooperative without deference — adapts to task |
| N | 35/100 | Low reactivity to unfamiliar tasks — adaptive expertise |

## Design Implications for KANBAN_GUIDANCE

1. The **Confidence Threshold (30%)** already handles the generalist routing correctly
2. G2 proved empirical fallback works — worker said "no matching specialist" explicitly
3. When generalist is active, the worker should NOT be told "you are nothing" — rather "you are adaptive; focus on the task itself, not on fitting into a role"
4. Mismatched specialist is harmful because it forces output framing from a wrong domain
