# Onu — Agent Space Operating Rules

**Location:** `D:\MW_CENTRAL\agent_space\`  
**Status from thread:** under evaluation as possible agent-memory root  
**Source session:** @session:default/20260829_002402_0d4c7d

## Current role

`agent_space` is a legacy/agent workspace containing active tool code, policy references, project memory, and historical artifacts. The thread explicitly says it must be inventoried deeply before being treated as a memory root.

## Rules for Onu

1. Every new Onu file in this folder starts with `Onu_`.
2. No deletion or destructive cleanup without explicit scope.
3. Do not import secrets or raw Hermes credentials.
4. Do not treat generated notes as human source.
5. Keep Onu working memory separate from Plato canon and User H1.
6. Prefer small route/index documents over full corpus copies.
7. Version scripts before edits.
8. If an item is uncertain, mark it under review instead of canonical.
