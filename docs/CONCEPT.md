# Concept and honest boundary

## Trust problem

When an issuing-bank role prefunds a documentary-presentation purse, the beneficiary and applicant need a shared, replay-resistant result. A single bank operator, oracle, expert, or AI process must not unilaterally rewrite the locked credit terms or decide a consequential result from an unbound summary.

## Frozen MVP

One contract instance represents one documentary credit. The issuer is the deployer; applicant and beneficiary are constructor-bound addresses. Activation locks exactly 2 GEN. The only external source is the DCSA commit-addressed synthetic eBL fixture recorded in `docs/SOURCE-LOCK.md`. The beneficiary invoice is supplied in a transaction envelope, bound to the beneficiary sender and an exact SHA-256 digest. Validators refetch the DCSA bytes and independently perform the same bounded semantic examination over the locked rule profile and exact invoice bytes.

## Consequence

After finalized consensus, successful execution, exact source digest, exhaustive expected-document coverage, allowed discrepancy codes, and root/class consistency:

- `COMPLIANT` creates exactly one beneficiary credit for the locked 2 GEN purse.
- `DISCREPANT_OPEN` leaves the purse locked for applicant waiver or a bounded beneficiary cure.
- `UNVERIFIABLE_OPEN` leaves the purse locked and permits a bounded retry without penalty.
- Expiry creates exactly one issuer refund credit.
- Pull withdrawal debits the credit before an external GEN transfer; closure is possible only at zero liability.

No LLM text supplies an amount, destination, authority, or state. The contract derives all of those from immutable state.

## Explicit exclusions

The contract does not verify the truth of goods, shipment, title, payment, sanctions, fraud, signatures beyond the transaction-bound invoice envelope, legal enforceability, governing law, full UCP/ISBP compliance, bank compulsion, fiat settlement, or adoption.
