---
name: workspace-orientation
description: Tell projects, folders, and git repos apart in Hermes.
version: 1.0.0
category: autonomous-ai-agents
tags: [hermes, workspace, projects, git, orientation, filtering, filesystem]
related_skills: [hermes-agent]
---

# Workspace Orientation

When a user is confused about what they see in their Hermes workspace — extra folders, things that look like projects but aren't, uncertainty about what's linked to what — the goal is to **identify deterministically, not guess**, and give them a clean focused view without deleting anything.

## Core principle

**Hermes projects ≠ filesystem folders ≠ git repos ≠ git worktrees.** Each is a distinct thing and they can sit side by side in the same directory tree without any relationship. Don't assume a visible folder is a project, a worktree, or linked to the user's project unless you verify.

## Verification sequence

Always trace what you see to its actual nature before answering "why is this here":

### 1. What are the actual Hermes projects?
```bash
project_list
```
This tells you the REAL projects Hermes knows about — name, id, primary_path, active state. Everything else visible may just be a filesystem folder.

### 2. Are any visible folders git worktrees of the main repo?
```bash
cd <repo-root> && git worktree list
```
Worktrees show up in this list with their branch. If a folder is NOT in this list, it's not a worktree.

### 3. Are any visible folders separate git repos?
```bash
cd <suspicious-folder> && git status
```
A separate `.git` directory + its own branch/remote = independent repo. Each has its own history, remotes, and branches — not derived from the parent.

### 4. Are there symlinks bridging folders into the project?
```bash
find <project-path> -maxdepth 1 -type l
```
A symlink would make a folder outside the project appear inside it. Not present = no bridging.

### 5. What does the filesystem actually contain?
```bash
find <path> -maxdepth 1 -type d          # directories only
find <path> -maxdepth 1 -name '.*'       # hidden items
ls -la <path>                             # full listing with permissions
```
Ground your answer in what's actually on disk.

## Reading the results

| Finding | What it means |
|---|---|
| Folder NOT in `project_list` | Not a Hermes project — just a filesystem folder |
| Folder NOT in `git worktree list` | Not a git worktree |
| `git status` shows its own branch/remote | Independent git repo, separate from anything else |
| No symlink into project path | Nothing is bridging it into the project view |
| Folder IS inside the project's `primary_path` | It's just a subdirectory of the project root — visible because the project mirrors its filesystem |

## Why things appear in the project view

The project sidebar/file browser shows the contents of the project's `primary_path`. If that path is a folder that already contained many subfolders when the project was created, **all of those pre-existing subfolders show up** — they're not projects, not worktrees, just folders that were there before.

If the view shows things OUTSIDE the `primary_path` (siblings, parent folders), the sidebar is rendering a wider tree than just the project root. That's a view-scope thing, not a linking thing.

## Getting a clean focused view

If the user wants to see ONLY what they created and nothing else:

1. **Use filters** — the project view/filter feature is exactly for this. Apply it to narrow to the single project or folder they care about. This is non-destructive: everything stays on disk, nothing is deleted, no breakage risk.
2. **Optionally create a fresh project** on an empty folder:
   ```
   project_create(name="Clean project", path="D:/path/to/empty/folder")
   ```
   Only if they want a truly blank slate. Not required — filtering is enough.

## What NOT to do

- **Don't delete or remove folders** to "clean up" the view. The user explicitly wants to avoid breakage. Filters are the non-destructive answer.
- **Don't guess** that something is "linked" or "a worktree" or "a branch" without running the verification commands above.
- **Don't conflate** git worktrees, separate repos, and Hermes projects — verify each independently.

## Common confusion patterns

| What the user sees | Typical reality |
|---|---|
| "I see solob-portal, orbital_book_studio, etc. but I only created one project" | These are separate git repos in `active_apps/` — siblings of the project root, not projects, not worktrees. Visible because the sidebar shows a wider tree. |
| "Are these linked to git branches or worktrees?" | Check `git worktree list` — if not listed, not a worktree. Check `git status` in each folder — if it has its own repo, it's independent. |
| "I created one project but see many directories" | The project's `primary_path` already contained those directories. The project just mirrors the filesystem at that path. |
| "I filtered and now only my project shows" | Correct — filters narrow the view to what you choose. Non-destructive. Safe to proceed. |

