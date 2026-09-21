# AppCtx Model Lock

Status: active
Agent: AppCtx
Reports to: Onu

## Assigned model

Task type: active-apps documentation, extraction, context writing
Provider/model: `deepseek-v4-flash-free` (provider `opencode-free`)
Reason: model matrix recommends `deepseek-v4-flash` for data extraction and Patois/Jamaican code-work backup. The free route is `deepseek-v4-flash-free` on `opencode-free` — the bare `deepseek-v4-flash` resolves to the PAID deepseek API, which we avoid.

## Concurrency rule

Only one active instance of `deepseek-v4-flash-free` should run at a time across scoped agents unless Onu/Plato explicitly approves an exception.

## Release condition

When AppCtx finishes a work session, write a release receipt under `AppCtx_logs/` before another agent uses `deepseek-v4-flash-free`.
