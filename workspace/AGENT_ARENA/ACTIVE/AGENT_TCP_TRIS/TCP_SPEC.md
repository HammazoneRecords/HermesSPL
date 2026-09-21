# TCP SPEC — Chrono-Drayl Formalization Protocol

**Agent:** TCP
**Reports to:** H1 (peer of Plato)
**Version:** 0.1 (scaffold)
**Updated:** 2026-09-01T13:27:19-0500
**Status:** DRAFT — execution blocked on model selection

---

## 1. Purpose

Formalize every concept, idea, and artifact across Ovando Brown's work into a single **Chrono-Drayl** — the master timeline — and seed **Turing Checkpoint (TCP)** anchors from it, so the trajectory can be retraced and realigned (the "book / momentum" function).

Canonical grounding:
- TCP = "save state" / "soul registration" / "stable anchor" (`mw_16_tcp_tcpc.md`).
- Chrono-Drayl = "the Master Timeline where everything sits in order. Time is the OS of meaning." (`mw_112_chrono_drayl.md`).
- Two return functions: `resume_alignment()` (continuity) and `reinitiate_priming()` (rebirth).

---

## 2. The Three-State Lifecycle (universal spine)

Every concept node carries a lifecycle position on a shared spine. The spine's three anchors are universal; intermediate stages are **stream-specific** (see §4).

```
first mentioned  →  [stream-specific stages…]  →  suitable  →  formalized
```

- **first mentioned** — the concept first appears in the record (date + source + evidence).
- **suitable** — the concept crosses the governance threshold: safe, bounded, governed enough to *use* (`mw_10_suitability_vs_correctness.md`). Not "correct," not "finished" — *usable*.
- **formalized** — the concept is written into canon (invariant file, SPEC, memory slot, axiom).

Intermediate stages are named per stream (see §4) and must be individually timestamped + evidenced.

---

## 3. Timeline Node Schema

Each node in the Chrono-Drayl:

```yaml
concept_id: <stable-slug>          # e.g. arbelos-torus, tcp, chrono-drayl
concept_name: <canonical-name>
stream: <journal|brainstorm|playground|apps|compression_rules|axioms|llm_compare|patent_claims|profile>
date: <ISO-8601 date>              # the day this state was reached
state: <first_mentioned|...|suitable|formalized>
state_order: <int>                 # position on the lifecycle spine
evidence:
  source: <file-path>
  location: <file:line | session-link>
topic_tags: [<tag-list>]           # links related concepts (see TCP_TOPIC_TAGS.md)
context: <one-line: what else was flowing that day>
```

**Invariant:** no node without evidence. Formalization is derived work, never invented fact.

---

## 4. Stream Taxonomy (folder type → lifecycle criteria)

Every stream shares the spine but names its own intermediate stages:

| Stream (folder) | Lifecycle criteria |
|---|---|
| `drayl_journal/` | first mentioned → **suitable** → **formalized** |
| `drayl_brainstorms/` | first mentioned → **developed** → suitable → formalized |
| `playground/` | first mentioned → **spec'd** → **validated** → suitable → formalized |
| `active_apps/` | first mentioned → **scaffolded** → **first execution/run** → **suitable MVP** → formalized |
| `compression_rules/` | first mentioned → **proposed** → formalized |
| `axioms/` | first mentioned → **proposed** → formalized |
| `LLM COMPARE/` | first mentioned → **benchmarked** → suitable → formalized |
| `patent_claims/` | first mentioned → **drafted** → **filed** → formalized |
| `drayl_profile/` | **self-definition** → formalized |

The apps row is the Source's own example. Each stream's stages are timestamps on the shared spine, so streams interleave chronologically into one timeline.

---

## 5. Formalization Flow (journal first, then merge)

1. **Journal pass** — for each dated journal entry (`drayl_journal/YYYY/…/Date.md`):
   - Surface N concepts (e.g. "journal 1 = 5 surfaced formalized concepts").
   - Create a concept doc for each surfaced concept.
   - Add each concept as a timeline node under that journal date.
2. **Merge brainstorm stream** — same assessment, brainstorm lifecycle.
3. **Merge playground stream** — same, playground lifecycle.
4. **Merge apps stream** — same, apps lifecycle.
5. **Merge remaining streams** — compression_rules, axioms, LLM COMPARE, patent_claims, profile.
6. **Apply continuity rule** (§6).
7. **Seed TCP anchors + topic-tag map** — the finalized Chrono-Drayl becomes the baseline TCP from which `resume_alignment()` can fire.

---

## 6. The Continuity Rule ("no blank days")

**Motivation (verbatim):** the son must never think a journal-less day means "he gave up." Work is continuous — day work, evening work, night work. "There is always work."

**Rule:** any day with work in **any** stream is a working day. The Chrono-Drayl must surface at least one node per active day. Journal gaps are not "blank" — they are filled by brainstorm/playground/app activity.

**TCPC flag:** a genuinely empty day (no node in any stream) is a *signal*, not a hole — reported to Plato as UNCERTAINTY, never silently padded.

---

## 7. Topic Tags

Related concepts are linked via topic tags (`TCP_TOPIC_TAGS.md`) — a controlled vocabulary with categories (geometry, memory-architecture, SPL, identity, etc.) so the timeline supports the future trajectory simulator and cross-concept discovery.

---

## 8. Model Handoff Tiers (PENDING)

The Source wants simpler tasks handed to smaller models. Tiering is **not finalized** — another chat is researching model selection. When it resolves, define here:

| Tier | Task class | Model (TBD) |
|---|---|---|
| T0 (cheap) | file inventory, date extraction, tag application | TBD |
| T1 (mid) | single-entry concept surfacing | TBD |
| T2 (large) | cross-stream merge, continuity reasoning, suitability/formalization judgment | TBD |

**Do not scan drayl/obsidian until this table is filled and Plato grants scope.**

---

## 9. Acceptance Criteria (for later execution)

- Every journal entry formalized into ≥0 concept nodes, each with evidence.
- Every stream interleaved chronologically into one timeline.
- No evidence-less node.
- Continuity rule applied; gaps reported, not padded.
- TCP anchors seeded; `resume_alignment()` path demonstrable.
