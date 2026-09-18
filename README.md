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

The contract has 18 public methods (10 views and 8 writes), and the direct suite contains 10 tests. `npm run check` runs the pinned-runner lint, schema emission, and all direct adversarial tests. This is the Intelligent Contracts track, so there is deliberately no frontend or frontend build.

## Verified Studionet run

The target network is Studionet (chain 61999). The read-only target schema preflight matched the local schema before deployment. The resumable lifecycle finalized these writes with `MAJORITY_AGREE` and successful canonical leader execution: deployment (`0x8c31ced9db9a29429ccd4a80e8d704faae85b88c5bf8a11920ec0f56aa892757`), activation (`0xeed92419b9155520eb5421d506214d82148f9a6759f274d1dbd6bf762e9228f3`), presentation (`0x52861fe7a658acd8f2fb4f5ea2f447fe4559aeea093ecb432c51b3d0e1e510d6`), adjudication (`0xce6a9a2fdaa0e1e81963c1a473aab14a0fe70aa70e27d542b8d14387208ed604`), beneficiary withdrawal (`0xf2befd8d2ad65b469de3140133f9c289f57666a6ea522bdb9e6a01edc2d217cd`), and closure (`0xd7773fdc1fa37b3d692c9150bc7b80ed744ff7c1155607bb92babdd64e8968d4`). The current Studionet Explorer contract page is [`0x2D9a2942f1700280e633E08d62528896332C480d`](https://explorer-studio.genlayer.com/contracts/0x2D9a2942f1700280e633E08d62528896332C480d). Canonical reads ended in `CLOSED`, `total_withdrawn = 2 GEN`, and `zero_liability = true`; adjudication reached `COMPLIANT` before withdrawal.

Sanitized, allowlisted receipts and canonical reads are in [`docs/evidence/studionet/deployment.json`](docs/evidence/studionet/deployment.json); the fresh final state check is [`docs/evidence/studionet/final-verification.json`](docs/evidence/studionet/final-verification.json), and the preflight record is [`docs/evidence/studionet/target-network-preflight.json`](docs/evidence/studionet/target-network-preflight.json). Local/direct evidence remains distinct from finalized network evidence.

## Reuse

An adapter can deploy one instance per documentary mandate, replace the fixed official source profile with a reviewed issuer matrix, and consume only the canonical views (`get_credit`, `get_presentation`, `get_attempt`, `get_discrepancies`, `get_accounting`, `get_withdrawable`). A consumer remains responsible for its own authorization and any downstream consequence.
