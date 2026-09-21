# Spec: Dedicated Cron Activity Section

> **Status**: Draft · **Author**: HermesSPL · **Target**: Hermes Desktop + TUI

## 1. Problem Statement

When cron jobs deliver output to a chat platform (`deliver=telegram`, `deliver=bot-chat`, etc.), each run appends a message to the active conversation. With 100 cron runs, the user's chat history is flooded with 100 cron deliveries that bury real conversations.

**Current workarounds and their gaps**:

| Workaround | Trade-off |
|---|---|
| `deliver=local` | Output saved to `~/.hermes/cron/output/` but invisible — user must go hunting in the filesystem. |
| `[SILENT]` marker | Suppresses quiet runs but fails when the user *wants* to see output without chat flooding. |
| Existing `#/cron` overlay | A **job management** UI (create/edit/pause/trigger). Run history is per-job, buried behind a click, and shows only session metadata — not output preverbs or a unified activity feed. |
| Sidebar "Cron jobs" section | Shows next-run countdowns and a 5-run peek per job. Not a real activity log — no filtering, no output preview, no cross-job view. |

**The core gap**: There is no single surface that answers *"what did my cron jobs do today?"* without either (a) flooding chat or (b) opening individual job detail pages.

## 2. Proposed UI Change

### 2.1 New "Cron Activity" view (Desktop)

A dedicated panel accessible from the sidebar or as a new tab in the existing `#/cron` overlay. Two complementary surfaces:

#### A. Activity Feed (unified, cross-job)
A reverse-chronological feed of **all** cron runs across all jobs, in one scrollable list. Each row shows:

```
[status dot]  Job name              [time ago]
              └─ output preview (1–2 lines, truncated)
```

- Click a row → opens the full run output in a detail pane (or navigates to the session).
- Sticky header with filter bar (see §2.3).
- Grouped by date header (Today / Yesterday / Sep 14 / …) for scannability.

#### B. Per-job run timeline (existing `#/cron` enhancement)
The existing job-detail panel already lists runs. Enhance it with:
- Output preview inline (expandable).
- Status filter chips (ok / error / silent / running).
- Time-range selector (last 24h / 7d / 30d / all).

### 2.2 Navigation entry point

- **Sidebar**: Add a "Cron Activity" row to the sidebar nav (next to the existing "Cron jobs" section) that opens the full activity feed.
- **Existing `#/cron` overlay**: Add a top-level toggle: `[Jobs] [Activity]` so the user switches between management and monitoring without leaving the overlay.
- **Status bar**: A cron-activity unread badge (count of runs since last viewed) — opt-in via `cron.activity.unread_badge`.

### 2.3 Filters

| Filter | Type | Default |
|---|---|---|
| Job | multi-select chip list (all jobs) | All jobs |
| Status | chip toggle: `ok` / `error` / `silent` / `running` | All except silent |
| Time range | preset: 1h / 24h / 7d / 30d / custom | 24h |
| Search | free-text on job name + output content | Empty |

Filters are URL-encoded (`#/cron?activity&status=error&job=foo,bar&range=7d`) so they survive refresh and are shareable.

### 2.4 Output preview

Each run row shows a 1–2 line preview of the output. Source of truth:

1. **Preferred**: `last_output` field on the job (already persisted by the scheduler for `deliver=local` jobs).
2. **Fallback**: Read the first N characters of the run's session transcript (via existing `getSessionTranscript` API).
3. **Last resort**: Read `~/.hermes/cron/output/<job_id>/<latest>.md` (already written by `save_job_output`).

Preview is plain-text only (no markdown rendering) to keep the feed fast. Full output in the detail pane renders markdown.

## 3. Data Model

### 3.1 What the UI needs per run

```typescript
interface CronRunActivity {
  runId: string;            // execution id (uuid)
  jobId: string;            // owning job id
  jobName: string;          // human label
  profile: string;          // owning profile
  status: 'ok' | 'error' | 'silent' | 'running' | 'unknown';
  scheduledAt: string;      // ISO instant the run was due
  startedAt: string;        // ISO instant execution began
  finishedAt: string | null;
  outputPreview: string;    // first ~200 chars, plain text
  outputFormat: 'text' | 'markdown';
  deliveryTarget: string;   // 'local' | 'telegram:...' | 'bot-chat' | ...
  deliveryStatus: 'delivered' | 'unverified' | 'failed' | 'queued' | 'n/a';
  errorSummary: string | null;  // tail of error if status=error
  sessionId: string | null;     // linked chat session (if deliver != local)
}
```

