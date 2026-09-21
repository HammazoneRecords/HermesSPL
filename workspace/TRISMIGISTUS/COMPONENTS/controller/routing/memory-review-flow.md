# Memory Review Flow

Controller: TRISMIGISTUS
Agent: MEMORY_CURATOR
Updated UTC: 2026-09-15T00:00:00Z

## Flow

### Tier 1 (curator autonomous — no TRIS loop)
1. Curator detects candidate (stale entry, duplicate, format issue, expired temp)
2. Curator executes action directly
3. Receipt written to `MEMORY_CURATOR/receipts/YYYY-MM-DD/`

### Tier 2 (curator executes, TRIS notified)
1. Curator identifies promotable candidate (evidence-backed, no contradiction)
2. Curator executes promotion/merge/split/add
3. Receipt written with full evidence
4. Notification appended to TRIS working plan ledger

### Tier 3 (human in the loop)
1. Curator identifies candidate requiring human judgment
2. Candidate written to `MEMORY.staged.md` with `status: pending_human`
3. Human reviews and approves/declines
4. Curator executes or archives based on decision

### Cross-tier rules
- All receipts immutable once written
- Tier 1 batches daily; Tier 2 individual receipts
- FACTCHECK pre-resolution required for Tier 2/3 claim-bearing entries
- Tris remains sole activator for cross-profile reviews (always Tier 3)
