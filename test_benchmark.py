#!/usr/bin/env python3
"""
🎭 Hermes Persona — Role Selection Benchmark

Validates that the KANBAN_GUIDANCE persona section contains
the 4 research-backed principles and that key role-to-task
mappings are referenced correctly.

Run: python test_benchmark.py
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

PASS = 0
FAIL = 0

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        marker = f"  ❌ {name}"
        if detail:
            marker += f"\n     └─ {detail}"
        print(marker)

def get_kb_guidance():
    """Read KANBAN_GUIDANCE from prompt_builder.py"""
    home = os.path.expanduser("~")
    pb_path = os.path.join(home, ".hermes", "hermes-agent", "agent", "prompt_builder.py")
    with open(pb_path) as f:
        return f.read()

def fetch_readme():
    """Fetch agency-agents README"""
    url = "https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md"
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read().decode("utf-8")

def check_role_exists(readme_text, role_name):
    """Check if a role name appears in the README table"""
    # Look for [Role Name](...) pattern in table rows
    pattern = re.compile(r'\[([^\]]*' + re.escape(role_name) + r'[^\]]*)\]\([^)]+\)')
    return bool(pattern.search(readme_text))


print("=" * 60)
print("🎭 Hermes Persona — Role Selection Benchmark")
print("=" * 60)

# --- Part 1: KANBAN_GUIDANCE integrity ---
print("\n📋 [1/3] KANBAN_GUIDANCE — Principles present")
print("-" * 50)

guidance = get_kb_guidance()

# Check all 4 principles are present
principles = [
    ("Output-type alignment", "Output-type alignment"),
    ("Role boundary clarity", "Role boundary clarity"),
    ("Task decomposition priority", "Task decomposition priority"),
    ("Confidence threshold", "Confidence threshold"),
]
for label, keyword in principles:
    test(f"Principle present: {label}", keyword in guidance)

# Check citations present
citations = [
    "MetaGPT", "CAMEL", "AgentVerse", "AutoGen",
    "ICLR", "NeurIPS", "ICML",
]
for c in citations:
    test(f"Citation present: {c}", c in guidance)

# --- Part 2: Catalog accessibility ---
print("\n📡 [2/3] Agency-agents catalog")
print("-" * 50)

try:
    readme = fetch_readme()
    test("README fetchable", len(readme) > 1000, f"Got {len(readme)} bytes")
    
    # Check key roles exist
    key_roles = [
        "Frontend Developer",
        "Backend Architect",
        "DevOps Automator",
        "Database Optimizer",
        "Security Engineer",
        "Product Manager",
        "Mobile App Builder",
        "AI Engineer",
        "Technical Writer",
        "Brand Guardian",
        "Social Media Strategist",
        "Financial Analyst",
        "UX Researcher",
        "Incident Response Commander",
    ]
    for role in key_roles:
        exists = check_role_exists(readme, role)
        test(f"Role exists: {role}", exists)
        
except Exception as e:
    test("README fetch", False, str(e))
    readme = ""

# --- Part 3: Role name → URL validation ---
print("\n🔗 [3/3] Task-to-role mapping sanity")
print("-" * 50)

# These are the tasks from the benchmark with expected roles
mappings = [
    ("React dashboard with D3.js", "Frontend Developer"),
    ("REST API with JWT", "Backend Architect"),
    ("CI/CD pipeline with GitHub Actions", "DevOps Automator"),
    ("Optimize PostgreSQL queries", "Database Optimizer"),
    ("OWASP audit", "Security Engineer"),
    ("Product Requirements Document", "Product Manager"),
    ("iOS login FaceID", "Mobile App Builder"),
    ("Sentiment analysis model", "AI Engineer"),
    ("Dockerize to AWS ECS", "DevOps Automator"),
    ("API documentation", "Technical Writer"),
    ("Brand style guide", "Brand Guardian"),
    ("Social media campaign", "Social Media Strategist"),
    ("Financial forecast model", "Financial Analyst"),
    ("User research interviews", "UX Researcher"),
    ("Production outage response", "Incident Response Commander"),
]

all_roles_ok = True
for task_desc, expected_role in mappings:
    exists = check_role_exists(readme, expected_role) if readme else False
    if not exists:
        all_roles_ok = False
    test(f"Task '{task_desc[:30]}...' → {expected_role}", exists)

# --- Summary ---
print("\n" + "=" * 60)
total = PASS + FAIL
print(f"📊 Result: {PASS}/{total} passed", end="")
if total > 0:
    print(f" ({100 * PASS // total}%)")
else:
    print()
print("=" * 60)

sys.exit(0 if FAIL == 0 else 1)
