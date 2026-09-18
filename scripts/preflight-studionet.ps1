$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:GENVM_VERSION = "v0.2.16"

New-Item -ItemType Directory -Force artifacts, docs/evidence/studionet | Out-Null

Write-Host "Checking locked runner, class recognition, and typecheck"
genvm-lint check contracts/presentment_covenant.py --json
if ($LASTEXITCODE -ne 0) { throw "contract lint failed" }
genvm-lint typecheck contracts/presentment_covenant.py --strict --json
if ($LASTEXITCODE -ne 0) { throw "contract typecheck failed" }
genvm-lint schema contracts/presentment_covenant.py --json --output artifacts/presentment_covenant.schema.json
if ($LASTEXITCODE -ne 0) { throw "local schema generation failed" }

Write-Host "Selecting and inspecting the locked Studionet profile"
$profileJson = python -c "from genlayer_py import studionet; import json; print(json.dumps({'rpc': studionet.rpc_urls['default']['http'][0], 'chain_id': studionet.id}))"
$profile = $profileJson | ConvertFrom-Json
$rpc = [string]$profile.rpc
$chainId = [string]$profile.chain_id
if ([string]::IsNullOrWhiteSpace($rpc) -or [string]::IsNullOrWhiteSpace($chainId)) { throw "unable to resolve current Studionet profile" }
if ($chainId -ne "61999") { throw "locked Studionet chain id drifted: $chainId" }

$contractPath = (Resolve-Path "contracts/presentment_covenant.py").Path
$sourceBytes = [IO.File]::ReadAllBytes($contractPath)
$sourceHash = (Get-FileHash $contractPath -Algorithm SHA256).Hash.ToLowerInvariant()
$hex = "0x" + (($sourceBytes | ForEach-Object { $_.ToString("x2") }) -join "")
$request = @{ jsonrpc = "2.0"; id = 1; method = "gen_getContractSchemaForCode"; params = @($hex) } |
    ConvertTo-Json -Compress
$response = Invoke-RestMethod -Uri $rpc -Method Post -ContentType "application/json" -Body $request
if ($null -ne $response.error) { throw "Studionet schema RPC returned an error" }
$response.result | ConvertTo-Json -Depth 30 | Set-Content -Encoding utf8 artifacts/target_schema.json

$localCanonical = python -c "import json; print(json.dumps(json.load(open('artifacts/presentment_covenant.schema.json',encoding='utf-8-sig')),sort_keys=True,separators=(',',':')))"
$remoteCanonical = python -c "import json; print(json.dumps(json.load(open('artifacts/target_schema.json',encoding='utf-8-sig')),sort_keys=True,separators=(',',':')))"
if ($localCanonical -ne $remoteCanonical) { throw "target schema differs from local schema" }

$localSchemaHash = (Get-FileHash artifacts/presentment_covenant.schema.json -Algorithm SHA256).Hash.ToLowerInvariant()
$remoteSchemaHash = (Get-FileHash artifacts/target_schema.json -Algorithm SHA256).Hash.ToLowerInvariant()
$checkedAt = (Get-Date).ToUniversalTime().ToString("o")
$evidence = [ordered]@{
    kind = "target_network_preflight"
    network = "studionet"
    chain_id = 61999
    rpc = $rpc
    explorer = "https://explorer-studio.genlayer.com"
    checked_at_utc = $checkedAt
    runner_version = "v0.2.16"
    depends_hash = "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"
    source_sha256 = $sourceHash
    local_schema_sha256 = $localSchemaHash
    target_schema_sha256 = $remoteSchemaHash
    schema_match = $true
    constructor_abi = "9 string parameters; role strings are converted to validated native Address values inside the contract"
    write_methods_checked = @("activate_credit", "submit_presentation", "adjudicate", "waive_discrepancies", "retry_unverifiable", "expire_credit", "withdraw", "close_credit")
    status = "READ_ONLY_PREFLIGHT_PASSED"
}
$evidence | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 docs/evidence/studionet/target-network-preflight.json
Write-Host "Studionet preflight passed: chain 61999, schema match, evidence written to docs/evidence/studionet/target-network-preflight.json"