## Deep workspace research: source, reflection, and runtime boundaries

When a workspace contains a personal knowledge archive, agent files, generated summaries, or mirrored vaults, do not treat all Markdown as one corpus. Perform a read-only inventory before routing or restructuring.

1. Identify the authoritative roots and their roles from orientation files, project instructions, catalogs, and handoffs. Distinguish source material, derived analysis, runtime/system state, staging, legacy mirrors, and generated output.
2. Use an ownership matrix rather than filename heuristics:
   - **H1 — human source:** the user's journal, voice, media, creative work, and direct observations. Preserve verbatim; never silently normalize or promote.
   - **H2 — reflection:** profiles, extraction output, indexes, candidate axioms, gems, and contradiction/review queues. Every claim needs provenance and status; derived text never replaces its source.
   - **H3 — Hermes/system:** `SOUL.md`, `USER.md`, `MEMORY.md`, project rules, governance specs, manifests, logs, and runtime state. This describes the agent/system and routing rules, not the user's source identity.
3. Keep ownership planes separate from conceptual/framework layers. A Drayl ontology/physics/architecture/OS/manifestation model is a subject taxonomy, not permission to merge H1, H2, and H3.
4. Treat conceptual Main/Shadow/Current/Deviation routing as a state machine, not as four folders to bulk-populate. Contradictions remain visible; unstable material stays current or archived; promotion requires explicit review.
5. Before any mirror or graph build, exclude the destination route, prior mirrors, caches, VCS/dependency trees, and generated corpus directories. A mirror must never be scanned as a source for itself.
6. If a bulk corpus already exists and the user reports deleting it, verify each canonical and mirror location separately. Report stale remnants; do not delete them without explicit scope.
7. Prefer a small route of indexes, provenance links, and reviewed notes over a full duplicate corpus. Keep original sources in place and make the route non-destructive.
8. **Legacy agent workspaces** (e.g., `agent_space`) must be inventoried deeply before reuse as a memory root. Classify each file as active tool code, policy reference, project memory, or historical artifact. Do not assume current relevance from filename alone.
9. **Authority filenames are live-law names, not archive labels.** If the desired end state is one workspace authority file, retire every other exact authority basename from active search surfaces. Convert app/component instructions into project skills, archive old content under generic names such as `historical-instructions.md` or compressed `component-governance-history.md.gz`, and avoid plaintext references like “old AGENTS.md”; exact-name hits make agents chase historical rabbit holes as possible law. When retiring an exact authority basename: copy to the generic name first, verify hash/size match, then remove the original — never the reverse. If a destination generic name already exists with different content, use a timestamped variant rather than overwriting.
10. **Scoped agent folders** inside `agent_space` use `agent-{AGENT}_{REPORTS_TO}` (example: `agent-ONA_Plato`). When creating agent agency surfaces, use agent-prefixed files/folders such as `Ona_SOUL.md`, `Ona_USER.md`, `Ona_MEMORY.md`, `Ona_SCOPE.md`, `Ona_T1_Intention/`, and `Ona_T2_Execution/`. Do **not** create `.hermes.md`, `AGENTS.md`, or `CLAUDE.md` inside these scoped folders unless explicitly requested; those names can cause the agent to pull Plato/Hermes context instead of the scoped agent contract.
13. **Agent-local skills/hooks are proposals first.** Store scoped capability registries under the agent's prefixed folders (for example `Onu_skills/Onu_skill_hook_registry.md` and `Onu_plugins/`), not as global Hermes skills or live hooks. Promote only after an intent packet, execution artifact, filesystem/log evidence, claim capture, and an accuracy ledger compare `what Plato/user said` vs `what logs show happened` vs `what the agent claimed happened`.

## Workspace Intelligence Matrix

The `ANDROMALIUS/MATRIX/` folder holds workspace-wide intelligence artifacts:

- `document-dependency-matrix.md` — canonical files, update groups, charge levels (CRITICAL → LOW)
- `reverse-dependency-index.json` — given any file, what depends on it
- `agent-readiness.json` — readiness scores per agent across 3 layers
- `fw-file-mapping.json` — which files each FW entry touches
- `agent-skill-usage-matrix.json` — agent × skill × usage routing
- `component-direction-map.md` — folder map with direction per component

