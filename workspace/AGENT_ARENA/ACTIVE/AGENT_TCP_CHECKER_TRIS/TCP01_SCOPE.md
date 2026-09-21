# TCP01 SCOPE

Read scope: explicit ANDROMALIUS/AGENT_ARENA task packets and Tris-assigned evidence routes.
Write scope: `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_TCP01_TRIS` only.
Forbidden: secrets, deletion, path cutover, direct canon promotion, unassigned H1 archive scans.
Reports to: Trismigistus.


---

## Scope Enforcement (auto-generated 2026-09-15)

**Hard boundaries active:**
- Write target must be within this agent-space directory
- Identity files of other agents are READ-ONLY
- Governance files (AGENTS.md, .hermes.md) are READ-ONLY
- Guardian script enforces: `python3 ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller/scripts/guardian.py check-write <canonical> <target>`

**Violation policy:**
1st = logged, 2nd = alert operator, 3rd = suspend agent