### 3.2 Backend data sources (already exist)

| Field | Source |
|---|---|
| `runId`, `jobId`, `status`, `scheduledAt`, `startedAt`, `finishedAt` | `cron/executions.db` — `executions` table |
| `jobName`, `deliveryTarget` | `cron/jobs.json` — `jobs[].name`, `jobs[].deliver` |
| `outputPreview` | `jobs[].last_output` (already persisted) or `cron/output/<job>/<ts>.md` |
| `deliveryStatus` | `jobs[].last_delivery_unverified`, `jobs[].last_delivery_queued` |
| `sessionId` | `state.db` sessions where `source='cron' AND job_id=<jobId>` |

### 3.3 New backend API needed

```
GET /api/cron/activity
    ?profile=...            # optional, default 'all'
    &jobs=job1,job2         # optional filter
    &status=ok,error        # optional filter
    &range=24h              # optional, default 24h
    &limit=100              # optional, default 100, max 500
    &cursor=<opagination>   # optional, for infinite scroll

→ {
    runs: CronRunActivity[],
    nextCursor: string | null,
    total: number,           # total matching (for "showing N of M")
    byStatus: { ok: N, error: N, silent: N, running: N }  # summary for filter chips
  }
```

**Implementation**: A new module `cron/activity.py` that joins `executions.db` with `jobs.json` and projects the activity feed. No new persistence — it reads existing data.

### 3.4 New field on `CronJob` (optional, for richer previews)

Add `last_output_preview?: string` to the `CronJob` type — a truncated (~200 char) plain-text snapshot the scheduler persists alongside `last_output`. This avoids reading the full output file for the list view. Written by `save_job_output()` in `cron/jobs.py`.

## 4. Backend Requirements

### 4.1 New endpoint: `GET /api/cron/activity`

- **File**: `gateway/platforms/api_server.py` (or a new `gateway/cron_activity.py` imported by it).
- **Logic**:
  1. Parse query params (profile, jobs, status, range, limit, cursor).
  2. Query `executions.db` with the appropriate `WHERE` clauses.
  3. Join with `jobs.json` to enrich with `jobName`, `deliveryTarget`, `last_output_preview`.
  4. Compute `deliveryStatus` from job bookkeeping fields.
  5. Return paginated response.

### 4.2 New internal module: `cron/activity.py`

- Pure-read API over existing data. No side effects.
- Functions:
  - `list_activity_runs(profile, filters, cursor, limit) → ActivityPage`
  - `get_run_detail(run_id) → CronRunActivity` (single run with full output)
- Reuses `cron/executions.py` for DB access and `cron/jobs.py` for job metadata.

### 4.3 Persist `last_output_preview`

In `cron/jobs.py::save_job_output()`, after writing the full output file, also persist a truncated preview to `jobs.json`:

```python
job['last_output_preview'] = output[:200].split('\n')[0]  # first 200 chars, first line
```

This is a schema-additive change to `jobs.json` — backward-compatible (absent field → UI falls back to reading the output file).

### 4.4 `deliver=section:cron` (new delivery mode)

A new delivery target that:
- Does NOT deliver to any chat platform.
- Does NOT suppress output (unlike `[SILENT]`).
- Writes output to the activity feed only (via `save_job_output` + `last_output_preview`).
- Sets `deliveryTarget: 'section:cron'` so the activity feed can render it distinctly.

**Implementation**: In `cron/scheduler_delivery.py::_resolve_single_delivery_target()`, recognize `deliver=section:cron` as a no-op target (like `local`) but tag the job's `last_run.delivery_target` as `section:cron` for the activity feed.

## 5. Minimal Implementation Plan

### Phase 1: Read-only activity feed (no core changes)

**Effort**: ~2 days. Uses only existing data.

