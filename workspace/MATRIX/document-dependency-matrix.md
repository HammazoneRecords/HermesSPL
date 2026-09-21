# ANDROMALIUS — Document Dependency Matrix

Version: v1.0.0
Updated: 2026-09-15
JSON source: `MATRIX/document-dependency-matrix.json`

---

## Charge Levels

| Level | Meaning |
|---|---|
| **CRITICAL** | Changing these ripples everywhere. Workspace authority + infrastructure. |
| **HIGH** | Agent identity, gate definitions, knowledge/evidence. Affects multiple agents. |
| **MEDIUM** | Active apps, projects in motion. Scoped to specific work. |
| **LOW** | Personal journals, ideas, brainstorms. Minimal external dependency. |

---

## CRITICAL — Governance

**Ripple: changes here affect EVERYTHING**

### Canonical Files

| Document | Path | Purpose |
|---|---|---|
| Root Authority | `/root/MW_CENTRAL/AGENTS.md` | Single workspace law |
| Hermes Context | `/root/MW_CENTRAL/.hermes.md` | Declares AGENTS.md as authority |
| ANDROMALIUS Hermes | `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/.hermes.md` | ANDROMALIUS-specific Hermes context |
| Plan Types | `ANDROMALIUS/.hermes/plans/plan-types-and-chain.md` | Working → Implementation → PEV chain |
| Plan Ledger | `ANDROMALIUS/.hermes/plans/PLAN_EVOLUTION_LEDGER.md` | All working plan statuses |
| FW Registry | `ANDROMALIUS/TRISMIGISTUS/.../fw-registry.md` | 277 future work entries |
| FW TOC | `ANDROMALIUS/TRISMIGISTUS/.../fw-toc.md` | Registry index |
| Agent Standard | `ANDROMALIUS/TRISMIGISTUS/.../full-agent-standard.md` | 3-layer agent definition |
| Identity Clarifications | `ANDROMALIUS/TRISMIGISTUS/.../agent-identity-clarifications.md` | What each agent is |
| Purpose Analysis | `ANDROMALIUS/TRISMIGISTUS/.../agent-layer-purpose-analysis.md` | Mind/Body/Soul per agent |
| Historical Source | `ANDROMALIUS/TRISMIGISTUS/.../historical-source-policy.md` | Provenance rules |
| Authority Timeline | `ANDROMALIUS/TRISMIGISTUS/.../authority-evolution-timeline.md` | System evolution record |
| Authority Flowchart | `ANDROMALIUS/TRISMIGISTUS/.../workspace-evolution.html` | Visual authority flow |
| Naming Skill | `ANDROMALIUS/.hermes/skills/file-naming/SKILL.md` | File naming protocol |

### Update Groups (change these TOGETHER)

| Group | Files | Why |
|---|---|---|
| **Authority Chain** | AGENTS.md → .hermes.md → ANDROMALIUS/.hermes.md | If root authority changes, Hermes context must reflect it |
| **Plan System** | plan-types + ledger | New plan types need ledger tracking |
| **Agent Definition** | standard + clarifications + purpose analysis | Agent identity is 3 views of the same truth |

---

## CRITICAL — Infrastructure

**Ripple: breaking these breaks deploys/backups/entropy**

### Canonical Files

| Document | Path | Purpose |
|---|---|---|
| VPS Facts | `ANDROMALIUS/VPS_MANAGEMENT/` | VPS state, procedures |
| RunPod Protocols | `ANDROMALIUS/RUNPOD_PROTOCOLS/` | Spend-aware GPU workflow |
| RunPod Ledger | `ANDROMALIUS/RUNPOD_PROTOCOLS/runpod-session-ledger-*.md` | Entropy run spend tracking |
| RunPod Outputs | `ANDROMALIUS/ENTROPY_MODEL/RUNPOD_OUTPUTS/` | 4 generated entropy files |
| Entropy Model | `ANDROMALIUS/ENTROPY_MODEL/entropy-model-modelfile-v2.md` | Modelfile spec |

### Update Groups

| Group | Files | Why |
|---|---|---|
| **RunPod Spend** | ledger ↔ ENTROPY_MODEL ↔ JHANOS_ECHO | Echo agent assesses entropy results |
| **Backup Chain** | sealed backup root → captures ANDROMALIUS + earth + profiles | All-or-nothing snapshot |

---

## HIGH — Agent Components

**Ripple: changes affect one agent's 3 layers**

### Rule: Per-Agent Triple Must Stay In Sync

Each agent has 3 files that are the SAME identity in different layers:

| Layer | Location | File |
|---|---|---|
| Mind | `TRISMIGISTUS/COMPONENTS/agents/<NAME>/identity.md` | Governance identity |
| Body | `AGENT_ARENA/ACTIVE/AGENT_<NAME>_TRIS/<Name>_SOUL.md` | Operational identity |
| Soul | `~/.hermes/profiles/<name>/SOUL.md` | Runtime identity |

**When one changes, all three must be updated.**

### Update Groups

| Group | Agents | Why |
|---|---|---|
| **Jhanos Family** | BARA, KHEM, LOMI, ORON, SYLA, TARA, VORAK, ZAYN, ASSESSOR, ECHO | Gates reference each other via dualities + triads |
| **Curator System** | MEMORY_CURATOR policy + runner + flow | 3 files define one agent's autonomy |

---

## HIGH — Jhanos Gates

**Ripple: changes affect Book + agents + entropy model**

