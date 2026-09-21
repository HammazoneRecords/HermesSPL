# Onu — state.db and Sessions Surface

**Locations:**
- `C:\Users\Owner\AppData\Local\hermes\state.db`
- `C:\Users\Owner\AppData\Local\hermes\sessions\`

**Layer:** 5 — live session state  
**Source session:** @session:default/20260829_002402_0d4c7d

## Role

`state.db` stores sessions, messages, search index, delegations, and Lane A summaries. `sessions/` stores gateway routing, request dumps, and JSONL transcripts.

## Onu rule

Read through `session_search`, Hermes CLI, or controlled SQLite inspection. Do not directly mutate `state.db` or session files.
