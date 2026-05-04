# Role URL Patterns — agency-agents

GitHub raw URL construction for every category in the
[agency-agents](https://github.com/msitarzewski/agency-agents) catalog.

Base URL: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/`

## Category URL map (14 divisions)

| # | Category (emoji) | Directory | Example Role File |
|---|------------------|-----------|-------------------|
| 1 | 💻 Engineering | `engineering/` | `engineering/engineering-backend-architect.md` |
| 2 | 🎨 Design | `design/` | `design/design-ui-designer.md` |
| 3 | 💰 Paid Media | `paid-media/` | `paid-media/paid-media-ppc-strategist.md` |
| 4 | 💼 Sales | `sales/` | `sales/sales-outbound-strategist.md` |
| 5 | 📢 Marketing | `marketing/` | `marketing/marketing-growth-hacker.md` |
| 6 | 📊 Product | `product/` | `product/product-sprint-prioritizer.md` |
| 7 | 🎬 Project Management | `project-management/` | `project-management/` |
| 8 | 🧪 Testing | `testing/` | `testing/` |
| 9 | 🛟 Support | `support/` | `support/` |
| 10 | 🥽 Spatial Computing | `spatial-computing/` | `spatial-computing/` |
| 11 | 🎯 Specialized | `specialized/` | `specialized/` |
| 12 | 💵 Finance | `finance/` | `finance/` |
| 13 | 🎮 Game Development | `game-development/` | `game-development/unity/` |
| 14 | 📚 Academic | `academic/` | `academic/` |

## URL construction formula

```
https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md
```

Where:
- `{category}` = directory name from the table above (lowercase, hyphenated)
- `{filename}` = the agent file name without `.md` (e.g., `engineering-backend-architect`)

The filename is extracted from the README table row by:
1. Matching the Markdown link pattern: `[Role Name](category/filename.md)`
2. Extracting `category` and `filename` from the path
3. Constructing the full raw URL

## Full URL examples

| Role | Full GitHub Raw URL |
|------|-------------------|
| Backend Architect | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-backend-architect.md` |
| Frontend Developer | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-frontend-developer.md` |
| Security Engineer | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-security-engineer.md` |
| UI Designer | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/design/design-ui-designer.md` |
| Growth Hacker | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/marketing/marketing-growth-hacker.md` |
| Database Optimizer | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-database-optimizer.md` |
| Product Manager | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/product/` |
| Financial Analyst | `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/finance/` |

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
