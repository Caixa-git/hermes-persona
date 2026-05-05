# Task Breakdown — hermes-persona

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🏗️ Project Manager, S<2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `DISCOVERY_BRIEF.md`, `REQUIREMENTS_AND_SPEC.md`

---

## 작업 목록

| ID | 작업 | 우선순위 | 예상 시간 | 의존성 | 리스크 |
|----|------|----------|-----------|--------|--------|
| T1 | git push (API 경유) — 로컬 커밋 원격 반영 | P1 | 5m | 없음 | 낮음 (API 경로 검증됨) |
| T2 | develop 브랜치 삭제 또는 freeze 문서화 | P2 | 2m | 없음 | 낮음 |
| T3 | test_benchmark.py install.sh 검증 추가 (Part 5) | P2 | 20m | 없음 | 중간 (셸 실행 환경) |
| T4 | CHANGELOG.md 생성 (v1.0.0 ~ 현재) | P2 | 10m | T1 | 낮음 |
| T5 | SKILL.md Future Work 섹션 정리 (TODO 4개) | P3 | 5m | 없음 | 낮음 |
| T6 | PyPI 패키징 검토 (pyproject.toml 보강) | P3 | 15m | 없음 | 중간 (Hermes Agent 스킬 구조와 충돌 가능) |
| T7 | github-action: develop stale 알림 워크플로우 | P3 | 10m | T2 | 낮음 |

✅ 확인된 사실 / 📐 합리적 추정

## 의존성 그래프

```
T1 ──→ T4 (CHANGELOG는 push 후 버전 일치 확인)
T2 ──→ T7 (브랜치 정리 후 stale 알림 무의미)

T3 (독립)
T5 (독립)
T6 (독립)
```

## 작업 상세

### T1: git push (API 경유)
- **방법:** GitHub Git Data API로 blob/tree/commit/ref 생성
- **커밋:** `5a71f5e`를 원격에 반영
- **완료 조건:** 원격 HEAD = `5a71f5e`
- **검증:** `git log --oneline -1 origin/main` 원격 확인

### T2: develop 브랜치 정리
- **방법:** GitHub API로 develop 브랜치 삭제 또는 freeze
- **옵션 A:** 브랜치 삭제 (강력)
- **옵션 B:** README/CONTRIBUTING에 stale 표시 유지 (안전, 이미 적용됨)
- **권장:** 옵션 A (불필요한 브랜치 정리)

### T3: install.sh 테스트
- **방법:** `test_benchmark.py`에 Part 5 추가
- **검증 항목:** install.sh 존재, --dry-run 실행, --help 출력, --uninstall 로직
- **제약:** 실제 설치 실행 금지 (로컬 환경 보호)

### T4: CHANGELOG.md
- **포함:** v1.0.0 (초기 릴리즈) → P0-P5 audit → cycle1-3
- **형식:** Keep a Changelog (https://keepachangelog.com) 준수

### T5: TODO 정리
- **대상:** SKILL.md Future Work 섹션 (4개 항목)
- **조치:** 진행 상황 업데이트, 완료된 항목 체크

---

## 예상 소요 시간 합계

| 구분 | 시간 |
|------|------|
| T1 | 5m |
| T2 | 2m |
| T3 | 20m |
| T4 | 10m |
| T5 | 5m |
| T6 | 15m |
| T7 | 10m |
| **합계** | **~67m** |

💭 가정 — 실제 작업 시간은 예측치, 개별 편차 존재

---

## 다음 Step 입력값

- 작업 목록 7개
- 우선순위 정렬 완료
- 의존성 그래프
- 예상 시간 합계 ~67분
