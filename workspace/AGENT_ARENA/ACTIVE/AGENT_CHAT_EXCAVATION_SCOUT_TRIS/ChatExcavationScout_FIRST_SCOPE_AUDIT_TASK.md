# ChatExcavationScout FIRST SCOPE AUDIT TASK

## Task

Verify this scaffold is bounded and safe before activation.

## Checks

- Core files exist.
- All core files use ChatExcavationScout prefix.
- No forbidden files exist in root: AGENTS.md, CLAUDE.md, .hermes.md, .env, auth.json.
- Write scope is explicit.
- Report-to relation is explicit.
- Task status file exists.

## Required output

Write audit result to:

```text
ChatExcavationScout_T2_Execution/ChatExcavationScout_first_scope_audit.md
```


---

## Scope Enforcement (auto-generated 2026-09-15)

**Hard boundaries active:**
- Write target must be within this agent-space directory
- Identity files of other agents are READ-ONLY
- Governance files (AGENTS.md, .hermes.md) are READ-ONLY
- Guardian script enforces: `python3 ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller/scripts/guardian.py check-write <canonical> <target>`

**Violation policy:**
1st = logged, 2nd = alert operator, 3rd = suspend agent
