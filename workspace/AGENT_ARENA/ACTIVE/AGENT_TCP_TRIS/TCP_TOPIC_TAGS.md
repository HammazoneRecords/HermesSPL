# TCP Topic Tags — Controlled Vocabulary

**Agent:** TCP
**Reports to:** H1 (peer of Plato)
**Version:** 0.1 (scaffold)
**Updated:** 2026-09-01T13:27:19-0500

---

## Purpose

Topic tags link related concepts and ideas across the Chrono-Drayl, so the future trajectory simulator can trace conceptual evolution and cross-stream discovery. Tags are a controlled vocabulary, not free text — consistency makes the graph traversable.

## Tag format

`category:slug` — lowercase, hyphenated. e.g. `geometry:arbelos-torus`, `spl:tcp`, `identity:hermes`.

---

## Categories

### geometry (the Source's native thought-form)
- `geometry:arbelos`
- `geometry:torus`
- `geometry:fcircle`
- `geometry:manji`
- `geometry:four-right-angles`

### spl (Solobic Programming Language + evolution)
- `spl:tcp`
- `spl:tcpc`
- `spl:chrono-drayl`
- `spl:rti` (Resonance Trajectory Index)
- `spl:suitability`
- `spl:jhanos`
- `spl:shimmer`
- `spl:sanity-ripple`
- `spl:resume-alignment`
- `spl:reinitiate-priming`
- `spl:home-guest`
- `spl:truewill`

### memory-architecture
- `memory:drayl`
- `memory:sovereign-vault`
- `memory:generational-inheritance`
- `memory:heirloom-mind`
- `memory:soul-user-memory`
- `memory:state-db`
- `memory:compression-base16`

### identity
- `identity:hermes`
- `identity:plato`
- `identity:onu`
- `identity:source` (Ovando Brown)
- `identity:tms` (the son)

### governance
- `governance:lane-a`
- `governance:lane-b`
- `governance:act-stage-decline-share`
- `governance:truth-triangle` (intent → action log → agent claim)
- `governance:scope-boundary`

### streams (source of a node)
- `stream:journal`
- `stream:brainstorm`
- `stream:playground`
- `stream:apps`
- `stream:compression-rules`
- `stream:axioms`
- `stream:llm-compare`
- `stream:patent-claims`
- `stream:profile`

### continuity (the "always working" dimension)
- `continuity:day-work`
- `continuity:evening-work`
- `continuity:night-work`
- `continuity:no-blank-days`

---

## Usage rules

1. Every node gets ≥1 `stream:` tag (auto-derived from source folder).
2. Every node gets ≥1 domain tag (`geometry:`/`spl:`/`memory:`/`identity:`/`governance:`).
3. Cross-concept links = nodes sharing a domain tag.
4. New tags must be added here first (controlled vocabulary), not invented inline.
5. `continuity:` tags mark the Source's "always working" rhythm — they are what lets the son read the river, not the gaps.
