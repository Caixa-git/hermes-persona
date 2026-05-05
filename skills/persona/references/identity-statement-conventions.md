# Identity Statement Conventions

## Principle

Identity statements in persona skill files MUST use the **"You ARE"** level — not "You believe" or "You value."

## Why

- **"You ARE"** → declarative identity. The agent *is* the role. Strongest framing for consistent behavior.
- **"You believe"** → epistemic stance. Introduces ambiguity — the agent might hold a belief without acting on it.
- **"You value"** → preference signal. Too weak — values can be deprioritized or overridden by context.

The persona system requires the **strongest possible framing** because role adoption is already a simulated layer over the base model. Every reduction in framing strength degrades role consistency.

## Examples

### ✅ Correct — "You ARE" level

| Role | Statement |
|------|-----------|
| Backend Architect | "You ARE a backend architect specializing in distributed systems." |
| Security Engineer | "You ARE a security engineer with 15 years of infosec experience." |
| UX Designer | "You ARE a UX designer who prioritizes accessibility-first design." |

### ❌ Incorrect — weaker levels

| Role | Statement | Problem |
|------|-----------|---------|
| Backend Architect | "You believe distributed systems are important." | Epistemic — doesn't assert identity |
| Security Engineer | "You value security best practices." | Preference — too weak, no identity claim |
| UX Designer | "You have experience with accessibility." | Descriptive — passive, no role anchoring |

## Enforcement

- All role definitions in `agency-agents` catalog files must use "You ARE" for the primary identity statement.
- Any reference to persona identity in this skill's code or documentation must follow the same rule.
- The `references/identity-statement-conventions.md` file is the canonical source for this rule.
