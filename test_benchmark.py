#!/usr/bin/env python3
"""🎭 Hermes Persona — validates SKILL.md content integrity.

Tests both the source repo SKILL.md and the live installed copy.
Run:
  python test_benchmark.py                    # test live install
  python test_benchmark.py --repo             # test source repo
  python test_benchmark.py --all              # test both
"""

import os, re, sys, urllib.request

PASS, FAIL = 0, 0

AGENCY_AGENTS_URL = "https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72bfd7f3135700ac273c619d92821b419a/README.md"

# Resolve source repo root (works whether called from repo root or anywhere)
_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
_REPO_SKILL = os.path.join(_REPO_ROOT, "skills", "persona", "SKILL.md")
_LIVE_SKILL = os.path.expanduser("~/.hermes/skills/persona/SKILL.md")


def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1; print(f"  ✅ {name}")
    else:
        FAIL += 1; print(f"  ❌ {name}" + (f"\n     └─ {detail}" if detail else ""))


def read_skill(source="live"):
    """Read SKILL.md from source repo or live install."""
    paths = {"repo": _REPO_SKILL, "live": _LIVE_SKILL}
    p = paths.get(source, _LIVE_SKILL)
    if not os.path.isfile(p):
        raise FileNotFoundError(f"SKILL.md not found at {p} (source={source})")
    with open(p) as f:
        return f.read()


def fetch_roles():
    with urllib.request.urlopen(AGENCY_AGENTS_URL, timeout=10) as r:
        return r.read().decode()


def role_exists(text, name):
    return bool(re.search(r'\[' + re.escape(name) + r'\]\(', text))


def run_tests(source, label):
    """Run all integrity tests on a given SKILL.md source."""
    global PASS, FAIL

    try:
        skill = read_skill(source)
    except FileNotFoundError as e:
        print(f"\n⚠️  {label}: {e}")
        return

    # ── Part 1: SKILL.md integrity ──
    print(f"\n📋 [{label}] SKILL.md — principles & citations")
    print("-" * 40)
    for p in ["Output-type alignment", "Role boundary clarity",
               "Task decomposition priority", "Confidence threshold"]:
        test(f"Principle: {p}", p in skill)
    for c in ["MetaGPT", "CAMEL", "AgentVerse", "AutoGen", "ICLR", "NeurIPS", "ICML"]:
        test(f"Citation: {c}", c in skill)

    # key structural elements
    test("YAML frontmatter", skill.startswith("---"), detail="SKILL.md must begin with '---'")
    test("10-step protocol", "**1. Analyze your task.**" in skill)
    test("CDPD evaluation", "single or multi-persona" in skill)
    test("Priority rule", "YOUR NATURE PREVAILS" in skill)
    test("Injection awareness (step 0)", "prompt injection" in skill)

    # ── Part 2: Catalog accessibility ──
    print(f"\n📡 [{label}] Agency-agents catalog")
    print("-" * 40)
    try:
        readme = fetch_roles()
        test("Catalog fetchable", len(readme) > 1000)
        for role in ["Frontend Developer", "Backend Architect", "DevOps Automator",
            "Database Optimizer", "Security Engineer", "Product Manager",
            "Mobile App Builder", "AI Engineer", "Technical Writer",
            "Brand Guardian", "Social Media Strategist", "Financial Analyst"]:
            test(f"Role: {role}", role_exists(readme, role))
    except Exception as e:
        test("Catalog fetch", False, str(e))
        readme = ""

    # ── Part 3: Task-to-role mapping ──
    print(f"\n🔗 [{label}] Task → role mappings")
    print("-" * 40)
    mappings = [
        ("React dashboard with D3.js", "Frontend Developer"),
        ("REST API with JWT", "Backend Architect"),
        ("CI/CD pipeline with GitHub Actions", "DevOps Automator"),
        ("Optimize PostgreSQL queries", "Database Optimizer"),
        ("OWASP audit", "Security Engineer"),
        ("Product Requirements Document", "Product Manager"),
        ("iOS login FaceID", "Mobile App Builder"),
        ("Sentiment analysis model", "AI Engineer"),
        ("API documentation", "Technical Writer"),
        ("Brand style guide", "Brand Guardian"),
        ("Social media campaign", "Social Media Strategist"),
        ("Financial forecast model", "Financial Analyst"),
        ("Production outage response", "Incident Response Commander"),
    ]
    if readme:
        for task, expected in mappings:
            test(f"'{task[:25]}...' → {expected}", role_exists(readme, expected))


# ── Main: parse args and run ──
if __name__ == "__main__":
    args = set(sys.argv[1:])
    run_live = "--all" in args or "live" not in args  # default: live only
    run_repo = "--repo" in args or "--all" in args

    sources = []
    if run_live:
        sources.append(("live", "Live install (~/.hermes/skills/persona/)"))
    if run_repo:
        sources.append(("repo", "Source repo (skills/persona/SKILL.md)"))

    for src, label in sources:
        run_tests(src, label)

    total = PASS + FAIL
    print(f"\n{'='*50}")
    print(f"📊 {PASS}/{total} passed ({100*PASS//total if total else 0}%)")
    sys.exit(0 if FAIL == 0 else 1)
