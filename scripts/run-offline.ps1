$taskRoot=Split-Path $PSScriptRoot -Parent
$taskPython=Join-Path $taskRoot 'baseline/sdk-0.47.0/.venv/Scripts/python.exe'
if (-not (Test-Path $taskPython)) { throw 'Run scripts/setup-windows.ps1 first.' }
Push-Location $taskRoot
try { & $taskPython scripts/run_offline.py; exit $LASTEXITCODE } finally { Pop-Location }
