# Privacy Tagging and Sensitive Hinting Pattern

Use this pattern when Deego asks to prepare a personal archive, legacy curriculum, Know-Me system, or workspace scan that may encounter private, son-only, sealed, third-party, legal/financial, health-sensitive, credential-adjacent, or IP-sensitive material.

## Trigger

The user wants broad or long-term personal understanding from workspace/projects/chats, but also wants the agent to avoid data leaks, vulnerability exposure, alarmist language, or direct disclosure of sensitive material. This includes future dynamic passphrase/gating ideas, but the immediate reliable layer is file/claim privacy tags plus safe hinting.

## First move

Before questionnaires or full workspace scans, create/verify these surfaces in the project/curriculum folder:

- `privacy-routing-matrix.md`
- `sensitive-hinting-schema.md`
- `pre-questionnaire-readiness.md`

The readiness file should keep personal questioning blocked until consent, claim schema, stop/skip/fatigue rules, scan receipt, archive manifest, son-facing leakage audit, and voice anti-caricature rubric exist.

## Privacy labels

Primary labels:

- `OPEN`
- `PRIVATE`
- `SON-ONLY`
- `SEALED-UNTIL-DATE`
- `DO-NOT-USE`
- `QUARANTINE_REVIEW`

Operational flags:

- `THIRD_PARTY`
- `MINOR_RELATED`
- `LEGAL_FINANCIAL`
- `HEALTH_SENSITIVE`
- `CREDENTIAL_ADJACENT`
- `PUBLIC_BUT_SENSITIVE`
- `CULTURAL_SEMANTIC`
- `IP_SENSITIVE`
- `SEALED_REFERENCE_ONLY`
- `GENERATED_DERIVATIVE`

Most restrictive route wins. `SON-ONLY` is an inheritance route, not public permission.

## Communication modes

Use the lowest disclosure level that lets Deego decide:

- `DO_NOT_DISCUSS`
- `SEALED_STUB`
- `ASK_TO_OPEN`
- `HINT_ONLY`
- `REDACTED_EXCERPT`
- `SOFT_SUMMARY`
- `SON_SAFE`
- `DIRECT_CITE`

## HINT pattern

When direct detail could leak, use:

- **H**igh-level class: what type of issue/material exists?
- **I**mpact shape: what could it affect?
- **N**eeded decision: what should Deego choose?
- **T**race-safe pointer: where it is, without exposing protected content.

Example: “I found a credential-adjacent item in an approved scan area. It may affect service access if mishandled. I’m not opening or repeating the value. Do you want me to quarantine it, skip it, or create a redacted inventory entry?”

## Dynamic passphrase/gate parking lot

The user proposed a long-term trajectory-based passphrase gate: feed recent chats/context to a deterministic script, ask the user for a phrase/word, use bounded LLM follow-up only for ambiguity, and have a hook stop sensitive communication until pass. Do not implement this ad hoc. Capture it as a later Hermes hook/security design task with requirements:

1. Do not store passphrases in plaintext.
2. Do not let the LLM invent acceptance after failure.
3. Separate deterministic checks from LLM clarification.
4. Fail safe without blocking normal non-sensitive chat forever.
5. Log pass/fail without exposing the phrase.

## Pitfall

Do not start extracting personal biography or scanning “all folders” just because a curriculum exists. Onu’s STAGE finding showed that safety/schema prerequisites must come before Daily Questionnaire 001 or broad workspace archaeology.