When a user asks "where is X?" or "what depends on Y?", check MATRIX/ before scanning the full tree. When workspace structure changes, update MATRIX/ artifacts (especially `document-dependency-matrix.md` and `reverse-dependency-index.json`).
11. **Spawned Hermes agents are not automatically clean-room.** Runtime logs may show automatic skill/context loads outside the explicit agent file list (for example `workspace-orientation`, `hermes-spl-governance`, or `hermes-agent`). Score behavior and context isolation separately; if unlisted context loads, call the result partial even when the agent answers leak questions correctly. When testing canary leakage, keep exact canary values outside every agent-readable prompt, ledger, and prior-result summary; put answer keys/runner scripts in a Plato/parent harness outside the scoped agent folder.
12. **Skill minimization flags are evidence, not proof.** `hermes chat --ignore-rules` may still show a visible skill-load event; `hermes chat --safe-mode` may remove visible skill events while global memory/profile context remains visible. Record direct file reads, visible skill events, and injected non-file context as separate evidence classes rather than collapsing them into a single pass/fail.
13. **Lane A intake routing is a detector/receipt layer unless it runs before Hermes context assembly.** For scoped agents, create a parent-owned intake router plus `{Agent}_AGENT_MANIFEST.json`, `{Agent}_skills/{Agent}_hermes_spl_governance.md`, and `{Agent}_plugins/{Agent}_intake_routing_spec.md`; keep exact canaries in the parent harness only. If the router observes forbidden global skill/context loading, mark the result STAGE/PARTIAL and do not claim clean-room isolation.

See `references/drayl-memory-boundaries.md` for the reusable H1/H2/H3 matrix, anti-recursion checks, and proposed route shape.
See `references/agent-space-inventory-pattern.md` for the legacy workspace evaluation workflow.
See `references/agent-scoped-folder-pattern.md` for the scoped agent folder convention and Ona-style scaffold.
See `references/agent-runtime-verification-pattern.md` for testing whether a scoped agent actually loaded/used its files, refused absent facts, and obeyed safe/forbidden/unknown task boundaries during runtime.
See `references/scoped-agent-canary-and-runtime-isolation.md` for the Onu-derived canary-leak and minimized-runtime isolation pattern, including contamination pitfalls.
See `references/agent-intake-routing-pattern.md` for the Lane A parent-owned intake router template: manifests, local governance packets, receipts, canary handling, and scoring.
See `references/agent-local-precedence-probes.md` for safe local-vs-global governance contradiction tests, increasing-stakes ladders, hard-fail criteria, and the rule to score behavior separately from clean-room isolation.
See `references/agent-sideways-canary-detector.md` for applying parent-held canaries and Lane A intake receipts as a sideways-agent detection mesh; it separates prevention, detection, and false-positive handling when agents drift or global skills contaminate a run.
See `references/workspace-search-technique.md` for the multi-pass comprehensive search methodology when a user asks to "search everywhere" or "find all references" across a multi-root workspace.
See `references/script-discovery-and-documentation-pattern.md` for the three-layer script documentation pattern (header → notes → index) that lets an agent discover and use workspace tools without loading everything into context.
See `references/missing-infrastructure-detection.md` for the pattern to identify structural gaps when orientation or governance docs reference files, folders, or tools that don't actually exist.
See `references/project-local-skill-discovery.md` for searching workspace-local skills before the global Hermes registry, including hidden `.agents/skills` / `.hermes/skills`, project trust, and session refresh verification.
See `references/privacy-tagging-and-sensitive-hinting.md` for the privacy-label + HINT communication pattern to use before personal questionnaires or broad workspace scans in legacy/Know-Me archive work.
See `references/curriculum-first-then-audit.md` for the pattern of building a full curriculum first, auditing it with a scoped scout agent (Onu), then only beginning personal questionnaires after the audit passes.

## When to stop and ask

- If verification is inconclusive (folder has no `.git`, isn't in worktree list, isn't in project list, and isn't a symlink) — it's just a regular folder. Say so plainly.
- If the user wants to move forward but is uncertain about what they're seeing — resolve the uncertainty first (run the verification sequence), then confirm they're clear before proceeding. Don't let "I think it's fine" substitute for verified clarity.
