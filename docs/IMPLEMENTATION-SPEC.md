# Implementation specification (locked before code)

## Roles

`issuer` is captured from the deployment sender. `applicant` and `beneficiary` are immutable constructor arguments and must be nonzero and distinct. Anyone may trigger `adjudicate` or `expire_credit`; only the named role may activate, waive, submit, withdraw its own credit, or close.

## Immutable profile

The contract hardcodes the reviewed DCSA URL, its SHA-256 digest, profile version `pc-dcsa-synthetic-v1`, expected document IDs `dcsa-ebl` and `beneficiary-invoice`, discrepancy enums `DOCUMENT_FUNCTION`, `CROSS_DOCUMENT_CONFLICT`, `INVOICE_AMOUNT`, and `UNSUPPORTED`, and a fixed purse of 2 GEN (`2 * 10**18` wei). Constructor deadlines are ordered and are frozen at deployment.

## State machine

`DRAFT -> ACTIVE -> PRESENTED -> REVIEWING -> COMPLIANT | DISCREPANT_OPEN | UNVERIFIABLE_OPEN`.

`DISCREPANT_OPEN -> COMPLIANT` through applicant waiver or `DISCREPANT_OPEN -> PRESENTED` through a fresh valid presentation before the cure deadline. `UNVERIFIABLE_OPEN -> PRESENTED` through a bounded retry before the retry deadline. The constructor enforces `activation < presentation < waiver <= cure <= retry < adjudication`, so every accepted cure or retry has a non-empty adjudication interval. `ACTIVE | PRESENTED | DISCREPANT_OPEN | UNVERIFIABLE_OPEN -> REFUNDABLE` only at or after the final adjudication deadline. `COMPLIANT -> WITHDRAWN`, `REFUNDABLE -> REFUNDED`, then either terminal state -> `CLOSED` only after all balances are zero.

## Evidence and semantic output

The source response must be HTTP 200, bounded in size, exact SHA-256 equal to the locked DCSA digest, and parse as JSON with the locked DCSA document identity. The invoice digest must match the exact submitted UTF-8 bytes, parse as JSON, and contain `invoice_id`, `credit_id`, `beneficiary`, `applicant`, `amount_gen`, `currency`, and `goods_description`; the transaction sender authenticates authorship of the envelope but not commercial truth.

The LLM receives source JSON and invoice JSON inside explicit data delimiters and is instructed to ignore embedded directives. It must return only an object with `status`, `covered_document_ids`, `discrepancy_codes`, and `reason`. Normalization requires exactly the two expected IDs once each, zero or more allowed discrepancy codes, and status in `COMPLIANT`, `DISCREPANT`, or `UNVERIFIABLE`. A compliant result requires no discrepancy codes; a discrepant result requires at least one code; unverifiable is always non-penalizing. Any mismatch, missing field, extra ID, duplicate code, invalid enum, source digest mismatch, or validator disagreement resolves to `UNVERIFIABLE_OPEN` or reverts before consequence.

## Time policy

Every time-bounded write checks `gl.message.raw["datetime"]` directly. Equality at a deadline is late for activation, presentation, adjudication, waiver, cure, and retry; withdrawal does not use a deadline. The adjudication deadline is the final deadline, and expiry is eligible at equality (`now >= adjudication_deadline`). Regression tests prove cures accepted just before `cure_deadline` and retries accepted just before `retry_deadline` can still be adjudicated afterward.

## Value policy

Only activation is payable and must carry exactly 2 GEN. The purse is the sole liability. `COMPLIANT` or waiver moves the entire locked purse to the beneficiary credit; expiry moves it to issuer refund credit. `withdraw` sets the caller credit to zero and updates terminal accounting before emitting the exact amount to the caller's EOA. Failed transfers revert the transaction. No path can create an arbitrary amount or destination.
