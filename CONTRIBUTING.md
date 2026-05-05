# Contributing

PRs welcome! This repo distributes a single prompt file (`skills/persona/SKILL.md`) plus supporting tools and references.

## Quick start

```bash
git clone https://github.com/Caixa-git/hermes-persona
cd hermes-persona

# Install locally for testing
bash install.sh --dry-run
bash install.sh

# Run tests
python3 test_benchmark.py
```

## Development workflow

1. **Branch from `main`** (not `develop` — it's stale behind main)
2. **Edit `skills/persona/SKILL.md`** for persona logic changes
3. **Update references/** if adding citations or experiments
4. **Run `python3 test_benchmark.py`** — all tests must pass
5. **Open a PR to `main`**

## What to check before PR

- [ ] `test_benchmark.py` passes
- [ ] `install.sh --dry-run` format is valid
- [ ] SKILL.md YAML frontmatter is valid
- [ ] All referenced URLs use SHA-pinned commits (not `main` branch)
- [ ] `pyproject.toml` version matches git tag (if tagging)
- SHA change detection: `.github/workflows/sha-check.yml` runs weekly + on push to main
- `develop` branch is **stale** (behind `main`). New work branches from `main`.

## Design principles

- **Anima > Persona** — core nature always prevails on conflict
- **Single-file SKILL.md** — keep persona logic centralized
- **6 reference docs** — research backing for every design decision
- **SHA-pinned URLs** — no mutable dependencies
- **No hardcoded paths** — use `$HERMES_HOME` and dynamic resolution

## Adding a new reference document

1. Create `skills/persona/references/<topic>.md`
2. Link from the relevant section in `skills/persona/SKILL.md`
3. Add to the reference docs listing in the SKILL.md

## Testing

```bash
# Full test suite (network required for Part 2 & 3)
python3 test_benchmark.py

# Verify identity section integrity
python3 skills/persona/scripts/verify-identity-section.py

# Anima vs persona priority experiment (requires DEEPSEEK_API_KEY)
python3 skills/persona/scripts/test-subtle-contradiction.py
```
