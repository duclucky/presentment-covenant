# Compatibility matrix (frozen before implementation)

| Component | Locked fact | Evidence / boundary |
|---|---|---|
| Target network | Studio Dev, chain ID 61997 | official Consensus v0.6 migration docs; current source lock |
| Runtime | `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`, GenVM manager `v0.6.0-rc5` | current official runner bundle and target schema preflight |
| Contract API | `import genlayer as gl`, one `gl.contract.Contract` subclass, `gl.storage.TreeMap`, `gl.storage.DynArray`, `u256`, `gl.vm.run_nondet` | current v0.3 runner SDK |
| Linter | `genvm-linter 0.11.1rc2`, `genvm-lint check` | exact requirement pin and observed venv package |
| Direct SDK | `genlayer-test 0.30.0rc2`, pytest fixtures | exact requirement pin and observed venv package |
| Python | repository `.venv`, Python 3.12.13 | current RC toolchain requirement |
| Client / CLI | `genlayer-py 0.19.0rc2`; CLI `0.40.0-rc.3`; Studio Dev profile only | official coherent RC family; no custom network substitution |
| Receipt policy | `SUBMITTED -> ACCEPTED -> FINALIZED`; execution success is separate | official deployment/testing docs |
| Source endpoint | commit-addressed GitHub raw DCSA Conformance-Gateway fixture | exact URL, 200 response, 2588 bytes, SHA-256 below |
| ABI evidence | canonical local schema and `gen_getContractSchemaForCode` Studio Dev result match; all eight writes are enumerated | `docs/evidence/studio-dev/target-network-preflight.json`; read-only preflight passed 2026-09-21T10:30:56Z |

The contract/API/runtime row is an inseparable versioned unit. Any change requires a new fingerprint and deployment revision.
