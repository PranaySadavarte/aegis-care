# CLI-F001: Installed Windows CLI unsigned

## In plain language

The installed program has no publisher signature. Windows cannot use a signature to confirm who released this inspected file. We found no evidence of malware or tampering.

## Which test caught this?

**Case:** `SDK-002 / CLI artifact audit`

**Detector:** `Manual Get-AuthenticodeSignature on installed binary`

**Source:** `PowerShell artifact inspection`

**Relevant owner:** Guava release engineering

**Execution layer:** Artifact inspection; no binary execution

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#cli-f001)


The installed executable was observed as NotSigned in the prior Authenticode inspection.

[Installer audit and evidence provenance](../../sdk-evaluation/installer-audit-2026-10-11.md)

Expected owner behavior: publish a trusted digest/signing identity and enforce artifact verification before atomic replacement. This is a proposed solution, not an applied SDK or installer fix. Unsigned status is not evidence of malware. The originally used installer route/provenance remains unknown. Partial-download rollback evidence is documented in [CLI-X003](CLI-X003.md).
