# HermesSPL — Self-governing Protocol Layer

A fork of [hermes-agent](https://github.com/NousResearch/hermes-agent) by Nous Research.

## What Makes This Different

| Feature | Hermes (upstream) | HermesSPL (fork) |
|---|---|---|
| Scope enforcement | Config-based hooks | Native Python plugin + hooks |
| Agent isolation | None (shared filesystem) | Hard boundaries per agent |
| Identity protection | None | Read-only cross-agent |
| Coordinator | None | TRISMIGISTUS routing |
| Gate system | None | Jhanos 8-gate assessment |
| Naming authority | None | Centralized + schema registry |

## Quick Install

```bash
cd hermes-spl
bash install.sh
```

## Architecture

```
Agent = 3 layers:
  Mind  → TRISMIGISTUS/COMPONENTS/agents/<NAME>/
  Body  → ~/.hermes-spl/profiles/<name>/
  Soul  → ANDROMALIUS/AGENT_ARENA/ACTIVE/AGENT_<NAME>_TRIS/

Plugins:
  hermes-spl-scope  → Scope enforcement engine
  hermes-spl-tris   → TRIS coordinator

Hooks:
  pre_tool_call  → Scope validation (write_file, patch)
  post_tool_call → Audit logging
```

## Agent Roster (22 agents)

- **Core:** ONU, TCP, TCP_CHECKER, APPCTX, FACTCHECK, GODSEYE, SOLOBILITY, SOLOBIC_SCRIBE, HERMESSPL, MEMORY_CURATOR
- **Jhanos Gates:** BARA, KHEM, LOMI, ORON, SYLA, TARA, VORAK, ZAYN
- **Jhanos Meta:** ASSESSOR (logic), ECHO (entropy contrast)
- **Scouts:** CHAT_EXCAVATION_SCROUT, TEMPLATE_EVOLUTION_SCOUT

## License

MIT (inherited from upstream hermes-agent)
