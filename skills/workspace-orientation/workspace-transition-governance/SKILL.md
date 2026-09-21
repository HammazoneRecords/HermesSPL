---
name: workspace-transition-governance
description: Use when transitioning a workspace safely.
version: 1.0.0
created_by: agent
tags: [workspace, migration, transition, inventory, agents, rag, verification]
related_skills: [workspace-orientation, workspace-migration-transition]
---

# Workspace Transition Governance

Use this skill when a recovered, cluttered, or cross-machine workspace must be reorganized without losing continuity. The goal is a functional after-state, not merely a smaller folder tree.

## Core rules

- **Simulate before moving.** Before moving one file, know what it would take to move every file class: source, reflection, app, archive, dependency, cache, build output, generated index, private ops, and unknown.
- **Treat recovered workspaces as evidence first.** Baseline and route before normalizing paths, reinstalling dependencies, deleting caches, or resuming feature work.
- **Observed action does not define motive.** A file/folder existing proves only that it exists; do not infer why it was created unless a source states the reason.
- **Functional after-state beats survival.** Files should have role, route, staging state, RAG car, rebuildability status, rollback, and verification path.
- **Movement needs explicit authorization.** A route ledger or simulation is not permission to move/delete/edit.
- **Use trash as quarantine, not deletion.** When the user asks to clear files with no live purpose, create an in-scope trash/quarantine folder, move only obvious low-risk artifacts first, and write a manifest so every move is reversible.
- **Derive quarantine scope from names, not only from the inspected path.** If a requested folder name contains a project/root signal such as `pluto_TRASH`, place it at that named root; stop and confirm when the inspected subfolder and the name-implied root disagree, because generic “trash under current folder” behavior can mis-scope the move.

## Procedure

1. **Find and freeze the current body.** Identify the exact workspace root and archive sources. Write a landing receipt with path, archive/source location, size, and a clear no-move state.
2. **Build a complete baseline manifest.** Record every file with current path, size, extension/format, category, and location. If old file indexes exist, compare file counts and bytes against the new baseline so the story has before/now context.
3. **Classify top-level routes before any move.** Produce an ownership matrix for H1 human source, H2 reflection, H3 system/agent files, active apps, cold archive, rebuildable dependencies, private ops, and unknown/Jhanos X.
4. **Create a route ledger.** Every route entry needs current path, role, after-state group, stage, candidate RAG car, rebuildability, movement type, prerequisites, rollback, verification, approval status, and continuity risk.
5. **Define move classes.** Use staged classes instead of ad-hoc commands: metadata/reference only; external store creation; rebuildable dependency externalization; stage-copy; archive/cold movement. If the task is a light cleanup, start with unambiguous backups/caches/generated debris and leave canonical docs, adapters, templates, manifests, and logs in place unless their role is disproven.
6. **Write a move manifest for quarantine work.** Before creating the quarantine folder, report the inspected path, action root, quarantine root inferred from the folder name, and whether those roots match. For every move into a trash/quarantine folder, record source path, destination path, reason, timestamp, and scope policy; verify the active-tree count after moving rather than relying on visual inspection.
7. **Prepare external stores before dependency cleanup.** Keep source, lockfiles, route notes, and manifests in the workspace. Put rebuildable package stores, caches, venvs, model/build artifacts, and generated bundles in a separate data root after approval.
7. **Route RAG by classified area.** Never broad-ingest the workspace. Use separate cars such as app registry, per-app codebase, agent governance, personal legacy, reflection, private ops metadata, archive catalog, source library, and Jhanos review.
8. **Verify every movement class.** Run after-transition indexes and compare before/after. Every missing path must be explained as intentionally moved, externalized/rebuildable, archived with receipt, excluded as generated/cache, or held in Jhanos X; anything else is potential loss.
9. **Maintain an efficacy overview.** During long transitions, keep an hourly or recurring overview that shows agent relationships, task progress, artifact paths, issues/successes, morale/temperament as interpretation, what-if scenarios, next action, and explicit move authorization state.

## Agent status protocol

For multi-agent transitions, each agent or scout should publish a compact status record with: agent name, mode, current focus, tasks with status/priority/scope/evidence/blockers/next action, risks, user-decision needs, last artifact, and explicit `move_authorized`. The team lead uses these records for a high-level board rather than reading every report.

## Vault/archive handling

Treat vault/archive folders as black-box evidence first. Catalog archive metadata before extraction; never extract into the vault itself. Moving something out of active interpretation is not the same as deleting evidence. Archive contents become RAG sources only after provenance and sensitivity review.

## Hindsight reports for RAG cars

