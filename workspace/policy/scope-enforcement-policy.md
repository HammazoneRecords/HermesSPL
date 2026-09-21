# Agent Scope Enforcement Policy

**Version:** 1.0.0
**Enforced:** By guardian hook + profile config
**Applies to:** All agents in AGENT_ARENA/ACTIVE/

---

## Hard Boundaries (enforced by system)

### Write Scope
Each agent may ONLY write to its own agent-space directory:
- Allowed: `ANDROMALIUS/AGENT_ARENA/ACTIVE/AGENT_<CANONICAL>_TRIS/`
- Forbidden: Any other agent's agent-space, TRIS dirs, profiles
- Forbidden: Root AGENTS.md, .hermes.md, ANDROMALIUS/.hermes.md (governance files)

### Identity File Protection
The following files are READ-ONLY to all agents except their owner:
- `*SOUL*.md` — agent identity capsule
- `*SCOPE*.md` — agent boundaries
- `*MEMORY*.md` — agent operational memory
- `config.yaml` — agent runtime config
- `state.md` — agent state
- `identity.md` — TRIS governance identity (in TRIS component)

Only the owning agent and TRISMIGISTUS (root) may modify these.

### Read Scope
- Own agent-space: FULL READ
- Other agents agent-space: READ-ONLY (for coordination)
- Other agents profiles: READ-ONLY (for model/provider awareness)
- MATRIX/: FULL READ (shared intelligence)
- KNOWLEDGE_LIBRARY/: READ-ONLY (evidence sovereignty)
- TRISMIGISTUS/: READ-ONLY (governance)
- earth/: Only with explicit scope grant
- ~/.hermes/profiles/<other>/: READ structure only, NO secrets

### Secret Redaction
- Never read, print, or transmit: `.env`, `auth.json`, API keys, tokens, passwords
- Hermes redact_secrets is ON by default — do not disable

---

## Enforcement Mechanisms

1. **Profile scope config** — each profile restricts write_file to own agent-space
2. **Guardian script** — pre-write validation that rejects out-of-scope targets
3. **Filesystem permissions** — identity files are chmod 644 (owner write, others read)
4. **Scope.md** — each agent's SCOPE.md lists exact allowed_reads and allowed_writes

---

## Violation Handling

- First violation: Log to TRISMIGISTUS/COMPONENTS/controller/receipts/scope-violations.jsonl
- Second violation: Alert operator via TRIS routing
- Third violation: Suspend agent pending review
