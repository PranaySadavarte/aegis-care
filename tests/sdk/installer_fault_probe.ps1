param([ValidateSet('before-write','partial-write')][string]$Mode='partial-write')
$ErrorActionPreference='Stop'
$RepoRoot=(Get-Location).Path
$CaseRoot=[IO.Path]::GetFullPath((Join-Path $RepoRoot ('evidence\2026-10-11\extended-sdk\installer-'+$Mode+'-'+[guid]::NewGuid().ToString('N'))))
$EvidenceRoot=[IO.Path]::GetFullPath((Join-Path $RepoRoot 'evidence\2026-10-11\extended-sdk'))
if (-not $CaseRoot.StartsWith($EvidenceRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe test root' }
New-Item -ItemType Directory -Path $CaseRoot | Out-Null
$Dest=Join-Path $CaseRoot 'guava.exe'
[IO.File]::WriteAllText($Dest,'SYNTHETIC PRIOR FILE - NOT AN EXECUTABLE')
$Before=(Get-FileHash -LiteralPath $Dest -Algorithm SHA256).Hash
$UserPathBefore=[Environment]::GetEnvironmentVariable('PATH','User')
$env:GUAVA_INSTALL_DIR=$CaseRoot
$env:GUAVA_VERSION='0.47.0'
function Invoke-WebRequest {
 param($Uri,$OutFile,[switch]$UseBasicParsing)
 $Resolved=[IO.Path]::GetFullPath($OutFile)
 if ($Resolved -ne $Dest) {throw 'Unexpected download destination'}
 if ($Mode -eq 'partial-write') {[IO.File]::WriteAllText($Resolved,'SYNTHETIC INTERRUPTED DOWNLOAD')}
 throw 'AEGIS synthetic download fault; no network, no binary execution'
}
try { . (Join-Path $RepoRoot 'evidence\2026-10-11\installer-audit\install-current.ps1') } catch { $Fault=$_.Exception.Message }
$After=(Get-FileHash -LiteralPath $Dest -Algorithm SHA256).Hash
$Row=[ordered]@{mode=$Mode;version='0.47.0';installer_sha256=(Get-FileHash -LiteralPath (Join-Path $RepoRoot 'evidence\2026-10-11\installer-audit\install-current.ps1')).Hash;prior_file_preserved=($Before -eq $After);user_path_unchanged=($UserPathBefore -eq [Environment]::GetEnvironmentVariable('PATH','User'));fault=$Fault;scope='Current official installer control flow with mocked download failure; synthetic destination only; original install untouched'}
$Row | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $CaseRoot 'result.json') -Encoding UTF8
$Row | ConvertTo-Json -Compress
