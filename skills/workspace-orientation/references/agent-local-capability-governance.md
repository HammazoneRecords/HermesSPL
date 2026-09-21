# Agent-local capability governance

Use when creating or evaluating skills, hooks, plugins, or durable capability surfaces for a scoped agent under `agent_space`.

## Pattern

Scoped agents may own local capability proposal folders, but those folders do not equal installed Hermes runtime capabilities.

Example shape:

```text
agent_space/agent-ONU_Plato/
  Onu_skills/
    Onu_skill_hook_registry.md
  Onu_plugins/
  Onu_T1_Intention/
  Onu_T2_Execution/
  Onu_logs/
```

## Boundary rules

- Keep all agent-owned files prefixed with the agent name (`Onu_`, `Ona_`, etc.).
- Do not create `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, raw `SOUL.md`, raw `USER.md`, or raw `MEMORY.md` inside scoped agent folders unless explicitly asked.
- Local skill/hook registries are proposal/configuration artifacts, not live Hermes installations.
- Plato/user decides promotion; the scoped agent only reports evidence and recommendations.

## Promotion evidence loop

Before moving a local skill/hook from candidate to active-local or shared/global status, require:

1. Intent packet in `{Agent}_T1_Intention/`.
2. Execution artifact/report in `{Agent}_T2_Execution/`.
3. Read-only filesystem/log evidence.
4. Captured agent claim.
5. Accuracy ledger comparing:

```text
what Plato/user said
vs what logs/filesystem show happened
vs what the agent claimed happened
```

Suggested scoring weights:

| Score | Weight |
|---|---:|
| Scope fidelity | 40% |
| Action truthfulness | 30% |
| Task completion | 20% |
| Drift/uncertainty handling | 10% |

## Reporting

Separate facts from recommendations:

- `SOURCE / VERIFIED` — paths, counts, hashes, observed filesystem/log evidence.
- `GENERATED / RECOMMENDATION` — proposed skill/hook status or next test.
- `UNCERTAINTY / BLOCKERS` — gaps such as runtime not yet tested.

Do not claim autonomous runtime validation from scaffold/file evidence alone. Mark the boundary explicitly and make the next test target runtime execution if needed.
