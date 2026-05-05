# External System Integration Review (Persona-driven)

## When to use

A user points you at an external open-source project and asks whether it
could improve a system you maintain. The answer isn't obvious — you need
to explore the project's architecture, compare it against your system's
design, and produce a feasibility analysis.

## Methodology

1. **Load the persona skill** — `skill_view(name='persona')`
2. **Adopt a fitting role** for system architecture analysis
   - 🏗️ Backend Architect — for memory systems, databases, backends
   - 🏛️ Software Architect — for overall system design comparison
3. **Explore the external project** via browser + `curl`:
   - README: what problem does it solve, benchmark claims, install method
   - Key source files: architecture, API surface, dependencies
   - Docs site: concepts, guides, reference
4. **Compare against your system's current design**:
   - Create a side-by-side comparison table
   - Identify gaps the external project could fill
   - Note integration costs (dependencies, licensing, API compatibility)
5. **Produce an integration feasibility report**:
   - Concrete wins (what specifically improves)
   - Caveats (what doesn't map well)
   - Integration approach (MCP server, plugin, backend swap, etc.)
   - Effort estimate (pip install, config change, code changes)

## Example: MemPalace → Hermes Agent analysis

| Dimension | Current Hermes | MemPalace | Improvement |
|-----------|---------------|-----------|-------------|
| Memory structure | Flat key-value + FTS5 | Palace hierarchy (wing/room/drawer) | Organization + scoped search |
| Retrieval | FTS5 string matching | Vector + keyword hybrid (96.6% R@5) | Semantic search, no LLM cost |
| Knowledge graph | None | SQLite temporal entity graph | Entity tracking with time validity |
| Worker memory | None (per-task isolation) | Wing per agent + diary | Cross-session context |
| Integration | Built-in | MCP server (29 tools) | Native MCP client wire-up |
| Install | Bundled | `pip install mempalace` | One command |

**Verdict:** Promising for Hermes Agent's next memory system iteration.
