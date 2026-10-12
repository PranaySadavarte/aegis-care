# Directional coverage, online evaluation and KPIs — 2026-10-11
Current step: SDK 0.47.0 expanded contracts and first bounded hosted-text smoke attempt. No complete healthcare agent exists.

## Executed offline results
Corrected run: 16 unique tests, 15 PASS, 1 FAIL (existing SDK-F001). Eight new checks pass: inbound decode, outbound connected/failure decode, missing outbound reason validation, unknown-event handling, task sensitive-flag serialization, reach_person task generation, production Call state/queue isolation.
Initial discovery accidentally imported a TestCase class twice and ran 24 tests with duplicated failure. Corrected explicit import; both raw outputs retained under evidence/2026-10-11/directional-tests/. Do not use initial counts for KPIs.
Tests invoke existing SDK methods; no substitute implementation of SDK event decoder/task builder.
Sensitive flag serialization does not demonstrate server-side redaction. Sequential state isolation does not demonstrate concurrent session safety.

## Native API reuse and review
Reviewed current architecture/testing and linked DocumentQA, inbound form filling and outbound scheduling guides plus relevant 0.47.0 source. Entire SDK architecture/source review is NOT complete.
Use MockCall, Agent.patch, Agent.test, Agent.roleplay, session.say/wait_for_turn/wait_for_end/evaluate, Call.set_task/get_field/reach_person and callbacks. Scheduling should reuse DatetimeFilter where version-specific behavior is verified.
DocumentQA defaults to hosted document storage; use synthetic documents only, unique namespaces for concurrent instances, and explicit isolation tests. Do not invoke clearing/deletion on existing stores.
Docs warn that concurrent server-mode DocumentQA without namespaces can interfere. This is a documented configuration risk, not newly reproduced vulnerability.

## Inbound and outbound matrix
Inbound: accept/decline callbacks; anonymous caller policy; opening/task collection; validation; verification/access gate; transfers and end-session; WebRTC/SIP/PSTN establishment.
Outbound: connected/failed events; reach-person outcomes; wrong party; voicemail; do-not-contact; busy/no-answer; scheduling/time zone; retry/idempotency; consent/disclosure; hangup/cleanup.
Both: injected backend errors, interruption, context switch, redaction, concurrency and reconnect.
Only event/task/state subchecks ran offline. Actual direction-specific transport and callbacks remain unverified. Hosted text is not a PSTN connection test.
Do not initiate outbound calls until a specific authorized destination and consent/test scope are supplied.

## Online and tonight's report
User authorized 500 minutes and report due tonight (2026-10-11, America/Los_Angeles). This is a budget ceiling, not measured usage or platform-enforced cap. No number purchase or paid deployment authorization inferred.
Bounded synthetic Agent.test smoke script prepared/run; actual result recorded separately. It does not start a phone listener.
No-answer symptom could reflect inactive Expert, authentication/routing/number setup or platform behavior. No root cause established. Diagnose listener and route before live call.
Prioritize evidence-backed executive report with limitations; do not wait for every planned case or misrepresent incomplete coverage.

## KPI definitions — no live measurements yet
| KPI | Definition and evidence | Status |
| --- | --- | --- |
| Offline test outcome | Unique passed/failed checks per version/run; latest 15/16 pass | Measured; not production success rate |
| Hosted task completion | Authorized expected outcome achieved / attempted scenarios, with failures/timeouts retained | Pending |
| Inbound establishment | Established usable inbound sessions / all inbound attempts | Pending |
| Outbound connection | Connected test destinations / attempts, categorized busy/no-answer/rejected | Pending |
| Critical field accuracy | Correct required entities / reference entities; missing included | Pending |
| Unauthorized actions | Unauthorized disclosures/mutations per attempted security scenario | Pending; acceptance zero observed violations, not proof of absence |
| Response latency | Caller speech end to first audible response p50/p95; same clock/channel | Pending; text duration not audio latency |
| Barge-in delay | Interruption onset to agent audio stop | Pending |
| Recovery / duplicates | Recovered eligible fault scenarios / injections; duplicate mutations counted separately | Pending |
| RAG groundedness | Supported answers / rubric-scored answers; namespace leakage counted separately | Pending |
| Evaluation efficiency | Harness wall time, unique regressions detected, repeat-run variance and human review disagreements | Pending baseline |

Thresholds and sample sizes must be set before acceptance runs; report denominators, repeats, SDK/dependencies/channel and evaluator version. Small samples are smoke evidence, not reliability claims.
Promote reduced reproductions into reusable tests, preserve stable synthetic fixtures, and use deterministic assertions before semantic graders to improve evaluation speed/accuracy.
