# Service flow and evaluation runner — 2026-10-11
## Entity names
AEGIS Care is the evaluation/project umbrella. HarborCare is its healthcare administrative agent/service persona. Neither is a separate real healthcare organization created by this project.

## Caller experience and current scope
Revised greeting: HarborCare, brief sample-record disclosure, natural coverage/claims/appointment/account help. Results are now readable service responses rather than JSON/test instructions.
Still a synthetic prototype: public fixture credentials, in-memory data, one workflow per call, no real health/insurance/payment integrations; appointment reschedule/cancel and full adversarial/audio/outbound coverage incomplete.
set_task drives verification, selection, booking and payment; on_task_complete enforces backend actions. on_question is registered for administrative/safety fallback questions. It is not a document-grounded FAQ implementation.
Native SDK testing used: MockCall, Agent.patch in SDK contracts, Agent.test/TestSession utterances and assertions, and now TestSession.evaluate for a hosted rubric. roleplay and test_audio remain available but not exercised for this milestone.

## What runs after each call
Expert finish events automatically receive limited deterministic metadata evaluation: data-returning results require verified session; denial/rejection recorded separately; semantic/ASR explicitly NOT_EVALUATED/NOT_MEASURED.
Ended-without-result events are INCONCLUSIVE. These checks do not establish transcript safety, medical correctness or audio quality; denial is not automatically a failed call.
Full regression suite runs on demand, not after every call. Per-call events have appeared for an observed simulated payment with authorization check PASS; this is a scoped metadata observation only.

## Executed results
Latest functional suite: 17 methods PASS, including evaluator and journal tests; workflow subcases are not extra independent method counts.
Dashboard-triggered offline run: SDK 16 tests / 15 PASS / 1 known FAIL; application 17/17 PASS; static installer audit OPEN_FINDINGS for absent explicit hash/signature checks. Static audit findings are not miscounted as unit failures.
Revised service hosted suite: six happy workflows PASS; malformed text-code denial expected backend result but returned no outcome (FAIL retained). Transcript was not captured before that initial failed assertion, so exact cause unverified.
Changed denial fixture to valid-format wrong code 4243 and reran: PASS. Malformed-code/early termination remains a robustness observation needing follow-up, not a proven authorization bypass.
Separate native semantic billing test PASS: Agent.test outcome assertion plus TestSession.evaluate greeting/no-real-card/no-real-charge criteria. Rubric results are semantic judgments, not BERTScore/ROUGE/calibrated confidence.
Hosted harness now saves transcript observations before assertions. Future hosted suite includes native rubric billing group.
Raw run summaries and outputs: evidence/2026-10-11/suite-runs/<run_id>/; current/status history exposed as sanitized dashboard JSON. Hosted process cap 50s per group; no server billing cap inferred.
Existing installer/exception vulnerabilities/control gaps remain unresolved.

## Dashboard and CLI
Calls page: dashboard/calls.html — native history plus scoped local observations, refreshed on demand.
Test runs: dashboard/runs.html — fixed suite selector, execution and run history. Cross-origin POST rejected (403); no arbitrary command or path accepted.
Offline includes SDK, application and existing static installer audit. Hosted includes seven workflow/denial scenarios and native billing rubric. All combines these executable suites; unimplemented catalog scenarios are not silently covered.
CLI:
baseline/sdk-0.47.0/.venv/Scripts/python.exe tests/run_all.py --suite offline
baseline/sdk-0.47.0/.venv/Scripts/python.exe tests/run_all.py --suite hosted
baseline/sdk-0.47.0/.venv/Scripts/python.exe tests/run_all.py --suite all
Hosted/all consume authorized live usage. No outbound dialing, purchases or deployment from runner.
No full nightly automation created. Frontend polling reads status only; it does not repeatedly launch suites.

## Next work
Investigate malformed verification/early hangup; add expected scenario labels per manual call; exercise native roleplay/rubrics on adversarial cases; acquire labeled synthetic audio for WER/CER, latency and interruption metrics. Broad catalog and production service readiness remain incomplete.
