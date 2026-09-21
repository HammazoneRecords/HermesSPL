# Hermes Memory Locations — Thread Extract for Onu

**Created:** 2026-08-30T20:24:28.658108+00:00  
**Source session:** @session:default/20260829_002402_0d4c7d  
**Source thread:** Messages around 2215–2301, especially 2296, plus N-0007/N-0008/N-0009 files created from that session.  
**Purpose:** Extract the prior work that identified Hermes memory/storage locations, then provide Onu-ready versions in `D:\MW_CENTRAL\agent_space`.

---

## 1. Located thread

The thread was found in session @session:default/20260829_002402_0d4c7d, titled **“Assess logic behind unexpected directories after PR”**. The relevant section is the later Lane A / HermesSPL memory architecture work around message ids **2215–2301**, with the clearest memory-location payloads in:

- `N-0007_hermes-mesh-operationul-procedures.md`
- `N-0008_obsidian-integration-spec.md`
- `N-0009_hermes-spl-product-architecture.md`
- `HERMES_DOCS_GENERATED.md`

The session extracted Hermes memory into a **7-layer model** and tied it to Lane A, Obsidian, Shadow Drayl, and `agent_space`.

---

## 2. Core finding from the thread

Hermes memory is not one file. It is a layered system:

1. `SOUL.md` — identity/personulity
2. `USER.md` — user profile capsule
3. `MEMORY.md` — agent notes capsule
4. `.hermes.md` / `AGENTS.md` / `CLAUDE.md` — project context and folder rules
5. `state.db` / `sessions/` — sessions, messages, tool calls, FTS5, delegations, routing/transcripts
6. `skills/`, `plugins/`, `desktop-plugins/`, `cron/` — durable capabilities and scheduled behavior
7. Shadow Drayl0 / playground specs / Drayl2 / drayl-t2 — external canon, mirror, and Lane A evidence routes

---

## 3. Memory-location table

| Layer | Location | Role | Onu handling |
|---:|---|---|---|
| 1 | `C:\Users\Owner\AppData\Local\hermes\SOUL.md` | Hermes identity/personulity slot #1 | Reference only; do not bulk-copy as canon |
| 2 | `C:\Users\Owner\AppData\Local\hermes\memories\USER.md` | User profile frozen snapshot | Capsule reference only |
| 3 | `C:\Users\Owner\AppData\Local\hermes\memories\MEMORY.md` | Agent notes frozen snapshot | Capsule reference only |
| 4 | `.hermes.md` / `AGENTS.md` / `CLAUDE.md` under active cwd/project | Project rules and local governance | Load from current working route; never globalize blindly |
| 5 | `C:\Users\Owner\AppData\Local\hermes\state.db` | Sessions, messages, FTS5 search, delegations, Lane A summaries | Query via tools/CLI; do not edit directly |
| 5b | `C:\Users\Owner\AppData\Local\hermes\sessions\` | Gateway routing, request dumps, jsonl transcripts | Evidence store; read-only unless session tools manage it |
| 6a | `C:\Users\Owner\AppData\Local\hermes\skills\` | Durable procedures | Onu may get skill maps, not raw uncontrolled copies |
| 6b | `C:\Users\Owner\AppData\Local\hermes\plugins\` | Runtime extension code | Code/control surface; version before editing |
| 6c | `C:\Users\Owner\AppData\Local\hermes\desktop-plugins\` | Desktop UI extensions | Code/control surface; version before editing |
| 6d | `C:\Users\Owner\AppData\Local\hermes\cron\` | Scheduled jobs | Governance-sensitive; list before changes |
| Ops | `C:\Users\Owner\AppData\Local\hermes\config.yaml` | Settings, active providers/models/toolsets | Settings, not memory; use Hermes config commands |
| Ops | `C:\Users\Owner\AppData\Local\hermes\auth.json` and `.env` | OAuth/API credentials | Secret-bearing; never copy to agent_space |
| Ops | `C:\Users\Owner\AppData\Local\hermes\logs\` | Runtime evidence/errors | Evidence supplement, not canon |
| Ops | `C:\Users\Owner\AppData\Local\hermes\cache\` | Tool/model/cache/spillover | Temporary evidence; not canon |
| Profile pattern | `C:\Users\Owner\AppData\Local\hermes\profiles\<name>\` | Per-profile isolated Hermes home | Same layout as default when profiles exist |
| Canon | `D:\MW_CENTRAL\Shadow Drayl0\Plato-V0.0625\` | Plato structured notes/index/specs | Source/canon reference for Onu |
| Canon | `D:\MW_CENTRAL\playground\2026-08-hermes-spl-alignment\` | Lane A plans/specs/ledgers/reports | Source/canon reference for Onu |
| Canon | `D:\MW_CENTRAL\drayl-t2\` | Current Drayl canonical workspace truth | Do not mirror wholesale |
| Mirror | `C:\Users\Owner\Videos\Drayl2\` | Obsidian mobile-linked user mirror | User-facing mirror; not automatic source ingestion |
| Onu root | `D:\MW_CENTRAL\agent_space\` | Agent-space staging/memory root under review | New Onu-prefixed docs live here |


---

## 4. Thread-derived rules for Onu

- `agent_space` is **under evaluation**, not automatically canonical.
- Onu files must be prefixed `Onu_`.
- Do not copy secrets (`auth.json`, `.env`) into agent space.
- Do not treat generated summaries as User H1 source.
- Keep User H1, Plato notes, Hermes runtime memory, and Onu working memory distinct.
- Prefer route/index/reference documents over full mirror copies.
- Version scripts before editing them.
- Read state via tools (`session_search`, Hermes CLI, SQLite inspection), not direct mutation.

---

## 5. Onu files created from this extract

- `Onu_Hermes_Memory_Locations_Thread_Extract.md`
- `Onu_Hermes_Memory_Location_Map.md`
- `Onu_SOUL_md_Surface.md`
- `Onu_USER_md_Surface.md`
- `Onu_MEMORY_md_Surface.md`
- `Onu_Project_Context_Surface.md`
- `Onu_State_DB_and_Sessions_Surface.md`
- `Onu_Durable_Capabilities_Surface.md`
- `Onu_External_Canon_and_Mirrors_Surface.md`
- `Onu_Agent_Space_Operating_Rules.md`
