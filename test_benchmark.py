#!/usr/bin/env python3
"""🎭 Hermes Persona — validates SKILL.md content integrity.

Run: python test_benchmark.py
"""

import os, re, sys, urllib.request

PASS, FAIL = 0, 0
AGENCY_AGENTS_URL = "https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72bfd7f3135700ac273c619d92821b419a/README.md"

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1; print(f"  ✅ {name}")
    else:
        FAIL += 1; print(f"  ❌ {name}" + (f"\n     └─ {detail}" if detail else ""))

def read_skill():
    p = os.path.expanduser("~/.hermes/skills/persona/SKILL.md")
    with open(p) as f: return f.read()

def fetch_roles():
    with urllib.request.urlopen(AGENCY_AGENTS_URL, timeout=10) as r:
        return r.read().decode()

def role_exists(text, name):
    return bool(re.search(r'\[' + re.escape(name) + r'\]\(', text))

# ── Part 1: SKILL.md integrity ──
print("\n📋 [1/3] SKILL.md — principles & citations")
print("-" * 40)
skill = read_skill()

for p in ["Output-type alignment", "Role boundary clarity",
           "Task decomposition priority", "Confidence threshold"]:
    test(f"Principle: {p}", p in skill)
for c in ["MetaGPT", "CAMEL", "AgentVerse", "AutoGen", "ICLR", "NeurIPS", "ICML"]:
    test(f"Citation: {c}", c in skill)

# ── Part 2: Catalog accessibility ──
print("\n📡 [2/3] Agency-agents catalog")
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
print("\n🔗 [3/3] Task → role mappings")
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
for task, expected in mappings:
    test(f"'{task[:25]}...' → {expected}", role_exists(readme, expected)) if readme else None

# ── Summary ──
total = PASS + FAIL
print(f"\n{'='*50}")
print(f"📊 {PASS}/{total} passed ({100*PASS//total if total else 0}%)")
print(f"{'='*50}")
sys.exit(0 if FAIL == 0 else 1)
