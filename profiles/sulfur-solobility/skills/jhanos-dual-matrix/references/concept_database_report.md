# Concept Database — Second Pass Results

**Database:** `/root/.hermes/profiles/solobility/skills/jhanos-dual-matrix/references/solobility_concepts.db`

## Final Counts

| Table | Count | Source Claim | Variance |
|-------|-------|--------------|----------|
| Concepts | 164 | 165 | -1 (source off-by-one) |
| FOCs | 160 | 142 | +18 (source undercounts) |
| Axioms | 38 | 39 | -1 (AX_038 missing from source) |
| Invariants | 109 | 118 | -9 (pattern text not formally labeled) |
| Chapters | 37 | 37 | ✓ |
| Gate Resonance | 8 | 8 | ✓ |

## Gaps Found

### 1. Concepts (164 of 165)
The source document claims 165 but only contains 164 unique concept entries. The count in the source is off by one.

### 2. FOCs (160 vs 142 claimed)
Source undercounts. The actual FOC table contains 160 entries across 4 categories:
- Reception: 75
- Reflection: 56
- Integration: 17
- Collective: 12

### 3. Axioms (38 of 39)
Source claims 39 (AX_001–AX_039) but **AX_038 is missing** from the source document. It's referenced in the summary but has no entry in the table.

### 4. Invariants (109 of 118)
Source claims 118 but only 109 are formally labeled with INV: IDs in the table. The remaining 9 are described in prose but not given formal invariant labels.

### 5. Orphaned FOCs (154)
154 of 160 FOCs don't have matching entries in the concepts table. This is **expected** — FOCs (Focal Points of Consciousness) are distinct from named concepts. They represent moments of activation rather than definitions.

### 6. Skill Concept Coverage
- **Gate Resonance Print**: Present as `INV: Gate Resonance Print` (invariant, not named concept)
- **Shimmer Trigger**: Present as `AX_035` (axiom, not named concept)
- All other skill concepts: ✓ Present

## Database Schema

```
concepts          → name, gate, chapter, definition, sok_mode
foc_catalog       → foc_name, chapter, gate, foc_type, description, category
axioms            → id (AX_####), statement, gate, chapter
invariants        → id (INV: ...), summary, gate, chapter
gate_resonance    → gate, aligned_state, distorted_state, axis_partner, key_concepts, diagnostic_questions
chapters          → chapter_num, title, primary_sok, secondary_sok
sok_map           → concept_name, sok_mode
```

## Sample Queries

```sql
-- All concepts for a gate
SELECT name, definition FROM concepts WHERE gate = 'BARA';

-- All axioms for an axis
SELECT * FROM axioms WHERE gate LIKE '%BARA%' OR gate LIKE '%LOMI%';

-- FOCs by category
SELECT foc_name, description FROM foc_catalog WHERE category = 'Somatic';

-- Chapter SOK modes
SELECT chapter_num, title, primary_sok FROM chapters ORDER BY chapter_num;

-- Gate resonance diagnostic
SELECT diagnostic_questions FROM gate_resonance WHERE gate = 'BARA';
```
