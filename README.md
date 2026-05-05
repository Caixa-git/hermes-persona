# 🎭 hermes-persona

Every kanban worker automatically adopts the best-fitting specialist role for its task. 172 roles from [agency-agents](https://github.com/msitarzewski/agency-agents) across 15 categories.

## One-line install

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

## Usage

```bash
hermes kanban create 'Security audit: OWASP top 10' --skill persona
hermes kanban assign t_xxxx persona-worker
hermes kanban dispatch
```

The worker fetches agency-agents, picks the best-fit role, and announces via heartbeat.

## Paired with

| System | Repo | Role |
|:-------|:-----|:-----|
| **Anima** | [hermes-anima](https://github.com/Caixa-git/hermes-anima) | Core nature (always-on identity) |
| **Persona** | this repo | Social role (opt-in specialist) |

- Persona = opt-in. Anima = always-on.
- Anima > Persona on conflict (nature prevails over role).
- When no specialist matches (confidence <30%), worker proceeds without a role — not with a forced mismatch.

## Structure

```
hermes-persona/
├── skills/persona/SKILL.md    ← The persona system (prompt)
├── install.sh                  ← One-line installer
├── test_benchmark.py           ← CI test
├── archive/                    ← Historical docs & single-use scripts
├── SECURITY_AUDIT.md           ← Minimal risk assessment
├── CONTRIBUTING.md
└── README.md
```

## Validation

```bash
python3 test_benchmark.py
```

## License

MIT
