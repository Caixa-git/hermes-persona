<p align="center">
  <samp>
    <strong>🎭 Hermes Persona</strong><br>
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

<br>

---

## 📦 설치

### 1. Hermes Agent 설치

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 2. Hermes Persona 설치

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

### 설치 확인

```bash
# KANBAN_GUIDANCE에 persona 섹션이 추가되었는지 확인
hermes kanban create "테스트" && hermes kanban list
# → 워커가 자동으로 역할 분석 → 실행
```

---

## 🎯 동작 방식

```
워커 생성 ─→ KANBAN_GUIDANCE 로드 (persona 섹션 내장)
  → 태스크 분석 (kanban_show)
  → GitHub raw ← README 조회 (curl)
  → 210개 역할 중 매칭
  → kanban_heartbeat("🎭 Role adopted: 🏗️ Backend Architect")
  → 역할 .md 로드
  → 전문가 모드 ON → 태스크 실행
```

모든 칸반 워커가 **자동**으로 수행합니다. `--skill persona` 같은 플래그가 **필요 없습니다.**

<p align="center">
  <img src="docs/kanban-screenshot.svg" alt="Kanban tasks with adopted roles" width="90%">
</p>

---

## 🤔 사용자는 아무것도 할 필요가 없습니다

일반적인 칸반 명령어만 사용하면 됩니다:

```bash
hermes kanban create "React 대시보드 UI 개발"
hermes kanban create "AWS CI/CD 파이프라인 구축"
hermes kanban create "PostgreSQL 쿼리 성능 최적화"
```

워커가 스스로:

| 태스크 | 워커가 선택한 역할 |
|--------|-------------------|
| React 대시보드 UI | 🎨 Frontend Developer |
| AWS CI/CD 파이프라인 | 🚀 DevOps Automator |
| PostgreSQL 최적화 | 🗄️ Database Optimizer |
| REST API + JWT | 🏗️ Backend Architect |
| API 취약점 진단 | 🔒 Security Engineer |

---

## 🔧 Hermes Agent 변경 사항

**KANBAN_GUIDANCE에 persona 섹션 1개를 추가했습니다.**

| 항목 | 내용 |
|------|------|
| 수정 파일 | `agent/prompt_builder.py` |
| 추가된 코드 | 13줄 (아래 참조) |
| 영향 범위 | 모든 칸반 워커 — 단, 매칭 역할이 없으면 일반 워커로 동작 |

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

---

## 🗺️ 로드맵

- [x] KANBAN_GUIDANCE 내장 — `--skill persona` 불필요
- [x] 이모지 역할 표시 — 칸반 이벤트에 기록
- [ ] **지능형 역할 선택** — 다차원 벡터 유사도 기반 최적 역할 추천
- [ ] 멀티 역할 분해 — 단일 태스크 → 복수 전문가 sub-task 자동 생성
- [ ] 성과 피드백 — 역할 선택 이력 기반 지속 개선

---

## 🙏 크레딧

| 프로젝트 | 제작자 | 설명 |
|----------|--------|------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | [msitarzewski](https://github.com/msitarzewski) | 15개 분야 172개 전문가 역할 카탈로그 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [Nous Research](https://nousresearch.com) | 칸반 기반 멀티에이전트 프레임워크 |

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>만든 사람 <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