1. Add `cron/activity.py` — read-only query layer over `executions.db` + `jobs.json`.
2. Add `GET /api/cron/activity` endpoint to `api_server.py`.
3. Add `getCronActivity()` to `apps/desktop/src/api/cron.ts`.
4. Add "Activity" tab to the existing `#/cron` overlay (`apps/desktop/src/app/cron/index.tsx`).
5. Render feed with filters (job, status, time range).
6. Click row → open existing session detail (reuse `PanelDetail`).

**Verification**: `hermes cron list` shows jobs; the new endpoint returns the same runs enriched with metadata. Manual test: fire 5 jobs, confirm they appear in the activity feed with correct status.

### Phase 2: Output previews + unread badge

**Effort**: ~1 day.

1. Persist `last_output_preview` in `save_job_output()`.
2. Surface preview in feed rows.
3. Add unread badge to sidebar nav (count runs since `last_viewed_at`, persisted to profile config).

### Phase 3: `deliver=section:cron` delivery mode

**Effort**: ~1 day.

1. Add `section:cron` to the recognized delivery tokens in `scheduler_delivery.py`.
2. Treat it as a no-op for actual delivery but tag the run.
3. Update the delivery-target checkbox group to offer "Activity feed only" as an option.
4. Document in `website/docs/guides/automate-with-cron.md`.

### Phase 4: TUI parity (optional)

**Effort**: ~2 days.

1. Add a `:cron-activity` command to the TUI that renders a textual activity feed.
2. Reuse the same `/api/cron/activity` endpoint.
3. Filter via command flags (`--status=error --range=7d`).

## 6. What Can Be Done NOW vs. What Needs Core Hermes Changes

### Can be done NOW (HermesSPL fork, no upstream changes)

| Item | Where |
|---|---|
| Read-only activity feed UI | `apps/desktop/src/app/cron/` |
| `cron/activity.py` query layer | `cron/activity.py` (new, in-fork) |
| `GET /api/cron/activity` endpoint | `gateway/platforms/api_server.py` (fork already has custom endpoints) |
| `last_output_preview` persistence | `cron/jobs.py` (fork already patches jobs.py) |
| Activity tab in `#/cron` overlay | `apps/desktop/src/app/cron/index.tsx` |
| Sidebar nav entry point | `apps/desktop/src/app/chat/sidebar/` + `routes.ts` |

### Needs upstream Hermes core changes

| Item | Why |
|---|---|
| `deliver=section:cron` token recognition | `cron/scheduler_delivery.py` is core; the SPL fork can patch it but upstream should adopt for consistency. |
| `CronRunActivity` type in `@hermes/shared` | The shared types package is upstream-owned. Fork can use a local type but divergence risk. |
| `last_output_preview` in `CronJob` type | Same — the `CronJob` type lives in `@hermes/shared`. |
| TUI `:cron-activity` command | TUI is upstream-owned (`ui-tui/`). |

### Recommended sequencing

1. **Fork-only first**: Build Phase 1 + 2 entirely in the SPL fork. Ship it. Get user feedback.
2. **Upstream PR**: Once validated, PR the `deliver=section:cron` token and the `CronRunActivity` / `last_output_preview` type additions to upstream Hermes.
3. **TUI**: Only if users ask for it.

## 7. Out of Scope (intentionally)

- **Run retries from the activity feed** — the feed is read-only. Retries are a management action, stay in the Jobs tab.
- **Live tailing of running jobs** — too complex for v1. The feed refreshes on `cron.changed` event or 8s poll.
- **Aggregated cron analytics** (success rate, avg duration) — v2 feature. The `byStatus` summary in the API response lays the groundwork.
- **Deleting/pruning run history** — the executions DB already prunes terminal states at 1000 rows. No UI needed.

## 8. Success Criteria

- [ ] A user with 50 cron jobs can see all runs from the last 24h in a single scrollable list.
- [ ] The list loads in < 500ms for 500 runs (pagination + indexed queries).
- [ ] Filtering by status and job updates the list without a full refetch (client-side cache).
- [ ] `deliver=section:cron` jobs never appear in any chat but are fully visible in the activity feed.
- [ ] The activity feed does not increase chat session count (no new sessions created for `section:cron` runs).
