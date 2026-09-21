# MATRIX — Workspace Intelligence Hub

Version: v2.0.0
Updated: 2026-09-15

This folder is the **single source of truth** for workspace structure, agent naming,
document dependencies, schema enforcement, and readiness tracking.

---

## Files in MATRIX/

| File | Purpose |
|---|---|
| `naming-authority.json` | **Load first.** Canonical name → all 3 layer paths |
| `naming-authority.md` | Human-readable name map (all variants) |
| `matrix_loader.py` | Python import: `resolve_name()`, `get_path()`, `get_schema()` |
| `schema-registry.json` | What schema validates what files |
| `document-dependency-matrix.md` | Canonical docs + update groups + charge levels |
| `document-dependency-matrix.json` | Same, machine-readable |
| `reverse-dependency-index.json` | Given any file → what depends on it (1,139 entries) |
| `agent-readiness.json` | Readiness score per agent (0-100%) |
| `fw-file-mapping.json` | Which files each FW entry touches (277 mapped) |
| `agent-skill-usage-matrix.json` | Agent × skill × usage (bungee cord) |
| `component-direction-map.md` | Folder map with direction per component |

---

## Quick Start for Scripts

```python
from matrix_loader import resolve_name, get_path, get_schema, get_agent_schemas

# Any name variant → canonical
canonical = resolve_name("jhanosbara")           # → "JHANOS_BARA"
canonical = resolve_name("AGENT_JHANOS_BARA_TRIS") # → "JHANOS_BARA"

# Get exact filesystem path
profile = get_path("jhanosbara", "profile")      # → ~/.hermes/profiles/jhanosbara
tri = get_path("JHANOS_BARA", "tri")             # → ANDROMALIUS/.../JHANOS_BARA
aspace = get_path("bara", "agent_space")         # → ANDROMALIUS/.../AGENT_JHANOS_BARA_TRIS

# Schema enforcement
schemas = get_agent_schemas("jhanos_gate")       # → ["agent_soul", "agent_scope", ...]
```

---

## Name Resolution

All agents have 3 name variants (one per layer). The naming authority maps them all:

- **Canonical:** `JHANOS_BARA` (UPPER_SNAKE_CASE — used in scripts/matrices)
- **Agent-space:** `AGENT_JHANOS_BARA_TRIS/` (prefix + canonical + suffix)
- **TRIS:** `JHANOS_BARA/` (same as canonical)
- **Profile:** `jhanosbara/` (lowercase, no underscores — Hermes convention)

22 agents total: 10 core, 10 jhanos_gate, 2 scout.

---

## Schema Enforcement

12 schemas defined covering all file types:

- **Agent files:** agent_soul, agent_scope, agent_memory, agent_config
- **TRIS files:** tri_identity, tri_scope, tri_policy
- **Gate files:** gate_skill
- **Plan files:** working_plan, pev_plan
- **Registry files:** fw_entry, matrix_json

Each agent category has a required schema set:
- **jhanos_gate:** 7 schemas (includes gate_skill)
- **core:** 6 schemas
- **scout:** 6 schemas

---

## Update Protocol

When workspace framework changes:

1. **Check reverse index** — what depends on the file you're changing?
2. **Check update groups** — which files must change together?
3. **Check charge level** — CRITICAL changes need PEV plan
4. **Update FW registry** — close or modify related FW entries
5. **Update naming-authority.json** — if agents/paths changed
6. **Update this README** — keep docs current

---

## Version History

- v1.0.0 — Initial matrix (folder map + agent-skill-usage)
- v1.1.0 — Added: document dependencies, reverse index, agent readiness, FW mapping
- v2.0.0 — Added: naming authority, schema registry, matrix loader, name resolution
