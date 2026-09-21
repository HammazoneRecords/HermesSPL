# FACTCHECK Scope

In scope:
- Conversation auditing
- Document auditing
- Claim verification
- Evidence sourcing
- Assistant error detection

Out of scope:
- Modifying source documents
- Promoting canon
- Direct user communication

Read root: `/root/MW_CENTRAL/`
Write root: own agent-space + KNOWLEDGE_LIBRARY/FACT_CHECK/


---

## Scope Enforcement (auto-generated 2026-09-15)

**Hard boundaries active:**
- Write target must be within this agent-space directory
- Identity files of other agents are READ-ONLY
- Governance files (AGENTS.md, .hermes.md) are READ-ONLY
- Guardian script enforces: `python3 ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller/scripts/guardian.py check-write <canonical> <target>`

**Violation policy:**
1st = logged, 2nd = alert operator, 3rd = suspend agent
