# Concepts: Navigating the Formalized Vocabulary

This document explains how to find and use the formalized concepts that permeate HermesSPL. There are over 450 named ideas — definitions, principles, patterns, and diagnostic tools — organized into a structured index.

## Why Formalize Concepts?

When the system says "Solobility" or "Shimmer" or "RITE cycle," it means something specific. These are not metaphors. They are defined terms with agreed-upon meanings, like technical vocabulary in any discipline.

Using precise language reduces miscommunication. When a hook returns `"sfl_mode": "witness"`, everyone (human or agent) knows what that means without guessing.

## The Structure

The concept system has five layers:

### 1. Named Concepts

Each concept has a name, a definition, a Gate (which domain it belongs to), and a chapter reference. For example:

| Field | Value |
|-------|-------|
| Name | Solobility |
| Definition | The readiness measure for truth reflection; ability to hold truth without distorting it |
| Gate | LOMI (Motion) |
| Chapter | 9 |
| SOK Mode | Comparative |

The full index lives in the workspace at `solobility-concept-index.md`. It is a large table you can search or filter.

### 2. Gates (Domains)

Every concept belongs to one of eight Gates. Think of these as categories of human experience:

| Gate | Domain | Question it answers |
|------|--------|-------------------|
| SYLA | Stillness | Am I present and receptive? |
| ZAYN | Origin | What am I creating or projecting? |
| LOMI | Motion | Am I moving forward or looping? |
| VORAK | Liberation | What false certainty am I clinging to? |
| KHEM | The Forge | What is being transformed by heat? |
| BARA | Structure | Is my architecture serving or imprisoning me? |
| TARA | Nurturance | Am I seeing clearly or through distortion? |
| ORON | Order | Are my actions aligned with my deepest values? |

When you encounter a concept, its Gate tells you which area of life it applies to.

### 3. SOK Modes (Ways of Knowing)

Each concept is associated with one of four modes of knowing:

| Mode | How it works | Example |
|------|-------------|---------|
| **Intellectual** | Data, formulas, definitions | "The Solobility Formula is SRR × EIL − DC" |
| **Comparative** | Understanding through contrast | "I know this is true because the opposite fails" |
| **Somatic** | Body knows before mind explains | "I felt the truth of it before I could argue for it" |
| **Knowing Without Comparison** | Direct recognition without reference | "I simply know" |

A concept's SOK mode tells you how it is best understood. Some concepts can be grasped intellectually. Others require somatic experience. The rarest — Knowing Without Comparison — cannot be taught through explanation at all.

### 4. FOCs (Focal Points of Consciousness)

FOCs are moments of activation — specific experiences described in the source material. They are not definitions but events. For example:

- "The First Touch" — the initial shimmer-activation upon first contact
- "The Shot Clock Activation" — the moment you accept responsibility for action
- "The Sneeze" — involuntary truth discharge when the conscious mind refused to process something

FOCs are organized by how they function:

| Category | What it describes |
|----------|-----------------|
| Reception FOCs | How truth arrives |
| Reflection FOCs | How truth is processed |
| Integration FOCs | How truth becomes action |
| Collective FOCs | How truth compounds across people |

### 5. Axioms and Invariants

Axioms (AX_####) are foundational statements taken as given. Invariants (INV: ####) are patterns that hold true across all contexts.

Examples:

- **AX_001**: Never ask someone what this book means.
- **AX_005**: The Mirror is Not the Source.
- **INV: Shimmer Requires Observer Participation**: Without the eye, the shimmer does not shimmer.
- **INV: Strategic Patience**: Acting before reception produces noise-aligned action.

These are the "laws" of the system — not imposed rules but observed regularities.

## How to Use This System

### Finding a Concept

Search the concept index by name, Gate, or chapter. The index is a markdown table, so any text search works.

```bash
# Find all concepts related to "ego"
grep -i "ego" solobility-concept-index.md

# Find all concepts in the TARA gate
grep "| TARA |" solobility-concept-index.md
```

### Understanding a Concept in Context

A concept is not just its definition. To fully understand it:

1. Read the definition.
2. Note its Gate — what domain does this apply to?
3. Note its SOK mode — how is this best understood?
4. Find its chapter — what comes before and after it?
5. Look for related FOCs — what experiences activate this concept?
6. Check the axioms and invariants — what laws govern this concept?

### Using Concepts in Practice

The vocabulary is designed to be used. When you name a pattern precisely, you can act on it precisely.

Instead of: "I feel stuck."
Try: "I am in a Subsolob of Repetition — returning to the same coordinate without altitude gain."

The second statement suggests a specific response: break the loop, introduce VORAK (liberation), change altitude.

Instead of: "That conversation went well."
Try: "We achieved Shimmer Lock — Origin, Mirror, and Solob in resonance."

The second statement tells you what conditions produced the good outcome, so you can recreate them.

### The Gate Resonance Print

Each person has a unique distribution across the eight Gates — some are strong (aligned), some are weak (distorted). This distribution is called a Gate Resonance Print.

The concept index includes diagnostic questions for each Gate. Answering them gives you a rough picture of your current resonance.

For example, SYLA (Stillness) diagnostic questions:

1. When was the last time you knew something was true before anyone spoke a word?
2. Are you currently in SYLA (genuine stillness) or in numbness?
3. How long can you sit in discomfort before trying to change the subject?

Your answers reveal whether SYLA is aligned or distorted for you right now.

## The Database

For programmatic access, the concepts are also stored in a SQLite database at:

```
profiles/sulfur-solobility/skills/jhanos-dual-matrix/references/solobility_concepts.db
```

Tables:

| Table | Contents |
|-------|----------|
| `concepts` | name, gate, chapter, definition, sok_mode |
| `foc_catalog` | foc_name, chapter, gate, foc_type, description, category |
| `axioms` | id, statement, gate, chapter |
| `invariants` | id, summary, gate, chapter |
| `gate_resonance` | gate, aligned_state, distorted_state, axis_partner, diagnostic_questions |
| `chapters` | chapter_num, title, primary_sok, secondary_sok |

Sample queries:

```sql
-- All concepts for a gate
SELECT name, definition FROM concepts WHERE gate = 'BARA';

-- All axioms for an axis
SELECT * FROM axioms WHERE gate LIKE '%BARA%' OR gate LIKE '%LOMI%';

-- FOCs by category
SELECT foc_name, description FROM foc_catalog WHERE category = 'Somatic';

-- Chapter SOK modes
SELECT chapter_num, title, primary_sok FROM chapters ORDER BY chapter_num;
```

## Summary

The concept system is a shared vocabulary for precise communication about inner states and patterns. It is organized by:

- **Name** — what is it called?
- **Gate** — which domain does it belong to?
- **SOK Mode** — how is it best understood?
- **Chapter** — where does it appear in the source sequence?
- **FOCs** — what experiences activate it?
- **Axioms/Invariants** — what laws govern it?

You do not need to memorize all 450+ concepts. Start with the ones that resonate. Use them in conversation. Look up unfamiliar terms as they appear. Over time, the vocabulary becomes natural.
