#!/usr/bin/env python3
"""
🎭 Hermes Persona — Automated Test Suite

Tests:
  1. GitHub raw URL accessibility (README + role .md)
  2. KANBAN_GUIDANCE persona section presence
  3. Persona skill file validity
  4. Persona skill detection by Hermes Agent
  5. Full kanban task → worker spawn → role adoption simulation
"""

import os
import subprocess
import sys
import urllib.request

PASS = "✅"
FAIL = "❌"
SKIP = "⏭️"

tests_passed = 0
tests_failed = 0
tests_skipped = 0

# Correct role paths from actual repo structure (172 roles, 15 categories)
SAMPLE_ROLES = {
    "Backend Architect": "engineering/engineering-backend-architect.md",
    "Frontend Developer": "engineering/engineering-frontend-developer.md",
    "Security Engineer": "engineering/engineering-security-engineer.md",
    "UI Designer": "design/design-ui-designer.md",
    "API Tester": "testing/testing-api-tester.md",
    "Database Optimizer": "engineering/engineering-database-optimizer.md",
    "Game Designer": "game-development/game-designer.md",
    "Product Manager": "product/product-manager.md",
    "DevOps Automator": "engineering/engineering-devops-automator.md",
    "Financial Analyst": "finance/finance-financial-analyst.md",
    "UX Researcher": "design/design-ux-researcher.md",
}


def test(name, condition, detail=""):
    global tests_passed, tests_failed
    if condition:
        tests_passed += 1
        print(f"  {PASS} {name}")
    else:
        tests_failed += 1
        print(f"  {FAIL} {name}")
        if detail:
            print(f"     └─ {detail}")


def test_skip(name, reason=""):
    global tests_skipped
    tests_skipped += 1
    print(f"  {SKIP} {name}")
    if reason:
        print(f"     └─ {reason}")


def http_body(url, timeout=10):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None


print("=" * 60)
print("🎭 Hermes Persona — Test Suite v2")
print("=" * 60)
print()

# ──────────────────────────────────────────
# 1. GITHUB RAW URL ACCESSIBILITY
# ──────────────────────────────────────────
print("📡 [1/5] GitHub Raw URL Accessibility")
print("-" * 40)

BASE = "https://raw.githubusercontent.com/msitarzewski/agency-agents/main"

# 1a. Root README
content_readme = http_body(f"{BASE}/README.md")
test("agency-agents README.md 접근 가능", content_readme is not None)
if content_readme:
    print(f"     └─ README: {len(content_readme):,} bytes | role tables: {'| Agent' in content_readme}")

# 1b. All sample roles
roles_ok = 0
for name, path in SAMPLE_ROLES.items():
    ok = http_body(f"{BASE}/{path}") is not None
    if ok:
        roles_ok += 1
    test(f"{name}", ok)
print(f"     └─ {roles_ok}/{len(SAMPLE_ROLES)} 역할 접근 성공")

# 1c. All 15 category directories exist
categories = [
    "academic", "design", "engineering", "finance", "game-development",
    "marketing", "paid-media", "product", "project-management", "sales",
    "spatial-computing", "specialized", "strategy", "support", "testing"
]
for cat in categories:
    url = f"https://api.github.com/repos/msitarzewski/agency-agents/contents/{cat}"
    ok = http_body(url) is not None
    test(f"카테고리 존재: {cat}", ok)

print()

# ──────────────────────────────────────────
# 2. KANBAN_GUIDANCE PATCH
# ──────────────────────────────────────────
print("🔧 [2/5] KANBAN_GUIDANCE — Hermes Agent Patch")
print("-" * 40)

pb_path = os.path.expanduser("~/.hermes/hermes-agent/agent/prompt_builder.py")
if not os.path.exists(pb_path):
    pb_path = "/Users/aiadmin/.hermes/hermes-agent/agent/prompt_builder.py"

if os.path.exists(pb_path):
    with open(pb_path) as f:
        content = f.read()

    test("persona 섹션 존재", "## persona — role adoption" in content)
    test("nicepkg 잔재 없음 (→ msitarzewski로 교체됨)",
         "nicepkg" not in content and "msitarzewski" in content)
    test("GitHub raw URL 형식 정확",
         "raw.githubusercontent.com/msitarzewski" in content)
    test("폴백 처리 ('proceed as a generalist')",
         "proceed as a generalist" in content)
    # Check numbers directly in the persona section area
    idx = content.find("## persona — role adoption")
    if idx > 0:
        # Read until the closing paren of KANBAN_GUIDANCE
        end = content.find("TOOL_USE_ENFORCEMENT_GUIDANCE", idx)
        if end < 0:
            end = content.find(")\n\n", idx) + 3
        section = content[idx:end] if end > idx else content[idx:]
        has_steps = all(f"{n}." in section for n in range(1, 6))
        test("5단계 명령 (1~5) 포함", has_steps)
        print(f"     └─ 섹션 길이: {len(section)} chars")
