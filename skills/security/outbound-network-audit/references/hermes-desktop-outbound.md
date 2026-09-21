# Hermes Desktop — Outbound Network Audit (findings)

Concrete findings from auditing the installed Hermes desktop app + agent backend
(source at `~/AppData/Local/hermes/hermes-agent/` on Windows). Re-verify against
the live source — paths/versions move.

## Source layout (Windows)
- Python core: `~/AppData/Local/hermes/hermes-agent/`
  - `hermes_cli/` — CLI, web server, config, observability, banner/update check
  - `agent/` — agent runtime, relay_runtime, monitoring (OTLP exporter)
  - `plugins/` — platform adapters + optional third-party plugins
- Electron desktop: `apps/desktop/`
  - `src/` — React renderer (chat surface)
  - `electron/` — native main process (updater, OAuth, plugin install)

## Outbound paths (non-model), by trigger

### AUTOMATIC — the only one
- **Update check** — `hermes_cli/banner.py:413` `check_for_updates()`; cached 6h
  (`_UPDATE_CHECK_CACHE_SECONDS`), result in `~/.hermes/.update_check`.
  - `git ls-remote https://github.com/NousResearch/hermes-agent.git refs/heads/main`
  - `GET https://api.github.com/repos/NousResearch/hermes-agent/compare/<cur>...<target>`
    with `User-Agent: hermes-cli-update-check` (`banner.py:216-222`).
  - **Sends only**: local git revision SHA in URL + generic UA. No install_id,
    no account, no content. Skipped for docker/apt installs (`banner.py:437`).

### OPT-IN, OFF by default
- **Shared metrics** — `telemetry.shared_metrics.enabled: false` in both
  `config.yaml` and `config_defaults.py:3471`. Local-only when on: writes
  `~/.hermes/telemetry/shared_metrics/metrics.sqlite3` + exports JSON deltas to a
  LOCAL `outbox/` dir. Docstring: *"Collection is opt-in and no remote sink
  exists."* (`hermes_cli/observability/shared_metrics.py`).
- **NeMo Relay exporters (OTLP)** — only activate via explicit `plugins.toml`
  (`agent/relay_runtime.py:1983`); none ships by default. `nemo_relay` is NVIDIA's
  local agent-runtime binding, not a telemetry beacon.
- **Gateway monitoring / OTLP** — `monitoring.gateway_health_export.enabled:
  false`, `monitoring.export.otlp.enabled: false` + empty endpoint
  (`config_defaults.py:3119-3148`). Docstring: *"No default destination ships"*
  (`agent/monitoring/otlp_exporter.py:9`). Content-free (no prompts/messages).
- **install_id** — local pseudonymous UUID (`~/.hermes/install_id`);
  "carries no account identity"; only attached to OTLP signals if monitoring is
  enabled (`agent/monitoring/policy.py`). Not sent otherwise.

### USER-INITIATED only
- OAuth/auth: `portal.nousresearch.com` + provider endpoints (`electron/native-oauth.ts`).
- Plugin/extension installs: VS Code marketplace
  (`marketplace.visualstudio.com/_apis/public/gallery/extensionquery`),
  `raw.githubusercontent.com`, `hermes-agent.nousresearch.com/install.sh`.
- Messaging adapters (Telegram/Discord/Slack…) — only when the gateway is configured.

## What does NOT exist
- No analytics/attribution SDK (Sentry/Posthog/Mixpanel/Amplitude/Datadog/beacon).
  The only "sentry"/"datadog" strings are MCP-catalog entries in
  `apps/desktop/src/lib/mcp-directory.ts` (servers you *could* install) + an
  OTLP-exporter comment.
- Project policy bans un-gated telemetry: root `AGENTS.md` contribution rubric
  lists *"Outbound telemetry / usage attribution without opt-in gating"* as
  rejected.

## Flag worth surfacing
- STT enabled with `local.model: base` (local Whisper) → audio transcribed
  locally. `openai.model: whisper-1` is an available alternative — if the user
  ever switches STT to OpenAI, audio leaves the machine (a model call, but a
  distinct privacy surface).

## Key file:line anchors
- `hermes_cli/banner.py:413` — update check entry; `:216-222` — GitHub UA/URL.
- `hermes_cli/config_defaults.py:3471` — telemetry default off; `:3119-3148` — monitoring/OTLP off.
- `hermes_cli/observability/shared_metrics.py` — local SQLite + outbox (no remote sink).
- `agent/monitoring/otlp_exporter.py:9` — "no default destination ships".
