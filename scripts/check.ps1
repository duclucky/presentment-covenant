$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:GENVM_VERSION = "v0.2.16"

Write-Host "[1/4] GenVM lint + class recognition"
genvm-lint check contracts/presentment_covenant.py --json
if ($LASTEXITCODE -ne 0) { throw "genvm-lint check failed" }

Write-Host "[2/4] Strict typecheck"
genvm-lint typecheck contracts/presentment_covenant.py --strict --json
if ($LASTEXITCODE -ne 0) { throw "strict typecheck failed" }

Write-Host "[3/4] ABI schema emission"
New-Item -ItemType Directory -Force artifacts | Out-Null
genvm-lint schema contracts/presentment_covenant.py --json --output artifacts/presentment_covenant.schema.json
if ($LASTEXITCODE -ne 0) { throw "genvm-lint schema failed" }

Write-Host "[4/4] Direct-mode adversarial lifecycle tests"
pytest tests/direct/ -q
if ($LASTEXITCODE -ne 0) { throw "direct tests failed" }

Write-Host "Contract checks passed. Track is Intelligent Contracts; no frontend build is in scope."
