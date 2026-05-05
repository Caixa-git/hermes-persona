# Roadmap Update — Cycle 1

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🧠 System Thinker + 📈 Product Manager, S=2)

---

## Completed

- **P1: GitHub Release v1.0.1** — 생성 완료 (CHANGELOG 기반 릴리즈 노트)
- **P2: install.sh 단위 테스트** — test_benchmark.py Part 5 추가, 28/28 통과
- **read_skill() profile-context fallback** — os.path.expanduser 환경에서도 동작

## Partially Completed

— (없음)

## Newly Discovered

- test_benchmark.py가 profile-context 환경에서 read_skill() 실패 → fallback 경로로 해결
- git push HTTPS 타임아웃 환경 이슈 지속 확인 → API 우회 표준화 필요

## Deferred (다음 사이클)

- **P3 (PyPI)**: Hermes 스킬 구조와 충돌 가능. 설계 결정 필요
- **M1 (CDPD 교정)**: 현재 모델 변경 없음. 새 모델 등장 시점에 재검토
- **M3 (오프라인 캐시)**: 이미 depth=1 clone으로 충분

## Removed

— (없음)

---

## Next Cycle Recommendation

### Now (1-3개 항목)

| 항목 | 근거 |
|------|------|
| M2: Future Work 4개 중 1개 해결 | 기술 부채 감소. CDPD 교정 프로토콜 우선 |
| M1: CDPD 교정 대비 벤치마크 스크립트 작성 | 새 모델 arrival 시 바로 사용 가능 |

### Next (3-5개)

| 항목 | 근거 |
|------|------|
| install.sh 실제 실행 테스트 (Docker 환경) | 정적 분석 → 동적 검증으로 확장 |
| scripts/patch-gateway-anima-persona.py 단위 테스트 | 패치 신뢰성 확보 |

### Later

| 항목 | 비고 |
|------|------|
| L1: 멀티-모델 멀티-페르소나 | Shin 2026 Reasoning Trap 우회 |
| L2: 자동 CDPD 파라미터 교정 | 새 모델 등장 시 |
| L3: hermes-anima 통합 릴리즈 | 두 저장소 동기화 |
| PyPI 패키징 | 설계 결정 후 진입 |
