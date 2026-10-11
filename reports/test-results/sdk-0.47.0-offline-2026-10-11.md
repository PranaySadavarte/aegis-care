# SDK 0.47.0 baseline and offline results — 2026-10-11
## Current step
SDK evaluation: isolated Python SDK baseline operational; CLI baseline unresolved. Healthcare implementation not started.

## Baseline
Windows; CPython 3.12.14 from bundled runtime; isolated baseline/sdk-0.47.0/.venv.
guava-sdk 0.47.0 successfully imported and exact version asserted.
requirements.lock.txt is a frozen installed-version inventory, not a hash-verified resolver lock. Transitive dependencies reflect the present index, not Guava's original release environment.
Original harborcare-agent and its 0.47.1 dependency lock retained unchanged.
CLI is unresolved on PATH. Searches in common locations and a recursive user-directory search yielded no executable output; search exited 1, so this does NOT establish that the CLI is absent from the machine. No reinstall or authentication changes performed.
Python virtual environments created by uv need not include pip; pip --version reported missing pip. uv handles package management; this is not an SDK defect.

## Official documentation
Retrieved current https://goguava.ai/docs/agent-testing.md and architecture-overview.md; snapshots under evidence/2026-10-11/sdk-baseline/.
MockCall supports offline handler tests. agent.test() connects to a live service; roleplay invokes hosted conversation/evaluation capabilities. Neither was run.
Current docs are not proof of every historical release contract; inspected installed 0.47.0 implementations before tests.

## Executed tests
Command: baseline/sdk-0.47.0/.venv/Scripts/python.exe -m unittest discover -s tests/sdk -p "test_*.py" -v
8 tests executed, 7 PASS, 1 FAIL; process exit 1.
PASS: exact SDK version, MockCall field/variable isolation, invalid non-JSON variable rejection without state/queue mutation, MockCall command queue isolation, Agent.patch handler independence, dummy API-key repr not exposing key, successful HTTP response preservation.
FAIL: SDK HTTP error exception includes synthetic sensitive response-body marker.
Raw output: evidence/2026-10-11/sdk-baseline/offline-test-output.txt. Test code: tests/sdk/test_offline_contracts.py.
No xfail or skipped test disguises the failure. No live credentials used.
Network socket connections blocked before SDK import; Client construction mocked for Agent.patch; telemetry send_event disabled for offline contracts.
MockCall tests do not verify production Call lifecycle, concurrent dispatch, ended-session enforcement or server isolation. API-key repr check does not prove all log sinks are safe.

## Finding SDK-F001
Classification: confirmed SDK exception-content behavior; potential privacy/security disclosure risk, not demonstrated real-world data exfiltration.
Owner: Guava Python SDK error handling; AEGIS application owns downstream logging policy.
Problem: check_response includes complete response body and URL in HTTPStatusError text. Responses containing sensitive values can propagate into exceptions/logs.
Expected: AEGIS security acceptance criterion requires sensitive response values excluded from exception text. This criterion is a project safety requirement, not a claim that Guava documentation promises redaction.
Actual: synthetic marker appears in exception message for local fabricated 401 response.
Evidence: failed test and installed guava/utils.py check_response implementation. No network request involved.
Proposed vendor solution: omit/redact body and sensitive URL components by default; offer explicit bounded diagnostic handling.
Proposed app workaround: intercept status errors at boundary; log only safe status/correlation metadata and generic user messages. Workaround NOT implemented or tested. SDK telemetry also formats exceptions with repr(e); end-to-end upload/redaction implications remain untested.
No severity assigned without impact/reachability assessment.

## Remaining coverage
SDK-001 PARTIAL: SDK verified, CLI unresolved.
SDK-003 PARTIAL/FAIL subcheck: exception-body disclosure reproduced; log/telemetry sink coverage incomplete.
SDK-007 PARTIAL: one non-JSON variable case only.
SDK-009 PARTIAL: sequential MockCall isolation only.
Other catalog cases NOT_RUN. Installer, auth rejection, cross-org access, TLS, malformed events, callback faults/timeouts, reconnect/replay, advisories and other platforms remain unverified.
Next: expand offline production Call/event and callback tests, inspect error/telemetry redaction paths with mocked sinks, and locate CLI. Hosted tests require separately confirmed resource/billing boundaries before execution.
