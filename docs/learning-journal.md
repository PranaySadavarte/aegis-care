# Learning journal
Earlier entries: journal/learning-journal.md.
## 2026-10-11 — Coverage and layered testing
No SDK vulnerabilities have been independently confirmed; coverage areas are hypotheses until tested.
Learned: verification is a backend authorization decision, not field extraction. Payment redaction does not authorize access to billing data. Disconnect recovery requires idempotency and reconciliation to avoid duplicate transactions.
VAD/endpointing controls when speech is considered started/finished; ASR converts speech to text; TTS converts response text to audio. Their quality must be measured separately from business outcomes.
Next: exact-version baseline, then offline SDK contracts and documented live test capabilities. No security/behavior tests ran this milestone.

## 2026-10-11 — First executed SDK contracts
Established exact SDK 0.47.0 environment using working bundled Python 3.12.14; executed eight offline tests (seven passes, one failure).
Learned: MockCall isolates handler state but does not emulate server authorization or lifecycle. Agent.patch copies callback maps without changing the original. The Client constructor can perform a deprecation request; offline tests must prevent network side effects.
An exception is a data sink: HTTP response content may become exception text and later logs or telemetry. Reproducing synthetic marker inclusion confirms that behavior, but not an actual production breach.
Official agent-testing guide separates offline MockCall from live scripted/roleplay sessions. Next extend mock-backed SDK fault/security tests and complete CLI identification.
