# Lane A Context Engine — Version Note

## v1.0.0 (current, backed up)
**Path:** `C:/Users/Owner/AppData/Local/hermes/plugins/lane-a-context-engine/`
**Backup:** `D:/MW_CENTRAL/agent_space/lane-a-context-engine-v1-backup/`
**Config:** `context.engine = lane-a-engine`

### What it does
- Wraps built-in `ContextCompressor`
- Emits transient notifications at 50% and 60% context full
- Stores summaries to SQLite `lane_a_summaries` table
- Has placeholder for arbelos/manji geometry-aware partitioning

### Known issues
- Threshold config expects list of floats `[0.5, 0.6]` but config.yaml stores list of objects `[{ratio: 0.5, message: "..."}]`
- No pin-aware compression
- No memory bank / data dump
- No retrieval mechanism
- No `select_context()` implementation
- No `on_turn_complete()` implementation
- No agent-callable tools for pin management

---

## v2.0.0 (in development)
**Path:** `D:/MW_CENTRAL/agent_space/lane-a-context-engine-v2-dev/`

### Goals
1. Pin-aware compression with integrity checks
2. Memory bank (read-only auto-retrieved context)
3. Data dump (archived compressed-out info)
4. Context-aware retrieval via `select_context()`
5. Agent-callable tools: `context_pin`, `context_unpin`, `context_search_memory`, `context_search_dump`, `context_promote`
6. SQLite storage for pins, memory bank, data dump, compression events, integrity reports
7. Fix threshold config parsing
