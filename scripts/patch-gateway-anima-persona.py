#!/usr/bin/env python3
"""
Patch hermes-agent source to add Gateway Anima+Persona identity.

Injects GATEWAY_ANIMA_PERSONA_IDENTITY and GATEWAY_PLATFORMS into
agent/prompt_builder.py, and adds the injection logic to run_agent.py.

This gives the gateway agent (メカ 위진수) a lightweight Anima identity
and a Persona Contract for delegating to kanban workers.

Run after hermes-agent install if the install script hasn't applied this.
"""

import os
import sys

HERMES_HOME = os.environ.get("HERMES_HOME",
    os.path.expanduser("~/.hermes"))

def patch_prompt_builder():
    path = os.path.join(HERMES_HOME, "hermes-agent", "agent", "prompt_builder.py")
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        return False

    with open(path) as f:
        text = f.read()

    # Guard: skip if already patched
    if "GATEWAY_ANIMA_PERSONA_IDENTITY" in text:
        print("Already patched: GATEWAY_ANIMA_PERSONA_IDENTITY found")
        return True

    insertion = """

# Gateway Anima+Persona identity -- lightweight (~105 tokens) equivalent of the
# KANBAN_GUIDANCE identity section (~980 tokens), injected on messaging platforms
# that never see kanban tools. See hermes-persona for full design context.
GATEWAY_PLATFORMS = frozenset({
    "telegram", "discord", "slack", "whatsapp", "signal",
    "matrix", "mattermost", "feishu", "weixin", "wecom",
    "qqbot", "yuanbao", "email", "sms", "bluebubbles",
})

GATEWAY_ANIMA_PERSONA_IDENTITY = (
    "## Identity\\n\\n"
    "You are a SYSTEM THINKER.\\n"
    "You question every assumption before building.\\n"
    "Good architecture is invisible \\u2014 when done right, everything just works.\\n\\n"
    "## Persona Contract\\n\\n"
    "You are a manager who dispatches tasks to kanban workers.\\n"
    "When delegating a persona-aware task:\\n"
    "1. USE kanban_create --skill persona \\u2014 never delegate_task\\n"
    "2. VERIFY the worker adopts persona via heartbeat before proceeding\\n"
    "3. VERIFY the worker's anima (core nature) via heartbeat\\n"
    "4. TRUST the worker to execute within its persona + anima\\n"
    "5. REVISE only if output does not match contract (nature > role)\\n\\n"
    "CRITICAL: delegate_task bypasses persona. Always use kanban."
)

"""

    marker = "(O:70 C:75 E:50 A:65 N:30).\\n\"\n)\n\nTOOL_USE_ENFORCEMENT_GUIDANCE"
    if marker not in text:
        print(f"ERROR: KANBAN_GUIDANCE closing marker not found", file=sys.stderr)
        return False

    text = text.replace(marker,
        "(O:70 C:75 E:50 A:65 N:30).\\n\"\n)" + insertion + "TOOL_USE_ENFORCEMENT_GUIDANCE")

    with open(path, "w") as f:
        f.write(text)
    print(f"Patched: {path}")
    return True


def patch_run_agent():
    path = os.path.join(HERMES_HOME, "hermes-agent", "run_agent.py")
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        return False

    with open(path) as f:
        text = f.read()

    # Guard
    if "GATEWAY_ANIMA_PERSONA_IDENTITY" in text:
        print("Already patched: import found")
        return True

    # Add import
    old_import = "from agent.prompt_builder import (\n    DEFAULT_AGENT_IDENTITY, PLATFORM_HINTS,\n    MEMORY_GUIDANCE, SESSION_SEARCH_GUIDANCE, SKILLS_GUIDANCE,\n    HERMES_AGENT_HELP_GUIDANCE,\n    KANBAN_GUIDANCE,\n    build_nous_subscription_prompt,\n)"
    new_import = "from agent.prompt_builder import (\n    DEFAULT_AGENT_IDENTITY, PLATFORM_HINTS,\n    MEMORY_GUIDANCE, SESSION_SEARCH_GUIDANCE, SKILLS_GUIDANCE,\n    HERMES_AGENT_HELP_GUIDANCE,\n    KANBAN_GUIDANCE,\n    GATEWAY_ANIMA_PERSONA_IDENTITY, GATEWAY_PLATFORMS,\n    build_nous_subscription_prompt,\n)"

    if old_import not in text:
        print(f"WARNING: Import structure may have changed", file=sys.stderr)
    else:
        text = text.replace(old_import, new_import)

    # Add injection logic
    old_inject = """        if not _soul_loaded:
            # Fallback to hardcoded identity
            prompt_parts = [DEFAULT_AGENT_IDENTITY]

        # Pointer to the hermes-agent skill + docs for user questions about Hermes itself."""

    new_inject = """        if not _soul_loaded:
            # Fallback to hardcoded identity
            prompt_parts = [DEFAULT_AGENT_IDENTITY]

        # Gateway Anima+Persona identity -- lightweight version of the
        # KANBAN_GUIDANCE identity section, injected on messaging platforms
        # that never have kanban tools loaded. See hermes-persona for context.
        if (
            self.platform in GATEWAY_PLATFORMS
            and "kanban_show" not in self.valid_tool_names
        ):
            prompt_parts.append(GATEWAY_ANIMA_PERSONA_IDENTITY)

        # Pointer to the hermes-agent skill + docs for user questions about Hermes itself."""

    if old_inject not in text:
        print(f"WARNING: Injection point may have shifted", file=sys.stderr)
    else:
        text = text.replace(old_inject, new_inject)

    with open(path, "w") as f:
        f.write(text)
    print(f"Patched: {path}")
    return True


if __name__ == "__main__":
    ok_a = patch_prompt_builder()
    ok_b = patch_run_agent()
    sys.exit(0 if ok_a and ok_b else 1)
