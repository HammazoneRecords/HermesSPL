# Naming Authority — Canonical Name Resolution

Source: `MATRIX/namingauthority.json` (machine-readable)
Loader: `MATRIX/matrix_loader.py` (Python import)

---

## The Problem This Solves

Agent names appear in 3 different formats across layers:

- Agent-space: `AGENT_JHANOS_BARA_TRIS/` (prefix + UPPER_SNAKE + suffix)
- TRIS component: `JHANOS_BARA/` (UPPER_SNAKE)
- Hermes profile: `jhanosbara/` (lowercase, no underscores)

Scripts kept guessing. No more.

---

## Resolution Rules

1. Strip `AGENT_` prefix and `_TRIS` suffix from agent-space dirs → canonical
2. Profile dirs: remove underscores/dashes, lowercase, compare to canonical
3. TRIS dirs: match agent-space exactly (UPPER_SNAKE_CASE)
4. Always look up in `naming-authority.json` first

---

## Usage

```python
from matrix_loader import resolve_name, get_path, get_schema

canonical = resolve_name("jhanosbara")        # → "JHANOS_BARA"
canonical = resolve_name("AGENT_JHANOS_BARA_TRIS")  # → "JHANOS_BARA"
canonical = resolve_name("JHANOS_BARA")       # → "JHANOS_BARA"

profile = get_path("jhanosbara", "profile")   # → ~/.hermes/profiles/jhanosbara
tri = get_path("JHANOS_BARA", "tri")          # → ANDROMALIUS/.../JHANOS_BARA
aspace = get_path("bara", "agent_space")      # → ANDROMALIUS/.../AGENT_JHANOS_BARA_TRIS

schemas = get_agent_schemas("jhanos_gate")    # → ["agent_soul", "agent_scope", ...]
```

---

## Full Name Map

### Core Agents

| Canonical | Agent-Space Dir | TRIS Dir | Profile Dir |
|---|---|---|---|
| ONU | AGENT_ONU_TRIS | ONU | onu |
| TCP | AGENT_TCP_TRIS | TCP | tcp |
| TCP_CHECKER | AGENT_TCP_CHECKER_TRIS | TCP_CHECKER | tcpchecker |
| MEMORY_CURATOR | (none — TRIS direct) | MEMORY_CURATOR | memorycurator |
| APPCTX | AGENT_APPCTX_TRIS | APPCTX | appctx |
| FACTCHECK | AGENT_FACTCHECK_TRIS | FACTCHECK | factcheck |
| GODSEYE | AGENT_GODSEYE_TRIS | GODSEYE | godseye |
| SOLOBILITY | AGENT_SOLOBILITY_TRIS | SOLOBILITY | solobility |
| SOLOBIC_SCRIBE | AGENT_SOLOBIC_SCRIBE_TRIS | SOLOBIC_SCRIBE | solobicscribe |
| HERMESSPL | AGENT_HERMESSPL_TRIS | HERMESSPL | hermesspl |

### Jhanos Gate Agents

| Canonical | Agent-Space Dir | TRIS Dir | Profile Dir |
|---|---|---|---|
| JHANOS_BARA | AGENT_JHANOS_BARA_TRIS | JHANOS_BARA | jhanosbara |
| JHANOS_KHEM | AGENT_JHANOS_KHEM_TRIS | JHANOS_KHEM | jhanoskhem |
| JHANOS_LOMI | AGENT_JHANOS_LOMI_TRIS | JHANOS_LOMI | jhanoslomi |
| JHANOS_ORON | AGENT_JHANOS_ORON_TRIS | JHANOS_ORON | jhanosoron |
| JHANOS_SYLA | AGENT_JHANOS_SYLA_TRIS | JHANOS_SYLA | jhanossyla |
| JHANOS_TARA | AGENT_JHANOS_TARA_TRIS | JHANOS_TARA | jhanostara |
| JHANOS_VORAK | AGENT_JHANOS_VORAK_TRIS | JHANOS_VORAK | jhanosvorak |
| JHANOS_ZAYN | AGENT_JHANOS_ZAYN_TRIS | JHANOS_ZAYN | jhanoszayn |
| JHANOS_ASSESSOR | AGENT_JHANOS_ASSESSOR_TRIS | JHANOS_ASSESSOR | jhanosassessor |
| JHANOS_ECHO | AGENT_JHANOS_ECHO_TRIS | JHANOS_ECHO | jhanosecho |

### Scout Agents

| Canonical | Agent-Space Dir | TRIS Dir | Profile Dir |
|---|---|---|---|
| CHAT_EXCAVATION_SCOUT | AGENT_CHAT_EXCAVATION_SCOUT_TRIS | CHAT_EXCAVATION_SCOUT | chatexcavationscout |
| TEMPLATE_EVOLUTION_SCOUT | AGENT_TEMPLATE_EVOLUTION_SCOUT_TRIS | TEMPLATE_EVOLUTION_SCOUT | templateevolutionscout |

---

## Schema Enforcement

What validates what:

| File Pattern | Schema | Required Fields |
|---|---|---|
| `*SOUL*.md` | agent_soul | identity_block, purpose, posture |
| `*SCOPE*.md` | agent_scope | allowed_reads, allowed_writes, reports_to |
| `*MEMORY*.md` | agent_memory | state_format, retrieval_rules |
| `config.yaml` | agent_config | provider, model |
| `identity.md` (TRIS) | tri_identity | core_function, reports_to, category |
| `scope.md` (TRIS) | tri_scope | boundaries, permissions |
| `gate-*-SKILL.md` | gate_skill | identity, red_team, blue_team |
| `2026-*.md` (plans) | working_plan | goal, acceptance_criteria, distance |
| `*-pev-plan.md` | pev_plan | objective, steps, verification, rollback |
| `*.json` (MATRIX) | matrix_json | _meta |

### Per-Category Requirements

**jhanos_gate** needs: agent_soul + agent_scope + agent_memory + agent_config + tri_identity + tri_scope + gate_skill
**core** needs: agent_soul + agent_scope + agent_memory + agent_config + tri_identity + tri_scope
**scout** needs: agent_soul + agent_scope + agent_memory + agent_config + tri_identity + tri_scope
