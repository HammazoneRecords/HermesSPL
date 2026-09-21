# Comprehensive Workspace Search Technique

A repeatable methodology for thorough text searches across complex multi-location workspaces.

## When to use

- User asks to "search everywhere", "find all references to X", "check the whole workspace"
- The workspace has multiple roots (e.g., `D:\MW_CENTRAL`, `D:\MW_CENTRAL\drayl-t2`, `C:\Users\Owner\Videos\Drayl2`, `D:\MW_CENTRAL\ANDROMALIUS`)
- The search term has known variants, derivatives, or conceptual relatives
- First-pass results feel incomplete or the user pushes back ("that can't be")

## Before a blanket search for a referenced artifact — ask first

When the user references a specific document or location by name ("the runbook", "the earth folder") and a targeted name/file lookup comes up empty, do NOT escalate straight to a recursive grep across the entire workspace root — especially not across hidden state dirs (`~/.hermes`, `.git`) or large generated trees (`vault/.../dist`). That scan is slow, floods results with irrelevant hits (novel chapters, node_modules, build output), and usually the user can name the location faster and cheaper than a full-tree sweep. Ask the user where the thing lives; if they point at a path, verify that path directly.

Reserve the exhaustive multi-pass methodology below for when the user explicitly asks to "search everywhere" or "find all references", and then still exclude state/dependency/dist trees from the scan unless the question demands them.

## The methodology

### Pass 1: Bare term, primary locations

Search the obvious term across all workspace roots:

```
search_files(pattern="vine", path="D:\MW_CENTRAL")
search_files(pattern="vine", path="D:\MW_CENTRAL\drayl-t2")
search_files(pattern="vine", path="C:\Users\Owner\Videos\Drayl2")
```

Report what you find. If the user pushes back or results feel thin, proceed to Pass 2.

### Pass 2: Expanded patterns, all locations

Expand the search to catch:
- **Plurals/derivatives**: `vines`, `vineyard`, `vined`, `vine-like`, `vine's`
- **Case variations**: `Vine`, `VINE`
- **Related/conceptual terms**: `whisk`, `wiss` (for vine); `sequenced`, `sequencing`, `sequential`, `consequence`, `subsequence`, `chain`, `cascade`, `series`, `progression` (for sequence)
- **Hidden/gitignored directories**: Check `ANDROMALIUS/`, `_Hermes_Route/`, `.gitignored` dirs that may contain mirrors

```
search_files(pattern="vines|vineyard|vined|vine-like|vine's", ...)
search_files(pattern="sequenced|sequencing|sequential|consequence|...", ...)
search_files(pattern="whisk|wiss", ...)
```

### Pass 3: Verify against known mirrors

Many workspaces have mirrored content across locations. Check:
- Is the same file present in multiple roots? (e.g., vault file mirrored in `drayl-t2/drayl_journal/`)
- Are there extraction/index files that reference the term? (e.g., `relationships_map.md`, `drayl-pattern-analysis.md`)
- Are there technical/code files that use the term in a different domain? (e.g., `active_apps/` using "sequence" for auth flows)

## Reporting structure

When reporting multi-pass search results:

1. **Organize by location** — group findings under each root path
2. **Include line numbers** — every reference gets a line number for traceability
3. **Quote the context** — show enough surrounding text to understand the usage
4. **Flag conceptual relatives** — explicitly note when a term is related but not identical (e.g., "vine" appears as substring of "divine" — NOT a vine reference)
5. **Build a conceptual map** — show how the terms relate to each other (e.g., whisk→wiss→vine, sequence→consequence→chain)
6. **Summarize counts** — give a table of references by location and term

## Common pitfalls

| Pitfall | How to avoid |
|---------|--------------|
| Only searching the primary workspace | Always check all roots: `MW_CENTRAL`, `drayl-t2`, vault, `ANDROMALIUS`, `active_apps` |
| Missing plural/derivative forms | Use regex alternation: `vines|vineyard|vined` |
| Missing conceptual relatives | Think about etymology and domain-specific synonyms (wiss→vine, consequence→sequence) |
| Substring false positives | Flag when a term appears as a substring of a larger word (vine in divine, sequence in consequence) and explicitly exclude or categorize separately |
| Ignoring hidden directories | ANDROMALIUS, `_Hermes_Route`, and gitignored dirs often contain mirrored/derived content |
| Stopping at pass 1 | Always do at least a second pass with expanded patterns when the user asks for "everywhere" or "all references" |

## Example: Vine + Sequence search

**Pass 1** (bare term): Found 7 "vine" matches — all substrings of "divine". Found 2 "sequence" matches.

**User**: "that can't be"

**Pass 2** (expanded): Found 26+ vine references, 77+ sequence references, 28+ consequence references across all locations.

**Key discoveries from pass 2**:
- Today's journal entry (Aug.30.26) introducing vine as "sequential memory network"
- DRAYL EXCAVATION files documenting the whisk→wiss→vine etymological discovery
- "Law of sequential confirmation" in Apr.21.26 and Aug.24.25
- Plato notes on "promotion chain" and "restore continuity into main chain"
- Technical sequence usage in `active_apps/` (cashpot, chat2cash)

This methodology turned an apparent empty result into a comprehensive map of the concept across the entire workspace.
