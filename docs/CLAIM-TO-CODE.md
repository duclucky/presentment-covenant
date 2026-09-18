# Claim-to-code map

| Claim | State transition / code | Canonical view | Test | Evidence |
|---|---|---|---|---|
| Roles and configuration are immutable after activation | `__init__`, `activate_credit` | `get_credit`, `get_rule_profile` | access and mutation rejection | local verification record |
| Only the beneficiary can submit its invoice envelope | `submit_presentation` | `get_evidence_binding` | wrong caller, digest mismatch, replay | direct test report |
| Validators inspect exact source bytes and invoice bytes | `adjudicate`, `run_nondet_unsafe` | `get_attempt` | source mismatch, prompt injection, validator disagreement | target-network evidence when available |
| Settlement output is exhaustive and bounded | `_normalize_verdict`, `adjudicate` | `get_discrepancies` | missing/extra/duplicate/invalid IDs and codes | direct adversarial tests |
| COMPLIANT is the only beneficiary entitlement path | `adjudicate`, `waive_discrepancies` | `get_accounting`, `get_withdrawable` | compliant and waiver conservation | lifecycle evidence |
| Missing or unauthenticated evidence is non-penalizing | `submit_presentation`, `adjudicate` | `get_credit`, `get_accounting` | unavailable/mismatch keeps purse locked | lifecycle evidence |
| Expiry refunds the issuer exactly once | `expire_credit` | `get_accounting` | boundary and duplicate expiry | lifecycle evidence |
| Withdrawals cannot double-credit or orphan value | `withdraw` | `get_withdrawable`, `is_closable` | duplicate/failed transfer/closure invariants | lifecycle evidence |
| This is a reusable contract primitive, not a bank product | repository boundary and docs | all public views | public-hygiene scan | README and source-lock record |
