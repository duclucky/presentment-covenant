# Evidence Authority Matrix

| Input | Authority and binding | Deterministic precheck | Consequential failure |
|---|---|---|---|
| Locked credit profile | Contract deployment and storage; issuer, applicant, beneficiary, deadlines, purse, profile, expected IDs and source digest are immutable | role, ordering, nonzero addresses, fixed purse | revert; no state/value change |
| DCSA synthetic eBL | Commit-addressed official DCSA Conformance-Gateway raw JSON; URL and SHA-256 digest are hardcoded | HTTP 200, bounded bytes, exact digest, JSON identity and required fields | `UNVERIFIABLE_OPEN`; no payout/refund/penalty |
| Beneficiary invoice | Beneficiary transaction sender authenticates exact envelope bytes; SHA-256 digest and presentation/credit IDs bind it | sender, digest, schema, amount/currency syntax, replay and size | revert on envelope invalidity; no state/value change |
| Presentation time | Native transaction timestamp and sender | method-specific `< deadline` checks | revert; no mutation |
| Validator output | GenLayer leader/validator consensus over refetched source and exact invoice bytes | exhaustive IDs, allowed enums, class/code consistency, no arbitrary amount/destination | `UNVERIFIABLE_OPEN`; purse stays locked |

Hashes establish exact bytes only; the DCSA URL and issuer profile establish the authority boundary. The invoice's sender binding establishes authorship, not truth. No actor-supplied prose can redefine authority, payout, or objective.
