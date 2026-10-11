# Learning journal
Earlier entries: journal/learning-journal.md.
## 2026-10-11 — Coverage and layered testing
No SDK vulnerabilities have been independently confirmed; coverage areas are hypotheses until tested.
Learned: verification is a backend authorization decision, not field extraction. Payment redaction does not authorize access to billing data. Disconnect recovery requires idempotency and reconciliation to avoid duplicate transactions.
VAD/endpointing controls when speech is considered started/finished; ASR converts speech to text; TTS converts response text to audio. Their quality must be measured separately from business outcomes.
Next: exact-version baseline, then offline SDK contracts and documented live test capabilities. No security/behavior tests ran this milestone.
