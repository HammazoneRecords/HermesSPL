---
name: workspace-transition-simulation
description: Use when simulating workspace moves before edits.
version: 1.0.0
created_by: agent
tags: [workspace, migration, transition, simulation, inventory, rag, staging, recovery]
related_skills: [workspace-orientation, workspace-migration-transition, agent-system-scaffolding]
---

# Workspace Transition Simulation

Use this skill when a recovered, migrated, cluttered, or cross-machine workspace must be reorganized without breaking continuity. The job is to define the after-state and simulate the transition before moving files.

## Core rule

Before moving one file, know what it would take to move all file classes.

```text
Do not take the first step until the whole path can be mentally walked.
```

This does not mean every file must move. It means every class of file must have a route, staging state, requirements, risk, rollback, and verification story before any real movement begins.

## Procedure

1. **Declare read-only mode.** Do not move, delete, normalize, reinstall, or rewrite project files during discovery.
2. **Find the exact recovered root.** Verify path existence and record the source archive/download path when available.
3. **Write receipts outside the recovered workspace.** Create a landing receipt and cold-archive receipt with exact paths, size, timestamp, and `no edits yet` status.
4. **Run complete baseline inventory.** Record current location, size, extension/format, category, top-level folder, and total counts. Save a manifest and summary outside the recovered workspace.
5. **Search for prior self-observation artifacts.** Look for file lists, mtime summaries, compare reports, manifests, inventory outputs, and workspace watcher outputs. Compare prior totals to the new baseline; treat old Windows paths as historical, not live.
6. **Create an ownership matrix.** Classify top-level paths as H1 source, H2 reflection, H3 system/agent, active app, archive, rebuildable dependency/cache, generated output, or unknown.
7. **Create a RAG/staging matrix.** Assign candidate RAG cars and ACT/STAGE/DECLINE/SHARE/JHANOS_X state. A functional after-state requires role, route, RAG car, staging state, and rebuildability status — not merely smaller size.
8. **Define dependency/binary externalization policy.** Workspace stores source, specs, manifests, and lockfiles; external stores hold rebuildable dependencies, caches, binaries, model files, package stores, and build artifacts.
9. **Scaffold a transition architect when needed.** The architect is read-only: it defines the desired after-state, notifies blind spots, and emits a dry-run transition ledger.
10. **Simulate before execution.** The dry-run ledger must include current path, proposed group, staging state, candidate RAG car(s), rebuildability, continuity risk, prerequisites, rollback path, verification, and `move_authorized: false`.
11. **Mitigate blind spots.** Do not approve a move class while any high-risk path involved in that move remains unknown, mixed-source, security-sensitive, or JHANOS_X.
12. **Request explicit approval for one move class.** Move only the smallest reversible class after baseline + after-state spec + dry-run ledger + blind-spot mitigation + rollback path + approval all exist.
13. **Verify and compare after-state.** Re-run the same inventory after approved moves and write a transformation diff showing what moved, stayed, shrank, externalized, or remained held.

## File class requirements

Every transition item needs:

- current exact path
- current role: source, reflection, app, agent-space, archive, dependency, cache, build output, generated output, unknown
- proposed after-state group: Earth/H1-H2, Pluto/H3, Active Apps, Cold Archive, External Rebuildable Store, Jhanos X Hold
- staging state: ACT, STAGE, DECLINE, SHARE, JHANOS_X
- candidate RAG car(s) or `none`
- rebuildability: source, generated, dependency, cache, archive, unknown
- reference impact and path assumptions
- continuity risk and confusion risk
- prerequisites
- movement type: leave-in-place, reference-only, stage-copy, externalize, archive, hold
- rollback path
- verification command/report
- approval status

## RAG/staging rules

- H1/H2 personal source and reflection can feed personal legacy, Solobility, philosophy, reflection, or pre-frontal-vortex RAG only after provenance/status is visible.
- H3 agent/system material feeds agent-governance or HermesSPL RAG; keep it separate from H1 human source.
- Active apps feed app-registry and per-app codebase RAG; separate source/lockfiles from dependencies and build outputs.
- Ops/VPS material is private and secret-safe only; never broad-ingest secrets or environment dumps.
- Cold archives feed no RAG by default; route by provenance after review.
- Unknown or mixed folders go to JHANOS_X until classified.
- Generate hindsight reports for RAG/transition work when missing prerequisites are discovered. Do not merely list what was missing; state the difficulty caused by each missing asset and compare the current temperament/state to the task-start state.

## Vault and archive handling

Treat archive/vault areas as black-box evidence, not cleanup targets. Moving an archive into a vault is a preservation act; extracting it or interpreting it is a separate, later step.

- Catalog archives metadata-first: path, size, type, source relation, historical period, hash/receipt need, and whether represented elsewhere.
- Do not extract archives into the vault itself; extract only to an approved temporary/staging location.
- Do not broad-ingest vaults or archives. Use an archive catalog RAG for metadata, and route selected source documents only after provenance and sensitivity checks.
- For workspace recovery, keep a stable archive as proof before sculpting the working copy.

## Hindsight report shape

When a transition, archive recovery, RAG build, or digitization task reveals missing prerequisites, write a short hindsight report with:

- task-start state and temperament,
- friction encountered,
- missing assets or knowledge,
- difficulty caused by each missing asset,
- current state compared with the start,
- what would assist if known before,
- updates needed to RAG cars, protocols, or agents.

A good hindsight report says how not having the screwdriver changed the job, not just that a screwdriver was needed.

## Pitfalls

- Do not treat survival as organization; files existing does not mean they have a functional route.
- Do not clean dependencies globally; app dependencies are rebuildable only when lockfiles and rebuild commands are verified per app.
- Do not scan archives, mirrors, generated corpora, or dependency trees as canonical source for themselves; this creates recursion and false authority.
- Do not move personal/vault material before H1/H2/H3 boundaries are explicit; mixing source, reflection, and system rules creates continuity confusion.
- Do not use old Windows paths as live paths after Linux restore; compare them as historical evidence and translate only through an explicit route map.
- Do not let a transition architect become a mover; it must write designs, simulations, and approval queues only.
- Do not optimize for smallest size alone; dependency/background removal is like removing a green screen around the artwork, and the irreplaceable source/provenance must remain intact.

## Report shape

Final reports should separate:

- **Source / verified:** exact root, archive paths, baseline counts, prior-index comparison, paths inspected, generated report paths.
- **Generated / recommendation:** proposed after-state, RAG/staging matrix, dependency externalization strategy, next safe move class.
- **Uncertainty / blockers:** JHANOS_X paths, unclassified folders, missing prior indexes, unverified rebuild commands, pending approvals.

Include a short before/now/after storyboard when recovering from a crash or migration: what prior indexes say existed, what the current baseline proves exists, and what after-state the simulation proposes.
