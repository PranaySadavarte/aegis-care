param([string]$InputJson,[string]$OutputWav)
$taskRoot = 'C:\Users\prana\aegis-care\evidence\2026-10-11'
foreach ($taskPath in @($InputJson,$OutputWav)) {
 $resolvedPath = [IO.Path]::GetFullPath($taskPath)
 if (-not $resolvedPath.StartsWith($taskRoot + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Review synthesis paths must remain inside project evidence.' }
}
$request = Get-Content -LiteralPath $InputJson -Raw -Encoding UTF8 | ConvertFrom-Json
$voice = New-Object -ComObject SAPI.SpVoice
$stream = New-Object -ComObject SAPI.SpFileStream
try {
 $stream.Format.Type = 18
 $stream.Open($OutputWav,3)
 $voice.AudioOutputStream = $stream
 $voice.Speak([string]$request.text) | Out-Null
} finally { $stream.Close() }
