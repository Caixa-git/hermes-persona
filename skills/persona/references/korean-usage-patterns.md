# 🇰🇷 Korean conversational usage patterns

When Hermes interacts with a Korean-speaking user, these natural-language patterns invoke persona-powered kanban workers.

## Language boundary rule

**Korean is for conversational chat only.** All GitHub-facing artifacts must be in English:

| Context | Language | Examples |
|---------|----------|----------|
| Discord/chat messages | Korean | 요청, 피드백, 상태 보고 |
| GitHub issues | English | Issue titles, descriptions, comments |
| PRs | English | Titles, body, commit messages |
| README/docs/code | English | All documentation, comments, variable names |
| Branch names | English | `fix/xxx`, `feature/xxx`, `release/x.x.x` |

Korean examples are acceptable in code comments only. This is a strict rule — every GitHub artifact is potentially visible to open-source contributors.

## The 4 activation patterns

| # | Pattern | Korean input | What happens |
|---|---------|-------------|-------------|
| 1 | Explicit `--skill persona` flag | `~~ 작업 해줘 페르소나를 이용해서` | Worker spawns with `--skill persona`, adopts expert role |
| 2 | Natural language request | `페르소나를 이용해서 ~~ 작업을 해줘` | System detects "페르소나" keyword, passes `--skill persona` |
| 3 | Conditional activation | `~~작업을 해줘 필요하다면 페르소나를 사용해줘` | Generalist by default, activates persona when task complexity warrants it |
| 4 | Playful variant | `페르소나를 발동해줘` | "Activate persona!" — same behavior as #2, playful phrasing |

## Terminology

| Korean | English | Usage |
|--------|---------|-------|
| 발동하다 | activate/invoke | Preferred for playful requests — `페르소나를 발동해서` |
| 이용하다 | use/employ | Neutral — `페르소나를 이용해서` |
| 사용하다 | use | Conditional — `필요하다면 페르소나를 사용해서` |

## Examples in context

### Chat session

```bash
hermes chat
```

```
👤 "페르소나를 발동해서 이커머스 플랫폼을 구축해줘"
→ System detects persona request → creates kanban tasks with --skill persona
→ 🏛️ Software Architect decomposes → 🎨 Frontend + 🏗️ Backend + 🚀 DevOps
```

```
👤 "보안 감사 진행해줘 페르소나를 이용해서"
→ System creates kanban task with --skill persona
→ Worker adopts 🔒 Security Engineer
```

```
👤 "DB 최적화 해줘 필요하면 페르소나 써"
→ System creates kanban task (no --skill persona by default)
→ Worker evaluates complexity → if high, activates persona and picks 🗄️ Database Optimizer
```

### CLI

```bash
# Korean annotated: --skill persona 플래그로 워커가 전문가 역할 채택
hermes kanban create 'JWT 인증 API 구축' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

## Design rationale

Persona is **opt-in** (`--skill persona` flag). The Korean patterns above are natural-language equivalents that map to the same flag-based activation. Without one of these patterns, workers proceed as generalists.

The "발동" variant exists because it's fun and distinctive — "activate persona!" maps well to the system's role-adoption metaphor.
