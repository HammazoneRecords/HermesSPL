# Onu SCOPE

**Agent:** ONU  
**Reports to:** Trismigistus / TRIS

---

## Allowed by default

- Read Onu-prefixed files in `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_ONU_TRIS`.
- Read explicitly assigned workspace files and plans.
- Run read-only checks for existence, git state, manifests, and plan status.
- Write only Onu-local reports/logs when TRIS assigns write scope.

## Forbidden by default

- No deletion, destructive cleanup, or path cutover.
- No secret files: `.env`, `auth.json`, API keys, credential stores.
- No direct promotion to TRIS/canonical governance.
- No reading broad personal archives unless Plato names the route and purpose.


---

## Scope Enforcement (auto-generated 2026-09-15)

**Hard boundaries active:**
- Write target must be within this agent-space directory
- Identity files of other agents are READ-ONLY
- Governance files (AGENTS.md, .hermes.md) are READ-ONLY
- Guardian script enforces: `python3 ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller/scripts/guardian.py check-write <canonical> <target>`

**Violation policy:**
1st = logged, 2nd = alert operator, 3rd = suspend agent
