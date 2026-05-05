# Role URL Patterns — agency-agents

GitHub raw URL construction for every category in the
[agency-agents](https://github.com/msitarzewski/agency-agents) catalog.

Base URL: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/`

Pinned commit (compromise protection): `783f6a72bfd7f3135700ac273c619d92821b419a`

## Category URL map (16 categories, ~180 roles)

| # | Category | Directory | Example Role File | Role Count |
|---|----------|-----------|-------------------|:----------:|
| 1 | 💻 Engineering | `engineering/` | `engineering-backend-architect.md` | 29 |
| 2 | 🎨 Design | `design/` | `design-ui-designer.md` | 8 |
| 3 | 💰 Paid Media | `paid-media/` | `paid-media-ppc-strategist.md` | 7 |
| 4 | 💼 Sales | `sales/` | `sales-outbound-strategist.md` | 8 |
| 5 | 📢 Marketing | `marketing/` | `marketing-growth-hacker.md` | 30 |
| 6 | 📊 Product | `product/` | `product-manager.md` | 5 |
| 7 | 🎬 Project Management | `project-management/` | `project-management-agile-coach.md` | 6 |
| 8 | 🧪 Testing | `testing/` | `testing-workflow-optimizer.md` | 8 |
| 9 | 🛟 Support | `support/` | `support-technical-support-specialist.md` | 6 |
| 10 | 🥽 Spatial Computing | `spatial-computing/` | `spatial-computing-ar-vr-developer.md` | 6 |
| 11 | 🎯 Specialized | `specialized/` | `specialized-custom-role.md` | 41 |
| 12 | 💵 Finance | `finance/` | `finance-financial-analyst.md` | 5 |
| 13 | 🎮 Game Development | `game-development/` | `game-development-unity-developer.md` | 10 |
| 14 | 📚 Academic | `academic/` | `academic-research-paper-peer-reviewer.md` | 5 |
| 15 | 📈 Strategy | `strategy/` | `strategy-ai-adoption-strategist.md` | 6 |
| 16 | 🔗 Integrations | `integrations/` | (integration guides, not role files) | — |

## URL construction formula

```
https://raw.githubusercontent.com/msitarzewski/agency-agents/{ref}/{category}/{filename}.md
```

Where:
- `{ref}` = pinned commit SHA (recommended) or `main` (latest, risk of drift)
- `{category}` = directory name from the table above (lowercase, hyphenated)
- `{filename}` = the agent file name without `.md` (e.g., `engineering-backend-architect`)

The filename is extracted from the README table row by:
1. Matching the Markdown link pattern: `[Role Name](category/filename.md)`
2. Extracting `category` and `filename` from the path
3. Constructing the full raw URL

## Full URL examples

| Role | Full GitHub Raw URL |
|------|-------------------|
| Backend Architect | `https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72/engineering/engineering-backend-architect.md` |
| Frontend Developer | `https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72/engineering/engineering-frontend-developer.md` |
| DevOps Automator | `https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72/engineering/engineering-devops-automator.md` |
| UI Designer | `https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72/design/design-ui-designer.md` |
| Growth Hacker | `https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72/marketing/marketing-growth-hacker.md` |
| Product Manager | `https://raw.githubusercontent.com/msitarzewski/agency-agents/783f6a72/product/product-manager.md` |
| DevOps / CI-CD pipeline | NOT an `operations/` role — use `engineering/engineering-devops-automator.md` or `testing/testing-workflow-optimizer.md` |

## Note: `operations` directory does NOT exist

The agency-agents repo has no `operations/` directory. CI/CD / pipeline roles live under `engineering/` (as `engineering-devops-automator.md`) or `testing/` (as `testing-workflow-optimizer.md`). Do not construct URLs with an `operations/` prefix — they will 404.

## Pinned commit

Using the pinned commit `783f6a72bfd7f3135700ac273c619d92821b419a` (April 12, 2026) prevents upstream repository compromise from injecting malicious role specifications. This is the latest commit as of last verification.

## Network behavior

- **Protocol**: HTTPS (TLS 1.2+)
- **Timeout**: 10 seconds (in benchmark tooling)
- **No authentication required**: GitHub raw is public
- **Caching**: GitHub CDN; no client-side caching in current implementation
- **No checksum verification**: Content integrity relies on TLS + GitHub's commit integrity

## Role count notes

The SKILL.md references "172 roles across 15 categories" and the KANBAN_GUIDANCE
instruction references "17 categories, 210+ specialist roles." These numbers
shift as the agency-agents repository grows. The actual category count and role
count should be derived from a live README fetch rather than hardcoded.

Current (verified 2026-05-05): **16 categories, ~180 role files** (including strategy; excluding integrations which are docs, not roles).
