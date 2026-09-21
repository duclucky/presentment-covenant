# PresentmentCovenant

PresentmentCovenant is a standalone GenLayer Intelligent Contract primitive for a bounded documentary-presentation exercise. An issuing-bank role locks a small 2 GEN purse, a beneficiary submits an authenticated invoice envelope plus one commit-addressed official DCSA synthetic eBL record, and validators independently refetch the exact DCSA bytes and compare a structured semantic examination. Deterministic contract code validates coverage and derives the only value consequence.

This repository is intentionally contract-only. It is not a bank integration, a real trade transaction, a full UCP/ISBP implementation, a legal opinion, sanctions or fraud screening, an oracle for goods reality, or evidence of production adoption. The DCSA record is a public synthetic conformance fixture; the invoice is authenticated as a beneficiary submission but is not independently proof of its commercial assertions.

## Contract boundary

The contract owns immutable roles, deadlines, rule profile, evidence commitments, presentation state, validator-bound semantic status, exhaustive discrepancy codes, waiver/cure/retry/expiry, the fixed GEN purse, withdrawals, and zero-liability closure. External authorities own their source records. A future adapter may supply an authoritative invoice or insurance endpoint, but unsupported or unavailable evidence remains `UNVERIFIABLE` and cannot move value.

## Local checks

```text
genvm-lint check contracts/presentment_covenant.py
pytest tests/direct/ -v
npm run check
```

The contract has 18 public methods (10 views and 8 writes), and the direct suite contains 12 tests. `npm run check` runs the pinned-runner lint, strict typecheck, schema emission, and all direct adversarial tests. The deadline regression tests prove that cures and retries accepted in their respective windows remain adjudicable because `adjudication_deadline` is strictly last. This is the Intelligent Contracts track, so there is deliberately no frontend or frontend build.

## Studio Dev revision

The active target is Studio Dev (chain 61997) with the Consensus v0.6 RC-compatible contract API and fee profile. The read-only target schema preflight matches the local schema. Live deployment evidence is intentionally added only after the corrected source is committed and the finalized Studio Dev state has been read back.

The current preflight record is [`docs/evidence/studio-dev/target-network-preflight.json`](docs/evidence/studio-dev/target-network-preflight.json). Files under `docs/evidence/studionet/` are retained only as historical evidence for the superseded legacy revision and must not be mixed with Studio Dev claims.

## Reuse

An adapter can deploy one instance per documentary mandate, replace the fixed official source profile with a reviewed issuer matrix, and consume only the canonical views (`get_credit`, `get_presentation`, `get_attempt`, `get_discrepancies`, `get_accounting`, `get_withdrawable`). A consumer remains responsible for its own authorization and any downstream consequence.
