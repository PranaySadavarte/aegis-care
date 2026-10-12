$taskRoot=Split-Path $PSScriptRoot -Parent
$taskPython=Join-Path $taskRoot 'baseline/sdk-0.47.0/.venv/Scripts/python.exe'
if (-not (Test-Path $taskPython)) { throw 'Run scripts/setup-windows.ps1 first.' }
Write-Host 'Dashboard: http://127.0.0.1:8765/dashboard/'
Push-Location $taskRoot
try { & $taskPython dashboard/serve.py } finally { Pop-Location }
