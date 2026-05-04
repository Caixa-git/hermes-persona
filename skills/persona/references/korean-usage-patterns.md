# Korean Language Usage Patterns (한국어 사용 패턴)

## 개요 (Overview)

This document documents how the persona skill activates and operates in Korean
language contexts. Korean is fully supported — the 4 research-backed role
selection principles work identically in Korean as they do in English. The
difference is in the **activation patterns** (발동/이용/사용) and the
communication style expected of adopted roles.

## Activation Patterns (발동 패턴)

### Chat Mode (채팅)

```bash
# Korean session with persona skill loaded
hermes -s persona chat -q "보안 감사 진행해줘: 데이터베이스 접근 권한 검토"
# → 🔒 Security Engineer 역할 채택 → 작업 수행
```

The worker fetches the agency-agents catalog (English), identifies the 🔒 Security
Engineer role as the best match for "보안 감사", announces adoption in Korean
as `🎭 역할 채택: 🔒 Security Engineer`, and works the task in Korean.

### CLI Mode (CLI)

```bash
# Direct personified kanban task in Korean
hermes kanban create '[감사] DB 접근 권한 검토' \
  --body '모든 데이터베이스 사용자의 접근 권한을 검토하고 불필요한 권한을 제거하세요' \
  --skill persona

hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
# → Worker reads Korean body, adopts 🔒 Security Engineer
```

### Mixed Language (혼용)

```yaml
# Task body can mix Korean and English
body: |
  ## 목표
  Set up CI/CD pipeline with GitHub Actions
  
  ## 상세
  - GitHub Actions 워크플로우 생성
  - Deploy to AWS ECS
  - 테스트 자동화
```

The worker analyzes the task body for matching keywords. English technical terms
(CI/CD, GitHub Actions, AWS ECS) are recognized. The worker adopts ⚙️ DevOps
Automator and continues in the language of the task body.

## Usage Examples (이용 예시)

### Security Audit in Korean

```bash
hermes kanban create '[감사🔐] OWASP 상위 10대 취약점 점검' \
  --body 'OWASP Top 10 기준으로 웹 애플리케이션의 보안 취약점을 점검하고 보고서를 작성하세요' \
  --skill persona

hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

**Expected worker output (role adoption):**
```
🎭 역할 채택: 🔒 Security Engineer
OWASP Top 10 취약점 점검을 시작합니다...
```

### Frontend Development in Korean

```bash
hermes kanban create '[프론트] React 대시보드 제작' \
  --body 'D3.js를 이용한 실시간 데이터 시각화 대시보드를 React로 구현하세요. Material-UI 사용.' \
  --skill persona
```

**Expected role adoption:** 🎨 Frontend Developer

### Backend Architecture in Korean

```bash
hermes kanban create '[백엔드] REST API 설계' \
  --body '사용자 인증 시스템을 포함한 REST API를 설계하세요. JWT 토큰, PostgreSQL.' \
  --skill persona
```

**Expected role adoption:** 🏗️ Backend Architect

## Child Propagation (자식 전파)

Korean parent tasks propagate persona to children just like English tasks:

```python
kanban_create(
    title="프론트엔드: React 스토어프론트",
    assignee="persona-worker",
    skills=["persona"],
    parents=[parent_task_id],
)
```

Each child independently analyzes its Korean body and adopts the best-fitting
role. See `chain-propagation-test.md` for full propagation test details.

## Language Behavior Rules

| Rule | Behavior |
|------|----------|
| **Announcement** | Heartbeat text includes 🎭 followed by role name in English (e.g., `🎭 역할 채택: 🔒 Security Engineer`) |
| **Work output** | Worker produces output in the language of the task body |
| **Code** | Code examples and file contents remain in English (no Korean variable names) |
| **Comments** | Code comments match the task body language |
| **Metadata** | `kanban_complete` summary and metadata use the task body language |

## Known Edge Cases

| Case | Behavior |
|------|----------|
| Mixed Korean/English body | Worker uses the dominant language of the body for output |
| Korean role names in query | Not supported — role names must match English agency-agents catalog |
| Korean code comments | Worker comments code in Korean but preserves English syntax |
| English task + Korean instructions | Worker outputs in English with Korean task notes inline |

## References

- `chain-propagation-test.md` — Full propagation test transcript
- `benchmark-methodology.md` — 15-task benchmark design and results
- `dispatcher-worker-architecture.md` — Two-layer architecture documentation
