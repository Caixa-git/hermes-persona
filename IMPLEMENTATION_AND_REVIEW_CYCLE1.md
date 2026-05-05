# Implementation + Review Plan — Cycle 1

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🔧 Full-Stack Developer, S=1)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `TASK_BREAKDOWN_CYCLE1.md`

---

## 구현 순서

1. C1-T4 (install.sh test, 독립)
2. C1-T1 (CHANGELOG, T2의 전제)
3. C1-T2 (GitHub Release)
4. C1-T3 (git tag)

---

## C1-T4: test_benchmark.py Part 5

test_benchmark.py에 install.sh 정적 검증 섹션 추가. **실제 셸 실행(subprocess) 없음** — 환경 보호 + 테스트 속도 유지.

```python
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
    test("install.sh has ACTION=install", "ACTION=\"install\"" in ish)
    test("install.sh has ACTION=uninstall", "ACTION=\"uninstall\"" in ish)
else:
    test("install.sh exists", False, f"Not found: {ish_path}")
```

변경 diff: +25 lines (18→23 tests)

## C1-T1: CHANGELOG → v1.0.1

`## [Unreleased]` → `## [1.0.1] - 2026-05-06`
링크 업데이트: `[Unreleased]` 비교 대상 변경

## C1-T2: GitHub Release 생성

```bash
export CHANGELOG_BODY="$(cat CHANGELOG.md | sed -n '/## \[1\.0\.1\]/,/## \[1\.0\.0\]/p' | head -n -2)"
gh api repos/Caixa-git/hermes-persona/releases \
  --method POST \
  --field tag_name="v1.0.1" \
  --field target_commitish="main" \
  --field name="v1.0.1" \
  --field body="$CHANGELOG_BODY"
```

## C1-T3: git tag

```bash
git tag v1.0.1
# push via API (환경 HTTPS 타임아웃 우회)
```

---

## 리뷰 기준

| 항목 | 기준 |
|------|------|
| test_benchmark.py | 기존 18개 테스트 수정 금지, Part 5만 추가 |
| CHANGELOG.md | 날짜 형식 ISO 8601, Keep a Changelog 형식 유지 |
| GitHub Release | tag_name=v1.0.1, target=main, body=CHANGELOG 내용 |
| install.sh | **수정 금지** — 검증만 추가 |

## 롤백 방법

- CHANGELOG: `git checkout -- CHANGELOG.md`
- test_benchmark.py: `git checkout -- test_benchmark.py`
- GitHub Release: `gh api repos/Caixa-git/hermes-persona/releases/<id> --method DELETE`
- git tag: `git tag -d v1.0.1 && git push origin :refs/tags/v1.0.1`

---

## 다음 Step 입력값

- C1-T4 구현 → Part 5 코드 완성
- C1-T1→T2→T3 구현 완료
- 전체 테스트 23/23 검증
