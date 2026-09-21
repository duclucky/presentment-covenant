# Architecture

`activate_credit` -> `submit_presentation` -> `adjudicate` -> (`COMPLIANT` credit | `DISCREPANT_OPEN` waiver/cure | `UNVERIFIABLE_OPEN` retry) -> `withdraw` -> `close_credit`. Deadline order is `activation < presentation < waiver <= cure <= retry < adjudication`; adjudication is deliberately last so a cure or retry accepted in its own window cannot strand the contract in `PRESENTED`.

The adjudication boundary is:

1. deterministic code loads the immutable profile, expected IDs, source URL/digest, invoice digest, sender, and deadlines;
2. a nondeterministic leader fetches the commit-addressed DCSA bytes and asks for a bounded JSON result;
3. validators independently repeat the fetch and examination, agreeing only on normalized decision fields and exact source digest;
4. deterministic code rejects malformed or semantically inconsistent output before any value movement;
5. only the derived status changes the state machine; prose is stored only as a bounded audit explanation.

All web/LLM calls are inside `gl.vm.run_nondet`; storage writes, transfers, and state consequences remain outside the nondeterministic functions.

The contract deliberately has no frontend, callback consumer, or second contract. Consumers read canonical views and implement their own role checks.
