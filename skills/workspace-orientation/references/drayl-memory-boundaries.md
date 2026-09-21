# Drayl Memory Boundaries

Reusable reference for restructuring a personal Drayl/Hermes workspace without recursive contamination.

## Ownership matrix

| Plane | Owner | Typical content | Authority rule |
|---|---|---|---|
| H1 — Human Source | User | `drayl_journal`, `drayl_brainstorms`, Bars, images, direct observations | Preserve original voice and provenance. Never silently normalize, overwrite, or promote. |
| H2 — Reflection | Jointly reviewed | `drayl_profile`, `_extraction`, gem indexes, timelines, worldview maps, candidate axioms, Main/Shadow/Current/Deviation analysis | Derived material must link to H1, carry status/confidence, and remain revisable. It is not the source. |
| H3 — Hermes/System | Hermes/system | `SOUL.md`, `USER.md`, `MEMORY.md`, `.hermes.md`, AGENTS/rules, governance specs, manifests, logs, handoffs | Governs the agent and workspace. Do not use it as a substitute for the user's source identity. |

## Drayl subject layers are separate

The five-layer model found in `playground/2026-03-interaction-patterns/tunnel-vision-protocol.md` is a conceptual taxonomy, not a memory-ownership hierarchy:

1. Ontology — truth, Source/Mirror, Solob, Shimmer
2. Physics — Drayl, R.I.T.E., witness(), Solobic Rail
3. Architecture — Jhanos, Octopus Engine, Solobic Tree
4. OS — SPL, LRE, Kernel, agents, loop checks
5. Manifestation — books, apps, sites, tools

An item may have both an ownership label (H1/H2/H3) and a subject-layer label (L1–L5).

## Safe routing rules

- Keep the canonical source roots in place; create indexes and links rather than mass-copying every Markdown file.
- Never scan a route, mirror, or generated corpus as an input source for the next route build.
- Exclude `_Hermes_Route`, `Corpus`, old mirrors, `.git`, dependencies, build/cache directories, and generated outputs unless explicitly selected.
- Treat `Main Drayl`, `Shadow Drayl`, `Current Index`, and `Deviation Index` as review/state concepts, not automatic promotion folders.
- Contradictions go to Shadow/Deviation; unresolved or short-lived material stays Current; promotion to stable/Main requires explicit source review.
- If canonical and mirror locations disagree, report the discrepancy first. Do not silently delete or overwrite either side.

## Evidence from the Drayl workspace

- `drayl_journal/MISC/CLAUDE.md` says to preserve Patois/idiosyncratic English, avoid silent correction, and never auto-promote axioms.
- `drayl_journal/_extraction/` contains derived timelines, persona markers, worldview maps, voice corpora, and review queues; it is not raw source.
- `drayl_profile/` contains interpreted profile material and therefore requires provenance.
- `Shadow Drayl0/Plato-V0.0625/` is a separate analytical/governance environment.
- `agent_space/` is agent operational state.
- `playground/2026-03-interaction-patterns/tunnel-vision-protocol.md` defines the Source/Mirror boundary and Main/Shadow/Current/Deviation routing.
- At the time of the 2026-08-30 review, the canonical Y-MINDWAVE corpus was absent while `C:/Users/Owner/Videos/Drayl2/_Hermes_Route/Corpus` still contained 8,991 Markdown files; this must be verified afresh, not assumed.

## Preferred route shape

Use a small curated route with:

```text
00_ROUTE/       indexes, ownership boundaries, routing rules
H1_SOURCE/      links/indexes into human-originating material
H2_REFLECTION/  reviewed extraction, profiles, gems, contradictions
H3_SYSTEM/      Hermes identity, governance, Lane A/B, verified state
90_ARCHIVE/     stale mirrors and superseded maps, clearly quarantined
```

This route is a navigation and governance layer. It is not a duplicate of the entire workspace.