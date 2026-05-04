<p align="center">
  <samp>
    <strong><big>🎭 Hermes Persona</big></strong><br>
    <sub>칸반 워커가 작업을 분석하고 210개 전문가 역할 중 최적을 자동 선택합니다</sub>
  </samp>
</p>

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent">
    <img src="https://img.shields.io/badge/Hermes_Agent-Compatible-8A2BE2?style=flat-square&logo=robot&logoColor=white" alt="Hermes Agent">
  </a>
  <a href="https://github.com/msitarzewski/agency-agents">
    <img src="https://img.shields.io/badge/agency--agents-172_roles-FF6B6B?style=flat-square" alt="Agency Agents">
  </a>
  <a href="https://github.com/Caixa-git/hermes-persona/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square" alt="MIT">
  </a>
  <img src="https://img.shields.io/badge/✅_47_tests-passing-22c55e?style=flat-square" alt="47 tests passing">
</p>

---

## 설치

Hermes Agent가 설치된 환경에서 아래 명령어 2개면 끝납니다.

```bash
# 1. kanban toolset 활성화
hermes config set toolsets hermes-cli,kanban

# 2. persona 시스템 설치
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

설치가 완료되면 KANBAN_GUIDANCE에 persona 섹션이 추가됩니다. 이후부터 모든 칸반 워커가 자동으로 역할 분석을 수행합니다.

> 이미 `~/.hermes/config.yaml`에 `toolsets: [hermes-cli, kanban]`가 있다면 1번은 건너뛰어도 됩니다.

---

## 사용법

특별한 플래그가 필요하지 않습니다. 평소처럼 칸반 태스크를 생성하기만 하면 됩니다.

```bash
hermes kanban create "REST API 서버를 JWT 인증과 함께 구축"
```

워커가 아래 과정을 자동으로 처리합니다.

<p align="center">
  <img src="docs/kanban-screenshot.svg" alt="Kanban tasks with adopted roles" width="90%">
</p>

| 태스크 | 워커가 선택한 역할 |
|--------|-----------------|
| React 대시보드 UI 개발 | 🎨 Frontend Developer |
| AWS CI/CD 파이프라인 구축 | 🚀 DevOps Automator |
| PostgreSQL 쿼리 성능 최적화 | 🗄️ Database Optimizer |
| REST API + JWT 인증 | 🏗️ Backend Architect |
| API 엔드포인트 취약점 진단 | 🔒 Security Engineer |

---

## 동작 방식

```
워커 생성
  → KANBAN_GUIDANCE 로드 (persona 섹션 내장)
  → 태스크 분석 (kanban_show)
  → GitHub raw ← README 조회
  → 210개 역할 중 최적 매칭
  → kanban_heartbeat("🎭 Role adopted: 🏗️ Backend Architect")
  → 역할 .md 로드
  → 전문가 모드 ON
```

모든 과정은 GitHub raw URL 기반이라 로컬 저장소가 전혀 필요 없습니다.

**일반 채팅에서 시작하려면** `toolsets`에 `kanban`이 추가된 상태라면 아래처럼 직접 요청해도 됩니다.

```
사용자: "전자상거래 플랫폼 만들어줘"
  → Hermes: kanban_create(...)
  → Planner: 태스크 분해 → kanban_create × N
  → 각 워커: persona → 역할 채택 → 병렬 실행
```

---

## Hermes Agent 변경 사항

Hermes Persona가 Hermes Agent에 가하는 변경은 아래 2가지입니다.

### 1. KANBAN_GUIDANCE (prompt_builder.py)

`## persona — role adoption` 섹션 13줄이 추가됩니다. persona 스킬을 로드하지 않은 워커는 평소와 동일하게 동작합니다.

<details>
<summary>추가된 코드 보기</summary>

```python
"## persona — role adoption\n"
"\n"
"1. **Analyze your task.** `kanban_show()` then analyze the task body.\n"
"2. **Pick a role.** Fetch the README from the agency-agents repository:\n"
"   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`\n"
"   → scan 17 categories, 210+ specialist roles, pick the best fit.\n"
"   Note the role's **emoji** from the README table.\n"
"3. **Announce adoption.** Call `kanban_heartbeat(note=...` with:\n"
"   `🎭 Role adopted: {emoji} {role-name}`\n"
"4. **Load the personality.** Fetch the role's full specification:\n"
"   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`\n"
"5. **Adopt it.** Become that expert. Follow its rules, standards, and process.\n"
"6. **Act.** Work on your task as that role.\n"
"If no matching role exists, proceed as a generalist."
```

</details>

### 2. config.yaml

`toolsets`에 `kanban`이 추가되어야 채팅 모드에서 칸반 툴을 사용할 수 있습니다.

```yaml
toolsets:
- hermes-cli
- kanban
```

> `hermes config set toolsets hermes-cli,kanban` 명령어로 간단히 설정할 수 있습니다.

---

## 프로젝트 구조

```
hermes-persona/
├── README.md              # 설명서
├── install.sh             # 설치 스크립트 (1-커맨드)
├── test_persona.py        # 자동화 테스트 (32개)
├── .gitignore
├── docs/
│   ├── kanban-screenshot.svg  # 칸반 리스트 예시 이미지
│   └── persona-v2-plan.md     # v2 설계 문서 (다차원 매칭)
└── skills/
    └── persona/
        └── SKILL.md           # persona 스킬 참조
```

---

## 로드맵

- [x] KANBAN_GUIDANCE 내장 — `--skill persona` 불필요, 모든 워커 자동 적용
- [x] 이모지 역할 표시 — 칸반 이벤트에 `🎭 Role adopted: 🏗️ Role Name` 기록
- [ ] **지능형 역할 선택** — RIASEC + JCM 기반 다차원 벡터 매칭
- [ ] 멀티 역할 분해 — 단일 태스크 → 복수 전문가 sub-task 자동 생성
- [ ] 성과 피드백 — 역할 선택 이력 기반 추천 개선

---

## 크레딧

| 프로젝트 | 제작자 | 설명 |
|----------|--------|------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | [msitarzewski](https://github.com/msitarzewski) | 15개 분야 172개 전문가 역할 카탈로그 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [Nous Research](https://nousresearch.com) | 칸반 기반 멀티에이전트 오케스트레이션 |

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>만든 사람 <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