### Canonical Files

| Document | Path | Purpose |
|---|---|---|
| Gate Skills (×8) | `ANDROMALIUS/ENTROPY_MODEL/REVIEW_PACKAGE/gate-skills/gate-*-SKILL.md` | RED/BLUE team per gate |
| Entropy Matrix | `ANDROMALIUS/ENTROPY_MODEL/jhanos-entropy-matrix-extended.md` | Entropy variants per gate |
| Dual Matrix | `ANDROMALIUS/ENTROPY_MODEL/REVIEW_PACKAGE/jhanos-dual-matrix-skill.md` | Gate relationships |

### Update Groups

| Group | Rule |
|---|---|
| **Gate Definition** | When a gate skill changes → update agent-space SOUL + TRIS identity + Hermes profile SOUL |
| **Four Faces** | BARA/LOMI, TARA/ZAYN, KHEM/SYLA, VORAK/ORON — changes to one affect axis partner |
| **Triad Protocol** | KHEM+SYLA→ZAYN, VORAK+ORON→TARA — synthesis gates inherit from duality partners |
| **Entropy Outputs** | RUNPOD_OUTPUTS/ (4 files) depend on gate skill definitions |

---

## HIGH — Knowledge + Evidence

**Ripple: changes affect curator + fact-check + concepts**

### Canonical Files

| Document | Path | Purpose |
|---|---|---|
| Concepts | `ANDROMALIUS/KNOWLEDGE_LIBRARY/CONCEPTS/` | Formal concept graph |
| Digests | `ANDROMALIUS/KNOWLEDGE_LIBRARY/DIGESTS/` | Session/topic digests |
| Fact Checks | `ANDROMALIUS/KNOWLEDGE_LIBRARY/FACT_CHECK/` | Verification records |
| Quarantine | `ANDROMALIUS/KNOWLEDGE_LIBRARY/QUARANTINE/` | Pending review |
| Receipts | `ANDROMALIUS/KNOWLEDGE_LIBRARY/RECEIPTS/` | Action receipts |
| Schemas | `ANDROMALIUS/KNOWLEDGE_LIBRARY/SCHEMAS/` | Data schemas |

### Update Groups

| Group | Flow |
|---|---|
| **Curator Pipeline** | QUARANTINE → MEMORY_CURATOR → CONCEPTS + DIGESTS |
| **FactCheck Chain** | FACT_CHECK ↔ TRIS ↔ FACTCHECK agent receipts |

---

## MEDIUM — Active Apps

**Ripple: scoped to specific app + its agents**

### Update Groups

| Group | Apps | Why |
|---|---|---|
| **AppCtx Staging** | All active apps | APPCTX gathers facts → stages doc updates |
| **Solob Portal** | solob-portal | Book of Solobility delivery |
| **Time-Check** | Time-Check-App | Payroll system |
| **Marcus** | MarcusGarvey App WWMD | Garveyite app |
| **Melissa** | melissa ledger | Relief tracker |
| **Earn** | earn-mindwaveja | Transcription platform |
| **Love Ref** | love-ref | Couples accountability |

---

## MEDIUM — Projects in Motion

**Ripple: scoped to project family**

### Update Groups

| Group | Projects | Why |
|---|---|---|
| **Three-App Family** | love-ref, sieve, pact | Shared referee engine |
| **Artist Sites** | 15 domains | Single multi-tenant app |
| **MW Journal** | MWJournalX, MOctopus, concept shell | Journal/reflection tools |

---

## LOW — Drayl / Personal

**Ripple: minimal external dependency**

### Canonical Files

| Document | Path | Purpose |
|---|---|---|
| Journals | `earth/H1_CANON/drayl-t2/drayl_brainstorms/` | 465 brainstorm entries |
| Profile | `earth/H1_CANON/drayl-t2/drayl_profile/` | Personal profile |
| Axioms | `earth/H1_CANON/MIndwaVe_Ja/axioms/` | 12 axiom files |
| Invariants | `earth/H1_CANON/MIndwaVe_Ja/mw_invariants/` | 130 invariant files |
| Books | `earth/H1_CANON/my_books/` | 37 book drafts |
| Solob Source | `earth/H1_CANON/my_books/Book Of Solobility-volume0/` | Vol 0 source |

### Update Groups

| Group | Flow |
|---|---|
| **Drayl Extraction** | drayl_brainstorms → CHAT_EXCAVATION_SCOUT → KNOWLEDGE_LIBRARY |
| **Book Pipeline** | my_books/Book Of Solobility → SOLOBILITY agent + gate skills |
| **Axioms → Concepts** | axioms/ + mw_invariants/ → KNOWLEDGE_LIBRARY/CONCEPTS |

---

## Quick Reference: What to Update When

| If you change... | Also update... |
|---|---|
| AGENTS.md | .hermes.md, ANDROMALIUS/.hermes.md |
| A gate skill | That gate's: agent-space SOUL, TRIS identity, Hermes profile SOUL |
| Axis partner gate | Its duality partner (BARA↔LOMI, KHEM↔SYLA, etc.) |
| A synthesis gate | Its component gates (ZAYN needs KHEM+SYLA) |
| Curator policy | Curator runner + memory-review-flow |
| An app's structure | APPCTX stages doc update for that app |
| FW registry | FW TOC (counts + most recent) |
| Agent identity (any layer) | Other 2 layers (mind/body/soul) |
| RunPod spend | Ledger + JHANOS_ECHO assessment |
