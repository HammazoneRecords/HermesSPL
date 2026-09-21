# Project-local skill discovery and adapter verification

Use this when the user asks to find a skill **in the workspace**, says a workspace procedure/skill is missing, or suspects a Hermes adapter is incomplete.

## Search order

1. Treat “search workspace” literally: search the repository filesystem first, not memory and not only the injected Hermes skill registry.
2. Include hidden and gitignored adapter roots. Check at minimum:
   - `<repo>/.agents/skills/**/SKILL.md`
   - `<repo>/.hermes/skills/**/SKILL.md`
   - `<repo>/.claude/skills/**/SKILL.md`
   - `<repo>/procedures/` and `<repo>/procedures/adapters/`
3. Only after the filesystem pass, compare what Hermes currently exposes through its skill registry.

A registry miss does **not** prove the skill is absent. It may exist locally but be undiscovered, untrusted, quarantined, disabled, or absent from the active session’s cached skill index.

## Hermes project-skill prerequisites

Hermes can discover trusted project-local skills beneath both `.hermes/skills` and `.agents/skills`. Project skills are deliberately gated because repository content can inject instructions.

From the repository root, verify or establish trust with:

```bash
hermes skills trust <repo-root>
hermes config get skills.trusted_project_dirs
```

Trust confirmation should state the canonical repo path and the number of project skills that will load. Do not hand-edit `config.yaml`.

For source-level diagnosis, verify three facts separately:

1. the enclosing git root is the expected repository;
2. that exact canonical path is trusted;
3. project skill discovery returns the expected local skill directory.

Use the same root-resolution code path Hermes uses before claiming a nested project's skills are runtime-loadable:

```bash
# --- local (bash) ---
python -c "
from agent.skill_utils import find_project_root, get_project_skills_dirs
print('project_root=', find_project_root())
print('project_skills_dirs=', [str(p) for p in get_project_skills_dirs()])
"
```

If a workspace folder sits inside a larger git checkout, Hermes resolves project skills from the nearest git root, not from every nested `.hermes/skills` directory. Put runtime-loadable wrappers under the resolved git root's `.hermes/skills`, make the nested folder its own project root, or label the nested skills filesystem-defined only; otherwise `hermes skills trust <nested-folder>` can report skills while `hermes chat --skills <name>` still returns unknown.

Remember that direct Python probes must use the same `HERMES_HOME` and surface workdir/`TERMINAL_CWD` as the running Hermes profile. A probe with the wrong profile home can falsely report no trusted directories.

## Active-session cache boundary

Project trust changes do not retroactively rewrite an already-built session prompt or injected skill index. After trust changes:

- use `/reload-skills` where the surface supports it, or
- start a new session inside the trusted repository.

Verify in the fresh/reloaded session that the named project skill resolves. Do not rely solely on `hermes skills list` or `hermes skills inspect`; some administrative/listing surfaces emphasize profile-installed skills or catalog sources rather than the project tier. The decisive runtime probe is prompt assembly itself:

```bash
hermes chat --skills <name> --quiet --max-turns 1 -q "If this skill loaded, answer SKILL_VISIBLE and quote one safe rule from it."
```

Treat `SKILL_VISIBLE` plus a skill-specific rule as runtime-load evidence. Treat a successful trust/list/inspect command without a fresh chat or prompt-builder probe as discovery evidence only, not proof that a session can preload the skill.

## Nested CLI discovery gotcha

When a parent Desktop terminal launches a nested `hermes chat` subprocess, **do not assume the subprocess cwd controls discovery.** Hermes prefers the surface's `TERMINAL_CWD` environment variable over the process cwd for project-skill resolution. A stale `TERMINAL_CWD` that points outside the repository makes the subprocess resolve zero project skills even when `PWD` is correct.

Diagnose and fix:

```bash
# --- local (bash) ---
printf 'PWD=%s\nTERMINAL_CWD=%s\n' "$PWD" "$TERMINAL_CWD"
TERMINAL_CWD='D:/MW_CENTRAL' hermes chat --skills <name> --quiet -q "..."
```

External shells with no `TERMINAL_CWD` fall back to their actual cwd, so a plain `cd D:/MW_CENTRAL && hermes ...` works there but fails under a parent Desktop session that exported a bad value.

## Duplicate-project-skill-name trap

Hermes discovers trusted project skills beneath **both** `.hermes/skills/` and `.agents/skills/`. When the same skill name exists in both roots, `skill_view()` refuses the load with `Ambiguous skill name: N candidates` — it does **not** silently apply directory precedence. An old cross-agent `.agents/skills/` full-copy can therefore block the newer `.hermes/skills/` thin wrapper from ever loading.

Before claiming native invocation works, verify uniqueness:

```bash
# --- local (bash) ---
python -c "
from agent.skill_commands import build_preloaded_skills_prompt
p, loaded, missing = build_preloaded_skills_prompt(['<name>'])
print('loaded=', loaded, 'missing=', missing)
"
```

If a collision is found, resolve it non-destructively: archive or rename the older root (e.g. `mv .agents/skills .agents/skills-legacy-YYYYMMDD`) and log the move in the session's move log. Deleting without a reference breaks CON-001 and loses the history that the collision existed.

## Adapter completeness test

When the workspace has an adapter map, compare it with the actual native integration:

- Does the adapter map list the high-value procedures?
- Are thin wrappers present in a Hermes-discoverable project skill root?
- Is the repository trusted?
- Was at least one procedure invoked end-to-end from a fresh session?
- Does the adapter map honestly say `SCAFFOLD`, `DRIFT`, or `IN SYNC` based on that proof?

A context packet or adapter-loop document alone is not a complete skill adapter if native project skills exist but Hermes cannot discover them.

## Common pitfall

Wrong sequence:

1. search `skills_list`;
2. see no match;
3. conclude “the skill does not exist.”

Correct sequence:

1. filesystem search including hidden roots;
2. inspect canonical procedure and adapter map;
3. check project trust/discovery;
4. refresh or start a new session;
5. verify invocation end-to-end;
6. only then report adapter status.
