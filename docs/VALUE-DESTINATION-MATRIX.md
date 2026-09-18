# Value-destination matrix

| Value | Source / lock | Release | Terminal proof | Duplicate / late behavior |
|---|---|---|---|---|
| 2 GEN purse | Issuer payable `activate_credit`; `locked_purse` | COMPLIANT or waiver -> beneficiary credit; expiry -> issuer refund credit | `get_accounting` and `get_withdrawable` | wrong amount, wrong state, late activation, duplicate activation revert |
| Beneficiary credit | Locked purse only; amount never an argument | `withdraw` to beneficiary EOA | `beneficiary_credit=0`, `total_withdrawn`, terminal `WITHDRAWN` | wrong caller/zero credit/duplicate withdraw revert |
| Issuer refund credit | Locked purse only after eligible expiry | `withdraw` to issuer EOA | `issuer_refund_credit=0`, terminal `REFUNDED` | before final deadline or duplicate expiry revert |
| Residual / remainder | None: all amounts are exact fixed whole-purse transfers | Not applicable | accounting invariant `locked + credits + withdrawn = purse` | no arbitrary residual path |
