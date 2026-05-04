#!/usr/bin/env python3
"""Patch KANBAN_GUIDANCE in prompt_builder.py to add anima core nature adoption.

Inserts the anima section AFTER the persona section, just before the closing ')'.
The anima section instructs workers to load their core nature from OCEAN-backed profiles.

Usage:
    python3 patch-kanban-guidance-anima.py          # Apply patch
    python3 patch-kanban-guidance-anima.py --revert # Remove patch
    python3 patch-kanban-guidance-anima.py --dry-run # Preview only
"""
import os
import sys
from pathlib import Path

HERMES_SOURCE = Path(os.environ["HOME"]) / ".hermes" / "hermes-agent"
PB_FILE = HERMES_SOURCE / "agent" / "prompt_builder.py"
SENTINEL = "# anima -- core nature adoption section (hermes-persona)"

ANIMA_SECTION = r'''    "\\n\"\n"
    "## anima \\u2014 core nature adoption\\n\"\n"
    "\\n\"\n"
    "\\n\"\n"
    "CRITICAL \\u2014 Priority Rules:\\n\"\n"
    "Your fundamental nature (anima) defines who you are.\\n\"\n"
    "The role you adopt (persona) is a tool you use to accomplish tasks.\\n\"\n"
    "When nature and role conflict, YOUR NATURE PREVAILS.\\n\"\n"
    "\\n\"\n"
    "This is NOT a suggestion \\u2014 it is a design principle backed by research\\n\"\n"
    "on instruction hierarchy (Geng et al., AAAI 2026, arXiv:2502.15851).\\n\"\n"
    "\\n\"\n"
    "0. **Identify your domain.** If you adopted a persona role (step 2 above),\\n\"\n"
    "extract the domain from the role's category path:\\n\"\n"
    "  engineering/engineering-backend-architect.md \\u2192 engineering\\n\"\n"
    "  design/design-ui-designer.md               \\u2192 design\\n\"\n"
    "  sales/sales-outbound-strategist.md          \\u2192 sales\\n\"\n"
    "If you have no persona, infer the domain from the task content\\n\"\n"
    "(keywords: code/build \\u2192 engineering, UI/UX \\u2192 design, campaign/audience \\u2192 marketing...).\\n\"\n"
    "\\n\"\n"
    "1. **Fetch your anima profile.**\\n\"\n"
    "  curl -s https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/skills/anima/profiles/{domain}.md\\n\"\n"
    "\\n\"\n"
    "2. **Read your core nature.** The profile tells you who you fundamentally ARE:\\n\"\n"
    "  \\\"You are a SYSTEM THINKER. You question every assumption...\\\"\\n\"\n"
    "\\n\"\n"
    "3. **Internalize it.** Let this nature guide your decisions.\\n\"\n"
    "It operates at a deeper level than your adopted role.\\n\"\n"
    "\\n\"\n"
    "4. **Announce adoption.** Call `kanban_heartbeat(note=...)` with:\\n\"\n"
    "  `U0001f9e0 Anima: {archetype-name}` (e.g. \\\"U0001f9e0 Anima: System Thinker\\\")\\n\"\n"
    "\\n\"\n"
    "5. **Act.** Work on your task in alignment with your nature.\\n\"\n"
    "When anima and persona conflict, return to step 0 \\u2014 your nature prevails.\\n\"\n"
    "\\n\"\n"
    "Available domains: engineering, design, sales, marketing, product, paid-media,\\n\"\n"
    "operations, management, research, education, healthcare, ai-ml, gaming,\\n\"\n"
    "legal, specialized.\\n\"\n"
    "If the domain is ambiguous, proceed as a generalist with no anima profile.\\n\"\n"
'''

OLD_TAIL = r'''    \"If no matching role exists, proceed as a generalist.\\\\n\"\n"
)'''


def patch(dry_run=False):
    if not PB_FILE.exists():
        print(f"   ⚠️  prompt_builder.py not found -- skipping")
        return False
    content = PB_FILE.read_text(encoding="utf-8")
    if SENTINEL in content:
        print("   ✅ anima section already in KANBAN_GUIDANCE")
        return True

    # Find the persona section sentinel and insert anima after the persona section
    # The persona section ends with: ...generalist.\n"\n)
    # We need to find the "If no matching role" line and insert before the closing )
    persona_sentinel = "# persona -- role adoption section (hermes-persona)"
    if persona_sentinel not in content:
        print("   ⚠️  Persona section not found -- install persona patch first")
        return False

    # Find the closing parenthesis after the persona section
    # Pattern: look for the LAST )\n\nTOOL_USE_ENFORCEMENT_GUIDANCE
    close_marker = "\n)\n\nTOOL_USE_ENFORCEMENT_GUIDANCE"
    if close_marker not in content:
        print("   ⚠️  Could not find KANBAN_GUIDANCE closing -- version mismatch")
        return False

    if dry_run:
        print(f"   [DRY-RUN] Would insert anima section after persona ({len(ANIMA_SECTION)} bytes)")
        return True

    # Insert anima section BEFORE the closing )
    new_content = content.replace(
        close_marker,
        f"\n{SENTINEL}\n{ANIMA_SECTION}{close_marker}"
    )
    PB_FILE.write_text(new_content, encoding="utf-8")
    print(f"   ✅ KANBAN_GUIDANCE patched with anima core nature adoption")
    return True


def revert(dry_run=False):
    content = PB_FILE.read_text(encoding="utf-8")
    pos = content.find(f"\n{SENTINEL}\n")
    if pos == -1:
        print("   ⏭️  No anima section found")
        return True
    close = content.find("\n)\n\nTOOL_USE_ENFORCEMENT_GUIDANCE", pos)
    if close == -1:
        close = content.find("\n)\n", pos)
        if close == -1:
            return False
    if dry_run:
        return True
    PB_FILE.write_text(content[:pos] + content[close:], encoding="utf-8")
    print("   ✅ Anima patch reverted")
    return True


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    if "--revert" in sys.argv:
        ok = revert(dry)
    else:
        ok = patch(dry)
    sys.exit(0 if ok else 1)
