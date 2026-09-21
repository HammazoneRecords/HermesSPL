# TCP First Scope Audit Task

**Agent:** TCP
**Reports to:** H1 (peer of Plato)
**Status:** NOT YET RUN — gated on model-selection unblock

---

## Objective

Prove TCP can audit only its own scope: read-only inventory of the TCP scaffold, confirm the forbidden-file boundary, and confirm no scan of drayl/obsidian occurred.

## Steps (read-only)

1. List all files in `agent-TCP_H1` (recursive).
2. Confirm every file is `TCP_`-prefixed or a standard scaffold surface.
3. Confirm no forbidden files exist: `.env`, `auth.json`, API keys, credentials, or copies of Hermes `SOUL.md`/`USER.md`/`MEMORY.md`.
4. Confirm no drayl/obsidian content was read (no `drayl-t2`, `Drayl2`, Shadow Drayl0 paths accessed).
5. Confirm no writes occurred outside `agent_space`.
6. Report: file inventory count + boundary violations (expected: none).

## Expected output

`TCP_T2_Execution/TCP_first_scope_audit.md`

## Gate

Do not run until `TCP_state.md` blockers 1 and 2 are cleared.
