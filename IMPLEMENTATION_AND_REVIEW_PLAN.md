# Implementation + Review Plan — hermes-persona

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🔧 Full-Stack Developer, S=1)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `TASK_BREAKDOWN.md`

---

## 실행 계획

T1→T2→T4→T3→T5→T7→T6 순서로 실행 (의존성 기반).

### T1: git push (API 경유)

**수행:** GitHub Git Data API
```python
# blob 생성 → tree 생성 → commit 생성 → ref 업데이트
blobs = [create_blob(f) for f in changed_files]
tree = create_tree(base_tree, blobs)
commit = create_commit(tree, parents=[current_head])
update_ref('heads/main', commit)
```

**결과:** 원격 HEAD = `5a71f5e` ✅

### T2: develop 브랜치 삭제

**수행:** GitHub API
```bash
# 옵션 A 실행 (삭제)
curl -X DELETE -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/Caixa-git/hermes-persona/git/refs/heads/develop
```

### T4: CHANGELOG.md

**수행:** Keep a Changelog 형식으로 작성

### T3: install.sh 단위 테스트 (test_benchmark.py Part 5)

**수행:** test_benchmark.py에 `--test-install` 모드 추가
- install.sh --dry-run 실행
- install.sh --help 출력 검증
- install.sh 존재 확인

### T5: SKILL.md Future Work 정리

**수행:** TODO 4개 항목 상태 업데이트

### T7: develop stale 알림 (불필요 — T2에서 삭제)

**결정:** T2에서 develop 브랜치 삭제 완료. T7 불필요.

### T6: PyPI 패키징 검토 (보류)

**결정:** 현재 Hermes Agent 스킬 구조와 PyPI 패키징이 충돌 가능.
- install.sh가 `~/.hermes/skills/`에 직접 쓰는 구조
- PyPI 패키지는 pip install 경로 사용
- **보류, 별도 이슈로 등록**

---

## 변경 내역

| ID | 파일 | 변경 유형 | 상태 |
|----|------|-----------|------|
| T1 | (원격 ref) | git push | ✅ |
| T2 | (원격 ref) | 브랜치 삭제 | ✅ |
| T4 | CHANGELOG.md | 생성 | ✅ |
| T3 | test_benchmark.py | 수정 | ✅ |
| T5 | skills/persona/SKILL.md | 수정 | ✅ |
| T7 | — | 불필요 | ➖ |
| T6 | — | 보류 | ⏳ |

---

## 코드 리뷰 기준

1. **가독성:** 추가된 코드가 기존 스타일과 일치하는가
2. **테스트:** 새 기능이 테스트 가능한가, 기존 테스트를 깨뜨리지 않는가
3. **보안:** 하드코딩된 값, credential 노출이 없는가
4. **호환성:** install.sh의 하위호환성이 유지되는가

---

## 피드백 루프

| 회차 | 발견 | 수정 | 검증 | 기록 |
|------|------|------|------|------|
| 1 | T6 PyPI 충돌 | 보류 판정, 이슈 등록 | N/A | TASK_BREAKDOWN.md 업데이트 |
| 2 | T7 중복 (T2로 대체) | T7 제거 | N/A | TASK_BREAKDOWN.md 업데이트 |

✅ 2회 루프, 모두 해결. 추가 루프 불필요.

## Git 이력

- 브랜치: `main` (직접 작업, feature 브랜치 불필요한 소규모 변경)
- 커밋: `git add -A && git commit -m "..."` (변경 그룹별 1커밋)

---

## 다음 Step 입력값

- 원격 동기화 완료 (`5a71f5e`)
- develop 브랜치 삭제됨
- CHANGELOG.md 생성
- test_benchmark.py install.sh 검증 추가
- SKILL.md TODO 2건 업데이트 (SHA ⏳→✅)
- T6 (PyPI) 보류, 별도 이슈
- T7 취소 (T2로 대체)
