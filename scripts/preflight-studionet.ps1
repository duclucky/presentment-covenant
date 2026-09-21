$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:GENVM_VERSION = "v0.6.0-rc5"
$lint = ".\.venv\Scripts\genvm-lint.exe"
$python = ".\.venv\Scripts\python.exe"

New-Item -ItemType Directory -Force .gltest-artifacts, docs/evidence/studio-dev | Out-Null

Write-Host "Checking locked runner, class recognition, and typecheck"
& $lint check contracts/presentment_covenant.py --json
if ($LASTEXITCODE -ne 0) { throw "contract lint failed" }
& $lint typecheck contracts/presentment_covenant.py --strict --json
if ($LASTEXITCODE -ne 0) { throw "contract typecheck failed" }
& $lint schema contracts/presentment_covenant.py --json --output .gltest-artifacts/presentment_covenant.schema.json
if ($LASTEXITCODE -ne 0) { throw "local schema generation failed" }

Write-Host "Selecting and inspecting the locked Studio Dev profile"
$profileJson = & $python -c "from genlayer_py.chains import studio_devnet; import json; print(json.dumps({'rpc': studio_devnet.rpc_urls['default']['http'][0], 'chain_id': studio_devnet.id}))"
$profile = $profileJson | ConvertFrom-Json
$rpc = [string]$profile.rpc
$chainId = [string]$profile.chain_id
if ([string]::IsNullOrWhiteSpace($rpc) -or [string]::IsNullOrWhiteSpace($chainId)) { throw "unable to resolve current Studio Dev profile" }
if ($chainId -ne "61997") { throw "locked Studio Dev chain id drifted: $chainId" }

$contractPath = (Resolve-Path "contracts/presentment_covenant.py").Path
$sourceBytes = [IO.File]::ReadAllBytes($contractPath)
$sourceHash = (Get-FileHash $contractPath -Algorithm SHA256).Hash.ToLowerInvariant()
$hex = "0x" + (($sourceBytes | ForEach-Object { $_.ToString("x2") }) -join "")
$request = @{ jsonrpc = "2.0"; id = 1; method = "gen_getContractSchemaForCode"; params = @($hex) } |
    ConvertTo-Json -Compress
$response = Invoke-RestMethod -Uri $rpc -Method Post -ContentType "application/json" -Body $request
if ($null -ne $response.error) { throw "Studio Dev schema RPC returned an error" }
$response.result | ConvertTo-Json -Depth 30 | Set-Content -Encoding utf8 .gltest-artifacts/target_schema.json

$localCanonical = & $python -c "import json; print(json.dumps(json.load(open('.gltest-artifacts/presentment_covenant.schema.json',encoding='utf-8-sig')),sort_keys=True,separators=(',',':')))"
$remoteCanonical = & $python -c "import json; print(json.dumps(json.load(open('.gltest-artifacts/target_schema.json',encoding='utf-8-sig')),sort_keys=True,separators=(',',':')))"
if ($localCanonical -ne $remoteCanonical) { throw "target schema differs from local schema" }

$localSchemaHash = (Get-FileHash .gltest-artifacts/presentment_covenant.schema.json -Algorithm SHA256).Hash.ToLowerInvariant()
$remoteSchemaHash = (Get-FileHash .gltest-artifacts/target_schema.json -Algorithm SHA256).Hash.ToLowerInvariant()
$checkedAt = (Get-Date).ToUniversalTime().ToString("o")
$evidence = [ordered]@{
    kind = "target_network_preflight"
    network = "studio-dev"
    chain_id = 61997
    rpc = $rpc
    explorer = "https://explorer-studio-dev.genlayer.com"
    checked_at_utc = $checkedAt
    runner_version = "v0.6.0-rc5"
    depends_hash = "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng"
    source_sha256 = $sourceHash
    local_schema_sha256 = $localSchemaHash
    target_schema_sha256 = $remoteSchemaHash
    schema_match = $true
    constructor_abi = "9 string parameters; role strings are converted to validated native Address values inside the contract"
    write_methods_checked = @("activate_credit", "submit_presentation", "adjudicate", "waive_discrepancies", "retry_unverifiable", "expire_credit", "withdraw", "close_credit")
    status = "READ_ONLY_PREFLIGHT_PASSED"
}
$evidence | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 docs/evidence/studio-dev/target-network-preflight.json
Write-Host "Studio Dev preflight passed: chain 61997, schema match, evidence written to docs/evidence/studio-dev/target-network-preflight.json"
