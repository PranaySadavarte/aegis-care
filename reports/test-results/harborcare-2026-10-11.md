# HarborCare prototype results — 2026-10-11
Current step: application implementation and initial functional/hosted text evaluation.
SDK 0.47.0 on Windows/Python 3.12.14. Original harborcare-agent scaffold preserved.
Native APIs used: Agent, on_call_start, on_task_complete, on_question, on_session_end, Field, Say, set_task, get_field, set_variable, hangup, MockCall and Agent.test.

## Implemented scope
Synthetic ID/code verification; eligibility lookup; claims status; billing balance; appointment booking; consented simulated payments.
Backend authorizes each read/mutation by session subject; unsuccessful re-verification clears authorization. Booking/payment mutations guarded by process lock; repeated same payment key returns previous result.
One workflow per call; no real medical advice, clinical decisions, payment/card collection or integrations. Demo codes are public fixtures, not strong identity proof.
Process-memory data only: booking/payment state resets at restart and is not shared across replicas. Durable reconciliation, production auth/rate limits, cancellation/rescheduling and comprehensive disclosure/adversarial handling are NOT implemented.
Outbound scheduling/phone direction coverage remains planned; the prototype currently uses inbound start flow and hosted text sessions.

## Executed tests and actual behavior
7 backend test methods passed: unauthorized reads, verified reads, failed identity switch, booking conflict/repeat, payment idempotency, payment authorization/consent/amount, cleanup.
Corrected combined functional run: 10 methods PASS, including one method with six workflow-handler subcases. Do not count subcases as independent method totals.
Initial handler test wrongly assumed claims response was a dict, producing a test-harness AttributeError. Corrected to assert list contents; initial and corrected outputs preserved. No application defect established by that error.
Hosted text: six workflows individually PASS with expected result and bot-hangup asserted. Durations are process wall time, not audio latency:
identity 12.766 s; eligibility 29.343 s; claims 30.703 s; billing 12.329 s; appointments 15.359 s; payments 15.406 s.
Live wrong-code case: corrected run PASS, denial and bot-hangup asserted; process 9.406 s.
Initial wrong-code harness mistakenly waited for a subsequent turn after expected hangup and raised ConnectionClosedOK. Fixed branching; retain initial attempt separately. This is a harness sequencing error, not proof of SDK/agent failure.
Corrected hosted scenarios 7/7; initial harness errors retained, not included as unique failed agent scenarios. Sample too small for reliability claims.
Raw outputs/transcripts: evidence/2026-10-11/harborcare/. Synthetic only. Dashboard embeds outcomes, not transcripts.

## Phone status / blocked action
Attempted to launch phone listener, but automatic approval review rejected the action before execution: attaching to configured number could alter live/shared routing; exact listener side effect had not been explicitly approved.
No phone listener started and no live phone/audio result claimed. Explicit approval question pending. No purchase or deployment.
Expected phone readiness after approval: listener registers successfully, user makes synthetic call, capture route/call result. Current no-answer root cause remains unknown.

## Metric and stage coverage
Catalog now has PipelineStage and Direction labels. ASR, LLM and robustness dashboard pages specify metric readiness; numeric values not measured are not fabricated.
Native testing/audio/rubric API review: docs/native-metrics-review.md. Full SDK review still incomplete. No new CER/WER/RTF/confidence/BERT/ROUGE metric implementation; reuse established libraries if needed.
Next: approved listener + user call; audio dataset and event timing instrumentation; adversarial verification/injection; persisted transaction backend if broader prototype needed.

## Findings / recommendations
No new confirmed SDK vulnerabilities in this milestone. Existing response-body and installer issues unresolved.
Application limitations: public synthetic codes, in-memory persistence, one-workflow calls and untested adversarial/acoustic behavior. Owner AEGIS application.
Workarounds: remain synthetic-only; evaluate each boundary before production. Do not call this release-ready healthcare software.

Dashboard QA: updated overview served HTTP 200; ASR page served HTTP 200; pipeline ASR filter returned 2/32 catalog cases; ASR navigation verified in browser. Preview required restart because the prior local server was unavailable. Metric pages contain readiness definitions, not measured scores.
