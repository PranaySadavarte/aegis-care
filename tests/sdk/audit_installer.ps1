# Installer static evaluation — does not execute installer or modify CLI
param([Parameter(Mandatory=$true)][string]$InstallerPath)
$source = Get-Content -LiteralPath $InstallerPath -Raw
$tokens = $null
$parseErrors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseInput($source, [ref]$tokens, [ref]$parseErrors)
$commands = $ast.FindAll({ param($node) $node -is [System.Management.Automation.Language.CommandAst] }, $true)
$names = @($commands | ForEach-Object { $_.GetCommandName() })
[ordered]@{
 syntax_parse = if ($parseErrors.Count -eq 0) { 'PASS' } else { 'FAIL' }
 explicit_hash_verification_command_present = [bool]($names -match 'Get-FileHash|certutil|openssl')
 explicit_authenticode_command_present = [bool]($names -match 'Get-AuthenticodeSignature')
 broader_integrity_keywords_present = [bool]($source -match '(?i)sha256|checksum|authenticode|verifyhash|signature')
 direct_destination_download_present = [bool]($source -match 'Invoke-WebRequest.*-OutFile\s+\$Dest')
 rollback_or_atomic_replace_keywords_present = [bool]($source -match '(?i)Move-Item|Replace\(|rollback|backup|\.tmp')
 limitation = 'Static indicators plus manual whole-source review; no installer execution or failure injection. Keyword absence alone is not proof of all possible verification paths.'
} | ConvertTo-Json
