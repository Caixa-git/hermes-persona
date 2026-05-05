# Release Note Draft — Cycle 1

**작성:** 2026-05-06

---

## 릴리즈 범위

Cycle 1 개선: GitHub Release 생성 + install.sh 검증 테스트

## 변경 파일

| 파일 | 변경 유형 | 내용 |
|------|-----------|------|
| CHANGELOG.md | 수정 | Unreleased → v1.0.1 (2026-05-06) |
| test_benchmark.py | 수정 | Part 5 추가 (6 tests), 18→28 tests |
| ROADMAP_ITEM_SELECTION.md | 생성 | Now/Next/Later 분류 |
| REQUIREMENTS_AND_SPEC_UPDATE.md | 생성 | P1/P2 상세 spec |
| TASK_BREAKDOWN_CYCLE1.md | 생성 | 4개 task 상세 |
| IMPLEMENTATION_AND_REVIEW_CYCLE1.md | 생성 | 실행 계획 |

## 검증 완료

- [x] test_benchmark.py --offline: 28/28 통과
- [x] install.sh 정적 검증 (Part 5)
- [x] GitHub Release v1.0.1 생성 완료
- [x] git tag v1.0.1 원격 존재
- [x] CHANGELOG v1.0.1 날짜 확정

## Known Issues

- git push HTTPS 타임아웃 (환경) → API 기반 push 우회 중
- install.sh 실제 실행 검증 미포함 (정적 분석만)

## 롤백 방법

```bash
# CHANGELOG 복원
git checkout HEAD~1 -- CHANGELOG.md test_benchmark.py

# GitHub Release 삭제
gh api repos/Caixa-git/hermes-persona/releases/<id> --method DELETE

# tag 삭제
git tag -d v1.0.1 && git push origin :refs/tags/v1.0.1
```

## 권장 태그

v1.0.1 ✅ (생성 완료)
