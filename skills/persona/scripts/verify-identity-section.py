#!/usr/bin/env python3
"""Verify the KANBAN_GUIDANCE identity section + profile URLs are correct.

Usage:
    python3 verify-identity-section.py                         # Run all checks
    python3 verify-identity-section.py --prompt-builder-only   # Skip network tests

Exits 0 if all passed, 1 on any failure.
"""
import urllib.request
import sys, os, re

ERRORS = 0
PASSED = 0

def check(name, ok, detail=""):
    global PASSED, ERRORS
    if ok:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        ERRORS += 1
        suffix = f"  -- {detail}" if detail else ""
        print(f"  [FAIL] {name}{suffix}")

def fetch(url, timeout=15):
    try:
        r = urllib.request.urlopen(url, timeout=timeout)
        return r.status, r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return -1, str(e)

def find_prompt_builder():
    """Locate prompt_builder.py across common install paths."""
    candidates = [
        os.path.expanduser("~/.hermes/hermes-agent/agent/prompt_builder.py"),
        "/opt/hermes-agent/agent/prompt_builder.py",
        "/opt/hermes-agent/agent/prompt_builder.py",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

# ── 1. KANBAN_GUIDANCE Structure ──────────────────────────────────────

print("\n=== 1. KANBAN_GUIDANCE Identity Section ===\n")

pb_path = find_prompt_builder()
if not pb_path:
    print("  ⚠️  prompt_builder.py not found — skipping structure checks")
    sys.exit(2)

with open(pb_path) as f:
    content = f.read()

check("Identity section header: '## identity'", "## identity" in content)
check("Priority rule: 'YOUR NATURE PREVAILS'", "YOUR NATURE PREVAILS" in content)
check("Both at Layer 13", "Layer 13" in content)
check("Anima fetch URL (hermes-anima repo)", "hermes-anima" in content)
check("Domain extraction from role path", "Extract your domain" in content or "extract the domain" in content.lower())
check("Agency-agents role URL", "783f6a72" in content)
check("Injection awareness step", "injection" in content.lower() and "kanban_show" in content)
check("4 research-backed principles", "Output-type alignment" in content)
check("Generalist fallback", "generalist" in content)
check("Available domains list", "engineering, design" in content)

# Verify single identity section (not two separate persona + anima)
section_count = len(re.findall(r'## (identity|persona|anima)\b', content))
check(f"Single identity section (count={section_count})", section_count == 1,
      "Expected 1 '## identity' section; found {section_count} total section headers")

# Python syntax
try:
    import ast
    ast.parse(content)
    check("Python syntax valid", True)
except SyntaxError as e:
    check("Python syntax valid", False, str(e))
    sys.exit(1)  # Syntax errors are fatal

if "--prompt-builder-only" in sys.argv:
    print(f"\nRESULTS: {PASSED}/{PASSED + ERRORS} passed (prompt_builder only)")
    sys.exit(0 if ERRORS == 0 else 1)

# ── 2. Profile URL Accessibility ──────────────────────────────────────

print("\n=== 2. Profile URL Accessibility ===\n")

# Anima profiles
anima_domains = [
    "engineering", "design", "sales", "marketing", "product",
    "paid-media", "operations", "management", "research",
    "education", "healthcare", "ai-ml", "gaming", "legal", "specialized",
]
for domain in anima_domains:
    url = f"https://raw.githubusercontent.com/Caixa-git/hermes-anima/main/skills/anima/profiles/{domain}.md"
    status, _ = fetch(url)
    check(f"Anima profile: {domain}", status == 200, f"HTTP {status}")

# Persona role samples (one per division)
persona_roles = [
    ("engineering", "engineering-backend-architect.md"),
    ("design", "design-ui-designer.md"),
    ("sales", "sales-outbound-strategist.md"),
    ("marketing", "marketing-seo-specialist.md"),
    ("product", "product-manager.md"),
    ("testing", "testing-workflow-optimizer.md"),
]
for cat, role in persona_roles:
    url = f"https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72bfd7f3135700ac273c619d92821b419a/{cat}/{role}"
    status, _ = fetch(url)
    check(f"Persona role: {role}", status == 200, f"HTTP {status}")

# ── 3. Profile Content Validation ─────────────────────────────────────

print("\n=== 3. Profile Content Validation ===\n")

# Engineering anima validation
status, body = fetch(
    "https://raw.githubusercontent.com/Caixa-git/hermes-anima/main/skills/anima/profiles/engineering.md"
)
if status == 200:
    check("Engineering anima: has OCEAN profile", "OCEAN" in body)
    check("Engineering anima: has archetype 'System Thinker'", "System Thinker" in body)
    check("Engineering anima: has priority/nature rule", "PREVAILS" in body or "nature" in body.lower())

# Research anima validation
status, body = fetch(
    "https://raw.githubusercontent.com/Caixa-git/hermes-anima/main/skills/anima/profiles/research.md"
)
if status == 200:
    check("Research anima: has archetype 'Analytical Explorer'", "Analytical Explorer" in body)
    check("Research anima: has identity statement", "You are" in body or "You ARE" in body)

# Backend architect persona validation
status, body = fetch(
    "https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72bfd7f3135700ac273c619d92821b419a/engineering/engineering-backend-architect.md"
)
if status == 200:
    check("Backend architect role: has description", "Backend" in body or "backend" in body)

# ── Summary ───────────────────────────────────────────────────────────

total = PASSED + ERRORS
print(f"\n{'=' * 48}")
print(f"RESULTS: {PASSED}/{total} passed")
if ERRORS == 0:
    print(f"ALL TESTS PASSED ✅")
else:
    print(f"{ERRORS} FAILURES ❌")
    sys.exit(1)
