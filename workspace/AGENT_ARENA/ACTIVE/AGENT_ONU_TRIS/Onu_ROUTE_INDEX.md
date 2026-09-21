# Onu Route Index

**Agent:** ONU  
**Reports to:** Plato  
**Created/Updated:** 2026-08-30T21:58:00Z  
**Root:** `D:\MW_CENTRAL\agent_space\agent-ONU_Plato`

---

## Purpose

This is Onu's local route index. Plato initializes Onu's scope from these Onu-prefixed files, the same way Hermes/Plato may use identity, user, memory, and project context surfaces — but without letting Onu pull Plato's global `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `USER.md`, or `MEMORY.md` directly.

---

## Scope Rule

Onu reads **only Onu-prefixed scope surfaces** in this folder unless Plato explicitly passes additional context.

Forbidden automatic context pulls:

- `.hermes.md`
- `AGENTS.md`
- `CLAUDE.md`
- Hermes `SOUL.md`
- Hermes `USER.md`
- Hermes `MEMORY.md`
- Hermes `.env`
- Hermes `auth.json`

---

## Onu-owned Surfaces

| Surface | Path | Role |
|---|---|---|
| Identity | `Onu_SOUL.md` | Onu identity and posture |
| User/Plato contract | `Onu_USER.md` | Who Onu serves and how to interpret Plato directives |
| Working memory | `Onu_MEMORY.md` | Stable Onu-local facts only |
| Scope rules | `Onu_SCOPE.md` | What Onu may read/write/report |
| Reporting contract | `Onu_REPORTS_TO_Plato.md` | How Onu returns findings to Plato |
| Config | `Onu_config.yaml` | Non-secret agent config |
| State map | `Onu_state.md` | State model, not a live DB |
| T1 | `Onu_T1_Intention/` | Intention/planning side |
| T2 | `Onu_T2_Execution/` | Execution/output side |
| Sessions | `Onu_sessions/` | Onu session summaries/transcripts if generated |
| Skills | `Onu_skills/` | Onu procedural notes/templates |
| Plugins | `Onu_plugins/` | Onu plugin proposals, not live Hermes plugins |
| Cron | `Onu_cron/` | Onu schedule proposals, not live cron jobs |
| Logs | `Onu_logs/` | Onu run/report logs |
| Cache | `Onu_cache/` | Temporary Onu artifacts |
| Drayl | `Onu_Drayl/` | Onu-local Drayl conceptual workspace |
| Obsidian mirror | `Onu_Obsidian_Drayl/` | Onu-specific mirror/staging notes |
| Shadow | `Onu_Shadow_Drayl0/` | Onu private/reflection notes for Plato review |
| Alignment | `Onu_alignment_playground/` | Onu experiments and draft alignment work |

---

## Initialization + First Audit Artifacts

| Artifact | Path | Role |
|---|---|---|
| Init packet | `Onu_INIT_PACKET_FOR_PLATO.md` | Single compact file Plato can pass to initialize Onu without exposing global Plato/Hermes context |
| First audit task | `Onu_FIRST_SCOPE_AUDIT_TASK.md` | Bounded task proving Onu can audit only its own scope |
| First audit result | `Onu_T2_Execution/Onu_first_scope_audit.md` | Verified read-only inventory of Onu scaffold and forbidden-file boundary |
