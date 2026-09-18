# Copy-ready submission packet

## Category

`Intelligent Contracts`

## English description

PresentmentCovenant is a contract-only GenLayer primitive for a bounded documentary presentation. An issuer locks exactly 2 GEN; a beneficiary submits an invoice envelope bound to its exact SHA-256 bytes; validators independently refetch a commit-addressed official DCSA synthetic eBL fixture and compare a structured examination. Deterministic code validates coverage and derives the consequence. A finalized COMPLIANT result creates one beneficiary credit, and withdrawal closes the purse. It does not prove commercial truth, signatures, legal enforceability, sanctions, fraud, or adoption.

## Contract and tests

- Primary contract: `contracts/presentment_covenant.py`
- Public methods: **18** (**10** views, **8** writes)
- Direct tests: **10**
- Aggregate local check: `npm run check` (lint, schema emission, direct tests)

## Links and evidence

- Repository: **not published**; local project root is `ideation-lab/demand-mechanism-forge/presentment-covenant`. Publication and CI require a separate authorization.
- Primary contract Explorer: https://genlayer-explorer.vercel.app/address/0x77BBd0FaF7600bD1dD23087B6D6E76D332683CB2
- Deployment source commit: `25911bf991c2a372df74de49c8daccf180815bff` (contract source SHA-256 is recorded in the lifecycle evidence)
- Sanitized lifecycle evidence: `docs/evidence/studionet/deployment.json`
- Fresh canonical state verification: `docs/evidence/studionet/final-verification.json`
- Target schema preflight: `docs/evidence/studionet/target-network-preflight.json`
- CI link: **not available** (no remote repository); local `npm run check` passed.

## What validators inspect

The leader and independent validator fetch only the frozen DCSA URL, recompute the exact source digest, parse the JSON, and compare normalized status, exhaustive expected document IDs, allowed discrepancy codes, and source digest. Invoice bytes are checked against the beneficiary-supplied digest and role/credit bindings. Invalid, unavailable, mismatched, or contradictory evidence stays non-penalizing and cannot move value.

## Finalized consequence

The recorded Studionet run finalized deployment, activation, presentation, adjudication (`COMPLIANT`), beneficiary withdrawal of exactly 2 GEN, and closure. Final canonical state is `CLOSED`, `total_withdrawn = 2 GEN`, and `zero_liability = true`.

## Reuse value

Deploy one isolated instance per documentary mandate; replace the reviewed source/profile constants only through a new compatibility fingerprint; keep the same fail-closed adjudication, bounded retry/cure/waiver, canonical accounting, withdrawal, and closure pattern. A consumer remains responsible for its own authorization and downstream effects.

## Honest limits

The fixture is synthetic conformance data, not a real bill of lading or commercial authority. The invoice sender is authenticated as the envelope author, not as proof of invoice truth. The contract does not verify goods, title, shipment, legal effect, signatures beyond transaction authorship, sanctions, fraud, fiat settlement, or adoption. No frontend is included by the locked track.

`portal_submit_performed: false` — final Portal Submit remains explicitly action-authorized and was not performed.
