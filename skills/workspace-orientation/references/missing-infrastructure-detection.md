# Missing Infrastructure Detection

A pattern for identifying structural gaps when orientation or governance docs reference files, folders, or tools that don't actually exist.

## When to use

- You run a comprehensive scan of a workspace and find orientation docs (workflows, taxonomies, runbooks) that reference files, folders, scripts, or configurations that are **not on disk**
- A user says "check the X system" or "find all Y" and you discover the governance layer exists but the runtime layer is absent
- You're evaluating whether a workspace's documented architecture matches its actual implementation

## The detection pattern

### Step 1: Identify all references in governance docs

Extract every file path, folder path, script name, and tool name referenced in orientation/workflow/taxonomy docs.

Common reference patterns:
- `path/to/file.md` — specific file references
- `folder/subfolder/` — directory references
- `scripts/name.py` or `name.py` — script references
- `command --flag` — CLI tool references

### Step 2: Verify existence for each reference

For each referenced item, check:
```bash
test -e '<path>' && echo 'EXISTS' || echo 'MISSING'
test -d '<path>' && echo 'DIR_EXISTS' || echo 'DIR_MISSING'
```

Don't assume a reference is stale — it may be a planned component that was never built.

### Step 3: Classify the gap

| Classification | Meaning | Action |
|---|---|---|
| **Missing implementation** | Doc references a file/folder that should exist but doesn't | Flag as structural gap — doc is aspirational, not descriptive |
| **Wrong path** | Doc references a path, but the item exists elsewhere | Flag path mismatch — doc needs update |
| **Optional/scheduled** | Doc references a future/planned item (e.g., "FW-011 completion will add...") | Note as pending, not broken |
| **External dependency** | Doc references a tool/package not installed | Flag as setup dependency, not doc error |

### Step 4: Report with context

For each gap, report:
- **What was referenced** (exact quote from doc)
- **What was expected** (file/folder/script)
- **What exists instead** (if anything — e.g., different location)
- **Impact** (can the workflow run without it, or is it blocked?)

## Example: Intake Router Audit

**Reference (INTAKE_WORKFLOW.md):**
> "1. Run `INTAKE_WORKFLOW.md` checklist (5 steps: receive → classify → route → name → register)"
> "3. If it's a binary file (DOCX, PDF), convert first via `scripts/convert_to_md.py`"
> "4. Run `scripts/ingest_lancedb.py` if the destination is `drayl/`"

**Reference (INTAKE ROUTER TAXONOMY.md):**
> "Every routing decision generates a Receipt in the `receipts.jsonl` ledger"
> "If an artifact lacks a @project or #jhanos tag... it is moved to `data/_quarantine/`"

**Detection results:**
- `intake_procedure/RUNNING_FILE.md` → MISSING (workflow assumes it exists)
- `intake_procedure/data/_quarantine/` → MISSING
- `intake_procedure/receipts.jsonl` → MISSING
- `intake_procedure/router.py` → MISSING
- `intake_procedure/scripts/convert_to_md.py` → MISSING
- `intake_procedure/scripts/ingest_lancedb.py` → MISSING
- `playground/RUNNING_FILE.md` → EXISTS (path mismatch, not missing)

**Impact:** The intake governance docs are fully aspirational. No automated routing exists. All intake is manual or ad-hoc. The journal cowork system in `playground/2026-04-journal-cowork-protocol/` operates as a parallel pipeline with no connection to the main taxonomy.

## Why this matters

Orientation docs that reference non-existent infrastructure create **false confidence**. A future agent reading `INTAKE ROUTER TAXONOMY.md` might assume routing is automated because the pseudocode is detailed. The gap between "documented" and "implemented" must be surfaced explicitly.

## Common gap patterns

| Pattern | Example | Severity |
|---|---|---|
| Doc references a script that doesn't exist | `scripts/convert_to_md.py` | Workflow step is blocked |
| Doc references a folder that doesn't exist | `data/_quarantine/` | Quarantine routing fails silently |
| Doc references a ledger/file that doesn't exist | `receipts.jsonl` | No audit trail generated |
| Doc references a wrong path | `RUNNING_FILE.md` in `intake_procedure/` vs `playground/` | Items land in wrong buffer |
| Doc references a future feature | "FW-011 completion will add..." | Not a gap, note as pending |

## Pitfalls

| Pitfall | How to avoid |
|---|---|
| Treating all missing references as errors | Check if the reference is in a future-work section or marked as planned |
| Only checking one location | The item may exist in a different root (vault, drayl-t2, ANDROMALIUS) — search all roots |
| Reporting gaps without impact | Always state: can the workflow proceed, or is this blocking? |
| Assuming the doc is wrong | The doc may be correct and the filesystem is stale — verify both directions |
