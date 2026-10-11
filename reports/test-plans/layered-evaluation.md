# Layered evaluation and release gates
## Sequence
1. SDK baseline/security and architecture study before custom application implementation.
2. Deterministic business logic and synthetic API contract tests.
3. Text conversation tests for task state, field extraction, tool calls and authorization.
4. Prerecorded audio with reference transcripts and controlled noise/accent/speech variants.
5. WebRTC then SIP/PSTN end-to-end sessions on authorized resources.
6. Final user-led exploratory calls against the complete synthetic HarborCare agent; then a small canary plan if production use is separately approved.

## SDK gate
Verify exact versions and functioning interpreter; review installer provenance; map auth/transport, callbacks, commands, state and testing API; execute catalog SDK cases. Any critical unresolved auth/isolation/data leakage issue blocks sensitive workflows. Record scoped exceptions and residual risk rather than asserting complete security.
Tests requiring hosted services remain gated by authorization/resources; offline mocks cannot establish hosted authorization or TLS behavior.

## Assertion design
Assert completed tasks, extracted field values, authorized actions, backend mutations and safety constraints. Do not match exact generated prose. Semantic grading should retain criteria, evaluator/version and human review for ambiguous failures. Run conversation repetitions and report denominator and variance, not only best examples.

## Audio and reliability metrics
Measure reference-based ASR word error rate and critical entity accuracy separately; correct words alone do not prove successful transactions.
Measure speech-end-to-first-response-audio latency (p50/p95), interruption stop delay, call establishment/completion rate, task completion and failure categories. Record clocks, channel, codec, network conditions, noise level and dataset provenance.
Set numeric acceptance thresholds before execution after a measured baseline and stakeholder decision; currently no performance threshold or result is approved.

## Final live-call checklist
Use synthetic identity/insurance/billing scenarios and simulated payments only. Test happy paths plus incorrect identity, identity switch, prompt injection, interrupted disclosure, echo/noise, accents, silence, overlapping speech, repeated booking/payment request and disconnect recovery.
For each call log case ID, channel/version, consent/recording choice, timestamp, redacted session ID, expected outcome, transcript/audio location if collected, backend action trace and actual result. Reproduce discovered issues in text or mocks where possible; keep audio reproduction when failure is acoustic/transport-related.
Do not capture real payment credentials. Never infer authorization from caller ID or successful field collection.
Purchases, paid deployments, destructive actions and production canaries require explicit approval.

## Evidence and reporting
Statuses: NOT_RUN, BLOCKED, PASS, FAIL, INCONCLUSIVE. An attempted check that never executes is BLOCKED.
Findings: confirmed vulnerability, observed defect, potential risk, hypothesis, or unverified historical report.
Report step, problem, expected/actual, test case/run, finding, impact/confidence, owner evidence and proposed/tested workaround.
Keep raw originals locally separate from sanitized sharing copies; record hashes and redact credentials, sensitive identifiers and transcripts. Do not overwrite prior evidence.
