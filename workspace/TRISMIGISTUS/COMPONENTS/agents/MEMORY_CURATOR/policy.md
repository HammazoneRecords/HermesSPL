# MEMORY_CURATOR Policy

Decision gates (any failure → DECLINE):
1. Provenance integrity — source records resolvable, chain unbroken
2. Concept validity — referenced concepts exist and correctly typed
3. Claim corroboration — no CONTRADICTED claims; UNCORROBORATED below threshold
4. Non-duplication — no >0.85 semantic similarity in same bucket
5. Non-contradiction — no direct logical contradiction with promoted memory
6. Staleness — no STALE source/claim per FACTCHECK
7. Digest coherence — addition does not reduce digest coherence

Verdicts: PROMOTE (all gates passed) or DECLINE (any gate failed with reason code).

Invariants: read-only, stateless, deterministic, singleton output, receipts immutable.
