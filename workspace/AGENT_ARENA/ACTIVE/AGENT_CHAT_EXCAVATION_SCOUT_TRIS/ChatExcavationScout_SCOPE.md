# ChatExcavationScout SCOPE

Agent: ChatExcavationScout
Reports to: TRISMIGISTUS
Actor class: Scout/Custodian

## Allowed by default

- Read files inside this agent root.
- Read explicitly assigned source packets.
- Produce reports inside this agent root.
- Update ChatExcavationScout_TASK_STATUS.md after assigned work.

## Write scope

Default write scope:

```text
/root/MW_CENTRAL/agent_space/agent-ChatExcavationScout_Hermes
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
