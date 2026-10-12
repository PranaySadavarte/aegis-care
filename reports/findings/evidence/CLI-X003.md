# CLI-X003: Interrupted destination download loses prior binary in fault probe

**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** Interrupted destination download loses prior binary in fault probe. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** Installation / supply chain. **Owner category:** Guava SDK / installer.

**Problem:** Interrupted destination download loses prior binary in fault probe

**Expected:** Preserve prior artifact until successful verified replacement.

**Actual:** Real installer control flow with mocked partial download overwrote a synthetic prior file; no rollback occurred. PATH and real install unchanged.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/installer-partial-write-f3a5f7884683447da8c9e2015383a69c/result.json`; SHA-256: `734ff4529538d4e0bbf55226bec8e6d032c906fafa8f5856b0e6e1fa5b53c717`.

```text
{
  "mode": "partial-write",
  "version": "0.47.0",
  "installer_sha256": "55D89800714FCE05FF4CD40946F705A24B214E73D409437E37FBE9CFE96A3502",
  "prior_file_preserved": false,
  "user_path_unchanged": true,
  "fault": "AEGIS synthetic download fault; no network, no binary execution",
  "scope": "Current official installer control flow with mocked download failure; synthetic destination only; original install untouched"
}
```

**Proposed owner action / workaround (not applied):** Use a staged/verified atomic replacement design; this is a proposed owner solution, not an applied fix.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
