# Security Audit — hermes-persona

**Repository:** https://github.com/Caixa-git/hermes-persona
**Date:** 2026-05-06

## Risk Assessment

| Vector | Risk | Rationale |
|:-------|:----:|:----------|
| **Code execution** | None | No Python/JS/binary shipped. Only SKILL.md (prompt text). |
| **Credential exposure** | None | No API keys, tokens, or secrets in repo. |
| **Supply chain** | Low | Pinned commit `783f6a72` for agency-agents catalog fetch. Network read-only at runtime. |
| **Prompt injection** | Low | SKILL.md is system prompt — advisory context, not executable. |

## Verdict

This repo distributes a **prompt file** (`SKILL.md`). No executable code, no credentials, no network write operations. Risk profile: minimal.