When a task exposes a missing tool, source, protocol, or prerequisite, write a hindsight report that states the starting state, friction encountered, missing asset, difficulty caused by the missing asset, current temperament compared to task start, and what would help next time. Do not merely list that a tool was missing; explain the operational cost of its absence.

## Target structure preferences

When the user asks to reorganize a folder tree, these standing preferences shape the proposed after-state (surface them for sign-off, do not silently assume them):

- **Route to a single canonical home — no neutral/orphan pile.** The aim is a two-domain split (e.g. canon/reflection/business on one root, agent-space/governance/protocol on another). Cross-domain material is routed to its owning domain, not left in a staging folder. Ambiguous cross-domain placement is a decision to surface and get answered, not a default.
- **An empty folder is a defect, not a neutral state.** It means the work missed something or there is an unseen blind spot. Determine what belongs there or archive it — never leave an empty folder standing as if it were structure.
- **Numbered-prefix top-level scheme** (`01_CANON/`, `02_REFLECTION/`, `03_WORK/`, ...) is the preferred grouping — stable and self-ordering.
- **Naming must say what is inside.** A folder/file name that no longer matches its content is naming drift — rename or re-home it, do not leave a divergent or typo-ridden name. One name per concept (e.g. `mw-session-close.md`, never a parallel `session-close.md`). A file whose name lies about its state (`FLAWS.md` when all flaws are resolved) gets renamed to match reality. This user checks for it and corrects it: fix drift on sight, do not wait to be told.
- **Flatten single-child wrappers.** A folder holding exactly one inner folder (`ACTIVE_APPS/active_apps/`) is a useless layer; promote the inner folder and archive the empty wrapper.
- **Archive stale duplicates and retired wrappers, never delete.** Duplicate app copies and retired folders go to an archive/quarantine with a manifest, not the trash.
- **Fix pointers as part of the move.** After moving or renaming a canonical file/folder, sweep every wrapper, index, bridge, and skill that referenced the old path and repoint it, then grep for the old path and confirm zero dead references remain. A move that leaves dangling pointers is half-done.

## Consolidating a duplicated charge

When the same "charge" (procedures, configs, an index, a running log) exists in two places, consolidate to ONE canonical root instead of leaving two sources of truth:

1. Pick one canonical root and copy+verify there (file count and byte-hash match).
2. Standardize the name — one name per concept; rename drift on sight.
3. Fix every pointer/reference to the old location (skill wrappers, bridges, indexes, READMEs) and grep to confirm zero dead references.
4. Archive the old copies to vault with a receipt recording before/after counts — never delete.
5. Retiring adapters (per-IDE wrappers) means the charge lives once in the canonical root; the adapters are archived, not maintained.

## Reconciling a numbered running list

When a running log (`FW-NNN` style) has two distinct entries accidentally sharing one ID, do not merge them and do not drop one — a duplicate ID is a numbering collision, not proof of duplicate content (confirm the titles differ first):

1. Extract the colliding second-occurrence blocks (by heading line span), leaving the first in place.
2. Verify the remaining IDs are unique.
3. Renumber the extracted blocks with fresh IDs and append them at the end.
4. Add a `Renumbered from: <old-id>` trace line on each so lineage survives.
5. Re-verify: total entries unchanged, zero duplicate IDs.

## Reserved-file flow audit

Before archiving files in a reorganized folder, determine whether each is part of the active flow rather than deleting or leaving orphans:

- Grep the governing procedures/skills for references to each filename (and its underscore/hyphen variants).
- In-flow → keep.
- A stray single-entry file whose content belongs inside a canonical log → merge into the log, then archive the stray.
- An orphan whose managing script no longer exists on disk → archive it (or move it to the owning domain if still live, e.g. a live VPS runbook belongs under the VPS folder, not the orphaned scripts folder).

Every file ends up either in the active flow or in the vault — nothing orphaned in place.

## Pitfalls

- Do not run global dependency cleanup because a category is large; dependency externalization must be app-by-app with lockfile, rebuild command, approval, and verification.
- Do not treat vector databases, generated RAG indexes, manifests, or cached outputs as primary sources; route them as generated artifacts unless provenance says otherwise.
- Do not mix H1/H2 personal source with H3 agent/system material in one RAG car without explicit boundary labels.
- Do not infer agent/user motive from observed file changes or command logs; separate observed action, stated intent, inferred motive, and outcome.
- Do not activate write-capable agents until their read scope, write scope, forbidden surfaces, allowed RAG cars, and evidence-citation rules are explicit.
- Do not move canonical procedure files just because backup copies exist nearby; first confirm the canonical file has a named role in an index, adapter map, template list, or active procedure system.
- Do not let a cleanup subpath silently become the quarantine root; compare the trash/quarantine name against ancestor folder names and use the ancestor when the name clearly points there, because this user's folder names often encode scope boundaries.
