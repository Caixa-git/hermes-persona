# Security Audit Methodology (kanban + persona)

## Proven pattern

The persona system successfully auto-adopts a **🔒 Security Engineer** role when tasked with a vulnerability assessment. The worker reads the agency-agents catalog, identifies `engineering/engineering-security-engineer.md` as the best fit, and conducts a structured review.

## Trigger

A kanban task with security-focused language in its title/body causes the persona worker to adopt Security Engineer. Explicit checklist items in `--body` produce better results.

```bash
hermes kanban create "Vulnerability assessment — <repo>" \
  --body 'Checklist:
1. install.sh — curl-pipe-bash safety, env handling, credential exposure
2. Source code — injection risks, hardcoded paths, path traversal
3. README — sensitive info disclosure, exposed URLs
4. Config/docs — XSS from GitHub raw fetch, canonical URL correctness
5. .gitignore — missed files
6. Supply chain risk assessment
7. Remediation recommendations for each finding
Output a structured vulnerability report to <path>/SECURITY_AUDIT.md'
```

## Checklist template

When creating a security audit task, structure `--body` with these categories:

1. **Distribution script** (`install.sh`) — curl-pipe-bash safety, sed fragility, backup creation, env var handling, credential exposure
2. **Source code** — hardcoded paths, command injection, path traversal, dead imports
3. **Prompt injection** — user-controlled content flowing into system prompts (kanban task titles, context files)
4. **Documentation** — sensitive info disclosure, promoted anti-patterns, dead reference links
5. **Network fetch** — GitHub raw URLs, TLS, content integrity, commit SHA pinning, MITM risk
6. **.gitignore** — missed patterns (`.env`, IDE dirs, backup files)
7. **Supply chain** — dependency tree, risk matrix, integrity gaps, positive practices

## Report structure

The worker outputs a report in this format:

```markdown
# Security Audit Report — <project>
**Date**: YYYY-MM-DD
**Auditor**: 🔒 Security Engineer
**Methodology**: STRIDE threat modeling, OWASP Top 10 mapping, supply chain risk analysis

## Severity classification
| Level | Definition |
|-------|-----------|
| Critical | RCE, auth bypass, credential theft, prompt injection with tool exec |
| High | Stored injection, privilege escalation, data exfiltration |
| Medium | Missing controls, defense-in-depth gaps, risky patterns |
| Low | Best practice deviations, hardening opportunities |
| Informational | Observations, suggestions |

## Per-file findings (numbered subsections)
Each finding includes: description, impact, evidence, exploit scenario, remediation

## Supply chain risk matrix
| Risk | Likelihood | Impact | Severity |
|------|-----------|--------|----------|

## Remediation recommendations (by priority)
### Critical/High — address immediately
### Medium — next release
### Low — when convenient
### Informational — roadmap

## Summary
Findings by severity, key strengths, primary concerns, risk posture
```

## Files to inspect

| File | What to check |
|------|--------------|
| `install.sh` | `set -euo pipefail`, credential exposure, sed backup, symlink scope |
| `*.py` test files | `subprocess.run()` calls, `os.system()`, `eval()`, path construction, path traversal |
| `README.md` | No secrets, no private URLs, no env var values |
| `skills/*/SKILL.md` | Injection from fetched content, dead reference paths |
| `.gitignore` | Missing `.env`, IDE dirs, backup files |
| `agent/prompt_builder.py` | KANBAN_GUIDANCE injection surface, context content scanning |

## Lessons from real run (hermes-persona v1.0)

- 445-line report, 6 medium + 4 low findings across 7 categories
- Worker read every file in the repo, ran `git ls-files`, checked `git status --short`
- Worker cross-referenced prompt_builder.py for injection vectors
- Worker included exploit scenarios and remediation code blocks
- Worker generated the report *before* completing the task — write to target path mid-execution
- Worker may create sub-tasks via `todo` tool for multi-part tasks — monitor with `hermes kanban log`
