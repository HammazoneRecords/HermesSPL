---
name: outbound-network-audit
description: Audit an app's outbound traffic besides its primary job.
---

# Outbound Network / Privacy Surface Audit

Determine what an application or agent actually phones home, **apart from its
primary job** (for an LLM agent, that means apart from model calls). The user
is security-conscious: they want exact file:line evidence, an honest statement
of what is *proven by code inspection* vs *proven at runtime*, and a clean
categorization of every outbound path.

## When to use
- "does X send anything out besides Y" / "is X phoning home" / "what telemetry
  does this app have" / privacy-audit requests.
- Before adopting a new tool into a trust boundary (agent-space, coordinator,
  anything with secrets).

## Methodology (ordered)

1. **Locate the real source, not the cwd.** Installed apps do not live in your
   working directory. For Hermes: `~/AppData/Local/hermes/hermes-agent/`
   (Windows) holds the Python core + `apps/desktop/` (Electron renderer in
   `src/`, native main process in `electron/`). Find it with a targeted
   `find`/`ls` before grepping anything.

2. **Enumerate the endpoint surface fast.** In the source tree:
   `grep -rhoE "https?://[a-zA-Z0-9./_-]+" --include="*.ts" .` (add `*.py`,
   `*.tsx` as needed). Then filter test fixtures out of the count — they
   dominate raw URL greps:
   `example.com / *.example / .test / .invalid / localhost / 127.0.0.1 /
   RFC5737 ranges (10.x, 192.168.x, 100.x) / placeholder hosts`.

3. **Search for the behavior, not just URLs.** Plain-token alternation, not
   regex — see pitfalls: `telemetry|analytics|update_check|sendBeacon|beacon|
   sentry|posthog|mixpanel|amplitude|datadog|crash.*report`.

4. **Read BOTH the config defaults and the live config** for every telemetry/
   monitoring knob. A feature defaulting to `false` can still be `true` in the
   user's `config.yaml`. Check `config_defaults.py` (or equivalent) AND the
   installed config file. The docstring/comment next to the default is often
   the authoritative statement of sink behavior (e.g. "no remote sink exists").

5. **Classify every call site** by two axes:
   - **Trigger**: automatic (fires on startup/interval) vs opt-in (off by
     default, needs config) vs user-initiated (auth, plugin install).
   - **Payload**: does it send a stable identifier (install_id), content
     (prompts/messages), or only incidental data (git SHA + User-Agent)?

6. **Distinguish local sink from remote sink.** A SQLite DB or an "outbox"
   directory is NOT a network call. A local outbox + "no remote sink" means
   data stays on the machine. Only an exporter with a configured endpoint
   leaves the box.

## Pitfalls

- **`search_files` mangles regex.** Patterns with `(` / `\(` / `?` produce rg
  "unclosed group" or "regex parse error". Use simple plain-token alternation
  (`fetch|axios|telemetry`) instead.
- **Do NOT wrap `search_files` in `execute_code` for large outputs.** The
  wrapper JSON-parses the result and dies with `JSONDecodeError: Extra data`
  when output is big/truncated. Call `search_files` directly.
- **Test files pollute every grep.** Always exclude `*.test.ts`, `*.spec.ts`,
  `e2e/`, `node_modules`, `dist`. Otherwise you'll report Sentry/Datadog/analytics
  "findings" that are actually test fixtures or an MCP catalog entry.
- **"Analytics" hits are often local.** `@app.get("/api/analytics/usage")` is a
  local dashboard endpoint, not outbound. Read the route before flagging it.
- **A library's SDK ≠ your app using it.** A third-party optional plugin may
  bundle posthog/segment (e.g. mem0); that's the *dependency's* code, only
  active if that plugin is installed AND configured. Say so, don't overclaim.

## Verification (gold standard)

Code inspection proves intent, not behavior. When the user wants certainty,
offer a **live packet capture** of the running app (watch its actual
connections while idle and under use) and diff it against the code-derived
list. State clearly in the report which claims are code-proven vs runtime-proven.

## Reporting conventions for this user

- Cite **exact file:line** (`hermes_cli/banner.py:413`), never vague module names.
- Lead with a one-line verdict, then the categorized list.
- Explicitly separate: **automatic / opt-in (off by default) / user-initiated**.
- For each path state **what it sends** and **where**, not just "it phones X".
- Be honest about scope: "no analytics SDK found in code" ≠ "nothing is sent".

See `references/hermes-desktop-outbound.md` for the concrete Hermes findings
from a full audit (endpoints, config knobs, file:line map).
