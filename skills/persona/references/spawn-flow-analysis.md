# Kanban Worker Spawn Flow — Complete API Message Assembly

**Source:** run_agent.py, hermes_cli/kanban_db.py, agent/prompt_builder.py, hermes_cli/oneshot.py
**Date:** 2026-05-05

## Spawn command

```
hermes -p persona-worker --skills kanban-worker --skills persona chat -q "work kanban task t_xxx"
```

## Message assembly order (actual API call)

When the worker's first inference is sent to the LLM API, messages are assembled in this exact order:

```
[1] system    ← _build_system_prompt(): SOUL.md + guidance + memory + skills + timestamp
                  (cached, rebuilt on context compression)
                  Layers within system prompt:
                    Layer 1:  SOUL.md / DEFAULT_AGENT_IDENTITY
                    Layer 2:  HERMES_AGENT_HELP_GUIDANCE
                    Layer 3:  MEMORY + SESSION_SEARCH + SKILLS + KANBAN_GUIDANCE guidance
                    Layer 4:  TOOL_USE_ENFORCEMENT_GUIDANCE
                    Layer 5:  system_message (caller-supplied)
                    Layer 6-7: persistent + external memory
                    Layer 8:  skills manifest
                    Layer 9:  context files (AGENTS.md)
                    Layer 10: timestamp + model info
                    Layer 11: environment hints
                    Layer 12: platform hints
                  + ephemeral_system_prompt (API-call-time)

[2] user      ← prefill_messages (--skills content)
                  "The user launched this session with the 'kanban-worker' skill preloaded..."
                  "The user launched this session with the 'persona' skill preloaded..."

[3] user      ← "work kanban task t_xxx" (from -q prompt)

--- tool loop starts ---

[4] tool      ← kanban_show() result: task title, body, parent handoffs, comments
[5] tool      ← curl README result: 172 roles list from agency-agents
[6] tool      ← curl {role}.md result: role file content (persona/identity)
[7] assistant ← "I am Backend Architect. Let me work on this task..."
```

## Key code paths

### System prompt build (run_agent.py:4869)
```python
def _build_system_prompt(self, system_message: str = None) -> str:
    # Layer 1: SOUL.md (if exists) → prompt_parts[0]
    # Layer 2-12: appended sequentially
    return "\n".join(prompt_parts)
```

### User message (run_agent.py:10595)
```python
user_msg = {"role": "user", "content": user_message}
messages.append(user_msg)
```

### Prefill insertion (run_agent.py:10998-11003)
```python
if self.prefill_messages:
    sys_offset = 1 if effective_system else 0
    for idx, pfm in enumerate(self.prefill_messages):
        api_messages.insert(sys_offset + idx, pfm.copy())
```

### Context compression rebuild (run_agent.py:9142-9144)
```python
self._invalidate_system_prompt()
new_system_prompt = self._build_system_prompt(system_message)  # ← reads SOUL.md fresh
self._cached_system_prompt = new_system_prompt
```

## Anima / Persona mapping

| Concept | Layer | What | Where it arrives |
|---------|-------|------|------------------|
| **Anima** (본성) | User messages | --skills content, user intent | prefill_messages / chat prompt |
| **Persona** (역할) | Tool results | curl-fetched role file | tool loop fetch result |
| **Identity** (Layer 1) | SOUL.md | Gateway or profile personality | system prompt build |

## Implications

1. **System prompt is immutable after spawn** — SOUL.md changes mid-session only take effect after context compression rebuilds the prompt
2. **Anima arrives before Persona** — --skills content (anima) is prefill, tool results (persona) come later → anima naturally has higher priority
3. **No tool for manual invalidation** — `_invalidate_system_prompt()` exists (run_agent.py:5417) but no public tool or API exposes it
4. **SOUL.md must exist BEFORE spawn** to be Layer 1 Identity from the start
