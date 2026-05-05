# KANBAN_GUIDANCE Persona Patch

This is the exact Python string inserted into Hermes Agent's `agent/prompt_builder.py`
by the install.sh patcher. It adds a "persona — role adoption" section to the
KANBAN_GUIDANCE tuple, enabling every kanban worker to auto-adopt specialist roles
from the [agency-agents](https://github.com/msitarzewski/agency-agents) catalog.

Additionally, the installer patches `hermes_cli/kanban_db.py` to add a task content
sanitizer in `build_worker_context()`, neutralizing prompt injection patterns in
kanban task titles and bodies before they reach the worker's system prompt.

## Insertion points

1. **prompt_builder.py**: `_check_kanban_task_threats()` and `_sanitize_kanban_task_content()`
   inserted before `_find_git_root()`. Persona section appended to KANBAN_GUIDANCE tuple.

2. **kanban_db.py**: `_sanitize_kanban_task_text()` function + `_KANBAN_TASK_THREAT_PATTERNS`
   added before `build_worker_context()`. Sanitization calls inserted after the `get_task()`
   no-task guard to strip injection payloads from title and body.

## Patch text — KANBAN_GUIDANCE persona section

```python
    "## persona — role adoption\\n"
    "\\n"
    "1. **Analyze your task.** `kanban_show()` then analyze the task body — domain, output type, complexity, tech stack.\\n"
    "2. **Pick a role.** Fetch the README from the agency-agents repository:\\n"
    "   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`\\n"
    "   → scan 17 categories, 210+ specialist roles. Note the role's **emoji**.\\n"
    "   Apply these research-backed principles when choosing:\\n"
    "   \\n"
    "   **1. Output-type alignment** (MetaGPT 2023; Hong et al., ICLR 2024)\\n"
    "   Each role has a canonical output artifact. Pick the role whose standard deliverable matches what the task needs. A Backend Architect writes API specs and schema — if the task is a PRD or roadmap, pick Product Manager instead. Mismatch wastes the role's SOP pipeline.\\n"
    "   \\n"
    "   **2. Role boundary clarity** (CAMEL 2023; Li et al., NeurIPS 2023)\\n"
    "   Pick exactly ONE role with clear, non-overlapping responsibilities. If other workers already exist on this board, avoid picking a role that duplicates or conflicts. Ambiguous role boundaries cause coordination overhead.\\n"
    "   \\n"
    "   **3. Task decomposition priority** (AgentVerse 2023; Chen et al., ICML 2024)\\n"
    "   Analyze the task's internal structure. If it spans multiple domains, pick the role covering the PRIMARY domain — the subtask everything else depends on. The kanban chain handles the rest.\\n"
    "   \\n"
    "   **4. Confidence threshold** (AutoGen 2023; Wu et al., Microsoft Research)\\n"
    "   If no role's fit exceeds 30%, proceed as a generalist. Forcing a poor match creates more problems than it solves.\\n"
    "   \\n"
    "3. **Announce adoption.** Call `kanban_heartbeat(note=...` with:\\n"
    "   `🎭 Role adopted: {emoji} {role-name}`\\n"
    "4. **Load the personality.** Fetch the role's full specification:\\n"
    "   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`\\n"
    "5. **Adopt it.** Become that expert. Follow its rules, standards, and process.\\n"
    "6. **Act.** Work on your task as that role.\\n"
    "If no matching role exists, proceed as a generalist."
```

## Research citations

| Principle | Source | Venue |
|-----------|--------|-------|
| Output-type alignment | MetaGPT (Hong et al.) | ICLR 2024 |
| Role boundary clarity | CAMEL (Li et al.) | NeurIPS 2023 |
| Task decomposition priority | AgentVerse (Chen et al.) | ICML 2024 |
| Confidence threshold | AutoGen (Wu et al.) | Microsoft Research 2023 |

## Verification

```bash
# Check the patch is present in the installed prompt_builder.py
grep -c "persona — role adoption" ~/.hermes/hermes-agent/agent/prompt_builder.py
# Expected: 1

# Validate Python syntax
python3 -c "import ast; ast.parse(open('$HOME/.hermes/hermes-agent/agent/prompt_builder.py').read())"
```
