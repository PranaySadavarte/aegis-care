# CLI-F002: Installer verification controls absent

Current official installer source has no explicit downloaded-binary checksum comparison or Authenticode check. Neither control has been fixed.

[Installer audit and evidence provenance](../../sdk-evaluation/installer-audit-2026-10-11.md)

Expected owner behavior: publish a trusted digest/signing identity and enforce artifact verification before atomic replacement. This is a proposed solution, not an applied SDK or installer fix. Unsigned status is not evidence of malware. The originally used installer route/provenance remains unknown. Partial-download rollback evidence is documented in [CLI-X003](CLI-X003.md).
