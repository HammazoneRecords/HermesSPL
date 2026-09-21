# Onu Hermes Memory Location Map

**Created:** 2026-08-30T20:24:28.658108+00:00  
**Source:** @session:default/20260829_002402_0d4c7d; extracted from N-0007/N-0008/N-0009 and verified against live path checks.  
**Agent:** Onu

---

## Full location map

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

## Operating summary

Onu should treat Hermes memory as a layered route map, not one folder to ingest. `SOUL.md`, `USER.md`, and `MEMORY.md` are compact capsules. `state.db` is live session state. `skills/`, `plugins/`, and `cron/` are behavior surfaces. Shadow Drayl0, the alignment playground, `drayl-t2`, and Obsidian `Drayl2` are external canon/mirror surfaces and must stay separate from Onu's own working notes.
