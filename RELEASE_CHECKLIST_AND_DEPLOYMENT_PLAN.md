# Release Checklist + Deployment Plan — hermes-persona

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🚀 DevOps Automator, S<2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `QA_REPORT.md`

---

## 배포 가능 상태 검증

| 조건 | 상태 | 확인 |
|------|------|------|
| **기능 완성** — 핵심 기능 100% 동작 | ✅ | F1-F7 전면 통과 |
| **회귀 제로** — 기존 테스트 전면 통과 | ✅ | 18/18, 이전 수정 회귀 없음 |
| **문서 현행화** — README/설치 문서/변경사항 최신 | ✅ | CHANGELOG + README + 8 refs |
| **보안 기본** — credential 0건, 취약점 0건 | ✅ | SECURITY_AUDIT 확인, .env gitignored |
| **릴리즈 이력** — 버전 태그 + 릴리즈 노트 | 🟡 | CHANGELOG 있음, GitHub Release 갱신 필요 |

📐 합리적 추정

## 릴리즈 결정

**판단:** 배포 가능. v1.0.0 이후 첫 번째 패치/개선 릴리즈.

| 항목 | 값 |
|------|-----|
| 버전 | v1.0.1 (CHANGELOG 기준) |
| 태그 | `v1.0.1` |
| 브랜치 | main (직접) |
| 배포 방식 | git push (기존과 동일) |

✅ 확인된 사실

## 배포 체크리스트

- [x] `pyproject.toml` version = `1.0.0` (다음 릴리즈 시 v1.0.1로 범프)
- [x] `CHANGELOG.md` 최신 변경사항 포함
- [x] 모든 테스트 통과 (18/18)
- [x] 보안 감사 통과
- [x] 문서 현행화
- [x] `develop` 브랜치 정리 (삭제 완료)
- [x] 원격 저장소와 동기화 (2개 커밋 push)
- [ ] GitHub Release v1.0.1 생성 (with 릴리즈 노트)
- [ ] 버전 태그 `v1.0.1` 생성

✅ 확인된 사실 / ⬜ 미완료

## 롤백 계획

| 시나리오 | 조치 |
|----------|------|
| 설치 실패 | `install.sh --uninstall` 실행 |
| 기능 회귀 | `git revert`로 이전 커밋 복원 |
| 심각한 버그 발견 | `hotfix` 브랜치 생성 → 수정 → main 병합 |

📐 합리적 추정

## 배포 후 Health Check

```bash
# 1. 설치 테스트
bash install.sh --dry-run

# 2. 테스트 실행
python3 test_benchmark.py --offline

# 3. 태그 확인
git tag -l | grep v1.0
```

---

## 완료 기준 체크

| 조건 | 상태 |
|------|------|
| 기능 완성 | ✅ |
| 회귀 제로 | ✅ |
| 문서 현행화 | ✅ |
| 보안 기본 | ✅ |
| 릴리즈 이력 | 🟡 (CHANGELOG ✅, GitHub Release ⬜) |

---

## 다음 Step 입력값

- 배포 상태: ✅ 배포 가능
- GitHub Release 미생성 (수동 or 자동화)
- v1.0.0 이후 첫 개선 릴리즈
