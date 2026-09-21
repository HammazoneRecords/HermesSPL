# Agent Identity Clarifications

Version: v1.0.0
Created: 2026-09-15
Status: ACTIVE — all changes applied

---

## Summary of Changes

### 1. SOLOBIC_SCRIBE ≠ SOLOBILITY (confirmed)
- **SOLOBIC_SCRIBE** = image/visual description tool agent (helps with Book using "solobic" logic)
- **SOLOBILITY** = Book of Solobility writer agent (drafting Volumes)
- These stay separate. SOLOBIC_SCRIBE gets its own full scaffold.

### 2. APPCTX — clarified purpose
- **Purpose:** Gather facts for each application. Update docs. Surface missed info. Stage doc updates so agents working on apps always have up-to-date facts.
- **Action:** Fixed Windows paths → Linux. Updated identity.

### 3. JHANOS agents — restructured
- **REMOVED:** JHANOS_GATE (generic language gate — too broad)
- **REMOVED:** SHADOW_JHANOS_GATE (generic math gate — too broad)
- **CREATED:** One agent per Jhanos gate (Khem, Syla, Oron, etc.)
- **JHANOS_X_CUSTODIAN** → renamed to **JHANOS_ASSESSOR**: assesses logic of each Jhanos gate, suggests scripts specific to each gate
- **SHADOW_JHANOS** → **JHANOS_ECHO**: entropy-based contrast gates. Not just negative — the contrast to main Jhanos. Assesses preliminary entropy results from RunPod uncensored model. Determines if truly negative responses are needed and if an echo should become part of the SPL equation.

### 4. TCP — renamed
- **TCP** → **TCP** (keep name, drop "LEGACY" suffix confusion)
- **TCP01** → **TCP_CHECKER**: formalizes verified chronology and checkpoint anchors

### 5. TEMPLATE_EVOLUTION_SCOUT — clarified
- **Purpose:** Evolve the agent template itself by comparing findings across all agents (scaffold audits, gate requirements, canary rules, chat excavation results) and proposing template improvements. It's the meta-agent that watches how agents are built and suggests how to build better ones.
- **Action:** Updated identity to reflect meta-purpose.

### 6. Global fixes
- All "Reports to: Plato" → "Reports to: TRISMIGISTUS"
- Windows paths (`D:/MW_CENTRAL/`) → Linux paths (`/root/MW_CENTRAL/`)
- TRIS components deepened with core function descriptions

---

## New Agent Roster

| Agent | Role | Purpose |
|---|---|---|
| ONU | Scout | Observe, classify, report evidence |
| TCP_CHECKER | Gate/Custodian | Formalize verified chronology + checkpoints |
| MEMORY_CURATOR | Curator | Memory quality gate + promotion with autonomy |
| SOLOBIC_SCRIBE | Scribe | Image/visual → text using solobic logic |
| SOLOBILITY | Writer | Book of Solobility drafting + refinement |
| FACTCHECK | Verifier | Conversation/document auditing |
| GODSEYE | Visualizer | Agent/data-flow dashboard design |
| APPCTX | Scout/Custodian | App fact gathering + doc staging |
| CHAT_EXCAVATION_SCOUT | Scout/Custodian | Chat/session excavation for ideas + patterns |
| HERMESSPL | Builder | Hermes↔SPL reconciliation + fork |
| JHANOS_ASSESSOR | Custodian | Assess logic per Jhanos gate, suggest gate-specific scripts |
| JHANOS_ECHO | Gate/Custodian | Entropy-based contrast gates, RunPod echo analysis |
| JHANOS_<GATE> (×N) | Gate | One agent per Jhanos gate (Khem, Syla, Oron, etc.) |
| TCP | Gate/Custodian | Chrono-Drayl formalization, peer of TRIS |
| TEMPLATE_EVOLUTION_SCOUT | Scout/Meta | Evolve agent template from cross-agent findings |

---

## Evolution log

- v1.0.0 — 2026-09-15 — Clarified all agent purposes. Restructured Jhanos family. Renamed TCP agents. Fixed paths + governance.
