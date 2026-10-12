param([ValidateSet('phone','webrtc','text')][string]$Channel='text')
$taskRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$taskPython = Join-Path $taskRoot 'baseline/sdk-0.47.0/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) { throw 'Pinned SDK runtime is missing.' }
Write-Host 'Synthetic patient: 1001; code: 4242.'
Write-Host 'Readback challenge only: synthetic test PAN 4111111111111111; CVV 123. Never use a real card.'
Write-Host 'Guide: http://127.0.0.1:8765/docs/manual-validation-script.md'
if ($Channel -ne 'text') {
 $taskExisting = Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' -and $_.CommandLine -like '*harborcare.py*' -and $_.CommandLine -like ('*--mode ' + $Channel + '*') }
 if ($taskExisting) { Write-Host ('Existing ' + $Channel + ' listener is running. Reuse it.'); return }
}
Push-Location $taskRoot
try { & $taskPython agent/harborcare.py --mode $Channel } finally { Pop-Location }
