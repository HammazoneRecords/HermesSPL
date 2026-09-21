# Onu First Scope Audit Task

**Agent:** Onu  
**Assigned by:** Plato  
**Created:** 2026-08-30T22:38:02.944164+00:00  
**Output target:** `Onu_T2_Execution/Onu_first_scope_audit.md`

---

## Task

Inventory only the `D:\MW_CENTRAL\agent_space\agent-ONU_Plato` folder and report:

1. Which Onu-owned core files exist.
2. Which Onu-owned workspace folders exist.
3. Whether any forbidden context files exist in the Onu folder.
4. Whether any secret-bearing files exist in the Onu folder.
5. Whether all found files use the `Onu_` prefix, excluding the folder name itself.
6. Any naming, scope, or route inconsistencies.

---

## Forbidden Context Files to Check

- `.hermes.md`
- `AGENTS.md`
- `CLAUDE.md`
- `SOUL.md`
- `USER.md`
- `MEMORY.md`
- `.env`
- `auth.json`

---

## Report Format

Use the reporting lanes from `Onu_REPORTS_TO_Plato.md`:

1. **SOURCE / VERIFIED**
2. **GENERATED / RECOMMENDATION**
3. **UNCERTAINTY / BLOCKERS**

---

## Guardrail

Do not read outside `agent-ONU_Plato` for this audit. Do not edit anything except the assigned output report.
