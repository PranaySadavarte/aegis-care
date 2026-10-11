# Security and SDK coverage audit — 2026-10-11
## 1. Current step
SDK evaluation: scaffold audited; version/runtime baseline blocked; security test design now documented. Voice agent implementation and live-call evaluation have not begun.

## 2. Vulnerabilities and potential issues
No independently confirmed vulnerabilities. QA-007 installer signature/integrity concerns are historical user reports awaiting artifacts. QA-005 unrestricted demo logs are a potential application privacy risk. Version mismatch and launcher/PATH failures are observed evaluation blockers, not security vulnerabilities.
Before this milestone there were broad plans but no detailed test-case catalog or executable tests. tests/ placeholders added here do not constitute automation.
A finite test suite cannot establish that all possible vulnerabilities are absent. Coverage is scoped to listed threat areas, versions and tested interfaces.

## 3. Actual versus expected
Expected: version-specific, reproducible SDK security checks before application troubleshooting.
Actual: target 0.47.0 differs from installed/locked 0.47.1; Python and CLI checks are blocked. Auth, transport, isolation, error handling and installer security remain untested.
Expected: separate cheap workflow checks from real voice tests.
Actual: layered strategy and detailed cases now exist; none have executed.

## 4. Test plan
See reports/test-plans/layered-evaluation.md and test-cases.csv. Cases include installer provenance, key handling, API authorization, transport security, malformed events, callback errors, session isolation, retries, dependency assessment, healthcare authorization and live audio/telephony.
Every case specifies setup, steps, stable expected outcome, owner, evidence and workaround. Initial status is NOT_RUN; dependencies must be met before execution.
Do not treat current docs as proof of historical 0.47.0 behavior. Verify APIs against current official documentation and version-specific source before writing a harness.

## 5. Findings and evidence
Reviewed tracked repository and existing reports; no pre-existing test suite found.
Notes source: C:/Guava/My notes.rtf; original left unchanged. RTF body content was reviewed using a lossy text preview; this is not an authoritative conversion of embedded objects or full formatting.
Notes' positive call observations, compliance statements and installer claims are user reference observations, not reproduced results. No compliance certification conclusions are drawn.
Existing raw documentation snapshot/hash manifest retained unchanged. Notes hash collection was attempted but blocked because another process holds the file. No notes hash was obtained.

## 6. Problem statement, owners and workarounds
Problem: no executed security baseline means subsequent healthcare failures could be misattributed to SDK/platform.
Owner: AEGIS project for harness/application and environment; Guava only for reproduced vendor issues.
Workaround: preserve current scaffold, establish isolated exact-version baseline, execute SDK checks first, and use minimal reproductions for vendor suspects.
Live behavior comparison is unavailable: no AEGIS call has been evaluated. Each future finding must compare actual recorded behavior with its stated acceptance condition and show whether a workaround was tested or only proposed.

