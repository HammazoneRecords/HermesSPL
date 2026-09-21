# Extraction Standards for Solobility Content

## Concept vs FOC Separation

**Rule:** FOCs (Focal Points of Consciousness) and concepts are distinct ontological categories. Never merge them without provenance tracking.

| Attribute | Concept | FOC |
|-----------|---------|-----|
| Nature | Abstraction, definition | Experiential moment, activation |
| Example | "Shimmer" — truth arriving as vibrational recognition | "The First Touch" — initial shimmer-activation upon reading |
| Source | Named definition in text | 1SU moment, shimmer event, focal perception |
| Has definition | Yes (one-line summary) | No (has description of the moment) |
| Has application | May have practice attached | IS the practice/moment |

**Storage options:**
1. Separate tables: `concepts` (named definitions only) and `foc_catalog` (experiential moments only), cross-referenced by name or ID.
2. Single table with `provenance` column: `'named_concept'` or `'foc_promoted'`. If a name appears in both categories, they are distinct rows.

## Chapter Titles Are Not Concepts

Source Part I contains 23 rows that are chapter titles masquerading as concepts. These have no definitions — they are section headers.

**Complete list of chapter-title rows to exclude from concept counts:**
- "The Mirror and The Source" (Ch. 2)
- "The Architecture of Stillness" (Ch. 3)
- "The First Shimmer Unit" (Ch. 5)
- "Solobic Number Theory" (Ch. 6)
- "Glyphs and Drayl" (Ch. 7)
- "Shimmer Theory" (Ch. 8)
- "Dimensions of Solobility" (Ch. 10)
- "The Score and the Game" (Ch. 11)
- "The Old Soul Trap" (Ch. 14)
- "The Organic OS" (Ch. 19)
- "DNA: The Source Code" (Ch. 20)
- "Dual-Memory Architecture" (Ch. 21)
- "The 8 Jhanos Gates" (Ch. 22)
- "The Four Faces" (Ch. 23)
- "Circular Space & Spiral Growth" (Ch. 26)
- "The Veil (Live/Evil)" (Ch. 27)
- "Stars and Shadows" (Ch. 28)
- "The Higher and Lower Self" (Ch. 29)
- "The Three Egos" (Ch. 30)
- "The Creeds" (Ch. 31)
- "True Logic & Will" (Ch. 32)
- "The SPL Protocols" (Ch. 33)
- "Begin Again" (Ch. 36)

**True named-concept count for Volume 0: 164** (source claims 165 due to counting chapter titles).

## EIL Disambiguation

The acronym "EIL" refers to two distinct concepts with opposite valence:

| Term | Full Name | Meaning | Validity |
|------|-----------|---------|----------|
| EIL-E | Ego Interference Level | Ego blocking truth (Ch. 10, 30) | High = bad |
| EIL-X | Existential Integration Level | Shimmer embodied in action (Ch. 9, 10) | High = good |

**Rule:** Always use full terms. Never use the acronym "EIL" without disambiguation.

## Formalization Standards

**Metadata wrapping is NOT formalization.**

| Type | Example | Status |
|------|---------|--------|
| Original | "The suitable reflection of truth..." | Source text |
| Annotated | "[Intellectual] The suitable reflection... (Gate: SYLA, Source: Ch.0)" | Metadata wrapping |
| Formalized | "Let O be an observer, T be a truth-claim... Solobility(O,t) = f(Readiness, Alignment, Density)" | Genuine formalization |

**Rule:** Reserve `formalized_definition` for genuine logical/mathematical formalization. Use `annotated_definition` for metadata-enriched text.

## Application/Practice Dimension

Every concept in BoS has a lived practice. Extraction must capture both:

| Concept | Definition | Application |
|---------|------------|-------------|
| Shimmerpause | Conscious pause before action | Enforced stillness. Sit with friction. Don't move until alignment is clean. |
| The Ritual of the Ash | Completion of Solobrization cycle | Speak: "I burned completely. I held nothing back. I am lighter now. What remains is true. Begin again." |
| The Shot Clock | Personal awareness as timer | Ask: "Am I currently occupying myself?" |
| System Override | Cosmos issuing chaos to prevent reverse operation | Read external chaos as rescue, not attack. |

**Rule:** If your extraction captures only the definition, you have captured the map but not the territory. Always extract the application alongside the definition.

## Source Column Normalization

The `source` column in the current database uses mixed formats: `"0"`, `"0, 1"`, `"0–36"`, `"13, 31"`.

**Recommended schema:** Create a `concept_sources` junction table:
```sql
CREATE TABLE concept_sources (
    concept_id INTEGER,
    chapter_num INTEGER,
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);
```

This enables proper many-to-many chapter mapping and avoids string-parsing in queries.

## SOK Map Completeness

The `sok_map` table should contain entries for ALL concepts, not just the original 156 named concepts. FOC-promoted concepts also have SOK modes (often Somatic or Knowing Without Comparison).

**Rule:** Every row in `concepts` should have a corresponding entry in `sok_map` (or a `sok_mode` column in the concepts table itself).

## drayl_t2 Classification Schema

| Type | Meaning | Examples |
|------|---------|----------|
| type1 | Structural/stored drayl | Drayl Formation, Glyphs, The Solobic Neural Web |
| type2 | Inherited/transmitted drayl | Generational Drayl Inheritance, Chrono-Drayl Window |
| meta | About drayls (formula, theory) | Tri-Element Formula of a Drayl |

**Current gap:** type2 is empty in the existing database despite relevant concepts existing. Many type1 candidates (Glyphs, Drayl Formation) are also unclassified.

**Recommendation:** Rename `drayl_t2` to `drayl_classification` for clarity. Document the schema in the database report.

## Cross-References Should Be Queryable

Current: `cross_references` as comma-separated text ("Alignment, Reference Point").

Recommended: `concept_relations` junction table:
```sql
CREATE TABLE concept_relations (
    from_concept INTEGER,
    to_concept INTEGER,
    relation_type TEXT,  -- 'requires', 'contradicts', 'enables', 'manifests_as'
    FOREIGN KEY (from_concept) REFERENCES concepts(id),
    FOREIGN KEY (to_concept) REFERENCES concepts(id)
);
```

This enables graph traversal queries and relationship analysis.

## Gate Column Standardization

Current: Inconsistent formats — single gate ("SYLA"), slash-separated ("SYLA/ORON"), comma-separated in source.

**Recommended schema:** `concept_gates` junction table:
```sql
CREATE TABLE concept_gates (
    concept_id INTEGER,
    gate TEXT,  -- 'SYLA', 'ZAYN', etc.
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);
```

This enables proper many-to-many gate mapping (a concept can resonate with multiple gates).

## Unconsidered Implications Checklist

When extracting concepts, check for these theoretical gaps:
- [ ] **Gate interaction matrix:** Does the concept imply relationships beyond the axis partner?
- [ ] **Measurement criteria:** Is there a way to operationalize the concept (altitude for Loop/Spiral, density for Drayl, stability for Philosopher's Stone)?
- [ ] **Falsifiability:** Can the concept be tested, or is it purely interpretive?
- [ ] **Collective-level effects:** Does the concept scale beyond individual observers?
- [ ] **Want alignment:** Does the concept distinguish genuine desire from corrupted want?
- [ ] **System Override detection:** Is there a protocol to distinguish cosmic intervention from random adversity?