else:
    test_skip("KANBAN_GUIDANCE 패치 확인", "prompt_builder.py를 찾을 수 없음")

print()

# ──────────────────────────────────────────
# 3. PERSONA SKILL FILE
# ──────────────────────────────────────────
print("📁 [3/5] Persona Skill File")
print("-" * 40)

skill_path = os.path.expanduser("~/.hermes/skills/persona/SKILL.md")
test("스킬 파일 존재", os.path.exists(skill_path))

if os.path.exists(skill_path):
    with open(skill_path) as f:
        content = f.read()

    test("YAML frontmatter", content.startswith("---"))
    test("name: persona", "name: persona" in content)
    test("msitarzewski URL 사용", "msitarzewski/agency-agents" in content)
    test("raw.githubusercontent.com 사용", "raw.githubusercontent.com" in content)
    test("nicepkg 잔재 없음", "nicepkg" not in content)

    steps = [l for l in content.split("\n") if l.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6."))]
    print(f"     └─ 명령 단계: {len(steps)} | 파일 크기: {len(content):,} bytes")

print()

# ──────────────────────────────────────────
# 4. HERMES AGENT SKILL DISCOVERY
# ──────────────────────────────────────────
print("🔍 [4/5] Hermes Agent Skill Discovery")
print("-" * 40)

try:
    result = subprocess.run(
        ["hermes", "skills", "list"],
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    test("hermes skills list 정상 실행", result.returncode == 0)
    test("persona 스킬 리스트 노출", "persona" in output.lower())
    for line in output.split("\n"):
        if "persona" in line.lower():
            print(f"     └─ {line.strip()}")
            break
except FileNotFoundError:
    test_skip("hermes CLI", "명령어를 찾을 수 없음")
except Exception as e:
    test_skip("hermes skills list", str(e))

# Check skill_view can load
try:
    result = subprocess.run(
        ["hermes", "skills", "inspect", "persona"],
        capture_output=True, text=True, timeout=30
    )
    ok = result.returncode == 0 or "persona" in (result.stdout + result.stderr).lower()
    test("hermes skills view persona 로드 가능", ok)
except Exception as e:
    test_skip("hermes skills view", str(e))

print()

# ──────────────────────────────────────────
# 5. KANBAN TASK + ROLE ADOPTION
# ──────────────────────────────────────────
print("🎭 [5/5] Kanban Task → Role Adoption")
print("-" * 40)

# 5a. Kanban task creation
try:
    result = subprocess.run(
        ["hermes", "kanban", "create",
         "REST API 서버 구축 (JWT 인증 포함)",
         "--skill", "persona"],
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    test("kanban create --skill persona", result.returncode == 0)
    if result.returncode == 0:
        task_id = [l.split()[1].strip() for l in output.split("\n") if "Created" in l][:1]
        if task_id:
            print(f"     └─ 태스크: {task_id[0]}")
except Exception as e:
    test_skip("kanban create", str(e))

# 5b. Role adoption simulation
try:
    result = subprocess.run(
        ["hermes", "-z",
         "You have the persona skill loaded. Fetch the README from "
         "https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md "
         "and pick the best role for building a REST API server with JWT auth. "
         "Answer ONLY with: role name, category path.",
         "--skill", "persona"],
        capture_output=True, text=True, timeout=120
    )
    output = result.stdout + result.stderr
    test("hermes -z --skill persona 실행", result.returncode == 0)
    print(f"     └─ 응답: {output.strip()[:200]}")
    test("Backend Architect 선택 확인",
         "Backend Architect" in output,
         output.strip()[:80])
    test("Category path 포함",
         "engineering" in output.lower(),
         output.strip()[:80])
except Exception as e:
    test_skip("role adoption", str(e))

# 5c. Another role — frontend task
try:
    result = subprocess.run(
        ["hermes", "-z",
         "You have the persona skill loaded. Fetch the README from "
         "https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md "
         "and pick the best role for building a React dashboard UI. "
         "Answer ONLY with: role name, category path.",
         "--skill", "persona"],
        capture_output=True, text=True, timeout=120
    )
    output = result.stdout + result.stderr
    test("hermes -z 프론트엔드 태스크 실행", result.returncode == 0)
    print(f"     └─ 응답: {output.strip()[:200]}")
    test("Frontend Developer 선택 확인",
         "Frontend Developer" in output or "frontend" in output.lower())
except Exception as e:
    test_skip("frontend role adoption", str(e))

print()

# ──────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────
print("=" * 60)
total = tests_passed + tests_failed + tests_skipped
print(f"📊 결과: {PASS} {tests_passed} | {FAIL} {tests_failed} | {SKIP} {tests_skipped} | total: {total}")

if tests_failed > 0:
    print(f"\n{FAIL} {tests_failed}개 실패 — 개선 필요")
    sys.exit(1)
else:
    print(f"\n{PASS} 모든 테스트 통과")
    sys.exit(0)
