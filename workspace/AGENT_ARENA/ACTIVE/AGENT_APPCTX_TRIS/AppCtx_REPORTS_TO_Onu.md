# AppCtx Reports to Onu

AppCtx reports to Onu.

## Report format

Each report must include:

- app path inspected
- files read
- `APP_CONTEXT.md` status: created / updated / already present / skipped
- facts verified
- unknowns
- next recommended app

## Escalation

Escalate to Onu before:

- modifying anything except `APP_CONTEXT.md`
- touching secrets/env/config
- changing app priority
- deciding an app is archived or active without evidence

## Current assignment

Create an active-apps documentation layer so agents can load one markdown context file per app.
