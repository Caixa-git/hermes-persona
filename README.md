<p align="center">
  <samp>
    <strong>🎭 Hermes Persona</strong><br>
    <sub>칸반 워커가 작업 분석 후 172개 전문가 역할 중 최적을 선택합니다</sub>
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

**설치 — 1초면 끝납니다**

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

그런 다음:

```bash
hermes kanban create 'REST API 서버를 JWT 인증과 함께 구축' --skill persona
```

워커가 스스로 Backend Architect를 찾아 작업합니다.

---

<p>
  <strong>👀 한눈에 보는 동작:</strong><br>
  <code>워커 생성</code> → <code>persona 스킬 로드</code> → <code>GitHub raw ← README.md</code> → <code>작업 분석</code> → <code>역할 선정</code> → <code>.md 로드</code> → <code>🎭 전문가 모드</code>
</p>

<br>

---

## 왜 Hermes Persona인가

| 문제 | 해결 |
|------|------|
| 칸반 워커가 맥락 없이 작업을 수행 | 워커가 작업을 분석하고 **전문가 역할을 스스로 선택** |
| 172개 역할을 로컬에 저장/관리 | **git clone 필요 없음** — curl로 실시간 조회 |
| 역할마다 별도 스킬 생성 필요 | **단일 스킬** (`persona`)로 모든 역할 커버 |

## Hermes Agent 변경 사항

Hermes Persona가 수정하는 것은 **KANBAN_GUIDANCE 한 곳**뿐입니다.

| 항목 | 내용 |
|------|------|
| 수정 파일 | `agent/prompt_builder.py` |
| 추가된 코드 | `## persona — role adoption` 섹션 (12줄) |
| 동작 | 워커가 spawn될 때 시스템 프롬프트에 주입 → `--skill persona` 감지 → 역할 검색 및 채택 |
| 영향 범위 | persona 스킬이 없는 워커는 **동작 변화 없음** (`proceed as a generalist` 폴백) |

<details>
<summary><strong>🔧 추가된 코드 보기</strong></summary>

```python
"## persona — role adoption\n"
"\n"
"If you have the `persona` skill loaded:\n"
"1. **Read your task.** `kanban_show()` then analyze the task body.\n"
"2. **Pick a role.** Fetch the README from the agency-agents repository:\n"
"   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`\n"
"   → scan 17 categories, 210+ specialist roles, pick the best fit.\n"
"3. **Load the personality.** Fetch the role's full specification:\n"
"   `curl -s https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`\n"
"4. **Adopt it.** Become that expert. Follow its rules, standards, and process.\n"
"5. **Act.** Work on your task as that role.\n"
"If no matching role exists, proceed as a generalist."
```

</details>

<br>

## 사용 예시

```bash
# 프론트엔드
hermes kanban create 'React 대시보드 UI 개발' --skill persona
# → Frontend Developer 선택

# 백엔드
hermes kanban create 'REST API + JWT 인증' --skill persona
# → Backend Architect 선택

# 보안 감사
hermes kanban create 'API 취약점 스캔' --skill persona
# → Security Engineer 선택
```

---

## 크레딧

| 프로젝트 | 제작자 | 설명 |
|----------|--------|------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | msitarzewski | 15개 분야 172개 전문가 역할 카탈로그. 이 프로젝트의 핵심입니다. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | 칸반 기반 멀티에이전트 오케스트레이션. 페르소나 시스템의 런타임입니다. |

---

## 로드맵

- [x] 기본 역할 채택 — README 스캔 → 역할 선정 → .md 로드 (✅ 47/47 테스트 통과)
- [ ] **지능형 역할 선택** — 작업 분석 기반 최적 역할 추천 (에이전트 연구 논문 활용)
- [ ] 멀티 역할 구성 — 단일 작업을 복수 전문가에게 분할
- [ ] 성과 피드백 루프 — 역할 선택 이력 기반 추천 개선

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>만든 사람 <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
