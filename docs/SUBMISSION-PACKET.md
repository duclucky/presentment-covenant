# Copy-ready submission packet

## Category

`Intelligent Contracts`

## English description

PresentmentCovenant is a contract-only GenLayer primitive for a bounded documentary presentation. An issuer locks exactly 2 GEN; a beneficiary submits an invoice envelope bound to its exact SHA-256 bytes; validators independently refetch a commit-addressed official DCSA synthetic eBL fixture and compare a structured examination. Deterministic code validates coverage and derives the consequence. A finalized COMPLIANT result creates one beneficiary credit, and withdrawal closes the purse. It does not prove commercial truth, signatures, legal enforceability, sanctions, fraud, or adoption.

## Contract and tests

- Primary contract: `contracts/presentment_covenant.py`
- Public methods: **18** (**10** views, **8** writes)
- Direct tests: **13**
- Aggregate tests: **17**
- Aggregate local check: `npm run check` (lint, strict typecheck, schema emission, direct and evidence-parser tests)

## Links and evidence

- Repository: https://github.com/duclucky/presentment-covenant
- Primary contract Explorer: https://explorer-studio-dev.genlayer.com/address/0xCEF68c363B17E95ca5aCFF8f23d400e044fE0B93
- Deployment source commit: https://github.com/duclucky/presentment-covenant/commit/d6bbaa52443e42bfb95b7f71aaac44e18941efa0
- Deployed source SHA-256: `12cfc0e00eb8b62f1573880ee666d71cef51495481b9d43cd826b3780f59752f`
- Sanitized lifecycle evidence: `docs/evidence/studio-dev/deployment.json`
- Fresh canonical state verification: `docs/evidence/studio-dev/final-verification.json`
- Target schema preflight: `docs/evidence/studio-dev/target-network-preflight.json`
- CI link: **not configured**; local `npm run check` passed.

## What validators inspect

The leader and independent validator fetch only the frozen DCSA URL, recompute the exact source digest, parse the JSON, and compare normalized status, exhaustive expected document IDs, allowed discrepancy codes, and source digest. Invoice bytes are checked against the beneficiary-supplied digest and role/credit bindings. Invalid, unavailable, mismatched, or contradictory evidence stays non-penalizing and cannot move value.

## Finalized consequence

The matching Studio Dev source finalized as `COMPLIANT`. Withdrawal transaction `0x633bc5e59f7ba4eddfa1ee7a87e8b353a34c688728d2958b999b5f6d22c73d3a` emitted a finalized external transfer of exactly 2 GEN (`0xdf70605873123d7b548826ed609d06e3a12f06dc043a7a6a8acd92461e456c88`) to the beneficiary. Close transaction `0x1a5422d4c687c14d23fb4fbfe5692af8649ce4d5c2ce46b913b0a160388f8755` finalized successfully. Canonical state is `CLOSED`, liability and withdrawable credits are zero, and `total_withdrawn` is exactly 2 GEN.

## Reuse value

Deploy one isolated instance per documentary mandate; replace the reviewed source/profile constants only through a new compatibility fingerprint; keep the same fail-closed adjudication, bounded retry/cure/waiver, canonical accounting, withdrawal, and closure pattern. A consumer remains responsible for its own authorization and downstream effects.

## Honest limits

The fixture is synthetic conformance data, not a real bill of lading or commercial authority. The invoice sender is authenticated as the envelope author, not as proof of invoice truth. The contract does not verify goods, title, shipment, legal effect, signatures beyond transaction authorship, sanctions, fraud, fiat settlement, or adoption. No frontend is included by the locked track.

`portal_submit_performed: false` — final Portal Submit remains explicitly action-authorized and was not performed.

## Copy-ready Portal fields

**Title:** `PresentmentCovenant — Adjudicable Documentary Presentment`

**Notes / Description:**

`PresentmentCovenant is a reusable, contract-only GenLayer primitive for bounded documentary presentment. An issuer locks exactly 2 GEN; a beneficiary submits invoice bytes bound by SHA-256; validators independently refetch a commit-addressed official DCSA synthetic eBL fixture and compare a structured examination. Deterministic checks enforce exact evidence coverage and derive the consequence. Cure and unverifiable-retry windows are ordered before the final adjudication deadline, so every accepted transition remains adjudicable. The matching Studio Dev deployment finalized COMPLIANT, transferred exactly 2 GEN through a finalized EVM message, and closed with zero liability. Limits: synthetic fixture, no commercial-truth, legal-effect, sanctions, fraud, fiat-settlement, or adoption claim.`

**Evidence URL:** `https://explorer-studio-dev.genlayer.com/address/0xCEF68c363B17E95ca5aCFF8f23d400e044fE0B93`
