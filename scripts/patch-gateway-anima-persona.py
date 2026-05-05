#!/usr/bin/env python3
"""
Patch hermes-agent source to add Gateway Anima+Persona identity.

Injects GATEWAY_ANIMA_PERSONA_IDENTITY and GATEWAY_PLATFORMS into
agent/prompt_builder.py, and adds the injection logic to run_agent.py.

This gives the gateway agent (메카 위진수) a lightweight Anima identity
and a Persona Contract for delegating to kanban workers.

Run after hermes-agent install if the install script hasn't applied this.

Multi-strategy patching:
  1. Exact-string match (fast, works on clean installs)
  2. Regex fallback (tolerates whitespace/format differences)
  3. AST-level insertion (--force mode, most robust)

A backup (.bak) is created before every write.
"""

import os
import re
import sys
import shutil

HERMES_HOME = os.environ.get("HERMES_HOME",
    os.path.expanduser("~/.hermes"))

FORCE_MODE = "--force" in sys.argv


def backup(path):
    """Create .bak copy before modifying."""
    bak = path + ".bak"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
        print(f"  Backup: {bak}")


def try_exact(text, old_str):
    """Strategy 1: exact match."""
    if old_str in text:
        return old_str
    return None


def try_regex(text, pattern):
    """Strategy 2: regex match, returns (matched_text, replacement_group)."""
    m = re.search(pattern, text, re.DOTALL)
    if m:
        return m.group(0)
    return None


def fail(msg, expected_ctx=None, found_ctx=None):
    """Print diagnostic error and exit."""
    print(f"  ❌ {msg}", file=sys.stderr)
    if expected_ctx:
        print(f"     Expected context snippet: {expected_ctx[:80]!r}", file=sys.stderr)
    if found_ctx:
        print(f"     Nearest match attempt:   {found_ctx[:80]!r}", file=sys.stderr)
    sys.exit(1)


IMPORT_MARKER = "from agent.prompt_builder import ("
IMPORT_ALT = r"from agent\.prompt_builder import\s*\("

INJECT_FIRST_LINE = "        # Pointer to the hermes-agent skill + docs"


def patch_prompt_builder():
    path = os.path.join(HERMES_HOME, "hermes-agent", "agent", "prompt_builder.py")
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        return False

    with open(path) as f:
        text = f.read()

    # Guard: already patched
    if "GATEWAY_ANIMA_PERSONA_IDENTITY" in text:
        print("Already patched: GATEWAY_ANIMA_PERSONA_IDENTITY found")
        return True

    backup(path)

    # ── Step 1: Insert import ──
    import_stmt = (
        'from agent.anima_persona import ANIMA_PERSONA_LOADED, '
        'GATEWAY_PLATFORMS, GATEWAY_ANIMA_PERSONA_IDENTITY  # noqa: F401\n'
        'from utils import atomic_json_write\n'
    )

    # Strategy 1: exact match of "from utils import atomic_json_write"
    marker = "from utils import atomic_json_write"
    if marker in text:
        text = text.replace(marker, import_stmt)
        print("  Import: exact match")
    else:
        # Strategy 2: regex
        m = re.search(INJECT_ALT, text)
        if m:
            # Find the next import line after the prompt_builder import block
            pos = m.end()
            rest = text[pos:]
            next_import = re.search(r'^from\s+\S+\s+import', rest, re.MULTILINE)
            if next_import:
                insert_pos = pos + next_import.start()
                text = text[:insert_pos] + import_stmt + text[insert_pos:]
                print("  Import: regex match")
            else:
                # Strategy 3: AST level — find first top-level import
                lines = text.split('\n')
                insert_line = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        insert_line = i
                        break
                text = text[:insert_pos_start] + import_stmt + text[insert_pos_start:]
                print("  Import: AST fallback")
        else:
            print("  Import: no match found, skipping", file=sys.stderr)
            return False

    # Write after import step
    with open(path, 'w') as f:
        f.write(text)

    print(f"  Patched: {path}")
    return True


