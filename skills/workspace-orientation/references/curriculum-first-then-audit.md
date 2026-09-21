# Curriculum-First Then Audit Pattern

Use this pattern when Deego asks to build a long-term personal archive, legacy curriculum, Know-Me system, or any structured understanding project that will eventually touch private workspace content, personal history, or son-facing inheritance.

## Trigger

The user wants a multi-course, multi-year personal understanding system (e.g., a "Know-Me" curriculum equivalent to a master's degree). The danger is starting questionnaires or workspace scans before the safety and schema surfaces exist, causing sidetracks and potential privacy leaks.

## Core workflow

1. **Build the full curriculum first.**
   - Write `FULL_CURRICULUM.md` with all courses, objectives, assignments, exams, and evidence requirements.
   - Do NOT start Daily Questionnaire 001 yet.

2. **Onu audit (scout only).**
   - Create an Onu task packet in `Onu_T1_Intention/`.
   - Onu reads only assigned curriculum files.
   - Onu writes audit report to `Onu_T2_Execution/` and JSON summary to `Onu_logs/`.
   - Onu must NOT scan the full workspace, open secrets, ask personal questions, or modify the curriculum directly.

3. **Patch from audit.**
   - Apply Onu's recommended patches (consent receipt, claim schema, privacy matrix, hinting schema, scan receipt, archive manifest, son audit, voice rubric, exam framework).
   - Re-audit if verdict is STAGE.

4. **ACT on questionnaires.**
   - Only after verdict moves to ACT does Daily Questionnaire 001 begin.
   - First questions stay limited to method, consent, boundaries, and legacy intent.

## Onu task packet format

```markdown
# Onu Task NNN — <Title>

**Agent:** Onu
**Reports to:** Plato
**Date:** YYYY-MM-DD
**Status:** ASSIGNED

## Mission
<One sentence>

## Scope
Allowed:
- Read assigned files
- Write to Onu_T2_Execution/ and Onu_logs/

Forbidden:
- No full workspace scan
- No secrets/credentials
- No personal questions
- No curriculum edits

## Audit questions
<Specific questions Onu must answer>

## Required report format
<Expected sections>

## Scoring
- ACT: safe to proceed
- STAGE: needs fixes first
- DECLINE: unsafe, do not proceed
- SHARE: report upward for decision
```

## Verdict meanings

| Verdict | Meaning | Next step |
|---|---|---|
| ACT | Curriculum is safe/complete enough | Begin Daily Questionnaire 001 |
| STAGE | Promising but needs specific fixes | Patch, then re-audit |
| DECLINE | Unsafe/incomplete | Do not proceed, redesign |
| SHARE | Report upward to Plato/Deego | Wait for decision |

## Pre-questionnaire readiness checklist

Do not begin Daily Questionnaire 001 until:

- [ ] Consent Receipt v1 exists and is approved
- [ ] Daily Questionnaire 001 protocol exists (method/consent/boundaries/legacy only)
- [ ] Privacy routing matrix exists
- [ ] Sensitive hinting schema exists
- [ ] Claim-card schema exists with review status transitions
- [ ] Stop/skip/seal/private/fatigue rules are visible
- [ ] No workspace scan is authorized by default
- [ ] Archive extraction is forbidden unless separately approved
- [ ] Scan-scope receipt template exists
- [ ] Archive and derivative manifest schema exists
- [ ] Son-facing leakage audit exists
- [ ] Voice anti-caricature rubric exists
- [ ] Exam rubric framework exists

## File naming convention

All Onu files use the `Onu_` prefix under `agent-ONU_Plato/`:

- `Onu_T1_Intention/Onu_task_NNN_*.md` — task packets
- `Onu_T2_Execution/Onu_task_NNN_*.md` — audit reports
- `Onu_logs/Onu_task_NNN_summary.json` — structured summaries

## Pitfall

Do not let the user skip the audit phase because the curriculum "looks done." Onu's STAGE finding in the Know-Me project showed that even a strong 72-course plan needs prerequisite safety/schema patches before personal questions begin. The audit is not bureaucracy — it is the gate that prevents sidetracks and leaks.