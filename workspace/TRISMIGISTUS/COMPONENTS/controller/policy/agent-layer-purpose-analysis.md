# Agent Layer Purpose Analysis

Version: v1.0.0
Created: 2026-09-15

---

## The Three Layers — Intended Purpose

### Layer 1: Hermes Profile (`~/.hermes/profiles/<name>/`)

**Intended purpose:** Runtime execution config. Tells Hermes HOW to run this agent.
- Which model + provider to use
- Fallback routing
- Aliases for different modes
- The SOUL loaded into context when this profile is active

**Should contain:** config.yaml, SOUL.md (capsule), optional USER/MEMORY/scope

### Layer 2: TRIS Component (`TRISMIGISTUS/COMPONENTS/agents/<NAME>/`)

**Intended purpose:** Governance identity. Tells the system WHO this agent is and what it's allowed to do.
- Identity (name, role, reports-to)
- Scope (what it can read/write)
- Policy (decision gates, invariants)
- Routing (how it communicates with other agents)
- Task packet schemas

**Should contain:** identity.md, manifest.json, scope.md, policy.md, routing.md, state/, receipts/, skills/, links/, task-packets/

### Layer 3: Agent-Space (`AGENT_ARENA/ACTIVE/AGENT_<NAME>_TRIS/`)

**Intended purpose:** Operational workspace. Where the agent's actual work lives.
- Task surface (current task, status, history)
- State (runtime state, session data)
- Logs (execution history)
- Receipts (proof of work)
- T1/T2 layers (intention vs execution split)

**Should contain:** SOUL/SCOPE/MEMORY/USER mirrors, config mirror, state, TASK_STATUS, AGENT_MANIFEST, ROUTE_INDEX, REPORTS_TO, T1_Intention/, T2_Execution/, logs/, sessions/, skills/, cache/, cron/, plugins/, alignment_playground/

---

## Current Purpose vs Intended — By Agent

### ONU

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Full scout identity + purpose + posture + talents | Runtime config + SOUL capsule | ✅ Aligned — but SOUL is 3.6KB (over budget) |
| TRIS Component | Role: Scout, reports to TRIS | Governance identity | ⚠️ Minimal — identity.md is 3 lines, no core function described |
| Agent-Space | Full scout identity, extensive surfaces (22 files) | Operational workspace | ✅ Aligned — but has many "Surface" files that may be redundant |

**Verdict:** All three layers exist but TRIS component is thin. Agent-Space is overbuilt with surface files.

---

### TCP01

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Gate/Custodian identity (compact) | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Gate/Custodian, reports to TRIS | Governance identity | ⚠️ Minimal — 3 lines |
| Agent-Space | SCOPE, SOUL, ROUTE, REPORTS_TO, TASK_STATUS | Operational workspace | ✅ Aligned |

**Verdict:** Lean and consistent. TRIS component needs depth.

---

### MEMORY_CURATOR

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Full identity + autonomy tiers + decision gates | Runtime config + SOUL capsule | ✅ Aligned — most complete profile |
| TRIS Component | Full identity + scope + policy + scripts dir | Governance identity | ✅ Aligned — most complete component |
| Agent-Space | Not present as separate folder | Operational workspace | ❌ Missing — uses TRIS component directly |

**Verdict:** Best-aligned agent. No agent-space folder but doesn't need one (stateless evaluator).

---

### SOLOBILITY (profile-only)

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Book of Solobility writer with reading tiers | Runtime config + SOUL capsule | ✅ Aligned — clear specialist purpose |
| TRIS Component | SOLOBIC_SCRIBE exists (image description) | Governance identity | ⚠️ Mismatch — profile says "writer" but component says "scribe/image describer" |
| Agent-Space | ❌ Missing | Operational workspace | ❌ Missing |

**Verdict:** Profile is clear. TRIS component is a different agent (SOLOBIC_SCRIBE ≠ SOLOBILITY). Needs its own component + agent-space.

---

### FACTCHECK (profile-only)

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Conversation/document auditor with MOA | Runtime config + SOUL capsule | ✅ Aligned — clear specialist purpose |
| TRIS Component | ❌ Missing | Governance identity | ❌ Missing |
| Agent-Space | ❌ Missing | Operational workspace | ❌ Missing |

**Verdict:** Profile is clear and active. Needs TRIS component + agent-space.

---

### GODSEYE (profile-only)

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Visualization dashboard designer | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | ❌ Missing | Governance identity | ❌ Missing |
| Agent-Space | ❌ Missing | Operational workspace | ❌ Missing |

**Verdict:** Same as FACTCHECK — profile-only, needs full scaffold.

---

### APPCTX

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | App context documenter | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Scout/Translator | Governance identity | ⚠️ Minimal — 3 lines |
| Agent-Space | Full scaffold (11 files + 9 dirs) | Operational workspace | ✅ Aligned but Windows paths (D:/) |

