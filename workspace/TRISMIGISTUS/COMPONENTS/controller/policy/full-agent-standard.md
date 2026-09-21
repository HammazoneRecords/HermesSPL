# Full Agent Standard

Version: v1.0.0
Created: 2026-09-15
Status: DRAFT — awaiting approval

---

## Definition

A **full agent** is an autonomous identity that can be activated, tasked, and verified without manual scaffolding. It has three layers:

1. **Hermes Profile** — runtime config (model, provider, routing)
2. **TRIS Component** — identity, scope, policy, routing rules
3. **Agent-Space Folder** — task surface, state, logs, receipts

All three layers must exist and be consistent for an agent to be "full."

---

## Required Files by Layer

### Layer 1: Hermes Profile (`~/.hermes/profiles/<name>/`)

| File | Required | Purpose |
|---|---|---|
| `config.yaml` | ✅ | Model, provider, aliases, fallback |
| `SOUL.md` | ✅ | Identity + posture capsule (<2KB) |
| `USER.md` | Optional | User-specific context |
| `MEMORY.md` | Optional | Durable facts |
| `scope.md` | Optional | Scope boundaries |

### Layer 2: TRIS Component (`TRISMIGISTUS/COMPONENTS/agents/<NAME>/`)

| File | Required | Purpose |
|---|---|---|
| `identity.md` | ✅ | Name, reports-to, role, core function |
| `manifest.json` | ✅ | Agent class, capabilities, boundaries |
| `scope.md` | ✅ | In-scope / out-of-scope, read/write roots |
| `policy.md` | ✅ | Decision gates, invariants |
| `routing.md` | ✅ | How this agent routes to others |
| `state/` | ✅ | Runtime state |
| `receipts/` | ✅ | Action receipts |
| `skills/` | ✅ | Linked skills |
| `links/` | ✅ | Cross-agent links |
| `task-packets/` | ✅ | Task schemas |

### Layer 3: Agent-Space (`AGENT_ARENA/ACTIVE/AGENT_<NAME>_TRIS/`)

| File | Required | Purpose |
|---|---|---|
| `<Name>_SOUL.md` | ✅ | Agent-space SOUL (mirrors profile) |
| `<Name>_SCOPE.md` | ✅ | Agent-space scope |
| `<Name>_MEMORY.md` | ✅ | Agent-space memory |
| `<Name>_USER.md` | ✅ | Agent-space user context |
| `<Name>_config.yaml` | ✅ | Agent-space config (mirrors profile) |
| `<Name>_state.md` | ✅ | Current state |
| `<Name>_TASK_STATUS.md` | ✅ | Task state machine |
| `<Name>_AGENT_MANIFEST.json` | ✅ | Class, capabilities, boundaries |
| `<Name>_ROUTE_INDEX.md` | ✅ | Routing table |
| `<Name>_REPORTS_TO_*.md` | ✅ | Reporting chain |
| `T1_Intention/` | ✅ | Intention layer |
| `T2_Execution/` | ✅ | Execution layer |
| `logs/` | ✅ | Session logs |
| `sessions/` | ✅ | Session data |
| `skills/` | ✅ | Agent-specific skills |
| `cache/` | ✅ | Cache |
| `cron/` | ✅ | Scheduled tasks |
| `plugins/` | ✅ | Plugin configs |
| `alignment_playground/` | ✅ | Alignment testing |

---

## Activation States

| State | Meaning |
|---|---|
| `scaffolded_not_activated` | All files exist, no live model/task |
| `profile_active` | Hermes profile has live model |
| `component_active` | TRIS component has identity + scope |
| `task_assigned` | Has a current task |
| `fully_operational` | All three layers + live task + evidence |

An agent is only **fully operational** when all three layers are consistent AND it has a live task with evidence of execution.

---

## Current Agent Status

### Full Agents (3/3 layers)

| Agent | Hermes Profile | TRIS Component | Agent-Space | Status |
|---|---|---|---|---|
| ONU | ✅ | ✅ | ✅ | **fully_operational** |
| TCP01 | ✅ | ✅ | ✅ | **fully_operational** |
| MEMORY_CURATOR | ✅ | ✅ | ✅ | **fully_operational** |

### Profile + Component (no agent-space)

| Agent | Hermes Profile | TRIS Component | Agent-Space | Status |
|---|---|---|---|---|
| SOLOBILITY | ✅ | ✅ (SOLOBIC_SCRIBE) | ❌ | Needs agent-space |
| FACTCHECK | ✅ | ❌ | ❌ | Needs component + agent-space |
| GODSEYE | ✅ | ❌ | ❌ | Needs component + agent-space |

### Profile + Agent-Space (no TRIS component)

| Agent | Hermes Profile | TRIS Component | Agent-Space | Status |
|---|---|---|---|---|
| APPCTX | ✅ | ✅ | ✅ | scaffolded_not_activated |
| CHAT_EXCAVATION_SCOUT | ✅ | ✅ | ✅ | scaffolded_not_activated |
| HERMESSPL | ✅ | ✅ | ✅ | scaffolded_not_activated |
| JHANOS_GATE | ✅ | ✅ | ✅ | scaffolded_not_activated |
| JHANOS_X_CUSTODIAN | ✅ | ✅ | ✅ | scaffolded_not_activated |
| SHADOW_JHANOS_GATE | ✅ | ✅ | ✅ | scaffolded_not_activated |
| TCP_LEGACY | ✅ | ✅ | ✅ | scaffolded_not_activated |
| TEMPLATE_EVOLUTION_SCOUT | ✅ | ✅ | ✅ | scaffolded_not_activated |

### Profile Only (no TRIS component, no agent-space)

| Agent | Hermes Profile | TRIS Component | Agent-Space | Status |
|---|---|---|---|---|
| — | — | — | — | — |

(All profiles have at least agent-space or component.)

---

## Gap Analysis

**Missing agent-space folders:**
- SOLOBILITY → needs `AGENT_ARENA/ACTIVE/AGENT_SOLOBILITY_TRIS/`
- FACTCHECK → needs `AGENT_ARENA/ACTIVE/AGENT_FACTCHECK_TRIS/` + TRIS component
- GODSEYE → needs `AGENT_ARENA/ACTIVE/AGENT_GODSEYE_TRIS/` + TRIS component

**Missing TRIS components:**
- FACTCHECK → needs `TRISMIGISTUS/COMPONENTS/agents/FACTCHECK/`
- GODSEYE → needs `TRISMIGISTUS/COMPONENTS/agents/GODSEYE/`

**Inactive (scaffolded but no task):**
- APPCTX, CHAT_EXCAVATION_SCOUT, HERMESSPL, JHANOS_GATE, JHANOS_X_CUSTODIAN, SHADOW_JHANOS_GATE, TCP_LEGACY, TEMPLATE_EVOLUTION_SCOUT

---

## Bring-Up Protocol

To bring an agent from `scaffolded_not_activated` to `fully_operational`:

1. **Verify consistency** — SOUL/SCOPE/MEMORY match across all three layers
2. **Assign model** — ensure `config.yaml` has working provider + model
3. **Define task** — write first task to `TASK_STATUS.md`
4. **Smoke test** — run a bounded task, verify receipt
5. **Promote** — mark `fully_operational` in TASK_STATUS + ledger

---

## Evolution log

- v1.0.0 — 2026-09-15 — Initial standard. Three-layer model defined. Gap analysis complete.
