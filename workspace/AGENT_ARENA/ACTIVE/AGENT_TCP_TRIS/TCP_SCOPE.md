# TCP SCOPE

**Agent:** TCP
**Reports to:** H1 (peer of Plato)

---

## Allowed by default

- Read/write TCP-prefixed files inside `agent-TCP_H1`.
- **View (read-only) Plato's surfaces and actions** — peer right, so TCP can record governance decisions in the timeline.
- Read bounded, Plato/H1-assigned source routes for formalization (once scope is granted).
- Produce timeline nodes, concept docs, topic-tag maps inside `TCP_Drayl/`, `TCP_T2_Execution/`.

## Forbidden by default

- **No scanning `drayl-t2`, Obsidian `Drayl2`, or Shadow Drayl0 until model selection is locked.** (Hard block — see `TCP_state.md`.)
- No **writes** outside `agent_space` — writes stay in the agent world. Viewing Plato's territory is a read right, not a write right.
- No deletion, destructive cleanup, or path cutover.
- No secret files: `.env`, `auth.json`, API keys, credential stores.
- No direct promotion to canon (Plato and H1 promote).

## The agent-world boundary (verbatim directive)

> "agent space is the agent world. All agent actions should be taken there. No agent should work on any file directly outside of that space. Outside that space is Plato territory."

**Refinement (verbatim, later):** TCP is "on the same level as Plato, so it can view Plato actions." So the boundary is asymmetric for TCP: **writes** stay inside `agent_space`; **reads** may extend to Plato's governance surfaces as a peer, so the timeline captures the whole system, governor included.

## Peer-vs-subordinate distinction

| | Onu | TCP |
|---|---|---|
| Reports to | Plato | H1 (peer of Plato) |
| Role | scout forward | reconstruct backward |
| Views Plato actions | no (scoped) | **yes (peer)** |
| Writes | Onu folders only | agent_space only |


---

## Scope Enforcement (auto-generated 2026-09-15)

**Hard boundaries active:**
- Write target must be within this agent-space directory
- Identity files of other agents are READ-ONLY
- Governance files (AGENTS.md, .hermes.md) are READ-ONLY
- Guardian script enforces: `python3 ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller/scripts/guardian.py check-write <canonical> <target>`

**Violation policy:**
1st = logged, 2nd = alert operator, 3rd = suspend agent
