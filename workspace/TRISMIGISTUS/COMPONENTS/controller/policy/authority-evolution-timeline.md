# Authority Evolution Timeline

Purpose: explain how workspace instruction/routing surfaces evolved without making historical surfaces look like current law.

Visual diagram:
`/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/TRISMIGISTUS/COMPONENTS/controller/policy/workspace-evolution.html`

Future work registry:
`/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/TRISMIGISTUS/COMPONENTS/controller/registry/fw-registry.md`

## CURRENT RULE

`/root/MW_CENTRAL/AGENTS.md` is the single workspace authority file.

Project/app-specific operational guidance lives in ANDROMALIUS-managed project skills under:

`/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/PROJECT_SKILLS/`

Historical instruction material is provenance only. It must not be treated as live routing.

## HISTORICAL — adapter era

Earlier workspace operation used model/tool-specific adapter surfaces. These included assistant-specific prompts, IDE/tool rules, and local instruction files. They helped bootstrap governance but created ambiguity because different tools loaded different files.

Status: `HISTORICAL`

Current handling:
- preserve evidence where needed,
- do not route from old adapter surfaces,
- convert useful rules into current law or project skills,
- rename retired instruction material to generic historical names.

## TRANSITIONAL — multi-agent / scoped-agent migration

ANDROMALIUS introduced scoped agents, agent arena roots, manifests, scope files, and proof-led workflows. During this period, nested component instruction files and source-fork guides existed beside root workspace rules.

Status: `TRANSITIONAL`

Current handling:
- scoped agents use prefixed files and manifests,
- nested component guidance becomes project/component skills,
- old source mirrors are treated as sediment/provenance,
- agents must not rummage through historical instruction files to infer law.

## CURRENT — TRIS / ANDROMALIUS project-skill era

TRIS coordinates current ANDROMALIUS work. Active app/project guidance is moving into ANDROMALIUS-owned project skills. Project skills are explicit, scoped, and model-agnostic. They preserve useful legacy rules while removing authority ambiguity.

Status: `CURRENT`

Current handling:
- root workspace law stays singular,
- per-project instructions live as skills,
- old instruction docs are archived under generic names,
- receipts preserve proof without forcing any operator into authority rabbit holes.

## DEPRECATED — exact-name local authority surfaces

Local exact-name authority files inside apps, forks, mirrors, or old docs are deprecated unless they are the single root law file.

Status: `DEPRECATED`

Current handling:
- do not create new local exact-name authority files,
- do not archive retired files under authority-looking basenames,
- do not leave pointer files with authority-looking basenames,
- sanitize plaintext references where they create rabbit holes.

## CURRENT — authority clarity rule

Design for all operators and runtimes. Names and headings must carry status explicitly so current law, transitional material, deprecated material, and historical provenance cannot be confused.

Status labels:

- `CURRENT` — live authority/routing.
- `TRANSITIONAL` — migration-era, temporary, or being converted.
- `HISTORICAL` — provenance only.
- `DEPRECATED` — preserved evidence, not instruction.

If a future operator has to open a historical file to decide whether it is law, the name/protocol failed.

## Examples

Preferred historical names:

- `historical-instructions.md`
- `legacy-project-instructions.md`
- `component-governance-history.md`
- `legacy-model-adapter-pointer.md`
- `adapter-history.md`

Preferred current names:

- `SKILL.md` inside `PROJECT_SKILLS/<project-slug>/`
- `workspace-script-index.md`
- `historical-source-policy.md`
- `authority-evolution-timeline.md`

## Sanitation dependency

Plaintext sanitation should happen after this timeline and naming protocol are in place. Sanitation must distinguish:

- current-law references,
- forbidden-context detector lists,
- historical logs,
- receipts/proofs,
- code literals.

Do not blindly replace all text. Remove rabbit holes while preserving proof.
