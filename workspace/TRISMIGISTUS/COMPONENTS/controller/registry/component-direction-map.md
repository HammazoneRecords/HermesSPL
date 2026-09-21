# ANDROMALIUS — Component Direction Map

Version: v1.0.1
Updated: 2026-09-15

---

## Controller (TRISMIGISTUS)

| Component | File | Purpose | Direction |
|---|---|---|---|
| Policy | `controller/policy/historical-source-policy.md` | Historical material provenance | Stable |
| Policy | `controller/policy/authority-evolution-timeline.md` | System evolution record | Stable |
| Flowchart | `controller/policy/workspace-evolution.html` | Visual authority + evolution | Stable |
| FW Registry | `controller/registry/fw-registry.md` | 277 future work entries | Growing |
| Gaps | `controller/registry/gaps.md` | Unfilled gaps | Shrinking |
| Folder Map | `controller/registry/workspace-folder-map.md` | This file's predecessor | Superseded by this |
| Memory Flow | `controller/routing/memory-review-flow.md` | Curator ↔ TRIS flow | Updated |

## Curator (MEMORY_CURATOR)

| Component | File | Purpose | Direction |
|---|---|---|---|
| Runner | `MEMORY_CURATOR/scripts/curator_runner.py` | Tier 1+2 automation | Active |
| Policy | `MEMORY_CURATOR/policy/curator-autonomy-tiers.md` | 3-tier autonomy | Stable |
| Receipts | `MEMORY_CURATOR/receipts/` | Daily JSONL logs | Growing |
| Identity | `MEMORY_CURATOR/` (folder) | Agent identity + scope | Stable |

## Profiles (~/.hermes/profiles/)

| Profile | Model | SOUL | Refs | Direction |
|---|---|---|---|---|
| root | gpt-5.5 | 1250B | +2 | Stable |
| tcp01 | solar-pro4:free | 572B | 0 | Live |
| onu | longcat-2.0:free | 1102B | +2 | Live |
| factcheck | gpt-5.6-luna | 1695B | 0 | Live |
| godseye | longcat override | 1797B | 0 | Live |
| solobility | longcat override | 933B | +1 | Live |
| memorycurator | longcat override | 1108B | +1 | Live |
| appctx | — | 817B | 0 | Partial |
| chatexcavationscout | — | 1015B | 0 | Partial |
| hermesspl | — | 935B | 0 | Partial |
| jhanosgate | — | 899B | 0 | Partial |
| jhanosxcustodian | — | 909B | 0 | Partial |
| shadowjhanosgate | — | 950B | 0 | Partial |
| tcplegacy | — | 1019B | +1 | Partial |
| templateevolutionscout | — | 1002B | 0 | Partial |

## Agents (AGENT_ARENA/ACTIVE)

| Agent | Status | Direction |
|---|---|---|
| AGENT_TCP01_TRIS | Live profile | Stable |
| AGENT_ONU_TRIS | Live profile | Stable |
| AGENT_FACTCHECK_TRIS | Live profile | Stable |
| AGENT_GODSEYE_TRIS | Live profile | Stable |
| AGENT_SOLOBILITY_TRIS | Live profile | Stable |
| AGENT_MEMORY_CURATOR_TRIS | Live profile | Stable |
| AGENT_APPCTX_TRIS | Partial | Needs model + task |
| AGENT_CHAT_EXCAVATION_SCOUT_TRIS | Partial | Needs model + task |
| AGENT_HERMESSPL_TRIS | Partial | Needs model + task |
| AGENT_JHANOS_GATE_TRIS | Partial | Needs model + task |
| AGENT_JHANOS_X_CUSTODIAN_TRIS | Partial | Needs model + task |
| AGENT_SHADOW_JHANOS_GATE_TRIS | Partial | Needs model + task |
| AGENT_TCP_LEGACY_TRIS | Partial | Needs model + task |
| AGENT_TEMPLATE_EVOLUTION_SCOUT_TRIS | Partial | Needs model + task |

## Authority Chain

| Link | File | Direction |
|---|---|---|
| Root law | `/root/MW_CENTRAL/AGENTS.md` | Being cleaned (old CLAUDE.md framing) |
| Hermes context | `/root/MW_CENTRAL/.hermes.md` | Stable |
| ANDROMALIUS Hermes | `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/.hermes.md` | Stable |
| Plan types | `.hermes/plans/plan-types-and-chain.md` | Stable |
| Ledger | `.hermes/plans/PLAN_EVOLUTION_LEDGER.md` | 2C 1A 1P |

## Plans

| Type | Count | Direction |
|---|---|---|
| Working plans | 14 | Growing slowly |
| Implementation plans | 2 | As needed |
| PEV plans | 683 | Historical + active |

## Knowledge + Evidence

| Component | Location | Direction |
|---|---|---|
| Concepts | `KNOWLEDGE_LIBRARY/CONCEPTS/` | 18 unresolved |
| Digests | `KNOWLEDGE_LIBRARY/DIGESTS/` | Growing |
| Fact-checks | `KNOWLEDGE_LIBRARY/FACT_CHECK/` | Growing |
| Quarantine | `KNOWLEDGE_LIBRARY/QUARANTINE/` | 225 files |
| Receipts | `KNOWLEDGE_LIBRARY/RECEIPTS/` | Growing |

## Infrastructure

| Component | Location | Direction |
|---|---|---|
| RunPod | `RUNPOD_PROTOCOLS/` | $6.21, 0 pods |
| VPS | `VPS_MANAGEMENT/` | 121 files |
| Backups | Not yet in ANDROMALIUS | Needs setup |
| Matrix | `MATRIX/` | Static → Live (deferred) |

## Deprecated / Historical

| What | Where | Direction |
|---|---|---|
| FRAMELESS/ | `FRAMELESS/` | DEPRECATED → TRISMIGISTUS/registry |
| Old AGENTS.md copies | vault/archive | Archived |
| agent_space mirrors | AGENT_ARENA/SOURCE_MIRRORS | Proof only |

---

## Direction Key

- **Stable** — working, no imminent change
- **Growing** — actively accumulating content
- **Active** — running, being used
- **Live** — has model + routing
- **Partial** — scaffolded, needs activation
- **Needs X** — gap identified, queued
- **Shrinking** — being resolved/closed
- **Superseded** — replaced by another file
- **DEPRECATED** — do not use, content moved
