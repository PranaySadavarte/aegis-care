param([switch]$WithMetrics)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskUv=Get-Command uv -ErrorAction Stop
Push-Location $taskRoot
try {
 foreach ($taskArea in @('sdk-0.47.0','dashboard')) {
  $taskEnv=Join-Path $taskRoot ('baseline/'+$taskArea+'/.venv')
  if (-not (Test-Path (Join-Path $taskEnv 'Scripts/python.exe'))) {
   & $taskUv.Source venv --python 3.12 $taskEnv
   if ($LASTEXITCODE -ne 0) { throw 'Environment creation failed.' }
  }
  & $taskUv.Source pip sync --python (Join-Path $taskEnv 'Scripts/python.exe') (Join-Path $taskRoot ('baseline/'+$taskArea+'/requirements.lock.txt'))
  if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
 }
 if ($WithMetrics) {
  $taskMetrics=Join-Path $taskRoot 'baseline/metrics/.venv'
  & $taskUv.Source venv --python 3.12 $taskMetrics
  if ($LASTEXITCODE -ne 0) { throw 'Metrics environment creation failed.' }
  & $taskUv.Source pip sync --python (Join-Path $taskMetrics 'Scripts/python.exe') (Join-Path $taskRoot 'baseline/metrics/requirements.lock.txt')
  if ($LASTEXITCODE -ne 0) { throw 'Metrics installation failed.' }
 }
 & (Join-Path $taskRoot 'baseline/sdk-0.47.0/.venv/Scripts/python.exe') -c "from importlib.metadata import version; assert version('guava-sdk') == '0.47.0'; print('Guava SDK 0.47.0 ready')"
 if ($LASTEXITCODE -ne 0) { throw 'Version verification failed.' }
 Write-Host 'Ready. Run scripts/start-dashboard.ps1 or scripts/run-offline.ps1.'
} finally { Pop-Location }
