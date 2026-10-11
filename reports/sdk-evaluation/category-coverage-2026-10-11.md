# SDK evaluation category coverage — 2026-10-11
Current step: SDK evaluation; isolated 0.47.0 offline baseline only. Overall CLI/SDK baseline is incomplete.

## Why installer checks were not executed
SDK-002 already listed checksum/signature/installer inspection, but no installer executable test was implemented or run. Work advanced to inexpensive offline Python contracts after CLI discovery failed. This was a sequencing and reporting gap: inability to locate the binary did not prevent designing the remaining installation checks or inspecting a separately retrieved current installer. Current installer evidence must not be presented as the original 0.47.0 installer.
Corrective action: prioritize CLI/artifact discovery and non-executing installer inspection next; do not treat seven passing offline checks as complete SDK evaluation.

## Eight-category coverage
| Category | Existing coverage | Actually executed | Missing / next coverage |
| --- | --- | --- | --- |
| Installation | SDK-001/002/011 | Isolated SDK install/import and version; dependency inventory; CLI discovery attempt | Installer checksum enforcement, Authenticode status/enforcement, Windows PATH/setup, permissions, interrupted install and rollback; SDK-013/014 |
| Developer experience | Broad earlier plan only | Launcher/auth-related source inspection and documented errors; no measured DX evaluation | Time to first call, docs accuracy/usability, actionable errors; SDK-015 |
| Functional API | SDK-007/008/009 | MockCall fields/variables/queues and patch independence | Task commands, event decoding/dispatch, validation, production state transitions; SDK-016 |
| Security | SDK-002 through 006/009/011 | Dummy auth repr and HTTP response exception check; mock isolation | Installer, key/log/telemetry sinks, hosted authorization, TLS, isolation; existing cases remain incomplete |
| Error handling | SDK-007/008/010 | Non-JSON variable rejection and HTTP response success/failure | Event faults, callbacks, timeout and connection loss; existing cases NOT_RUN or partial |
| Testability | MockCall tests and layered strategy | Deterministic mock contracts | Live scripted/roleplay sessions, assertion reliability and harness limitations; SDK-017 |
| Compatibility | SDK-001/012 | One Windows Python 3.12.14 SDK 0.47.0 configuration | 0.47.1 comparison, supported Python versions, Linux/macOS; SDK-018 and SDK-012 |
| Deployment | Broad earlier plan only | Configuration file inspection only | Config validation, isolation, startup/shutdown and health probes; SDK-019/020 |

All eight categories were recognized conceptually, but developer experience and deployment lacked dedicated detailed cases. Installation was represented too narrowly. These gaps are now explicit and additional cases have been added. No category is fully validated.

## Installer acceptance and evidence
Separate four observations: installer computes any hash; installer compares it with a trusted expected hash; binary signature is present/valid; installer verifies/enforces publisher/signature policy. None implies the others.
Collect exact installer source URL/date/hash and executable version/hash/signature output. A hash comparison is meaningful only when the expected value has trustworthy provenance.
Inspect source without executing installation. Failure-path and rollback tests belong in an isolated disposable environment, with before/after files, PATH, permissions and exit codes recorded. Do not damage or uninstall the user's existing setup.
Missing checksum enforcement or an unsigned binary is a confirmed control gap only after evidence; exploitability and impact need separate assessment.

## Next execution order
1. Locate existing CLI and original installer/evidence; query version and Authenticode without exposing auth config.
2. Retrieve official installer as a separately dated artifact; inspect trusted-hash and signature checks without running it.
3. Execute isolated installation/permissions/rollback tests when a disposable environment is available.
4. Expand production SDK task/event/error contracts, then hosted tests with clear resource/billing boundaries.
No new behavior tests ran for this coverage correction. Previous result remains eight tests, seven passes, one failure.
