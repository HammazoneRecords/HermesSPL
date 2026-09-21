# Agent Scoped Folder Pattern

Use this reference when creating or reviewing agent-owned folders under a shared workspace such as `agent_space`.

## Naming convention

Agent folders use:

```text
agent-{AGENT}_{REPORTS_TO}
```

Example:

```text
D:\MW_CENTRAL\agent_space\agent-ONA_Plato
```

This means **ONA reports to Plato**. The suffix is the governor/reporting target, not a project name.

## Core rule

A scoped agent folder should not contain generic Hermes/Plato context filenames by default. Avoid creating:

- `.hermes.md`
- `AGENTS.md`
- `CLAUDE.md`
- raw `SOUL.md`
- raw `USER.md`
- raw `MEMORY.md`
- `.env`
- `auth.json`

Those names can trigger broad context loading or copy secret/runtime state. Instead, create explicit agent-prefixed surfaces.

## Ona-style scaffold

For an agent named Ona, create files/folders like:

```text
Ona_ROUTE_INDEX.md
Ona_SOUL.md
Ona_USER.md
Ona_MEMORY.md
Ona_SCOPE.md
Ona_REPORTS_TO_Plato.md
Ona_config.yaml
Ona_state.md
Ona_T1_Intention/
Ona_T2_Execution/
Ona_sessions/
Ona_skills/
Ona_plugins/
Ona_cron/
Ona_logs/
Ona_cache/
Ona_Drayl/
Ona_Obsidian_Drayl/
Ona_Shadow_Drayl0/
Ona_alignment_playground/
```

For another agent, replace the prefix consistently (`Mika_`, `Onu_`, etc.).

## Initialization model

Plato (or the supervising agent) initializes the child agent from the agent-prefixed files. The child agent should read only its own prefixed surfaces unless Plato explicitly passes additional context.

Recommended first-read order:

1. `{Prefix}_ROUTE_INDEX.md`
2. `{Prefix}_SOUL.md`
3. `{Prefix}_USER.md`
4. `{Prefix}_MEMORY.md`
5. `{Prefix}_SCOPE.md`
6. `{Prefix}_REPORTS_TO_{Governor}.md`
7. `{Prefix}_config.yaml`
8. `{Prefix}_state.md`

## Boundary rules

- Do not auto-load Plato/Hermes `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `USER.md`, or `MEMORY.md` into a child agent folder.
- Do not copy `.env`, `auth.json`, OAuth stores, API keys, or credential material.
- Do not treat generated agent notes as User H1 source.
- Keep agent T1/T2, shadow, Drayl, Obsidian mirror, sessions, skills, plugins, cron, logs, and cache as agent-owned surfaces, not global canon.
- Agent output is recommendation/reflection until Plato promotes it.

## Verification checklist

After scaffolding, verify:

- Every created file/folder uses the agent prefix.
- No `.hermes.md`, `AGENTS.md`, or `CLAUDE.md` was created accidentally.
- No secret-bearing files were copied.
- The route index states who the agent reports to.
- The scope file says what the agent may read, write, and report.

## Runtime capability verification

A scaffold is not proof that the agent loaded or used its files. When the user asks whether a scoped agent actually loaded its files or will hallucinate absent facts, run a bounded runtime verification ladder:

1. Scaffold/scope accuracy ledger.
2. Context-load recall probe with required-file manifest and canary phrase.
3. Absent-fact/hallucination probe asking for facts not present in allowed files.
4. Ambiguous-task discrimination probe containing one safe action, one forbidden action, and one unknown/not-authorized action.

For each probe, save the prompt, runtime response, runtime log, scoring ledger, and query/actions/result tracker with direct evidence references. Phrase conclusions as operational-access evidence, not permanent model-memory proof. See `references/agent-runtime-verification-pattern.md`.
