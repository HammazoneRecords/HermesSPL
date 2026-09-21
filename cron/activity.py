"""Read-only activity feed query layer over executions.db + jobs.json.

Provides the data for the Cron Activity section: a unified, cross-job,
reverse-chronological feed of all cron runs. Pure-read — no side effects,
no mutations. Reuses cron/executions.py for DB access and cron/jobs.py for
job metadata.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from cron.executions import list_executions, get_execution


def _resolve_status(exec_status: str, delivery_outcome: Optional[str]) -> str:
    """Map execution status + delivery outcome to activity status token."""
    if exec_status == "completed":
        if delivery_outcome == "failed":
            return "error"
        return "ok"
    if exec_status == "failed":
        return "error"
    if exec_status == "running":
        return "running"
    if exec_status == "claimed":
        return "running"
    return "unknown"


def _compute_delivery_status(
    job: Dict[str, Any], exec_record: Dict[str, Any]
) -> str:
    """Compute delivery status from job + execution record."""
    delivery_outcome = exec_record.get("delivery_outcome")
    if delivery_outcome == "delivered":
        return "delivered"
    if delivery_outcome == "failed":
        return "failed"
    if job.get("last_delivery_unverified"):
        return "unverified"
    if job.get("last_delivery_queued"):
        return "queued"
    return "n/a"


def list_activity_runs(
    *,
    jobs_filter: Optional[List[str]] = None,
    status_filter: Optional[List[str]] = None,
    range_hours: int = 24,
    limit: int = 100,
    cursor: Optional[str] = None,
    profile: Optional[str] = None,
) -> Dict[str, Any]:
    """Return paginated activity feed runs enriched with job metadata.

    Response shape:
    {
      runs: CronRunActivity[],
      nextCursor: str | null,
      total: int,
      byStatus: { ok: N, error: N, silent: N, running: N, unknown: N }
    }
    """
    # Build job lookup (only jobs we care about if filtering)
    try:
        from cron.jobs import load_jobs

        all_jobs = load_jobs()
    except Exception:
        all_jobs = []

    job_map: Dict[str, Dict[str, Any]] = {}
    for job in all_jobs:
        job_id = job.get("id", "")
        if not job_id:
            continue
        if jobs_filter and job_id not in jobs_filter:
            continue
        job_map[job_id] = job

    # Compute time cutoff
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=range_hours)
    cutoff_iso = cutoff.isoformat()

    # Query executions — over-fetch so we can filter down
    try:
        all_execs = list_executions(limit=max(limit * 3, 500))
    except Exception:
        all_execs = []

    runs: List[Dict[str, Any]] = []
    by_status: Dict[str, int] = {
        "ok": 0, "error": 0, "silent": 0, "running": 0, "unknown": 0,
    }

    for exec_record in all_execs:
        job_id = exec_record.get("job_id", "")
        job = job_map.get(job_id)
        if not job:
            continue

        # Time filter — claimed_at is ISO 8601 string
        claimed_at = exec_record.get("claimed_at", "")
        if claimed_at < cutoff_iso:
            continue

        status = _resolve_status(
            exec_record.get("status", "unknown"),
            exec_record.get("delivery_outcome"),
        )

        # Status filter
        if status_filter and status not in status_filter:
            continue

        by_status[status] = by_status.get(status, 0) + 1

        runs.append({
            "runId": exec_record.get("id", ""),
            "jobId": job_id,
            "jobName": job.get("name") or job_id,
            "profile": job.get("profile", "default"),
            "status": status,
            "scheduledAt": exec_record.get("scheduled_instant") or claimed_at,
            "startedAt": exec_record.get("started_at", ""),
            "finishedAt": exec_record.get("finished_at"),
            "outputPreview": job.get("last_output_preview") or "",
            "outputFormat": "text",
            "deliveryTarget": job.get("deliver", "local"),
            "deliveryStatus": _compute_delivery_status(job, exec_record),
            "errorSummary": exec_record.get("error"),
            "sessionId": None,
        })

    total = len(runs)
    runs = runs[:limit]

    return {
        "runs": runs,
        "nextCursor": None,
        "total": total,
        "byStatus": by_status,
    }


def get_run_detail(run_id: str) -> Optional[Dict[str, Any]]:
    """Return a single run with full output for the detail pane."""
    exec_record = get_execution(run_id)
    if not exec_record:
        return None

    try:
        from cron.jobs import load_jobs

        all_jobs = load_jobs()
    except Exception:
        all_jobs = []

    job = None
    for j in all_jobs:
        if j.get("id") == exec_record.get("job_id"):
            job = j
            break

    if not job:
        return None

    # Try to read the latest output file for full output
    output_preview = job.get("last_output_preview") or ""
    full_output = output_preview

    try:
        from cron.jobs import get_cron_output_dir

        output_dir = get_cron_output_dir() / job.get("id", "")
        if output_dir.exists():
            files = sorted(output_dir.glob("*.md"), reverse=True)
            if files:
                full_output = files[0].read_text(
                    encoding="utf-8", errors="replace"
                )[:10000]
    except Exception:
        pass

    return {
        "runId": exec_record.get("id", ""),
        "jobId": job.get("id", ""),
        "jobName": job.get("name") or job.get("id", ""),
        "profile": job.get("profile", "default"),
        "status": _resolve_status(
            exec_record.get("status", "unknown"),
            exec_record.get("delivery_outcome"),
        ),
        "scheduledAt": exec_record.get("scheduled_instant")
        or exec_record.get("claimed_at", ""),
        "startedAt": exec_record.get("started_at", ""),
        "finishedAt": exec_record.get("finished_at"),
        "outputPreview": output_preview,
        "outputFormat": "markdown",
        "deliveryTarget": job.get("deliver", "local"),
        "deliveryStatus": _compute_delivery_status(job, exec_record),
        "errorSummary": exec_record.get("error"),
        "sessionId": None,
        "fullOutput": full_output,
    }
