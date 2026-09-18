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

The target network is Studionet (chain 61999). The read-only target schema preflight matched the local schema before deployment. The resumable lifecycle finalized these writes with `MAJORITY_AGREE` and successful leader execution: deployment (`0x09c3e33a00090d0725915fc5a83ff110068a810dbf8a85482c1ee400a0797ce8`), activation (`0x19cf047505d5b42acad69e7398f1b0a9d6cec06ef9b249ac0bed919fac67791a`), presentation (`0x8bf7ae1066eff3461a9c844e97e66d3a333b272177ae244f8fbaacc1c86fb33a`), adjudication (`0x7e41e6fd9c726e846203e45f167ab776dc813fcb5082d1960156f69341849d83`), beneficiary withdrawal (`0x723fbfbdd2352318b5d48fb0775dbb46be2107d7dcf59073d7612cda1ab6688a`), and closure (`0x0b67e29a100bb96372d7f0e30d7c95458c018430d023dac4c6b538a1f1f36bcc`). The primary contract is [`0x77BBd0FaF7600bD1dD23087B6D6E76D332683CB2`](https://genlayer-explorer.vercel.app/address/0x77BBd0FaF7600bD1dD23087B6D6E76D332683CB2). Canonical reads ended in `CLOSED`, `total_withdrawn = 2 GEN`, and `zero_liability = true`; adjudication reached `COMPLIANT` before withdrawal.

Sanitized, allowlisted receipts and canonical reads are in [`docs/evidence/studionet/deployment.json`](docs/evidence/studionet/deployment.json); the fresh final state check is [`docs/evidence/studionet/final-verification.json`](docs/evidence/studionet/final-verification.json), and the preflight record is [`docs/evidence/studionet/target-network-preflight.json`](docs/evidence/studionet/target-network-preflight.json). Local/direct evidence remains distinct from finalized network evidence.

## Reuse

An adapter can deploy one instance per documentary mandate, replace the fixed official source profile with a reviewed issuer matrix, and consume only the canonical views (`get_credit`, `get_presentation`, `get_attempt`, `get_discrepancies`, `get_accounting`, `get_withdrawable`). A consumer remains responsible for its own authorization and any downstream consequence.
