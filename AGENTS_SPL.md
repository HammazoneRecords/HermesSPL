# HermesSPL — Self-governing Protocol Layer

**Version:** 1.0.0 (fork of hermes-agent v0.21.2)
**License:** MIT (inherited from upstream)

---

## Core Principles

1. **Protocol is the car. The model is only the driver.** (frameless)
2. **We trust the agents, but we trust the facts more.** (evidence sovereign)
3. **Not efficiency, order.** (optimize for operational order)
4. **There is always work.** (continuity under collapse)
5. **Direction greater than current state.**

---

## Agent Standard (3 Layers)

Every full agent has:
- **Mind:** TRIS component (`TRISMIGISTUS/COMPONENTS/agents/<NAME>/`)
- **Body:** Hermes profile (`~/.hermes.profiles/<name>/`)
- **Soul:** Agent-space (`ANDROMALIUS/AGENT_ARENA/ACTIVE/AGENT_<NAME>_TRIS/`)

---

## Scope Enforcement

- Agents write ONLY to their own agent-space
- Identity files (SOUL, SCOPE, MEMORY, config, state) are read-only cross-agent
- Governance files (AGENTS.md, .hermes.md) are read-only for all agents
- MEMORY_CURATOR has special write access to MEMORY.md across all agent-spaces
- Violations: 1st=log, 2nd=alert, 3rd=suspend

---

## No-Deletion Law

No agent may delete files. Archive according to workspace procedure.

---

## Model Agnostic

The protocol works with any model. Free models preferred for testing.
