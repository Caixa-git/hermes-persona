# Roadmap Item Selection — Cycle 1

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🧠 System Thinker + 📈 Product Manager, S=2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `NEXT_ROADMAP.md`, `DISCOVERY_BRIEF.md`, `QA_REPORT.md`

---

## 전체 Roadmap 항목

| ID | 항목 | 기존 분류 | RICE |
|----|------|-----------|------|
| P1 | GitHub Release v1.0.1 생성 | 단기 | 36 |
| P2 | install.sh 단위 테스트 (test_benchmark.py Part 5) | 단기 | 13.5 |
| P3 | PyPI 패키징 타당성 조사 | 단기 | 2.7 |
| M1 | CDPD 모델 교정 (Φ/α/β/Γ_base 재계산) | 중기 | — |
| M2 | Future Work 4개 항목 중 1-2개 해결 | 중기 | — |
| M3 | 역할 카탈로그 오프라인 완전 캐시 | 중기 | — |
| L1 | 멀티-모델 멀티-페르소나 | 장기 | — |
| L2 | 자동 CDPD 파라미터 교정 파이프라인 | 장기 | — |
| L3 | hermes-anima 통합 릴리즈 | 장기 | — |
| T6 | PyPI 패키징 검토 | 미해결 | — |
| F-4 | Future Work 4개 항목 (SKILL.md) | 미해결 | — |
| B1 | git push HTTPS 타임아웃 | 미해결 | — |

✅ 확인된 사실

## 이번 사이클 선택

### Now (2개)

| 항목 | 선택 이유 | 예상 시간 |
|------|-----------|-----------|
| **P1: GitHub Release v1.0.1** | RICE 1위. CHANGELOG 내용은 이미 있음. GitHub UI 또는 API로 Release 생성만 하면 됨. 릴리즈 이력 조건 🟡→✅로 전환. | 10m |
| **P2: install.sh 단위 테스트** | RICE 2위. 설치 신뢰성에 직접 영향. test_benchmark.py에 Part 5로 추가. 검증 방법 명확. | 20m |

### Next (다음 사이클 후보)

| 항목 | 제외 이유 |
|------|-----------|
| M1 (CDPD 교정) | 현재 모델(deepseek-v4-flash) 변경 없음. 교정할 대상 없음. |
| M3 (오프라인 캐시) | 이미 clone --depth=1로 캐시 있음. full clone은 대역폭 낭비. |
| P3 (PyPI) | Hermes 스킬 구조와 충돌 가능. 설계 결정 필요. |

### Later

| 항목 | 상태 유지 이유 |
|------|---------------|
| L1-L3, T6, F-4, B1 | 모두 장기/환경 귀속. 현재 사이클에서 처리 불필요. |

📐 합리적 추정

## 이번 사이클 목표

1. GitHub Release v1.0.1 생성 → 릴리즈 이력 조건 ✅
2. install.sh 설치 신뢰성 검증 추가 → test_benchmark.py 18→23테스트
3. CHANGELOG Unreleased → v1.0.1로 확정

---

## 완료 기준

| 조건 | 현재 | 목표 |
|------|------|------|
| GitHub Release 존재 | ❌ | ✅ v1.0.1 |
| install.sh 검증 | ❌ | ✅ test_benchmark.py Part 5 |
| CHANGELOG v1.0.1 | Unreleased | 2026-05-06 확정 |
| 기존 테스트 | ✅ 18/18 | ✅ 23/23 (회귀 없음) |

---

## 다음 Step 입력값

- Now 항목: P1 (GitHub Release), P2 (install.sh test)
- Next 항목: M1, M3
- 목표: Release 존재 + install.sh 검증 + CHANGELOG 확정
