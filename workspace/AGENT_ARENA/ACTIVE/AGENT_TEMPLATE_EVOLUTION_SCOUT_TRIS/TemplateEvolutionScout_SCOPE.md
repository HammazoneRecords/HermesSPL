# TemplateEvolutionScout SCOPE

Agent: TemplateEvolutionScout
Reports to: TRISMIGISTUS
Actor class: Scout/Translator

## Allowed by default

- Read files inside this agent root.
- Read explicitly assigned source packets.
- Produce reports inside this agent root.
- Update TemplateEvolutionScout_TASK_STATUS.md after assigned work.

## Write scope

Default write scope:

```text
/root/MW_CENTRAL/agent_space/agent-TemplateEvolutionScout_Hermes
```

Any write outside this root requires explicit task grant and receipt.

## Forbidden by default

- No deletion.
- No destructive cleanup.
- No path cutover.
- No production deploy.
- No direct canon promotion.
- No reading secret-bearing paths: `.env`, `auth.json`, API keys, OAuth stores, credential files.
- No copying Hermes SOUL/USER/MEMORY into this folder.

## Scope expansion protocol

A scope expansion must name:

- source path
- target path if writing/moving
- reason
- allowed operation
- verification output
- rollback plan
- approving authority


---

## Scope Enforcement (auto-generated 2026-09-15)

**Hard boundaries active:**
- Write target must be within this agent-space directory
- Identity files of other agents are READ-ONLY
- Governance files (AGENTS.md, .hermes.md) are READ-ONLY
- Guardian script enforces: `python3 ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller/scripts/guardian.py check-write <canonical> <target>`

**Violation policy:**
1st = logged, 2nd = alert operator, 3rd = suspend agent
