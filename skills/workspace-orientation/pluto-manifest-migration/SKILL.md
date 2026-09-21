---
name: pluto-manifest-migration
description: Manage Pluto staging with manifests and hash proof.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [pluto, manifests, migration, hashes, lane-a, folder-purity]
    related_skills: [workspace-orientation, hermes-spl-governance]
---

# Pluto Manifest Migration Skill

Use this skill when staging, admitting, copying, moving, or verifying folders/files into the Pluto workspace.

Pluto is the workspace house. Y-MINDWAVE is the route/junction. This skill protects the system from recursion, silent source mutation, hashless moves, unmanifested files, and folder-purity drift.

## When to Use

- User asks to move/copy/stage/admit files or folders into `D:\MW_CENTRAL\ANDROMALIUS`.
- User asks whether staged folders have manifests.
- User asks to update or verify Pluto manifests.
- User asks to map external source roads into H1/H2/H3 or Lane A destinations.
- User asks to proceed with Lane A migration or Pluto road creation.

Do not use this for unrelated file edits outside the Pluto migration context.

## Prerequisites

Known Pluto root:

```text
D:\MW_CENTRAL\ANDROMALIUS
```

Known route/junction:

```text
D:\MW_CENTRAL\ANDROMALIUS\Y-MINDWAVE
```

Manifest system paths:

```text
D:\MW_CENTRAL\ANDROMALIUS\Y-MINDWAVE\H3_SYSTEM\00_MANIFESTS\00_MAIN\main_manifest.md
D:\MW_CENTRAL\ANDROMALIUS\Y-MINDWAVE\H3_SYSTEM\00_MANIFESTS\02_REGISTRY\manifest_of_manifests.md
D:\MW_CENTRAL\ANDROMALIUS\Y-MINDWAVE\H3_SYSTEM\00_MANIFESTS\03_HASHES\manifest_hashes.md
D:\MW_CENTRAL\ANDROMALIUS\Y-MINDWAVE\H3_SYSTEM\06_SCRIPTS\01_TOOLS\update_pluto_manifests.py
D:\MW_CENTRAL\ANDROMALIUS\Y-MINDWAVE\H3_SYSTEM\06_SCRIPTS\01_TOOLS\verify_pluto_manifests.py
```

Before editing these scripts, version them first.

## Core Rules

1. **No source mutation.** User H1/source files are read-only to Plato, Shadow, Onu, Dream, and route processes.
2. **No blind moves.** Never move/copy/delete/retire a source road without explicit scope and approval.
3. **Stage folder before file.** If a file is selected for staging, stage/register its containing folder first unless the folder is unsuitable or meaningless.
4. **Hash before and after.** Before any file move/copy: hash source; after move/copy: hash destination; confirm only if hashes match exactly.
5. **Manifest every Pluto folder.** Every folder under Pluto must have a folder manifest listing direct files/subfolders.
6. **External hashes.** Registered manifest hashes live in `manifest_hashes.md`, not as fake self-hashes inside each manifest.
7. **No exclusions.** Updater/verifier must report `unmanifested_folders=0` and `unmanifested_files=0`.
8. **Folder purity.** A Pluto folder must not contain both direct files and direct subfolders.
9. **No recursive corpus.** Do not recreate the deleted corpus or scan generated route output as H1.
10. **Lane A first.** Lane A governance/adapter/checklist must remain verified before Lane B migration or fork work.

## Procedure

### 1. Classify the request

Determine whether the user is asking for:

- assessment only;
- route/index creation;
- source-road staging;
- actual file/folder migration;
- manifest refresh;
- verifier repair.

Completion criterion: the response path is classified as ACT, STAGE, DECLINE, or assessment-only.

### 2. Check current manifest state

Run with `terminal`:

```bash
python 'D:/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/Y-MINDWAVE/H3_SYSTEM/06_SCRIPTS/01_TOOLS/verify_pluto_manifests.py'
```

Completion criterion: verifier output is captured. If it fails, fix manifest logic or stale manifests before claiming the system is clean.

### 3. For staging, register the containing folder

If the user names a file, identify its containing folder first. Stage or map the folder unless:

- the file is directly at a root with no meaningful container;
- the container is too broad/unsafe;
- a narrower Pluto destination is clearly more suitable.

Completion criterion: the folder/source road and proposed Pluto destination are written to the appropriate route/index/manifest note.

### 4. Before editing migration scripts, version them

Run with `terminal` using a UTC timestamp and copy the script to a `.bak-<timestamp>` file in the same folder.

Completion criterion: backup files exist before the edit.

### 5. For actual copy/move, use hash proof

Before copy/move:

1. compute SHA-256 for each source file;
2. record exact source path and destination path;
3. copy/move only the approved scope;
4. compute SHA-256 for each destination file;
5. compare source/destination hashes;
6. fail the migration if any hash differs;
7. keep the old road until explicitly retired.

Completion criterion: every moved/copied file has matching source and destination SHA-256.

### 6. Refresh manifests after any Pluto change

Run with `terminal`:

```bash
python 'D:/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/Y-MINDWAVE/H3_SYSTEM/06_SCRIPTS/01_TOOLS/update_pluto_manifests.py'
python 'D:/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/Y-MINDWAVE/H3_SYSTEM/06_SCRIPTS/01_TOOLS/verify_pluto_manifests.py'
```

Completion criterion: verifier returns:

```text
VERIFY_STATUS=PASS
unmanifested_folders=0
unmanifested_files=0
folder_purity_violations=0
```

### 7. Report exact state

Report:

- files/folders created;
- files/folders moved/copied, if any;
- manifest counts;
- hash proof status;
- excluded file/folder count;
- folder-purity result;
- old roads retired or preserved.

Completion criterion: final answer distinguishes staged/proposed paths from actually migrated/admitted paths.

## Pitfalls

- A Pluto destination folder existing does not mean migration is complete.
- A route/index file is not the same as source admission.
- Manifest files are self-referential; keep manifest hashes in the separate hash file.
- Do not treat generated manifests, route files, or context packets as external H1.
- Broad folders like `procedures`, `scripts`, `drayl_brainstorms`, and `drayl_journal` need subfolder/file-role maps before migration.
- If updater finds unmanifested files, treat it as a real blocker and fix coverage before proceeding.
- If a path breaks, record it as a migration finding; do not guess a replacement.

## Verification

A Pluto manifest operation is verified only when:

```text
VERIFY_STATUS=PASS
folders_verified=<N>
folder_manifests_verified=<N>
registry_entries=<M>
external_hash_entries=<M>
unmanifested_folders=0
unmanifested_files=0
folder_purity_violations=0
```

A file migration is verified only when:

```text
source_sha256 == destination_sha256
```

A folder migration is verified only when every file in scope has matching source/destination hashes and the updated Pluto manifests pass verification.