**Verdict:** Scaffold is complete but references Windows paths. Needs Linux path correction + activation.

---

### CHAT_EXCAVATION_SCOUT

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Chat/session excavator | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Scout/Custodian | Governance identity | ⚠️ Minimal |
| Agent-Space | Full scaffold + AGENT_MANIFEST | Operational workspace | ✅ Aligned |

**Verdict:** Well-defined purpose. Ready for activation.

---

### HERMESSPL

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Hermes↔SPL reconciler | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Builder/Scout | Governance identity | ⚠️ Minimal |
| Agent-Space | Full scaffold + T2_Execution with fork | Operational workspace | ✅ Aligned — most complex agent-space |

**Verdict:** Purpose is clear (reconcile upstream Hermes with SPL). T2_Execution contains the actual fork code.

---

### JHANOS_GATE

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Language/meaning gate | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Gate | Governance identity | ⚠️ Minimal |
| Agent-Space | Full scaffold + AGENT_MANIFEST | Operational workspace | ✅ Aligned |

**Verdict:** Clear purpose — assess statements for category/contradiction/motive-overread.

---

### JHANOS_X_CUSTODIAN

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Hold unresolved payloads safely | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Custodian | Governance identity | ⚠️ Minimal |
| Agent-Space | Full scaffold + AGENT_MANIFEST | Operational workspace | ✅ Aligned |

**Verdict:** Clear purpose — escrow/holding orbit for unmanifestable payloads.

---

### SHADOW_JHANOS_GATE

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Math/continuation gate | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Gate | Governance identity | ⚠️ Minimal |
| Agent-Space | Full scaffold + AGENT_MANIFEST | Operational workspace | ✅ Aligned |

**Verdict:** Clear purpose — assess entropy pressure, survival claims, hold conditions.

---

### TCP_LEGACY

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Chrono-Drayl formalizer, peer of TRIS | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Historical | Governance identity | ⚠️ Minimal + "Historical" is not a role |
| Agent-Space | Full scaffold + Drayl/Shadow_Drayl0 dirs | Operational workspace | ✅ Aligned |

**Verdict:** Purpose is clear but TRIS component undersells it ("Historical" ≠ "Chrono-Drayl formalizer").

---

### TEMPLATE_EVOLUTION_SCOUT

| Layer | Current Purpose | Intended Purpose | Gap |
|---|---|---|---|
| Hermes Profile | Compare findings, propose template v0.2 | Runtime config + SOUL capsule | ✅ Aligned |
| TRIS Component | Role: Scout/Translator | Governance identity | ⚠️ Minimal |
| Agent-Space | Full scaffold + AGENT_MANIFEST | Operational workspace | ✅ Aligned |

**Verdict:** Clear purpose but depends on other agents (Jhanos gate, chat excavation) being active first.

---

## Cross-Cutting Issues

### 1. TRIS Components Are Uniformly Thin
All 12 components have the same 3-line identity.md pattern:
```
Role: <class>
Reports to: TRISMIGISTUS.
Historical source is preserved separately and has no routing authority.
```
Only MEMORY_CURATOR and SOLOBIC_SCRIBE have real depth. The rest are placeholders.

### 2. Agent-Space ↔ Profile SOUL Mismatch
Most agent-space SOUL files are **richer** than profile SOUL files. The profile says "I am X, a scoped agent" while the agent-space says "X exists to perform this bounded role: <actual purpose>". The profile should be the authoritative identity, not a mirror header.

### 3. SOLOBIC_SCRIBE ≠ SOLOBILITY
The TRIS component for solobility work is called SOLOBIC_SCRIBE (image description). The Hermes profile is called SOLOBILITY (Book writing). These are different jobs. Either rename or create separate agents.

### 4. Windows Paths in Agent-Space
APPCTX and others reference `D:/MW_CENTRAL/` — these are stale from the Windows era. Need Linux path correction before activation.

### 5. "Reports to: Plato" vs "Reports to: TRISMIGISTUS"
Some agent-space files say "Reports to: Plato" (JHANOS_GATE, JHANOS_X_CUSTODIAN, SHADOW_JHANOS_GATE, TCP_LEGACY). TRIS components say "Reports to: TRISMIGISTUS". This is a governance inconsistency — Plato is not the current coordinator.

---

## Recommended Actions

| Priority | Action |
|---|---|
| 1 | Fix "Reports to: Plato" → "Reports to: TRISMIGISTUS" in agent-space files |
| 2 | Deepen TRIS component identity.md files (add core function, not just role) |
| 3 | Resolve SOLOBIC_SCRIBE vs SOLOBILITY naming |
| 4 | Fix Windows paths in APPCTX agent-space |
| 5 | Create missing TRIS components (FACTCHECK, GODSEYE) |
| 6 | Create missing agent-space folders (SOLOBILITY, FACTCHECK, GODSEYE) |
| 7 | Make profile SOUL authoritative (not just a mirror header) |
