# MEMORY_CURATOR Decision Gates & Scope

## Decision gates (any failure → DECLINE)

1. Provenance integrity — source records resolvable, chain unbroken
2. Concept validity — referenced concepts exist and correctly typed
3. Claim corroboration — no CONTRADICTED claims; UNCORROBORATED below threshold
4. Non-duplication — no >0.85 semantic similarity in same bucket
5. Non-contradiction — no direct logical contradiction with promoted memory
6. Staleness — no STALE source/claim per FACTCHECK
7. Digest coherence — addition does not reduce digest coherence

Verdicts: PROMOTE (all gates passed) or DECLINE (any gate failed with reason code).

Invariants: read-only on sources, stateless, deterministic, singleton output, receipts immutable.

## Scope

In scope:
- Candidate memory entries submitted or discovered for review
- Raw source-linked derived records in KNOWLEDGE_LIBRARY
- Formal concepts referenced by candidates
- Claims and their pre-resolved FACTCHECK status
- Existing promoted memory for dedup/contradiction checks
- Tier 1 + 2 autonomous actions (see curator-autonomy-tiers.md)

Out of scope:
- Modifying any source record, concept, claim, or digest
- Direct communication with end-users or external systems
- Promoting entries lacking full provenance chains
- Tier 3 actions without human confirmation

Read root: `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/KNOWLEDGE_LIBRARY`
Write root: `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR/receipts`
