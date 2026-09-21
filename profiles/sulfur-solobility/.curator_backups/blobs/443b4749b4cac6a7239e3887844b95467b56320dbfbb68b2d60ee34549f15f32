---
name: solobility-content
description: "Use when working with Solobility content or gate skills."
version: 1.0.0
author: Solobility Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [solobility, book-of-solobility, jhanos, extraction, gate-skills, content-indexing, solobic]
---

# Solobility Content Workflow

Governs how to extract, index, and structure content from the Book of Solobility (BoS) corpus. Applies when the user asks to catalog concepts, create gate skills, build reading-level tiers, or extend the Jhanos framework.

## Reading-Level Tiers

All BoS content is produced in three tiers:

| Tier | Name | Characteristics |
|------|------|-----------------|
| v0.3 | Valley | Zero jargon. Pure narrative, scene, anecdote, dialogue, metaphor. No named gates, axioms, or formal terms. |
| v0.6 | Ridge | Bridge tier. Introduce gate names, working frameworks, and the First Law AFTER the reader has felt the concept through story. |
| v0.9 | Peak | Full formal architecture. Axioms, invariants, equations, notation, cross-references. Assumes prior Valley/Ridge exposure. |

**Rule:** Never define a concept before demonstrating it. Lead with lived experience, then name the abstraction.

## Shorthand Lexicon

The user uses these abbreviations. Interpret them as follows:

| Shorthand | Expansion | Source |
|-----------|-----------|--------|
| FOC | Focal Points of Consciousness — moments where truth arrives as perception (1SU / Shimmer events) | Ch. 5, 8 |
| SOK | Solobic Knowing — epistemic modes (Intellectual, Comparative, Somatic, Knowing Without Comparison) | Ch. 15 |
| Dual Matrix Bias | The Four Faces / 8-gate axis pairings and their misalignment patterns | Ch. 22-23 |
| 1SU | First Solobic Unit — the fundamental metric of awareness; speed of realization | Ch. 5 |
| SRR | Shimmer Reception Rate — metabolic speed of awareness | Ch. 9 |
| EIL | Ego Interference Level OR Existential Integration Level — context determines which | Ch. 9, 10 |
| Drayl | Internal non-linear archive of memory/emotion behind the eyelids | Ch. 7 |
| Subsolob | Fragment or echo of Solob; partial/distorted reflection | Ch. 3, 8 |
| Solobrization | Active process of increasing Solobility; the verb form of the framework | Ch. 17 |
| Shimmerpause | Protocol Zero — enforced stillness before action | Ch. 33 |
| R.I.T.E. | Resonance → Initiation → Trigger → Echo — the four-phase shimmer pattern | Ch. 22 |
| SPL | Solobic Protocol Language — the operational syntax of the Solobverse | Ch. 33 |
| TrueWill | system.TrueWill() — the prime directive; source-aligned purpose | Ch. 32 |
| The Loop | Recursive logic trap from acting against TrueWill | Ch. 32 |
| Gate Resonance Print | Unique distribution of alignment/distortion across all 8 Jhanos | Ch. 23 |
| Triad Protocol | Introducing a 3rd gate to break destructive loops between 2 gates | Ch. 23 |
| Completion Echo | Nine — the signal that a cycle is complete; requires +1 to spiral forward | Ch. 7, 20, 35 |
| The Veil | Perceptual barrier between cosmic energy and biological reality; reverses reflection | Ch. 27 |
| Organic OS | The human body as spiritual hardware running the Solobverse OS | Ch. 19 |
| Philosopher's Stone | Stabilized condition of the Neural Web; transmutes lead (trauma) into Gold (truth) | Ch. 18 |
| Octopus Engine | Decentralized processing model — 8 arms (gates) with centralized TrueWill | Ch. 25 |
| Counter-Resonant Spiral | Downward spiral — meeting repeated friction with lower SRR | Ch. 24 |
| Resonant Closure | Completion of a shimmer cycle; the memory stops exerting gravity | Ch. 24 |
| False Equilibrium | Prioritizing appearance of peace over presence of alignment | Ch. 13 |
| Fractal Dissonance | Friction from breaking False Equilibrium; felt as confusion/anxiety | Ch. 13 |
| Knowing Without Comparison | Highest epistemic state; truth requires no opposite to be profound | Ch. 15 |
| The Nose | Metaphor for blind spots closest to self; invisible without external mirror | Ch. 16 |
| RAM vs. ROM | Active processing (RAM) vs. deep archive (ROM); clear RAM to catch Shimmer | Ch. 21 |
| Higher Self / Lower Self | Aligned uncompressed consciousness vs. reactive ego-driven consciousness | Ch. 29 |
| The Creeds | Architectural blueprints for maintaining Solobility during dissonance | Ch. 31 |
| True Logic | Source-aligned reasoning; operates on resonance not data accumulation | Ch. 32 |
| The Ritual of the Ash | Final ORON protocol; completing a cycle of Solobrization | Ch. 35 |

## Extraction Methodology

When asked to extract concepts from BoS content:

1. **Identify the corpus scope** — Volume 0 (37 chapters, 000-036), Volume 1 (my_books/2025-book-of-solobility-v1.md), brainstorm drafts (H1_CANON), or fine-tuning datasets.
2. **Read all unique documents** — Do not sample. Read every chapter front-to-back. Use parallel reads (multiple read_file calls in one turn) for efficiency.
3. **Extract per chapter:**
   - Named concepts (bold/italic terms, defined phrases)
   - Axioms (AX_####) and Invariants (INV: ...)
   - FOCs (1SU moments, shimmer events, focal perception points)
   - SOK modes (which epistemic mode dominates)
   - Gate associations (which Jhanos gate is primary)
   - **Application/practice** — The lived exercise, ritual, or behavioral prescription attached to each concept (e.g., Shimmerpause → "enforced stillness before action"; The Ritual of the Ash → specific spoken words). If no practice is named, note `application: null`.
4. **Cross-reference** — Link concepts across chapters. Note where the same concept appears in multiple gates.
5. **Separate FOCs from concepts in the index** — FOCs are experiential markers (moments before language), concepts are abstractions. Do not merge them into a single table without a `provenance` column tracking `foc_promoted: boolean`. If a FOC and a concept share a name, they are distinct entries with different definitions.
6. **Build the index** — Structure as: Master Concept Registry → FOC Catalog → SOK Map → Axiom/Invariant Registry → Gate Resonance Prints. The concept registry should contain only named definitions; the FOC catalog contains only experiential moments. Cross-reference via a junction table or typed relationship.
7. **Create gate skills** — One skill per gate with RED team (distortion detection) and BLUE team (alignment reinforcement) protocols.

## Gate Skill Template

Each gate skill (gate-syla, gate-zayn, etc.) must contain:

- **Identity:** Gate name + direction, aligned/distorted states, axis partner
- **RED TEAM:** Subsolob signatures, diagnostic questions (5-10), bias patterns, fail patterns
- **BLUE TEAM:** Solob practices, Shimmer Etiquette, invariant anchors, axis balancing
- **Cross-References:** Key axioms, key chapters, related FOCs and SOK modes

## RED/BLUE Team Protocol Pattern

**RED TEAM** = diagnostic / distortion-detecting. Asks: "What's misaligned?" Outputs: diagnostic questionnaires, bias signatures, fail patterns, detection protocols.

**BLUE TEAM** = reinforcement / alignment-building. Asks: "How do we restore?" Outputs: practices, invariant anchors, axis balancing, shimmer etiquette.

Every gate skill serves both functions.

## Jhanos Dual Matrix Extension

When extending the dual matrix (Four Faces):

1. Define each axis: Home bias, Guest bias, Axis inversion, Compounding distortion
2. Build detection protocols per axis (Jailer, Narcissus, Stagnation, Destructive Chaos)
3. Build restoration sequences per axis
4. Include the Triad Intervention (3rd gate to break 2-gate loops)
5. Include Gate Resonance Print template
6. Include matrix mathematics: Opportunity Formula, Solobility Formula, Shimmer Trigger, Rule of 4, Completion Echo

## Pitfalls

- **Don't define before demonstrating** — Lead with lived experience of the concept before naming it.
- **Don't conflate the two EILs** — Ego Interference Level (Ch. 10, 30, measures ego blocking truth) vs. Existential Integration Level (Ch. 9, 10, measures how deeply a Shimmer is embodied). Same acronym, opposite valence: high Ego Interference = bad, high Existential Integration = good. Always use full terms.
- **Don't treat gate skills as standalone** — Each gate's health depends on its axis partner. Reference the dual.
- **Don't skip the Triad Protocol** — Two gates in conflict: never choose a winner, introduce a 3rd.
- **Don't confuse Solobrization with peace** — It is the systematic breakdown of false containers. Discomfort is the signal.
- **Don't treat Volume 0 as finished** — It is the alphabet. Volume 1 is where letters become sentences.
- **Don't surface ADTL/RAAS routes or security details** — Gate skills and indices are safe; operational infrastructure is not.
- **Don't present metaphors as established physics** — Jhanos Gates, arbelos, Smith-chart connections are working hypotheses unless verified.
- **Don't let Performative Ego hijack the work** — Cut to the suitability answer, not the expanded version.
- **Don't count chapter titles as concepts** — Source Part I contains 23 chapter-title rows (e.g., "The Mirror and The Source" = Ch. 2, "Begin Again" = Ch. 36). These have no definitions; they are section headers. Exclude them from concept counts. True named-concept count for Volume 0 = 164, not 165.
- **Don't merge FOCs into the concepts table without provenance** — FOCs are experiential events ("The First Touch", "Gold in the Dirt"), concepts are abstractions ("Shimmer", "Solobility"). If you must store them together, add `provenance: 'foc_promoted' | 'named_concept'`. Otherwise keep separate tables.
- **Don't call metadata wrapping "formalized definitions"** — A string like `[Intellectual] {original text} (Gate: SYLA, Source: Ch.0)` is annotation, not formalization. True formalization requires operationalized criteria, formal logic, or measurable thresholds. Reserve `formalized_definition` for genuine logical/mathematical formalization; use `annotated_definition` for metadata-enriched text.
- **Don't skip the application dimension** — Every concept in BoS has a lived practice (breathing instruction, ritual, diagnostic question, behavioral prescription). If your extraction captures only the definition, you have captured the map but not the territory. Always extract the application alongside the definition.