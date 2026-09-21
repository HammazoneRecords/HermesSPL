# ANDROMALIUS Workspace — Folder Map

Version: v1.0.0
Updated: 2026-09-15

---

## Top-Level Folders

| Folder | Files | Dirs | Purpose |
|---|---|---|---|
| `.hermes/` | 208 | 46 | Plans, skills, hooks, profile config |
| `AGENT_ARENA/` | 23,667 | 2,513 | Active agents, source mirrors, exchange |
| `TRISMIGISTUS/` | 155 | 131 | Controller: policy, routing, registry |
| `KNOWLEDGE_LIBRARY/` | 313 | 27 | Concepts, digests, fact-checks, quarantine |
| `PEV_PLANS/` | 1,355 | 683 | Proof-tracked execution plans |
| `PEV_MIRROR/` | 264 | 61 | Chat/session mirrors (proof artifacts) |
| `FRAMELESS/` | 8 | 0 | **DEPRECATED** — moved to TRISMIGISTUS/registry |
| `Y-MINDWAVE/` | 2,108 | 235 | Mindwave project source |
| `ENTROPY_MODEL/` | 23 | 3 | Entropy work: Modelfiles, matrix, RunPod outputs |
| `RUNPOD_PROTOCOLS/` | 2 | 0 | Spend-aware GPU workflow + session ledger |
| `PROJECT_SKILLS/` | 13 | 6 | Per-app skills (love-ref, hermes-spl-fork) |
| `REPORTS/` | 11 | 0 | Inventory, sanitation, readiness scans |
| `MATRIX/` | 1 | 0 | Agent × skill × usage matrix |
| `MEMORY/` | 3 | 12 | Memory receipts, archives |
| `INTAKE_PROCEDURE/` | 5 | 1 | Intake flow |
| `VPS_MANAGEMENT/` | 121 | 56 | VPS facts, procedures |
| `DERIVED_CORPUS/` | 1 | 3 | Derived records |
| `WORKSPACE/` | 8 | 3 | Script index, receipts |
| `ARCHIVE_STAGING/` | 0 | 0 | Empty — ready for staging |
| `GODSEYE_DASHBOARD/` | 2 | 1 | Dashboard config |
| `AGENT_SHADOW_DRAYL/` | 15 | 8 | Shadow agent configs |
| `vault/` | 169 | 38 | Black box / evidence chamber |

## Key Files (Top-Level)

| File | Size | Purpose |
|---|---|---|
| `AGENTS.md` | — | Does NOT exist in ANDROMALIUS (root authority is `/root/MW_CENTRAL/AGENTS.md`) |
| `.hermes.md` | — | ANDROMALIUS Hermes context |
| `no-edits.md` | 661B | No-edit boundaries |
| `ovando_brown_roadmap.md` | 4.7KB | OB roadmap |
| `vape-overview.md` | 4.1KB | Vape project overview |
| `MODEL_LOCK_REGISTRY.md` | 1.8KB | Model lock registry |

---

## FW Registry Locations

| Location | Entries | Status |
|---|---|---|
| `TRISMIGISTUS/COMPONENTS/controller/registry/fw-registry.md` | 277 | **CANONICAL** |
| `FRAMELESS/future-work.md` | 277 | Historical copy (redirected) |
| `PEV_MIRROR/` (snapshots) | 8+ mirror copies | Proof artifacts only — ignore |
| `PEV_PLANS/staging/snapshots/` | 6+ `.before` snapshots | Proof artifacts only — ignore |

**Rule:** Only `TRISMIGISTUS/COMPONENTS/controller/registry/fw-registry.md` is canonical.
All other copies are historical or proof artifacts.

---

## Plan Locations

| Type | Folder | Count |
|---|---|---|
| Working plans | `.hermes/plans/` | 14 |
| Implementation plans | `.hermes/plans/implementations/` | 2 |
| Plan ledger | `.hermes/plans/PLAN_EVOLUTION_LEDGER.md` | 1 |
| PEV proof plans | `PEV_PLANS/PLN-*/` | 683 |
| Status files | `.hermes/plans/status/` | multiple |

---

## Agent Locations

| Location | Count | Contents |
|---|---|---|
| `AGENT_ARENA/ACTIVE/` | 10 agents | Live agent folders |
| `AGENT_ARENA/REGISTRY/` | 1 file | Activation registry |
| `AGENT_ARENA/EXCHANGE/` | 1 folder | Inter-agent mail tickets |
| `AGENT_ARENA/SOURCE_MIRRORS/` | 1 folder | Safe mirrors |
| `TRISMIGISTUS/COMPONENTS/agents/` | multiple | Agent identity, scope, policy |
| `~/.hermes/profiles/` | 14 dirs | Live Hermes profiles |

---

## Governance Locations

| File | Purpose |
|---|---|
| `/root/MW_CENTRAL/AGENTS.md` | Root workspace authority |
| `/root/MW_CENTRAL/.hermes.md` | Hermes context (declares AGENTS.md) |
| `TRISMIGISTUS/COMPONENTS/controller/policy/historical-source-policy.md` | Historical material provenance rules |
| `TRISMIGISTUS/COMPONENTS/controller/policy/authority-evolution-timeline.md` | System evolution record |
| `TRISMIGISTUS/COMPONENTS/controller/policy/workspace-evolution.html` | Visual flowchart |
| `.hermes/plans/plan-types-and-chain.md` | Plan type definitions |
| `TRISMIGISTUS/COMPONENTS/controller/registry/gaps.md` | Unfilled gaps |

---

## Profile Locations

| Location | Contents |
|---|---|
| `~/.hermes/profiles/<name>/config.yaml` | Model, provider, routing |
| `~/.hermes/profiles/<name>/SOUL.md` | Capsule (<2KB) |
| `~/.hermes/profiles/<name>/SOUL.*.md` | Extended references |
| `~/.hermes/profiles/<name>/USER.md` | User context (rare) |
| `~/.hermes/profiles/<name>/MEMORY.md` | Durable facts (rare) |
| `~/.hermes/profiles/<name>/scope.md` | Scope boundaries (rare) |

---

## Curator Locations

| Path | Purpose |
|---|---|
| `TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR/policy/curator-autonomy-tiers.md` | Tier definitions |
| `TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR/scripts/curator_runner.py` | Runner script |
| `TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR/receipts/` | Daily receipts |
| `TRISMIGISTUS/COMPONENTS/controller/routing/memory-review-flow.md` | Flow diagram |

---

## Version History

- v1.0.0 — 2026-09-15 — Initial folder map. FW registry consolidated to TRISMIGISTUS. FRAMELESS deprecated. 277 FW entries.
