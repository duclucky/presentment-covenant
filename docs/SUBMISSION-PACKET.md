# Copy-ready submission packet

## Category

`Intelligent Contracts`

## English description

PresentmentCovenant is a contract-only GenLayer primitive for a bounded documentary presentation. An issuer locks exactly 2 GEN; a beneficiary submits an invoice envelope bound to its exact SHA-256 bytes; validators independently refetch a commit-addressed official DCSA synthetic eBL fixture and compare a structured examination. Deterministic code validates coverage and derives the consequence. A finalized COMPLIANT result creates one beneficiary credit, and withdrawal closes the purse. It does not prove commercial truth, signatures, legal enforceability, sanctions, fraud, or adoption.

## Contract and tests

- Primary contract: `contracts/presentment_covenant.py`
- Public methods: **18** (**10** views, **8** writes)
- Direct tests: **12**
- Aggregate local check: `npm run check` (lint, schema emission, direct tests)

## Links and evidence

- Repository: https://github.com/duclucky/presentment-covenant
- Primary contract Explorer: **pending corrected Studio Dev deployment**
- Deployment source commit: **pending corrected source commit**
- Sanitized lifecycle evidence: `docs/evidence/studio-dev/deployment.json` (created only after finalization)
- Fresh canonical state verification: `docs/evidence/studio-dev/final-verification.json` (created only after finalization)
- Target schema preflight: `docs/evidence/studio-dev/target-network-preflight.json`
- CI link: **not configured**; local `npm run check` passed.

## What validators inspect

The leader and independent validator fetch only the frozen DCSA URL, recompute the exact source digest, parse the JSON, and compare normalized status, exhaustive expected document IDs, allowed discrepancy codes, and source digest. Invoice bytes are checked against the beneficiary-supplied digest and role/credit bindings. Invalid, unavailable, mismatched, or contradictory evidence stays non-penalizing and cannot move value.

## Finalized consequence

No corrected Studio Dev consequence is claimed until the matching deployment and canonical reads finalize. The legacy Studionet run is historical and is not evidence for this corrected source.

## Reuse value

Deploy one isolated instance per documentary mandate; replace the reviewed source/profile constants only through a new compatibility fingerprint; keep the same fail-closed adjudication, bounded retry/cure/waiver, canonical accounting, withdrawal, and closure pattern. A consumer remains responsible for its own authorization and downstream effects.

## Honest limits

The fixture is synthetic conformance data, not a real bill of lading or commercial authority. The invoice sender is authenticated as the envelope author, not as proof of invoice truth. The contract does not verify goods, title, shipment, legal effect, signatures beyond transaction authorship, sanctions, fraud, fiat settlement, or adoption. No frontend is included by the locked track.

`portal_submit_performed: false` — final Portal Submit remains explicitly action-authorized and was not performed.
