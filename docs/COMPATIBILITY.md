# Compatibility matrix (frozen before implementation)

| Component | Locked fact | Evidence / boundary |
|---|---|---|
| Target network | Studionet, chain ID 61999 | official network docs; current source lock |
| Runtime | `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6` | write-contract skill and current runner guidance |
| Contract API | `from genlayer import *`, one `gl.Contract` subclass, `TreeMap`, `DynArray`, `u256`, `gl.vm.run_nondet_unsafe` | official first-contract/equivalence docs |
| Linter | `genvm-linter 0.11.0`, `genvm-lint check` | observed local executable and version |
| Direct SDK | `genlayer-test 0.29.2`, pytest fixtures | observed local package and official testing docs |
| Python | system Python 3.13.14; official requirement is 3.12+ | no Python 3.12 interpreter was available; 3.13 is within stated lower-bound support |
| CLI | installed `genlayer` command; built-in network selection required | CLI skill; no custom RPC override |
| Receipt policy | `SUBMITTED -> ACCEPTED -> FINALIZED`; execution success is separate | official deployment/testing docs |
| Source endpoint | commit-addressed GitHub raw DCSA Conformance-Gateway fixture | exact URL, 200 response, 2588 bytes, SHA-256 below |
| ABI evidence | local schema and `gen_getContractSchemaForCode` target result match exactly; all eight writes are enumerated | `docs/evidence/studionet/target-network-preflight.json`; read-only preflight passed 2026-09-17T23:54:19Z |

The contract/API/runtime row is an inseparable versioned unit. Any change requires a new fingerprint and deployment revision.
