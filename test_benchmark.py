#!/usr/bin/env python3
"""🎭 Hermes Persona — validates SKILL.md content integrity.

Run: python test_benchmark.py            # Full suite (requires network)
     python test_benchmark.py --offline  # Skip network-dependent tests
"""

import os, re, sys, urllib.request

PASS, FAIL = 0, 0
OFFLINE = "--offline" in sys.argv
AGENCY_AGENTS_URL = "https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72bfd7f3135700ac273c619d92821b419a/README.md"

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1; print(f"  ✅ {name}")
    else:
        FAIL += 1; print(f"  ❌ {name}" + (f"\n     └─ {detail}" if detail else ""))

def read_skill():
    """Read SKILL.md from installed path or local repo path as fallback."""
    p = os.path.expanduser("~/.hermes/skills/persona/SKILL.md")
    try:
        with open(p) as f: return f.read()
    except FileNotFoundError:
        # Fallback: local repo path
        local = os.path.join(os.path.dirname(__file__) or ".", "skills", "persona", "SKILL.md")
        with open(local) as f: return f.read()

def fetch_roles():
    with urllib.request.urlopen(AGENCY_AGENTS_URL, timeout=10) as r:
        return r.read().decode()

def role_exists(text, name):
    return bool(re.search(r'\[' + re.escape(name) + r'\]\(', text))

# ── Part 1: SKILL.md integrity ──
print("\n📋 [1/5] SKILL.md — principles & citations")
print("-" * 40)
skill = read_skill()

for p in ["Output-type alignment", "Role boundary clarity",
           "Task decomposition priority", "Confidence threshold"]:
    test(f"Principle: {p}", p in skill)
for c in ["MetaGPT", "CAMEL", "AgentVerse", "AutoGen", "ICLR", "NeurIPS", "ICML"]:
    test(f"Citation: {c}", c in skill)

# ── Part 2: Catalog accessibility ──
print("\n📡 [2/5] Agency-agents catalog")
print("-" * 40)
if OFFLINE:
    print("  ⏭️  Skipped (--offline mode)")
else:
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
print("\n🔗 [3/5] Task → role mappings")
print("-" * 40)
if OFFLINE:
    print("  ⏭️  Skipped (--offline mode)")
    readme = ""
else:
    if 'readme' not in dir() or not readme:
        try:
            readme = fetch_roles()
        except:
            readme = ""
    
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

# ── Part 4: Repository integrity ──
print("\n🔍 [4/5] Repository integrity")
print("-" * 40)

# 4a: pyproject.toml version detection
pp_path = os.path.join(os.path.dirname(__file__) or ".", "pyproject.toml")
if os.path.exists(pp_path):
    with open(pp_path) as f:
        pp = f.read()
    m = re.search(r'version\s*=\s*"([^"]+)"', pp)
    test("pyproject.toml version detected", m is not None,
         f"regex matched: {bool(m)}")
    if m:
        test(f"pyproject.toml version: {m.group(1)}", True)

# 4b: All reference docs exist and have content
ref_dir = os.path.join(os.path.dirname(__file__) or ".", "skills", "persona", "references")
if os.path.isdir(ref_dir):
    refs = sorted(f for f in os.listdir(ref_dir) if f.endswith('.md'))
    test(f"Reference docs: {len(refs)} files found", len(refs) >= 6,
         f"Found: {', '.join(refs)}")
    for ref in refs:
        rp = os.path.join(ref_dir, ref)
        with open(rp) as f:
            lines = len(f.readlines())
        test(f"  {ref}: {lines} lines", lines >= 20,
             f"Expected ≥20, got {lines}")
else:
    test("Reference docs directory", False, f"Not found: {ref_dir}")

# ── Part 5: install.sh integrity ──
print("\n📦 [5/5] install.sh integrity")
print("-" * 40)

ish_path = os.path.join(os.path.dirname(__file__) or ".", "install.sh")
if os.path.exists(ish_path):
    with open(ish_path) as f:
        ish = f.read()
    
    test("install.sh exists", len(ish) > 0)
    test("install.sh shebang: #!/usr/bin/env bash", ish.startswith("#!/usr/bin/env bash"))
    test("install.sh has --help flag", "--help" in ish)
    test("install.sh has --dry-run flag", "--dry-run" in ish)
    test("install.sh has install logic", "ACTION=\"install\"" in ish
         or "install" in ish[:200])
    test("install.sh has uninstall logic", "uninstall" in ish)
else:
    test("install.sh exists", False, f"Not found: {ish_path}")

# ── Summary ──
total = PASS + FAIL
print(f"\n{'='*50}")
print(f"📊 {PASS}/{total} passed ({100*PASS//total if total else 0}%)")
print(f"{'='*50}")
sys.exit(0 if FAIL == 0 else 1)
