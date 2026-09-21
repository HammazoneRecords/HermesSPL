# Script Discovery and Documentation Pattern

This reference captures the three-layer pattern for documenting workspace scripts so an agent can discover, understand, and use them without loading everything into context at once. The user identified this as the "first skill is survival" — an agent must know what it can do before it can do anything.

## Trigger

When a workspace has many scripts/utilities and the agent needs to:
- Discover what tools are available for a task
- Understand a script's purpose without reading the full source
- Track version history, issues, and fixes
- Map user intent (keywords) to the right script

## The Three Layers

### Layer 1: YAML Header (Synopsis)

Every script gets a compact header block at the top (after shebang if present):

```python
#!/usr/bin/env python3
# PURPOSE: Extract chat transcripts from Claude/Cline/VSCode into lean markdown corpus
# VERSION: 1.2.0
# STATUS: working
# ISSUES:
#   v1.0.0 — initial release
#   v1.1.0 — added streaming line-by-line for 260MB+ JSONL files
#   v1.2.0 — added venv noise filter, fixed regex newline bug
# TRIGGERS: chat, corpus, transcript
```

**Fields:**
- `PURPOSE`: One-line description of what the script does
- `VERSION`: Semver
- `STATUS`: `working`, `broken`, `experimental`
- `ISSUES`: Version history with bug fixes and changes
- `TRIGGERS`: 3+ comma-separated keywords that map user intent to this script

**Why YAML-style comments instead of actual YAML:** The header lives inside a Python file, so it must be comments. The structure is machine-parseable with simple regex (`^# PURPOSE:`, `^# VERSION:`, etc.) but also human-readable.

### Layer 2: Per-Script Notes (Comprehensive Docs)

Each script has a dedicated notes file in `agent_space/mw.script-notes/<script-name>.md`:

```markdown
# extract_chat_corpus.py — Script Notes

> **PURPOSE:** Extract chat transcripts from Claude/Cline/VSCode into lean markdown corpus
> **VERSION:** 1.2.0
> **STATUS:** working
> **TRIGGERS:** chat, corpus, transcript

## Synopsis

Extracts lean, searchable text from local AI chat stores (Claude Code JSONL, Cline tasks, VS Code empty-window sessions). Streams line-by-line to handle 260MB+ files. Redacts secrets inline.

## Version History

- v1.0.0 — initial release
- v1.1.0 — added streaming line-by-line for 260MB+ JSONL files
- v1.2.0 — added venv noise filter, fixed regex newline bug

## Imports

`json`, `re`, `sys`, `pathlib`

## Functions

- `redact()`
- `extract_content_blocks()`
- `process_claude_jsonl()`
- `process_cline_task()`
- `process_emptywindow_jsonl()`
- `main()`

## Usage

```bash
python scripts/extract_chat_corpus.py
```

## Related

- See script header for quick reference
- See this file for comprehensive docs
```

**Why separate notes files:** The agent can load just the synopsis (Layer 1) for quick reference, or load the full notes file when it needs comprehensive understanding. This avoids loading all documentation into context at once.

### Layer 3: Index in SOUL.md / AGENTS.md

A compact index in the agent's always-loaded context file:

```markdown
# SCRIPT INDEX — Survival Kit

> One-line reference for all scripts. Load individual notes from `agent_space/mw.script-notes/<script>.md` for full docs.

| Script | Purpose | Triggers |
|--------|---------|----------|
| `extract_chat_corpus.py` | Extract chat transcripts from Claude/Cline/VSCode | `chat, corpus, transcript` |
| `detect_patterns.py` | Session log pattern detector | `pattern, session, detect` |
| `vape_check.py` | MW Variable Truth Tree Verifier | `vape, verify, truth` |

## Trigger → Script Lookup

> When user mentions these keywords, check the corresponding script notes first.

- **chat** → `extract_chat_corpus.py`, `scan_chats_for_patois.py`
- **patois** → `patois_chat_scan.py`, `scan_chats_for_patois.py`
- **verify** → `vape_check.py`, `chat2cash_verify_submission_reset.py`
- **pattern** → `detect_patterns.py`
```

**Why in SOUL.md/AGENTS.md:** This file is always loaded into context. The agent can see all available scripts + their triggers without any additional tool calls. When a user says "scan chats for patois", the agent knows exactly which script to use.

## Workflow: Adding a New Script

1. Create the script with Layer 1 header (PURPOSE, VERSION, STATUS, ISSUES, TRIGGERS)
2. Create Layer 2 notes file in `agent_space/mw.script-notes/<script>.md`
3. Add row to Layer 3 index in SOUL.md/AGENTS.md
4. Add trigger keywords to the Trigger → Script Lookup section

## Workflow: Using a Script

1. User makes a request
2. Agent checks Layer 3 index (always in context) for matching triggers
3. If match found, agent loads Layer 2 notes via `read_file` for full docs
4. Agent runs the script via `terminal`

## Workflow: Fixing a Bug

1. Fix the bug in the script
2. Add new entry under `# ISSUES:` in Layer 1 header (e.g., `#   v1.2.1 — fixed off-by-one in line counting`)
3. Update Layer 2 notes with the fix details
4. Layer 3 index stays the same (purpose hasn't changed)

## Future Enhancement: Trigger Keyword Expansion

The `TRIGGERS` field can be expanded by analyzing chat corpus for keywords that always accompany certain requests. For example:
- User says "mine chats" → `mine_tasks.py`
- User says "check drift" → `check_procedure_drift.py`
- User says "pull Last.fm" → `pull_lastfm.py`

A future version of `skill_candidate_detector.py` can scan the chat corpus for these keyword→script mappings and auto-populate the trigger index.

## Pitfalls

- **Don't put all docs in the script header** — keep it to one line. Full docs go in the notes file.
- **Don't skip the TRIGGERS field** — this is how the agent discovers the script from user intent.
- **Don't let the index drift** — when you add a new script, update all three layers immediately.
- **Don't use separate notes files for every tiny utility** — only scripts that are non-trivial (50+ lines, complex logic, or frequently used) need full notes.

## Example: Full Three-Layer Implementation

See `D:\MW_CENTRAL\scripts\extract_chat_corpus.py` (Layer 1), `D:\MW_CENTRAL\agent_space\mw.script-notes\extract_chat_corpus.py.md` (Layer 2), and `D:\MW_CENTRAL\agent_space\SCRIPT_INDEX.md` (Layer 3) for a complete example.
