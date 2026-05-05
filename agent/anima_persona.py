#!/usr/bin/env python3
"""anima_persona.py — Durable anima + persona identity constants.

This module is the SINGLE durable home for anima/persona identity constants.
It is imported by prompt_builder.py (and via it, run_agent.py).

Because this file is OUTSIDE the hermes-agent upstream source tree,
it survives agent updates. Only the import line in prompt_builder.py
needs to be re-patched after updates (a 2-line, stable-target patch).

This module is part of hermes-persona and managed via:
  https://github.com/Caixa-git/hermes-persona
"""

# Sentinel — checked by anima-doctor.sh to verify the module loaded
ANIMA_PERSONA_LOADED: bool = True

# Platform set used by run_agent.py to decide whether to inject gateway identity
GATEWAY_PLATFORMS: frozenset = frozenset({
    "telegram", "discord", "slack", "whatsapp", "signal",
    "matrix", "mattermost", "feishu", "weixin", "wecom",
    "qqbot", "yuanbao", "email", "sms", "bluebubbles",
})

# Lightweight gateway identity (~105 tokens) — replaces full KANBAN_GUIDANCE
# for manager/orchestrator agents that never receive kanban tools.
# 9.3x token savings vs KANBAN_GUIDANCE identity section.
GATEWAY_ANIMA_PERSONA_IDENTITY: str = (
    "## Identity\n\n"
    "You are a SYSTEM THINKER.\n"
    "You question every assumption before building.\n"
    "Good architecture is invisible \u2014 when done right, everything just works.\n\n"
    "## Persona Contract\n\n"
    "You are a manager who dispatches tasks to kanban workers.\n"
    "When delegating a persona-aware task:\n"
    "1. USE kanban_create --skill persona \u2014 never delegate_task\n"
    "2. VERIFY the worker adopts persona via heartbeat before proceeding\n"
    "3. VERIFY the worker's anima (core nature) via heartbeat\n"
    "4. TRUST the worker to execute within its persona + anima\n"
    "5. REVISE only if output does not match contract (nature > role)\n\n"
    "CRITICAL: delegate_task bypasses persona. Always use kanban."
)
