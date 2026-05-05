# Task Breakdown — Cycle 1

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🏗️ Project Manager, S<2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `REQUIREMENTS_AND_SPEC_UPDATE.md`

---

## Task 목록

### T1: CHANGELOG Unreleased → v1.0.1 확정

- **Task ID:** C1-T1
- **제목:** CHANGELOG v1.0.1 릴리즈 날짜 확정
- **우선순위:** P1
- **Roadmap 연결:** P1
- **변경 대상 파일:** `CHANGELOG.md`
- **구현 내용:** `## [Unreleased]` 헤더 + 내용을 `## [1.0.1] - 2026-05-06`로 변경, `[Unreleased]` 링크 업데이트
- **완료 기준:** CHANGELOG에 v1.0.1 섹션이 날짜와 함께 표시
- **검증 방법:** `grep "1.0.1" CHANGELOG.md && grep "2026-05-06" CHANGELOG.md`
- **예상 리스크:** 낮음. 단순 텍스트 변경
- **Git 이력:** `docs: bump CHANGELOG v1.0.1 release date`

### T2: GitHub Release v1.0.1 생성

- **Task ID:** C1-T2
- **제목:** GitHub Release 생성 (API)
- **우선순위:** P1
- **Roadmap 연결:** P1
- **변경 대상 파일:** GitHub 저장소 메타데이터
- **구현 내용:** `gh api /repos/{owner}/{repo}/releases` POST로 Release 생성. body는 CHANGELOG v1.0.1 내용
- **완료 기준:** GitHub Releases 탭에 v1.0.1 표시
- **검증 방법:** `curl -s https://api.github.com/repos/Caixa-git/hermes-persona/releases/latest | jq .tag_name`
- **예상 리스크:** 낮음. gh CLI 인증됨 (GITHUB_TOKEN)
- **Git 이력:** GitHub Release + tag v1.0.1

### T3: git tag v1.0.1 생성

- **Task ID:** C1-T3
- **제목:** git tag v1.0.1 생성 및 push
- **우선순위:** P1
- **Roadmap 연결:** P1
- **변경 대상 파일:** git refs
- **구현 내용:** `git tag v1.0.1 && git push origin v1.0.1` (또는 API로 tag 생성)
- **완료 기준:** `git tag -l | grep v1.0.1`
- **검증 방법:** 원격 태그 조회
- **예상 리스크:** 중간. git push HTTPS 타임아웃 환경 이슈 → API 대체 가능
- **Git 이력:** tag v1.0.1

### T4: test_benchmark.py Part 5 — install.sh 검증

- **Task ID:** C1-T4
- **제목:** install.sh 단위 테스트 추가
- **우선순위:** P2
- **Roadmap 연결:** P2
- **변경 대상 파일:** `test_benchmark.py`
- **구현 내용:** Part 5 섹션 추가. 검증 항목: (a) 파일 존재, (b) shebang 확인, (c) --help 출력 확인 (subprocess 실행 없이 grep), (d) --dry-run 플래그 확인, (e) 주요 함수 존재 (install/update/uninstall/setup)
- **완료 기준:** test_benchmark.py --offline 23/23 통과
- **검증 방법:** `python3 test_benchmark.py --offline | grep "23/23"`
- **예상 리스크:** 중간. install.sh 내부 로직 실행 없이 정적 분석만 수행
- **Git 이력:** `test: add install.sh validation tests (Part 5)`

---

## 우선순위 정렬

```text
C1-T1 (CHANGELOG) ──→ C1-T2 (GitHub Release) ──→ C1-T3 (git tag)
                                                      │
C1-T4 (test install.sh) ──→ 독립 실행 가능 ──────────┘
```

## 예상 시간

| Task | 시간 |
|------|------|
| C1-T1 | 3m |
| C1-T2 | 5m |
| C1-T3 | 2m |
| C1-T4 | 20m |
| **합계** | **~30m** |

---

## 다음 Step 입력값

- Task 4개 (C1-T1~T4)
- 의존성: T1→T2→T3 순차, T4 독립
- 예상 30분
