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
import sys
import urllib.request

PASS = 0
FAIL = 0

# Configurable base path — overridable via env for profile context compatibility
PERSONA_BASE = os.environ.get("HERMES_PERSONA_BASE") or os.path.expanduser("~")

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
    """Read research principles from persona SKILL.md (source of truth since opt-in transition)"""
    skill_path = os.path.join(PERSONA_BASE, ".hermes", "skills", "persona", "SKILL.md")
    with open(skill_path) as f:
        return f.read()

def fetch_readme():
    """Fetch agency-agents README (pinned to same commit as install.sh)"""
    url = "https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72bfd7f3135700ac273c619d92821b419a/README.md"
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

# --- Part 1: Persona SKILL.md integrity ---
print("\n📋 [1/3] Persona SKILL.md — Research principles present")
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

# --- Part 4: Kanban toolset in config ---
print("📋 [4/6] Hermes config — kanban in toolsets")
print("-" * 50)

def check_kanban_in_config():
    config_path = os.path.join(PERSONA_BASE, ".hermes", "config.yaml")
    if not os.path.exists(config_path):
        return False, f"Config file not found at {config_path}"
    with open(config_path) as f:
        content = f.read()
    return "kanban" in content, f"kanban {'found' if 'kanban' in content else 'not found'} in toolsets"

kanban_ok, kanban_detail = check_kanban_in_config()
test("Kanban toolset in config.yaml", kanban_ok, kanban_detail)

# --- Part 5: Persona skill file ---
print("📋 [5/6] Persona skill — SKILL.md with research principles")
print("-" * 50)

def check_persona_skill():
    skill_path = os.path.join(PERSONA_BASE, ".hermes", "skills", "persona", "SKILL.md")
    if not os.path.exists(skill_path):
        return False, f"SKILL.md not found at {skill_path}"
    with open(skill_path) as f:
        content = f.read().lower()
    principles_keywords = ["research", "principle", "guideline", "framework"]
    found = [kw for kw in principles_keywords if kw in content]
    if len(found) >= 2:
        return True, f"Research principles found (keywords: {', '.join(found)})"
    else:
        return False, f"Insufficient research principle keywords found: {found}"

skill_ok, skill_detail = check_persona_skill()
test("Persona SKILL.md exists and has research principles", skill_ok, skill_detail)

# --- Part 6: Repository essential files ---
print("\U0001f4cb [6/7] Repository — essential files present")
print("-" * 50)

repo_path = os.path.dirname(os.path.abspath(__file__))
required_files = ["LICENSE", "install.sh", "README.md", ".gitignore"]
for fname in required_files:
    fpath = os.path.join(repo_path, fname)
    exists = os.path.exists(fpath)
    test(f"Repo file: {fname}", exists, f"Path: {fpath}" if not exists else "")

# --- Final summary ---
# --- Part 7: Script syntax validation ---
print("\U0001f4cb [7/7] Script syntax validation")
print("-" * 50)

repo_path = os.path.dirname(os.path.abspath(__file__))

# Python scripts
py_scripts = [
    "archive/scripts/generate-role-manifest.py",
    "archive/scripts/generate-sbom.py",
    "archive/scripts/scan-role-content.py",
]
import subprocess
for script in py_scripts:
    path = os.path.join(repo_path, script)
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", path],
        capture_output=True, text=True
    )
    test(f"Python syntax: {script}", result.returncode == 0, result.stderr)

# Bash scripts
bash_scripts = ["install.sh"]
for script in bash_scripts:
    path = os.path.join(repo_path, script)
    result = subprocess.run(
        ["bash", "-n", path],
        capture_output=True, text=True
    )
    test(f"Shell syntax: {script}", result.returncode == 0, result.stderr)

# Verify install.sh references opt-in design
install_path = os.path.join(repo_path, "install.sh")
with open(install_path) as f:
    install_content = f.read()
mentions_optin = "--skill persona" in install_content or "opt-in" in install_content.lower()
test("install.sh references opt-in design", mentions_optin)

print()
print("=" * 60)
total = PASS + FAIL
print(f"📊 Result: {PASS}/{total} passed", end="")
if total > 0:
    print(f" ({100 * PASS // total}%)")
else:
    print()
print("=" * 60)

sys.exit(0 if FAIL == 0 else 1)
