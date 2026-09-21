---
name: workspace-migration-transition
description: Use when migrating or decluttering workspaces safely.
version: 1.0.0
created_by: agent
tags: [workspace, migration, declutter, pev, hermes, subagent, onu]
related_skills: [workspace-orientation, hermes-agent, obsidian]
---

# Workspace Migration / Transition

Use this skill when the user wants to move from an old cluttered workspace into a clean/current workspace, continue an unfinished move, or coordinate a scout agent for workspace transition work.

## Core posture

- **Read-only first.** Inventory and classify before changing anything.
- **Filter/isolate over delete.** A clean view is preferred to removing folders.
- **No destructive transition step without explicit scope.** Moving, deleting, replacing, or junction-cutover requires a verified source, target, plan, and user approval.
- **PEV proof is required for multi-step execution.** In `D:/MW_CENTRAL`, use `plans/` and `procedures/pev-execute.md`; done means checks returned 0 and proof files exist.
- **Do not trust visual clutter as project truth.** Hermes projects, filesystem folders, git repos, and worktrees are separate things.

## Verification sequence

1. Load `workspace-orientation` and `hermes-agent`; load `obsidian` if notes/vault routes are involved.
2. List real Hermes projects:
   - Use `desktop_project(action="list")` in the desktop app.
   - If using CLI, check `hermes project --help` first; do not guess flags.
3. Read workspace map:
   - `D:/MW_CENTRAL/AGENTS.md`
   - relevant folder `*_orientation.md`
   - `D:/MW_CENTRAL/plans/README.md`
   - `D:/MW_CENTRAL/procedures/pev-execute.md`
4. Find relevant plans under `D:/MW_CENTRAL/plans/` by parsing `plan.md` frontmatter and goals for terms like `workspace`, `drive`, `migration`, `clutter`, `adapter`, `Hermes`, `Onu`.
5. Verify filesystem reality:
   - existence and real path for old and new roots
   - `git -C <root> rev-parse --show-toplevel`
   - `git -C <root> rev-parse HEAD`
   - `git -C <root> status --short`
   - worktree list if a folder might be a worktree
   - symlink/junction status if an old path should point to a new root
6. Check model/provider state before spawning agents:
   - `hermes config get model`
   - `hermes fallback list`
   - `hermes auth list` with secret redaction
   - local caches when needed: `provider_models_cache.json`, `cache/model_catalog.json`, `models_dev_cache.json` under Hermes home.

## Onu / free-model routing notes

Prior verified environment evidence found these free model lanes:

- Current fallback: `nous` / `meituan/longcat-2.0:free`.
- Good Onu scout default: `nous` / `tencent/hy3:free` — free, reasoning-capable, tool-call-capable, long-context document/coding tasks.
- Strong structured verifier: `nous` or catalog route / `nvidia/nemotron-3-super-120b-a12b:free` — free, reasoning, tool calling, structured output, but NVIDIA free endpoints may log trial use; avoid confidential source if that matters.
- Governance/high reasoning: `opencode-free` / `nemotron-3-ultra-free` or catalog equivalent `nvidia/nemotron-3-ultra-550b-a55b:free`, with the same trial/logging caveat.
- If OpenRouter credentials are absent, do not assign OpenRouter-only routes unless a live runtime proves routing works.

For Onu read-only scouting, prefer `tencent/hy3:free` via `nous` unless the task explicitly needs structured machine output; then use `nvidia/nemotron-3-super-120b-a12b:free` only with non-confidential inputs.

## Spawning a scout

Use a bounded background process for a real independent Hermes subagent when model selection matters:

```bash
hermes -m tencent/hy3:free --provider nous --skills workspace-orientation,hermes-agent chat -Q --max-turns 12 -q "<read-only scout prompt>"
```

Prompt requirements:

- State `READ-ONLY` and `NO WRITES / NO DELETES / NO MOVES`.
- Name the workspace root and exact plans to inspect if known.
- Ask for evidence with paths, plan IDs, statuses, git heads, and uncertainty.
- Require a final JSON or compact report so the parent can monitor and compare.

Monitor with `process(action="poll"|"wait"|"log")` if spawned through `terminal(background=true, notify=true)`. Do not claim completion until the process exits or a log/proof is read.

## Report shape

Final answer should separate:

- **Source / verified:** tool-observed project list, plan statuses, path status, git status, model/auth evidence, process state.
- **Generated / recommendation:** safest next action and why.
- **Uncertainty / blockers:** missing old path, absent junction, unverified live inference, missing credentials, pending approval.

## Known MW_CENTRAL transition checkpoint (2026-08-30)

- Active Hermes project: `MIndwave_Jamaica_CENTRAL` with primary path `D:\MW_CENTRAL\playground`.
- Main workspace root exists at `D:\MW_CENTRAL` and is a git checkout.
- Legacy path `C:\Users\Owner\Desktop\MW_CENTRAL` was not present in the latest check, so the old D-drive move plan's junction task was not satisfied.
- Relevant unfinished plan: `PLN-2026-06-25-1747-workspace-d-drive-move` — Task 001 confirmed, Tasks 002-003 pending.
- Relevant completed Hermes adapter plans: `PLN-2026-08-29-1809-hermes-adapter-loop` and `PLN-2026-08-29-2125-hermes-no-mirror`.
