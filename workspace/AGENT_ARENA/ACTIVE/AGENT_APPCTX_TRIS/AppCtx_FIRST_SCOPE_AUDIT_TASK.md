# AppCtx First Scope Audit Task

**Agent:** AppCtx
**Assigned by:** Onu
**Created:** 2026-09-02
**Output target:** `AppCtx_T2_Execution/AppCtx_first_scope_audit.md`

---

## Task

Inventory only the `D:\MW_CENTRAL\agent_space\agent-AppCtx_Onu` folder and report:

1. Which AppCtx-owned core files exist.
2. Which AppCtx-owned workspace folders exist.
3. Whether any forbidden context files exist in the AppCtx folder.
4. Whether any secret-bearing files exist in the AppCtx folder.
5. Whether all found files use the `AppCtx_` prefix, excluding the folder name itself.
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

Use the reporting lanes from `AppCtx_REPORTS_TO_Onu.md`:

1. **SOURCE / VERIFIED**
2. **GENERATED / RECOMMENDATION**
3. **UNCERTAINTY / BLOCKERS**

---

## Guardrail

Do not read outside `agent-AppCtx_Onu` for this audit. Do not edit anything
except the assigned output report.
