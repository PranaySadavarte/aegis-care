# Windows CLI / installer audit — 2026-10-11
Current step: SDK/CLI baseline and installer static security evaluation. No healthcare code changes.

## Executed checks and findings
CLI found at standard LOCALAPPDATA/guava/bin/guava.exe. Direct version query succeeds: guava 0.47.0. Previous PATH resolution failure did not mean installation was absent.
Binary size 5155328 bytes; SHA256 61BF547AC29984D26B876749BA63B7D24C637DA3A42816C1C866C63EF00EDAEA.
Get-AuthenticodeSignature returns NotSigned and no signer certificate.
CLI-F001: confirmed lack of Authenticode signature on this exact installed binary. Owner: Guava CLI release engineering. This establishes a missing publisher signature, not tampering or exploitation. Authentication and binary provenance are not verified by --version.

Current official installer retrieved from https://goguava.ai/install.ps1 and preserved without execution.
Installer SHA256 55D89800714FCE05FF4CD40946F705A24B214E73D409437E37FBE9CFE96A3502.
CLI-F002: whole-source review plus static checks confirms no explicit downloaded-binary checksum comparison or Authenticode verification in this retrieved script. Owner: Guava installer/release engineering.
Expected: project security criterion requires integrity/publisher verification before trusting installed executables.
Actual: script resolves version, creates directory, downloads executable directly to destination, then updates PATH; optional sample-project executes downloaded binary.
HTTPS is present; absent additional verification does not establish compromised transport. Locally computed hashes preserve evidence but are not independently authenticated expected release hashes.
Original installer used for the local 0.47.0 installation was not recovered; findings about this current script must not be assigned retrospectively to that original installer.

CLI-H001: potential rollback/partial-replacement risk. Direct destination download and no explicit atomic swap/backup/rollback logic observed. Interrupted downloads, permission failures and preservation of prior installation are NOT tested.
Static script syntax parses successfully. Signature/hash verification indicators absent; these are observations, not passing security controls.

## Raw evidence and owner packet
evidence/2026-10-11/installer-audit/install-current.ps1: original downloaded current script.
baseline.json: timestamp, binary path/version/hash/size, signature output and installer hash.
static-results.json: parsed static indicators.
tests/sdk/audit_installer.ps1: repeatable non-executing audit.
Binary itself remains untouched at original installation path; hash identifies it but no archived binary copy was made.
Relevant source: installer configuration selects LOCALAPPDATA/guava/bin; Invoke-WebRequest writes directly to Dest; PATH is updated afterward.
Prior evidence files and original scaffold remain intact.

## Workarounds / recommendations
Proposed, untested: vendor signs Windows releases and verifies trusted publisher/signature plus authenticated expected hash before activation; download to staging and atomically replace after validation with prior-version recovery.
AEGIS interim practice: preserve exact hashes/version and avoid unattended upgrades until provenance policy is established. Hash alone is not proof of publisher identity.
No reinstall, PATH mutation, login/logout, deployment, purchase or destructive operation performed.

## Coverage and next task
SDK-001: CLI and SDK 0.47.0 now verified on this Windows environment; original scaffold still 0.47.1. Broader reproducibility/authentication not established.
SDK-002 PARTIAL: installed signature and current script inspection complete; original installer provenance, trusted expected release hash and behavioral enforcement remain unresolved.
SDK-013/014 NOT_RUN: isolated setup/permissions/failure/rollback experiments pending disposable environment.
Next: mocked installer failure-path tests and SDK event/callback contracts; no live installation failure injection on the existing setup.
