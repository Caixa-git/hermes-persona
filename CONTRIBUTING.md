# Contributing to Hermes Persona

## Git Flow
- `main` — production
- `develop` — integration  
- `fix/*`, `feature/*` — branch from develop, PR to develop

No direct commits to main or develop.

## Local dev
```bash
python3 test_benchmark.py
bash -n install.sh
```

## PR checklist
- [ ] Tests pass
- [ ] bash -n install.sh valid
- [ ] Reference docs match SKILL.md mentions
- [ ] Branch follows Git Flow naming
- [ ] Commits reference issue number
