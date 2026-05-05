# Security Audit Methodology — 🔒 Security Engineer Persona

## Overview

This document defines the step-by-step security audit workflow when a kanban
worker adopts the 🔒 Security Engineer role. The workflow is designed for
hermes-persona repository audits but applies to any codebase.

## Audit Phases

### Phase 1: Reconnaissance (10% of time)

Read the repository structure and identify high-risk areas before deep-diving.

```bash
# Map the attack surface
# 1. List all executable files
find . -type f -executable | sort

# 2. Identify config files with secrets potential
find . -name "*.env*" -o -name "*secret*" -o -name "*credential*" -o -name "*config*"

# 3. Find network-touching code
grep -rn "requests\|urllib\|curl\|http://\|https://" --include="*.py" --include="*.sh" --include="*.js"

# 4. List all dependencies
cat requirements.txt pyproject.toml package.json 2>/dev/null || echo "No dep files found"

# 5. Check permissions
ls -la install.sh *.sh
```

Document the initial risk inventory before proceeding.

### Phase 2: Vulnerability Scan (40% of time)

Systematically inspect each high-risk area. Use a checklist approach.

**🔑 Secrets and Credentials**

| Check | Method |
|-------|--------|
| Hardcoded API keys | `grep -rn "sk-\|api_key\|API_KEY\|secret\|password\|token" --include="*.py" --include="*.sh" --include="*.yaml" --include="*.yml"` |
| .env files committed | `git log --diff-filter=A --name-only --pretty=format: -p -- .env*` |
| Credentials in tests | `grep -rn "api_key\|password\|secret" tests/` |
| COMMIT_CHECK: Review staged changes before commit | `git diff --cached --check` |

**🔐 Code Injection**

| Check | Method |
|-------|--------|
| eval/exec usage | `grep -rn "eval\|exec\|compile\|__import__" --include="*.py"` |
| Shell injection | `grep -rn "os.system\|subprocess\|Popen\|communicate" --include="*.py"` |
| SQL injection | `grep -rn "execute\|cursor\|query.*+" --include="*.py"` |
| Unsafe YAML load | `grep -rn "yaml.load(" --include="*.py"` (should use `yaml.safe_load`) |

**🏗️ Supply Chain**

| Check | Method |
|-------|--------|
| Unpinned dependencies | Review `requirements.txt`, `pyproject.toml` for version ranges |
| Direct curl-pipe-bash | `grep -rn "curl.*|.*bash\|curl.*sh\|wget.*|.*bash" --include="*.sh" --include="*.md"` |
| SHA256 verification | Check if install.sh.sha256 exists and is verified before install |
| SBOM | Check if Software Bill of Materials is generated |

**📁 File System**

| Check | Method |
|-------|--------|
| World-writable files | `find . -perm -o+w -type f` |
| Unsafe install paths | Review `install.sh` for `sudo` usage or writes to `/tmp` |
| Symlink attacks | `find . -type l` and review target paths |

### Phase 3: Deep Dive (30% of time)

For each finding from Phase 2, trace the code path:

1. **Read the file** containing the issue
2. **Understand the context** — is this a real vulnerability or a false positive?
3. **Determine exploitability** — what would an attacker need to exploit this?
4. **Assess impact** — what's the worst-case outcome?
5. **Propose mitigation** — specific code change or process change

**Severity classification:**

| Severity | Definition | Action |
|----------|------------|--------|
| 🔴 Critical | Remote code execution, credential leaks | Fix immediately, block CI |
| 🟠 High | Privilege escalation, data exposure | Fix this sprint |
| 🟡 Medium | Best practice violation, defense in depth | Fix next sprint |
| 🟢 Low | Informational, hardening opportunity | Document, fix when convenient |

### Phase 4: Report (20% of time)

Write a structured audit report. Include:

```markdown
# Security Audit Report — <repository name>

**Date:** <date>
**Auditor:** 🔒 Security Engineer (persona)
**Repository:** <repo path>
**Branch:** <branch>
**Commit:** <commit hash>

## Summary

<2-3 sentence overview of findings>

## Findings

### [CRITICAL] Finding title
**File:** path/to/file.py:42
**Severity:** 🔴 Critical
**Type:** Hardcoded API key

**Issue:**
<description>

**Exploitation:**
<how an attacker would exploit this>

**Mitigation:**
<specific code fix>

### [HIGH] Finding title
...

## Post-Fix Re-Audit

After fixes are applied, re-run:
```bash
# Regression check
grep -rn "hardcoded_pattern" path/to/file.py
# Expected: no matches
```

If all findings are resolved, update the report with verification notes.
```

## Persona-Specific Guidance

When adopting the 🔒 Security Engineer role:

1. **Assume breach mentality.** Think about what an attacker would look for.
2. **Be thorough, not alarmist.** Distinguish real vulnerabilities from
   theoretical risks.
3. **Provide actionable fixes.** Every finding should include a specific code
   change, not a vague recommendation.
4. **Document false positives.** If you spend time investigating something
   that turns out to be safe, note it — saves the next auditor's time.

## Audit Checklist Reference

```bash
# Quick audit command — run all at once
echo "=== Secrets ==="
grep -rn "sk-\|api_key\|API_KEY\|secret\|password\|token" --include="*.py" --include="*.sh" --include="*.yaml" .
echo "=== Injection ==="
grep -rn "eval\|exec\|os.system" --include="*.py" .
echo "=== Permissions ==="
find . -perm -o+w -type f -name "*.sh" -name "*.py"
echo "=== Supply Chain ==="
grep -rn "curl.*|.*bash\|pip install\|npm install" --include="*.sh" --include="*.md" .
echo "=== Shellcheck ==="
find . -name "*.sh" -exec shellcheck {} \; 2>/dev/null || echo "shellcheck not installed"
```
