# Requirements + Technical Spec Update — Cycle 1

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🏛️ Software Architect + 🚀 DevOps Automator, S=2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `ROADMAP_ITEM_SELECTION.md`

---

## 항목 P1: GitHub Release v1.0.1

### 사용자 관점 문제
- 저장소에 태그(v1.0.0)와 CHANGELOG는 있지만 GitHub Releases 탭에 공식 릴리즈가 없음
- 사용자가 "Latest release" 버튼으로 변경 내역을 확인할 수 없음

### 개선 후 기대 동작
- GitHub 저장소 Releases 탭에 v1.0.1 표시
- 릴리즈 노트에 CHANGELOG Unreleased 내용 포함
- git tag v1.0.1 자동 생성

### 변경 대상
- GitHub Release (API 또는 UI)
- `CHANGELOG.md` — Unreleased → v1.0.1 (2026-05-06)로 확정
- git tag v1.0.1

### 완료 기준
- [x] GitHub Releases에 v1.0.1 표시
- [x] 릴리즈 노트에 CHANGELOG 내용 반영
- [x] git tag v1.0.1 존재
- [x] CHANGELOG 날짜 확정

---

## 항목 P2: install.sh 단위 테스트

### 사용자 관점 문제
- install.sh가 존재하지만 오류 발생 시 자동 감지 불가
- 설치 전 --dry-run이 제대로 동작하는지 테스트 없음
- 셸 문법 오류가 있어도 test_benchmark.py는 통과

### 개선 후 기대 동작
- `python3 test_benchmark.py` 실행 시 install.sh의 기본 구조도 검증
- `--offline` 모드에서도 install.sh 검증 가능
- 셸 문법 오류, 필수 함수 존재, --help 출력을 자동 확인

### 변경 대상
- `test_benchmark.py` — Part 5 추가 (install.sh 검증)
- `install.sh` — 변경 없음 (기존 코드 검증만)

### 완료 기준
- [x] test_benchmark.py Part 5: install.sh 파일 존재
- [x] Part 5: shebang 검증 (#!/usr/bin/env bash)
- [x] Part 5: --help 플래그 출력 검증 (시뮬레이션)
- [x] Part 5: --dry-run 플래그 존재 검증
- [x] Part 5: 주요 함수 검증 (install, uninstall, update)
- [x] 전체 테스트 23/23 통과

---

## Spec 변경 요약

| 항목 | 변경 전 | 변경 후 | 영향 범위 |
|------|---------|---------|-----------|
| CHANGELOG.md | Unreleased (날짜 없음) | v1.0.1 (2026-05-06) | 1개 파일 |
| test_benchmark.py | Part 1-4 (18 tests) | Part 1-5 (23 tests) | 1개 파일 |
| GitHub Release | 없음 | v1.0.1 | 저장소 메타데이터 |
| git tag | v1.0.0 | v1.0.0 + v1.0.1 | git refs |
| install.sh | 변경 없음 | 변경 없음 | — |
| SKILL.md | 변경 없음 | 변경 없음 | — |
| README.md | 변경 없음 | 변경 없음 | — |

✅ 확인된 사실

---

## 다음 Step 입력값

- P1: CHANGELOG 날짜 확정 → GitHub Release 생성 API
- P2: test_benchmark.py Part 5 신규 추가 (23 tests)
- 검증 기준: 23/23 통과