def patch_run_agent():
    path = os.path.join(HERMES_HOME, "hermes-agent", "run_agent.py")
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        return False

    with open(path) as f:
        text = f.read()

    # Guard: already patched
    if "GATEWAY_ANIMA_PERSONA_IDENTITY" in text:
        print("Already patched: import found")
        return True

    backup(path)

    # ── Step 1: Add import ──
    import_line = "from agent.prompt_builder import ("
    new_import = (
        "from agent.prompt_builder import (\n"
        "    DEFAULT_AGENT_IDENTITY, PLATFORM_HINTS,\n"
        "    MEMORY_GUIDANCE, SESSION_SEARCH_GUIDANCE, SKILLS_GUIDANCE,\n"
        "    HERMES_AGENT_HELP_GUIDANCE,\n"
        "    KANBAN_GUIDANCE,\n"
        "    GATEWAY_ANIMA_PERSONA_IDENTITY, GATEWAY_PLATFORMS,\n"
        "    build_nous_subscription_prompt,\n"
        ")"
    )

    match = try_exact(text, import_line)
    if match:
        text = text.replace(
            "from agent.prompt_builder import (\n"
            "    DEFAULT_AGENT_IDENTITY, PLATFORM_HINTS,\n"
            "    MEMORY_GUIDANCE, SESSION_SEARCH_GUIDANCE, SKILLS_GUIDANCE,\n"
            "    HERMES_AGENT_HELP_GUIDANCE,\n"
            "    KANBAN_GUIDANCE,\n"
            "    build_nous_subscription_prompt,\n"
            ")",
            new_import
        )
        print("  Import: exact match")
    else:
        # Regex: find from agent.prompt_builder import (...) block
        m = re.search(
            r'from agent\.prompt_builder import\s*\(([^)]+)\)',
            text, re.DOTALL
        )
        if m:
            old_block = m.group(0)
            # Inject GATEWAY_ANIMA_PERSONA_IDENTITY, GATEWAY_PLATFORMS, before build_nous
            new_block = old_block.replace(
                "build_nous_subscription_prompt",
                "GATEWAY_ANIMA_PERSONA_IDENTITY, GATEWAY_PLATFORMS,\n    build_nous_subscription_prompt"
            )
            text = text.replace(old_block, new_block)
            print("  Import: regex match")
        else:
            # Last resort: just add after KANBAN_GUIDANCE
            text = text.replace(
                "from agent.prompt_builder import (",
                import_line + "\n    GATEWAY_ANIMA_PERSONA_IDENTITY, GATEWAY_PLATFORMS,"
            )
            print("  Import: forced insert")
            return False

    # ── Step 2: Add injection logic ──
    injection_code = (
        "\n"
        "        # Gateway Anima+Persona identity -- lightweight version of the\n"
        "        # KANBAN_GUIDANCE identity section, injected on messaging platforms\n"
        "        # that never have kanban tools loaded. See hermes-persona for context.\n"
        "        if (\n"
        "            self.platform in GATEWAY_PLATFORMS\n"
        "            and \"kanban_show\" not in self.valid_tool_names\n"
        "        ):\n"
        "            prompt_parts.append(GATEWAY_ANIMA_PERSONA_IDENTITY)\n"
    )

    # Strategy 1: find `# Pointer to the hermes-agent skill` comment
    pointer_line = "        # Pointer to the hermes-agent skill + docs for user questions about Hermes itself."
    if pointer_line in text:
        text = text.replace(pointer_line, injection_code + pointer_line)
        print("  Injection: exact match")
    else:
        # Strategy 2: find prompt_parts.append pattern after SOUL.md fallback
        fallback_marker = "# Fallback to hardcoded identity"
        if fallback_marker in text:
            # Find the next blank line or code line after the fallback block
            idx = text.index(fallback_marker)
            after = text[idx:]
            lines = after.split('\n')
            inject_pos = 0
            for i, line in enumerate(lines):
                if line.strip() == "" or (line.strip().startswith('#') and 'SOUL.md' not in line and 'Fallback' not in line):
                    continue
                if line.strip().startswith('prompt_parts') or line.strip().startswith('# Pointer'):
                    inject_pos = idx + sum(len(l) + 1 for l in lines[:i])
                    break
            if inject_pos:
                text = text[:inject_pos] + injection_code + text[inject_pos:]
                print("  Injection: fallback marker match")
            else:
                print("  Injection: no match found, skipping", file=sys.stderr)
                return False
        else:
            # Strategy 3: find that exact comment anywhere
            if "hermes-agent skill" in text or "about Hermes itself" in text:
                for marker_variant in ["hermes-agent skill", "about Hermes itself"]:
                    idx = text.find(marker_variant)
                    if idx >= 0:
                        # Find start of that line
                        line_start = text.rfind('\n', 0, idx) + 1
                        text = text[:line_start] + injection_code + text[line_start:]
                        print(f"  Injection: keyword match ('{marker_variant}')")
                        break
                else:
                    print("  Injection: no match found", file=sys.stderr)
                    return False
            else:
                print("  Injection: no match found", file=sys.stderr)
                return False

    with open(path, 'w') as f:
        f.write(text)
    print(f"  Patched: {path}")
    return True


if __name__ == "__main__":
    print("🔧 Gateway Anima+Persona Patch")
    print("=" * 40)

    ok_a = patch_prompt_builder()
    ok_b = patch_run_agent()

    if ok_a and ok_b:
        print("\n✅ Patch complete")
        sys.exit(0)
    else:
        print("\n⚠️  Partial patch — some steps failed", file=sys.stderr)
        sys.exit(1)
