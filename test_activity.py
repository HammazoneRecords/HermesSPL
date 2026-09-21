#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/MW_CENTRAL/TRIANGULUM/hermes-spl-fork')
from cron.activity import list_activity_runs, get_run_detail
r = list_activity_runs(range_hours=720, limit=3)
print("total:", r["total"], "byStatus:", r["byStatus"])
if r["runs"]:
    run = r["runs"][0]
    print("first:", run["jobName"], run["status"], "preview_len:", len(run["outputPreview"]))
    detail = get_run_detail(run["runId"])
    if detail:
        print("detail OK: fullOutput len =", len(detail.get("fullOutput", "")))
