# Next Roadmap — hermes-persona

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🧠 System Thinker + 📈 Product Manager, S=2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `RELEASE_CHECKLIST_AND_DEPLOYMENT_PLAN.md`

---

## 단기 (1-2주)

| 우선순위 | 항목 | RICE 점수 | 비고 |
|----------|------|-----------|------|
| P1 | GitHub Release v1.0.1 생성 | R:4 I:3 C:3 E:1 = 36 | 릴리즈 노트 포함 |
| P2 | install.sh 단위 테스트 (test_benchmark.py Part 5) | R:3 I:3 C:3 E:2 = 13.5 | 설치 신뢰성 |
| P3 | PyPI 패키징 타당성 조사 | R:2 I:2 C:2 E:3 = 2.7 | Hermes 스킬 구조와 충돌 확인 필요 |

💭 가정 — RICE 점수는 추정치, 실제 우선순위는 상황에 따라 변동 가능

## 중기 (1-2개월)

| 우선순위 | 항목 | 근거 |
|----------|------|------|
| M1 | CDPD 모델 교정 (Φ/α/β/Γ_base 재계산) | 새 모델 등장 시 최적 파라미터 변화 가능 |
| M2 | Future Work 4개 항목 중 1-2개 해결 | 기술 부채 감소 |
| M3 | 역할 카탈로그 오프라인 완전 캐시 (git clone full) | 네트워크 불안정 시 대응 |

📐 합리적 추정

## 장기 (3-6개월)

| 항목 | 설명 |
|------|------|
| L1 | 멀티-모델 멀티-페르소나 (major on A, minor on B) | Reasoning Trap 우회 (Shin 2026) |
| L2 | 자동 CDPD 파라미터 교정 파이프라인 | 새 모델 벤치마크 자동화 |
| L3 | hermes-anima와 통합 릴리즈 | 두 저장소 동기화 필요 |

💭 가정

## 미해결 이슈

| ID | 이슈 | 우선순위 | 상태 |
|----|------|----------|------|
| T6 | PyPI 패키징 검토 | P3 | ⏳ 보류 |
| F-4 | Future Work 4개 항목 (SKILL.md) | M2 | ⏳ 개방 |
| B1 | git push HTTPS 타임아웃 (환경) | P1 | ⚠️ API 우회 중, 환경 귀속 |

✅ 확인된 사실

## 기술 부채 현황

| 부채 | 유형 | 해결 계획 |
|------|------|-----------|
| PyPI 미배포 | Prudent deliberate | P3 검토 → 결정 |
| install.sh 단위 테스트 부재 | Reckless deliberate | P2 단기 해결 |
| CHANGELOG 부재 | Prudent deliberate | ✅ 해결 |
| develop 브랜치 방치 | Inadvertent | ✅ 해결 (삭제) |

✅ 확인된 사실 / 📐 합리적 추정

## 핵심 권장사항

1. **즉시:** GitHub Release v1.0.1 생성 — 릴리즈 노트는 CHANGELOG.md 기반
2. **1주일 내:** install.sh 단위 테스트 추가 — 설치 신뢰성 확보
3. **1개월 내:** PyPI 여부 결정 — pip install vs curl | bash 전략 선택
4. **지속:** Future Work 4개 항목 중 1개씩 해결 — 기술 부채 관리

---

## 완료 기준 체크

| 조건 | 상태 |
|------|------|
| 기능 완성 | ✅ |
| 회귀 제로 | ✅ |
| 문서 현행화 | ✅ |
| 보안 기본 | ✅ |
| 릴리즈 이력 | 🟡 (CHANGELOG ✅, GitHub Release ⬜) |
