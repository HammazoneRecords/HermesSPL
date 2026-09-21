---
name: hermes-state-investigation
description: "Hermes state investigation: profiles, notifications, status."
version: 1.0.0
tags: [hermes, debugging, diagnostics, profile, notifications]
---

# Hermes State Investigation

Use this skill when something in Hermes behaves unexpectedly and you need to understand **what's actually configured, running, or firing underneath** — not just what the surface shows.

## Triggers

- A notification flashed in the chat area and disappeared — what was it?
- A profile's model, provider, or credentials don't match what you expected
- `hermes status` shows something worth investigating (expired auth, missing credits, stopped gateway)
- A skill is "stale" or idle and you want to know what it did (or didn't do)
- You need to verify a provider/API key actually works end-to-end

## What this skill covers

### 1. Profile review (systematic)

A Hermes profile is a self-contained instance: model, provider, credentials, skills, SOUL.md, skins, sessions, memory. Review it methodically:

```bash
# Summary
hermes profile show <name>

# Full config
hermes config show                    # open config editor
hermes config get <section.key>       # inspect one key

# Model & provider
hermes model                          # interactive picker
hermes auth list                      # see registered credentials
hermes fallback list                  # fallback chain

# Skills
hermes skills list                    # all installed
hermes skills browse                  # catalog
hermes skills inspect <ID>            # read SKILL.md
hermes curator status                 # lifecycle state

# SOUL.md (personality/rules)
read_file("<profile-home>/SOUL.md")

# Skins (theme)
hermes skin list
hermes config get display.skin
hermes skin use <name>               # switch (live repaint)
hermes skin set <key> <hex>          # tweak one color

# Sessions & memory
hermes sessions list
hermes sessions stats
hermes memory status

# Health
hermes doctor [--fix]
```

### 2. Transient notification tracing

When something flashes in the chat area and disappears, trace it end-to-end:

**Step 1 — watch the logs in real-time**
```bash
hermes logs -f          # Ctrl+C to stop
```
Notifications are logged as INFO-level events. The log will show what fired, when, and through which callback.

**Step 2 — check background review completion**
The most common transient notification is the background review finishing:
```
INFO agent.background_review: Background review complete: thread=bg-review ...
```
This runs after each turn and surfaces "💾 Self-improvement review: ..." when it finds memory/skill updates.

**Step 3 — read the notification mechanism (if logs aren't enough)**

The desktop notification system has two layers:

- **In-app toast** — `notifications.ts` store (`$notifications` atom), `notify()` function with per-kind default duration (5s for info/success, 0/sticky for error/warning), max 4 stacked, TTL auto-dismiss via `window.setTimeout(dismissNotification(id), duration)`
- **Gateway event fan-out** — `notification.show` / `notification.clear` events emitted via `emitLocalGatewayEvent()`, dispatched through `use-message-stream/gateway-event/status.ts`

**Step 4 — check curator state**
Curator manages skill lifecycle. If it's enabled but hasn't run yet, it may fire a one-time notification:
```bash
hermes curator status          # enabled? last run? stale count?
hermes curator run             # force a pass
```

**Step 5 — understand delivery paths**

- **Background review** → `background_review_callback` (Python) → `_bg_review_send()` (gateway) → `_deliver_bg_review_message()` → `ctx._status_adapter.send()` with `_interim_metadata` marker → rendered as a transient in-chat message
- **Credit notices** (Nous billing) → `agent/credits_tracker.py` → `notification.show` gateway event → `agent-notices.ts` `showAgentNotice()` → `notify()` → toast. Only `credits.depleted` and `credits.restored` break through as native OS notifications when Hermes is backgrounded (the `NATIVE_NOTICE_KEYS` set)
- **Sticky vs TTL** — `sticky` notices stay until explicit `notification.clear`; `ttl` notices self-expires after `ttl_ms`

**Step 6 — dev credit-notice demo (workspaces)**

In the Hermes desktop app (dev builds only), there's a dev trigger that exercises the production credit-notice UX without needing real billing:

- **Hotkey:** `Ctrl+Shift+C` (Windows/Linux/macOS — uses Ctrl not Cmd specifically to avoid system chord clashes)
- **Palette:** ` Cmd+K` → "Dev: cycle credit notices"
- **Console:** `window.__creditsDemo()` calls `stepCreditsNoticeDemo()`

The demo cycles through: usage 50→75→90 (same-key escalation, in-place), grant-spent, depleted (error, native OS notification), restored (success, 8s TTL auto-dismiss). It's wired through the **real** `notification.show`/`notification.clear` fan-out — not a mock — so it exercises the actual dispatcher, TTL, key-based clearing, and native notification path.

**Dev-only guard:** the demo is wrapped in `import.meta.env.DEV` (wired in `contrib/wiring.tsx`), so it does not ship in production builds.

### 3. Status diagnostics

`hermes status` surfaces the full profile state. What to watch for:

| Section | What to check | Action if flagged |
|---|---|---|
| **Nous Tool Gateway** | "no usable paid credits" → managed tools (web, image, TTS, STT, browser, Modal) unavailable | Add credits at portal.nousresearch.com/billing, then `hermes model` to refresh |
| **Auth Providers** | Expiry time (e.g. "Access exp: 2026-08-28 20:55:06") — if expired, re-auth needed | `hermes auth add <provider>` or `hermes model` |
| **API-Key Providers** | How many are set vs "not configured" | Add keys for providers you want to use |
| **Gateway Service** | "stopped" → messaging platforms inactive | `hermes gateway start` |
| **Scheduled Jobs** | 0 jobs → no cron running | `hermes cron` or `cronjob create` |
| **Sessions** | Active count | Normal to be 0 when not in a session |

### 4. Desktop UI extension points

When you need to modify the Hermes desktop app's UI — add a route, insert a sidebar nav item, contribute a page:

**Sidebar navigation structure**

The sidebar top-nav is defined in the desktop source as the `SIDEBAR_NAV` array. Display order = array order:
1. new-session (robot icon)
2. skills (symbol-misc)
3. messaging (comment)
4. artifacts (files)
5. cron (watch)

To insert a new nav item between existing entries (e.g., between messaging and artifacts), add an entry with: `id`, `label`, `icon` (Codicon name), `route` (path string), `keybindActionId` (optional).

**Route registration**

Routes are declared in the desktop source routes file:
- Route constants (e.g., `MESSAGING_ROUTE = '/messaging'`)
- `APP_ROUTES` array maps id → path → view
- `AppView` union type lists all views the workspace can show
- `AppRouteId` union type lists all route ids

Adding a route requires touching all four: the constant, the APP_ROUTES entry, and both union types.

**Contribution registry (plugin path — no core edits)**

For plugins that want to add UI without modifying core source:
- `ROUTES_AREA` ('routes') — contributes a full page in the workspace pane at a path
- `SIDEBAR_NAV_AREA` ('sidebar.nav') — contributes a sidebar nav row

Contributed sidebar rows render **after** the built-ins (below artifacts), not between them. If you need exact positioning (e.g., between messaging and artifacts), you must edit the core sidebar nav array directly.

Contribution data shapes:
- `RouteContribution { path: string }` — absolute path, one segment, no params
- `SidebarNavContribution { codicon: string, label: string, path: string }` — codicon name, label, route to navigate to

**Built vs source**

The running desktop app loads compiled files from the release folder (`release/win-unpacked/resources/app.asar.unpacked/dist/`). Source edits under `src/` do NOT affect the running app — you must rebuild (electron/native build) or edit the built output in the release folder. The built-path approach is fragile (minified, hashed filenames); the real path is edit source → rebuild → relaunch.

**Key files (desktop source)**
- Routes file — route constants, APP_ROUTES, AppView/AppRouteId unions, contribution registry areas
- Sidebar file — `SIDEBAR_NAV` array, nav item rendering, contributed nav merging
- Messaging page — template for a full-page workspace route
- Artifacts page — template for a full-page workspace route with search/pagination
- Routes test file — route coverage tests

**Key files (built output — quick edits)**
- `release/win-unpacked/resources/app.asar.unpacked/dist/app/routes.*.js` — compiled routes
- `release/win-unpacked/resources/app.asar.unpacked/dist/app/chat/sidebar/index.*.js` — compiled sidebar

### Quick edits

| Change | Command |
|---|---|
| Switch model | `hermes model` (interactive) |
| Add provider credential | `hermes auth add <provider>` |
| Change skin | `hermes skin use <name>` or `hermes config set display.skin <name>` |
| Tweak one color | `hermes skin set <key> <hex>` |
| Toggle secret redaction | `hermes config set security.redact_secrets true/false` (then `/reset`) |
| Toggle approvals | `hermes config set approvals.mode smart/manual/off` (then `/reset`) |
| Start gateway | `hermes gateway start` |
| Health check | `hermes doctor [--fix]` |
| Watch logs | `hermes logs -f` |
| Force curator pass | `hermes curator run` |

## References

- [Profile review](references/profile-review.md) — detailed profile inspection methodology with what-to-look-for table
- [Transient notification tracing](references/transient-notification-tracing.md) — full investigation workflow, mechanism deep-dive, delivery path reference
