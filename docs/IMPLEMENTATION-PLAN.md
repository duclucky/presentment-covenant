# Implementation plan and acceptance checks

1. Freeze specification, source lock, authority/value matrices, safety cards, compatibility matrix, and claim map.
2. Add one pinned contract and deterministic helpers; lint immediately.
3. Add direct tests first for state, access, time, hashes, normalization, accounting, and all negative tripwires.
4. Add a small integration test and a deployment parser that projects only safe receipt fields.
5. Run `genvm-lint`, direct tests, AST/metadata checks, and schema extraction.
6. Run target-network read-only schema preflight, ABI round trips, and a bounded source/LLM capability smoke.
7. Deploy resumably only after the local and target preflight evidence is clean; wait for `FINALIZED`, then separately verify execution, semantic result, and canonical consequence.
8. Write sanitized evidence and exact counts, review public hygiene, and prepare—but do not submit—the Portal packet.

Acceptance requires no unresolved mandatory test, no unbound semantic claim, no orphaned GEN, and no claim of network evidence without a current receipt/state read.
