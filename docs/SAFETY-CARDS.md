# Write-method safety cards

| Method | Caller / states | Time and idempotency | Value / views | Required negatives |
|---|---|---|---|---|
| `activate_credit` | issuer; `DRAFT` only | `now < activation_deadline`; one use | payable exactly 2 GEN; `get_credit`, `get_accounting` | wrong caller/state/value; boundary -1/equal/+1 |
| `submit_presentation` | beneficiary; `ACTIVE` or cure-eligible `DISCREPANT_OPEN` | initial `now < presentation_deadline`; cure `now < cure_deadline`; constructor guarantees `cure_deadline < adjudication_deadline`; presentation ID one use | nonpayable; evidence/presentation views | wrong caller, schema/digest/origin/replay, boundary tripwire, cure remains adjudicable |
| `adjudicate` | permissionless; `PRESENTED` or retryable `UNVERIFIABLE_OPEN` | `now < adjudication_deadline`, which is strictly after retry; attempt nonce one use | no movement unless validated `COMPLIANT`; attempt/discrepancy/accounting views | malformed or malicious output, digest mismatch, duplicate, boundary |
| `waive_discrepancies` | applicant; `DISCREPANT_OPEN` | `now < waiver_deadline`; one use | entire locked purse -> beneficiary credit | caller/state/expiry/duplicate/conservation |
| `retry_unverifiable` | beneficiary; `UNVERIFIABLE_OPEN` | `now < retry_deadline < adjudication_deadline`; max 3 attempts | no movement | changed evidence, exhausted retry, caller/state/boundary, retry remains adjudicable |
| `expire_credit` | permissionless; live non-entitled states | `now >= adjudication_deadline`; one refund | entire locked purse -> issuer refund credit | early/equal/late, duplicate, after entitlement |
| `withdraw` | owner of nonzero credit; `COMPLIANT` or `REFUNDABLE` | N/A; credit itself is gate | zero credit before EOA transfer | wrong caller, duplicate, failed transfer, no double debit |
| `close_credit` | issuer; `WITHDRAWN` or `REFUNDED` | N/A; zero-liability gate | no value; records `CLOSED` | nonzero liability, active attempt, duplicate |

All methods leave canonical state and accounting unchanged on rejected calls. Recovery methods are treated as value transitions, not helpers.
