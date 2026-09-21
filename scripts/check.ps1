$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:GENVM_VERSION = "v0.6.0-rc5"
$lint = ".\.venv\Scripts\genvm-lint.exe"
$python = ".\.venv\Scripts\python.exe"

Write-Host "[1/4] GenVM lint + class recognition"
& $lint check contracts/presentment_covenant.py --json
if ($LASTEXITCODE -ne 0) { throw "genvm-lint check failed" }

Write-Host "[2/4] Strict typecheck"
& $lint typecheck contracts/presentment_covenant.py --strict --json
if ($LASTEXITCODE -ne 0) { throw "strict typecheck failed" }

Write-Host "[3/4] ABI schema emission"
New-Item -ItemType Directory -Force .gltest-artifacts | Out-Null
& $lint schema contracts/presentment_covenant.py --json --output .gltest-artifacts/presentment_covenant.schema.json
if ($LASTEXITCODE -ne 0) { throw "genvm-lint schema failed" }

Write-Host "[4/4] Direct-mode adversarial lifecycle tests"
& $python -m pytest tests/direct/ -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw "direct tests failed" }

Write-Host "Contract checks passed. Track is Intelligent Contracts; no frontend build is in scope."
