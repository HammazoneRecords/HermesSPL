# TCP Route Index

**Agent:** TCP
**Reports to:** H1 (peer of Plato)
**Created/Updated:** 2026-09-01T13:40:00-0500
**Root:** `D:\MW_CENTRAL\agent_space\agent-TCP_H1`

---

## Purpose

TCP's local route index. TCP initializes from these TCP-prefixed files only — no global `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `USER.md`, or `MEMORY.md` pulls.

## Scope Rule

TCP reads **TCP-prefixed scope surfaces** in this folder. As a **peer of Plato**, TCP may also *view* (read-only) Plato's governance surfaces to record governance decisions in the timeline. It never writes outside `agent_space`.

Forbidden automatic context pulls: `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, Hermes `SOUL.md`/`USER.md`/`MEMORY.md`, `.env`, `auth.json`, API keys/credentials.

## TCP-owned Surfaces

| Surface | Path | Role |
|---|---|---|
| Identity | `TCP_SOUL.md` | TCP identity and posture (peer of Plato) |
| User contract | `TCP_USER.md` | Who TCP serves + continuity rule |
| Working memory | `TCP_MEMORY.md` | Stable TCP-local facts |
| Scope rules | `TCP_SCOPE.md` | What TCP may read/write/report |
| Reporting contract | `TCP_REPORTS_TO_H1.md` | How TCP returns findings |
| Config | `TCP_config.yaml` | Non-secret agent config |
| State map | `TCP_state.md` | State model + execution blockers |
| **Spec** | `TCP_SPEC.md` | The formalization protocol (timeline schema, stream taxonomy, continuity, topic tags, model handoff) |
| **Topic tags** | `TCP_TOPIC_TAGS.md` | Tag taxonomy for linking related concepts |
| T1 | `TCP_T1_Intention/` | Intention/planning side |
| T2 | `TCP_T2_Execution/` | Execution/output side |
| Drayl | `TCP_Drayl/` | The Chrono-Drayl timeline nodes live here |
| Skills | `TCP_skills/` | TCP procedural notes |
| Plugins | `TCP_plugins/` | TCP plugin proposals (not live) |
| Cron | `TCP_cron/` | TCP schedule proposals (not live) |
| Logs | `TCP_logs/` | TCP run/report logs |
| Cache | `TCP_cache/` | Temporary artifacts |
| Shadow | `TCP_Shadow_Drayl0/` | TCP private reflection for H1/Plato review |
| Alignment | `TCP_alignment_playground/` | Draft alignment work |

## Initialization + First Audit

| Artifact | Path | Role |
|---|---|---|
| Init packet | `TCP_INIT_PACKET_FOR_H1.md` | Compact init packet for H1 |
| First audit task | `TCP_FIRST_SCOPE_AUDIT_TASK.md` | Bounded scope-audit task |
